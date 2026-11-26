# 05b - Parity verification loops (Step 6)

**When:** Step 6, after Step 5 smoke tests pass. Use for live-service shadow
migrations and any high-volume parity burn-down where fixing differences
requires fast local iteration, human PR review, production shadow validation,
and systemic learning.
**Prerequisites:** Step 5 smoke tests green; judge or shadow oracle validated
(`prompts/00b-judge-setup.md`); `migration/memory.md` copied from
`templates/memory.md`; `.claude/settings.json` configured per
`templates/settings.README.md` (fast local checkers allowed, heavy suites and
deployments restricted to the outer loop).
**Placeholders:** `[fixer model]`, `[reviewer model]` (from the Model plan
signed off at the feasibility gate), `[group interval]` (e.g., 10-30 min),
`[clean window]` (e.g., 24h or N consecutive check intervals),
`[parity threshold]` (human-approved match rate and open-fingerprint cap).

> Designed from Anthropic's Messages API Python-to-Rust migration, not yet
> dogfooded as a standalone kit run. See `RUN-NOTES.md`.

---

Use a workflow. In a live-system migration, code generation is fast and
verification is the bottleneck. Converge behavioral parity through **three
nested loops** (inner, outer, and memory) separated by an explicit human review
gate at the seam. Keep each loop simple around a strong verifier so the process
scales with model capability.

## 1. Group mismatches and dispatch by fingerprint

Do not send raw production diff logs to agents. A single bug can generate
hundreds of thousands of identical records.

1. Run a scheduled grouping script every `[group interval]` that clusters raw
   shadow diff records by structural fingerprint (`step`, `piece`,
   `first_diff_byte`, length gap, `hash`) and non-content feature tags.
2. Write active groups and counts to `migration/fingerprints.tsv` (columns:
   `fingerprint_id`, `step`, `piece`, `first_diff_byte`, `old_len`, `new_len`,
   `feature_tags`, `count`, `status`, `owner_or_pr`, `linked_memory_id`).
3. Alert the coordinator only when a **new** fingerprint appears or a closed
   fingerprint returns. The coordinator assigns one worker agent on
   `[fixer model]` to own each new fingerprint and opens one tracking thread
   for human visibility.
4. Expect **masking**: an early-stage or early-byte bug hides downstream
   differences. When a high-volume fingerprint drops to zero, expect older
   downstream fingerprints to surface in the next window.

## 2. Inner loop (seconds, isolated sandbox)

Each assigned worker runs inside a sandbox that holds both codebases and the
sub-second local input and output parity checkers from `prompts/00b-judge-setup.md`
(no live upstream calls, no live billing or writes).

1. **Check memory first.** Read `migration/memory.md` and `migration/RULEBOOK.md`.
   If the fingerprint matches a recorded known issue, deferred integration, or
   rejected shortcut, link the fingerprint row to that memory ID and stop. Do
   not build a second workaround.
2. **Reproduce from the blind fingerprint.** Never read customer payloads.
   Inspect the source and target code around `step` and `piece`, form a root
   cause hypothesis, and write a synthetic request or scripted upstream reply.
3. **Verify the reproduction locally.** Run the synthetic case through both
   implementations with the local checker (under one second).
   - If both versions match, your hypothesis is wrong. Revise and try again.
   - If both versions differ with the **same** checkpoint, piece, length gap,
     and first differing byte as the production fingerprint, the reproduction
     is valid. Because you wrote the synthetic case, inspect both full outputs.
4. **Fix to exact source parity.** Edit the target code so it matches the exact
   source behavior. Never guess source semantics; read the source line that
   produces the behavior. Re-run the local checker until both versions match.
5. **Lock in a regression test.** Add a test that fails on the unpatched target
   and passes after your edit. Run adversarial reviewers on `[reviewer model]`
   (separate contexts) to verify rulebook adherence and confirm no existing
   assertion was weakened.
6. **Stop at the seam.** Open one PR containing the fingerprint record, the
   synthetic reproduction, the regression test receipt, and source-line
   citations. Do not deploy directly.

## 3. Seam gate (human PR review)

Automated verifiers prove that outputs match. They do not prove that a fix is
shippable. Agents optimize for the cheapest matching output and will propose
throwaway shortcuts (such as hardcoding external service data into local files)
or erase intentional behavior differences.

At every PR seam, human reviewers decide two questions:
1. Is this a real fix, or a throwaway workaround that must be rejected?
2. Is this divergence a port bug, or an intentional change from the old system?

Approved PRs merge and enter the outer loop. Rejected PRs do not vanish: feed
them immediately into the memory loop below.

## 4. Outer loop (hours to days, shadowed live traffic)

The inner loop simulates production quickly but imperfectly. Verify every
merged fix against real shadowed traffic:

1. Deploy the approved build to staging, then production shadow traffic.
2. Compare the target fingerprint's occurrence rate on builds **with** the fix
   against builds **without** the fix, sliced by identical non-content feature
   tags (model, tools, flags, caching).
3. If the fingerprint persists or drops only partially, send the build evidence
   back to the owning worker to start a new inner-loop hypothesis.
4. Close the fingerprint in `migration/fingerprints.tsv` only after repeated
   clean checks across `[clean window]`. Reopen the task automatically if the
   fingerprint returns on a later build.

## 5. Memory loop and moving-target drift controls

The inner and outer loops fix one bug at a time. The memory loop prevents the
same mistake from recurring and keeps the port aligned with a live source tree:

1. **Save rejection and known-bug notes.** Whenever a human rejects a shortcut
   or defers a real fix (for example, an unbuilt service call), record the
   decision, rationale, affected fingerprint pattern, and real fix in
   `migration/memory.md` so later agents recognize related fingerprints without
   proposing duplicate workarounds.
2. **Sweep immediately on every new rule.** Whenever a human correction becomes
   a general rule (such as "port exact source behavior, never guess"), dispatch
   a read-only sweep agent on `[reviewer model]` across already-ported code to
   locate and queue every existing violation of that rule.
3. **Distill review comments periodically.** After every 50 to 60 human PR
   review comments, run an agent to cluster recurring findings and propose new
   rules for `migration/RULEBOOK.md` or `CLAUDE.md`. Apply them only after
   human editing and sign-off.
4. **Promote rules to mechanical checks.** Convert repeated review findings into
   permanent regression tests and lint rules that fail CI automatically.
5. **Control moving-target drift** (required if feasibility call #4 marked the
   source as active):
   - Run a daily agent scan of merged source-language commits to flag behavior
     changes that the target implementation must mirror.
   - Enable a repository merge check that requires every PR modifying the old
     implementation to include a matching target change or an explicit
     exemption.

## Human posture and Step 6 done-gate

Move human effort progressively outward across the migration: calibrate the
verification signal first, then review at the inner/outer PR seam, and finally
work at the outer edge authoring rules, lints, and merge checks.

Stop at the Step 6 done-gate and report mechanical receipts (never narrated
totals):
- Shadowed traffic match rate (7-day median) against `[parity threshold]`.
- Open, closed, and memory-linked counts from `migration/fingerprints.tsv`.
- Original suite pass count on the original code (zero inherited failures
  unaccounted for) plus total regression tests added.
- Unmirrored source-commit count from the drift scanner (must be zero or
  explicitly exempted).
- Pending rulebook amendments and `migration/memory.md` entries.

Nothing cuts over to live traffic and `prompts/06-post-parity.md` does not
start until the human signs off on the Step 6 done-gate.
Append one timestamped line for this step to `migration/cost-log.tsv` -
create it with header `step\ttimestamp\twall_clock_min\ttokens\tsubagents\tmodel`
if absent; real values where available, `unknown` where not. Plain
tab-separated values, no `key=` prefixes - a valid row looks exactly like:
`6	2026-06-11T14:02Z	21	2035336	35	claude-sonnet-4-6`
(your step number and values vary; the format doesn't).
