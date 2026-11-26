# Measurement traps, bounds, and qualification

Use this reference for bounds, bracketed server runs, measurement errors, and clean-build qualification.

## Practical bounds and limits

Measure the host rate on the target machine. State the rate and any assumed efficiency separately. A measured copy or compute rate gives a practical estimate. To prove a physical limit, use a verified upper rate limit and a minimum amount of unavoidable work.

Write units on both sides of every equation. Never declare a user target impossible unless you prove unavoidable work exceeds the hard physical bound.

- **Memory-bandwidth bound** (scans, serialization, LLM decode): measure large buffer copy bandwidth (`B_bw` in GB/s). Sum unavoidable bytes transferred per unit (`B_unit` in GB/unit) from real files or checkpoint tensors.
  - Estimated latency floor: `B_unit / B_bw` (seconds per unit).
  - Estimated throughput ceiling: `B_bw / B_unit` (units per second).

- **Compute bound** (codecs, renderers, LLM prefill): measure sustained peak throughput (`F_peak` in ops/s) on a large workload so thermal clock drop appears. Sum unavoidable ops per unit (`F_unit` in ops/unit).
  - Estimated latency floor: `F_unit / F_peak` (seconds per unit).
  - Practical throughput ceiling at efficiency `eta` (for example, `eta = 0.5`): `(eta * F_peak) / F_unit` (units per second).

- **Startup and I/O floor**: Divide the required GB by the measured GB/s for the disk or page cache. Add the measured runtime initialization time in seconds. Use the cache state that the journey specifies.

- **Capacity ceiling** (memory-capped concurrency): `floor((cap_bytes - fixed_base_bytes - runtime_bytes - headroom_bytes) / bytes_per_stream)` (streams). Keep host headroom (at least 1 to 2 GiB on desktop or unified-memory hosts) so the OS does not livelock.

- **Stage-time bound**: when hardware throughput does not explain the journey (for example, network RTT or a serial RPC), sum the measured durations of the unavoidable stages from the profile.

### LLM and inference server bounds (when applicable)

Use this section only when the target is a model server and your profile confirms the limiter.

- **Decode throughput ceiling (tok/s)**: divide measured device bandwidth (GB/s) by bytes read per emitted token (GB/tok). For each target step, count reads of dense weights, active experts, and the LM head. Estimate active experts as `expert_gb * top_k / n_experts`. Add KV reads at the target context length and hybrid SSM state reads and writes. For speculative decode (`k` drafts, mean accepted tokens `a`), use `(verify_gb + draft_gb) / a`, where verify reads the union of routed experts across `k + 1` tokens.

- **Prefill throughput ceiling (tok/s)**: divide `eta * measured_gemm_flops` (FLOP/s) by FLOP/tok (`2 * active_params` plus attention FLOP/tok at mean position `L / 2`).

- **Speculative decode rule**: measure per-step time (`s/step`) and accepted tokens (`tok/step`) separately because `tok/s = accepted / step_time`. Sweep draft length per concurrency and per context length.

- **Common server levers (apply only when supported by the profile)**:
  1. Persist compile, JIT, autotune, and graph caches (and check eager weight load if mmap is slow).
  2. Enable decode graph capture when launch overhead dominates step time.
  3. Tune speculative decode (prune draft LM head vocabulary, sample tokens on the GPU, use decode-style verify attention).
  4. Size concurrency, KV pool, and hybrid state slots for `N * context`, and verify prefix cache hits (`cached_tokens > 0`).
  5. Tune prefill chunk size, attention library, and labelled lossy precision trades when prefill compute dominates.
  6. Tune kernel tiles or threads for the target hardware, then edit kernels only after config levers plateau.

## Noise control, bracketed runs, and process safety

Run-to-run variation and thermal drift come from clocks, power profiles, battery state, and host CPU load. Use the journey's A/A results to estimate noise.

- **Interleaved blocks versus server brackets.** Use `scripts/bench.py` counterbalanced blocks (`A B`, `B A`) for fast commands. When startup or restart prevents per-run interleaves (for example, large containers or servers), run repeated independent brackets (`control`, `candidate`, `control` repeated at least 3 times). Compute each bracket's change against the mean of its two controls. If the controls drift beyond the A/A tolerance, invalidate the bracket. Set the sample count, margin, and uncertainty rule before the run. Treat each whole bracket as one observation. Keep only if the interval clears the margin.

- **Warmup and cache state.** Validate warmups and label cold runs separately from warm cache-hit runs. Isolate or explicitly precondition shared caches so side A never warms a cache that only benefits side B.

- **Memory use on unified memory and GPUs.** Built-in `tree_rss` sums process-tree RSS in MiB every 10 ms. It can double-count shared pages, miss brief peaks, and miss GPU or driver residency on unified-memory laptops and discrete GPUs. Pass `--mem-probe` to `scripts/bench.py` with a script that reads `OPLOOP_TARGET_PID` and prints real memory in bytes (driver residency plus process anonymous memory, such as Linux `drm-resident-*` deduplicated by `drm-client-id`, `nvidia-smi` compute-app memory, or Apple `vm_stat` and `ioreg`). Enforce an OS or container memory limit when the cap is a hard limit.

- **Safe process shutdown.** On servers, pass `--drain-cmd` to drain active requests before a planned stop. A forced kill mid-batch can corrupt files or fault GPU drivers. Kill by exact PID or process group, never with `pkill -f` patterns that can match your own shell. Detach long queues so terminal restarts do not abort them. Use `--out` to retain trial records if the session stops.

## Output checks and lever diagnostics

A fast run with broken output is a failure.

- **Verify outputs and units.** Use `--expect` (checked on raw stdout only) or a workload validator that logs completed work units and error counts. Count real units from authoritative sources (server tokenizer usage stats instead of streamed chunks, tokenized prompt lengths instead of word estimates, and unique non-cacheable prefixes for cold throughput).

- **Check lossless equivalence.** Run `--check-eq` on deterministic stdout workloads, or run a fixture-keyed differential validator for files and server responses. On float or parallel workloads, inspect the exact divergence point before you call it a bug. A tiny logit tie differs from a logic error.

- **Stop dead lever classes early.**
  - If fusion gives no measurable gain, profile the fused path. Stop fusion work if the main operations dominate.
  - If a cache, batch, or speculation hit rate rises while throughput drops, per-step overhead grew. Time each step directly.
  - If a result beats the physical bound, suspect skipped work, cache hits, unit errors, or dead-code elimination first.

## Clean-build qualification checklist

Run every step below before you ship a tuned build, recipe, or upstream PR:

1. **Pin all inputs.** Pin source commits, dependency versions, base image digests, and external data or model revisions. Never publish from a dirty tree or unpinned local patch.

2. **Rebuild cleanly.** Build the target from a clean checkout of the exact pinned commit and save the build log.

3. **Diff the launch config mechanically.** Compare flags, arguments, and environment variables against the best benchmark config. Change nothing casually.

4. **Run acceptance and full-scale stability gates.** Verify health, core paths, edge cases, and exact output or retrieval at full scale. Run a concurrent soak under the memory cap and confirm speed above the floor. Repeat the gate if warm-up affects throughput.

5. **Run both release A/B comparisons.**
   - **Parity check**: compare clean final against the best measured build and confirm parity within noise or stated tolerance.
   - **Cumulative gain check**: compare clean final against pinned `baseline/` (upstream) and confirm that the clean build reproduces the claimed total gain.

6. **Scrub before publish.** Search all logs, ledgers, configs, and diffs for secrets, tokens, credential paths, emails, and local usernames. Keep every branch or commit that a published build pins.

The bounds and server procedures draw on the [inference optimisation skill](https://github.com/sybil-solutions/inference-optimisation-skill/tree/main/skills/inference-optimisation).
