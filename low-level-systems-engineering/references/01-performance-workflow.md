# Performance engineering as an experiment

## Specify the contract

Document the primary objective (e.g. single-request p50 latency at batch size 1), hard constraints (bit-identical output, peak RSS, supported chips), secondary metrics (p99, power, start time), and reference baseline. 'Faster' without a workload and target machine is undefined. Prefer user-facing work over an isolated operation.

## Reproduce and instrument

1. Pin exact code revision, compiler/toolchain, flags, binary and model/data versions.
2. Warm data/code caches or include cold behavior, explicitly as the workload requires.
3. Isolate incidental variation: background processes, governor/power mode, thermal state, SMT occupancy, NUMA placement, and unrelated I/O.
4. Run enough samples to estimate the distribution. Record *every* sample and order. For short operations, batch iterations to exceed timer resolution and benchmark overhead; prevent dead-code elimination.
5. Capture stage time, not only total runtime. Use sampled profiling first; add targeted spans if necessary.
6. Check correctness *before* judging speed.

## Form a falsifiable hypothesis

Good: 'The decoder reconstructs K/V into head-major layout every step; keeping the cache in compute-friendly layout will reduce bytes copied from O(T²) accumulation to O(T) under append-only growth.' But verify the premise and memory strides first; head-specific row stride may vary as T grows.

Bad: 'Inline everything and enable AVX-512 because vectorized code is faster.' No demonstrated bottleneck or regression plan.

Write expected counter movement: fewer LLC writes, fewer allocations, unchanged executed model operations, lower decoder time. Define what observation would refute it.

## Estimate achievable effect

If a stage is fraction f of end-to-end time and gets s times faster, Amdahl's law gives total speedup = 1 / ((1-f)+f/s). If only 10% of request time is in a kernel, 2× kernel acceleration yields at most 5.26% overall. For parallel work, remember synchronization and memory bandwidth may impose additional limits.

## Controlled experiment

- Keep one functional change; save baseline commit and build artifacts.
- Measure local microbenchmark for causal mechanism *and* end-to-end benchmark for user value.
- Include input distributions: small/large, aligned/unaligned, hot/cold, 1/many threads, known hard cases.
- Compare baseline/candidate by alternating or randomized blocks; avoid 'all A then all B' when CPU conditions drift.
- Check multiple machines/ISAs or explicitly constrain dispatch scope.
- Record speedup as T_baseline/T_candidate; state if interval overlaps no effect.

## Keep/revert decision

A candidate passes only if correctness gates pass, intended primary metric improves beyond practical and statistical uncertainty, and no important tail latency, memory, startup, energy, or portability regression violates budget. Document failed experiments: they eliminate future wasted exploration.

See [experiment template](../templates/experiment.md), [benchmarking](09-benchmarking-profiling.md), [correctness](10-correctness-and-security.md).
