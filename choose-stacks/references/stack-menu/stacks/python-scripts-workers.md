# Python automation + AI

Scripts, integrations and workers close to the Python data and AI ecosystem.

Language: Python | Reviewed: 2026-10-10 | Evidence: documentation-reviewed research input

Source record: menu/inputs/research/python.json.

Core guidance checked: 2026-10-13. Review sources are listed below. /research-freshness.json describes the imported research packet; this record retains its own evidence scope. These recipes and selected dependency combinations need qualification in the actual project.

## Application role
Components: automation
UI: none
Deployment: server

## Use cases
- Reusable automation scripts
- Scheduled imports and transformations
- Model/tool orchestration workers

## Fit
- The deliverable is a bounded task or worker rather than a web product
- Python SDKs or data libraries materially simplify integrations

## Choose something else when
- A one-off script is being expanded into an undocumented product backend
- Hard real-time deadlines or a native deployment requirement dominate

## Agent workflow
- Read README, dependency manifests, lockfiles, runtime pins and the maintained project workflow before changing anything. Preserve an existing stack unless reconsidering it is part of the request.
- For a new component, read the Generators section before writing application files. Use its appropriate official initializer and retain its generated baseline; follow-up generators are conditional on the selected feature.
- Use this guide to select tools by requirement. Resolve compatible versions from official and installed-version documentation; record the actual lockfile and runtime versions.
- Create a plan for schema changes, identity, authorization, external effects and deployment. A library choice does not complete its integration.
- Run relevant checks after configuration. Exercise the real interface, failure paths and packaged artifact on the intended target. Report commands, versions, results and untested behavior.
- On failure, retain the command and diagnostic, fix the failing prerequisite and resume there. Do not regenerate over existing work or suppress failures to make a check green.

## Best practices
- Use scoped credentials, explicit timeouts and bounded concurrency for external calls.
- Validate model outputs and tool inputs; keep approval boundaries separate from model reasoning.
- Test with deterministic fake services and recorded fixtures, including partial failure and replay.
- Use a durable workflow engine only when restart recovery is required; make external effects idempotent.

## Generators: create the baseline first

Generator documentation reviewed: 2026-10-18. Evidence: documentation-reviewed; commands not executed.

### Required workflow

- Before writing a new project's application files, read its profile's starting points and use the official framework or language initializer appropriate to the component. Do not hand-recreate a generated skeleton. Where no full application generator exists, use the documented module/package initializer and assemble only the missing application pieces.
- Choose one starting point per component. Check the installed generator's version and help, prerequisites, template, database, UI, test and runtime options. Commands are examples: replace names and paths, resolve compatible versions, and record the exact invocation and selected options. Do not blindly run every listed generator.
- Generate in a new empty destination. For an existing repository, preserve its conventions and use relevant incremental generators. If a baseline comparison is needed, generate a separate disposable reference with matching versions/options and reconcile deliberately; never regenerate over existing work.
- Keep applicable generated configuration, hidden files, formatter/linter settings, ignore rules, manifests, lockfiles, tests, wrappers and entry points. Extend them for the project instead of replacing them with abbreviated handwritten copies. A generator may initialize version control or offer a commit; respect the user's Git instructions.
- Run the generated baseline's documented checks before feature changes, then relevant checks after configuration and implementation. Inspect what version control would include, including hidden files, build output, local secrets and operating-system metadata. Add needed ignore rules explicitly: no generator guarantees that .DS_Store or every local artifact is ignored.
- Use follow-up generators only when their feature or tool is selected. Review generated changes and dependencies, apply required migrations in the intended environment, and exercise the generated behavior. Scaffolding does not establish authorization, safe retries, production readiness or every best practice.
- If the required generator, template or IDE is unavailable, report the missing prerequisite and the documented route. Do not silently substitute a handwritten scaffold. Keep documentation review, generator execution, baseline checks and application qualification as separate evidence.

### Choose a starting point

#### Packaged uv application for maintained automation or a worker

Use when: Reusable modules, a CLI entry point, tests or a long-lived worker warrant a maintained project.

1. Install uv and inspect uv --version and uv init --help. Replace /path/to/local/source with an existing local source parent; use a new, absent target directory. Set PYTHON_VERSION to a supported Python minor compatible with the selected framework and dependencies. Record generator versions, selected flags and deliberate deviations.
2. Generate the packaged application, retain its importable src/worker_app package and generated console entry point, and replace the sample behavior with the bounded task or worker.
3. Install only required SDKs and configure tests, explicit inputs, credentials, timeouts and restart/checkpoint behavior. A Python project generator does not provision a queue, scheduler or orchestration service.

Working directory: /path/to/local/source

Generate a packaged application and console entry point, explicitly selecting packaging across uv versions.

```sh
uv init --app --package --python "$PYTHON_VERSION" worker-app
```

Working directory: /path/to/local/source/worker-app

Resolve the project lock/environment and install the generated package.

```sh
uv sync
```

Working directory: /path/to/local/source/worker-app

Smoke-test the generated console entry point before adapting it to application behavior.

```sh
uv run worker-app
```

- Use --lib instead when the actual deliverable is a distributable library consumed by other projects. Do not choose library semantics solely because the code contains reusable functions.
- The generic package generator supplies structure, not Celery tasks, Temporal workflows or safe retry semantics. Add the chosen worker integration only when required.
- Choose a source parent outside another uv workspace, or intentionally use --no-workspace for an independent project under parent project metadata.

#### Standalone script with inline dependency metadata

Use when: A small, independently executable file is the actual deliverable; promote shared logic to a package when it grows.

1. Install uv, choose a supported Python minor, and set PYTHON_VERSION accordingly. Use an existing local script folder and a new task.py; replace /path/to/local/scripts with that folder.
2. Generate the script, add only its required dependencies, implement the task, and create its adjacent lockfile for reproducible execution.

Working directory: /path/to/local/scripts

Generate a standalone Python script with inline metadata.

```sh
uv init --script task.py --python "$PYTHON_VERSION"
```

Working directory: /path/to/local/scripts

Example only when HTTPX is required: declare a script dependency in its metadata.

```sh
uv add --script task.py httpx
```

Working directory: /path/to/local/scripts

Generate task.py.lock; standalone scripts do not use a project uv.lock.

```sh
uv lock --script task.py
```

Working directory: /path/to/local/scripts

Execute the script with its declared and locked dependencies after fixture-safe implementation.

```sh
uv run --locked task.py
```

- The HTTPX dependency is conditional. A standard-library-only script needs no extra package. Inline script metadata owns script dependencies; do not add a redundant pyproject.toml merely to run one file.
- Keep task.py.lock with the script when reproducibility is required. For execution within a surrounding uv project, inspect project discovery and choose --no-project when the script should be independent.

### Conditional follow-up generators

#### Conditional Alembic migration environment and revisions

Use when: SQLAlchemy-backed persistent state is required; skip for stateless APIs/workers and preserve an existing migration owner.


Working directory: /path/to/local/source/worker-app

Install the selected PostgreSQL data dependencies; use a compatible driver for another chosen database.

```sh
uv add sqlalchemy alembic "psycopg[binary]"
```

Working directory: /path/to/local/source/worker-app

Generate the standard migration environment and config.

```sh
uv run alembic init migrations
```

Working directory: /path/to/local/source/worker-app

After configuring env.py metadata and database access, generate a candidate schema revision.

```sh
uv run alembic revision --autogenerate -m "initial schema"
```

Working directory: /path/to/local/source/worker-app

After manual review, apply the candidate migration to a disposable development database.

```sh
uv run alembic upgrade head
```

- Between init and revision, configure the database URL from environment-owned secrets and target_metadata from the application models. The default generic template is synchronous; use alembic list_templates and choose the async template only for an actual async DBAPI.
- Autogeneration cannot reliably infer every rename, constraint or data transformation. Review upgrade/downgrade operations and write data migrations intentionally; do not blindly apply its output.
- Commit migrations, env.py and the non-secret configuration, while keeping database credentials out of source. Verify upgrades and required rollback behavior before release.

### Preserve the generated foundation

- Keep generator-created project metadata, Python requirements, version selection and ignore rules; extend them rather than replacing them with a handwritten approximation.
- Commit the resolved uv.lock for projects; exclude .venv, caches, secrets and platform debris such as .DS_Store. Do not hand-edit lockfiles.
- Keep source repositories, virtual environments and caches in a local development workspace outside cloud-synced document folders.
- For the packaged application, retain its generated build backend, src layout and console-script mapping; resolve dependency changes through uv.
- For standalone scripts, preserve inline metadata and the adjacent task.py.lock rather than substituting a project uv.lock.
- Keep fixtures and dry-run modes separate from live side effects; document scheduling, non-overlap and failure-resume behavior before operational use.

### Baseline and generation checks

- For the packaged branch, from /path/to/local/source/worker-app run uv sync --locked and uv run worker-app using fixtures or an implemented dry-run mode; verify the packaged import and entry point after build/install when distributing.
- For the script branch, from /path/to/local/scripts run uv run --locked task.py in a fixture-safe mode; verify its adjacent lockfile and Python requirement.
- Run configured lint/type/test checks, then test explicit exit codes, malformed inputs, cancellation, bounded retries and partial failures at real effect boundaries.
- Compare the same uv-version/flag scaffold in a disposable folder; inspect tracked/staged files for environments, caches, secrets and .DS_Store. Conditional Alembic checks require a configured disposable database.

### Generation receipt

- Component and selected starting point, or the documented absence of a full application generator
- Generator/toolchain versions, exact commands or IDE template/settings, working directory and generated destination
- Generated files retained, deliberate deviations with reasons, and required supplemental ignore rules
- Baseline checks and later checks actually run, results and remaining prerequisites or untested behavior

### Generator sources

- [uv project creation and layout choices](https://docs.astral.sh/uv/concepts/projects/init/)
- [uv project dependency and environment workflow](https://docs.astral.sh/uv/guides/projects/)
- [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
- [uv script generation, inline metadata and adjacent lockfiles](https://docs.astral.sh/uv/guides/scripts/)
- [Alembic environment generation and templates](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Alembic candidate revision generation and limitations](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
- [uv command reference: explicit package and workspace options](https://docs.astral.sh/uv/reference/cli/)

## Tools

### Packaging and environments: uv + pyproject.toml + committed uv.lock

One project entry point for dependencies, Python selection, execution and reproducible sync.

Limits and integration: Pin a compatible Python minor and resolve actual package versions at implementation; do not hand-edit uv.lock. Keep environments and caches in a local development workspace.


- https://docs.astral.sh/uv/guides/projects/

Alternatives: Preserve an existing maintained packaging workflow

### Lint and format: Ruff

Fast lint and formatting feedback with one configuration.

Limits and integration: Ruff does not replace static typing, tests, authorization checks or runtime validation.


- https://docs.astral.sh/ruff/installation/

Alternatives: Preserve existing configured formatter/linter

### Static typing: mypy

Explicit checks on application boundaries with a conservative established checker.

Limits and integration: Configure strictness and third-party stubs; unchecked Any and untyped functions reduce coverage. No checker performance comparison was run.


- https://mypy.readthedocs.io/en/stable/getting_started.html
- https://docs.astral.sh/ty/type-checking/

Alternatives: ty after project-specific compatibility trial

### Testing: pytest with deterministic fake external services and captured fixtures

Fast repeatable tests can verify parsing, permissions and retry decisions.

Limits and integration: Add adversarial outputs and partial-failure cases for agents; do not confuse output snapshots with task success.


- https://docs.pytest.org/en/stable/getting-started.html

Alternatives: Integration suites against sandbox services

### Validation: Pydantic at configuration, tool-input and model-output boundaries

Reject malformed external structures before effects.

Limits and integration: Define strictness intentionally; a validated plan still needs permission and domain checks.


- https://pydantic.dev/docs/validation/latest/concepts/strict_mode/

Alternatives: Standard-library dataclasses for trusted internal values

### External I/O: Provider-supported Python SDK or HTTPX with explicit timeouts and bounded concurrency

Centralize transport settings, credentials and test seams.

Limits and integration: Configure total task deadlines as well as network inactivity timeouts; avoid retry storms and duplicated writes; redact credentials from logs.


- https://www.python-httpx.org/advanced/timeouts/

Alternatives: Standard-library clients for small dependency-free work

### Persistence and migrations: No database for stateless scripts; PostgreSQL + SQLAlchemy/Alembic for shared durable business state

Avoid introducing infrastructure before state ownership requires it.

Limits and integration: Files need atomic writes/checkpoints; database state does not automatically resume execution. Review migrations and use task-local sessions.


- https://docs.sqlalchemy.org/en/21/orm/session_basics.html
- https://alembic.sqlalchemy.org/en/latest/autogenerate.html

Alternatives: SQLite for one-machine local state

### Auth and credentials: Scoped service credentials injected by the execution platform

Workers generally need service authorization rather than user login UI.

Limits and integration: Credential storage/provider is deployment-specific and unselected; keep secrets out of source, fixtures, task payloads and output.


- https://docs.astral.sh/uv/guides/integration/docker/
- https://www.python-httpx.org/advanced/timeouts/

Alternatives: Delegated user OAuth when required by the integration

### Long-running durable agents: Temporal Python SDK when recovery across restarts is required

Persisted workflow orchestration and separate worker processes suit retries, pauses and human waits.

Limits and integration: Adds a service and operational cost. Keep external I/O in activities, make side effects idempotent, test replay and cancellation; no end-to-end integration was run.


- https://docs.temporal.io/develop/python
- https://docs.celeryq.dev/en/stable/userguide/tasks.html

Alternatives: Celery for independent queued jobs; direct function for bounded work

### Execution and deployment: uv-managed package and explicit CLI entry point; separate managed worker process for persistent workers

Make inputs, exit codes and restart behavior reproducible.

Limits and integration: Scheduler/platform is unselected; document non-overlap and checkpoint semantics. Do not add a web server just to run a job.


- https://docs.astral.sh/uv/guides/projects/
- https://docs.astral.sh/uv/guides/scripts/
- https://docs.astral.sh/uv/guides/integration/docker/

Alternatives: uv script metadata for a small standalone file; Scheduled container for bounded jobs

### Application logging: Python logging with configured handlers

Shared standard logging captures application and dependency diagnostics

Limits and integration: Configure logging at entry point, redact credentials and add request/job IDs, duration and failure context. Persist logs on the execution platform; metrics/tracing backend is a separate operational choice.


- https://docs.python.org/3/library/logging.html

Alternatives: Preserve an existing compatible project choice

### Bounded external-call retries: Tenacity only for retryable transient failures

Explicit stop/wait/filter rules support controlled retries

Limits and integration: Install tenacity; set attempt/deadline limits, jitter and exception filters. The bare decorator retries forever without delay; do not stack retries with SDK/worker retries or repeat non-idempotent effects without keys.


- https://tenacity.readthedocs.io/en/latest/

Alternatives: Provider SDK retry policy when sufficient

### Object storage: Boto3 S3 client when durable objects are required

Official SDK supports file transfer to S3

Limits and integration: Install boto3 only for S3-backed work; use platform credentials, private keys and bounded transfers. Boto3 is synchronous: keep blocking transfers out of an async event loop; verify alternative provider compatibility.


- https://docs.aws.amazon.com/boto3/latest/guide/s3-uploading-files.html

Alternatives: Preserve an existing compatible project choice

### HTTP timeouts: HTTPX client timeouts and connection limits

Connect/read/write/pool deadlines prevent unbounded remote waits

Limits and integration: Configure shared client timeout and limits; retain overall operation deadline separately because read timeout measures inactivity between chunks. Close clients and redact request logs.


- https://www.python-httpx.org/advanced/timeouts/

Alternatives: Preserve an existing compatible project choice

## Architecture and developer workflow

Recommendation: a maintained package owns validated inputs, a run/effect ledger, a CLI result contract and a bounded execution loop. A short task may run directly under a scheduler; independent queued jobs fit Celery when broker semantics are qualified; long waits and restart recovery may justify Temporal workflows with external effects in Activities. A prompt, validated model output or log is not proof of a completed effect.

Version scope: Python APIs: TaskGroup/asyncio.timeout require 3.11+; inspected /3 docs currently show 3.15.0. Use a supported minor compatible with selected SDKs and lock it; this does not recommend blindly upgrading to 3.15. Reviewed uv current guides, HTTPX current guides, Celery 5.6.3 task docs and Temporal Python guides. Resolve actual SDK versions in uv.lock before qualification.
Reviewed: 2026-10-11 | Evidence: documentation-reviewed | Source record: inputs/research/migrations-systems.json

### Architecture boundaries

- Recommendation: separate parsing/validation, pure transformation, provider adapters and effects. Use deterministic fixtures/dry-run for decision logic, scoped injected credentials and stable operation IDs; do not place secrets or raw provider tokens in run payloads.
- Recommendation: reuse HTTPX clients with explicit connect/read/write/pool timeouts and connection limits; add a total task deadline and bounded TaskGroup/semaphore or worker-queue execution. Connection limits alone do not bound all queued coroutines.
- Recommendation: persist source cursor, input/schema version, effect intent and acknowledged result where restart matters. One-machine SQLite can own local state; shared workers need a chosen shared durable store and lease/ownership model. A checkpoint is not atomically committed with a remote email or payment.
- Recommendation: in Temporal, deterministic Workflow code orchestrates Activities, waits and retries; Activities perform provider calls and heartbeat progress. In Celery, configure acknowledgement/redelivery and retry policy to the task's replay semantics. Avoid layering unbounded SDK, decorator and worker retries.

### Tools and feedback

- Recommendation: inspect existing scheduler, dependencies, input formats and receipts. For maintained local work, uv init --package worker-app creates a package; pin a supported Python minor, add SDK/validation dependencies and commit pyproject.toml plus uv.lock in the maintained source repository.
- Recommendation: uv sync --locked, uv run ruff check ., uv run mypy src and uv run pytest require the corresponding dev tools configured/installed. Add fixtures for malformed provider/model output, permission failures, partial effects, ambiguous acknowledgements and resume.
- Recommendation: define [project.scripts] for the package CLI and structured JSON results plus explicit success/usage/failure statuses. uv run --locked <entrypoint> uses the locked project; scheduler start, overlap policy, termination and resume command are deployment-owned choices.
- Recommendation: for durable orchestration, uv add temporalio and implement Workflow/Activity/Worker components connected to a separately operated Temporal service. Replay representative histories with temporalio.worker.Replayer before workflow changes; test Activity heartbeat/cancellation and time-skipping integration flows.
- Recommendation: use uv sync --locked --no-dev inside a reviewed container build, then record the actual entry point, writable state path, credential scopes and dependency/image pins. No scheduler, broker or Temporal integration was executed here.

### Translations to avoid

- Avoid resuming by rerunning every input: a crash after remote success before checkpoint creates ambiguous effects and needs reconciliation or a provider idempotency key.
- Avoid synchronous SDK calls in async execution; use a documented async client or bounded offload, with explicit cancellation limits.
- Avoid swallowing CancelledError in TaskGroup work; cooperative cancellation depends on it being propagated after cleanup.
- Avoid describing Celery late acknowledgement or a Temporal Workflow as exactly-once external effects. Application/provider idempotency remains necessary.
- Avoid importing time/random/network behavior into deterministic Temporal Workflow code; move external I/O into Activities and replay-test changes.

### Architecture sources

- [uv projects](https://docs.astral.sh/uv/guides/projects/): Project/package entry points, lockfile-based execution and dependency management are documented.
- [uv Docker](https://docs.astral.sh/uv/guides/integration/docker/): Locked/no-dev sync and build/runtime environment setup are explicit.
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html): Transactions and persisted local state are available; transaction control and concurrency need deliberate configuration.
- [Python os.replace](https://docs.python.org/3/library/os.html#os.replace): Replacement can be atomic on success and can fail across filesystems; sync/durability is separate.
- [Python asyncio tasks](https://docs.python.org/3/library/asyncio-task.html): TaskGroup/timeout require 3.11+ and use cancellation; swallowing cancellation breaks structured behavior.
- [Python asyncio synchronization](https://docs.python.org/3/library/asyncio-sync.html): Semaphore supports bounded task access and is not thread-safe.
- [HTTPX timeouts](https://www.python-httpx.org/advanced/timeouts/): Connect/read/write/pool timeouts are separate; read timeout concerns waiting for chunks.
- [HTTPX resource limits](https://www.python-httpx.org/advanced/resource-limits/): Connection and keepalive pool bounds are configurable.
- [Celery 5.6.3 tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html): Idempotency, acknowledgements, retries and worker-loss behavior need explicit policy; late ack has exceptions.
- [Temporal Python Workflow basics](https://docs.temporal.io/develop/python/workflows/basics): Workflow code must respect deterministic/replay constraints.
- [Temporal Activity basics](https://docs.temporal.io/develop/python/activities/basics): Activity definitions and worker registration place external work outside deterministic Workflow code; idempotency has a separate concept source.
- [Temporal Activity timeouts](https://docs.temporal.io/develop/python/activities/timeouts): Activity timeouts, retry policies and heartbeats support bounded/recoverable execution.
- [Temporal Python testing](https://docs.temporal.io/develop/python/best-practices/testing-suite): Replay checks history compatibility; Activity and time-skipping environments support recovery testing.
- [Temporal Activity idempotency](https://docs.temporal.io/activity-definition): Activities may execute more than once after an unreported completion; completed Activities are not rerun merely by Workflow replay. Provider idempotency keys are enforced by the called service.

## Transition options

Proposed designs and checks; these are not executed compatibility results.

### CLI and pipe contracts

**Inspect the source:** Capture old script arguments, environment/config precedence, file paths, exit codes and scheduler invocation behavior.

**During coexistence:** Recommendation: retain the old script as a thin entry point into an importable package while callers transition. Introduce structured output/version fields and an explicit noninteractive/dry-run mode without changing live side effects.

**Target design:** Recommendation: uv package with pyproject.toml entry point, committed uv.lock and supported Python minor; JSON results on stdout, diagnostics on stderr, schema and status policy in the CLI documentation.

**Rollback:** Recommendation: restore the previous package/environment and command while preserving versioned run/checkpoint files. Keep the old entry point until every scheduler/caller is migrated.

**Benefits and prerequisites**

- An importable locked package makes repeated automation easier to test and invoke consistently. Requires: Inputs/entry point/status are defined; compatible Python and SDKs are pinned; scheduler uses the same package build. Tradeoffs: A lockfile does not fix provider behavior or scheduler overlap; deploy-time environment/credentials remain required.

**Checks before transfer**

- Run old scheduler command against the package adapter and compare input/output/status.
- Start from a clean locked environment and parse output without progress/log contamination.
- Verify dry-run performs zero provider writes and reports the intended actions.

- https://docs.astral.sh/uv/guides/projects/
- https://docs.astral.sh/uv/guides/integration/docker/

### Data and schema

**Inspect the source:** Identify source pagination/cursors, input revisions, item identifiers, partial outputs and acknowledged versus uncertain effects.

**During coexistence:** Recommendation: introduce a run/effect ledger alongside the old logs and compare reconciliation in fixture mode. Keep one active execution owner; migrate old checkpoints with source-input/version provenance.

**Target design:** Recommendation: transactional SQLite checkpoint/receipt state for one host or an operated shared database for multiple workers. For exported files, validate temporary output then os.replace on the same filesystem; qualify sync/permissions separately.

**Rollback:** Recommendation: keep the ledger readable by the previous worker or convert it explicitly. Reconcile ambiguous remote outcomes before replay; reverting code cannot unsend a message or reverse a provider write.

**Benefits and prerequisites**

- Durable progress records allow targeted restart and investigation instead of blind replay. Requires: Stable item/effect IDs; checkpoint transactions; single writer or tested shared ownership; provider lookup/idempotency for uncertain effects. Tradeoffs: A file/database commit cannot atomically commit a remote side effect; os.replace atomicity does not establish power-loss durability or cross-filesystem replacement.

**Checks before transfer**

- Crash before effect, after remote success and after checkpoint; verify each resume decision.
- Resume the same input and prove acknowledged effects are skipped or reconciled.
- Interrupt export and verify a complete prior/new artifact; restore ledger from backup and compare cursor ownership.

- https://docs.python.org/3/library/sqlite3.html
- https://docs.python.org/3/library/os.html#os.replace

### Delivery and recovery

**Inspect the source:** Preserve provider rate limits, retry budgets, total run deadline and cleanup/cancellation behavior; SDK inactivity timeout is not a whole-run deadline.

**During coexistence:** Recommendation: retain sequential mode, add shared HTTPX clients and explicit capacity, and compare fixture results before enabling concurrency. Use a bounded queue for large inputs rather than creating one task for every item.

**Target design:** Recommendation: TaskGroup plus asyncio.timeout for operation lifetime, semaphore/worker limits for admission, HTTPX network timeouts and connection limits. Keep sync SDK work outside the event loop; cancellation of offloaded work needs a separate policy.

**Rollback:** Recommendation: return to sequential execution with the same receipt IDs and retry budget. Resolve uncertain effects from provider state before retrying; retain operation deadlines.

**Benefits and prerequisites**

- Bounded concurrency and total deadlines prevent unlimited waiting work and reduce abandoned I/O. Requires: Supported Python 3.11+; every provider adapter honors limits; aggregate retry budget and cancellation cleanup are configured. Tradeoffs: Read timeout measures inactivity between chunks; cancelling a coroutine does not prove a server write was cancelled; throughput gains are unmeasured.

**Checks before transfer**

- Slow streaming chunks beyond the total deadline while below read timeout; the whole operation still stops.
- Overload input and verify active plus queued work remain bounded.
- Cancel one task during provider I/O; TaskGroup cleanup closes clients and reports any ambiguous write.

- https://docs.python.org/3/library/asyncio-task.html
- https://docs.python.org/3/library/asyncio-sync.html
- https://www.python-httpx.org/advanced/timeouts/
- https://www.python-httpx.org/advanced/resource-limits/

### Jobs and schedules: Independent jobs with Celery

**Inspect the source:** Capture independent task payload versions, broker durability, acknowledgement timing, retries, dead-letter handling and scheduler overlap.

**During coexistence:** Recommendation: keep the old scheduler for unconverted tasks while routing selected task kinds into a qualified Celery queue. One scheduler/consumer owns each kind, and old backlog states remain accounted for.

**Target design:** Recommendation: Celery for independent jobs, with idempotent task bodies, bounded worker concurrency, explicit retry/backoff and intentionally selected acknowledgement/worker-loss settings. Keep existing brokers when their guarantees satisfy the contract.

**Rollback:** Recommendation: stop new producers, retain compatible workers for accepted tasks, and reroute only reconciled unstarted work. A scheduler rollback must not create a second schedule for the same task kind.

**Benefits and prerequisites**

- A qualified queue permits independent worker restart and retry for bounded jobs. Requires: Broker persistence/redelivery and payload mapping are tested; task effects are replay-safe; acknowledgement and worker-loss policy are deliberately configured. Tradeoffs: Late acknowledgement alone does not guarantee redelivery for every child-process termination; Celery worker settings and broker behavior matter; duplicate execution remains possible.

**Checks before transfer**

- Terminate the worker during a task and verify actual redelivery for the selected settings.
- Lose acknowledgement after an external effect; retries must not duplicate the logical effect.
- Drain or transform ready/delayed/retry/failed work before retiring the old scheduler/consumer.

- https://docs.celeryq.dev/en/stable/userguide/tasks.html

### Jobs and schedules: Recoverable multi-step workflows with Temporal

**Inspect the source:** Capture long-lived operation IDs, timer/human-wait behavior, provider effects and history/checkpoint schema before adopting durable orchestration.

**During coexistence:** Recommendation: keep old workflows running under their existing owner; start only newly routed operation IDs in Temporal. Keep provider calls in Activities and preserve effect IDs across retries. Do not duplicate a live run as a shadow test.

**Target design:** Recommendation: Temporal Python Workflows/Activities with specified timeouts, heartbeats, replay tests and compatible worker deployments. Temporal service/visibility/history retention and operational ownership are prerequisites, not Python package installation side effects.

**Rollback:** Recommendation: stop routing new IDs to the new workflow version and keep compatible workers servicing existing histories. Replay-test the rollback code; if incompatible, complete/version old executions rather than abandoning their state.

**Benefits and prerequisites**

- Persisted workflow history can resume orchestration across worker restarts and represent long waits. Requires: Temporal service and workers are operated; Workflow code is deterministic; Activity effects are idempotent/reconcilable; compatible histories pass replay. Tradeoffs: Adds a service and history/versioning obligations; Activity retries may repeat effects; orchestration recovery is not automatic compensation of external changes.

**Checks before transfer**

- Replay representative open and completed histories after code changes; fail promotion on nondeterminism.
- Restart workers during timers and Activities; verify orchestration resumes and heartbeat/checkpoint behavior.
- Crash after provider success before Activity completion; retry reconciles the stable effect ID.

- https://docs.temporal.io/develop/python/workflows/basics
- https://docs.temporal.io/develop/python/activities/basics
- https://docs.temporal.io/develop/python/activities/timeouts
- https://docs.temporal.io/develop/python/best-practices/testing-suite
- https://docs.temporal.io/activity-definition

Rewrite workflow: /rewrite/guide.md
Shared contracts and phases: /rewrite/contracts.json


## Setup
1. Complete the selected starting point and baseline checks in the Generators section first; then continue with the integration steps appropriate to the chosen component.
2. After completing the selected generated baseline, keep its package layout and console entry point for maintained workers. From that project root, run uv add httpx pydantic pydantic-settings only for required HTTP/validation/settings capabilities, and uv add --dev ruff mypy pytest for the configured checks.
3. For the standalone-file baseline, declare required dependencies with uv add --script task.py httpx pydantic rather than project uv add, then refresh task.py.lock using uv lock --script task.py. Skip unused dependencies and promote shared logic into a package when reuse warrants it.
4. Implement explicit inputs, a dry-run or fixture mode, bounded external calls, structured result/error output and credentials injected by the environment.
5. Only when shared persistent state is required, use the conditional SQLAlchemy/Alembic follow-up generators and reviewed migrations. For durable orchestration, add temporalio to the maintained project and implement workflows/activities plus a worker connected to a separately provisioned Temporal service.
6. Package the locked environment for the chosen scheduler or worker platform. Record startup, non-overlap, cancellation, retry, checkpoint and failure-resume behavior; verify fixture execution before live access.

## Verification
Commands below require the selected tools and project configuration. Replace example paths, schemes and IDs; distinguish tests from builds and interactive startup. These are instructions, not recorded passes.

```text
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
uv run python -m compileall -q src
```

## Open questions
- Which provider SDKs and minimum credential scopes are required?
- Are runs bounded, scheduled, queued or long-lived with human waits?
- Which effects are safe to retry, and what are run deadlines and cost budgets?
- Who owns execution history, alerts, secrets and recovery?

## Sources
- [uv projects](https://docs.astral.sh/uv/guides/projects/)
- [Ruff installation](https://docs.astral.sh/ruff/installation/)
- [mypy getting started](https://mypy.readthedocs.io/en/stable/getting_started.html)
- [ty type checking](https://docs.astral.sh/ty/type-checking/)
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)
- [Pydantic strict mode](https://pydantic.dev/docs/validation/latest/concepts/strict_mode/)
- [HTTPX timeouts](https://www.python-httpx.org/advanced/timeouts/)
- [SQLAlchemy session basics](https://docs.sqlalchemy.org/en/21/orm/session_basics.html)
- [Alembic autogeneration](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
- [uv Docker](https://docs.astral.sh/uv/guides/integration/docker/)
- [Temporal Python SDK](https://docs.temporal.io/develop/python)
- [Celery tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [uv scripts](https://docs.astral.sh/uv/guides/scripts/)
- [Python logging](https://docs.python.org/3/library/logging.html)
- [Tenacity documentation](https://tenacity.readthedocs.io/en/latest/)
- [Boto3 uploads](https://docs.aws.amazon.com/boto3/latest/guide/s3-uploading-files.html)

Keep the project README current and link the selected guidance; preserve existing project instructions.
