# Performance change report

## Summary

**Status:** Proposed / Implemented / Validated / Reverted. **Target metric:** ... **Hardware:** ... **Baseline revision:** ... **Candidate revision:** ...

## Results

| Workload / case | Baseline (median) | Candidate (median) | Speedup | Runs | Uncertainty | Correctness |
|---|---:|---:|---:|---:|---|---|
| Named reproducible case | | | | | | |

Attach full raw results and configuration. State units and whether lower or higher is better. p95/p99 only if sample count justifies them; do not infer product-wide tail improvements from tiny runs.

## Engineering explanation

**Bottleneck → Cause → Mechanism → Verification**. Include any compiler assembly/counter changes that corroborate the hypothesis and whether they were measured or inferred.

## Correctness and portability

List functional tests, exact-output/quality measures, vector tails, invalid inputs, race/UB checks, ISA selection and OS/compiler coverage. State tests unavailable or skipped.

## Regressions and decision

List memory, startup, throughput/latency tradeoffs, energy and maintainability. Keep or revert; cite concrete results, not a 'feels faster' judgement.
