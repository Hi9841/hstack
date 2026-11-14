# Optimization experiment record

- **ID / owner / date / branch / commit:**
- **Metric and workload:** exact input/corpus/shape/concurrency and primary p50/p95/throughput/footprint metric.
- **Correctness contract:** exact-output/tolerance/accuracy, concurrency and CPU/OS support.
- **Baseline environment:** machine, CPU/ISA, memory, governor/power, OS, compiler, build flags, model/data version, caches warm/cold.
- **Evidence:** profile references, stage times, counters and allocation information.
- **Bottleneck classification:** CPU front end/backend, cache, DRAM, I/O, synchronization or algorithm.
- **Hypothesis:** one-sentence causal mechanism and proposed change.
- **Upper-bound model:** Amdahl/Roofline/byte-count and assumptions.
- **Risk:** possible regressions, numeric/unsafe/ISA constraints.
- **Implementation:** diff and exact files/functions touched.
- **Microbenchmark (optional):** shape distribution and raw measurements.
- **Product A/B:** number/order of repeats, raw sample files, time distributions, speedup, uncertainty, tail metrics.
- **Correctness:** reference outputs, fuzz/property and edge cases, sanitizers/Miri/TSan, ISA fallback and WER if applicable; identify tests not run.
- **Decision:** keep/revert/further research; practical gain vs cost.
- **Follow-up:** what still limits performance; prior rejected hypotheses to avoid.
