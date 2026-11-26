# Migration memory (known issues, rejected shortcuts, and distilled lessons)

Read this file before you propose a parity fix. It records human review
decisions so agents do not repeat rejected workarounds or file duplicate fixes
for a known deferred integration.

## Known issues and rejected shortcuts

When a human rejects a shortcut or defers a real fix, add one row here with the
decision, rationale, and required real fix. New workers hitting a related
fingerprint link their fingerprint row to this ID and stop.

| ID | Date | Fingerprint pattern / scope | Decision and rejected shortcut | Required real fix | Status |
|---|---|---|---|---|---|
| MEM-001 | [date] | [e.g., step=build_prompt, missing tool description] | [e.g., REJECTED hardcoding text into local files] | [e.g., call internal tool-description service] | open |

## Distilled review rules (candidates for RULEBOOK.md, lints, or tests)

Every 50 to 60 human PR review comments, cluster recurring findings here and
queue them for human approval. Once promoted to `migration/RULEBOOK.md`, a
lint, or a regression test, mark the row `promoted` and link the commit.

| ID | Review cluster (count) | Proposed rule or mechanical check | Retroactive sweep result | Status |
|---|---|---|---|---|
| RULE-001 | [e.g., guessed source edge case (6 PRs)] | [e.g., port exact source logic; never infer behavior] | [e.g., 7 existing sites found and queued] | pending |
