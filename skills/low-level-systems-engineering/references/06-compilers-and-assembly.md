# Compiler, assembly and build configuration

## Treat the compiler as a collaborator

Before manually vectorizing, inspect what the optimizer did. Use production optimization settings and realistic type/alias constraints. Common issues include missed vectorization due to alias uncertainty, unpredictable branches, library calls, integer overflow semantics or complex loop-carried dependencies.

## Useful commands

```bash
# Rust native tuning is suitable only for binaries deployed to known compatible CPUs
RUSTFLAGS='-C target-cpu=native' cargo build --release
rustc --print target-cpus
# x86 disassembly (tool names/platform syntax vary)
objdump -drwC target/release/app | less
# Clang vectorization/optimization reports
clang -O3 -Rpass=loop-vectorize -Rpass-missed=loop-vectorize -c example.c
# GCC vectorization diagnostics
gcc -O3 -fopt-info-vec-optimized -fopt-info-vec-missed -c example.c
# Intel-syntax assembly and disassembly
gcc -O3 -S -masm=intel example.c
objdump -d -M intel ./bench
# MSVC vectorization report
cl /O2 /Qvec-report:2 example.c
```

[Compiler Explorer](https://godbolt.org) shows the assembly of several compilers and flag sets side by side.

Use `cargo asm` or LLVM IR inspection where available for Rust; ensure you inspect the correct monomorphized specialization and that measurement code doesn't affect the function.

## LTO, PGO and flags

- **LTO:** interprocedural optimization may eliminate calls and enable constant propagation; can increase build time, code size and even hurt instruction-cache behavior.
- **Codegen units:** fewer can enable optimization across local units; quantify compilation and binary impacts.
- **PGO:** profile real production-like input distributions. Biased training profiles can harm rare but important paths or instruction-cache placement.
- **`target-cpu=native`:** avoids portability; use baseline x86-64/AArch64 plus runtime dispatch for distributed binaries.
- **`-O3` versus `-O2`:** higher settings are not automatically faster in branch-heavy or cache-sensitive code.
- **`-ffast-math`:** changes numerical semantics; do not enable under exact-output requirements without explicit approval and strong validation. When some accuracy change is allowed, try narrower flags first, such as `-fno-math-errno` or `-ffp-contract=fast`.

## Assembly inspection checklist

Check actual vector length, loads/stores, spills, register reuse, branches, instruction dependencies, conversion, function calls, alignment behavior, bounds checks and loop counts. The printed assembly is a hypothesis about execution; hardware counters and end-to-end timings remain necessary.

Red flags in a hot loop:

- Scalar `ss`/`sd` operations where you expect vectors. Expect the widest registers the target has (`ymm`, `zmm`) and the matching instructions (`vfmadd`, `vpdpbusd` for int8 VNNI).
- Loads and stores to the stack inside the inner loop (spills).
- Redundant loads, unexpected gathers, or shuffles and permutes that take most of the loop.
- One accumulator that carries the full dependency chain. You need about latency × issue ports independent accumulators; for an FMA with 4-cycle latency on 2 ports, that is about 8.
- Branches or bounds checks in the inner loop.
- Unaligned loads that split a cache line.

GCC, Clang and ICX vectorize the same loop differently, so compare them before you write intrinsics.

Do not trust recalled instruction latencies, throughputs or port counts. Look them up on [uops.info](https://uops.info), and model the inner loop with [uiCA](https://uica.uops.info) or `llvm-mca` to see which ports saturate.

Sources: [Cargo profiles](https://doc.rust-lang.org/cargo/reference/profiles.html), [rustc codegen](https://doc.rust-lang.org/rustc/codegen-options/index.html), [LLVM remarks](https://llvm.org/docs/Remarks.html), [GCC optimization](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html), [Clang manual](https://clang.llvm.org/docs/UsersManual.html).
