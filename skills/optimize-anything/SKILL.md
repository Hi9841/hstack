---
name: optimize-anything
description: >-
  Measurement-driven optimization loop for any target: latency, memory, bundle size,
  build and test time, cloud spend, energy, LLM cost per request, error rate, or any
  budget that has crept up unnoticed. Use when asked to make something faster,
  smaller, cheaper, leaner, smoother, or more reliable, when a target "feels slow" with
  no data behind it, when a target needs a budget enforced in CI, or when a win has to
  be locked in so it cannot decay. Not for a one-off tweak on an already-measured hot
  path, and not for feature work with no target metric.
---

# Optimize anything

The central move: **once you can measure something, it becomes tractable.** So the lever
is not effort, it is finding more things to measure. Wall-clock time is what users feel,
but it is noisy and too flaky to gate CI on. So the loop runs against a deterministic
proxy in the lab, and a ratchet in CI makes that number only move one way.

This is the loop Anthropic ran to make claude.ai about 3x faster in two weeks, with the
speed-specific parts generalized. Every step applies to any measurable target; only step
2 changes with the domain.

## 1. Scope the climb to a few outcomes

1. Name the handful of user-visible outcomes that cover most real usage. Four beats
   twenty. In the source sprint, four journeys became thirteen measurements across two
   platforms, and those journeys were 95% of activity.
2. Split each into measurements that are actually comparable: each starts at a user
   action, ends when the result is rendered or returned, and disambiguates client work
   from server work. Two numbers that are not comparable produce conclusions that are
   not comparable. Fix the instrumentation first.
3. Fix the statistic before the target. p75 is the median experience, p95 is the tail.
   Say "p75 time to typeable page: 3.1s -> 0.55s", not "faster".
4. Estimate the impact of each candidate change in the target unit, sum them, and set
   the targets. If the targets land early, that is the signal to set new ones, not to
   stop.

## 2. Find a proxy you can beat in the lab

1. The field metric is the truth and the wrong CI gate. Find a deterministic count that
   stands in for it. Cheapest and best first: exact counts (instructions retired,
   tokens, rows examined, bytes, requests, objects), then structural counts (commits,
   calls, queries, modules), then exact frame timing.
2. Give every new benchmark exactly two jobs: a metric the agent can move in the lab,
   and a CI guardrail whose number can only ratchet down. A benchmark that does neither
   is unshipped, not tuned.
3. Prove the proxy before climbing it. Drive the count down on a real hot path and
   confirm the user-visible metric moved. In the source sprint, 48% and 31% fewer
   instructions produced 78% and 44% less wall-clock time, which is what justified
   checking those counts in CI. A benchmark that does not correlate is worse than no
   benchmark, because it will be climbed instead of the real target.
4. Unship anything flaky, and anything that measures a proxy of a proxy.

Read [references/proxy-ladder.md](references/proxy-ladder.md) for the per-domain ladder:
web and client runtime, node and server, database, build and test, cloud spend, LLM and
AI systems, mobile, memory, and reliability. It also lists the determinism checklist
(fixtures, seeds, worker counts, warm vs cold) that makes a count repeatable.

## 3. Run the loop on one narrow workstream

One workstream is one journey or one benchmark. Keep it narrow and sequential inside
itself; the parallelism is across workstreams, not within one.

1. Find a slow stretch, starting from a real artifact: screen recording, trace, field
   spike, ticket, or a human describing what felt wrong.
2. Trace the flow, then find or build a benchmark that demonstrates the problem. Show
   it going red on main before changing anything. A benchmark that has never been red is
   a guess.
3. Ship behind a flag, in PRs sized for review risk, with one human approval. Anything
   user-visible goes behind a flag.
4. Watch the deploy. Read the field data for the actual journey, not just the lab
   number.
5. Win: ratchet the benchmark down so the win cannot come back. No win: flag off,
   iterate or revert, and say plainly that the proxy was wrong.
6. Then go find the next slow stretch in the same journey. Do not close the workstream
   when the original request is answered. A finished thread is a wasted instrument.

## 4. Ratchet

- Check the budget in CI on every PR. A rise fails the build.
- When a number goes down, lower the ceiling in the same PR, or from a scheduled job
  that locks in the best recent value. A stale ceiling is a regression nobody sees.
- Never loosen a ratchet to unblock a merge. Lowering one requires a written reason, a
  real `file:line` justification, and a human. Refusing a PR with a red budget is a
  success, not an obstacle.
- `scripts/ratchet.py` does this: `check` (exit 1 on regression, `--update` to tighten),
  `set`, `list`. Budgets live in a checked-in JSON file, one entry per metric.
- Ratchets are the only reason the win survives. Performance decays in a fast-moving
  codebase; without a gate, the number quietly returns to where it started.

## 5. Guardrails before the pace

- Correctness tests first, always. Write the test, watch it pass, then optimize inside
  it. An optimization with no test is a regression waiting for a user.
- Automated review plus one named human approver per PR.
- Flags on anything risky. Classify each one as a kill switch or a ramp, retire it as
  soon as it is safe, and keep the count from growing. The source sprint introduced
  nearly 200 and cleaned up more than half.
- Roll out high-risk changes in stages: employees, then 1%, then everyone. The lab
  cannot see everything. A layout shift that broke their fastest win came from Chrome
  prerendering a page at the wrong height during speculative loading, invisible to
  headless tests because headless has no browser chrome to retract.
- Give every brittle win its own guardrail suite aimed at the exact way it breaks. Theirs
  was: render the real component in jsdom and fail if the static copy drifts, compare
  the static page to the live render across 14 viewports within 1px, type straight
  through the handoff and fail on any lost or reordered key, and open a thread on any
  nonzero shift in the field. Brittle by design is fine. Silently brittle is not.
- Every new instrument gets an alert and a named owner. That is how "31% of page loads
  moved something after the page was usable" turned into a named list of offenders that
  got fixed as a batch.

## 6. Steer

- **Ambition.** By default the agent hedges: it tickets findings, pads estimates, calls
  everything large. When the guardrails are solid, say so explicitly and push for bolder
  scope. Hedged estimates are how the easy half of the work gets left.
- **Taste.** Name a human owner per workstream and route every user-perceptible tradeoff
  to them with before-and-after evidence. Skeleton now or after 500ms. Table cell by cell
  or row by row. Is a streaming fade worth a fifth of the frame budget. Do not let the
  agent settle these alone; the shaving is cheap and the taste is not.
- **Direction.** Decide what to combine, what to prioritize, and when a workstream has
  hit diminishing returns. Kill changes whose value does not pay for their maintenance.
  A 900-line build plugin for 2ms per send is a loss, and saying so in one line is the
  whole job.

## 7. Keep finding things to measure

- Every instrument built for one purpose finds three more. Ask the standing question:
  what have we not measured, what can we hill climb on, where is the most opportunity
  now, and what are the wacky ideas.
- Cheap censuses are the highest yield per hour. Count hooks and store subscriptions in
  a hot path. Count selector cost per DOM change. Look for a leftover reload or a
  redundant serialization in an idle or background task. Check the encoding traps: one
  non-Latin-1 character can push an entire string onto a runtime's two-byte path and
  slow every regex that touches it.
- Fan out one workstream per parallel worker, each with its own benchmark and its own
  scope, and merge only the wins. Use `swarm` for the fan-out mechanics, `arena` when
  competing approaches chase the same target, and `diagnosing-bugs` when the job is one
  named regression rather than a search.
- Go after p95, the long tail, and absurd inputs next. The median is where the sprint
  started.

## When not to use this

- One known hot path that is already measured: fix it, add the ratchet, done.
- Feature work with no target metric. Pick a metric or skip the framing.
- Changing the metric instead of the system. If the only way to hit the number is to
  redefine the number, it is not an optimization.

## What to hand back

1. Baseline vs now per target, at the percentile promised, with the measurement method.
2. The ratchets added, their budget file path, and where they run.
3. Which proxies were proven to correlate, and which were thrown out for failing to.
4. Remaining targets, and the next workstreams you would open.
