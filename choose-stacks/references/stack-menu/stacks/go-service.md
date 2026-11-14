# Go service

HTTP APIs and backend services with a straightforward binary deployment.

Language: Go | Reviewed: 2026-10-10 | Evidence: documentation-reviewed research input

Source record: menu/inputs/research/go-rust.json.

Core guidance checked: 2026-10-13. Review sources are listed below. /research-freshness.json describes the imported research packet; this record retains its own evidence scope. These recipes and selected dependency combinations need qualification in the actual project.

## Application role
Components: api
UI: none
Deployment: binary

## Use cases
- APIs
- control planes
- concurrent network services
- background workers

## Fit
- Prefer explicit service code and standard tooling
- Kubernetes or Go infrastructure integration matters
- PostgreSQL already owns business state

## Choose something else when
- Need a batteries-included product framework
- Hard real-time or no-GC constraints
- Rich client UI is the primary product

## Agent workflow
- Read README, dependency manifests, lockfiles, runtime pins and the maintained project workflow before changing anything. Preserve an existing stack unless reconsidering it is part of the request.
- For a new component, read the Generators section before writing application files. Use its appropriate official initializer and retain its generated baseline; follow-up generators are conditional on the selected feature.
- Use this guide to select tools by requirement. Resolve compatible versions from official and installed-version documentation; record the actual lockfile and runtime versions.
- Create a plan for schema changes, identity, authorization, external effects and deployment. A library choice does not complete its integration.
- Run relevant checks after configuration. Exercise the real interface, failure paths and packaged artifact on the intended target. Report commands, versions, results and untested behavior.
- On failure, retain the command and diagnostic, fix the failing prerequisite and resume there. Do not regenerate over existing work or suppress failures to make a check green.

## Best practices
- Propagate contexts and set timeouts on external requests. Bound concurrency and handle shutdown.
- Keep SQL and migrations reviewed and generated query code synchronized with the schema.
- Test handlers with httptest and persistence against a disposable real PostgreSQL instance.
- Use River only when durable jobs are required; test retry-safe effects and worker shutdown.

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

#### Initialize the Go module

Use when: A new Go service has no go.mod; preserve an existing module rather than reinitializing it.

1. Install the project-selected Go toolchain; choose an empty local source directory outside synced storage.
2. Replace /path/to/workspace and example.com/project with the real local path and module import path; create project once, then enter it.
3. Initialize metadata, then implement the net/http service and its tests; the standard library does not provide an application scaffold generator.

Working directory: /path/to/workspace (existing local source parent)

Create an empty project directory.

```sh
mkdir project
```

Working directory: /path/to/workspace/project

Create go.mod using the real module path.

```sh
go mod init example.com/project
```

- There is no universal Go net/http service generator in this profile. Routing, configuration validation, graceful shutdown and tests remain application work.

### Conditional follow-up generators

#### sqlc query code

Use when: Only when sqlc is selected and schema, annotated queries and sqlc.yaml/sqlc.json have been written.


Working directory: /path/to/workspace/project (sqlc configuration directory; selected sqlc installed)

Generate typed query access from owned SQL inputs.

```sh
sqlc generate
```

- Install and record a selected sqlc release first. Configure pgx/v5 output for this profile. Regenerate after schema/query changes; this command does not create migrations or the HTTP application.

#### goose SQL migration

Use when: Only when goose owns migrations for this database.


Working directory: /path/to/workspace/project (selected goose installed)

Create a timestamped migration to edit and review.

```sh
goose -dir migrations create initial sql
```

- Install and record a selected goose release first. Keep one migration owner. Write and test migration SQL using a disposable PostgreSQL database before deployment.

#### templ component code

Use when: Only when the optional templ UI has been selected and .templ source exists.


Working directory: /path/to/workspace/project (selected templ CLI installed)

Generate Go component code from .templ sources.

```sh
templ generate
```

- Match the selected CLI and module versions; preserve editable .templ inputs and the chosen generated-code policy.

#### GoReleaser configuration

Use when: Only when GoReleaser is selected for this application and no release configuration exists.


Working directory: /path/to/workspace/project (module root; selected GoReleaser installed)

Generate .goreleaser.yaml.

```sh
goreleaser init
```

Working directory: /path/to/workspace/project

Validate the reviewed release configuration.

```sh
goreleaser check
```

- Install and record the project-selected GoReleaser release first. Review build entry points, targets, hooks and publishing settings; generation does not authorize a release.

### Preserve the generated foundation

- Preserve go.mod and go.sum when generated by dependency resolution; record the Go version and resolved generator versions.
- go mod init creates module metadata, not source files, tests, a service structure or .gitignore. Add project-specific ignores, including OS metadata, without claiming they came from Go.
- Keep generator-created files as the baseline; document deliberate changes and do not replace standard defaults with a handwritten approximation.
- Preserve SQL migrations, sqlc configuration, query sources and the agreed generated-code policy.

### Baseline and generation checks

- In the actual project, record generator versions and commands, then compare its initial files with a fresh output from the same versions and options.
- After source exists, run gofmt -l ., go test ./..., go vet ./... and go build ./... from the module root; a bare go.mod is not a runnable application.
- In a disposable copy, check candidate staging includes source and required manifests but excludes binaries, caches, local credentials and .DS_Store; inspect git add --dry-run -A before changing a real index.
- For selected tools, regenerate sqlc/templ and inspect changes; validate migrations against a disposable database.

### Generation receipt

- Component and selected starting point, or the documented absence of a full application generator
- Generator/toolchain versions, exact commands or IDE template/settings, working directory and generated destination
- Generated files retained, deliberate deviations with reasons, and required supplemental ignore rules
- Baseline checks and later checks actually run, results and remaining prerequisites or untested behavior

### Generator sources

- [Go module creation tutorial](https://go.dev/doc/tutorial/create-module)
- [Go modules reference: go mod init](https://go.dev/ref/mod#go-mod-init)
- [sqlc PostgreSQL getting started](https://docs.sqlc.dev/en/latest/tutorials/getting-started-postgresql.html)
- [goose CLI commands](https://pressly.github.io/goose/documentation/cli-commands/)
- [templ CLI](https://templ.guide/commands-and-tools/cli)
- [GoReleaser quick start](https://goreleaser.com/getting-started/quick-start/)

## Tools

### HTTP server: net/http

Standard handlers and request contexts minimize routing infrastructure.

Limits and integration: Set request/body limits, deadlines and graceful shutdown; middleware and authorization remain application work.


- https://pkg.go.dev/net/http

Alternatives: Existing project router when justified

### Optional server-rendered UI: templ + HTMX

Compiled components and HTML-fragment updates suit forms and dashboards.

Limits and integration: Generation adds a build step; advanced client state still needs browser-side design and testing.


- https://templ.guide/
- https://htmx.org/docs/

Alternatives: No UI for API-only services

### Database and migrations: PostgreSQL + pgx + sqlc + goose

Visible SQL, generated typed access and one migration owner.

Limits and integration: Generators do not prove query efficiency; review transaction boundaries, pool budgets and online migration behavior. Never mix migration owners.


- https://github.com/jackc/pgx
- https://docs.sqlc.dev/en/latest/
- https://github.com/pressly/goose
- https://github.com/golang-migrate/migrate

Alternatives: pgx without sqlc for small query sets; golang-migrate when already established

### Configuration: Typed settings loaded with os.LookupEnv

Explicit startup validation and standard structured logs.

Limits and integration: Define precedence; reject malformed required values; redact secrets. Environment access alone is not validation or secret management.


- https://pkg.go.dev/os
- https://pkg.go.dev/flag
- https://pkg.go.dev/log/slog

Alternatives: flag for small command surfaces

### Application logging: log/slog

Explicit startup validation and standard structured logs.

Limits and integration: Define precedence; reject malformed required values; redact secrets. Environment access alone is not validation or secret management.


- https://pkg.go.dev/os
- https://pkg.go.dev/flag
- https://pkg.go.dev/log/slog

### Tests and static checks: testing; go vet; race detector; govulncheck

Standard toolchain feedback plus exercised concurrency and known-vulnerability checks.

Limits and integration: Race detector requires supported target/toolchain and exercised code; no scanner proves absence of vulnerabilities.


- https://pkg.go.dev/testing
- https://go.dev/doc/articles/race_detector
- https://golangci-lint.run/docs/welcome/quick-start/
- https://go.dev/doc/security/vuln/

### HTTP and database integration tests: httptest + real disposable PostgreSQL

Exercise protocols and actual SQL/migrations.

Limits and integration: Database tests need an isolated database; mocks cannot establish PostgreSQL semantics.


- https://pkg.go.dev/net/http/httptest
- https://github.com/jackc/pgx

Alternatives: In-process handler tests for pure routing

### Durable work: River for PostgreSQL-backed jobs

Transactional enqueueing ties work to committed business data.

Limits and integration: External effects need idempotency. Default resumable checkpoints may be lost on crash; use transactional checkpoints where required. Inspect Pro feature boundaries.


- https://riverqueue.com/docs/transactional-enqueueing
- https://riverqueue.com/docs/resumable-jobs
- https://docs.temporal.io/develop/go

Alternatives: Temporal Go SDK for workflow requirements needing its service

### Deployment and distribution: Go build binary in a supervised process or container; GoReleaser for releases

Small explicit runtime boundary; release automation builds target artifacts.

Limits and integration: Target OS/architecture, libc/cgo, CA certificates, timezone data and signing need explicit verification. Snapshot builds are not publication.


- https://goreleaser.com/getting-started/quick-start/

### Browser identity: go-oidc + existing OIDC provider

Provider discovery and ID-token verification support owned login sessions

Limits and integration: Use v3 module; configure issuer/client, OAuth callback state and session lifecycle. go-oidc verifies ID tokens; API access-token validation follows the provider contract. Authorization stays near data.


- https://github.com/coreos/go-oidc

Alternatives: Preserve an existing compatible project choice

### Transactional email: go-mail + project-selected SMTP provider

Typed mail construction and SMTP transport support application messages

Limits and integration: Configure TLS, sender credentials and timeouts; send required mail through durable jobs with duplicate protection. Validate chosen async/runtime features in Rust; delivery receipts and bounces need provider handling.


- https://pkg.go.dev/github.com/wneessen/go-mail

Alternatives: Preserve an existing compatible project choice

### Uploads and object storage: AWS SDK for Go S3 client

Durable object storage avoids dependence on service-local disk

Limits and integration: Configure runtime credentials, region and least-privilege bucket access; authorize object keys and uploads, bound size/concurrency and define retention. Test multipart cleanup and selected provider compatibility.


- https://docs.aws.amazon.com/sdk-for-go/v2/developer-guide/go_s3_code_examples.html

Alternatives: Preserve an existing compatible project choice

### Realtime transport: coder/websocket

WebSocket support fits bidirectional connected clients

Limits and integration: Enable the documented module/feature; authorize handshake and every protected message, bound queues/message size and implement heartbeat/shutdown. Socket delivery is not durable history; define reconnect/resync.


- https://pkg.go.dev/github.com/coder/websocket

Alternatives: Server-sent events for one-way feeds; Polling for infrequent updates

## Architecture and developer workflow

Recommendation: a Go HTTP process owns request admission and cancellation, domain packages own invariants, and a bounded SQL connection pool provides parallel database access. Durable jobs have their own persisted queue and worker lifecycle. Goroutines and buffered channels are concurrency mechanisms; graceful drain does not turn them into a recoverable queue.

Version scope: Go 1.27 release documentation and current net/http/context APIs; sqlc latest transaction guide with pgx/v5; River current documentation, PostgreSQL composition. Resolve and record Go toolchain, sqlc, pgx and River versions in go.mod/go.sum and tool configuration before implementation. Official release notes identify Go 1.27 as the August 2026 release; this research does not qualify a lockfile or patch-version/security support.
Reviewed: 2026-10-11 | Evidence: documentation-reviewed | Source record: inputs/research/migrations-systems.json

### Architecture boundaries

- Recommendation: compose net/http handlers around small domain packages and explicit interfaces at external boundaries. Pass request contexts into SQL and outbound calls. Use bounded errgroup fan-out or a worker pool, with an overload policy separate from concurrency limits.
- Recommendation: maintain reviewed SQL migrations and sqlc-generated queries; share a pool, acquire transactions only around domain writes, and call generated WithTx for the transaction. A single global mutex around all queries recreates avoidable serialization.
- Recommendation: PostgreSQL-backed River workers can run with the web binary initially or in an independent process when their scaling or shutdown needs differ. Insert business state and a job in the same database transaction when atomic enqueue is required; cross-database work needs a separately designed outbox.
- Recommendation: retain an established identity provider, object store, email sender and broker during a service rewrite. Request/response, cookies, WebSocket application protocol, job payload and retry semantics are separate compatibility contracts.

### Tools and feedback

- Recommendation: start from the existing repository; inspect go.mod, go.sum, schema migrations and queue configuration. For a new local source project, go mod init example.com/service creates a module; choose the actual module path and supported toolchain deliberately.
- Recommendation: pin sqlc using the maintained tool installer, review sqlc.yaml and SQL source, then run sqlc generate after query/schema changes. Regenerate in CI and compare output; generated typing does not validate production schema drift.
- Recommendation: run gofmt on changed files, go vet ./..., go test ./... and go test -race ./... on a supported target. Add HTTP contract fixtures and cancellation/queue crash tests against the selected database; these are proposed checks, not executed here.
- Recommendation: build the service with go build ./cmd/server when that entry point exists. Set server/header/body deadlines, worker limits, pool capacity and shutdown budget from the deployment shape. Profile a representative workload with Go pprof; performance and cost remain unmeasured.

### Translations to avoid

- Avoid one fire-and-forget goroutine per email/payment: an acknowledged request can survive while its side effect disappears on process crash.
- Avoid spawning unlimited goroutines to hide slow SQL. The downstream pool becomes the queue; cancellation, memory and overload must be bounded explicitly.
- Avoid replacing Redis solely because Go has channels. Shared fan-out, sessions, queue persistence and locks have different semantics.
- Avoid treating Server.Shutdown as complete WebSocket shutdown; hijacked connections need separate notification and tracking.

### Architecture sources

- [Go 1.27 release notes](https://go.dev/doc/go1.27): Identifies the August 2026 release; runtime/tool behavior and JSON v2 are documented with compatibility caveats.
- [Managing Go dependencies](https://go.dev/doc/modules/managing-dependencies): go.mod and go.sum own module dependency versions.
- [sqlc transactions](https://docs.sqlc.dev/en/latest/howto/transactions.html): Generated WithTx binds queries to a transaction; pgx/v5 example is documented.
- [Go SQL connection management](https://go.dev/doc/database/manage-connections): sql.DB is a concurrent pool; limits can cause waits and deadlocks.
- [River transactional enqueue](https://riverqueue.com/docs/transactional-enqueueing): Enqueue with domain changes in one transaction avoids a two-store commit gap.
- [River retries](https://riverqueue.com/docs/job-retries): Retry attempts and delays are configurable; errors lead to repeated execution.
- [River Ruby integration](https://riverqueue.com/docs/ruby): Current documentation describes a shared River schema and explicit job kinds/JSON arguments.
- [net/http server shutdown](https://pkg.go.dev/net/http#Server.Shutdown): HTTP drain does not close or await hijacked WebSocket connections.
- [errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup): WithContext cancellation and SetLimit support bounded concurrent work.
- [os/signal](https://pkg.go.dev/os/signal#NotifyContext): NotifyContext connects OS signals to context cancellation.
- [coder/websocket README](https://github.com/coder/websocket): Go WebSocket transport supports contexts and close handshakes; application protocol is separate.
- [Redis Pub/Sub](https://redis.io/docs/latest/develop/pubsub/): Pub/Sub delivery is at-most-once; disconnected subscribers miss events.

## Transition options

Proposed designs and checks; these are not executed compatibility results.

### Data and schema

**Inspect the source:** Inventory the old schema, isolation, identifiers, null handling, timestamps and transaction invariants before changing language or driver.

**During coexistence:** Recommendation: let the old application own migrations while Go accesses backward-compatible columns through sqlc; route writes for one domain/cohort to one owner. Expand schema before either runtime needs it.

**Target design:** Recommendation: sqlc plus pgx/v5 or database/sql, a shared bounded pool and explicit transaction-scoped queries. Keep the existing database if its guarantees fit; PostgreSQL replacement is a separate migration.

**Rollback:** Recommendation: return domain traffic to the old writer while preserving expanded columns. Contract migrations wait until the rollback window closes; reconcile any new-only writes first.

**Benefits and prerequisites**

- Typed query access and concurrent pool usage can improve maintainability and remove an unnecessary application-wide lock. Requires: Queries generated from the reviewed schema; representative null/time/transaction fixtures; a pool sized across all replicas. Tradeoffs: Generated types do not prove isolation or business correctness; pool exhaustion and migrations still need operations.

**Checks before transfer**

- Verify old-write/new-read and new-write/old-read round trips, including nulls and time zones.
- Force a mid-transaction failure; neither half of the domain change may commit.
- Saturate the pool and cancel a request; verify bounded waiting and connection release.

- https://docs.sqlc.dev/en/latest/howto/transactions.html
- https://go.dev/doc/database/manage-connections

### Jobs and schedules

**Inspect the source:** Capture existing queue kind, JSON arguments, retry/schedule/dead-letter states and external-effect idempotency. Redis/Resque or Sidekiq payloads are not River payloads.

**During coexistence:** Recommendation: keep old workers consuming old queues. Route selected job kinds into River through versioned producers; transform outstanding states explicitly and retain one scheduler. River Ruby integration is a possible bridge, not automatic Active Job execution.

**Target design:** Recommendation: River PostgreSQL jobs with domain writes plus InsertTx in the same transaction, explicit queue concurrency and bounded retry policy. Keep Redis for any remaining broker/session/cache responsibility.

**Rollback:** Recommendation: stop new River producers and reroute only unstarted work after reconciliation. Keep a compatible River consumer for already accepted jobs; a broker switch cannot undo sent messages or payments.

**Benefits and prerequisites**

- Atomic enqueue closes the gap between committing domain state and creating work. Requires: Domain rows and River insertion use the same transaction/database; validated job-kind/argument mapping; replay-safe external effects. Tradeoffs: Adds queue schema/maintenance to the database; retries can repeat effects; backlog migration and adapter compatibility are separate work.

**Checks before transfer**

- Abort the domain transaction; no job may become available.
- Crash after sending an email but before job completion; retry must reconcile or reuse a stable external idempotency key.
- Account for ready, scheduled, retry, failed and in-flight jobs before retiring the old consumer.

- https://riverqueue.com/docs/transactional-enqueueing
- https://riverqueue.com/docs/job-retries
- https://riverqueue.com/docs/ruby

### Delivery and recovery

**Inspect the source:** Preserve response/error behavior, overload rules, deadlines and restart guarantees; establish separate budgets for HTTP and background jobs.

**During coexistence:** Recommendation: serve a fixed tenant/endpoint cohort from Go behind existing routing, with errgroup/context cancellation inside each operation and deployment-level readiness. Keep the old instance ready for contract-compatible rollback.

**Target design:** Recommendation: signal.NotifyContext, bounded admission/fan-out, Server.Shutdown with a fresh timeout context, tracked worker termination and pool closure after accepted work ends.

**Rollback:** Recommendation: return routing to the old process and inspect committed outcomes and queued work before any replay. Preserve identical database/schema contracts for both versions.

**Benefits and prerequisites**

- Cooperative cancellation limits work that callers no longer need and makes planned shutdown observable. Requires: Every called operation honors context; in-flight tasks are tracked; the platform shutdown grace period exceeds the configured drain budget. Tradeoffs: Cancellation does not reverse a committed write or external effect; forced termination still loses memory-only work.

**Checks before transfer**

- Cancel a client while SQL/outbound I/O is blocked; verify resources and goroutines settle.
- Send SIGTERM during a write; the server stops admitting traffic and records whether accepted work committed.
- Force SIGKILL; verify durable jobs recover independently of graceful drain.

- https://pkg.go.dev/net/http#Server.Shutdown
- https://pkg.go.dev/golang.org/x/sync/errgroup
- https://pkg.go.dev/os/signal#NotifyContext

### Realtime transport

**Inspect the source:** Preserve authentication, subscription identifiers, frame formats, ordering, reconnect cursors and cross-runtime fan-out. A WebSocket transport does not implement Action Cable automatically.

**During coexistence:** Recommendation: keep the existing broker and explicit application-protocol adapter while moving complete room/tenant cohorts, including reconnects, to Go. Publish/subscribe in both directions using captured protocol fixtures.

**Target design:** Recommendation: coder/websocket for transport plus bounded per-connection queues, tracked close handshakes and an application resynchronization path. Retain Redis Pub/Sub if ephemeral cross-process fan-out fits; add durable history separately where missed events matter.

**Rollback:** Recommendation: route the cohort and reconnects back together. Keep the broker and old protocol alive; rebuild client state from durable records rather than pretending ephemeral events can be replayed.

**Benefits and prerequisites**

- Explicit connection ownership and queue limits bound slow-client resource use. Requires: Capacity and disconnect policy are defined; clients can reconnect and reconstruct authoritative state; broker/protocol compatibility is tested. Tradeoffs: Redis Pub/Sub is at-most-once and does not replay disconnected messages; replacing it with process-local channels removes cross-instance delivery.

**Checks before transfer**

- Connect an old and new client to the same room; verify broadcasts in both directions and revocation.
- Disconnect a subscriber and publish; reconnect must fetch missed authoritative state.
- Throttle one client; verify the configured queue overflow policy and independent delivery to others.

- https://github.com/coder/websocket
- https://redis.io/docs/latest/develop/pubsub/
- https://pkg.go.dev/net/http#Server.Shutdown

Rewrite workflow: /rewrite/guide.md
Shared contracts and phases: /rewrite/contracts.json


## Setup
1. Complete the selected starting point and baseline checks in the Generators section first; then continue with the integration steps appropriate to the chosen component.
2. Resolve and record the selected Go/tool versions and dependencies; add pgx/v5 for PostgreSQL and River only when durable jobs are required.
3. After module initialization, implement the service entry point and application packages with typed settings, explicit http.Server limits, health/readiness and graceful shutdown.
4. When sqlc and goose are selected, use the follow-up generator instructions; write migrations, annotated queries and sqlc configuration, then generate typed query access. Keep database credentials in environment/secrets.
5. With GOOSE_DRIVER=postgres and GOOSE_DBSTRING pointing only to a disposable database, run goose -dir migrations up. Add HTTP, real-database, business transaction and selected River enqueue tests.
6. Add and review the chosen release configuration, pin tools and preserve go.mod/go.sum; document build, deployment and rollback. Qualify target runtime/cgo requirements. These application steps have not been executed.

## Verification
Commands below require the selected tools and project configuration. Replace example paths, schemes and IDs; distinguish tests from builds and interactive startup. These are instructions, not recorded passes.

```text
gofmt -l .
go test ./...
go test -race ./...
go vet ./...
govulncheck ./...
sqlc generate
goose -dir migrations status
go build ./cmd/server
```

## Open questions
- Which API contracts, browser login or service-token requirements apply?
- Does realtime need one-way updates or bidirectional sockets?
- Which database pool, worker throughput, storage and deployment/restore budgets apply?

## Sources
- [Go net/http](https://pkg.go.dev/net/http)
- [templ](https://templ.guide/)
- [HTMX](https://htmx.org/docs/)
- [pgx PostgreSQL driver](https://github.com/jackc/pgx)
- [sqlc documentation](https://docs.sqlc.dev/en/latest/)
- [goose migrations](https://github.com/pressly/goose)
- [golang-migrate](https://github.com/golang-migrate/migrate)
- [Go os configuration primitives](https://pkg.go.dev/os)
- [Go flag](https://pkg.go.dev/flag)
- [Go structured logging](https://pkg.go.dev/log/slog)
- [Go testing](https://pkg.go.dev/testing)
- [Go data race detector](https://go.dev/doc/articles/race_detector)
- [golangci-lint quick start](https://golangci-lint.run/docs/welcome/quick-start/)
- [Go vulnerability management](https://go.dev/doc/security/vuln/)
- [Go HTTP testing](https://pkg.go.dev/net/http/httptest)
- [River transactional enqueueing](https://riverqueue.com/docs/transactional-enqueueing)
- [River resumable jobs](https://riverqueue.com/docs/resumable-jobs)
- [Temporal Go SDK](https://docs.temporal.io/develop/go)
- [GoReleaser quick start](https://goreleaser.com/getting-started/quick-start/)
- [go-oidc repository](https://github.com/coreos/go-oidc)
- [go-mail documentation](https://pkg.go.dev/github.com/wneessen/go-mail)
- [AWS Go S3 examples](https://docs.aws.amazon.com/sdk-for-go/v2/developer-guide/go_s3_code_examples.html)
- [coder/websocket documentation](https://pkg.go.dev/github.com/coder/websocket)

Keep the project README current and link the selected guidance; preserve existing project instructions.
