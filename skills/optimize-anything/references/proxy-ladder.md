# Proxy ladder

Field metrics are what users feel. They are noisy, tail-heavy, and too flaky to gate CI.
Every row below is a count or an exact timing that stands in for a field metric, and how
to produce it. Take the cheapest row that moves, and prefer the top of the ladder:
exact counts beat structural counts, and both beat wall clock.

## Determinism checklist

A count is only worth a ratchet if it repeats. Before trusting one:

- Check the input fixture into the repo. A benchmark that generates its own data measures
  the generator.
- Fix the seed, the worker or concurrency count, and the clock. Node: `--predictable`.
- No network. Stub time, randomness, and the clock, or the count drifts.
- Say warm or cold explicitly, and measure the one you care about. Cold start and steady
  state are different targets with different fixes.
- Report per unit (per request, per render, per 1k rows), so the number survives changes
  in workload size.
- Report the field metric next to the proxy every time. Two numbers from one run is the
  only way correlation ever gets checked.

## Web and client runtime

Field: p75 time to a usable, typeable page; interaction latency; frame smoothness.

| Proxy | How |
| --- | --- |
| Retired instructions on a JS hot path | `node --predictable` under Valgrind/callgrind, compare the `Ir` count to a checked-in baseline. One run, no statistics. |
| Function call counts | V8 precise coverage: `NODE_V8_COVERAGE` in Node, DevTools coverage in the browser. |
| React commits per interaction | React `<Profiler onRender>`, or the DevTools profiler commit count for a scripted interaction. |
| Layout and style recalc counts | CDP `Performance.getMetrics`: `LayoutCount`, `RecalcStyleCount` and their durations. |
| DOM mutations | `MutationObserver` in a driven page, or CDP DOM events. |
| Transferred and parsed bytes | Build stats plus gzip/brotli size of the entry and its chunks. |
| Requests, and bytes per journey | HAR capture, diffed per journey. |
| Encoding class of hot strings | Count strings containing non-Latin-1 characters. Any of them can move a whole hot path onto the two-byte path and slow every regex that touches it. |

## Frame-exact timing

When smoothness is the target, do not sample frame times. Step them.

Drive headless Chrome with CDP begin-frame control at a fixed refresh rate, one
`beginFrame` per frame, and time each one. At 120 Hz the budget is 8.33 ms per frame and
"did this frame fit" becomes an exact read instead of a noisy one. A frame-over-budget
counter on a fixed fixture is an excellent nightly ratchet. This is how per-frame work
became countable, and counting it turned an unplanned sidequest into the smoothest
change in the sprint.

## Node and server

Field: p50/p95/p99 latency per route; throughput at concurrency; memory per request.

| Proxy | How |
| --- | --- |
| Retired instructions per request | `node --predictable` under callgrind on the request path. |
| Queries per request | Instrument the driver and assert the count. Exact, and catches N+1 that latency hides behind a warm cache. |
| Rows examined vs rows returned | `EXPLAIN (ANALYZE, BUFFERS)`. The gap is the bug. |
| Allocations per request | `perf stat` allocations, or `--trace-gc` totals for a fixed request count. |
| Lock and contention waits | `perf stat` futex/context-switch counts; a rising number here is a queue forming. |
| Load shape | `k6`, `vegeta`, `hey` or `autocannon` at fixed rate, fixed duration, p95 reported. Noisy but reproducible enough for a trend, not for a PR gate. |

## Database

Field: query latency under real traffic; database size; replication lag.

| Proxy | How |
| --- | --- |
| Rows examined, buffers read | `EXPLAIN (ANALYZE, BUFFERS)`, `pg_stat_statements` for the top offenders. |
| Index scans vs sequential scans | `pg_stat_user_indexes`, `EXPLAIN` plan shape diff. |
| Table and index bytes | `pg_total_relation_size` summed. Deterministic to the page. |
| Dead tuples and table bloat | `n_dead_tup` from `pg_stat_user_tables`. |
| WAL volume per unit of work | `pg_stat_wal` deltas around a fixed workload. |

A plan-shape diff belongs in CI next to the latency ratchet: it fails on a regression
that a benchmark on your machine would not reproduce.

## Build, test, and CI

Field: wall clock on a developer machine and on CI.

| Proxy | How |
| --- | --- |
| Files read, module count, transform calls | Build tool stats (`vite --debug`, webpack stats, `esbuild --metafile`). |
| Total collected test count | `vitest --reporter=json`, `jest --listTests`, `pytest --collect-only`. Growth here is the leading cause of slow suites. |
| Slowest tests and their share | `pytest --durations=0`, per-test timings from the JSON reporter. A fix is to delete or merge, not to parallelize harder. |
| Cache hit ratio | Count hits and misses explicitly. |
| Test count actually executed vs expected | Catches the suite that silently stopped running something. |

Wall clock is worth a coarse gate with a generous tolerance, but never the primary one.

## Cloud spend

Field: dollars per month, dollars per request.

Cost is the sum of exactly countable things, so it ratchets cleanly. Bytes egressed,
requests, provisioned capacity, idle reservations, origin cache misses, log and metric
volume, storage class tiers, snapshot count, idle CPU credits. A dollar figure in CI is
usually a derived number: assert the drivers, not the total, and let finance do the
multiplying.

## LLM and AI systems

Field: cost and latency per successful task, not per request.

| Proxy | How |
| --- | --- |
| Input and output tokens | Provider usage metadata on every response. Exact. |
| Cache hit ratio | Cached vs fresh input token counts. |
| Prompt cacheable prefix share | Hash the stable prefix of the prompt. The cacheable share is a percentage you can ratchet directly. |
| Tool-call round trips per task | Count turns. Usually the largest single lever on both cost and latency. |
| Context re-sends | Bytes and tokens resent after a retry or a compaction. |
| Time to first token, p75 | Streaming timestamps. |
| Retries and fallbacks per task | Retry amplification is invisible in the request count and expensive in every other unit. |

The target is cost per successful task, so hold the success rate fixed or the optimization
is fake.

## Mobile and native

Field: cold start to first meaningful paint, frame rate during interaction, jank count,
energy per session.

| Proxy | How |
| --- | --- |
| Main-thread or UI-thread work per frame | Perfetto, `xctrace`, `dumpsys gfxinfo`. The per-frame total is the number, not the average FPS. |
| Frames over budget | Counter per interaction on a scripted flow. Deterministic. |
| Bridge crossings and worklet runs | Per interaction count. High counts are a design smell you can count. |
| View count and view hierarchy depth | Static, exact, ratchets cleanly. |
| Bundle parse time and module init count | Count the modules, then the parse. |
| Image bytes decoded, and decode count | Per screen. |
| Energy per session | `dumpsys batterystats` on Android, `powermetrics` on macOS, MetricKit on iOS. |
| Wakelocks and background wakeups per hour | `dumpsys batterystats`. A background task waking the device is a battery bug you can count. |

## Memory and footprint

Field: RSS in production; heap after GC under a fixed workload.

| Proxy | How |
| --- | --- |
| Heap used after a forced GC | Fixed workload, then `global.gc()` and read the heap. Exact and comparable. |
| Object count and retained size | Heap snapshot diff between two runs. |
| Allocations per operation | Count, do not judge by RSS. RSS moves for reasons that are not yours. |
| Buffer and cache pool size | Config values, trivially ratcheted. |
| Binary, image, and asset bytes | Build output. Exact. |
| Peak memory in a fixed scenario | A test that fails over a threshold. |

Steady state after GC is the ratchet. Peak is a symptom metric and much harder to hold.

## Reliability

Field: error rate and retry rate per journey; time to detect; time to recover.

| Proxy | How |
| --- | --- |
| Retries per user action | Retry amplification factor. One user action should produce one attempt. |
| Uncovered error paths | Count of paths reachable without a test asserting them. Goes down as tests go in. |
| Timeouts and their budget | Count and total budget consumed per request. |
| Queue depth at failure | Depth and drain time in a fault-injection test. |
| Retained compatibility and fallback branches | Count of live fallback paths. A declining number is a leading indicator of reliability. |

## Worked example: the whole ladder in one bug

Symptom: highlighting a finished code block froze the page for about a second. No load
metric moved, no CLS entry fired, no field monitor caught it.

1. A human supplied a screen recording. That is the artifact the workstream starts from.
2. The lab metric became a script that renders a reply and times to interactive.
3. Profiling pointed at the highlighting regexes, and the count that moved was not
   instructions or time but the string encoding class: one non-Latin-1 character anywhere
   in the reply pushed the whole string onto the runtime's two-byte path.
4. Twenty lines to copy each code block into a one-byte string before highlighting.
5. A new ratchet: hot-path strings are asserted Latin-1 clean.

Nobody would have predicted the cause, and none of the existing monitors could have
found it. The recording and a benchmark were the only reason it was visible at all.
