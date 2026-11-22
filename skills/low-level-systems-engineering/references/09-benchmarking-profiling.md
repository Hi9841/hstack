# Benchmarking and profiling playbook

## Pick the right tool

| Environment | First step | Deeper investigation |
|---|---|---|
| Linux | `perf stat`, `perf record`, `perf report` | `perf annotate`, eBPF, FlameGraph, CPU-specific PMU events |
| Windows | Windows Performance Recorder (WPR) | WPA / ETW, Intel VTune, AMD uProf |
| Intel CPU | VTune Hotspots | VTune Microarchitecture Exploration and Memory Access; Intel Advisor Roofline |
| AMD CPU | AMD uProf | uProf pipeline and cache analysis |
| macOS | Instruments Time Profiler | Allocations, Counters, Signposts, System Trace as available |
| Rust | Criterion or representative app harness | `cargo asm`, Miri and sanitizer builds |
| C/C++ | Google Benchmark or app harness | Compiler remarks, ASan/TSan/UBSan |

Capabilities differ by hardware, OS privileges and profiler build. Don't pretend a particular counter exists or is reliable on all machines.

## Measurement quality

- Validate test data, work done and results; compiler can remove an unused benchmark body.
- Run warmups appropriate to workload and distinguish cold-start, first-inference and warm throughput.
- Report raw samples, median and spread; do not report p99 from insufficient runs.
- Interleave A/B with randomized or alternating short blocks to reduce drift. Block/randomization assumptions matter; one global p-value cannot correct a systematically biased experiment.
- Measure both process-level and function-level timing; process startup can drown out a 1µs hot loop.
- Keep thread count, CPU affinity, model, flags and inputs stable. Observe temperatures and power mode.
- Check that profiling itself does not alter runtime enough to invalidate comparisons.
- Account for frequency/SMT/core placement, cache warm state and NUMA. Pin threads (`taskset`, `numactl`, or thread affinity), disable turbo and frequency scaling when you can, and stop background load.
- For a kernel, keep a microbenchmark with the exact shapes and dtypes of the real workload, and also an end-to-end benchmark (for example real-time factor or tokens per second on a fixed input). A kernel win can be an end-to-end loss.
- Report the minimum with the median, never one run.
- Check the output against a reference (a naive implementation or a known-good library) with a tolerance on every benchmark run. Fast and wrong is a regression.

## Interpret counters carefully

- IPC = retired instructions / cycles; high or low IPC alone is not a diagnosis.
- Cache misses do not directly tell you bytes delivered by DRAM.
- Branch-miss rates matter only when the branches are on a meaningful critical path.
- Sampling identifies where time is spent, but not necessarily why.
- PMU event availability and semantics depend on CPU microarchitecture and kernel/tool versions.
- Some counters multiplex under limited event slots, making short runs noisier.
- Use IPC with miss counts as a first hypothesis, then confirm it. Low IPC with many cache misses suggests memory-bound. Low IPC with few misses suggests dependency chains or port pressure. High IPC but slow suggests too many instructions (poor vectorization or overhead).
- Use top-down analysis (`perf stat --topdown` or VTune) to split time into front-end bound, back-end memory bound, back-end core bound and bad speculation.
- Profile again after each kept change. The bottleneck moves.

## Statistical caution

Our provided helper compares process samples and prints bootstrap intervals and permutation p-values. These are *exploratory*, assuming approximately independent comparable samples; they do not replace a properly interleaved paired design or guarantee causality. Time series can be autocorrelated; sample size and practical significance matter. Large percent speedups on microbenchmarks may still have negligible product-level impact.

## Example measurements

```bash
# Basic portable Linux events; actual availability may vary
perf stat -r 5 -e cycles,instructions,branches,branch-misses,cache-misses,LLC-load-misses -- ./program
perf stat --topdown -- ./program
# Stack samples / annotated instructions
perf record -g --call-graph dwarf -- ./program
perf report
perf annotate
# CPU frequency, power/thermal and competing load should be tracked independently.
```

Script reference: [bench.py](../scripts/bench.py), [compare_bench.py](../scripts/compare_bench.py), [Linux profile](../scripts/profile-linux.sh), [Windows profile](../scripts/profile-windows.ps1).

Sources: [Google Benchmark guide](https://google.github.io/benchmark/user_guide.html), [Linux perf](https://kernel.org/doc/html/latest/admin-guide/workload-tracing.html), [WPR](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/introduction-to-wpr), [Instruments](https://developer.apple.com/tutorials/instruments).
