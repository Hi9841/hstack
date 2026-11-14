# SIMD, intrinsics, kernel engineering

## Preference order

1. Make the algorithm and layout efficient.
2. Give auto-vectorizers clear, alias-safe, contiguous loops; inspect vectorization remarks and assembly.
3. If evidence demands it, use architecture-specific intrinsics behind feature dispatch.
4. Consider hand-written assembly only when compiler codegen has a measured residual problem and maintenance budget permits.

## Inspect the kernel's real shapes

Tiny N, narrow K, irregular tails and batch=1 inference are different from large square GEMM. Record distribution of M/N/K, alignment, reuse count, datatype, and cache residency. A microkernel that wins on 1024×1024 may lose on 1×257 or K=127.

## Kernel mechanisms

- Block M/N/K to increase operand reuse, balancing registers, L1, L2 and output store bandwidth.
- Keep independent accumulators to hide arithmetic latency; check spills and stack frame.
- Use appropriate vector tail handling: scalar tails, masks, padding (when safe), or special-case kernels. Verify no out-of-bounds access, including masked behavior on each ISA.
- Quantization paths need correct scale, zero-point, signedness, saturation, rounding and overflow behavior.
- FMA and changes to reduction order can change numeric outputs; compare logits and downstream decisions.
- Use one-time runtime ISA dispatch or legal function multiversioning. Tests must exercise scalar/AVX2/AVX-512/NEON fallback where applicable.
- For x86 compare `vpmaddubsw`, VNNI dot products and widening carefully: saturation and operand signedness semantics differ; never substitute based on names alone.

## Why attractive ideas regress

- Larger unroll/tile → spills, icache misses, fewer resident working sets.
- Wider vector → lower frequency, masked tails, more shuffles, lower occupancy.
- Gather/scatter → expensive access and poor locality vs structured loads.
- Prefetch → useless traffic or cache pollution.
- Extra prepacking → pack cost exceeds gains for short-lived weights or small batches.
- Fused operation → pressure, altered arithmetic or loss of parallelism.

## Required tests

Test dimensions 0/1, SIMD_width±1, odd K and N, non-contiguous strides where supported, overreads at page boundary, unaligned pointers, negative/overflow integer edge cases, unusual scale factors, repeated invocations, and all supported ISAs. For SIMD unsafe blocks document pointer validity, exact bounds, alignment requirements, target feature and non-aliasing assumptions.

Sources: [Intel ISA manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [Arm architecture documentation](https://developer.arm.com/documentation), [Agner Fog](https://www.agner.org/optimize/), [LLVM remarks](https://llvm.org/docs/Remarks.html).
