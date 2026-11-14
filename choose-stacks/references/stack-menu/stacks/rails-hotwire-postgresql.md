# Rails + Hotwire

Database-backed products with HTML, accounts and jobs close together.

Language: Ruby | Reviewed: 2026-10-10 | Evidence: documentation-reviewed research input

Source record: menu/inputs/research/rails-laravel.json.

Core guidance checked: 2026-10-13. Review sources are listed below. /research-freshness.json describes the imported research packet; this record retains its own evidence scope. These recipes and selected dependency combinations need qualification in the actual project.

## Application role
Components: web, api
UI: server
Deployment: server

## Use cases
- SaaS
- Business CRUD
- Collaboration and workflow products

## Fit
- An integrated monolith and server-owned UI fit the product.
- A small team benefits from stable conventions and limited integration work.

## Choose something else when
- The core is an offline-first canvas or requires extensive browser-owned state.
- Hard CPU/latency constraints justify a specialist service.

## Agent workflow
- Read README, dependency manifests, lockfiles, runtime pins and the maintained project workflow before changing anything. Preserve an existing stack unless reconsidering it is part of the request.
- For a new component, read the Generators section before writing application files. Use its appropriate official initializer and retain its generated baseline; follow-up generators are conditional on the selected feature.
- Use this guide to select tools by requirement. Resolve compatible versions from official and installed-version documentation; record the actual lockfile and runtime versions.
- Create a plan for schema changes, identity, authorization, external effects and deployment. A library choice does not complete its integration.
- Run relevant checks after configuration. Exercise the real interface, failure paths and packaged artifact on the intended target. Report commands, versions, results and untested behavior.
- On failure, retain the command and diagnostic, fix the failing prerequisite and resume there. Do not regenerate over existing work or suppress failures to make a check green.

## Best practices
- Keep Turbo and Stimulus focused on interface behavior; put authorization in explicit policies.
- Run migrations and exercise the generated authentication flow before building product features around it.
- Treat Solid Queue workers as operated processes. Make retries safe and verify recovery after interruption.
- Use system tests for the critical browser journey and rehearse backups and restore before shipping.

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

#### rails new PostgreSQL application

Use when: A new server-rendered Rails application with the normal Hotwire stack.

1. Install/select a supported Ruby and Rails version, Bundler, PostgreSQL and the native prerequisites for the pg gem; record versions.
2. Inspect rails new help. Generate the full application with PostgreSQL; keep Hotwire and test/security defaults unless the actual brief requires an exception.
3. Configure development/test credentials through environment or ignored configuration, then prepare the intended development database.

Working directory: A local source-workspace parent outside synchronized storage; my-app must not already exist

Inspect the installed application generator.

```sh
rails new --help
```

Working directory: A local source-workspace parent outside synchronized storage; my-app must not already exist

Create the conventional Rails application and PostgreSQL configuration.

```sh
rails new my_app --database=postgresql
```

Working directory: The generated my_app directory, after database configuration

Prepare the intended local database and schema.

```sh
bin/rails db:prepare
```

- Replace my_app with the intended unused Rails name. The normal generator initializes Git without committing; review any custom application templates for extra effects.
- Do not add --skip-git just to avoid a commit: it also skips generated .gitignore/.gitattributes. Rails defaults already include Turbo/Stimulus; do not install a separate SPA or skip Hotwire without a product reason.

#### Rails API-only application

Use when: Choose for a new API-first backend whose clients consume JSON; this is a distinct application mode from the normal Rails/Hotwire web application above.

1. Select a supported Rails/Ruby release and inspect the installed `rails new --help`; the current Rails 8.1 guide documents the --api mode.
2. Generate into a new absent directory with PostgreSQL and API mode, then inspect generated middleware, controller base class, resource generators, database setup and tests.
3. Before implementing endpoints, decide whether clients are server-side, native, or browser-based and select the matching authentication/session contract. API mode omits browser middleware such as cookies by default; add only the browser/session pieces required by the chosen contract.

Working directory: A local source-workspace parent outside synchronized storage; my_api must not already exist

Confirm the installed generator supports the selected database and API flags.

```sh
rails new --help
```

Working directory: A local source-workspace parent outside synchronized storage; my_api must not already exist

Generate a Rails API-only app with PostgreSQL configuration.

```sh
rails new my_api --api --database=postgresql
```

Working directory: The generated my_api directory after configuring the intended development database

Prepare the generated app's development database.

```sh
bin/rails db:prepare
```

- Rails 8.1 `--api` reduces middleware, makes ApplicationController inherit from ActionController::API, and configures resource generators to omit views/helpers/assets. This changes the web application shape; use the normal Hotwire app when server-rendered browser pages are primary.
- Do not install authentication, cookie/session middleware or CORS support by reflex. Select an identity provider/token or cookie-session design from actual client needs; cookie-authenticated browser requests need a deliberate CSRF contract. Configure narrowly scoped CORS only for cross-origin browser clients, and test allowed and rejected origins.
- If a follow-up resource scaffold is selected, its generated JSON CRUD is only a starting point, not a proven API contract. Define request/response schemas, status/error behavior, versioning and object-level authorization before exposing resources.

### Conditional follow-up generators

#### Authentication

Use when: A new application needs Rails built-in session authentication and has not already selected another identity solution.


Working directory: The generated my_app directory

Generate session authentication support using the installed Rails version.

```sh
bin/rails generate authentication
```

Working directory: The generated my_app directory, after reviewing the new migrations and database target

Apply the generated authentication migrations locally.

```sh
bin/rails db:migrate
```

- Inspect bin/rails generate authentication --help first. Implement signup, mail configuration and per-resource authorization deliberately; generated login is not a complete product identity policy.

#### Model or scaffold

Use when: A new domain resource is required; choose a model for custom workflows or scaffold when generated CRUD screens fit.


Working directory: The generated my_app directory

Generate an example model with migration and test/fixture support.

```sh
bin/rails generate model Product name:string
```

- Product and name:string are examples; replace them with the actual domain design. Review constraints and indexes before migrating.
- Alternative: bin/rails generate scaffold Product name:string generates CRUD layers as well; choose it instead of generating the same model twice. Inspect generator help or --pretend before writes.

#### Additive migration

Use when: An existing Product model/table needs the example description column.


Working directory: The generated my_app directory with an existing Product table

Generate a migration for an existing resource.

```sh
bin/rails generate migration AddDescriptionToProducts description:text
```

- Review the generated migration before bin/rails db:migrate; do not edit a migration already shared/applied to disguise a later schema change. Names/attributes are examples.

### Preserve the generated foundation

- Generated .gitignore/.gitattributes, binstubs, Gemfile.lock, database configuration, credential exclusions, test/fixture layout, Hotwire/import-map setup and generated security/CI checks.
- Do not replace generated Rails defaults with a small handwritten skeleton; record brief-driven omissions and additions.

### Baseline and generation checks

- Inspect bin/rails generate and the relevant generator --help for the installed version.
- Run database migration status, bin/rails zeitwerk:check, domain/system tests and generated security/style checks that are present. For browser UI flows, inspect a browser journey; API-only apps should verify HTTP contracts through request/integration tests instead.
- For API mode, test documented JSON request/response and error contracts, authentication and object authorization; when browser clients are used, verify CSRF/session behavior and both permitted and rejected CORS origins.
- Run the generated server and inspect a browser journey; authentication/authorization still require behavior tests.

### Generation receipt

- Component and selected starting point, or the documented absence of a full application generator
- Generator/toolchain versions, exact commands or IDE template/settings, working directory and generated destination
- Generated files retained, deliberate deviations with reasons, and required supplemental ignore rules
- Baseline checks and later checks actually run, results and remaining prerequisites or untested behavior

### Generator sources

- [Rails 8.1 API-only applications](https://guides.rubyonrails.org/v8.1/api_app.html)
- [Rails 8.1 command line and application generation](https://guides.rubyonrails.org/v8.1/command_line.html)
- [Rails command line and generators](https://guides.rubyonrails.org/command_line.html)
- [Rails getting started, authentication and Hotwire](https://guides.rubyonrails.org/getting_started.html)
- [Rails migrations](https://guides.rubyonrails.org/active_record_migrations.html)
- [Rails application generator source: Git and ignore-file behavior](https://raw.githubusercontent.com/rails/rails/main/railties/lib/rails/generators/rails/app/app_generator.rb)
- [Pundit installation and policy generator](https://github.com/varvet/pundit)

## Tools

### UI: ERB + Turbo + Stimulus

Server-rendered HTML and selective JavaScript limit duplicated UI state.

Limits and integration: Do not force Hotwire onto rich offline editors.


- https://hotwired.dev/

Alternatives: React client when browser-owned state dominates; retain Rails API

### Database and migrations: PostgreSQL + Active Record migrations

Relational constraints and conventional migrations fit business data.

Limits and integration: Use unique/foreign-key constraints; assess locks and use expand/contract changes for rolling deploys.


- https://guides.rubyonrails.org/active_record_migrations.html

Alternatives: SQLite for deliberately single-host deployments

### Authentication: Rails authentication generator

Generated local sessions plus explicit per-resource authorization.

Limits and integration: Generator is a starting point; signup, authorization and account lifecycle require product decisions.


- https://guides.rubyonrails.org/getting_started.html
- https://github.com/varvet/pundit
- https://github.com/heartcombo/devise

Alternatives: Devise when its additional authentication modules are needed

### Authorization: Pundit policy classes

Generated local sessions plus explicit per-resource authorization.

Limits and integration: Generator is a starting point; signup, authorization and account lifecycle require product decisions.


- https://guides.rubyonrails.org/getting_started.html
- https://github.com/varvet/pundit
- https://github.com/heartcombo/devise

Alternatives: Existing resource-level policy implementation; keep authentication separate

### Jobs: Active Job + Solid Queue

Database-backed jobs avoid a mandatory separate broker.

Limits and integration: Configure worker capacity, retry limits and idempotency; separate queue DB does not guarantee atomic app-write/enqueue.


- https://guides.rubyonrails.org/active_job_basics.html

Alternatives: Another Active Job backend only for measured operational needs

### Tests: Minitest + Rails integration/system tests

Exercise authorization, database constraints and essential browser flows.

Limits and integration: Browser tests need their driver/browser; unit tests alone miss UI and transaction races.


- https://guides.rubyonrails.org/testing.html

Alternatives: Keep RSpec in an established RSpec repository

### Lint and security: RuboCop + Brakeman + bundler-audit

Style, application scanning and dependency advisories cover different risks.

Limits and integration: Scans do not establish security; test tenant isolation and unsafe uploads. bundler-audit has GPL-3.0 licensing.


- https://guides.rubyonrails.org/getting_started.html
- https://guides.rubyonrails.org/security.html
- https://github.com/rubysec/bundler-audit

Alternatives: Preserve existing compatible project tooling

### Deployment: Kamal + generated Dockerfile + PostgreSQL backups

Portable container deployment with application-owned configuration.

Limits and integration: Requires registry/server credentials and persistent data strategy; backups and restore drills remain operator work.


- https://kamal-deploy.org/docs/installation/
- https://guides.rubyonrails.org/getting_started.html

Alternatives: Managed container hosting when server operations are undesirable

### Agent tooling: Generators + routes/schema/test feedback + version-matched Rails guides

Conventions make edits easier to locate and verify.

Limits and integration: Agent productivity is an inference; no cross-framework coding-success benchmark established.


- https://rubyonrails.org/ai

Alternatives: Add only a reviewed MCP integration with a concrete need

### Licensing and hosting: Rails MIT; self-hostable

No mandatory proprietary Rails hosting service.

Limits and integration: Dependency licenses remain separate; do not infer all gems are MIT.


- https://github.com/rails/rails/blob/main/MIT-LICENSE

Alternatives: Paid infrastructure/support when operationally useful

### Transactional email: Action Mailer

Framework mailers integrate templates and queued delivery

Limits and integration: Configure provider transport and sender; use deliver_later when delivery must be queued; test content and failure behavior. Provider acceptance is not inbox delivery.


- https://guides.rubyonrails.org/action_mailer_basics.html

Alternatives: Preserve an existing compatible project choice

### Uploads and object storage: Active Storage

Framework attachments support external storage and direct uploads

Limits and integration: Run the installed-version Active Storage generator/migrations; configure private storage, authorization, limits and cleanup. Public blob URLs and user-supplied files need an explicit access policy.


- https://guides.rubyonrails.org/active_storage_overview.html

Alternatives: Preserve an existing compatible project choice

### Realtime transport: Action Cable

Rails channels integrate WebSocket messages with application code

Limits and integration: Configure chosen cable adapter and connection/channel authorization; test reconnect, revoked membership and host proxy behavior. Broadcast is not durable event history.


- https://guides.rubyonrails.org/action_cable_overview.html

Alternatives: Preserve an existing compatible project choice

## Architecture and developer workflow

Rails supplies a conventional MVC application and Active Record persistence. Turbo Drive, Frames and Streams support a server-rendered HTML interface with incremental browser updates. Recommendation: keep domain writes on the server and introduce browser-owned state only for interactions that need it; a framework rewrite is not a prerequisite for fixing an inefficient query or incorrect queue contract.

Version scope: Rails guides showing Rails 8.1 examples; current Turbo handbook. These describe target capabilities, not the source application's installed versions. Detect Gemfile.lock, Ruby version and configured adapters before choosing a move.
Reviewed: 2026-10-11 | Evidence: documentation-reviewed | Source record: inputs/research/migrations-server.json

### Architecture boundaries

- Recommendation: establish one authoritative domain writer and one schema migration runner per shared database during coexistence. Route a stable tenant or feature boundary, and keep the old application able to read new writes until rollback expires.
- Active Job is the application interface; Solid Queue is the Rails 8 default backend. Inspect the application's actual adapter before inferring a Redis dependency. Separate workers, recurring task configuration and domain writes are distinct responsibilities.
- Recommendation: treat Turbo stream DOM targets, Action Cable channel identifiers, job serialization and session cookies as separate contracts. Sharing a datastore does not prove any of their compatibility.

### Tools and feedback

- In an existing checkout, read Gemfile.lock and environment configuration before adapting generators. In a disposable feature prototype, bin/rails generate model Product name:string and bin/rails db:migrate demonstrate the conventional model/migration path; review generated schema changes before applying them.
- bin/rails generate job guests_cleanup creates an Active Job class; configure its selected backend and worker process separately. Recipe only: use bin/jobs start for a configured Solid Queue application, then exercise enqueue, failure and recovery against its real queue database.
- bin/rails console is useful for inspecting application objects. Recommendation: capture authorized and unauthorized request fixtures, mixed-version writes and browser stream behavior as acceptance checks rather than treating successful boot as migration qualification.
- For a new local-account prototype, bin/rails generate authentication creates User and Session models plus login surfaces. Review account lifecycle and resource authorization separately; do not run it over an established authentication system without an intentional migration design.

### Translations to avoid

- Avoid calling a queue-adapter configuration change a backlog migration: the old backend retains work and Active Job can serialize GlobalID and custom types that need the original Ruby classes and database semantics.
- Avoid claiming atomic domain-write-and-enqueue from a separate Solid Queue database. After-commit enqueue prevents premature execution but is not a transaction across two stores. Recommendation: use a durable outbox when a crash between commit and delivery must be recoverable.
- Avoid the Action Cable async adapter for distributed production delivery; the guide restricts it to development/testing and a single process. Avoid replacing session or lock data with a disposable cache just because both use Redis.

### Architecture sources

- [Getting Started with Rails](https://guides.rubyonrails.org/getting_started.html): Rails 8.1 examples, MVC/Active Record, model and authentication generators, migration and console commands.
- [Active Record Migrations](https://guides.rubyonrails.org/active_record_migrations.html): Schema migration files, database constraints, reversal and rollback semantics.
- [Active Job Basics](https://guides.rubyonrails.org/active_job_basics.html): Active Job serialization, Solid Queue default and process roles, bin/jobs, separate database default, enqueue timing, recurring tasks and retry handling.
- [Securing Rails Applications](https://guides.rubyonrails.org/security.html): CookieStore, signing/encryption rotation, replay/fixation and session expiration considerations.
- [Action Cable Overview](https://guides.rubyonrails.org/action_cable_overview.html): Cable connections/channels, adapter configuration, async locality, Solid Cable, origins and server deployment.
- [Caching with Rails](https://guides.rubyonrails.org/caching_with_rails.html): Rails cache interfaces, SQL cache lifetime, Solid Cache and alternative stores.
- [Turbo introduction](https://turbo.hotwired.dev/handbook/introduction): Drive, Frames and Streams extend server-rendered HTML navigation and updates.
- [Turbo Streams](https://turbo.hotwired.dev/handbook/streams): DOM target operations and stream transport options.
- [Sidekiq Best Practices](https://github.com/sidekiq/sidekiq/wiki/Best-Practices): Jobs must be idempotent; execution is at least once rather than exactly once.

## Transition options

Proposed designs and checks; these are not executed compatibility results.

### Data and schema

**Inspect the source:** Inventory table names, primary keys, timestamps, enum values, constraints, callbacks and the application that currently owns migrations; Active Record migrations define schema evolution but do not describe all application side effects.

**During coexistence:** Recommendation: keep the existing writer authoritative while the target reads representative data. Add backward-readable fields first; transfer one domain boundary explicitly. Keep a single migration runner rather than allowing two framework migration histories to modify the same tables independently.

**Target design:** Rails Active Record over the selected PostgreSQL schema, with reviewed database constraints and migrations. Recommendation: remove legacy fields only after old code and rollback readers have retired.

**Rollback:** Recommendation: route writes back only while the old reader understands new records. Preserve additive schema changes; rehearse reversible migrations separately and reconcile irreversible data changes.

**Benefits and prerequisites**

- Recommendation: conventional migrations and model access can concentrate schema work in one maintained application. Requires: A named schema owner, compatible value semantics and staged writer transfer. Tradeoffs: Shared tables constrain both deployments; deleting or rewriting data may require reconciliation rather than migration reversal.

**Checks before transfer**

- Create in the old application and read in Rails, then reverse the direction after writer transfer; compare IDs, timestamps and nullable values.
- Run the proposed migration against a disposable copy; verify both deployed versions can still read and update a fixture, including unique and foreign-key failures.

- https://guides.rubyonrails.org/active_record_migrations.html
- https://guides.rubyonrails.org/getting_started.html

### Jobs and schedules

**Inspect the source:** Record adapter, job class, argument serializers/GlobalIDs, queue names, retries, scheduled work, failed work and running leases. Rails exposes these through Active Job while each backend supplies execution behavior.

**During coexistence:** Recommendation: retain old consumers for old payloads; route a new job category to a new queue/backend. Transfer its producers and recurring-task owner together. Drain or deliberately transform ready, scheduled, retry, failed and in-flight work; do not run both schedulers for the same business operation.

**Target design:** Active Job with configured Solid Queue or the retained qualified adapter. Same-database enqueue may join a domain transaction; a separate queue database needs an explicit delivery design. Recommendation: require business idempotency even when job uniqueness exists.

**Rollback:** Recommendation: stop new producers before restoring old routing; retain both consumers through the rollback window and reconcile completed external effects before re-enqueueing.

**Benefits and prerequisites**

- SQL-backed job persistence may allow retirement of a dedicated broker. Requires: All broker uses inventoried and retired; workers, queue schema, failure monitoring and backlog reconciliation in place. Tradeoffs: Database work and queue operations remain operational responsibilities; retaining Redis for another capability yields no service-count reduction.

**Checks before transfer**

- Replay captured old serializer fixtures using the retained consumer; a deleted GlobalID target must follow the intended failure policy.
- Rollback a domain transaction and confirm no executable job escapes it; kill after an external effect before acknowledgement and verify a retry cannot repeat the business effect.
- Account for every backlog state and observe only one scheduled enqueue for the transferred category.

- https://guides.rubyonrails.org/active_job_basics.html
- https://github.com/sidekiq/sidekiq/wiki/Best-Practices

### Identity and authorization

**Inspect the source:** Distinguish the application's generated Session model from Rails session storage. Capture cookie name, serializer, signing/encryption configuration, expiration, account IDs, logout/revocation and per-resource authorization.

**During coexistence:** Recommendation: keep a shared identity authority or a documented session exchange endpoint. If cookies are shared, qualify the complete cookie format and rotation rules; route stable users and retain the old decoder for the agreed window.

**Target design:** An intentionally selected Rails authentication implementation with application authorization. CookieStore stores session data on the client; account/session lifecycle rules must be designed separately.

**Rollback:** Recommendation: preserve old account IDs and accepted session formats until routing stabilizes; coordinate revocation and key rotation so restoring traffic cannot revive invalidated sessions.

**Benefits and prerequisites**

- Recommendation: coherent account and session ownership can preserve login continuity during feature migration. Requires: Verified identity mapping, cookie/exchange fixtures and shared revocation behavior. Tradeoffs: Compatibility code and key rotation increase maintenance; planned reauthentication is an alternative when continuity is unnecessary.

**Checks before transfer**

- Authenticate through the old path and visit the new route; then logout, expire or revoke the session and confirm both paths deny access.
- Replay a modified cookie, a stale cookie and a valid session from another tenant against a protected resource; each unauthorized operation must be rejected.

- https://guides.rubyonrails.org/security.html
- https://guides.rubyonrails.org/getting_started.html

### Realtime transport

**Inspect the source:** Capture channel names, connection authentication, subscription commands, DOM target IDs, Turbo stream actions and reconnect behavior. Turbo Streams can arrive over WebSockets, SSE or request responses; Action Cable owns its own client/server protocol.

**During coexistence:** Recommendation: keep the current realtime endpoint for old clients; bridge versioned domain events to the selected target renderer. Assign one event publisher per committed change and route a room/user cohort including reconnects, rather than randomly splitting individual socket requests.

**Target design:** Turbo streams over the selected transport, with Action Cable using a configured shared adapter when multiple server processes must communicate. Solid Cable is database-backed; Redis remains a documented alternative.

**Rollback:** Recommendation: preserve the old event renderer/endpoint and backward-readable stream payloads until the cohort can reconnect there; reconcile already-delivered state rather than blindly rebroadcasting.

**Benefits and prerequisites**

- HTML updates can reuse server-rendered partials. Requires: Stable DOM targets, authorized subscriptions and compatible event-to-view rendering. Tradeoffs: A new socket protocol still needs client changes or a bridge; reconnection recovery is an application acceptance requirement.

**Checks before transfer**

- Place old and new clients on different server processes; commit one change and verify both authorized clients display it once.
- Disconnect during a write, reconnect and verify the UI converges to the persisted state; unauthorized origins and subscriptions must fail.

- https://guides.rubyonrails.org/action_cable_overview.html
- https://turbo.hotwired.dev/handbook/streams

### Caching and shared state

**Inspect the source:** List reconstructible values separately from sessions, counters and locks. Capture key namespaces, serialized values, TTLs and invalidation triggers; Rails.cache and request-local SQL query caching have different lifetimes.

**During coexistence:** Recommendation: use a new cache namespace when representations differ, read through to the authoritative data and maintain invalidation for both deployed readers. Keep shared coordination uses on their qualified store while moving only disposable values.

**Target design:** A deliberately selected Rails cache store; Solid Cache is database-backed and new Rails 8 applications include it. MemoryStore and RedisCacheStore remain choices with different process/service boundaries.

**Rollback:** Recommendation: switch to the previous namespace/store and repopulate from domain data; retain the old backend while any coordination capability still depends on it.

**Benefits and prerequisites**

- Database-backed caching can remove a dedicated cache service when it is the last use. Requires: Reconstructible contents, tested expiration/invalidation, adequate database capacity and retirement of all other service uses. Tradeoffs: Cache traffic moves to the database; cache durability does not make it the authoritative domain store.

**Checks before transfer**

- Warm both versions, update the source record and verify neither version serves the prior value after its specified invalidation boundary.
- Restart the application or empty only the dedicated cache namespace; requests must rebuild correctly without losing identity or coordination state.

- https://guides.rubyonrails.org/caching_with_rails.html

### Delivery and recovery

**Inspect the source:** Record deployed web and Cable processes, configured workers/dispatchers, recurring.yml tasks and database connections. A web deployment alone does not establish that workers or broadcasts are running.

**During coexistence:** Recommendation: give each process a named operational owner; keep existing backups and queue monitoring while deploying the new cohort. Transfer recurring schedule ownership once, after checking overlapping old and new schedules.

**Target design:** An explicit Rails process inventory with worker lifecycle, queue failure inspection and the chosen realtime adapter. Recommendation: document separate domain, queue and cache database restore ordering where applicable.

**Rollback:** Recommendation: freeze producers and scheduler ownership transfers, restore the previous process configuration, then reconcile work accepted by the new deployment.

**Benefits and prerequisites**

- Recommendation: visible process and schedule ownership makes failures and recovery boundaries reviewable. Requires: A deployment recipe for the selected adapters and an exercised restore/restart procedure. Tradeoffs: Coexistence temporarily operates both systems; one healthy HTTP endpoint cannot certify all processes.

**Checks before transfer**

- Stop a worker, enqueue a representative task and verify monitoring identifies its growing age; restart and observe the intended completion/failure policy.
- Restore a disposable backup and prove domain records, delayed tasks and session behavior are accounted for before promoting traffic.

- https://guides.rubyonrails.org/active_job_basics.html
- https://guides.rubyonrails.org/action_cable_overview.html

Rewrite workflow: /rewrite/guide.md
Shared contracts and phases: /rewrite/contracts.json


## Setup
1. Complete the selected starting point and baseline checks in the Generators section first; then continue with the integration steps appropriate to the chosen component.
2. Configure ignored development/test database credentials and prepare the intended databases using the generated configuration. Use the conditional authentication generator when login is required; implement signup and resource-level permissions deliberately.
3. If Pundit is the selected authorization library, add it through Bundler and run bin/rails generate pundit:install after reviewing installed help; implement and invoke policies rather than relying on authentication alone.
4. For an API-first product, use the separate Rails --api starting point. Choose a client-specific identity and session model; configure cookies/CSRF only when browser sessions require them, and configure restricted CORS only for cross-origin browser clients. Test JSON request/response contracts, authentication, per-resource authorization, error statuses, and permitted/rejected origins as applicable.
5. For the Hotwire web app, start bin/rails server and inspect a browser journey; for an API-only app, verify its HTTP request/response journeys instead. Configure Solid Queue using the installed-version guide and run its bin/jobs worker only when background work is required and enabled.
6. Preserve Gemfile.lock and the generated checks. Add bundler-audit in development only if it is required and absent. Define authorization, duplicate-job and migration tests for the features present.
7. Prepare the chosen deployment configuration, secret ownership, database persistence and backup/restore procedure. When Kamal is the selected host tooling and deployment is authorized, use bundle exec kamal setup for initial setup or bundle exec kamal deploy for a subsequent release.

## Verification
Commands below require the selected tools and project configuration. Replace example paths, schemes and IDs; distinguish tests from builds and interactive startup. These are instructions, not recorded passes.

```text
ruby --version
bundle exec rails --version
bin/rails db:migrate:status
bin/rails zeitwerk:check
bin/rails test
bin/rails test:system
bin/rubocop
bin/brakeman
bundle exec bundler-audit check --update
```

## Open questions
- Which signup, SSO/MFA and resource authorization policies are required?
- Does the product fit server-owned screens or need substantial offline/client state?
- Which host, mail/storage services, worker throughput and restore requirements apply?

## Sources
- [Hotwire: HTML Over The Wire](https://hotwired.dev/)
- [Active Record Migrations](https://guides.rubyonrails.org/active_record_migrations.html)
- [Getting Started with Rails](https://guides.rubyonrails.org/getting_started.html)
- [Pundit README](https://github.com/varvet/pundit)
- [Devise README](https://github.com/heartcombo/devise)
- [Active Job Basics](https://guides.rubyonrails.org/active_job_basics.html)
- [Testing Applications](https://guides.rubyonrails.org/testing.html)
- [Securing Rails Applications](https://guides.rubyonrails.org/security.html)
- [bundler-audit README and license](https://github.com/rubysec/bundler-audit)
- [Kamal Installation](https://kamal-deploy.org/docs/installation/)
- [Rails and AI](https://rubyonrails.org/ai)
- [Rails MIT License](https://github.com/rails/rails/blob/main/MIT-LICENSE)
- [Rails Action Mailer](https://guides.rubyonrails.org/action_mailer_basics.html)
- [Rails Active Storage](https://guides.rubyonrails.org/active_storage_overview.html)
- [Rails Action Cable](https://guides.rubyonrails.org/action_cable_overview.html)

Keep the project README current and link the selected guidance; preserve existing project instructions.
