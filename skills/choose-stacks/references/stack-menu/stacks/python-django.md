# Django

Data-heavy products with an ORM, forms, accounts and admin.

Language: Python | Reviewed: 2026-10-10 | Evidence: documentation-reviewed research input

Source record: menu/inputs/research/python.json.

Core guidance checked: 2026-10-13. Review sources are listed below. /research-freshness.json describes the imported research packet; this record retains its own evidence scope. These recipes and selected dependency combinations need qualification in the actual project.

## Application role
Components: web, api
UI: server
Deployment: server

## Use cases
- CRUD-heavy SaaS
- Internal products and admin tools
- Server-rendered business applications

## Fit
- Accounts, forms, admin and database workflows are central
- A cohesive conventional monolith reduces integration decisions

## Choose something else when
- Only a small stateless endpoint is needed
- The core workload needs a different runtime or hard real-time guarantees

## Agent workflow
- Read README, dependency manifests, lockfiles, runtime pins and the maintained project workflow before changing anything. Preserve an existing stack unless reconsidering it is part of the request.
- For a new component, read the Generators section before writing application files. Use its appropriate official initializer and retain its generated baseline; follow-up generators are conditional on the selected feature.
- Use this guide to select tools by requirement. Resolve compatible versions from official and installed-version documentation; record the actual lockfile and runtime versions.
- Create a plan for schema changes, identity, authorization, external effects and deployment. A library choice does not complete its integration.
- Run relevant checks after configuration. Exercise the real interface, failure paths and packaged artifact on the intended target. Report commands, versions, results and untested behavior.
- On failure, retain the command and diagnostic, fix the failing prerequisite and resume there. Do not regenerate over existing work or suppress failures to make a check green.

## Best practices
- Keep Django's auth, session and CSRF protections. Enforce tenant and object permissions in application operations.
- Use forms, domain validation and database constraints together; do not rely on one validation layer.
- Commit and rehearse migrations against an isolated database; check deployment settings separately from unit tests.
- Choose WSGI or ASGI for the actual workload and operate background workers independently.

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

#### uv environment plus native Django project generator

Use when: A new Django product application; preserve the established layout and packaging workflow when extending an existing app.

1. Install uv and inspect uv --version and uv init --help. Replace /path/to/local/source with an existing local source parent; use a new, absent target directory. Set PYTHON_VERSION to a supported Python minor compatible with the selected framework and dependencies. Record generator versions, selected flags and deliberate deviations.
2. Run commands in the stated directories in order. Use explicit --no-package for the conventional root manage.py layout; uv default application layouts vary by version.
3. After scaffolding, inspect the uv sample main.py and deliberately remove or repurpose that sample if Django manage.py is the only entry point. Configure secrets, database and installed apps before feature work.

Working directory: /path/to/local/source

Create the managed project metadata and selected Python environment.

```sh
uv init --no-package --python "$PYTHON_VERSION" django-app
```

Working directory: /path/to/local/source/django-app

Resolve Django into the project environment and lock.

```sh
uv add django
```

Working directory: /path/to/local/source/django-app

Generate manage.py and the Django settings, URLs, WSGI and ASGI package.

```sh
uv run django-admin startproject config .
```

- This is a composed bootstrap: uv owns Python packaging; django-admin owns framework scaffolding. Do not hand-create a substitute Django skeleton.
- Django scaffolding does not make production settings safe. Configure environment-owned secrets, DEBUG, ALLOWED_HOSTS and the selected production database/server.
- Choose a source parent outside another uv workspace, or intentionally use --no-workspace when creating an independent project under a directory with parent pyproject.toml metadata.

### Conditional follow-up generators

#### Conditional Django REST Framework API layer

Use when: Only after completing the Django project bootstrap above, and only when the application needs JSON API endpoints. Django has no built-in API-only project mode.


Working directory: /path/to/local/source/django-app

Install and lock the optional REST API framework in this project.

```sh
uv add djangorestframework
```

Working directory: /path/to/local/source/django-app

Generate the app that will own API serializers, views and routes.

```sh
uv run python manage.py startapp api
```

- Django's own `startproject` remains the general project bootstrap; DRF is a separately installed library and API layer, not a native Django API-only generator. Add both `rest_framework` and `api.apps.ApiConfig` (or the chosen generated API AppConfig) to INSTALLED_APPS, then follow the upstream quickstart for serializers, views, routers and API tests.
- DRF's default permission policy is AllowAny. Set an intentional global or per-view permission policy and add object/tenant checks where needed; authentication alone does not authorize access. Select authentication based on client type, and treat session-authenticated browser requests' CSRF requirements deliberately.
- Add CORS middleware/package and narrowly allow required origins only if a browser client actually calls the API cross-origin. Same-origin, server-to-server and native clients need different handling; do not install CORS or token-auth packages by default.

#### Django application module

Use when: A new domain app is needed inside the existing project; substitute a domain name for core.


Working directory: /path/to/local/source/django-app

Generate the app configuration, models, admin, tests and migrations package.

```sh
uv run python manage.py startapp core
```

- Register core.apps.CoreConfig in INSTALLED_APPS and implement the domain. The generator does not wire URLs, permissions or product behavior.

#### Django schema and data migrations

Use when: Registered application models change; use the configured disposable development database first.


Working directory: /path/to/local/source/django-app

Generate a migration from implemented model changes.

```sh
uv run python manage.py makemigrations core
```

Working directory: /path/to/local/source/django-app

Alternative for an intentional data migration: generate its empty revision.

```sh
uv run python manage.py makemigrations --empty core --name populate_reference_data
```

Working directory: /path/to/local/source/django-app

Inspect the configured database migration plan.

```sh
uv run python manage.py migrate --plan
```

Working directory: /path/to/local/source/django-app

Apply reviewed migrations to the development database.

```sh
uv run python manage.py migrate
```

- The empty data migration is conditional, not a mandatory extra step. Implement it using historical models and review reversibility. Review generated operations before applying; commit migration sources with model changes.
- Use Django ORM/migrations for this profile; do not add a second default migration system. PostgreSQL requires its driver and settings before database commands.

### Preserve the generated foundation

- Keep generator-created project metadata, Python requirements, version selection and ignore rules; extend them rather than replacing them with a handwritten approximation.
- Commit the resolved uv.lock for projects; exclude .venv, caches, secrets and platform debris such as .DS_Store. Do not hand-edit lockfiles.
- Keep source repositories, virtual environments and caches in a local development workspace outside cloud-synced document folders.
- Retain the generated manage.py, app configuration, middleware/security defaults, URL setup and WSGI/ASGI interfaces unless a documented application need changes them.
- Retain and review migration history; never regenerate an existing project over maintained code.

### Baseline and generation checks

- From /path/to/local/source/django-app: uv sync --locked; uv run python manage.py check; uv run python manage.py makemigrations --check --dry-run.
- For a DRF API, test explicit public/protected permissions, object/tenant denials, input validation and response contracts with DRF APIClient/APIRequestFactory; test session CSRF and narrowly allowed/rejected CORS origins when browser clients require them.
- After reviewed migrations on the configured development database: uv run python manage.py migrate --check. Run application tests using its configured runner and a production-relevant isolated database.
- Run uv run python manage.py check --deploy against the actual production settings module once it exists; runserver is a development server.
- Compare a disposable scaffold made with the same uv/Django versions and flags; review the generated baseline and document deviations. Inspect tracked/staged files and verify ignore rules against local debris, caches and secrets.

### Generation receipt

- Component and selected starting point, or the documented absence of a full application generator
- Generator/toolchain versions, exact commands or IDE template/settings, working directory and generated destination
- Generated files retained, deliberate deviations with reasons, and required supplemental ignore rules
- Baseline checks and later checks actually run, results and remaining prerequisites or untested behavior

### Generator sources

- [Django 6.0 project bootstrap and supported Python version](https://docs.djangoproject.com/en/6.0/intro/tutorial01/)
- [Django REST framework quickstart and project setup](https://www.django-rest-framework.org/tutorial/quickstart/)
- [Django REST framework authentication schemes](https://www.django-rest-framework.org/api-guide/authentication/)
- [Django REST framework permissions and AllowAny default](https://www.django-rest-framework.org/api-guide/permissions/)
- [Django REST framework API request testing](https://www.django-rest-framework.org/api-guide/testing/)
- [uv project creation and layout choices](https://docs.astral.sh/uv/concepts/projects/init/)
- [uv project dependency and environment workflow](https://docs.astral.sh/uv/guides/projects/)
- [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
- [Django tutorial: startproject and startapp](https://docs.djangoproject.com/en/6.0/intro/tutorial01/)
- [Django tutorial: app registration and migrations](https://docs.djangoproject.com/en/6.0/intro/tutorial02/)
- [Django management command reference](https://docs.djangoproject.com/en/6.0/ref/django-admin/)
- [Django production deployment checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
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

### Static typing: mypy + django-stubs plugin

Django-aware stubs and plugin improve checks around ORM and settings.

Limits and integration: Check the django-stubs compatibility table for the selected Django/Python/mypy combination; plugin imports application settings.


- https://github.com/typeddjango/django-stubs
- https://mypy.readthedocs.io/en/stable/getting_started.html

Alternatives: ty for isolated plain-Python modules after validation

### Testing: pytest + pytest-django

Database fixtures and Django integration while retaining pytest conventions.

Limits and integration: Set DJANGO_SETTINGS_MODULE; use isolated PostgreSQL tests for constraints and transactions. Unit tests alone miss request and migration behavior.


- https://docs.pytest.org/en/stable/getting-started.html
- https://pytest-django.readthedocs.io/en/latest/

Alternatives: Django built-in test runner

### Database and migrations: PostgreSQL + Django ORM/migrations + Psycopg

Use the framework's existing data layer and schema history.

Limits and integration: Review schema/data migrations and query counts; run production-relevant DB tests. Do not introduce SQLAlchemy as a second default ORM.


- https://docs.djangoproject.com/en/6.0/topics/migrations/

Alternatives: SQLite for low-concurrency local products

### Validation: Django Forms/ModelForms plus domain checks and DB constraints

Form lifecycle handles submitted values and field errors.

Limits and integration: Model saving is not a substitute for form/domain validation; enforce invariants at the appropriate transaction boundary.


- https://docs.djangoproject.com/en/6.0/ref/forms/validation/
- https://pydantic.dev/docs/validation/latest/concepts/strict_mode/

Alternatives: Pydantic at external JSON/tool boundaries

### Authentication: Django auth, sessions, permissions and CSRF protection

Built-in accounts and session conventions fit browser products.

Limits and integration: Object/tenant permissions still need explicit implementation and tests; do not expose the admin as the product UI by default.


- https://docs.djangoproject.com/en/6.0/topics/auth/
- https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

Alternatives: OIDC integration when an existing identity provider owns login

### Background jobs: Celery + a configured durable broker

Documented Django integration for off-request work.

Limits and integration: Broker required; enqueue after commit, retry only safe effects. Django Tasks built-in backends do not supply production workers or durable queues. Celery is a separate integration, not automatically a django.tasks backend.


- https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
- https://docs.celeryq.dev/en/stable/userguide/tasks.html
- https://docs.djangoproject.com/en/6.0/topics/tasks/

Alternatives: Django Tasks plus a reviewed production backend; Temporal for durable orchestration

### Long-running durable agents: Temporal Python SDK when recovery across restarts is required

Persisted workflow orchestration and separate worker processes suit retries, pauses and human waits.

Limits and integration: Adds a service and operational cost. Keep external I/O in activities, make side effects idempotent, test replay and cancellation; no end-to-end integration was run.


- https://docs.temporal.io/develop/python
- https://docs.celeryq.dev/en/stable/userguide/tasks.html

Alternatives: Celery for independent queued jobs; direct function for bounded work

### Deployment: Container or managed Python service; WSGI for sync applications, ASGI when justified

Use the Django production deployment interface and checklist.

Limits and integration: Choose/pin a compatible application server at implementation; never deploy runserver. Configure secrets, HTTPS, static assets, health checks and backups.


- https://docs.djangoproject.com/en/6.0/howto/deployment/
- https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/
- https://docs.astral.sh/uv/guides/integration/docker/

Alternatives: Existing organization deployment platform

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

### Transactional email: django.core.mail + selected SMTP backend

Built-in mail wrappers and test backends fit account/product messages

Limits and integration: Configure TLS, sender and backend; test HTML/text content and enqueue required delivery. Delivery and bounce monitoring remain provider responsibilities.


- https://docs.djangoproject.com/en/6.0/topics/email/

Alternatives: Preserve an existing compatible project choice

### Uploads and file storage: Django FileField + configured storage backend

Framework file APIs separate model metadata from storage

Limits and integration: Configure storage for the selected host; validate upload size/type and authorize serving. Local MEDIA_ROOT is unsuitable for unshared ephemeral replicas; choose an external backend when required.


- https://docs.djangoproject.com/en/6.0/topics/files/

Alternatives: Preserve an existing compatible project choice

## Architecture and developer workflow

Django organizes projects into applications, with conventional URL/view/model boundaries and integrated authentication. Recommendation: keep domain operations and permissions reusable across HTTP views, admin actions and workers. Optional Celery and Channels are separate execution/messaging systems rather than core Django features.

Version scope: Django 6.0 versioned docs; Celery 5.6.3 and Channels 4.3.2 current docs fetched 11 October 2026. The Django 6 Tasks API is version-specific and does not imply an existing Django 5.2 project should upgrade or abandon Celery. Pin actual Python/package versions before qualifying composition.
Reviewed: 2026-10-11 | Evidence: documentation-reviewed | Source record: inputs/research/migrations-server.json

### Architecture boundaries

- Django defaults to database autocommit; transaction.atomic defines an explicit transaction boundary. Recommendation: keep transactions around the domain operation and do external delivery after commit through a recoverable design when required.
- Django 6 Tasks defines and enqueues tasks but supplies no worker mechanism. A production backend/worker must be evaluated; Celery remains a separate established candidate. Recommendation: do not equate an API-level task declaration with durable execution.
- Channels channel layers exchange high-level application events. channels_redis is the official production-supported layer; the in-memory layer cannot communicate across processes. Recommendation: persist business state separately from transient fanout.

### Tools and feedback

- In a disposable target, django-admin startproject mysite creates the project and python manage.py startapp polls creates an application. Preserve the existing project/application structure when migrating a feature.
- Use python manage.py makemigrations to prepare reviewed migration files, python manage.py migrate to apply them and python manage.py showmigrations to inspect recorded state. Recommendation: nominate one deployment migration runner for shared tables.
- For a configured Celery application, adapt celery -A tasks worker --loglevel=INFO from the official first-steps recipe, replacing tasks with the actual application module. Broker and optional result backend are separate configuration choices.
- Before a production target, adapt python manage.py check --deploy to its production settings as the checklist instructs. Recommendation: exercise real database, session, task worker and Channels topology; the development runserver is not a production deployment.

### Translations to avoid

- Avoid deploying Django 6 ImmediateBackend/DummyBackend as a substitute for a durable production queue; the Tasks framework requires an external executing backend and documents built-in development/test backends.
- Avoid treating transaction.on_commit as durable cross-store delivery: callbacks run after commit and their failures cannot roll back the transaction. Recommendation: use an outbox when lost dispatch after commit is unacceptable.
- Avoid using LocMemCache or Channels in-memory layers as shared multi-process state; both are process-local. Avoid using cache-only session storage when eviction/restart logout violates the product contract.
- Avoid running two Celery beat schedulers for the same schedule; Celery documents duplicate task production. Recommendation: transfer ownership across frameworks as well as within Celery.

### Architecture sources

- [Django first application](https://docs.djangoproject.com/en/6.0/intro/tutorial01/): Project/application generator commands and development server boundary.
- [Django Migrations](https://docs.djangoproject.com/en/6.0/topics/migrations/): Migration commands, history, data migrations and reversibility.
- [Django Transactions](https://docs.djangoproject.com/en/6.0/topics/db/transactions/): Autocommit, atomic, on_commit timing/failure and application-state rollback limitations.
- [Django 6 Tasks](https://docs.djangoproject.com/en/6.0/topics/tasks/): Task API, no built-in worker, backend requirements, argument conversion and commit timing.
- [Django Sessions](https://docs.djangoproject.com/en/6.0/topics/http/sessions/): Database/cache/cached_db/cookie choices, persistence, eviction and serialization.
- [Django Authentication](https://docs.djangoproject.com/en/6.0/topics/auth/default/): Authentication, login/logout and permissions.
- [Django Cache](https://docs.djangoproject.com/en/6.0/topics/cache/): Backend setup, key versions, per-process local memory and filesystem security concerns.
- [Channels Channel Layers](https://channels.readthedocs.io/en/stable/topics/channel_layers.html): Official production channels_redis and lack of cross-process delivery in memory.
- [Celery Tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html): Task naming/serialization, retries, acknowledgement and idempotency concerns.
- [Celery Periodic Tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html): Single scheduler ownership, schedule timezone and overlap concerns.
- [Celery First Steps](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html): Worker command and distinction between broker and result backend.
- [Django Deployment Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/): Production settings, check --deploy and deployment responsibilities.

## Transition options

Proposed designs and checks; these are not executed compatibility results.

### Data and schema

**Inspect the source:** Capture schema, account IDs, database constraints and model/write side effects. Migration history is framework-owned metadata and must be reconciled deliberately when an existing schema changes owner.

**During coexistence:** Recommendation: retain one domain writer and schema runner; add compatible fields and move one application/domain boundary while old code still reads new records. Use historical models for Django data migrations as documented.

**Target design:** Django models/migrations with explicit transaction.atomic boundaries for related database writes. Recommendation: delay field deletion until the rollback reader retires.

**Rollback:** Recommendation: restore the old writer while retaining additive fields; rehearse reverse migrations on a disposable copy and reconcile non-reversible data operations.

**Benefits and prerequisites**

- Recommendation: coherent model and migration ownership makes a domain boundary reviewable. Requires: Tested schema mapping and explicit writer transfer. Tradeoffs: Database reversal may be irreversible for data operations; application objects/cache state also need reconciliation.

**Checks before transfer**

- Create in each permitted writer and read in both runtimes; compare identifiers, null values, timestamps and constraint failures.
- Fail inside transaction.atomic and verify database writes roll back; inspect whether in-memory/cache state requires explicit restoration.

- https://docs.djangoproject.com/en/6.0/topics/migrations/
- https://docs.djangoproject.com/en/6.0/topics/db/transactions/

### Jobs and schedules

**Inspect the source:** Inventory task names, argument serializer, broker/result backend, retry/acknowledgement policy, periodic schedule and ready/delayed/failed/running work. Django 6 Tasks and Celery payloads are distinct contracts.

**During coexistence:** Recommendation: keep old consumers for old tasks; isolate new categories and route producers deliberately. Retain the existing scheduler until an explicit one-owner transfer. Qualify any Django Tasks backend separately from the task API.

**Target design:** Celery with a selected broker/optional result backend, or a qualified Django 6 executing backend. Schedule dispatch after database commit; recommendation: add recoverable outbox delivery when a crash can occur before broker acceptance.

**Rollback:** Recommendation: pause new producers, retain consumers for accepted payloads and reconcile completed effects before switching categories back.

**Benefits and prerequisites**

- Recommendation: execution can migrate by task category while the old backlog remains executable. Requires: Qualified payload fixtures, retained consumers and one schedule owner. Tradeoffs: Two task systems may be operated; a framework API switch does not translate backlog or broker guarantees.

**Checks before transfer**

- Capture a task envelope and run it through its intended consumer, including argument conversion and missing-record behavior.
- Rollback the domain transaction and verify no dispatch; kill after an external effect and validate replay-safe completion.
- Account for delayed/retry/failed/in-flight tasks and confirm one periodic enqueue for each transferred schedule.

- https://docs.djangoproject.com/en/6.0/topics/tasks/
- https://docs.djangoproject.com/en/6.0/topics/db/transactions/
- https://docs.celeryq.dev/en/stable/userguide/tasks.html
- https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html

### Identity and authorization

**Inspect the source:** Record authentication backend, user mapping, session engine/cookie name, serializer, expiry and revocation. Django database, cached_db, cache-only and signed-cookie sessions have different persistence/failure behavior.

**During coexistence:** Recommendation: retain a shared identity authority or qualified exchange; do not treat Redis key sharing as session-format compatibility. Keep every resource permission enforced in the target view/operation.

**Target design:** Django authentication with a selected session backend. cached_db writes through to database/cache and reads the database on cache misses; recommendation: prefer it over cache-only sessions when eviction logout is unacceptable.

**Rollback:** Recommendation: preserve previous identity/session contracts through the rollback window and retain revocation state during traffic reversal.

**Benefits and prerequisites**

- Recommendation: a durable session authority can preserve access through cache eviction. Requires: Configured database sessions, compatible account mapping and tested revocation. Tradeoffs: Write-through caching adds operations; cookie continuity across runtimes still requires a decoder/exchange or planned reauthentication.

**Checks before transfer**

- Login in the old system, access the Django feature, then logout/expire/revoke and verify both deny unauthorized operations.
- Evict the selected session cache and confirm behavior matches the chosen engine; test another tenant’s identifier with a valid login.

- https://docs.djangoproject.com/en/6.0/topics/http/sessions/
- https://docs.djangoproject.com/en/6.0/topics/auth/default/

### Realtime transport

**Inspect the source:** Capture WebSocket protocol, group/event names, authentication and required missed-event behavior. Channels channel layers carry application-level events, not a universal client protocol.

**During coexistence:** Recommendation: keep old client endpoints, bridge versioned domain events and route room/user cohorts including reconnects. Designate one committed-change publisher; use the configured shared layer for multiple processes.

**Target design:** Channels with channels_redis when using the documented official production channel layer. Recommendation: reconstruct/replay from persistent domain state when missed broadcasts matter.

**Rollback:** Recommendation: retain the previous endpoint/event envelope and route cohorts back including their reconnects; avoid replaying already-applied effects.

**Benefits and prerequisites**

- Recommendation: a shared channel layer enables cross-process fanout. Requires: Configured Redis layer, matching consumers/events and authorized subscriptions. Tradeoffs: Redis remains operated; transient fanout alone does not provide durable business-message recovery.

**Checks before transfer**

- Connect subscribers to separate processes and verify one committed change reaches both authorized groups.
- Restart/disconnect during an event and verify reconnect obtains missing domain state; revoke access and confirm rejected subscriptions.

- https://channels.readthedocs.io/en/stable/topics/channel_layers.html

### Caching and shared state

**Inspect the source:** Inventory key versions/prefixes, serializers, TTLs and invalidation, separating disposable values from session/coordination ownership. Django local-memory cache is per-process even though it is thread-safe.

**During coexistence:** Recommendation: use separate namespaces for changed representations and invalidate both old/new readers. Retain shared storage for cross-process requirements; move only reconstructible local data to LocMemCache.

**Target design:** A deliberately selected Django cache backend with configured timeout/key version. Recommendation: use local caches only where node/process staleness is accepted and rebuilding is safe.

**Rollback:** Recommendation: restore old namespace/backend routing and repopulate from authoritative data without treating cache contents as business records.

**Benefits and prerequisites**

- Recommendation: reconstructible caching can change independently of domain writes. Requires: Defined staleness, invalidation and data ownership. Tradeoffs: Per-process caches duplicate state; sensitive filesystem cache locations/serialization require care as the docs explain.

**Checks before transfer**

- Warm two processes, commit a source update and verify both readers meet the stated staleness policy.
- Restart or empty only the dedicated cache and verify reconstruction; session/permission correctness must remain intact.

- https://docs.djangoproject.com/en/6.0/topics/cache/
- https://docs.djangoproject.com/en/6.0/topics/db/transactions/

### Delivery and recovery

**Inspect the source:** List production application server, settings/secrets, migrations, static/media handling, Celery worker/beat and Channels processes. Celery requires only one scheduler for a schedule at a time.

**During coexistence:** Recommendation: keep both process inventories and one named migration/schedule owner during coexistence. Define promotion thresholds for outcomes, queue age and denied access rather than promoting from a clean startup alone.

**Target design:** An explicitly configured deployment following Django’s checklist, plus independently supervised selected workers and scheduler. Recommendation: document restored database/session/queue consistency.

**Rollback:** Recommendation: restore old routing/settings and schedule ownership explicitly; preserve accepted tasks and reconcile effects before replay.

**Benefits and prerequisites**

- Recommendation: production checks and role ownership make recovery responsibilities visible. Requires: Actual production settings and a rehearsed restore/restart. Tradeoffs: check --deploy detects configuration issues, not end-to-end job, permission or restore correctness.

**Checks before transfer**

- Run the deployment checks against intended settings and exercise an authorized/denied request after a disposable restore.
- Stop a worker and verify queued work is visible; restart it, then verify one scheduler and intended recovery behavior.

- https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/
- https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html

Rewrite workflow: /rewrite/guide.md
Shared contracts and phases: /rewrite/contracts.json


## Setup
1. Complete the selected starting point and baseline checks in the Generators section first; then continue with the integration steps appropriate to the chosen component.
2. After completing the selected generated baseline, resolve compatible dependencies through uv. For the default PostgreSQL choice, run uv add "psycopg[binary]"; configure the selected development database before migrations. Preserve an existing maintained database choice.
3. From the project root, run uv add --dev ruff mypy django-stubs pytest pytest-django after checking the django-stubs compatibility table for the selected Django/Python/mypy combination.
4. Use the follow-up startapp generator when a domain app is needed; register its AppConfig and configure environment-owned PostgreSQL credentials, auth/session settings, pytest DJANGO_SETTINGS_MODULE and the django-stubs mypy plugin/settings module.
5. Implement one authorized vertical slice. Use the follow-up migration generator, inspect the resulting operations and apply reviewed migrations to the disposable development database.
6. Add Celery only for actual queued work; configure its broker, worker and after-commit enqueueing. Add Temporal only when durable multi-step recovery is required.
7. Document application server, static asset collection, migration release ordering, worker start/restart and rollback. Complete baseline and application verification before deployment.

## Verification
Commands below require the selected tools and project configuration. Replace example paths, schemes and IDs; distinguish tests from builds and interactive startup. These are instructions, not recorded passes.

```text
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run mypy core config
uv run pytest
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py migrate --check
uv run python manage.py check --deploy --settings=config.production
```

## Open questions
- Which supported Python/Django versions and third-party packages are required?
- Which host owns HTTPS, static/media serving and deployment settings?
- Which identity, email/storage, broker and job-delivery guarantees are required?

## Sources
- [uv projects](https://docs.astral.sh/uv/guides/projects/)
- [Ruff installation](https://docs.astral.sh/ruff/installation/)
- [django-stubs](https://github.com/typeddjango/django-stubs)
- [mypy getting started](https://mypy.readthedocs.io/en/stable/getting_started.html)
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)
- [pytest-django](https://pytest-django.readthedocs.io/en/latest/)
- [Django migrations](https://docs.djangoproject.com/en/6.0/topics/migrations/)
- [Django form validation](https://docs.djangoproject.com/en/6.0/ref/forms/validation/)
- [Pydantic strict mode](https://pydantic.dev/docs/validation/latest/concepts/strict_mode/)
- [Django authentication](https://docs.djangoproject.com/en/6.0/topics/auth/)
- [Django deployment checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
- [Celery Django integration](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html)
- [Celery tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [Django Tasks](https://docs.djangoproject.com/en/6.0/topics/tasks/)
- [Temporal Python SDK](https://docs.temporal.io/develop/python)
- [Django deployment](https://docs.djangoproject.com/en/6.0/howto/deployment/)
- [uv Docker](https://docs.astral.sh/uv/guides/integration/docker/)
- [Python logging](https://docs.python.org/3/library/logging.html)
- [Tenacity documentation](https://tenacity.readthedocs.io/en/latest/)
- [Django sending email](https://docs.djangoproject.com/en/6.0/topics/email/)
- [Django files](https://docs.djangoproject.com/en/6.0/topics/files/)

Keep the project README current and link the selected guidance; preserve existing project instructions.
