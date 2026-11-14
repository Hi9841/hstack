# FastAPI

Typed Python APIs alongside Python integrations, data or AI libraries.

Language: Python | Reviewed: 2026-10-10 | Evidence: documentation-reviewed research input

Source record: menu/inputs/research/python.json.

Core guidance checked: 2026-10-13. Review sources are listed below. /research-freshness.json describes the imported research packet; this record retains its own evidence scope. These recipes and selected dependency combinations need qualification in the actual project.

## Application role
Components: api
UI: none
Deployment: server

## Use cases
- Typed JSON APIs
- Integration services
- HTTP endpoints for model or worker products

## Fit
- API contracts and Python integrations matter more than built-in product/admin UI
- A separate frontend or service boundary already exists

## Choose something else when
- The team mostly needs accounts, admin, forms and CRUD that Django supplies
- Blocking or CPU-intensive jobs would be run inside request event loops

## Agent workflow
- Read README, dependency manifests, lockfiles, runtime pins and the maintained project workflow before changing anything. Preserve an existing stack unless reconsidering it is part of the request.
- For a new component, read the Generators section before writing application files. Use its appropriate official initializer and retain its generated baseline; follow-up generators are conditional on the selected feature.
- Use this guide to select tools by requirement. Resolve compatible versions from official and installed-version documentation; record the actual lockfile and runtime versions.
- Create a plan for schema changes, identity, authorization, external effects and deployment. A library choice does not complete its integration.
- Run relevant checks after configuration. Exercise the real interface, failure paths and packaged artifact on the intended target. Report commands, versions, results and untested behavior.
- On failure, retain the command and diagnostic, fix the failing prerequisite and resume there. Do not regenerate over existing work or suppress failures to make a check green.

## Best practices
- Validate tokens and permissions in dependencies; Pydantic validation does not establish authorization.
- Keep blocking calls out of async request handling and configure database connection lifetimes.
- Commit and rehearse Alembic migrations. Use isolated databases for integration tests.
- Move durable work to operated workers; an in-process background task cannot guarantee recovery.

## Generators: create the baseline first

Generator documentation reviewed: 2026-10-23. Evidence: documentation-reviewed; commands not executed.

### Required workflow

- Before writing a new project's application files, read its profile's starting points and use the official framework or language initializer appropriate to the component. Do not hand-recreate a generated skeleton. Where no full application generator exists, use the documented module/package initializer and assemble only the missing application pieces.
- Choose one starting point per component. Check the installed generator's version and help, prerequisites, template, database, UI, test and runtime options. Commands are examples: replace names and paths, resolve compatible versions, and record the exact invocation and selected options. Do not blindly run every listed generator.
- Generate in a new empty destination. For an existing repository, preserve its conventions and use relevant incremental generators. If a baseline comparison is needed, generate a separate disposable reference with matching versions/options and reconcile deliberately; never regenerate over existing work.
- Keep applicable generated configuration, hidden files, formatter/linter settings, ignore rules, manifests, lockfiles, tests, wrappers and entry points. Extend them for the project instead of replacing them with abbreviated handwritten copies. A generator may initialize version control or offer a commit; respect the user's Git instructions.
- Run the generated baseline's documented checks before feature changes, then relevant checks after configuration and implementation. Inspect what version control would include, including hidden files, build output, local secrets and operating-system metadata. Add needed ignore rules explicitly: no generator guarantees that .DS_Store or every local artifact is ignored.
- Use follow-up generators only when their feature or tool is selected. Review generated changes and dependencies, apply required migrations in the intended environment, and exercise the generated behavior. Scaffolding does not establish authorization, safe retries, production readiness or every best practice.
- If the required generator, template or IDE is unavailable, report the missing prerequisite and the documented route. Do not silently substitute a handwritten scaffold. Keep documentation review, generator execution, baseline checks and application qualification as separate evidence.

### Choose a starting point

#### Official fastapi-new project scaffold

Use when: A new FastAPI API where the official basic uv-configured scaffold is a suitable starting point; use the minimal assembly path below when you need a smaller/custom layout, or the full-stack template only when its additional choices fit.

1. Install uv using its official platform instructions, inspect uvx --help and the fastapi-new project README/release notes, and choose a new absent target directory. The package requires Python 3.10 or newer.
2. Run the official scaffold in the source parent, then inspect generated files, dependencies, README, ignore rules and lockfile before adapting it. Record the resolved fastapi-new, uv and Python versions.
3. Follow the generated README to start the app and check its initial endpoint; adapt the generated application deliberately to the requested API rather than assuming the scaffold covers production requirements.

Working directory: A local source-workspace parent; target must not already exist

Inspect the selected installed release's options before generating.

```sh
uvx fastapi-new --help
```

Working directory: A local source-workspace parent; api-service must not already exist

Generate the official basic FastAPI project configured with uv.

```sh
uvx fastapi-new api-service
```

Working directory: The generated api-service directory

Run the generated development application after reviewing its README and files.

```sh
uv run fastapi dev
```

- This is an official FastAPI organization project, but PyPI classifies it as Development Status 4 - Beta, has one maintainer, and its 0.0.7 release was uploaded 19 June 2026. Treat it as an optional scaffold and review the generated output; the documentation was reviewed but the command was not executed here.
- The official repository README documents `uvx fastapi-new <project-name>` and bare `uvx fastapi-new` for an existing directory. Do not use the latter on a populated project without first inspecting what it will add or change.
- This scaffold is distinct from FastAPI CLI's `fastapi dev`/`fastapi run` commands, which serve an existing application, and from the larger Full Stack FastAPI Template.

#### uv project initialization with explicit minimal FastAPI assembly

Use when: A new API/service requiring FastAPI without an entire full-stack template.

1. Install uv and inspect uv --version and uv init --help. Replace /path/to/local/source with an existing local source parent; use a new, absent target directory. Set PYTHON_VERSION to a supported Python minor compatible with the selected framework and dependencies. Record generator versions, selected flags and deliberate deviations.
2. Run uv initialization and dependency installation, then implement the minimal FastAPI application in app/main.py with app/__init__.py. This is deliberate assembly for the custom minimal uv path; use the official fastapi-new scaffold above when its generated baseline fits.
3. Use the official first-steps example as the initial app, add the required endpoint and test, then start the development server. Configure [tool.fastapi] entrypoint when the project uses a different import path.

Working directory: /path/to/local/source

Generate managed project metadata for the conventional flat app/ layout.

```sh
uv init --no-package --python "$PYTHON_VERSION" api-service
```

Working directory: /path/to/local/source/api-service

Resolve FastAPI and its CLI/server dependencies.

```sh
uv add "fastapi[standard]"
```

Working directory: /path/to/local/source/api-service

After the app file exists, run the development server; this command does not scaffold an application.

```sh
uv run fastapi dev app/main.py
```

- FastAPI documents a small application assembled from Python modules. The official fastapi dev and fastapi run commands serve existing apps; `fastapi-new` is the separate optional official project scaffold documented above.
- Inspect the generated uv sample main.py; adapt/remove it explicitly if app/main.py replaces it. Document any chosen package layout instead of letting two entry points drift.
- Choose a source parent outside another uv workspace, or intentionally use --no-workspace when creating an independent project under a directory with parent pyproject.toml metadata.

#### Official Full Stack FastAPI Template

Use when: The requested product explicitly needs the template’s React frontend, SQLModel/PostgreSQL, accounts and deployment structure.

1. Review the official repository README and its current development documentation. Record the selected revision and verify its actual dependency/layout choices.
2. Use GitHub Use this template to create the requested repository, then clone it into a local source workspace and follow its own initialization instructions.
3. Configure project identity and environment-owned secrets; replace example credentials and inspect generated workflows before enabling external effects.

- This is an official optional template, not the default for every API. Its extra frontend, ORM and infrastructure choices must match the application.
- The reviewed official README uses GitHub template creation; no unsupported Copier command is prescribed. Do not run another uv init over the template or replace its maintained lock/environment workflow.

### Conditional follow-up generators

#### Conditional Alembic migration environment and revisions

Use when: SQLAlchemy-backed persistent state is required; skip for stateless APIs/workers and preserve an existing migration owner.


Working directory: /path/to/local/source/api-service

Install the selected PostgreSQL data dependencies; use a compatible driver for another chosen database.

```sh
uv add sqlalchemy alembic "psycopg[binary]"
```

Working directory: /path/to/local/source/api-service

Generate the standard migration environment and config.

```sh
uv run alembic init migrations
```

Working directory: /path/to/local/source/api-service

After configuring env.py metadata and database access, generate a candidate schema revision.

```sh
uv run alembic revision --autogenerate -m "initial schema"
```

Working directory: /path/to/local/source/api-service

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
- Preserve the selected application layout, explicit FastAPI entrypoint and any chosen template tests/configuration; record template revision and changes.
- Do not add an ORM, database, frontend or queue solely to imitate a full-stack template.

### Baseline and generation checks

- From /path/to/local/source/api-service: uv sync --locked. Import the implemented app and exercise its API tests after installing/configuring the selected test tooling.
- With uv run fastapi dev app/main.py running locally, verify a real endpoint and /openapi.json. Choose and document production startup separately; development reload is not a deployment check.
- When Alembic is configured, run uv run alembic check and uv run alembic current against the disposable development database; verify migration behavior.
- Compare project metadata with a disposable scaffold from the same uv version and flags, or the selected official template revision. Review tracked/staged files and ensure local environments, secrets and .DS_Store are excluded.

### Generation receipt

- Component and selected starting point, or the documented absence of a full application generator
- Generator/toolchain versions, exact commands or IDE template/settings, working directory and generated destination
- Generated files retained, deliberate deviations with reasons, and required supplemental ignore rules
- Baseline checks and later checks actually run, results and remaining prerequisites or untested behavior

### Generator sources

- [Official fastapi-new project scaffold and command](https://github.com/fastapi/fastapi-new)
- [fastapi-new package metadata, release and maturity classification](https://pypi.org/project/fastapi-new/)
- [uv project creation and layout choices](https://docs.astral.sh/uv/concepts/projects/init/)
- [uv project dependency and environment workflow](https://docs.astral.sh/uv/guides/projects/)
- [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
- [uv FastAPI integration with explicit unpackaged layout](https://docs.astral.sh/uv/guides/integration/fastapi/)
- [FastAPI first application](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [FastAPI CLI: development and production serving](https://fastapi.tiangolo.com/fastapi-cli/)
- [Official Full Stack FastAPI Template overview](https://fastapi.tiangolo.com/project-generation/)
- [Official Full Stack FastAPI Template repository and creation instructions](https://github.com/fastapi/full-stack-fastapi-template)
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

### Testing: pytest + HTTPX / FastAPI TestClient

Test contract failures, auth and integration boundaries.

Limits and integration: Run startup/shutdown lifespan when relevant; include PostgreSQL and external-service fault tests.


- https://docs.pytest.org/en/stable/getting-started.html
- https://fastapi.tiangolo.com/deployment/docker/

Alternatives: Async client tests for async application lifecycles

### Database and migrations: PostgreSQL + SQLAlchemy + Psycopg + Alembic

Explicit transactions and versioned relational changes.

Limits and integration: Session per thread / AsyncSession per task. Review generated migrations, especially renames and data changes; a passing migration check does not prove production lock safety.


- https://docs.sqlalchemy.org/en/21/orm/session_basics.html
- https://alembic.sqlalchemy.org/en/latest/autogenerate.html

Alternatives: SQLite for local single-user work; no DB for stateless services

### Validation: Pydantic request/response models; strict validation where coercion is unsafe

Typed schemas clarify external contracts and generated documentation.

Limits and integration: Coercion is configurable; schema validity is not authorization or business correctness. Avoid returning unrestricted ORM objects.


- https://pydantic.dev/docs/validation/latest/concepts/strict_mode/

Alternatives: Explicit domain validation functions

### Authentication: Existing OIDC provider; validate access tokens and authorization in dependencies

Keep identity lifecycle with its owner while enforcing permissions at the API.

Limits and integration: Choose and verify token-validation integration at implementation. FastAPI's JWT tutorial is not a complete identity system; issuer, audience, expiry and permissions need tests.


- https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- https://docs.authlib.org/en/v1.7.0/oauth2/client/web/index.html

Alternatives: Authlib for browser OIDC client flow; First-party session authentication if architecture requires it

### Jobs: Separate Celery workers for queued jobs

Separate request latency from heavy or retried work.

Limits and integration: BackgroundTasks does not establish durable execution. Make job effects idempotent and set retry/deadline limits.


- https://fastapi.tiangolo.com/tutorial/background-tasks/
- https://docs.celeryq.dev/en/stable/userguide/tasks.html
- https://docs.temporal.io/develop/python

Alternatives: Temporal for restart-safe multi-step workflows; BackgroundTasks for small best-effort post-response work

### Long-running durable agents: Temporal Python SDK when recovery across restarts is required

Persisted workflow orchestration and separate worker processes suit retries, pauses and human waits.

Limits and integration: Adds a service and operational cost. Keep external I/O in activities, make side effects idempotent, test replay and cancellation; no end-to-end integration was run.


- https://docs.temporal.io/develop/python
- https://docs.celeryq.dev/en/stable/userguide/tasks.html

Alternatives: Celery for independent queued jobs; direct function for bounded work

### Serving and deployment: FastAPI standard CLI / Uvicorn in a container

Official deployment path with explicit process and container choices.

Limits and integration: Build from a supported base rather than deprecated framework images; choose process count to match deployment/memory, and run schema migration once per release.


- https://fastapi.tiangolo.com/deployment/docker/
- https://docs.astral.sh/uv/guides/integration/docker/
- https://fastapi.tiangolo.com/async/

Alternatives: Managed ASGI platform

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

### Uploads: FastAPI UploadFile

Spooling file interface avoids eagerly materializing all content in application memory

Limits and integration: Install python-multipart; enforce request/file limits and authorization, stream to durable storage and clean partial writes. Multipart parsing does not establish file safety.


- https://fastapi.tiangolo.com/tutorial/request-files/

Alternatives: Preserve an existing compatible project choice

### Realtime transport: FastAPI WebSocket endpoints

Native ASGI endpoint support fits connected API clients

Limits and integration: Authorize handshake/messages; bound per-client queues, handle disconnect and share state through an external service for replicas. In-memory tutorial connection lists are not multi-process state.


- https://fastapi.tiangolo.com/advanced/websockets/

Alternatives: Preserve an existing compatible project choice

### Object storage: Boto3 S3 client when durable objects are required

Official SDK supports file transfer to S3

Limits and integration: Install boto3 only for S3-backed work; use platform credentials, private keys and bounded transfers. Boto3 is synchronous: keep blocking transfers out of an async event loop; verify alternative provider compatibility.


- https://docs.aws.amazon.com/boto3/latest/guide/s3-uploading-files.html

Alternatives: Preserve an existing compatible project choice

## Architecture and developer workflow

FastAPI exposes Python type-annotated HTTP operations and dependency boundaries. It supports synchronous and async handlers; the choice depends on whether called libraries support await. Recommendation: keep request models distinct from persistence operations and explicitly select identity, durable jobs, database migrations and distributed messaging instead of assuming the API framework provides an integrated monolith.

Version scope: Current FastAPI online guides fetched 11 October 2026; these pages do not pin an application package release. SQLAlchemy 2.0 documentation, Alembic 1.20.0 documentation and Celery 5.6.3 reviewed. Pin actual Python/FastAPI/Pydantic/Starlette/database-driver versions before implementation.
Reviewed: 2026-10-11 | Evidence: documentation-reviewed | Source record: inputs/research/migrations-server.json

### Architecture boundaries

- Use async handlers with awaitable I/O, or normal def handlers for blocking libraries as the guide explains. Recommendation: keep CPU-heavy or durable work behind a deliberate worker boundary; adding async syntax does not change its durability or CPU execution model.
- SQLAlchemy Sessions are mutable transaction state and cannot be shared across concurrent tasks/threads. Recommendation: scope a Session to its operation, keep the engine/pool separate and use reviewed Alembic revisions for schema evolution.
- FastAPI lifespan manages startup/shutdown resources. Multiple worker processes are a deployment choice; recommendation: treat in-memory connections/caches as worker-local and keep one external scheduler and migration owner.

### Tools and feedback

- For a configured application, adapt fastapi run --workers 4 main.py or uvicorn main:app --workers 4 from the deployment guide; replace module and worker count for the actual host/container topology. The example is a recipe, not a capacity recommendation.
- For a configured SQLAlchemy/Alembic application, use alembic revision -m "Add a column", review upgrade/downgrade operations, then alembic upgrade head in a disposable database; alembic current and alembic history show recorded state.
- Use FastAPI TestClient and pytest for HTTP contract tests. Recommendation: add real database/worker tests for transaction and retry boundaries, plus WebSocket tests across the intended multi-process topology.
- Recommendation: initialize shared process resources through the lifespan context and create independent database sessions for concurrent operations. Validate selected sync/async client usage and cleanup on shutdown before rollout.

### Translations to avoid

- Avoid using BackgroundTasks as a durable queue replacement: it executes work associated with the application process, while the guide recommends larger worker tools such as Celery for work that belongs in multiple processes/servers. Recommendation: qualify crash/retry behavior explicitly.
- Avoid copying the tutorial’s in-memory WebSocket connection list into a multi-worker product; the docs explicitly say it works only in one running process.
- Avoid sharing one SQLAlchemy Session among requests/tasks or moving blocking library calls unchanged inside async handlers; the documented concurrency boundaries differ.
- Avoid treating a JWT tutorial as a complete identity migration. Recommendation: retain existing identity authority until issuer, account mapping, validation, expiry and revocation are designed. Starlette SessionMiddleware signs readable cookie contents; signing is not confidentiality.

### Architecture sources

- [FastAPI Concurrency](https://fastapi.tiangolo.com/async/): Choice of async handlers versus normal def for awaitable/blocking libraries.
- [FastAPI SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/): Request-scoped database dependency examples and external SQL library choice.
- [SQLAlchemy Session Basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html): Mutable transaction/session lifecycle and prohibition on sharing across concurrent threads/tasks.
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html): Revision, upgrade/downgrade, current/history commands and schema revision ownership.
- [FastAPI Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/): Same-process task examples and separate Celery/queue recommendation for larger execution boundaries.
- [Celery Tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html): Task serialization, retry/acknowledgement and idempotency concerns.
- [Celery Periodic Tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html): Only one scheduler per schedule to prevent duplicate production.
- [Celery First Steps](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html): Broker, worker and optional result backend are separate roles.
- [FastAPI OAuth2/JWT example](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/): Token/password validation and expiry example, not cross-framework session interoperability.
- [Starlette Middleware](https://starlette.dev/middleware/): Signed readable sessions, session cookie configuration and secure transport option.
- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/): Handler authentication/dependencies and explicit single-process limitation of in-memory connection list.
- [FastAPI Lifespan](https://fastapi.tiangolo.com/advanced/events/): Startup/shutdown resource ownership through lifespan.
- [FastAPI Server Workers](https://fastapi.tiangolo.com/deployment/server-workers/): FastAPI/Uvicorn worker commands and deployment process topology choices.
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/): TestClient and pytest request checks.
- [Redis redis-py guide](https://redis.io/docs/latest/develop/clients/redis-py/): Maintained Python client for Redis with sync/async documentation links.

## Transition options

Proposed designs and checks; these are not executed compatibility results.

### Data and schema

**Inspect the source:** Inventory schema, primary IDs, SQL value/constraint semantics and existing transaction ownership. The old application may use an ORM with callbacks absent from the target service.

**During coexistence:** Recommendation: keep one writer and migration runner; start with read-only target endpoints or a bounded domain operation. Preserve additive schema and qualify ORM/session behavior before transferring writes.

**Target design:** SQLAlchemy 2.0 Sessions scoped to operations, with reviewed Alembic upgrade/downgrade revisions and the selected PostgreSQL driver. Recommendation: keep transaction and external delivery boundaries explicit.

**Rollback:** Recommendation: restore the old writer while preserving backward-readable schema; use downgrade only for a rehearsed reversible change and reconcile accepted new data.

**Benefits and prerequisites**

- Recommendation: explicit sessions and migrations expose the persistence boundary to review. Requires: Qualified schema mapping, operation-scoped sessions and one writer owner. Tradeoffs: FastAPI does not remove ORM/migration choices; deleting data cannot be undone by traffic rollback.

**Checks before transfer**

- Create through each allowed writer and read through both runtimes; compare IDs, timestamps/null values and constraint failures.
- Run concurrent requests with separate sessions and fail one transaction; no other request’s changes or Session state may leak.
- Apply a reviewed revision to a disposable restored database and verify both deployed versions still read new writes.

- https://fastapi.tiangolo.com/tutorial/sql-databases/
- https://docs.sqlalchemy.org/en/20/orm/session_basics.html
- https://alembic.sqlalchemy.org/en/latest/tutorial.html

### Jobs and schedules

**Inspect the source:** Record old task name/class, serialized arguments, broker, retries/acknowledgements, schedule ownership and every backlog state. BackgroundTasks and a broker-backed worker are different execution contracts.

**During coexistence:** Recommendation: retain old consumers and isolate new categories behind a versioned task interface. Use configured Celery or another separately qualified persistent system when restart recovery matters; keep one schedule owner and a recoverable domain-to-broker handoff.

**Target design:** An explicitly selected durable worker/broker composition with business idempotency. Small best-effort same-process tasks may use BackgroundTasks only when their documented process boundary fits the requirement.

**Rollback:** Recommendation: stop new task production, retain consumers for accepted payload versions and reconcile external effects before restoring old routing.

**Benefits and prerequisites**

- Recommendation: durable work can move independently of the HTTP service. Requires: Selected broker/worker configuration, tested payloads and explicit idempotency/recovery policy. Tradeoffs: The broker and worker add operated components; returning HTTP success before enqueue acceptance must have a deliberate contract.

**Checks before transfer**

- Enqueue while the worker is stopped, restart it and verify the intended completion/failure result.
- Crash after an external effect before acknowledgement and verify retry is safe; test broker outage during a domain write.
- Reconcile delayed/retry/failed/running tasks and verify the old and new schedulers never both produce the category.

- https://fastapi.tiangolo.com/tutorial/background-tasks/
- https://docs.celeryq.dev/en/stable/userguide/tasks.html
- https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
- https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html

### Identity and authorization

**Inspect the source:** Capture the source identity authority, token/cookie format, issuer/audience rules, account IDs, expiration and revocation. The FastAPI OAuth2/JWT guide is a concrete example, not proof of compatibility with existing sessions.

**During coexistence:** Recommendation: retain the existing identity authority through qualified token verification or session exchange. Move resource authorization with the domain operation, and keep cookie scope/CSRF behavior explicit when using browser cookies.

**Target design:** Selected OAuth2/token or browser-session implementation with deliberate account mapping and authorization. If using Starlette SessionMiddleware, cookie data is signed and readable; use https_only and appropriate scope settings for the selected deployment.

**Rollback:** Recommendation: preserve account mapping and old credential/exchange support without reversing revocations; return routing only when validation remains compatible.

**Benefits and prerequisites**

- Recommendation: a shared identity authority can preserve access across service boundaries. Requires: Qualified token/session validation and common revocation policy. Tradeoffs: Bearer expiry and server-side revocation are distinct design choices; readable signed cookies must not contain secrets.

**Checks before transfer**

- Accept a valid source credential and reject modified/expired credentials and a valid credential for another tenant’s protected record.
- Logout/revoke and confirm both old/new paths follow the agreed policy, including an existing WebSocket connection.
- Inspect the selected cookie contents and transport flags; no secret should be exposed by a signed-but-readable session.

- https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- https://starlette.dev/middleware/
- https://fastapi.tiangolo.com/advanced/websockets/

### Realtime transport

**Inspect the source:** Capture the old client protocol, message envelope, connection authentication, subscription scopes and recovery requirements. FastAPI provides WebSocket handlers; its in-memory chat example is explicitly single-process.

**During coexistence:** Recommendation: retain the old endpoint for old clients, bridge versioned domain events and route a stable user/room cohort including reconnects. Keep fanout in a separately qualified shared system when multiple worker processes must reach the same recipients.

**Target design:** FastAPI WebSocket handlers with explicit shared fanout and persisted domain-state/cursor recovery when required. No specific broker/client combination is integration-qualified by this research.

**Rollback:** Recommendation: preserve old endpoint/message compatibility through reconnects; return the cohort and reconcile current domain state instead of reissuing effects.

**Benefits and prerequisites**

- Recommendation: an API service can take ownership of a realtime boundary incrementally. Requires: Matching message/client protocol, subscription authorization and a tested multi-worker fanout implementation. Tradeoffs: Connection lists remain worker-local; selecting a shared broker does not itself provide catch-up or protocol compatibility.

**Checks before transfer**

- Connect clients to different workers, commit one domain event and verify all authorized recipients converge.
- Restart the worker containing a connection, reconnect and recover missed state; test a revoked identity attempting to rejoin.

- https://fastapi.tiangolo.com/advanced/websockets/
- https://fastapi.tiangolo.com/deployment/server-workers/

### Caching and shared state

**Inspect the source:** List reconstructible values and representation/TTL/invalidation separately from identities, jobs, counters and locks. Multiple application workers have distinct in-memory resource ownership.

**During coexistence:** Recommendation: keep the existing shared store for coordination; use versioned keys for new representations. Move only disposable values to local caching when per-worker staleness and rebuilding are explicitly accepted.

**Target design:** A selected shared cache accessed with a qualified client such as redis-py, or an explicitly bounded local cache. Recommendation: match sync/async client usage to the handler and manage process resource lifetime deliberately.

**Rollback:** Recommendation: restore old key/backend routing and repopulate from domain data; preserve shared coordination ownership throughout.

**Benefits and prerequisites**

- Recommendation: cache choices can evolve without transferring domain ownership. Requires: Reconstructible values, explicit invalidation and a complete list of shared-store uses. Tradeoffs: Local values diverge across workers; removing Redis requires separately retiring sessions/queues/coordination, not merely replacing cached reads.

**Checks before transfer**

- Warm two workers, update the source and verify required invalidation/staleness across both.
- Restart one worker or evict its dedicated cache and verify reconstruction without losing identity or queued work.
- Make the shared cache unavailable and verify the agreed failure/fallback behavior rather than silently accepting stale authorization.

- https://redis.io/docs/latest/develop/clients/redis-py/
- https://fastapi.tiangolo.com/deployment/server-workers/
- https://fastapi.tiangolo.com/advanced/events/

### Delivery and recovery

**Inspect the source:** Inventory API workers, startup resources, database migration runner, durable workers, external scheduler and shared fanout/cache. Worker replication and lifespan resources are not a singleton schedule mechanism.

**During coexistence:** Recommendation: keep one schema runner and logical schedule owner while both services operate. Initialize per-process resources deliberately and transfer traffic by a stable domain/user cohort.

**Target design:** An explicit FastAPI/Uvicorn process/container deployment, lifespan cleanup, separate durable workers and monitored dependency boundaries. Recommendation: record actual worker count and deployment settings instead of inheriting tutorial values.

**Rollback:** Recommendation: preserve the old release and compatible schema, transfer role ownership before restoring traffic, and reconcile work accepted by the new service.

**Benefits and prerequisites**

- Recommendation: process/resource ownership makes multi-worker behavior reviewable. Requires: Named migration/schedule owners, configured shutdown and tested dependency failure behavior. Tradeoffs: More workers multiply process-local resources; successful HTTP startup cannot qualify broker, identity or restore behavior.

**Checks before transfer**

- Start the intended multi-worker deployment against disposable restored data; exercise authenticated HTTP, one task and cross-worker realtime delivery.
- Terminate a worker during active work, verify shutdown/restart behavior and confirm no extra scheduler or migration runner starts.

- https://fastapi.tiangolo.com/advanced/events/
- https://fastapi.tiangolo.com/deployment/server-workers/
- https://alembic.sqlalchemy.org/en/latest/tutorial.html
- https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html

Rewrite workflow: /rewrite/guide.md
Shared contracts and phases: /rewrite/contracts.json


## Setup
1. Complete the selected starting point and baseline checks in the Generators section first; then continue with the integration steps appropriate to the chosen component.
2. After completing the selected generated baseline, use uv add pydantic-settings when environment-backed typed settings are required, and uv add --dev ruff mypy pytest httpx for the configured checks/tests. Resolve compatible versions and commit uv.lock; for the optional full-stack template preserve its own declared dependency workflow.
3. Extend the generated or explicitly assembled FastAPI entry point with request/response models, one authorized API slice and a health endpoint. Use the actual application path chosen by the baseline.
4. Only when persistent SQL state is required, use the follow-up Alembic environment and revision generators. Configure an environment-owned connection URL and target_metadata, then implement per-request/task sessions and domain transaction boundaries; manually review migrations before applying to a disposable development database.
5. Configure the selected identity provider and token verification; implement tenant/object authorization before exposing protected endpoints.
6. Use uv run fastapi dev app/main.py only for the minimal baseline development server, adapting the path for another layout. Prepare the release with uv sync --locked --no-dev and an explicit production start command for the chosen host; add workers separately when needed.

## Verification
Commands below require the selected tools and project configuration. Replace example paths, schemes and IDs; distinguish tests from builds and interactive startup. These are instructions, not recorded passes.

```text
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest
uv run alembic check
uv run alembic current
```

## Open questions
- Which identity provider, token validation and tenant authorization model apply?
- Does workload justify async database access, or is synchronous I/O simpler?
- Which host/replica model, upload storage, realtime and worker guarantees apply?

## Sources
- [uv projects](https://docs.astral.sh/uv/guides/projects/)
- [Ruff installation](https://docs.astral.sh/ruff/installation/)
- [mypy getting started](https://mypy.readthedocs.io/en/stable/getting_started.html)
- [ty type checking](https://docs.astral.sh/ty/type-checking/)
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)
- [FastAPI containers](https://fastapi.tiangolo.com/deployment/docker/)
- [SQLAlchemy session basics](https://docs.sqlalchemy.org/en/21/orm/session_basics.html)
- [Alembic autogeneration](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
- [Pydantic strict mode](https://pydantic.dev/docs/validation/latest/concepts/strict_mode/)
- [FastAPI JWT tutorial](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [Authlib OAuth web clients](https://docs.authlib.org/en/v1.7.0/oauth2/client/web/index.html)
- [FastAPI background tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- [Celery tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [Temporal Python SDK](https://docs.temporal.io/develop/python)
- [uv Docker](https://docs.astral.sh/uv/guides/integration/docker/)
- [FastAPI concurrency](https://fastapi.tiangolo.com/async/)
- [Python logging](https://docs.python.org/3/library/logging.html)
- [Tenacity documentation](https://tenacity.readthedocs.io/en/latest/)
- [FastAPI request files](https://fastapi.tiangolo.com/tutorial/request-files/)
- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)
- [Boto3 uploads](https://docs.aws.amazon.com/boto3/latest/guide/s3-uploading-files.html)

Keep the project README current and link the selected guidance; preserve existing project instructions.
