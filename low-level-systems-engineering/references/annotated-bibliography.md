# Annotated research bibliography and reading order

The resources below are linked to authorized publisher/author/manual pages, not embedded as copyrighted copies. Each recommendation describes *what to learn*, not an invented quote from a specific page. Follow updated editions and processor-specific documents when possible.

## Core books: start here

| Priority | Work | Why it matters | How to use it |
|---|---|---|---|
| 1 | [Randal Bryant & David O'Hallaron — Computer Systems: A Programmer's Perspective](https://csapp.cs.cmu.edu/3e/perspective.html) | Assembly, memory, compiler, linking, VM, I/O, concurrency viewed as programmer-visible systems | Build causal mental model before chasing cycle counts |
| 1 | [Brendan Gregg — Systems Performance, 2nd ed.](https://www.brendangregg.com/systems-performance-2nd-edition-book.html) | Methodical performance diagnosis from applications to kernel/hardware | Use for workload definition, USE method, tracing and bottleneck work |
| 1 | [John Hennessy, David Patterson & Christos Kozyrakis — Computer Architecture: A Quantitative Approach, 7th ed.](https://shop.elsevier.com/books/computer-architecture/hennessy/978-0-443-15406-5) | Quantitative architecture and hardware-performance tradeoffs | Understand latency, instruction throughput, cache, parallelism |
| 1 | [Fedor Pikus — The Art of Writing Efficient Programs](https://www.packtpub.com/en-us/product/the-art-of-writing-efficient-programs-9781800208117) | Practical CPU performance in C++ with modern optimization mindset | Read alongside instrumented experiments; validate specifics on target |
| 1 | [Agner Fog — Optimizing Software in C++ and instruction/microarchitecture manuals](https://www.agner.org/optimize/) | Empirical x86 optimization, ABI, branch/data behavior, instruction tables | Go-to for analyzing assembly and x86 kernel hypotheses |

## Memory, cache and data-oriented structure

- [Ulrich Drepper — What Every Programmer Should Know About Memory](https://www.akkadia.org/drepper/cpumemory.pdf) (2007): excellent explanation of caches, locality, NUMA, prefetching and memory hierarchy; **actual latency/bandwidth numbers are old**. Read before changing layouts/allocators.
- [Samuel Williams, Andrew Waterman, David Patterson — Roofline (2009)](https://escholarship.org/uc/item/78h8v7mr): performance bound from arithmetic intensity and machine limits; use to choose between more FLOPs/s and fewer bytes. Count bytes at a declared memory level.
- [Martin Fowler / Martin Thompson — Principles of Mechanical Sympathy](https://martinfowler.com/articles/mechanical-sympathy-principles.html): useful synthesis of locality and single-writer patterns; evaluate each recommendation for your particular workload.
- [Richard Fabian — Data-Oriented Design](https://www.dataorienteddesign.com/dodbook/): memory-first organization and access patterns; do not treat SoA as universally superior to AoS.

## Parallelism, atomics and correctness

- [Maurice Herlihy, Nir Shavit et al. — The Art of Multiprocessor Programming, 2nd ed.](https://shop.elsevier.com/books/the-art-of-multiprocessor-programming/herlihy/978-0-12-415950-1): synchronization, progress, concurrent structures, correctness arguments. Essential before lock-free code.
- [Anthony Williams — C++ Concurrency in Action, 2nd ed.](https://www.manning.com/books/c-plus-plus-concurrency-in-action-second-edition): practical threading, synchronization, atomics and memory ordering.
- [Rustonomicon](https://doc.rust-lang.org/nomicon/) and [Rust Reference](https://doc.rust-lang.org/reference/): unsafe code and language model. Use exact formal constraints, not folklore.
- [Loom](https://github.com/tokio-rs/loom): concurrent Rust scheduling permutations; use for small reproducible state machines.

## Vendor manuals: target hardware authority

- [Intel Optimization Reference Manual](https://www.intel.com/content/www/us/en/developer/articles/technical/intel64-and-ia32-architectures-optimization.html): optimization guidance; pair with [SDM](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html) for ISA semantics and CPUID requirements.
- [AMD documentation library](https://docs.amd.com/): find the processor-family optimization guide (e.g. Zen 4/Zen 5) and relevant performance counter events. Use uProf for profiling when suitable.
- [Arm architecture/Neoverse documentation](https://developer.arm.com/documentation): distinguish ISA architecture guarantees from core-specific implementation details.
- [uops.info instruction tables](https://uops.info/): compare *measured* x86 throughput, latency, μops and port usage for specific microarchitectures/operand forms; cross-check against code context.

## Compiler and profiling references

- [LLVM Optimization Remarks](https://llvm.org/docs/Remarks.html): verify which loops were vectorized or missed.
- [GCC optimize options](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html): check compilation flags and PGO semantics.
- [Clang users manual](https://clang.llvm.org/docs/UsersManual.html): optimization, diagnostics and sanitizers.
- [Rust Cargo profiles](https://doc.rust-lang.org/cargo/reference/profiles.html), [rustc codegen](https://doc.rust-lang.org/rustc/codegen-options/index.html): LTO, target CPU, units, PGO.
- [Google Benchmark](https://google.github.io/benchmark/user_guide.html), [Criterion.rs](https://bheisler.github.io/criterion.rs/book/): dependable microbenchmarks, warmup/statistics and the risk of compiler eliminating work.
- [Linux perf](https://kernel.org/doc/html/latest/admin-guide/workload-tracing.html): events, call stacks, cycles and instructions.
- [Intel VTune](https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler.html), [AMD uProf](https://www.amd.com/en/developer/uprof.html): detailed hardware-counter-driven profiling, supported CPU permitting.
- [Microsoft WPR/WPA](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/introduction-to-wpr), [Apple Instruments](https://developer.apple.com/tutorials/instruments): platform-native tracing.
- [Brendan Gregg flame graphs](https://www.brendangregg.com/flamegraphs.html): reading stack-based execution profiles, including off-CPU analysis where applicable.

## Testing and native-code reliability

- [Clang AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html), [ThreadSanitizer](https://clang.llvm.org/docs/ThreadSanitizer.html), [UBSan](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html): dynamic bug detection, not formal proofs.
- [Miri](https://github.com/rust-lang/miri): Rust interpreter for many kinds of undefined behavior, with coverage limitations and restrictions around host functions/intrinsics.
- [libFuzzer with Clang](https://llvm.org/docs/LibFuzzer.html): coverage-guided fuzzing; pair with invariants and sanitizers.

## Suggested learning sequence

**Foundation (weeks 1–3):** CS:APP + systems performance methodology, write a profiled cache/stride experiment. **CPU and memory (weeks 4–6):** Hennessy/Patterson, Fog and Drepper; run assembly-annotated microbenchmarks. **Advanced (weeks 7–9):** SIMDs, profiling and Roofline, one controlled kernel improvement. **Concurrency and safety (weeks 10–12):** Herlihy/Shavit, Rustonomicon and Loom; prove a small concurrent component. **Ongoing:** study ISA/vendor manuals for the CPU you are shipping to, read rejected experiments, and maintain a benchmark/accuracy ledger.

## Research discipline

A book provides mechanisms and models; it does *not* certify one unconditional optimization trick. Inference must be based on the actual compiler output and target CPU. Cite the exact manual or source when recommending an instruction, flag, safety precondition or API. Read [SOURCES.md](../SOURCES.md) for the primary-source index.
