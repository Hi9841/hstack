# Worked example: replacing scattered reads with contiguous scans

Imagine a routine that sums one field over N records. An array-of-structures (AoS) layout is natural for per-record operations but may load unrelated fields during the hot scan:

```rust
struct Record { id: u64, score: f32, payload: [u8; 48] }
fn total_score(xs: &[Record]) -> f32 {
    xs.iter().map(|x| x.score).sum()
}
```

**Hypothesis:** if the application repeatedly scans `score` and rarely touches the other fields, contiguous `Vec<f32>` storage can improve cache-line usefulness and auto-vectorization:

```rust
struct Table { ids: Vec<u64>, scores: Vec<f32>, payloads: Vec<[u8; 48]> }
fn total_score(xs: &[f32]) -> f32 {
    xs.iter().copied().sum()
}
```

**Do not prematurely declare victory.** A full application that frequently accesses all fields per record may be faster with AoS. SoA also adds maintenance complexity, requires consistent lengths, and can harm update paths. Float summation across different vectorization patterns may change rounding if arithmetic order changes.

## A rigorous experiment

1. **Target:** p50 end-to-end request latency for the real operation and CPU; secondary RSS and mutation cost.
2. **Baseline:** generate representative N (e.g., thousands to millions), data distributions, and repeated/nonrepeated scans. Record actual build, inputs, CPU and sample order.
3. **Profile:** confirm the original scan is important. Check bytes per record, cache misses and compiler vectorization.
4. **Change:** add a separate score array only if the program can keep fields synchronized with clear ownership.
5. **Correctness:** compare results under an agreed numerical policy. If strict bitwise equality is required, preserve the reduction order or do not merge the change.
6. **Benchmark:** test sparse score-only scans, whole-record scans and updates across L1/L2/LLC/DRAM working-set sizes.
7. **Decide:** retain only if end-to-end gain and correctness justify extra memory/complexity.

## Failure modes

- An impressive 'scan 1M scores' microbenchmark matters little when scan is 1% of request time (Amdahl).
- Compiler constant-folding or optimization removes test work.
- SoA doubles allocations and slows whole-record processing.
- Faster per-thread scan causes contention elsewhere under concurrency.
- Changed floating-point accumulation leads to different business/model decisions.

Read [memory and layout](../references/04-memory-layout.md), [compiler](../references/06-compilers-and-assembly.md), [models](../references/02-performance-models.md).
