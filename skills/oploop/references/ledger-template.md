# OpLoop ledger: <project>

## Workspace and environment

- Baseline (upstream): `<path>` at `<upstream commit>`
- Prev (control A): `<path>` at `<last kept commit>`
- Work (candidate B): `<path>` on branch `oploop`
- Machine: `<CPU or GPU, cores, RAM, unified or discrete, OS>`
- Measured host rates: `<memory bandwidth, disk read rate, compute throughput, or stage floor>`
- Runtime: `<runtime and version>`
- Host settings changed: `<AC power, performance profile, lock file, restore plan>`

## Constraints and quality contract

- Memory cap: `<cap in MiB or none>`
- Scale and concurrency: `<max input size, concurrent streams>`
- Quality contract: `<lossless only | labelled lossy trades allowed>`
- Minimum useful margin: `<percent or absolute delta per journey>`
- Regression allowance: `<per protected journey>`

## Correctness floor

| Check | Command | Baseline pass/fail | Baseline failing identities | Current failing identities |
|---|---|---|---|---|
| Tests | `<command>` | `<pass>/<total>` | `<test names or none>` | |
| Typecheck | `<command>` | | | |
| Lint | `<command>` | | | |

## Journeys

| ID | Journey | Metric & runner | Bound (with assumptions) | A/A noise (median, range, n) | Current | Change vs upstream |
|---|---|---|---|---|---|---|
| J1 | | | | | | |

## Iterations

### I-001 <short name>

- Journey: J1
- Revisions: A `<prev commit>`, B `<candidate diff/commit>`
- Profile: `<file:line>` costs about N ms (M% of journey, distance to bound)
- Hypothesis: `<cause>`. `<Change>` will save about K ms (estimated cost: `<small/med/large>`).
- Test: `<existing or new test path>`
- Output check: `<check-eq digest / expect regex / validator + work count>`
- Result: A `<median>` vs B `<median>`, change `<% [95% CI]>`, p = `<value>`, blocks = `<valid>/<req>`, eligible_keep = `<true/false>`
- Protected journeys: `<all within allowance / regression details>`
- Decision: KEEP `<commit>` | REVERT (`<reason>`) | INVALID (`<env/infra cause>`)

## Plateau status

Record this block after three consecutive valid rejected hypotheses on one journey (invalid trials do not count, and a kept win resets the count).

- Journey: `<ID>`
- Best vs baseline vs bound: `<baseline -> best, distance to bound>`
- Measured limiter: `<hot spot and evidence>`
- Remaining profile-backed levers (ranked by estimated savings and cost):
  1. `<lever, estimated savings, estimated cost>`

## Qualification and system state

- Parity A/B (best measured build vs clean final): `<numbers and verdict>`
- Cumulative A/B (pinned upstream vs clean final): `<numbers and verdict>`
- Stability gate: `<full-scale / soak / sampled peak memory vs cap>`
- System state restored: `<power profile, stopped processes, removed temp files>`
- State intentionally retained: `<servers, uncommitted files, pinned branches>`
- Not verified: `<explicit gaps>`
