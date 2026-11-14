# CPU inference: kernels, quantization, decoding and accuracy

## Separate model mathematics from implementation work

Many wins come from executing the same computation with fewer temporaries, fewer conversions, better cache reuse, or less launch/synchronization overhead. Track shapes, dtype, per-layer latency, operation count, bytes read/written and decoder iterations. Avoid model simplifications unless the accuracy change is explicitly allowed.

## Kernel and activation pipeline

- For GEMM, investigate shape distribution, weight reuse, K tail behavior, tiling, SIMD packing, quantize/dequantize, FP16-to-FP32 conversion and dispatch overhead.
- For convolution, measure im2col/transposition cost relative to compute; direct and tiled convolutions have different tradeoffs.
- For attention, measure QK, softmax, AV, projections, key/value layout and cache copying separately.
- For activation chains, evaluate fusion if a full intermediate write/read can be eliminated without harming register pressure, numeric behavior or parallelism.
- For memory-mapped weights, distinguish cold page faults and stable warm reads. Repacking a model at each invocation is often costly; permanent packed weight storage may increase footprint and startup cost.

## Autoregressive decoding

Model step t may reread prefix state. If cache is repeatedly converted from token-major to head-major, aggregate layout conversion can grow quadratically in output length; an append-only representation can avoid repeated movement. **But** a head-major matrix's stride may depend on sequence capacity and consumers, so a naive append isn't automatically valid. Measure length distributions and beam-state clone costs first.

Beam search optimizations must preserve ranking, ties, masks, EOS rules, top-k semantics, and numeric stability. Replacing beam width with greedy decoding is not a behavior-preserving systems optimization.

## Quantization discipline

Specify signedness, zero points, per-channel/per-block scales, rounding, saturation, overflow range and accumulation width. Quantization typically changes numerical behavior unless it is already part of the model's established implementation; treat format changes as a separate research track with accuracy ratchets. Verify instruction semantics (VNNI, SDOT, I8MM etc.) on target ISA.

## Accuracy gates

Validate:

- Per-layer output distributions or max absolute/relative error where appropriate.
- Full decoder logits and chosen token sequences on tricky cases.
- WER/CER and named regression corpus, including silence, noisy speech, long recordings, uncommon language and odd length.
- Stability over repeated runs and different thread counts where determinism is required.
- Correct behavior across fallback ISAs, invalid input and unusual tensor shapes.

## Focus order

1. Profile model runtime by stage and shape.
2. Remove redundant model-independent work and layout materialization.
3. Improve fusion/reuse for expensive memory passes.
4. Optimize hot kernels *that are not already near a measured ceiling*.
5. Tune scheduling and decode steps if the critical path demands it.
6. Assess end-to-end changes, including WER and tail latency.

See [Trit application](../examples/trit.md) and [source index](../SOURCES.md).
