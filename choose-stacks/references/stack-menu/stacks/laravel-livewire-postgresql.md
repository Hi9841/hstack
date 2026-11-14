# Laravel + Livewire

PHP product applications with a cohesive UI, auth and queue toolset.

Language: PHP | Reviewed: 2026-10-10 | Evidence: documentation-reviewed research input

Source record: menu/inputs/research/rails-laravel.json.

Core guidance checked: 2026-10-13. Review sources are listed below. /research-freshness.json describes the imported research packet; this record retains its own evidence scope. These recipes and selected dependency combinations need qualification in the actual project.

## Application role
Components: web, api
UI: server
Deployment: server

## Use cases
- SaaS
- Administrative and business applications
- Server-driven interactive products

## Fit
- PHP team or Laravel ecosystem fit is strong.
- Integrated auth, queues and concrete agent inspection tools reduce assembly work.

## Choose something else when
- The UI fundamentally requires an offline/client-state architecture; use the Inertia alternative if Laravel still fits.
- A hosting plan cannot operate needed queue workers or scheduled jobs.

## Agent workflow
- Read README, dependency manifests, lockfiles, runtime pins and the maintained project workflow before changing anything. Preserve an existing stack unless reconsidering it is part of the request.
- For a new component, read the Generators section before writing application files. Use its appropriate official initializer and retain its generated baseline; follow-up generators are conditional on the selected feature.
- Use this guide to select tools by requirement. Resolve compatible versions from official and installed-version documentation; record the actual lockfile and runtime versions.
- Create a plan for schema changes, identity, authorization, external effects and deployment. A library choice does not complete its integration.
- Run relevant checks after configuration. Exercise the real interface, failure paths and packaged artifact on the intended target. Report commands, versions, results and untested behavior.
- On failure, retain the command and diagnostic, fix the failing prerequisite and resume there. Do not regenerate over existing work or suppress failures to make a check green.

## Best practices
- Use policies and gates for permissions; a starter's authentication flow does not supply product authorization.
- Preserve the selected starter's test conventions and verify Livewire behavior in a real browser.
- Supervise queue workers and schedule execution explicitly. Verify retries and avoid duplicate external effects.
- Use Laravel Boost during development with the project's installed documentation; keep production exposure separate.

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

#### Laravel installer with Livewire starter kit

Use when: A new Laravel application using the official Livewire authentication/UI starting point.

1. Select compatible PHP/Composer and Node/npm versions plus PostgreSQL and the PHP PostgreSQL PDO extension. Install the Laravel installer only if absent.
2. Inspect installed laravel new help; select Livewire and PostgreSQL explicitly. The example chooses Pest; use --phpunit instead if that is the project choice.
3. Configure ignored .env with the intended development database and secrets, review generated migrations, then migrate and build assets. Resume a failed installer database step from the generated project after correcting configuration; do not overwrite the project.

Working directory: A local source-workspace parent outside synchronized storage; my-app must not already exist

Install the official installer only when it is not already available.

```sh
composer global require laravel/installer
```

Working directory: A local source-workspace parent outside synchronized storage; my-app must not already exist

Confirm flags supported by the installed installer.

```sh
laravel new --help
```

Working directory: A local source-workspace parent outside synchronized storage; my-app must not already exist

Generate the official Livewire starter with explicit PostgreSQL and test choices.

```sh
laravel new my-app --livewire --database=pgsql --pest --no-boost
```

Working directory: The generated my-app directory after configuring its local .env and reviewing migrations

Apply pending migrations to the intended development database.

```sh
php artisan migrate
```

Working directory: The generated my-app directory

Install starter frontend dependencies if the installer has not already done so.

```sh
npm install
```

Working directory: The generated my-app directory

Build the generated frontend assets.

```sh
npm run build
```

- The installer may attempt database migration during creation; inspect its output and migrate:status before retrying. Database role/database provisioning and credential ownership must be established.
- Omit --git/--github and decline repository-creation prompts: those optional modes commit files and GitHub mode can publish. --no-boost keeps optional agent integration separate; configure it afterward only if selected, honoring README/instruction-file policy.
- Starter authentication is provided by Fortify. Resource policies, mail delivery and external identity choices remain application work; do not replace the starter auth by hand.

### Conditional follow-up generators

#### Conditional API routes and client authentication

Use when: Only when the application needs API endpoints for external, native or browser clients. Use this on the existing Laravel application after creation; the normal Livewire starter remains the web UI baseline.


Working directory: The generated my-app directory

Install Sanctum and create the stateless routes/api.php route file.

```sh
php artisan install:api
```

Working directory: The generated my-app directory

Inspect API routes and middleware after the API setup.

```sh
php artisan route:list --path=api -v
```

- Current Laravel 13 docs describe `install:api` as creating routes/api.php and installing Sanctum. The generated API route group is stateless; that does not mean every API endpoint must be stateless or authenticated. Keep intended public endpoints public, and apply auth:sanctum plus policy/ability checks only to protected routes. This setup is not necessary for a Livewire-only product.
- Choose the client contract deliberately. Sanctum supports bearer API tokens for native/third-party clients and cookie-based session authentication with CSRF protection for first-party SPAs sharing the same top-level domain. For cookie clients, configure stateful domains, CORS credentials, cookie scope and XSRF headers together; for cross-origin browser clients, allow only the required origins. Do not use bearer tokens for a first-party SPA when Sanctum's documented cookie flow fits.
- `php artisan install:api --passport` is a separate choice only when OAuth2 server capabilities are required. Do not install Passport and Sanctum indiscriminately.

#### Eloquent model and migration

Use when: Adding an example Product domain resource.


Working directory: The generated my-app directory

Generate an Eloquent model and companion migration.

```sh
php artisan make:model Product --migration
```

- Replace Product with the actual domain; inspect php artisan help make:model. Add constraints, relationships, allowed assignments and tests before applying migrations.

#### Additive migration

Use when: The existing products table needs an example description field.


Working directory: The generated my-app directory

Generate the next migration for an existing table.

```sh
php artisan make:migration add_description_to_products_table
```

- Edit the generated up/down methods deliberately and review SQL/data impact before php artisan migrate. Do not use migrate:fresh against retained data.

#### Livewire component/page

Use when: A new interactive server-driven page is required.


Working directory: The generated my-app directory with Livewire 4 installed

Generate an example Livewire page component.

```sh
php artisan make:livewire pages::product.create
```

- Confirm installed Livewire version and php artisan help make:livewire. Current Livewire 4 defaults differ from v3 class-based paths; retain the starter convention or deliberately choose the supported --class option.

#### Authorization policy

Use when: The Product model needs explicit per-resource permissions.


Working directory: The generated my-app directory with Product model present

Generate a conventional policy for application-specific authorization logic.

```sh
php artisan make:policy ProductPolicy --model=Product
```

- Implement and invoke the policy, then test rejected requests; the generated stub does not establish access control.

### Preserve the generated foundation

- Starter .gitignore, .env.example and secret exclusions, composer/package lockfiles, Artisan layout, Fortify auth flows, selected Pest/PHPUnit suite and Livewire/Tailwind/Flux integration.
- Free versus paid Flux components remain a product decision. Preserve the working starter before customizing its UI or adding optional Boost/browser tooling.

### Baseline and generation checks

- Run composer check-platform-reqs, php artisan about, php artisan migrate:status, php artisan test and npm run build.
- When API routes are selected, add HTTP tests for public/protected route behavior, authentication, policy denials, validation and response contracts; test CSRF, cookies and allowed/rejected CORS origins for browser clients that need them.
- Run the generated style/security checks available in the project; verify database tests use a dedicated test database.
- Use composer run dev and verify registration/login and one authorized plus one rejected browser flow. Record resolved versions and generation choices.

### Generation receipt

- Component and selected starting point, or the documented absence of a full application generator
- Generator/toolchain versions, exact commands or IDE template/settings, working directory and generated destination
- Generated files retained, deliberate deviations with reasons, and required supplemental ignore rules
- Baseline checks and later checks actually run, results and remaining prerequisites or untested behavior

### Generator sources

- [Laravel 13 API routing and install:api behavior](https://laravel.com/framework/docs/13.x/routing)
- [Laravel 13 Sanctum tokens, SPA sessions and CSRF](https://laravel.com/framework/docs/13.x/sanctum)
- [Laravel 13 Passport and OAuth2 selection](https://laravel.com/framework/docs/13.x/passport)
- [Laravel starter kits](https://laravel.com/framework/docs/13.x/starter-kits)
- [Laravel installation](https://laravel.com/framework/docs/13.x/installation)
- [Laravel installer source: flags and optional commits](https://raw.githubusercontent.com/laravel/installer/master/src/NewCommand.php)
- [Eloquent model generation](https://laravel.com/framework/docs/13.x/eloquent)
- [Laravel migrations](https://laravel.com/framework/docs/13.x/migrations)
- [Livewire 4 component generation](https://livewire.laravel.com/docs/4.x/components)
- [Laravel policy generation](https://laravel.com/framework/docs/13.x/authorization)
- [Laravel Boost](https://laravel.com/framework/docs/13.x/boost)
- [Laravel Dusk](https://laravel.com/framework/docs/13.x/dusk)

## Tools

### UI: Official Livewire starter kit + Blade/Tailwind

One supported starter establishes coherent UI/auth integration.

Limits and integration: Starter includes Flux; distinguish its free components from paid Pro assets.


- https://laravel.com/framework/docs/13.x/starter-kits
- https://fluxui.dev/pricing

Alternatives: Official React/Vue/Svelte Inertia kits for heavier client interactions

### Database and migrations: PostgreSQL + Eloquent + Laravel migrations

Conventional ORM and migrations with a production relational store.

Limits and integration: Use constraints; production-engine integration tests; never use migrate:fresh against retained data.


- https://laravel.com/framework/docs/13.x/database
- https://laravel.com/framework/docs/13.x/migrations

Alternatives: SQLite for local/small deployments; existing MySQL where operationally established

### Authentication: Starter-kit Fortify auth

Existing authentication flow plus resource-level authorization.

Limits and integration: Policies remain application work; managed identity adds external terms/cost.


- https://laravel.com/framework/docs/13.x/starter-kits
- https://laravel.com/framework/docs/13.x/authorization

Alternatives: WorkOS starter variant for managed identity requirements

### Authorization: Laravel policies and gates

Existing authentication flow plus resource-level authorization.

Limits and integration: Policies remain application work; managed identity adds external terms/cost.


- https://laravel.com/framework/docs/13.x/starter-kits
- https://laravel.com/framework/docs/13.x/authorization

Alternatives: Existing explicit resource-level authorization implementation; identity providers still require policies

### Queues: Laravel database queue + supervised workers

Simple starting infrastructure with explicit scale-up options.

Limits and integration: Use after-commit dispatch, idempotent jobs, finite retries and worker restarts. Horizon requires Redis.


- https://laravel.com/framework/docs/13.x/queues
- https://laravel.com/framework/docs/13.x/horizon

Alternatives: Redis + Horizon for queue dashboards/balancing; SQS for an established managed queue

### Tests: Pest or PHPUnit from starter; Dusk for key browser flows

Application and browser verification complement each other.

Limits and integration: Use a dedicated test database and install Dusk only in development.


- https://laravel.com/framework/docs/13.x/testing
- https://laravel.com/framework/docs/13.x/dusk

Alternatives: Keep the existing test runner rather than changing syntax for its own sake

### Lint, static analysis and security: Pint + Larastan/PHPStan + Composer audit

Formatting, static checks and dependency advisory checks expose different failures.

Limits and integration: Install a compatible Larastan version and configure its extension; no audit substitutes for authorization tests.


- https://laravel.com/framework/docs/13.x/pint
- https://github.com/larastan/larastan
- https://getcomposer.org/doc/03-cli.md#audit

Alternatives: Existing equivalent tooling if already maintained

### Deployment: PHP-FPM web service + worker supervisor + scheduler on chosen host

A conventional process model is a practical default.

Limits and integration: Serve only public/; APP_DEBUG=false; persist uploads; reload workers after releases; paid platforms are optional.


- https://laravel.com/framework/docs/13.x/deployment

Alternatives: Laravel Cloud for managed operation; Forge for server management

### Agent tooling: Laravel Boost development dependency

Version-aware documentation and route/schema/log inspection provide concrete context.

Limits and integration: Tools can execute application code; use development credentials and honor maintained repository instructions. A README-only integration is an optional project policy; inspect installed Boost help before opting out of generated instructions.


- https://laravel.com/framework/docs/13.x/ai

Alternatives: Normal CLI/docs when MCP is unavailable

### Licensing and hosting: Laravel framework MIT; self-hostable

Framework use does not mandate a hosting subscription.

Limits and integration: Check each optional asset/package/service license separately.


- https://github.com/laravel/framework/blob/13.x/LICENSE.md
- https://fluxui.dev/pricing

Alternatives: Optional paid Flux Pro and managed services

### Transactional email: Laravel Mail

Mailables and queue integration keep delivery in application conventions

Limits and integration: Configure the selected mailer and verified sender; use queued mail where required, after-commit handling and failed-job monitoring. Provider acceptance is not inbox delivery.


- https://laravel.com/framework/docs/13.x/mail

Alternatives: Preserve an existing compatible project choice

### Uploads and object storage: Laravel Storage / Flysystem

Storage disks support private local or S3-backed files

Limits and integration: Configure filesystems.php; install the selected adapter only, authorize downloads and uploads, define size/type limits and retention. Ephemeral deploy disks are not durable shared storage.


- https://laravel.com/framework/docs/13.x/filesystem

Alternatives: Preserve an existing compatible project choice

### Realtime transport: Laravel broadcasting + Reverb when self-hosted sockets are required

Private channels integrate realtime application events

Limits and integration: Use the installed broadcasting setup; configure Echo, channel authorization, queued events and a supervised Reverb process. Verify TLS/proxy/scaling and reconnect; broadcast is not durable replay.


- https://laravel.com/framework/docs/13.x/broadcasting

Alternatives: Preserve an existing compatible project choice

## Architecture and developer workflow

Laravel combines conventional routes, middleware, authentication guards/providers and database migrations. Livewire components combine PHP behavior with Blade rendering. Recommendation: use these conventions for connected forms and business screens; keep server authorization and domain writes explicit instead of treating public component properties as trusted state.

Version scope: Laravel 13.x and Livewire 4.x documentation fetched 11 October 2026. These are documentation scopes, not proof of installed compatibility; inspect composer.lock, PHP version, queue/session/cache drivers and current Livewire component format before implementation.
Reviewed: 2026-10-11 | Evidence: documentation-reviewed | Source record: inputs/research/migrations-server.json

### Architecture boundaries

- Recommendation: keep a single domain writer and migration owner during shared-schema coexistence; let controllers, Livewire actions and queued workers call the same application operation with its authorization and transaction rules.
- Queue connections select backends while queue names select work categories. The documented choices include relational storage, Redis and SQS. Recommendation: choose a backend from recovery and operation requirements rather than assuming every Laravel application needs Redis.
- Recommendation: list HTTP PHP execution, queue workers, the scheduler and a selected broadcast server separately. Livewire component interactivity does not by itself establish multi-client event delivery; broadcasting has its own backend/client and queue configuration.

### Tools and feedback

- In a configured local Laravel project, php artisan make:livewire post.create creates a Livewire 4 component; --class retains the established class-based style and --mfc creates a multi-file component. Inspect existing conventions before choosing a format.
- php artisan make:job ProcessPodcast creates a queued job. Configure the selected connection and run php artisan queue:work --queue=high,default only after those queues and priorities match the application; supervise the production worker separately.
- php artisan migrate applies reviewed migrations. For missing database session/queue tables, the selected-version docs provide php artisan make:session-table and php artisan make:queue-table; check existing migrations first to avoid duplicate tables.
- Recommendation: verify behavior with real driver instances in a disposable environment, including timeout/retry interaction, denied Livewire actions, concurrent session writes and private broadcast authorization. Faking queue submission alone cannot exercise worker serialization or crash recovery.

### Translations to avoid

- Avoid switching queue consumers solely because both use Redis: Laravel payloads and Eloquent identifier rehydration are framework execution contracts. Recommendation: preserve old consumers or translate deliberately versioned payloads.
- Avoid worker timeout values longer than retry_after; Laravel warns this can allow the job to be processed twice. Avoid assuming unique-job locks make external effects exactly once; recommendation: use business idempotency.
- Avoid calling onOneServer a cross-stack scheduler lock. It uses a shared supported Laravel cache store; recommendation: explicitly retire the old scheduler for the transferred business category.
- Avoid trusting client-editable Livewire properties or hidden buttons for authorization. Avoid Cache::flush on a backend shared with other applications; the documented flush ignores the configured prefix.

### Architecture sources

- [Laravel 13 Database Migrations](https://laravel.com/docs/13.x/migrations): Schema migration and rollback commands.
- [Laravel 13 Queues](https://laravel.com/docs/13.x/queues): Connections versus queues, model serialization, after-commit dispatch, workers and timeout/retry_after interaction.
- [Laravel 13 HTTP Session](https://laravel.com/docs/13.x/session): Database session default, driver/table prerequisites and session-blocking requirements.
- [Laravel 13 Authentication](https://laravel.com/docs/13.x/authentication): Guard/provider architecture, sessions, logout and authentication configuration.
- [Laravel 13 Broadcasting](https://laravel.com/docs/13.x/broadcasting): Broadcast drivers, ShouldBroadcast/queue execution, private authorization and after-commit dispatch.
- [Laravel 13 Cache](https://laravel.com/docs/13.x/cache): Backend capabilities, atomic lock prerequisites and prefix-independent cache flush.
- [Laravel 13 Scheduling](https://laravel.com/docs/13.x/scheduling): Scheduler operation, timezones, overlap prevention and shared-store onOneServer locking.
- [Livewire 4 Components](https://livewire.laravel.com/docs/4.x/components): PHP/Blade components and make:livewire format options.
- [Livewire 4 Security](https://livewire.laravel.com/docs/4.x/security): Client-controlled properties/actions require validation and authorization.

## Transition options

Proposed designs and checks; these are not executed compatibility results.

### Data and schema

**Inspect the source:** Inventory table identifiers, casts/nullability, timestamps, constraints and side effects currently attached to writes. Migrations evolve the schema; Eloquent models do not automatically reproduce another runtime’s callbacks.

**During coexistence:** Recommendation: keep the existing writer authoritative, add compatible fields and move one domain operation at a time. Let one named migration runner own shared tables and keep old readers functional during the rollback window.

**Target design:** Laravel database migrations and the selected PostgreSQL schema, with application operations reused by controllers/Livewire/workers. Recommendation: delay destructive schema contraction until all old readers retire.

**Rollback:** Recommendation: restore the old writer before contracting fields; preserve additive schema and reconcile writes accepted by Laravel.

**Benefits and prerequisites**

- Recommendation: conventional schema and application ownership can make changes reviewable in one maintained application. Requires: Explicit writer transfer, tested value mappings and a single schema owner. Tradeoffs: Both runtimes remain constrained by the shared schema; reversal does not recreate deleted business data.

**Checks before transfer**

- Create and update a representative fixture through both allowed paths; compare IDs, nulls, timezone handling and unique/foreign-key failures.
- Apply the reviewed migration to a disposable restored copy and confirm both deployed versions still understand new writes.

- https://laravel.com/docs/13.x/migrations

### Jobs and schedules

**Inspect the source:** Record connection, queue, PHP job class, serialized model identifiers/relationships, timeout, retry_after, failures and delayed/running work. Model arguments may be re-fetched when the worker executes.

**During coexistence:** Recommendation: keep old consumers for old payloads; route new categories to isolated Laravel queues. Transfer producers and each schedule owner together. Account for ready, delayed, failed, retry and in-flight work before retiring the old backend.

**Target design:** ShouldQueue jobs on an intentionally selected database/Redis/SQS connection, with supervised workers and explicit attempts/timeouts. after_commit or afterCommit delays dispatch until commit; recommendation: use a durable outbox for a required recoverable commit-to-broker handoff.

**Rollback:** Recommendation: stop the new producer, keep consumers for accepted payload versions and reconcile external effects before restoring old queue routing.

**Benefits and prerequisites**

- Recommendation: a job category can move without rebuilding the entire backlog. Requires: Versioned payload fixtures, isolated queues and retained old consumers. Tradeoffs: Two queue systems may remain temporarily; serialized framework objects are not a portable cross-runtime API.

**Checks before transfer**

- Enqueue a model, alter/delete it before execution and verify the intended rehydration/failure behavior.
- Roll back the domain transaction and verify after-commit dispatch produces no job; kill after an external effect and prove retry cannot duplicate the business effect.
- Set worker timeout below the applicable retry/visibility boundary and verify a long job cannot have two concurrent effects.

- https://laravel.com/docs/13.x/queues

### Identity and authorization

**Inspect the source:** Capture guard/provider, account mapping, session driver, cookie/encryption configuration, remember-me behavior, expiry and logout. The current docs default to database sessions; the application may use another driver.

**During coexistence:** Recommendation: retain a named identity authority or qualified session exchange; share cookies only after full-format fixtures pass. Map old per-resource permissions into every Livewire/server action and keep concurrent session semantics explicit.

**Target design:** Laravel authentication guard/provider plus a selected session store and resource authorization. Session blocking needs a supported atomic-lock cache driver and is unavailable with cookie sessions.

**Rollback:** Recommendation: retain old session/exchange support until the cohort can return, while preserving every revocation and account mapping.

**Benefits and prerequisites**

- Recommendation: explicit session/account ownership can preserve user continuity during feature migration. Requires: Qualified identity/session mapping and common revocation rules. Tradeoffs: Lock-capable session coordination adds a store dependency; a shared database alone does not prove cookie compatibility.

**Checks before transfer**

- Login through the old application, access the Laravel feature and revoke/logout; both paths must deny future operations.
- Run concurrent requests that modify one session and verify required data is not lost.
- Modify a Livewire public identifier to another tenant’s record and directly invoke the action; the server must reject it.

- https://laravel.com/docs/13.x/authentication
- https://laravel.com/docs/13.x/session
- https://livewire.laravel.com/docs/4.x/security

### Realtime transport

**Inspect the source:** Capture client protocol, event name/payload, private/presence channel identity, authorization endpoint and queue connection. ShouldBroadcast dispatches broadcast work; event production and broadcast execution are separate concerns.

**During coexistence:** Recommendation: retain the old endpoint for old clients and bridge versioned domain events to the selected Laravel broadcaster. Route a stable room/user cohort including reconnects; designate one publisher per committed domain change.

**Target design:** Laravel broadcasting with an explicitly chosen supported driver and client integration, plus working queue workers when required. Defer transactional events until commit with the documented mechanism; recommendation: persist domain state for reconnect recovery.

**Rollback:** Recommendation: preserve old event names/endpoints and stop new publication before restoring the old publisher; reconcile already-visible state.

**Benefits and prerequisites**

- Recommendation: backend events can update multiple authorized clients. Requires: Configured broadcaster, workers and matching event/client contracts. Tradeoffs: Livewire alone does not remove those operational pieces; changing the broadcaster protocol may require a bridge or client rollout.

**Checks before transfer**

- Put clients on separate server instances and verify one committed event reaches all authorized recipients.
- Rollback the domain write and confirm no premature broadcast occurs.
- Revoke private-channel access, disconnect/reconnect and verify unauthorized delivery fails and the UI catches up from source state.

- https://laravel.com/docs/13.x/broadcasting
- https://laravel.com/docs/13.x/queues

### Caching and shared state

**Inspect the source:** Inventory cached values, serialization, TTLs and invalidation separately from locks, unique jobs, scheduler coordination and sessions. Laravel supports several cache stores with different capabilities.

**During coexistence:** Recommendation: version namespaces for changed representations and keep coordination on the same qualified central store. Move reconstructible values separately; never globally flush a shared backend during cutover.

**Target design:** Selected Laravel cache driver for disposable cached data; a supported central store for atomic locks across servers. Recommendation: use explicit dedicated stores/namespaces for distinct ownership boundaries.

**Rollback:** Recommendation: restore previous cache routing and rebuild from domain data; preserve lock/session store ownership until a separate qualified transition.

**Benefits and prerequisites**

- Recommendation: a cache backend can change independently of domain storage when contents are reconstructible. Requires: Verified invalidation, serialization and coordination inventory. Tradeoffs: Lock owners and dependent scheduler/session features may still prevent retiring the old backend.

**Checks before transfer**

- Warm both application versions, update authoritative data and verify both observe the required invalidation/TTL rule.
- Contend for a lock from two servers; only the intended owner may act.
- Clear only the migration’s disposable cache and verify other applications and coordination keys survive.

- https://laravel.com/docs/13.x/cache

### Delivery and recovery

**Inspect the source:** List scheduler definitions, timezones, overlapping task prevention, worker lifecycle and cache-backed coordination. Laravel schedules and old cron/Celery/Rails schedules may describe the same business action.

**During coexistence:** Recommendation: give each scheduled action one logical owner. Transfer it at an explicit boundary; Laravel onOneServer coordinates Laravel instances using a shared supported store and does not retire an external scheduler.

**Target design:** A documented Laravel scheduler invocation and supervised queue workers. Use withoutOverlapping/onOneServer only with their selected store and intended lock scope; recommendation: document missed-run and business idempotency policies separately.

**Rollback:** Recommendation: stop the Laravel schedule before restoring the old owner; reconcile accepted jobs and completed effects before replay.

**Benefits and prerequisites**

- Recommendation: explicit schedule and worker ownership can prevent accidental duplicate production during rollout. Requires: Schedule inventory, shared supported locking when needed and a coordinated old-scheduler retirement. Tradeoffs: A lock prevents concurrent starts within its scope, not every replayed business effect; coexistence still needs two operational inventories.

**Checks before transfer**

- Run the scheduled fixture across two Laravel servers and verify one enqueue, then confirm the old scheduler stays disabled for that category.
- Exercise timezone and long-running/overlap cases; restart the worker and scheduler and verify intended missed-run behavior.

- https://laravel.com/docs/13.x/scheduling
- https://laravel.com/docs/13.x/queues

Rewrite workflow: /rewrite/guide.md
Shared contracts and phases: /rewrite/contracts.json


## Setup
1. Complete the selected starting point and baseline checks in the Generators section first; then continue with the integration steps appropriate to the chosen component.
2. Configure ignored .env database/mail/queue settings for the features selected and confirm application key generation. Review the target database and migration status before applying pending migrations; preserve the starter authentication and selected test framework.
3. When a stateless API is required, run the conditional install:api setup and classify each route as public or protected. Choose Sanctum bearer tokens, first-party cookie sessions with CSRF, or OAuth2 only from the actual clients; add explicit per-resource policies and test both allowed and denied requests. Configure CORS and credentials narrowly for cross-origin browser clients, not as a default for native/server clients.
4. Build frontend assets and start composer run dev for local verification. Configure a supervised queue worker and scheduler separately for production when the application uses them.
5. If Laravel Boost is selected, add composer require laravel/boost --dev only if absent, inspect php artisan help boost:install and configure the chosen integration. Honor repository instruction ownership; for README-only policies inspect installer opt-outs or configure supported MCP integration manually.
6. When static analysis is selected, install a compatible Larastan development dependency and configure phpstan.neon from its installed-version guide. For selected browser testing, install laravel/dusk as a development dependency and run php artisan dusk:install; keep database/browser tests isolated.
7. For an authorized release, install locked production dependencies, build assets, review migrations, run php artisan optimize and reload supervised services. Confirm backup/restore and rollback compatibility before production migrations.

## Verification
Commands below require the selected tools and project configuration. Replace example paths, schemes and IDs; distinguish tests from builds and interactive startup. These are instructions, not recorded passes.

```text
php --version
composer check-platform-reqs
php artisan about
php artisan migrate:status
php artisan test
php artisan dusk
vendor/bin/pint --test
vendor/bin/phpstan analyse
composer audit
npm run build
```

## Open questions
- Which starter-kit features and paid UI components are actually required?
- Which identity and per-resource authorization policies must be supported?
- Which host, mail/storage providers, realtime capacity and worker/scheduler operation will own production?

## Sources
- [Laravel Starter Kits](https://laravel.com/framework/docs/13.x/starter-kits)
- [Flux Pricing and Component Tiers](https://fluxui.dev/pricing)
- [Laravel Database: Getting Started](https://laravel.com/framework/docs/13.x/database)
- [Laravel Database Migrations](https://laravel.com/framework/docs/13.x/migrations)
- [Laravel Authorization](https://laravel.com/framework/docs/13.x/authorization)
- [Laravel Queues](https://laravel.com/framework/docs/13.x/queues)
- [Laravel Horizon](https://laravel.com/framework/docs/13.x/horizon)
- [Testing Applications](https://laravel.com/framework/docs/13.x/testing)
- [Laravel Dusk](https://laravel.com/framework/docs/13.x/dusk)
- [Laravel Pint](https://laravel.com/framework/docs/13.x/pint)
- [Larastan README](https://github.com/larastan/larastan)
- [Composer CLI: Audit](https://getcomposer.org/doc/03-cli.md#audit)
- [Laravel Deployment](https://laravel.com/framework/docs/13.x/deployment)
- [AI Assisted Development](https://laravel.com/framework/docs/13.x/ai)
- [Laravel Framework MIT License](https://github.com/laravel/framework/blob/13.x/LICENSE.md)
- [Laravel Mail](https://laravel.com/framework/docs/13.x/mail)
- [Laravel file storage](https://laravel.com/framework/docs/13.x/filesystem)
- [Laravel broadcasting](https://laravel.com/framework/docs/13.x/broadcasting)

Keep the project README current and link the selected guidance; preserve existing project instructions.
