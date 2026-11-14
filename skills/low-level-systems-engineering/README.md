# Low-Level Systems Engineering — coding-agent skill

A reusable, source-grounded skill for improving latency, throughput, CPU efficiency, memory use, and correctness in native systems software. The entry point is [SKILL.md](SKILL.md); detailed technical modules load on demand.

## Installation

Unzip this archive. Point a coding agent's skill loader at the **directory containing `SKILL.md`**. For agents that use repository-local skills, copy `low-level-systems-engineering-skill/` under the tool's documented skills directory (for example `.agents/skills/` or `.claude/skills/`, if that agent supports those locations). Directory conventions vary by agent version; check its instructions.

Example:

```bash
unzip low-level-systems-engineering-skill.zip
# Then copy the resulting directory into your agent's configured skills path.
```

The skill is not a compiler extension or runtime dependency. It provides instructions, checklists, sources and optional helper scripts. The scripts do not automatically modify your repository.

## Contents

- `SKILL.md` — concise operational behavior and reference routing
- `references/` — 11 deep topic guides plus annotated books/papers/manuals
- `examples/trit.md` — CPU-first Rust speech inference application
- `examples/hot-loop-review.md` — worked reasoning example
- `templates/` — repeatable experiment and reporting structures
- `scripts/` — repeatable benchmarking, statistical comparison, exact-output checking, Roofline estimator, profiling, and validation
- `SOURCES.md` — primary-source links, scope and reliability notes

## Typical use

Ask the agent to 'Use the low-level systems engineering skill to profile and optimize [specific operation] while preserving [correctness constraint] on [target machine].' The agent should baseline, investigate, implement an isolated change, test, and report measurements. If it has no machine access, it should provide a hypothesis and exact experiments rather than inventing results.

## Script quickstart

```bash
python3 scripts/check-skill.py
python3 scripts/bench.py --warmups 3 --rounds 12 --output before.json -- ./app sample.dat
python3 scripts/bench.py --warmups 3 --rounds 12 --output after.json -- ./app-new sample.dat
python3 scripts/compare_bench.py before.json after.json
python3 scripts/roofline.py --operations 1e9 --bytes 5e8 --peak-ops-per-second 1e12 --bandwidth-bytes-per-second 1e11
```

The simple benchmark helper times processes, including their startup. For tiny kernels use an in-process harness (Criterion, Google Benchmark, or calibrated internal microbenchmarks), then **confirm with the real application**. Interleave baseline and candidate runs manually or use an A/B harness to reduce drift.

## Important constraints

Information here summarizes public technical guidance; it does **not** reproduce commercial textbooks or vendor manuals. Target-specific advice is conditional on CPU generation, compiler version, and workload. The reference bibliography links to original sources and official docs. Correctness and security gates must never be bypassed to claim a speedup.
