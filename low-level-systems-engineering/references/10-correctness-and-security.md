# Correctness is a non-negotiable performance constraint

## Define invariants before unsafe changes

- **Memory:** bounds, alignment, initialization, validity, non-overlap/aliasing, lifetimes and ownership.
- **Concurrency:** data-race freedom, publication ordering, reclamation, cancellation and linearizability where required.
- **Numerics:** exact integer overflow/saturation, quantization scales, floating-point reduction order, NaN/Inf and signed zero behavior where observable.
- **ISA:** runtime feature gate matches compiled intrinsic, fallback path exists and works.
- **I/O:** errors, partial operations, interrupted operations, malformed input and resource cleanup.

## Testing ladder

1. Existing unit and integration tests.
2. Exact differential tests against known reference for integer/binary/transcript outputs.
3. Relative/absolute tolerance tests where mathematically justified for floating outputs; beware near-zero scaling and decoder discontinuities.
4. Property-based/randomized testing over shapes, strides, alignments, tails and extreme values.
5. Fuzzing over untrusted inputs and parsers.
6. Sanitizers for native code (ASan, UBSan, TSan where supported); Rust Miri for applicable unsafe components.
7. Concurrency schedule exploration with Loom where practical.
8. Cross-ISA and cross-platform tests.
9. Real end-to-end product regression corpus and user-visible quality metrics.

## Dangerous 'optimizations'

- Reading uninitialized memory because a later stage 'usually overwrites it'. Prove every used element is written before read on all paths.
- `get_unchecked` without a tested bounds invariant; a single invalid input can cause UB.
- Transmuting element types with mismatched alignment/validity or violating alias provenance.
- Assuming FMA, reassociation or `-ffast-math` preserves decoder output.
- Conflating release/acquire with relaxed atomics for shared mutable state.
- Introducing unsupported ISA instructions outside a correctly gated function.
- Removing error checks without understanding failure semantics.

## Specific Rust guidance

Treat `unsafe` as a *local proof obligation*. Add safety comments listing preconditions for every unsafe block; keep safe public wrappers that validate them. Tests and Miri can find UB but do not constitute a formal proof. Code that is safe under one compiler may still be invalid under the Rust memory model if it relies on uninitialized values or invalid pointer aliasing.

## Release gate

No change is accepted solely on the basis of speed. Include exact-output test where required, WER/accuracy for speech applications, per-ISA test coverage, sanitizer/Miri findings if run, and a clear account of anything not verified. Inferences from a tiny test corpus must not be generalized to all inputs.

Sources: [Rust Reference UB](https://doc.rust-lang.org/reference/behavior-considered-undefined.html), [Miri](https://github.com/rust-lang/miri), [Loom](https://github.com/tokio-rs/loom), [Clang sanitizers](https://clang.llvm.org/docs/UsersManual.html).
