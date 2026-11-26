# 00 - Feasibility report

**When:** before anything else. Read-only toward the repo under survey;
produces a report and a verdict. The single permitted write is appending to
`migration/cost-log.tsv`.
**Prerequisites:** none. **Placeholders:** `[target language]`, `[kit path]`.

---

Read [kit path]/README.md - it defines the six-step process and the prompts
that run it. Open your report by restating the six steps, one line
each. Beyond that opening index, the README is your rubric, not your evidence:
cite it only to name the step you're applying, never to support a claim about
this repo - and the case-study numbers it mentions are not estimates for this
one. Don't run the other prompts yet.

Then read this codebase and tell me what a migration to [target language]
would look like - a report, not code. Read-only commands (grep, git log, line
counts) are fine; no edits to the codebase under survey, no test runs, and
one build (plus the typecheck, if it's a separate command) - timing the
current build is your baseline. Every claim gets a file path or a count you
actually gathered; everything else is labeled an assumption. Too big to read
fully? Sample, and say what you skipped.

Start with the case for leaving: pain instances in this code, not the
language's reputation.

Then make four calls for this repo, each ending in one committed line naming
the files that forced it. A call without file paths is no call:

1. **Structure-preserving, redesign, or partial split?** Does this architecture
   translate one-to-one into idiomatic [target language], or does the move
   demand restructuring? Also test the incremental partial-rewrite alternative
   (porting only one hot component behind FFI or an internal service boundary):
   count how many times per request or hot-loop item data would cross the
   language boundary. If repeated boundary crossings and serialization erase
   the performance gain, reject the partial split and commit to a full-path
   migration once a trustworthy verifier exists.
2. **What does verification cost?** Time the current build and typecheck as
   the baseline; state the scaling assumption behind your estimate for the
   target.
3. **What is the correctness oracle, and do the tests survive?** Count the
   tests that hit the public surface versus those that import internals, which
   die with the old language. Give three examples of each. Then classify the
   oracle tier this repo actually needs:
   - **Formal rule:** an explicit spec or proof checker defines correctness.
   - **Independent public-surface suite:** existing external tests already
     cover real usage without editing tests alongside the port.
   - **Portable parity harness (`00b` Path A):** existing tests import
     internals, so build and validate a portable harness against the old code
     and mutated code before Step 1.
   - **Live-service shadow oracle (`00b` Path B + `05b`):** this is a live
     service whose feature flags, non-deterministic dependencies, or real
     traffic edge cases make any finite test suite incomplete (or porting
     coupled tests risks silent assertion weakening). Name the side effects
     that must run once only, the non-deterministic boundaries that require
     single-call replay, and any privacy constraints that forbid logging raw
     payloads.
   This is a gate, not an observation. The migration has no exit condition
   without a judge. If too little survives, the verdict must name "build the
   judge first" (`prompts/00b-judge-setup.md`, Path A or Path B) as a
   pre-Step-1 task and seed its parity scenarios or pipeline checkpoints.
4. **Is the source frozen or a moving target?** Check recent commit velocity in
   the paths under migration (`git log`). If production feature development
   continues during the migration, commit to moving-target drift controls for
   Step 6 (`prompts/05b-parity-loops.md`): a daily scan of merged source
   changes plus a merge check requiring a matching target change or an explicit
   exemption.

Then instantiate the six steps here: what each concretely means in this repo,
and which of this kit's prompts runs it - blanks filled in with this repo's
paths and units of work. Where a step needs analysis you can't do read-only,
the filled-in prompt is the answer, not a guess. Cost is a visible
multiplication - units of work × per-unit estimate - or the word unknown.

Then two sections the gate decision needs:

**Cost & duration.** A banded, order-of-magnitude token estimate for this
migration, derived from the repo you just surveyed - bands only; a precise
number is forbidden, because precise predictions will be wrong and erode
trust. Show the drivers explicitly: file count × review topology
(implementer, two reviewers, fixer per unit) × referee price. Then per
step, estimated wall-clock and active-attention minutes.

**Model plan.** Recommended model tier per phase for this repo, one line of
reasoning each - a decision I make at this gate, not a default. Tier by
blast radius: rulebook authorship and amendments → largest available model
(one-time work; every error replicates into every translated file); skeptic
reviewers → largest or mid tier, by gap complexity; high-volume translation
implementers → mid or small tier; fixers → mid tier (the compiler is the
real referee). Every post-feasibility prompt (01–06) takes my chosen models
as explicit `[model]` parameters.

End with a verdict: migrate now, later, or don't - "don't" is a valid outcome
of a fully sketched plan - plus the single fact that would change it, one this
repo can't tell you, and how you'd check it in under a day. Close with what
you read and what you ran.
Append one timestamped line for this step to `migration/cost-log.tsv` -
create it with header `step\ttimestamp\twall_clock_min\ttokens\tsubagents\tmodel`
if absent; real values where available, `unknown` where not. Plain
tab-separated values, no `key=` prefixes - a valid row looks exactly like:
`3	2026-06-11T14:02Z	21	2035336	35	claude-sonnet-4-6`
(your step number and values vary; the format doesn't).
