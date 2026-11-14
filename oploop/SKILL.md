---
name: oploop
description: >-
  OpLoop (optimization loop): the hands-on runner for a performance work session.
  It sets up a pristine baseline next to a work checkout, records journeys and a
  correctness floor, then runs one-hypothesis iterations (profile, hypothesize, test,
  change, gate, interleaved A/B measure, keep or revert, commit, log) until returns
  diminish. Use when the user says OpLoop or "optimization loop", asks to optimize,
  speed up, slim down, or reduce latency or memory of a codebase over many changes,
  wants to compare a fork against upstream, or wants a stream of small measured wins
  that can go upstream as a PR. Strategy comes from optimize-anything; number vetting
  comes from benchmark-checklist.
---

# OpLoop

OpLoop runs the optimization loop inside a work session. It does not repeat the method.

- **Strategy** (journeys, proxies, ratchets, guardrails, steering):
  [optimize-anything](../optimize-anything/SKILL.md). Read it once at setup.
- **Number vetting** (limiter, tuning, errors, repeatability, relevance):
  [benchmark-checklist](../benchmark-checklist/SKILL.md). Use it on the baseline and on
  each claimed win.
- **Mechanics** (this file): the folder layout, the ledger, the iteration, and the
  keep or revert rules.

The central rule: a change stays only if a test proves it is correct and a measurement
proves it is faster. All other changes go back out. This rule keeps a long stream of
changes safe, because each kept change has proof and each reverted change has a reason.

## Setup (once per target)

1. **Make the workspace.** Use this layout:

   ```
   <project>/
     baseline/   pristine upstream checkout. Never edit it.
     work/       the checkout you change, on branch `oploop`
     oploop/     JOURNEYS.md, LEDGER.md, results/, bench scripts
   ```

   The baseline lets you run a live A/B against upstream at any time. A number from
   memory or from an old run is not a baseline.

2. **Choose 3 to 5 journeys.** A journey is a thing a user waits for, with a start and
   an end (for example: "CLI start to first prompt ready", "send message to first
   token rendered", "idle memory after 60 s"). Write them in `oploop/JOURNEYS.md` with
   the exact command or harness that measures each one. Measure the journeys that the
   user feels. Do not measure only the parts that are easy to measure.

3. **Record the correctness floor.** Find the project's own test, typecheck, and lint
   commands (read CONTRIBUTING, CI config, package scripts). Run them in `baseline/`.
   Record the pass and fail counts in `LEDGER.md`. Failures that exist before you
   start are part of the floor. Note them and do not fix them inside the loop.

4. **Record the performance baseline.** Run `scripts/bench.py` for each journey,
   baseline against itself (A against A). This shows the noise level. If the noise is
   larger than the gains you expect, fix the harness first (see the determinism
   checklist in optimize-anything's proxy ladder).

5. **Start the ledger.** Copy `references/ledger-template.md` to `oploop/LEDGER.md`.

## The iteration

One iteration tests one hypothesis. Keep the iterations small. Ten measured 5% wins are
better than one large change that nobody can review.

1. **Profile.** Find where the time or memory goes in the journey you chose. Use the
   runtime's profiler (`--cpu-prof`, `perf`, `py-spy`, heap snapshots, or import-time
   traces). Name the hot spot with `file:line` and its share of the journey.
2. **Write the hypothesis in the ledger before you change code.** Use this format:
   "`<hot spot>` costs about N ms (M% of the journey) because `<cause>`. `<Change>`
   should save about K ms." A hypothesis that you write after the result is a story,
   not a test.
3. **Test first.** Make sure a test covers the behavior that you will change. If no
   test covers it, write the test, and make sure it passes on the unchanged code.
4. **Change.** Make the smallest diff that tests the hypothesis. Follow the style of
   the code around it.
5. **Gate.** Run the tests, typecheck, and lint. The result must equal or be better
   than the floor. A gate failure is a revert, not a debug session in the loop.
6. **Measure.** Run `scripts/bench.py` with the previous kept commit as A and the
   candidate as B. Also run the other journeys, so that you see regressions elsewhere.
7. **Decide.**
   - **Keep** if B is better beyond the noise (the script reports `significant`), no
     other journey regressed beyond noise, and the gain is worth the extra code.
   - **Revert** in all other cases. Use `git restore` or `git reset` for the candidate
     only. A revert is a correct result. Log it with the reason.
8. **Commit** each kept win as one commit. Put the number in the message, for example
   `perf(session): cache provider list (startup p50 412 -> 371 ms)`. Lower the ratchet
   with `optimize-anything/scripts/ratchet.py` if the project has one.
9. **Log** the result in `LEDGER.md` (kept or reverted, numbers, commit hash).
10. **Profile again.** The hot spot moves after each win. Do not continue on the old
    profile.

## When to stop or ask

- **Diminishing returns.** Three iterations in a row that give no significant gain on a
  journey: close that journey and move to the next one.
- **Complexity cost.** Reject a win when the code it adds costs more to maintain than
  the time it saves. Example: a 900-line build plugin for 2 ms per message.
- **Taste.** If a change alters what the user sees or feels (output order, animation,
  defaults, timing of UI), stop and ask the user with before and after evidence.
- **Contracts.** Ask before you change a public API, a config format, a file format, a
  wire protocol, or a plugin interface.

## Upstream PR mode

Use this mode when the work will go to the upstream project as a pull request.

- Keep each commit independent and reviewable, so that a maintainer can take some wins
  and refuse others.
- Follow the project's own contribution rules (AGENTS.md, CONTRIBUTING.md, lint rules).
  Use the project's package manager and runtime versions.
- Group the commits into PR-sized series by subsystem. Put one primary number in each
  PR body, and link the full ledger for details.
- Do not open, push, or comment on an upstream PR without explicit approval from the
  user. A PR is published content.

## Scripts and references

- `scripts/bench.py`: interleaved A/B benchmark. It records wall time, peak memory of
  the full process tree, and exit codes, and it reports median, range, and a rank-sum
  significance test. Run `uv run scripts/bench.py --help`. Memory is sampled every
  10 ms, so for runs shorter than about 100 ms the peak memory is a low estimate. Use
  `--hold` or `--ready` to measure memory of a program that stays open.
- `references/ledger-template.md`: the ledger format.

## Report

At the end of a session, give:

1. A table per journey: baseline, now, change, run count, and noise range.
2. The list of kept commits with their numbers, and the count of reverted hypotheses.
3. The correctness floor before and after.
4. The next three hypotheses you would test.
