# Example: applying the skill to Trit CPU speech inference

**Repo:** [Hi9841/trit](https://github.com/Hi9841/trit). Inspect the checked-out version; this example reflects the architecture and ledger described in the November 2026 research snapshot and may become stale.

## The four goals and invariants

1. **Lower latency:** warm end-to-end transcription latency by named model, input length, CPU and thread count.
2. **Compute efficiency:** useful work per core/cycle in matrix products, Conformer, attention, decoder, quantization and vector tails.
3. **Memory traffic:** minimize redundant FP16 weight conversion, K/V transposes, temporary tensors, buffer-zeroing and cloning.
4. **Preserve accuracy:** no text changes under the repository's exact-output gates, no WER regression, correct odd dimensions/ISA dispatch/threading. Use repo-specific accuracy ratchets rather than invented tolerances.

## Baseline checklist

Read `AGENTS.md`, `oploop/LEDGER.md`, `Cargo.toml` and key `src/cpu`/`src/models` paths. **Do not rely on an older summary when the checked-out files differ.** Record commit and CPU. Compare kernel paths using `TRIT_KERNELS=v2` and documented selective switches. Reuse `oploop/ab.py` and the recorded corpus where available; avoid replacing the existing interleaved harness with a weaker process-level one.

Possible build and quality checks (verify the repo's current commands):

```bash
cargo build --release --workspace
cargo clippy --workspace --all-targets --release -- -D warnings
cargo fmt --all -- --check
```

## Priority hypotheses (not guaranteed wins)

### A. V2 floating-point learnings — first experiment

- Inspect `src/cpu/fgemm.rs` and `src/cpu/v2/float.rs` or current equivalent.
- Identify conversion of FP16 weight panels into FP32 scratch and scalar handling of vector tails.
- Benchmark whether on-the-fly conversion and masked loads reduce work for real Moonshine/Whisper dimensions.
- Compare integrating isolated changes into default versus selecting V2; verify AVX2, AVX-512 and ARM fallback.
- Record per-model results; historical Moonshine gains do not imply every model improves.

### B. Decoder attention and KV layout

- Inspect `src/layers.rs`, `HeadMajor`, self/cross attention and beam clones.
- Count actual repeated copies, transposes, allocations and decoder steps with source inspection and spans.
- Experiment with a capacity-stable, incrementally updated layout if the same data is repacked each token.
- Design physical strides and beam ownership before coding; decoder K and V consumers may have conflicting optimal layouts.
- Compare short/long sequences and exact transcript behavior. Declare no gain if already cached.

### C. FastConformer + Parakeet Redux

- Inspect `src/models/parts/fastconformer.rs`, `transducer.rs`, ternary/INT8 kernels and buffer pool.
- The ledger reports ternary VNNI compute near its measured single-thread throughput ceiling on a tested Zen 4 CPU. Verify on the current machine. If still true, prioritize **fewer passes/bytes, quantization overhead and model-stage scheduling** over further instruction swaps.
- Look at activation reuse, convolution input conversion, layer fusion, redundant zeroing, worker partitions and joint-network cost.
- Preserve TDT decoding, WER ratchets and special-input behavior.

### D. Decoder beam management

- Inspect `src/models/parts/beam.rs`, top-k/vocabulary scans, EOS/masking and candidate construction.
- Ledger already documents removal of vocabulary-sized vectors and rejected experiments; do not redo finished work.
- Evaluate remaining candidate buffers, beam-state copying and output projection cost; verify all supported beam rule variants and tie behavior.

## Tracked experiment table

| ID | Measurement | Hypothesis | Test | Quality gate |
|---|---|---|---|---|
| TRIT-1 | Float kernel stage + full model | Reduce FP16 conversion or scalar tail work | Isolated kernel + A/B Moonshine/Whisper | exact text, ISA equivalent |
| TRIT-2 | Decoder copies and stage time | Avoid repeated K/V layout work | short/long decode A/B | beam semantics/text |
| TRIT-3 | Parakeet encoder stages and bytes | Remove activation/materialization passes | per-stage + end-to-end | TDT WER/accuracy |
| TRIT-4 | Worker spin/wakeup and small tasks | Tune scheduling if overhead observed | thread sweep + load | deterministic, idle CPU budget |

## Reporting

For each experiment: code revision, model and clip IDs, CPU and ISA, data-shape distribution, baseline and candidate raw timings, sample counts and uncertainty, per-stage effect, exact transcript/quality gate, p50/p95 where justified, memory footprint, cross-ISA limitations, and keep/revert decision. Record failures in `oploop/LEDGER.md` following the repo's established conventions.

The skill's generic [experiment template](../templates/experiment.md) is supplemental. **Trit's own test harness and requirements take precedence.**
