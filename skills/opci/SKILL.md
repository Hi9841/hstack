---
name: opci
description: Optimize CI latency and cost without loss of check coverage. Use for OPCI, slow pull request checks, long runner queues, or CI performance budgets.
---

# OPCI

Target a PR verdict in under 2 minutes at p50 and under 3 minutes at p95.

## Protect the merge gate

Require the full suite on the merge queue candidate before it can reach the default branch. Limit affected-project selection to PR feedback. Verify that the queue triggers the full suite and that branch protection requires its result.

Preserve check coverage, first-attempt failures, and existing test deadlines. Fix flaky checks at their source. If the full merge gate is absent, keep PR checks complete until the gate works.

## Measure the baseline

1. Read the CI workflows, required checks, runner configuration, and repository instructions.
2. Collect the latest 150 relevant runs, or all available runs if fewer exist. Record the sample size and time window.
3. Measure PR latency from commit or workflow trigger to required verdict. Use the same start event before and after.
4. Report p50 and p95 for PR latency and each job's queue, setup, and execution time. Use step timestamps to separate setup from execution. Mark unavailable timestamps.
5. Report cache hit rate, billed runner time, and cost. Report cancellations and failures separately so they cannot make latency appear lower.
6. Find the job sequence that determines the PR verdict. Rank changes by their expected effect on that sequence and fix the largest measured delay first.

## Apply and verify one change at a time

| Area | Default target | Candidate change |
| --- | --- | --- |
| Runner queue | Under 10 seconds | Compare faster runners, including Blacksmith for GitHub Actions. Include short jobs in the comparison. Cancel superseded runs for the same PR. Keep merge queue runs independent. |
| Setup | Under 30 seconds and over 95% PR cache hits | Seed caches from the default branch. Compare a package cache with an installed dependency cache. Key the latter by lockfile, platform, and runtime. Keep full history where diff selection needs it. Measure a blobless clone. |
| Lint | Under 5 seconds | Compare Oxlint with the current linter. Check rule and plugin coverage before removal. |
| Type check | Under 5 seconds | Compare supported fast checkers with the current compiler. Verify project references and diagnostics. |
| Format and install | Measure separately | Compare Oxfmt and, where repository rules permit it, Bun. Keep lockfile and install semantics reproducible. |
| Tests | Under 60 seconds per shard | Measure larger runners before you add shards. Balance shards by duration and match workers to available cores. Give each shard its own database. |
| Local pre-push | Under 9 seconds | Check format and lint on changed files. Type-check affected projects with their dependencies. |

Run independent lint, type-check, build, and test jobs in parallel when this reduces verdict time. Move independent migration checks or app tests off the longest job sequence if the split saves time.

For Vitest shared-process tests, verify cleanup before you disable isolation. Reset shared state after each file. Run randomized orders and record the seeds. Document the cleanup requirements in the repository instructions.

For affected-project selection, check the merge base, transitive dependencies, and shared configuration. Compare the selection with a full run for representative changes. In a disposable branch, place a known failure in an indirectly affected project and confirm that the required check fails. Use the full suite when selection lacks sufficient inputs.

Compare old and new tools side by side on the same revisions. Record checks or diagnostics the replacement misses. Keep the existing tool or run a supplemental check if coverage would fall. Confirm command support for the installed version before you adopt a tool.

Use real CI runs to compare the same workload and runner conditions. Include warm and cold caches where relevant. Enforce stable budgets with a separate failing check. Use CI service metrics for queue time, which the queued job cannot measure itself. Preserve test deadlines and report the phase that exceeded its budget.

## Deliver the changes

Use one small PR per independently verified change when the user authorizes PRs. Include before-and-after results in each PR. Complete independent work before you group requests for new accounts, secrets, or paid capacity. Include estimated monthly cost for each paid option.

Report before-and-after PR p50 and p95, billed runner time, and monthly cost. Label estimates and list targets that remain open. Include the evidence that the merge queue ran the full suite.
