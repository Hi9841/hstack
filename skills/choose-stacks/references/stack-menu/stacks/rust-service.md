# Rust service

Services where runtime control and explicit resource handling matter.

Language: Rust | Reviewed: 2026-10-10 | Evidence: documentation-reviewed research input

Source record: menu/inputs/research/go-rust.json.

Core guidance checked: 2026-10-13. Review sources are listed below. /research-freshness.json describes the imported research packet; this record retains its own evidence scope. These recipes and selected dependency combinations need qualification in the actual project.

## Application role
Components: api
UI: none
Deployment: binary

## Use cases
- Native network services
- resource-sensitive APIs
- services sharing a Rust core

## Fit
- Memory/resource control or Rust library reuse is important
- Team accepts ownership/async complexity for compile-time guarantees

## Choose something else when
- Primary goal is conventional CRUD delivery with minimal framework assembly
- Team cannot maintain Rust async code
- A full product framework is needed immediately

## Agent workflow
- Read README, dependency manifests, lockfiles, runtime pins and the maintained project workflow before changing anything. Preserve an existing stack unless reconsidering it is part of the request.
- For a new component, read the Generators section before writing application files. Use its appropriate official initializer and retain its generated baseline; follow-up generators are conditional on the selected feature.
- Use this guide to select tools by requirement. Resolve compatible versions from official and installed-version documentation; record the actual lockfile and runtime versions.
- Create a plan for schema changes, identity, authorization, external effects and deployment. A library choice does not complete its integration.
- Run relevant checks after configuration. Exercise the real interface, failure paths and packaged artifact on the intended target. Report commands, versions, results and untested behavior.
- On failure, retain the command and diagnostic, fix the failing prerequisite and resume there. Do not regenerate over existing work or suppress failures to make a check green.

## Best practices
- Keep blocking work off async executor threads and apply timeouts and concurrency limits.
- Use typed configuration and tracing; preserve useful context when returning errors.
- Rehearse SQLx migrations and validate prepared query metadata against the intended schema.
- Build for the actual deployment target. Type checks do not replace authorization, retry and load tests.

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

#### Cargo binary package

Use when: A new Rust service needs a new directory.

1. Install the chosen Rust toolchain. Replace /path/to/workspace with the actual local source parent; choose the real package name.
2. Generate a binary package; use --lib only for a reusable library rather than an executable.

Working directory: /path/to/workspace (existing local source parent)

Generate the executable package baseline.

```sh
cargo new project --bin
```

- A Cargo package is not a full framework application. Preserve generated defaults and add only selected dependencies.

#### Cargo in an existing directory

Use when: An existing source directory has no Cargo.toml and must become a package; choose this instead of cargo new.

1. Inspect existing files and parent VCS before initialization; preserve existing code.

Working directory: /path/to/workspace/project (existing directory without Cargo.toml)

Initialize a binary package in place.

```sh
cargo init --bin
```

- Use --lib for a library target. Do not run cargo init over an already initialized package.

### Conditional follow-up generators

#### SQLx migrations and checked-query metadata

Use when: Only when SQLx is selected and owns schema migrations; metadata applies when checked query macros are used.


Working directory: /path/to/workspace/project (matching sqlx-cli installed)

Create an editable migration file.

```sh
sqlx migrate add initial
```

Working directory: /path/to/workspace/project (DATABASE_URL targets a disposable database; migration SQL reviewed)

Apply migrations to the disposable database.

```sh
sqlx migrate run
```

Working directory: /path/to/workspace/project (checked query macros and matching disposable schema available)

Generate offline query metadata.

```sh
cargo sqlx prepare
```

- Install a selected sqlx-cli release compatible with the application and selected database/TLS features. Set DATABASE_URL through the environment or an untracked local file.
- Preserve migrations and commit .sqlx metadata for offline builds. Run cargo sqlx prepare --check after changes; pass workspace/feature/target options matching the project.

### Preserve the generated foundation

- Preserve Cargo.toml, generated source structure and Cargo.lock after dependency resolution for shipped applications. Record the chosen Rust toolchain and generator versions.
- Retain the VCS ignore baseline when generated, including build-output exclusions, and add project-specific OS metadata/secret rules. Cargo VCS behavior depends on parent repository and configuration; inspect actual output.
- Record and justify changes from the same-version generator baseline instead of recreating its files from memory.
- Preserve SQLx migrations and offline query metadata when selected; keep database credentials out of version control.

### Baseline and generation checks

- In the actual application, compare a fresh output from the recorded toolchain/options with the initial project and explain intentional differences.
- After initial dependency resolution, run cargo fmt --all -- --check, cargo test --locked and cargo build --locked from the package root; run the project-selected Clippy checks.
- In a disposable copy, inspect git add --dry-run -A and confirm source/manifests/lockfile are included while target/, credentials and .DS_Store are excluded.
- Cargo creates the package; Axum routing, Tokio runtime, configuration and shutdown remain explicit implementation. No full Axum application generator is asserted here.
- For SQLx, test migrations in the disposable database and run cargo sqlx prepare --check with the same relevant features and targets.

### Generation receipt

- Component and selected starting point, or the documented absence of a full application generator
- Generator/toolchain versions, exact commands or IDE template/settings, working directory and generated destination
- Generated files retained, deliberate deviations with reasons, and required supplemental ignore rules
- Baseline checks and later checks actually run, results and remaining prerequisites or untested behavior

### Generator sources

- [Cargo new](https://doc.rust-lang.org/cargo/commands/cargo-new.html)
- [Cargo init](https://doc.rust-lang.org/cargo/commands/cargo-init.html)
- [Cargo package and first build](https://doc.rust-lang.org/cargo/guide/creating-a-new-project.html)
- [Axum documentation](https://docs.rs/axum/latest/axum/)
- [SQLx CLI migrations and prepare](https://github.com/transact-rs/sqlx/blob/main/sqlx-cli/README.md)

## Tools

### HTTP server: Axum + Tokio + tower-http

Typed extractors/state and Tower middleware compose with Tokio networking.

Limits and integration: Configure limits, timeout/error mapping and graceful shutdown. Blocking work must not monopolize async workers.


- https://docs.rs/axum/latest/axum/
- https://tokio.rs/

Alternatives: Direct Hyper only for transport-specific needs

### Database and migrations: PostgreSQL + SQLx; sqlx-cli migrations

SQL-oriented async access with optional checked query macros and migration tooling.

Limits and integration: Select runtime/TLS/database features for the resolved release. Checked macros need a database or maintained offline metadata; runtime queries are not compile-time checked.


- https://docs.rs/sqlx/latest/sqlx/
- https://github.com/transact-rs/sqlx/blob/main/sqlx-cli/README.md

### Configuration: Serde-backed settings + config

Typed settings plus structured events/spans.

Limits and integration: Set precedence explicitly; validate semantics; install a tracing subscriber; never log secrets.


- https://docs.rs/config/latest/config/
- https://doc.rust-lang.org/std/env/fn.var.html
- https://docs.rs/tracing/latest/tracing/

Alternatives: std::env for a small fixed settings set

### Application logging: tracing + configured subscriber

Typed settings plus structured events/spans.

Limits and integration: Set precedence explicitly; validate semantics; install a tracing subscriber; never log secrets.


- https://docs.rs/config/latest/config/
- https://doc.rust-lang.org/std/env/fn.var.html
- https://docs.rs/tracing/latest/tracing/

### Tests and static checks: cargo test; rustfmt; Clippy; cargo audit

Compiler, style, behavior and known-advisory checks complement each other.

Limits and integration: Audit coverage is advisory-driven; compile success does not establish behavior or security. Test supported feature combinations rather than blindly enabling incompatible features.


- https://doc.rust-lang.org/cargo/commands/cargo-test.html
- https://github.com/rust-lang/rustfmt
- https://doc.rust-lang.org/clippy/usage.html
- https://rustsec.org/
- https://docs.rs/assert_cmd/latest/assert_cmd/

### Durable work: None for request-only service; Restate Rust SDK when durable workflows are required

Durable handlers and persisted workflow progress address work outliving a process.

Limits and integration: Requires a Restate service and adoption test. Journal external operations correctly; idempotency and business transactions remain explicit. Tokio tasks alone are not durable.


- https://docs.rs/restate-sdk/latest/restate_sdk/

### Deployment: cargo build --release --locked in a target-specific build pipeline

Reproducible dependency resolution from committed lockfile; native executable artifact.

Limits and integration: Not universally static: verify libc, TLS/native libraries, target support, certificates and container runtime needs.


- https://doc.rust-lang.org/cargo/commands/cargo-build.html

Alternatives: Container with explicit runtime libraries

### API token verification: jsonwebtoken + selected identity provider contract

Typed claims and signature checks fit JWT-bearing service APIs

Limits and integration: Configure accepted algorithms, issuer/audience, expiry and trusted key rotation; select required crypto features for resolved release. This is a verifier, not an OIDC login/session solution; opaque tokens need provider introspection.


- https://docs.rs/jsonwebtoken/latest/jsonwebtoken/

Alternatives: Preserve an existing compatible project choice

### Transactional email: lettre + project-selected SMTP provider

Typed mail construction and SMTP transport support application messages

Limits and integration: Configure TLS, sender credentials and timeouts; send required mail through durable jobs with duplicate protection. Validate chosen async/runtime features in Rust; delivery receipts and bounces need provider handling.


- https://docs.rs/lettre/latest/lettre/

Alternatives: Preserve an existing compatible project choice

### Uploads and object storage: AWS SDK for Rust S3 client

Durable object storage avoids dependence on service-local disk

Limits and integration: Configure runtime credentials, region and least-privilege bucket access; authorize object keys and uploads, bound size/concurrency and define retention. Test multipart cleanup and selected provider compatibility.


- https://docs.aws.amazon.com/sdk-for-rust/latest/dg/rust_s3_code_examples.html

Alternatives: Preserve an existing compatible project choice

### Realtime transport: Axum WebSocket extractor

WebSocket support fits bidirectional connected clients

Limits and integration: Enable the documented module/feature; authorize handshake and every protected message, bound queues/message size and implement heartbeat/shutdown. Socket delivery is not durable history; define reconnect/resync.


- https://docs.rs/axum/latest/axum/extract/ws/index.html

Alternatives: Server-sent events for one-way feeds; Polling for infrequent updates

## Architecture and developer workflow

Recommendation: Axum/Tower owns request extraction and middleware; domain functions return explicit errors; Tokio drives async I/O; SQLx pools and transactions own database access. Track child tasks and cancellation separately from persisted jobs. A Tokio channel coordinates tasks inside one live process and cannot recover accepted work after a crash.

Version scope: Reviewed docs expose Axum 0.8.9, Tokio 1.53.2 and SQLx 0.9.0 on 11 October 2026; Rust std docs show 1.99.0. These are documentation scopes, not a qualified composition or an automatic upgrade recommendation. Record rust-toolchain.toml, Cargo.lock, enabled features, SQLx CLI compatibility and database version before implementation.
Reviewed: 2026-10-11 | Evidence: documentation-reviewed | Source record: inputs/research/migrations-systems.json

### Architecture boundaries

- Recommendation: route through Axum extractors and typed State with cloneable pool/client handles. Keep domain logic independent of HTTP responses, and map business/infrastructure errors deliberately through IntoResponse.
- Recommendation: compose Tower limits and timeouts with explicit overload/error mapping. Use bounded channels/semaphores; a concurrency limit without an admission/queue policy does not bound every waiting request.
- Recommendation: use SQLx query macros where schema checking fits and dynamic queries where needed. Store reviewed migrations and offline metadata; runtime authorization and isolation remain separate from compile-time type checks.
- Recommendation: move sustained CPU work to a bounded blocking executor or dedicated worker process. Track async tasks with cancellation/termination coordination; a started spawn_blocking task cannot be forcibly aborted through Tokio.

### Tools and feedback

- Recommendation: inspect Cargo.toml/Cargo.lock, rust-toolchain.toml and enabled dependency features. For a new project, cargo new service and cargo add axum can establish the package; select Tokio runtime and SQLx database/TLS features deliberately rather than copying a broad feature list.
- Recommendation: run cargo fmt --check, cargo clippy --all-targets -- -D warnings and cargo test --locked with the project-supported feature matrix. Compile and run protocol/cancellation fixtures; no integration was executed in this research.
- Recommendation: install a SQLx CLI version compatible with the selected crate; against a disposable database run cargo sqlx migrate run, then cargo sqlx prepare --workspace and commit .sqlx metadata. CI cargo sqlx prepare --check --workspace detects stale metadata; an offline build does not prove the live schema matches.
- Recommendation: cargo build --release --locked prepares a release for the selected target. Use tracing/request IDs, pool-wait metrics and representative load profiles before asserting latency, cost or capacity advantages.

### Translations to avoid

- Avoid Arc<Mutex<Connection>> for all queries; a shared pool permits independent requests without a global database serialization boundary.
- Avoid blocking SDK calls or heavy loops on async runtime workers. spawn_blocking needs its own capacity limits and cannot abort a running closure.
- Avoid using Tokio mpsc as a drop-in replacement for durable Redis jobs; accepted jobs disappear with memory unless independently persisted.
- Avoid confusing Rust memory safety with correct authorization, queue delivery or compatibility guarantees.

### Architecture sources

- [Axum 0.8.9](https://docs.rs/axum/latest/axum/): Typed extractors/State and Tower middleware form the HTTP composition.
- [Tower limits](https://docs.rs/tower/latest/tower/limit/index.html): Concurrency and rate-limit middleware exist; admission/error policy needs application design.
- [Tokio graceful shutdown](https://tokio.rs/tokio/topics/shutdown): CancellationToken and TaskTracker coordinate shutdown and task completion.
- [Tokio channels](https://tokio.rs/tokio/tutorial/channels): Bounded mpsc coordinates tasks; capacity/backpressure is explicit, not disk persistence.
- [Tokio spawn_blocking](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html): CPU work needs a parallelism limit; started blocking tasks cannot be aborted.
- [SQLx 0.9.0 query macro](https://docs.rs/sqlx/latest/sqlx/macro.query.html): Literal queries need a matching database schema or offline metadata; engine binding and nullability have limits.
- [SQLx pool](https://docs.rs/sqlx/latest/sqlx/struct.Pool.html): A shared async pool supports reuse; a mutex around one connection creates serialization; close should be awaited.
- [SQLx CLI README](https://github.com/transact-rs/sqlx/blob/main/sqlx-cli/README.md): Migrations and prepare/prepare --check maintain offline query metadata.
- [Tokio broadcast](https://docs.rs/tokio/latest/tokio/sync/broadcast/index.html): A bounded local channel drops older values and reports lagging receivers.
- [River cross-language schema statement](https://riverqueue.com/docs/ruby): Current Ruby guide explicitly names Go, Rust and TypeScript sharing a schema; Rust API itself is unqualified here.
- [Redis Pub/Sub](https://redis.io/docs/latest/develop/pubsub/): Ephemeral shared fan-out remains at-most-once and needs a separate recovery path.

## Transition options

Proposed designs and checks; these are not executed compatibility results.

### Data and schema

**Inspect the source:** Capture the old SQL schema, transactions, tenant filters, nullable values and database engine behavior.

**During coexistence:** Recommendation: keep existing schema ownership and backward-compatible columns; run SQLx reads for a selected boundary before transferring its writer. Generate metadata against exactly the reviewed migration state.

**Target design:** Recommendation: SQLx pooled access with transaction-scoped domain changes; query! checks literals against a live build schema or checked-in .sqlx metadata. Keep database engine choice independent of the Rust rewrite.

**Rollback:** Recommendation: route writes back while retaining additive schema and a previous compatible binary. Delay destructive migrations; reconcile new-only persisted values before rollback.

**Benefits and prerequisites**

- Compile-time query/type checks can expose SQL/API mismatches before deployment. Requires: Query macros/features and metadata match the chosen engine and schema; nullable results and dynamic queries receive runtime checks. Tradeoffs: Dynamic SQL is outside macro checking; stale offline metadata can compile; schema ownership and deployment order still need controls.

**Checks before transfer**

- Run an offline locked build with the reviewed metadata and a live prepare --check against the migrated fixture DB.
- Verify both runtimes read each other's writes, including null/time/ID mappings.
- Cancel during a transaction and confirm the intended committed/rolled-back state plus pool recovery.

- https://docs.rs/sqlx/latest/sqlx/macro.query.html
- https://docs.rs/sqlx/latest/sqlx/struct.Pool.html
- https://github.com/transact-rs/sqlx/blob/main/sqlx-cli/README.md

### Jobs and schedules

**Inspect the source:** Preserve old broker serialization, acknowledgement, delayed/retry states, concurrency and effect IDs. Durable Redis workers cannot be replaced transparently by tokio::spawn.

**During coexistence:** Recommendation: Rust commits an outbox intent in its domain transaction; a replay-safe relay submits to the retained queue/worker interface. Existing workers retain queue ownership while new job kinds are qualified. This outbox design is inferred, not a shipped Axum feature.

**Target design:** Recommendation: keep proven durable workers until a chosen Rust queue implementation is qualified for retries, scheduling, leases and crashes. River current Ruby docs describe a shared schema with Rust; that statement alone does not qualify a Rust worker API or migration.

**Rollback:** Recommendation: stop the new producer, let accepted outbox entries settle and retain the old worker. Roll back traffic only after ambiguous effects are reconciled; avoid consuming a queue with incompatible handlers.

**Benefits and prerequisites**

- A retained worker boundary allows the HTTP layer to change without dropping backlog or broker guarantees. Requires: Same-transaction outbox intent; stable relay/effect IDs; explicit payload translator; observed delivery and backlog ownership. Tradeoffs: Two runtimes and a relay add operations; delivery may repeat; a SQLx transaction alone does not atomically submit to Redis.

**Checks before transfer**

- Crash after the domain commit but before relay delivery; an intent remains recoverable.
- Crash the relay after submission before marking sent; duplicate delivery produces one logical effect.
- Reconcile ready, scheduled, retry, failed and in-flight old jobs before any worker replacement.

- https://tokio.rs/tokio/tutorial/channels
- https://docs.rs/sqlx/latest/sqlx/macro.query.html
- https://riverqueue.com/docs/ruby

### Delivery and recovery

**Inspect the source:** Define HTTP admission/error behavior, task ownership, shutdown deadline and behavior for unavoidable CPU/blocking operations.

**During coexistence:** Recommendation: retain old routing while introducing Tower admission bounds and CancellationToken/TaskTracker-based ownership for a coherent endpoint cohort. Benchmark equivalent resource limits and durability before attributing gains to Rust.

**Target design:** Recommendation: bounded async work, cooperative cancellation, explicit shutdown notification plus tracked task completion, and SQLx pool close. For untrusted/hard-deadline native work, isolate it in a process whose termination contract is tested.

**Rollback:** Recommendation: return the cohort to the previous service and reconcile persisted outcomes. Do not simply retry every cancelled request; its external effect may already have occurred.

**Benefits and prerequisites**

- Tracked tasks and explicit admission limits make resource use and planned termination easier to reason about. Requires: Every child task is tracked; limits include waiting work; cancellation-safe I/O and shutdown budget are verified. Tradeoffs: spawn_blocking closures may continue after timeout; killing a process still requires durable recovery and external-effect reconciliation.

**Checks before transfer**

- Cancel an overloaded request and verify queue permits/resources are released.
- Send termination during async and blocking work; document tasks that drain and work that cannot be aborted.
- Force a crash after acceptance; verify recovery of persisted intents and honest failure of memory-only work.

- https://docs.rs/tower/latest/tower/limit/index.html
- https://tokio.rs/tokio/topics/shutdown
- https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html
- https://docs.rs/sqlx/latest/sqlx/struct.Pool.html

### Realtime transport

**Inspect the source:** Preserve subscriptions, authorization revocation, event versions, reconnect behavior and cross-instance fan-out.

**During coexistence:** Recommendation: keep the existing shared broker while a Rust gateway serves entire room/tenant cohorts; adapters translate existing messages without dual-emitting user effects. Test cross-runtime publication in both directions.

**Target design:** Recommendation: Axum WebSocket transport and bounded per-client queues. Tokio broadcast is appropriate only for local ephemeral fan-out with explicit Lagged handling; use durable state/event history to resync clients when loss is unacceptable.

**Rollback:** Recommendation: route the whole cohort back and retain the shared broker/protocol. Resynchronize from authoritative durable records; local channel state cannot be restored from a previous binary.

**Benefits and prerequisites**

- Local bounded fan-out can prevent slow receivers from retaining unbounded memory. Requires: Overflow/disconnect/resync policy exists; replica routing and shared fan-out remain covered; every broadcast error is handled. Tradeoffs: Tokio broadcast is process-local; old messages are evicted when capacity is exceeded; it is not a durable cross-node broker.

**Checks before transfer**

- Force receiver lag and verify Lagged triggers resync or the documented disconnect policy.
- Publish from each runtime and confirm the opposite runtime's subscribers receive the intended event.
- Reconnect after deployment/crash and rebuild state without trusting missing ephemeral frames.

- https://docs.rs/axum/latest/axum/
- https://docs.rs/tokio/latest/tokio/sync/broadcast/index.html
- https://redis.io/docs/latest/develop/pubsub/

Rewrite workflow: /rewrite/guide.md
Shared contracts and phases: /rewrite/contracts.json


## Setup
1. Complete the selected starting point and baseline checks in the Generators section first; then continue with the integration steps appropriate to the chosen component.
2. After the selected Cargo baseline, add compatible Axum and Tokio dependencies; the documented examples are cargo add axum and cargo add tokio --features macros,rt-multi-thread. Select required tower-http middleware explicitly.
3. Add SQLx with PostgreSQL, Tokio and the selected release's supported TLS configuration; install a compatible sqlx-cli release. Implement settings validation and a tracing subscriber.
4. Follow the selected SQLx migration instructions with DATABASE_URL pointing only to a disposable database. Write and review migration SQL before applying it; keep credentials outside tracked files.
5. For checked query macros, regenerate and commit .sqlx offline metadata after schema/query changes. Implement HTTP, real-database and cancellation tests, then run the profile verification checks with relevant features and targets.
6. Introduce Restate only after a separate restart/retry/idempotency proof. Pin the toolchain and release targets, preserve the application Cargo.lock after dependency resolution and qualify target/runtime/TLS dependencies. These application instructions were not executed.

## Verification
Commands below require the selected tools and project configuration. Replace example paths, schemes and IDs; distinguish tests from builds and interactive startup. These are instructions, not recorded passes.

```text
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --locked -- -D warnings
cargo test --workspace --locked
cargo audit
sqlx migrate info
cargo sqlx prepare --check
cargo build --release --locked
```

## Open questions
- Which API/token contract and trusted key-rotation mechanism apply?
- Which target/runtime/TLS and database configurations must ship?
- Does durable work justify a separate Restate service and its operation?
- Which workload, realtime capacity and restore objectives must be met?

## Sources
- [Axum](https://docs.rs/axum/latest/axum/)
- [Tokio](https://tokio.rs/)
- [SQLx](https://docs.rs/sqlx/latest/sqlx/)
- [SQLx CLI](https://github.com/transact-rs/sqlx/blob/main/sqlx-cli/README.md)
- [Rust config crate](https://docs.rs/config/latest/config/)
- [Rust environment variables](https://doc.rust-lang.org/std/env/fn.var.html)
- [Rust tracing](https://docs.rs/tracing/latest/tracing/)
- [Cargo test](https://doc.rust-lang.org/cargo/commands/cargo-test.html)
- [rustfmt](https://github.com/rust-lang/rustfmt)
- [Clippy usage](https://doc.rust-lang.org/clippy/usage.html)
- [RustSec](https://rustsec.org/)
- [assert_cmd](https://docs.rs/assert_cmd/latest/assert_cmd/)
- [Restate Rust SDK](https://docs.rs/restate-sdk/latest/restate_sdk/)
- [Cargo build](https://doc.rust-lang.org/cargo/commands/cargo-build.html)
- [jsonwebtoken API](https://docs.rs/jsonwebtoken/latest/jsonwebtoken/)
- [lettre documentation](https://docs.rs/lettre/latest/lettre/)
- [AWS Rust S3 examples](https://docs.aws.amazon.com/sdk-for-rust/latest/dg/rust_s3_code_examples.html)
- [Axum WebSocket extractor documentation](https://docs.rs/axum/latest/axum/extract/ws/index.html)

Keep the project README current and link the selected guidance; preserve existing project instructions.
