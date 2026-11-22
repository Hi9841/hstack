# SIMD, intrinsics, kernel engineering

## Preference order

1. Make the algorithm and layout efficient.
2. Give auto-vectorizers clear, alias-safe, contiguous loops; inspect vectorization remarks and assembly.
3. If evidence demands it, use architecture-specific intrinsics behind feature dispatch.
4. Consider hand-written assembly only when compiler codegen has a measured residual problem and maintenance budget permits.

If an intrinsics version is slower than the plain loop, the compiler possibly scheduled the plain loop better. Read both assemblies before you continue.

## Inspect the kernel's real shapes

Tiny N, narrow K, irregular tails and batch=1 inference are different from large square GEMM. Record distribution of M/N/K, alignment, reuse count, datatype, and cache residency. A microkernel that wins on 1024×1024 may lose on 1×257 or K=127.

## Kernel mechanisms

- Block M/N/K to increase operand reuse, balancing registers, L1, L2 and output store bandwidth. Follow the BLIS/GotoBLAS order: a register micro-kernel first (for example 6×16 or 8×8 outputs held in registers), then L1, L2 and L3 blocks. Tune tile sizes by measurement on each target CPU.
- Pre-pack weight panels in the exact order the inner loop reads them. Use structure-of-arrays, 64-byte alignment, and padding to the SIMD width where it removes tail loops safely.
- Order loops so that the innermost loop reads contiguous memory. Unroll to expose independent accumulators.
- Lower precision (bf16, fp16, int8, int4) moves fewer bytes and can use VNNI, AMX or dot-product instructions. It changes numerics, so apply the [quantization discipline](11-inference-and-numerics.md#quantization-discipline).
- Dequantize in registers, not to a temporary buffer in memory.
- Fuse bias, activation, scaling, normalization or softmax into the GEMM epilogue when it removes a write and a read of a full tensor.
- Consider a different algorithm when the loop is already good: Winograd or FFT for convolution, flash-attention-style tiling for attention, skipping zero or padded work, reusing repeated computation.
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

## Kernel at a wall

The tell: several small changes in a row give no gain, or the gains are less than the noise.

1. Calculate the bound again at the measured cache level. If the kernel is near the bandwidth roof, a faster loop cannot help. Move fewer bytes (quantize, pack, fuse) or do less work (a different algorithm, skip padded or zero work).
2. Run the best available library (oneDNN, OpenBLAS, BLIS, ggml, XNNPACK, Highway) on the same shapes. If it is much faster, read its micro-kernel and its assembly before you change your own.
3. Profile the full program again. The kernel is possibly no longer the bottleneck. Look for cost around it: allocation in the hot path, layout conversions, copies, synchronization, and Python or FFI boundaries.
4. Try one radical alternative (a different layout or micro-kernel shape) instead of more small tweaks.

To test one hypothesis, run 2 to 5 variants of its parameter (tile size, accumulator count, prefetch distance) in one harness on the same inputs. Print one table: time, ops per second, percent of the bound, and maximum error against the reference. Before the run, write which variant you expect to win and why. A wrong prediction shows that your model of the bottleneck is wrong. Keep the winner, write why it won, and log each variant with its result so that nobody tries a dead end again. Confirm the win end to end and on all shapes, and on each CPU class you ship to (AVX2-only, AMD and Intel).

## Model-written kernels

These rules apply when you write kernel code, and when you give kernel work to a subagent.

- Start from evidence, not "make this faster": the kernel source, the hot assembly from `perf annotate`, the counters (IPC, cache misses, top-down split), the target CPU and ISA, the shapes, and the Roofline numbers.
- Explain the bottleneck in the assembly first ("why is this loop at X% of peak?"). Then write specific variants ("3 versions with 4, 8 and 12 accumulators", "a 6×16 AVX2 FMA micro-kernel with packed B").
- Write the benchmark and the correctness harness together with the kernel.
- Use the measured results of each round ("B was 12% faster, C was wrong at the tail") as the input to the next round.

## Required tests

Test dimensions 0/1, SIMD_width±1, odd K and N, non-contiguous strides where supported, overreads at page boundary, unaligned pointers, negative/overflow integer edge cases, unusual scale factors, repeated invocations, and all supported ISAs. For SIMD unsafe blocks document pointer validity, exact bounds, alignment requirements, target feature and non-aliasing assumptions.

Sources: [Intel ISA manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [Arm architecture documentation](https://developer.arm.com/documentation), [Agner Fog](https://www.agner.org/optimize/), [LLVM remarks](https://llvm.org/docs/Remarks.html).
