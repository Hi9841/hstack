---
name: oploop
description: >-
  Run or resume a measured optimization session with a live baseline, a correctness
  floor, and one-hypothesis keep-or-revert iterations through plateau and clean-build
  qualification. Use when the user says OpLoop or "optimization loop", asks for
  repeated keep-or-revert performance iterations on a codebase or server, wants a
  measured fork comparison against upstream, or wants a reviewable series of small
  verified performance commits for an upstream PR. Strategy comes from
  optimize-anything. Number check rules come from benchmark-checklist.
---

# OpLoop

Read the [strategy, proxy, and budget guide](../optimize-anything/SKILL.md) once at setup.

Use [benchmark-checklist](../benchmark-checklist/SKILL.md) on the baseline and on each claimed win.

Report a broken baseline, an impossible target, or a correctness defect immediately.

## Start or resume

1. **Check for a prior session.** If `oploop/LEDGER.md` exists, resume from it. Read the workspace, floor, journeys, and rejected hypotheses before you run anything. Never overwrite a prior ledger. Never retest a rejected hypothesis without a new mechanism or a changed condition.

2. **Create the workspace (new session only).** Use this directory layout:

   ```
   <project>/
     baseline/   pinned upstream checkout. Never edit it.
     prev/       previous kept commit (control A) with isolated build outputs
     work/       candidate checkout on branch `oploop` (candidate B)
     oploop/     JOURNEYS.md, LEDGER.md, results/, bench scripts
   ```

   Copy `references/ledger-template.md` to `oploop/LEDGER.md` first, before you record any results.

3. **Define scope, limits, metric, and runner.** Start with the requested user-visible journey. Add a regression journey only if the candidate can affect it. Record exact commands in `oploop/JOURNEYS.md`. Record hard limits (memory cap, maximum input size, concurrency), the quality contract (lossless or labelled lossy trades), and the minimum useful margin in `LEDGER.md`. Pick the runner from the metric. Use `scripts/bench.py` for wall time or sampled peak memory. For throughput or tail latency, use a workload driver. Record completed work, errors, elapsed time, and the requested statistic. Define the output validator and acceptance rule before the first comparison.

4. **Estimate a bound.** Compute a practical bound from measured host limits or measured stage time (see [references/measurement-and-ceilings.md](references/measurement-and-ceilings.md)). Record the estimate and its assumptions in `LEDGER.md`. Report an impossible target only when a proven physical limit excludes it. Include the arithmetic.

5. **Fix the measurement environment.** Run on AC power with a fixed performance profile and an idle host. Run only one benchmark job at a time (use `--lock`). Record every host config that you change so you can restore it at session end.

6. **Record the correctness floor.** Run the project's test, typecheck, and lint commands in `baseline/`. Record pass counts, fail counts, and exact failed test identities in `LEDGER.md`. Do not fix prior failures inside the loop.

7. **Record the A/A noise baseline.** Run `baseline/` against itself for each journey and record median, range, and sample count. If noise exceeds the minimum useful margin, fix the benchmark script first (see the determinism checklist in `optimize-anything`).

Setup is done when `oploop/JOURNEYS.md` and `oploop/LEDGER.md` hold the scope, limits, and bound. They must also hold the correctness floor (with failed test identities) and the A/A noise baseline.

## The iteration

One iteration tests one hypothesis. Before you measure any edit, sync `prev/` to the last kept commit with isolated build outputs and record both revisions. Reserve `baseline/` for the initial baseline and final cumulative A/B.

1. **Profile.** Measure where time or memory goes in the active journey (for V8 or JSC profiles, summarize with `python scripts/cpuprofile.py PROFILE.cpuprofile`). Name the hot spot with `file:line`, its share of the journey, and its gap to the bound.

2. **Rank and record the hypothesis before edits.** Rank levers by estimated journey savings and implementation cost, backed by profile evidence. Record the hypothesis in `LEDGER.md`: "`<hot spot>` costs about N ms (M% of the journey) because `<cause>`. `<Change>` will save about K ms."

3. **Verify test coverage.** Confirm that a test covers the behavior you will change. If none exists, add one and confirm that it passes on unchanged code.

4. **Edit only the candidate.** Apply the smallest diff in `work/` that tests the hypothesis.

5. **Run the correctness gate.** Execute tests, typecheck, and lint. Reject any new failed test identity even when total fail counts stay equal. If an infrastructure fault breaks the check, log an invalid trial. Repair the host before you decide the candidate.

6. **Measure and verify outputs.** Compare `prev/` (side A) against `work/` (side B) with warmup and output checks:

   ```
   uv run "<skill-dir>/scripts/bench.py" --name J1 --a "<cmd>" --a-cwd ./prev --b "<cmd>" --b-cwd ./work --runs 10 --warmup 2 --min-improvement 2 --check-eq --require-ac --lock ./oploop/bench.lock --out ./oploop/results/ledger.jsonl
   ```

   Run this example from the directory that contains `prev/` and `work/`. Substitute the absolute skill path and journey commands. Use `--help` to select options. When restarts prevent per-run interleaves, use [repeated bracketed controls](references/measurement-and-ceilings.md#noise-control-bracketed-runs-and-process-safety). Run all protected regression journeys before you keep a change.

7. **Check anomalies before you trust a number.** On an unexpected win or strange number, suspect measurement error first. Repeat the run. Read [references/measurement-and-ceilings.md](references/measurement-and-ceilings.md) when a lever class gives 0% gain or outputs diverge.

8. **Decide keep, revert, or invalid.**

   - **Keep** only when every condition below passes:
     - Correctness gate introduces zero new failed test identities.
     - Output check passes (raw stdout match, `--expect`, or workload validator with completed work count).
     - The runner reports `eligible_keep=True` or meets the predefined acceptance rule for a custom driver.
     - Every protected regression journey stays within its regression allowance.
     - Added code complexity pays for the measured gain.

   - **Invalid trial** when power drops, a probe fails, or host interference breaks the run. Record the fault without a plateau count increase. Correct the fault before you measure again.

   - **Revert** a valid candidate that fails a keep condition. Restore only the changes from this iteration in `work/`. Record the reason in `LEDGER.md`.

9. **Commit and tighten the ratchet.** Commit each kept win as one commit with the measured delta in the message (for example, `perf(session): cache provider list (startup p50 412 to 371 ms)`). Tighten the budget with `optimize-anything/scripts/ratchet.py` if the project uses one. Update `prev/` to the new commit.

10. **Log and re-profile.** Append the full result to `LEDGER.md`. Profile again before the next iteration because the hot spot moves after each win.

## Plateau, stability gates, and escalations

- **Plateau checkpoint.** After three valid rejected hypotheses in a row on one journey (invalid trials do not count, and a kept win resets the count), write a `Plateau status` block in `LEDGER.md`. Include best versus baseline and bound, the measured limiter with evidence, and remaining profile-backed levers ranked by savings and cost. Close the journey and move on, or shift to deeper levers if the user asked to continue.

- **Full-scale stability gate.** Before you mark a branch "best" or ready to ship, run a full-scale stability test (maximum input size, concurrent soak, or exact retrieval under load). Confirm that memory stays under the cap.

- **Taste and contracts.** Stop and ask the user with before-and-after evidence before you change visible UI, defaults, or output order. Ask before you alter public APIs, config or file formats, wire protocols, or plugin interfaces.

## Qualify and ship (upstream PR mode)

Read [references/measurement-and-ceilings.md](references/measurement-and-ceilings.md) for the full release checklist before you deliver a build, recipe, or upstream PR.

- **Independent commits.** Keep each commit self-contained and reviewable, grouped by subsystem. Obey repository rules (`AGENTS.md`, `CONTRIBUTING.md`, package manager, runtime versions).

- **Honest labels.** Never mix numbers from different benchmark scripts, prompt panels, or cold and warm caches. Always label each number's source.

- Get explicit user approval before you open, push to, or comment on an upstream PR.

## Report and teardown

On every completion (normal finish, plateau handback, or user stop), stop all owned background servers or loops. Confirm that no owned processes remain, and restore every host or power config that you changed. Record anything intentionally left active.

Report these items at session end:

1. A table per journey: baseline, now, bound, change, valid blocks, 95% CI or range, and exact measurement method (runner, cache state, statistic).

2. Kept commits with numbers, count of valid reverts, count of invalid trials, and main negative findings.

3. What limits further gains, with profile evidence and distance to the bound.

4. Correctness floor (with failed test identities) and stability gates before and after.

5. System state restored and any state intentionally left active (servers, uncommitted files, pinned branches, cleanup items).

6. What you did not verify.

7. Remaining profile-backed hypotheses, if any, ranked by estimated savings and cost.
