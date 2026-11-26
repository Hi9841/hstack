---
name: code-migration
description: >
  Run a large-scale language migration with the six-step process and live-system
  verification loops: create the map and rules, stress-test rules, translate,
  compile, smoke-test, and prove behavioral parity via test suites, portable
  harnesses, or shadow traffic with inner, outer, and memory loops. Use when the
  user wants to migrate, port, or rewrite a codebase or live service to another
  language ("migrate this to Rust", "port our Python CLI to TypeScript", "verify
  our Rust API rewrite against production traffic", "should we rewrite this in
  Go?"), or asks for a migration feasibility assessment. Not for incremental
  JS-to-TS adoption or single-file conversions.
---

# Code migration (six-step process)

You orchestrate a language migration using the Claude Code Migration Kit.
Read C:/Users/hi/Desktop/skills/code-migration/README.md for the process and
C:/Users/hi/Desktop/skills/code-migration/CLAUDE.md for your standing rules
before you act. The standing rules override convenience: queues live on disk,
sign-off gates end workflows, the rulebook is read-only inside loops, reviewers
are adversarial and separate, and human review gates every inner-loop fix before
deployment.

## Routing

1. **No migration artifacts exist yet** (`migration/` absent): run
   `prompts/00-feasibility.md`. Produce the report (including boundary-crossing
   cost, correctness oracle class, and moving-target drift check), deliver the
   verdict, and STOP. Do not start Step 1 in the same session, even if the
   verdict is "migrate now". The human starts each phase.
1b. **Feasibility signed off, no judge yet:** confirm the correctness oracle
   before Step 1. If an independent public-surface test suite covers the real
   behavior, carry it to Step 6. If existing tests import internals, run
   `prompts/00b-judge-setup.md` Path A to build and validate a portable parity
   harness against the original and mutated code. If the target is a live
   service with combinatorial features or non-deterministic dependencies where
   tests miss production cases, run `prompts/00b-judge-setup.md` Path B to
   design and validate a shadow oracle (single-call replay, side-effect
   isolation, stage checkpoints, privacy-preserving fingerprints, and sub-second
   local checkers). STOP at its gate. Never start Step 1 without a judge.
2. **Feasibility and judge signed off, no map/rules:** run Step 1. Adapt a
   `scripts/depmap_*` for the source ecosystem (`prompts/01`), copy
   `templates/RULEBOOK.md` to `migration/RULEBOOK.md` and draft it with the
   human (the policy decisions are theirs; survey the codebase for facts),
   then run `prompts/02` for the gap inventory. Each prompt ends at its own
   gate.
3. **Step 1 signed off:** confirm that the HUMAN installed
   `.claude/settings.json` from `templates/settings.json`. Prompt 03 verifies
   it; never install it yourself. Then run `prompts/03-stress-test.md`. First
   check the rulebook's §0 posture: if this is a redesign migration, the
   bakeoff is invalid; substitute adversarial design-doc review and tell the
   human why.
4. **Stress test signed off:** confirm `migration/manifest.tsv` exists
   (prompt 01's closing action generates it), then run
   `prompts/04-translation-kickoff.md` with `scripts/queue_runner.mjs` as the
   queue. First check the referee price: if the target's typecheck is cheap,
   ask the human to remove those denies from `.claude/settings.json` at the
   gate so Step 4 dissolves into Step 3. Never edit `.claude/settings.json`
   yourself.
5. **Translation queue empty:** run Step 4 via `prompts/05-survey-build.md`
   (survey build, machine queue, and fixers without compiler access; skip
   entirely if Step 4 dissolved into Step 3), then run Step 5 (hello world and
   minimal smoke check).
5b. **Smoke tests green, behavior parity open (Step 6):** for static suites or
   portable harnesses, run the judge and triage every failure against the old
   code. For live services, shadow traffic, or high-volume parity burn-down,
   run `prompts/05b-parity-loops.md` (fingerprint grouping, fast local inner
   loop, human PR review at the seam, deployed outer loop on shadowed traffic,
   memory loop with retroactive sweeps, and moving-target drift controls).
   STOP at the Step 6 done-gate.
6. **Step 6 done-gate passed** (counts documented per README Step 6): run
   `prompts/06-post-parity.md`. Collect deferred port markers, classify
   fix-now versus document-and-close, and ship each fix as its own flagged
   change proved by a parity re-run. Ends at its own gate.

## Constant behaviors

- Report progress as burndown numbers (`queue_runner.mjs status`, matched
  shadow-traffic share, or open fingerprint counts), not prose.
- A failure seen three times is a rule bug: stop fixing instances, queue the
  rulebook amendment, sweep already-ported code for the same mistake class,
  and propose regenerating the affected slice.
- Verifiers prove output parity, not shippability: send every inner-loop fix
  through human PR review before deployment, and record rejected shortcuts or
  deferred integrations in `migration/memory.md`.
- "Don't migrate" and "stop here" are valid recommendations at every gate.
