# Models: throughput, latency, Amdahl, Roofline and queueing

## First define what you are measuring

- **Latency:** completion time for one request; focus on critical path and queuing.
- **Throughput:** completed work per second at a specified concurrency and input distribution.
- **CPU time:** summed execution time, not the same as latency under multithreading.
- **Tail latency:** percentiles require adequate sample sizes; p99 from 15 runs is meaningless.
- **Speedup:** old runtime / new runtime, ideally from comparable distributions.

## Amdahl's law

`S_total = 1 / ((1 - f) + f / S_component)` for a component that originally consumed fraction f. Measure f, don't guess. Distinguish serial critical path and parallel work.

## Roofline model

Arithmetic intensity `I = operations / bytes transferred` at a specified memory level. Performance upper bound `P <= min(P_compute_peak, I × B_effective)`. Choose consistent operation units: floating-point FMA often counts as 2 FLOPs; integer MAC as specified by the metric. For quantized bit operations, quote a meaningful work unit. DRAM bandwidth is not automatically the correct ceiling: some work is constrained by L1/L2 bandwidth, loads/stores, dependency latency, instruction decoding, or execution ports.

**Get the machine peaks.** Peak compute = cores × frequency × SIMD lanes × FMA units × 2. Measure sustainable bandwidth with a STREAM-style test, not the spec sheet, and measure each cache level (L1, L2, L3, DRAM) when you can. Intel Advisor has a Roofline view; otherwise use [roofline.py](../scripts/roofline.py).

**Read the position.**

- Near the bandwidth roof: arithmetic changes cannot help. Move fewer bytes: quantize weights, pack data, block for cache, fuse operations to remove round trips.
- Near the compute roof: the kernel is almost done, or it needs a better algorithm or wider instructions (VNNI, AMX).
- Far below both roofs: the code itself is inefficient. Most wins are here.

A CPU Roofline is less exact than a GPU Roofline, because the compiler, the out-of-order core and the prefetchers hide much behavior. Use it as a bound and confirm the position with counters.

**Example:** 2e9 useful FLOPs and 1e9 B of DRAM traffic → I=2 FLOP/B. With measured 80 GB/s sustainable bandwidth and 1 TFLOP/s sustainable compute, DRAM Roofline bound is min(1000, 160) GFLOP/s = 160 GFLOP/s. This is a modeling example, not measured Trit data.

## Little's Law and capacity

`L = λW` links average in-flight requests L, completed arrival rate λ and average time W in a stable system. Beware coordinated omission and nonstationary load. Increasing concurrency can raise throughput while making individual request latency worse.

## Scaling diagnosis

- Sublinear speedup: serial fraction, contention, bandwidth, task overhead, NUMA, cache traffic, per-core frequency effects.
- Flat single-thread improvement from larger SIMD: loop dominated by loads, calls, dependencies, or front-end rather than lane count.
- High bytes/work: investigate data structure and fused stages before instruction substitutions.

## Validation questions

1. Is the proposed kernel hot enough to matter in the product?
2. Is the measured metric bounded by arithmetic, data movement, or a dependency?
3. Which bytes and operation counts are *real*, not inferred solely from source loops?
4. Does input size move the bottleneck between cache levels?
5. Will the optimization trade p50 for p99, latency for throughput, or portability for native-only speed?

Sources: [Roofline](https://escholarship.org/uc/item/78h8v7mr), [Brendan Gregg's USE method](https://www.brendangregg.com/usemethod.html), [Computer Architecture: A Quantitative Approach](https://shop.elsevier.com/books/computer-architecture/hennessy/978-0-443-15406-5).
