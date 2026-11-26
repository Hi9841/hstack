# 00b - Judge setup

**When:** after the feasibility gate signs off "migrate," before Step 1. Choose
**Path A** when the feasibility report's call #3 found coupled internal tests
for a deterministic library, CLI, or bounded service. Choose **Path B** when
call #3 classified this repo as a **live service** whose combinatorial feature
space, non-deterministic dependencies, or real traffic edge cases make finite
tests insufficient. If an independent public-surface suite already covers real
usage, skip this prompt and carry that suite into Step 6.
**Prerequisites:** signed-off feasibility verdict; the call #3 test census and
oracle classification.
**Placeholders:** `[target language]`, `[reviewer model]` (from the Model plan
signed off at the feasibility gate).

> Designed, not yet dogfooded as a standalone kit run - see RUN-NOTES. Path A
> addresses Run 1's late-judge comparator bugs; Path B encodes Anthropic's
> Messages API shadow-oracle design. Treat the output as a draft to validate
> mechanically, not a verdict to believe.

---

Use a workflow. The migration has no exit condition until a **judge** exists: a
verifier that evaluates the original code and the port on equal terms, so "are
we done?" has a mechanical answer instead of a feeling. The original code is
the executable spec; the judge is how you query it. Build and validate it now,
while the old code still runs and nothing has been translated to bias you.

## Path A: Portable parity harness (deterministic libraries, CLIs, bounded services)

The judge must run against **both** implementations through the same external
interface (CLI, HTTP, file I/O, or exported API), never through source-language
internals. Never let one unreviewed agent port both production code and tests:
ported suites quietly lose assertions. Three steps:

**1. Categorize.** Take the call #3 census and confirm it against the source:
classify every existing test as **portable** (expressible as an external call
that both implementations answer) or **internal-bound** (depends on functions,
private state, or language features that will not exist in [target language]).
Internal-bound tests are not judge material. Note what behavior they guard so
it is not lost, and leave them behind. Report both counts as a grep/file
receipt, not a narrated total.

**2. Rewrite for portability.** Convert the portable tests into assertions that
run against both old and new through the external interface with identical
inputs and mechanical output diffs. Where no test exists for behavior the old
code clearly has, add real-world scenarios diffed against the original. Then
have two **adversarial reviewers**, in separate contexts and disjoint batches,
check that no rewrite weakened an assertion (no loosened tolerance, no dropped
field, no `assert truthy` replacing an exact value check). Run them on
[reviewer model], per the Model plan. Inheriting the session default is a
deviation; log it. Every confirmed weakening is a bug in the rewrite; fix the
harness and resample.

**3. Validate the judge against known answers.** A judge you have not tested is
a guess. Run the full harness against the **original** code: it must pass
clean, because the spec passes its own spec. Then run it against **deliberately
broken** original code: mutate a handful of behaviors by hand (flip a
comparison, drop an error path, change an output format) and confirm that the
judge **fails** on each. Report both runs: N/N pass on the original, and one
caught failure per injected mutation.

## Path B: Live-service shadow oracle (combinatorial production services)

When live traffic is the only complete specification, unit and integration
tests are necessary but never sufficient (a port can pass ~98% of ported tests
while matching only a quarter of live requests). Design and validate a
production shadow oracle plus fast local inner-loop checkers before Step 1:

**1. Isolate side effects.** List every mutating or billable operation on the
request path (billing, rate limits, quotas, database writes, external
webhooks). Design the shadow harness so side effects execute **once only** on
the authoritative old path. Prove structurally that a shadowed copy can never
double-bill, double-count, or double-write.

**2. Isolate non-determinism by single-call replay.** List every
non-deterministic dependency (LLM inference, RNG, clocks, upstream services).
Do not use naive "run old twice and ignore varying fields" diffing: on a
non-deterministic reply, that marks the entire output as noise and hides real
bugs. Call the non-deterministic dependency **once** on the live path, capture
its exact response, and **replay** that response into the shadow output path.

**3. Define pipeline checkpoints.** Break the request and response lifecycle
into ordered stages before and after each non-deterministic boundary (for
example: validate request, resolve settings, build upstream payload, parse
upstream stream, format response, compute usage). Compare old and new outputs
at every stage, and piece-by-piece inside structured payloads, so the **first
divergent checkpoint** locates the defect in code.

**4. Specify privacy-preserving structural fingerprints.** When user payloads
cannot be logged or read by engineers or agents, forbid raw text in diff
records. Emit only structural metadata per divergence:
- `step` (checkpoint name)
- `piece` (sub-component or field index)
- `first_diff_byte` (first differing byte or token offset)
- `old_len` and `new_len` (payload sizes on each side)
- `hash` (structural signature for deduplication)
- Non-content request tags (`build_id`, feature flags, model or route class)
  so outer-loop monitors can compare builds on identical traffic slices.

**5. Build sub-second local inner-loop checkers.** Build two local dual-run
tools that run both implementations in one sandbox with zero live upstream or
billing calls:
- **Local input checker:** takes a synthetic request, executes both input
  pipelines up to the non-deterministic boundary, and prints the exact full
  diff (safe because the agent wrote the synthetic input). Target runtime:
  under one second.
- **Local output checker:** feeds a scripted upstream reply through both output
  pipelines and prints the exact full diff. Target runtime: under one second.

**6. Validate the shadow oracle against known answers.** Run two copies of the
original implementation through the oracle and confirm: (a) N/N identical pass
with zero false diffs, (b) side-effect counters increment once only, (c)
injected mutations on both input and output stages trigger the exact expected
checkpoint and fingerprint, and (d) an automated privacy scan finds zero
payload text in emitted diff records. Run two adversarial reviewers on
[reviewer model] to audit the replay boundary, side-effect isolation, and
privacy filter.

---

Stop and show me the harness or shadow-oracle design, the counts (portable
versus internal-bound tests, or checkpoints and non-deterministic boundaries),
the reviewer findings, and every validation run (clean pass, caught mutations,
and privacy/side-effect receipts for Path B). Nothing in Step 1 starts until I
sign off that the judge is real. Keep this judge under version control and keep
it running until the end.
Append one timestamped line for this step to `migration/cost-log.tsv` -
create it with header `step\ttimestamp\twall_clock_min\ttokens\tsubagents\tmodel`
if absent; real values where available, `unknown` where not. Plain
tab-separated values, no `key=` prefixes - a valid row looks exactly like:
`3	2026-06-11T14:02Z	21	2035336	35	claude-sonnet-4-6`
(your step number and values vary; the format doesn't).
