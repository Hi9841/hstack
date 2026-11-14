# Rewrite an existing application

These are proposed engineering plans supported by documentation. No source/target pair, application integration, migration or performance claim has been qualified by execution.

Reviewed: 2026-10-11

## Required application inventory

Source and target runtime/library versions; dependency purpose and contracts; replaced boundary; coexistence requirement; each data/job/scheduler owner; routing cohort; backward compatibility and rollback window; actual qualification results.

The website composes researched guidance. Free-text inventory remains unresolved until the actual application is inspected. A shared capability name does not prove tools or protocols are interchangeable. Compare documented application roles before planning replacement: language overlap is insufficient. If the selected target does not cover the source roles, establish the replaced component boundary and how a retained interface or separate composition preserves them, or record an explicitly intended change to the product surface. An explicit component documented by the source can narrow that scope. Resolve target component, web UI, static-hosting and browser offline constraints without silently changing the selected target.

## Choose the kind of change

### Compatible replacement

Preserve the declared external behavior and operated dependencies. Any changed guarantee is a separate decision.

### Staged transition

Move a bounded responsibility while old and new systems coexist. Each data writer, job type and schedule has one declared execution owner.

### Target architecture

Evaluate the target stack's idioms and different dependencies. Qualify changed guarantees and recovery before retiring the old system.

## Steps and acceptance gates

### Inventory and choose the boundary

- Inspect runtime pins, manifests, lockfiles and actual infrastructure uses.
- Choose an endpoint, tenant, job type, command or client release cohort; name every writer, consumer and scheduler owner.

Gate: Versioned contract fixtures, side-effect inventory, baseline workload and explicit unknowns are recorded.

Rollback: Existing implementation remains authoritative.

### Build behind retained contracts

- Implement target-stack boundaries without copying source-framework internals.
- Keep old workers or services where compatibility is required; qualify adapters before sharing payloads.
- Use a shared transaction for data plus queue insertion when possible, or a durable outbox with replay-safe consumers across stores.

Gate: Old/new reads, writes, identity and selected capability fixtures pass; changes to guarantees are documented.

Rollback: Retain old artifacts and backward-readable schemas.

### Qualify behavior and recovery

- Compare outcomes with isolated effects; never duplicate live emails or payments in shadow traffic.
- Exercise crashes, retries, network interruption, load limits and restore.
- Set business, latency, error, queue-age and resource thresholds before cohort promotion.

Gate: Executed checks name exact versions, environment, expected/actual result and failures; documentation review alone does not pass.

Rollback: Run the recovery and owner-transfer procedure in a representative environment.

### Route a bounded cohort

- Use stable cohorts spanning sessions, writes, subscriptions and reconnects.
- Transfer job and scheduler ownership explicitly rather than letting both execute.
- Monitor business outcomes and reconcile data/backlog during each increase.

Gate: Measured outcomes meet the application's declared thresholds and rollback remains viable.

Rollback: Reverse routing only while contracts remain backward-readable; reconcile in-flight effects.

### Transfer ownership and reconcile

- Move remaining producers, consumers and schedules in an explicit order.
- Account for ready, scheduled, retry, failed and in-flight work.
- Keep old workers, objects, assets and client contracts through the rollback window.

Gate: Every responsibility has a single named owner and reconciliation finds no unaccounted work.

Rollback: Preserve the old execution path until the recorded window closes; irreversible effects need compensation or reconciliation.

### Evaluate the target and retire dependencies

- Adopt local caching, another queue engine or different UI protocols as separately qualified changes.
- Retire an operated service only after every consumer and recovery requirement is accounted for.
- Measure the target architecture separately from coexistence and preserve the evidence.

Gate: Claims of fewer services, lower cost or better performance have their prerequisites and actual measurement; a 100% traffic shift is insufficient.

Rollback: Use the preserved service/artifact while viable; after irreversible contraction, follow the documented restore or forward-repair plan.

## Capability contracts

### Data and schema

Inventory: Actual database, schema versions, migration owner, IDs, null/default semantics, time zones, transactions and backup/restore.

Gate: Keep one schema migration owner and explicitly partition authoritative writers. Use additive schema changes while both versions run; validate old reads against new writes and the reverse. Reconcile rows before destructive contraction.

Rollback: Keep backward-readable data during the rollback window. Reversing traffic cannot undo a destructive migration or external effect.

### Jobs and schedules

Inventory: Actual adapter/broker, payload version, serialization, producer/consumer, retry policy, scheduled/failed/in-flight backlog and scheduler owner.

Gate: Route each job type to one execution owner. Prove crash recovery and idempotent business effects, including a crash after the effect but before acknowledgement. Same broker access does not prove payload compatibility.

Rollback: Stop new producers before returning ownership; reconcile every backlog state and preserve old consumers until the rollback window ends.

### Caching and shared state

Inventory: Every use of Redis or another store: disposable cache, sessions, locks, counters, broker or rate limits. Record keys, namespace, codec, TTL and invalidation.

Gate: Qualify shared formats or deliberately isolate namespaces. A local cache must tolerate loss and staleness; it cannot silently replace shared sessions, locks or global counters.

Rollback: Retain the previous shared service until all uses are replaced and reconciled. Invalidate incompatible entries and maintain an explicit routing strategy.

### Identity and authorization

Inventory: Session/cookie format, signing/encryption, expiry, revocation, issuer/audience, CSRF, role and tenant/resource permissions.

Gate: Test old login/new request, new login/old request, logout, expiry, denied access and tenant isolation. Connecting to the same identity provider does not recreate authorization.

Rollback: Keep old token/session verification while required. New-only credential or policy formats need a deliberate reauthentication or conversion strategy.

### Realtime transport

Inventory: Wire protocol, channel names, subscription authorization, ordering, reconnect/replay, cross-node fanout and deployment proxy behavior.

Gate: Keep stable cohorts including sockets and reconnects. Verify delivery old-to-new and new-to-old. PubSub inside one ecosystem is not an adapter for another client's protocol.

Rollback: Keep the bridge and old endpoint until connections are drained and clients can reconnect; account for missed events and changed offsets.

### Files and objects

Inventory: Object key and metadata schema, stored-file references, signed URLs, access policies, upload limits and lifecycle/retention owners.

Gate: Exercise old upload/new read and the reverse, expiry, rejected access and partial upload cleanup. Sharing a bucket does not translate framework-specific database records.

Rollback: Preserve old readable references and object retention until reconciliation. Do not delete objects while old clients or jobs can still reference them.

### Email and external effects

Inventory: Provider, template IDs, delivery identity, deduplication keys, retries, webhooks and bounced/failed-message handling.

Gate: Use sandbox recipients for comparison and one live execution owner. A local sent flag cannot close the crash window after provider acceptance; reconcile using stable effect IDs where supported.

Rollback: Stop new sends before switching owner and reconcile accepted requests. Traffic rollback cannot unsend an email or reverse a payment.

### Search indexes

Inventory: Source of truth, document IDs, analysis/mapping version, update/delete feeds, access filters and rebuild checkpoint.

Gate: Build a new versioned index from authoritative data; replay mutations and deletions, reconcile results and permissions, then switch readers. Keep only one indexing owner per feed.

Rollback: Keep the old index and update feed during the rollback window; reconcile lag before switching back.

### Delivery and recovery

Inventory: Process/service inventory, runtime/library versions, licensing, deployment ownership, health/readiness, logs, metrics, recovery objectives and rollback window.

Gate: Exercise graceful shutdown and forced termination separately. Compare matched behavior, durable storage, load and tuning budgets; report latency, errors, resource use and queue delay rather than a universal language score.

Rollback: Keep a runnable previous artifact, backward-readable contracts and tested recovery. Define application-specific promotion thresholds before rollout.

### CLI and pipe contracts

Inventory: Command/flag names, stdin/stdout/stderr, JSON/text formats, exit codes, paths, config versions and supported OS/architecture packages.

Gate: Run captured scripts against both binaries; compare output/exit behavior, cancellation and interrupted writes. A faster binary is not a compatible replacement if downstream parsers break.

Rollback: Retain the previous binary and a configuration backup. New persistent formats require backward readability or an explicit conversion.

### Browser and installed clients

Inventory: Supported client/build versions, API schemas, local storage versions, offline writes, release cohorts, adoption and asset retention.

Gate: Test the oldest supported client against the new backend and fresh clients against retained APIs. Keep assets/endpoints while installed or open clients still use them; exercise offline conflicts and local data upgrades.

Rollback: A server rollback does not remove an installed application update. Preserve API compatibility and use a forward repair for irreversible local data migrations.

## Research by stack

- [Astro content site](/stacks/astro-content/guide.md) | /rewrite/profiles/astro-content.json
- [Phoenix + LiveView](/stacks/elixir-phoenix-liveview/guide.md) | /rewrite/profiles/elixir-phoenix-liveview.json
- [Next.js](/stacks/typescript-next-node/guide.md) | /rewrite/profiles/typescript-next-node.json
- [React + Vite](/stacks/typescript-react-vite-browser/guide.md) | /rewrite/profiles/typescript-react-vite-browser.json
- [Rails + Hotwire](/stacks/rails-hotwire-postgresql/guide.md) | /rewrite/profiles/rails-hotwire-postgresql.json
- [Laravel + Livewire](/stacks/laravel-livewire-postgresql/guide.md) | /rewrite/profiles/laravel-livewire-postgresql.json
- [Django](/stacks/python-django/guide.md) | /rewrite/profiles/python-django.json
- [Go service](/stacks/go-service/guide.md) | /rewrite/profiles/go-service.json
- [Rust service](/stacks/rust-service/guide.md) | /rewrite/profiles/rust-service.json
- [FastAPI](/stacks/python-fastapi/guide.md) | /rewrite/profiles/python-fastapi.json
- [Go CLI + TUI](/stacks/go-cli/guide.md) | /rewrite/profiles/go-cli.json
- [Rust CLI + TUI](/stacks/rust-cli/guide.md) | /rewrite/profiles/rust-cli.json
- [Python automation + AI](/stacks/python-scripts-workers/guide.md) | /rewrite/profiles/python-scripts-workers.json
- [Swift + SwiftUI](/stacks/swift-swiftui-ios/guide.md) | /rewrite/profiles/swift-swiftui-ios.json
- [Kotlin + Compose](/stacks/kotlin-compose-android/guide.md) | /rewrite/profiles/kotlin-compose-android.json
- [Expo + React Native](/stacks/expo-react-native/guide.md) | /rewrite/profiles/expo-react-native.json

## Specific boundaries

### Rails to Phoenix: three job paths

Recommendation: first inspect the actual Active Job adapter; Rails does not imply Redis. Keep Ruby workers behind an explicit submission interface, qualify a Redis-compatible Elixir consumer against exact wrappers and retries, or route selected job types to Oban while retaining legacy workers. Exq is a compatibility candidate, not proof that arbitrary Active Job jobs can execute unchanged. Oban ships SQL persistence engines, not Redis persistence. Running SQL beside Redis is feasible but adds operations; atomic domain write and enqueue requires the same transaction, otherwise use an outbox. Rails cache codecs and Action Cable frames need explicit bridges. ETS suits reconstructible node-local cache only; Redis may remain the right permanent dependency.

- https://guides.rubyonrails.org/active_job_basics.html
- https://guides.rubyonrails.org/caching_with_rails.html
- https://oban.hexdocs.pm/installation.html
- https://oban.hexdocs.pm/Oban.html
- https://exq.hexdocs.pm/readme.html
- https://github.com/sidekiq/sidekiq/wiki/Job-Format
- https://www.erlang.org/docs/27/apps/stdlib/ets.html

### Full-stack React to a browser client

Recommendation: separate the frontend from server responsibilities before moving UI routes. A Vite bundle does not replace server rendering, server functions, database access or private secrets. Retain an API/backend and define identity, CORS/CSRF, cache invalidation and asset-version contracts. Qualify any changed rendering, routing or offline behavior with open old browser sessions.

- https://nextjs.org/docs/app/getting-started/server-and-client-components
- https://vite.dev/guide/backend-integration.html

### Django to FastAPI: move an API boundary

Recommendation: retain Django as schema and identity owner while moving an explicit API component. Sharing PostgreSQL or Python does not preserve Django sessions, ORM migrations, middleware, permissions or Celery payload contracts. Keep one migration owner and isolate workers; moving to async handlers does not turn blocking database or SDK calls into nonblocking work.

- https://docs.djangoproject.com/en/6.0/topics/async/
- https://fastapi.tiangolo.com/async/
- https://fastapi.tiangolo.com/tutorial/background-tasks/

## Evidence to record

For each application check: purpose, selected tools/versions, prerequisites, environment, scenario/command, expected result, actual result and receipt. Documentation review, site build, application integration, verified coexistence and measured performance are distinct states. Unknown coverage must be researched, not marked satisfied.

## Sources

- [Incremental replacement with a facade](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig): Routing boundaries and incremental coexistence; per-application design still requires qualification.
- [Transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html): Cross-store delivery recommendation; committed outbox plus relay, duplicates and ordering require explicit handling.
- [Sidekiq job format](https://github.com/sidekiq/sidekiq/wiki/Job-Format): Payload serialization is a compatibility contract, not just a broker connection.
- [Sidekiq retries and idempotency](https://github.com/sidekiq/sidekiq/wiki/Best-Practices): Retryable jobs need replay-safe effects; no exactly-once execution assumption.


## Additional rewrite sources

Source coverage is separate from new-project target recommendations. Inspect installed versions and actual application responsibilities.

- [Create React App](/rewrite/sources/create-react-app.md)
- [AngularJS (1.x)](/rewrite/sources/angularjs.md)
- [Vue 2](/rewrite/sources/vue-2.md)
- [WordPress](/rewrite/sources/wordpress.md)
- [WooCommerce](/rewrite/sources/woocommerce.md)

[Source index](/rewrite/sources.json)
