# OpLoop ledger: <project>

## Workspace

- Baseline: `<path>` at `<upstream commit>`
- Work: `<path>` on branch `oploop`
- Machine: `<CPU, cores, RAM, OS>`
- Runtime: `<runtime and version>`

## Correctness floor

| Check | Command | Baseline result | Current result |
|---|---|---|---|
| Tests | `<command>` | `<pass>/<total>, known failures: ...` | |
| Typecheck | `<command>` | | |
| Lint | `<command>` | | |

## Journeys

| ID | Journey | Metric | Baseline (median, range, n) | Current | Change |
|---|---|---|---|---|---|
| J1 | | | | | |

## Iterations

### I-001 <short name>

- Journey: J1
- Profile: `<file:line>` costs about N ms (M% of the journey)
- Hypothesis: `<cause>`. `<change>` should save about K ms.
- Test: `<existing test or new test path>`
- Result: A `<median>` vs B `<median>`, p = `<value>`, n = `<runs>`
- Other journeys: `<no change / regression details>`
- Decision: KEEP `<commit>` | REVERT (`<reason>`)
