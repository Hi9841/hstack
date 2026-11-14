# Primary sources and evidence guide

Follow the authoritative source for **the exact architecture/compiler version** under test. Older materials are excellent for mental models but not an authoritative source for costs or hardware features on a 2026 processor.

## CPU and instruction behavior

- [Intel Optimization Reference Manual](https://www.intel.com/content/www/us/en/developer/articles/technical/intel64-and-ia32-architectures-optimization.html) — architecture-sensitive optimization guidance, cache, front end, vector execution.
- [Intel Software Developer's Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html) — instruction semantics, CPUID, memory ordering and ISA requirements.
- [AMD documentation](https://docs.amd.com/) — find the actual processor-family software optimization guide and event descriptions; do not apply Zen-family rules blindly to all AMD CPUs.
- [Arm Developer](https://developer.arm.com/documentation) — Arm Architecture Reference Manual, Neoverse/Cortex processor TRMs and optimization guides.
- [Agner Fog's optimization manuals](https://www.agner.org/optimize/) — empirical instruction tables, x86 microarchitecture and C++/assembly optimization.
- [uops.info](https://uops.info/) — measured instruction latency, throughput and execution-port usage (check exact microarchitecture and operand form).

## Performance modeling and memory

- [Roofline paper: Williams, Waterman & Patterson (2009)](https://escholarship.org/uc/item/78h8v7mr) — arithmetic intensity and compute/bandwidth bounds.
- [Ulrich Drepper, What Every Programmer Should Know About Memory](https://www.akkadia.org/drepper/cpumemory.pdf) — memory hierarchy, locality, NUMA; dated examples require current measurements.
- [Brendan Gregg, USE Method](https://www.brendangregg.com/usemethod.html) — utilization, saturation and errors across resources.
- [Brendan Gregg, Flame Graphs](https://www.brendangregg.com/flamegraphs.html) — stack-profile visualization and interpretation.

## Compilers and tooling

- [LLVM Optimization Remarks](https://llvm.org/docs/Remarks.html) — what did or did not optimize.
- [Clang Users Manual](https://clang.llvm.org/docs/UsersManual.html) — profile generation, compiler flags, instrumentation.
- [GCC Optimize Options](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html) — compiler switches and their conditions.
- [Cargo profiles](https://doc.rust-lang.org/cargo/reference/profiles.html), [rustc codegen options](https://doc.rust-lang.org/rustc/codegen-options/index.html) — Rust LTO, codegen units, target-cpu and PGO-related options.
- [Google Benchmark Guide](https://google.github.io/benchmark/user_guide.html) — warmups, benchmark setup, variance.
- [Criterion.rs](https://bheisler.github.io/criterion.rs/book/) — Rust statistical benchmarking.
- [Linux perf documentation](https://perf.wiki.kernel.org/index.php/Main_Page) and [kernel workload tracing](https://kernel.org/doc/html/latest/admin-guide/workload-tracing.html) — sampling and CPU counters.
- [Microsoft Windows Performance Recorder](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/introduction-to-wpr), [Windows Performance Analyzer](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-analyzer) — Windows ETW traces.
- [Apple Instruments](https://developer.apple.com/tutorials/instruments) — macOS/iOS profiling.

## Safety and numerical behavior

- [Rust Reference — undefined behavior](https://doc.rust-lang.org/reference/behavior-considered-undefined.html)
- [Rustonomicon — atomics](https://doc.rust-lang.org/nomicon/atomics.html)
- [Miri project](https://github.com/rust-lang/miri) — interpreter for many classes of Rust UB.
- [Loom](https://github.com/tokio-rs/loom) — explore concurrency interleavings in Rust.
- [ThreadSanitizer](https://clang.llvm.org/docs/ThreadSanitizer.html), [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html), [UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html)
- [IEEE 754 overview (IEEE Standards Association)](https://standards.ieee.org/ieee/754/6210/) — floating-point standard information.

## Application case

- [Trit repository](https://github.com/Hi9841/trit)
- [Trit AGENTS.md](https://raw.githubusercontent.com/Hi9841/trit/main/AGENTS.md) — repository-specific verification gates (read checked-out copy first).
- [Trit optimization ledger](https://raw.githubusercontent.com/Hi9841/trit/main/oploop/LEDGER.md) — previous kept/reverted experiments (read checked-out copy first).

**Evidence hierarchy:** representative end-to-end measurement and correctness tests on the target hardware > targeted profiling/counter data > microbenchmarks on the same target > target-specific vendor manuals and instruction tables > generic heuristics. This is a practical prioritization, not an assertion that benchmarks alone prove causality.
