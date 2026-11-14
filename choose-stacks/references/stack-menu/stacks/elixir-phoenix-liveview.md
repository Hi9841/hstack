# Phoenix + LiveView

Connected products, live updates and background work in one application.

Language: Elixir | Reviewed: 2026-10-10 | Evidence: documentation-reviewed research input

Source record: menu/inputs/research/elixir.json.

Core guidance checked: 2026-10-13. Review sources are listed below. /research-freshness.json describes the imported research packet; this record retains its own evidence scope. These recipes and selected dependency combinations need qualification in the actual project.

## Application role
Components: web, api
UI: server
Deployment: server

## Use cases
- Connected browser products and portals
- Real-time collaboration interfaces
- JSON APIs for native clients
- Durable application background work

## Fit
- Server-owned state and business rules dominate a connected product.
- Phoenix conventions and OTP process lifecycles match the service requirements.
- A relational store can also support durable background jobs.

## Choose something else when
- The main deliverable is a platform-native mobile UI or offline-first client.
- The application depends on a library, accelerator or vendor SDK unsupported by the intended Elixir deployment.
- A small static site, simple script or CLI does not need a running web application.

## Agent workflow
- Read README, dependency manifests, lockfiles, runtime pins and the maintained project workflow before changing anything. Preserve an existing stack unless reconsidering it is part of the request.
- For a new component, read the Generators section before writing application files. Use its appropriate official initializer and retain its generated baseline; follow-up generators are conditional on the selected feature.
- Use this guide to select tools by requirement. Resolve compatible versions from official and installed-version documentation; record the actual lockfile and runtime versions.
- Create a plan for schema changes, identity, authorization, external effects and deployment. A library choice does not complete its integration.
- Run relevant checks after configuration. Exercise the real interface, failure paths and packaged artifact on the intended target. Report commands, versions, results and untested behavior.
- On failure, retain the command and diagnostic, fix the failing prerequisite and resume there. Do not regenerate over existing work or suppress failures to make a check green.

## Best practices
- Keep business operations in contexts shared by controllers, LiveViews and workers. Contexts are not automatically processes.
- Enforce authorization on every protected operation, including direct context calls and after access is revoked.
- Use ordinary functions first. Add processes for state ownership or lifecycle; add durable storage for work that must survive a restart.
- Give retried external effects stable idempotency keys. Exercise reconnects, failed jobs and cross-account access.

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

#### Phoenix browser application with LiveView and PostgreSQL

Use when: A new connected browser application uses this profile. Generate the skeleton before adding application code.

1. Read the repository README, runtime pins and existing mix.exs/mix.lock first. Existing applications keep their structure; do not regenerate over them.
2. Choose a local source workspace and a new destination. Replace my_app with the chosen snake_case application name throughout these examples.
3. Install a compatible Erlang/OTP and Elixir pair using official installation guidance; check the chosen Phoenix release requirements. Set up PostgreSQL access for development and tests.
4. Check installed tools. Install Hex only if missing, and install the Phoenix archive only if missing or deliberately changing its version. Check installed generator help before choosing switches.
5. Generate the project, respond to the dependency-install prompt, then enter my_app. Review the generated README, mix.exs aliases, configuration and any agent guidance.
6. Configure database credentials outside committed secrets. Inspect the generated mix setup alias before running it; it can fetch dependencies, create/migrate the database and build assets. Resolve failures in place and retain their output.

Working directory: chosen local workspace

Inspect the active Elixir and Erlang/OTP versions

```sh
elixir --version
```

Working directory: chosen local workspace

Inspect the active Mix runtime

```sh
mix --version
```

Working directory: chosen local workspace

Install Hex only when missing; review the installation prompt

```sh
mix local.hex --if-missing
```

Working directory: chosen local workspace; only if installer is missing or a deliberate update is needed

Install the Phoenix generator; select/record a compatible version according to project policy

```sh
mix archive.install hex phx_new
```

Working directory: chosen local workspace

Record the installed Phoenix generator version

```sh
mix phx.new --version
```

Working directory: chosen local workspace

Confirm installed options and defaults

```sh
mix help phx.new
```

Working directory: parent directory of the new my_app directory

Generate the Phoenix application, including LiveView and asset defaults

```sh
mix phx.new my_app --database postgres
```

Working directory: my_app project root, after inspecting the generated alias and configuring local database access

Run the generated setup alias

```sh
mix setup
```

- LiveView is included by the normal Phoenix generator. Keep HTML and assets for this browser path.
- Dependency installation is interactive by default; installed help documents --install and --no-install. These examples do not request a Git commit.
- Use --no-agents-md only for an explicit repository instruction policy; preserve the generated guidance in its maintained README-linked owner when that policy requires it.

#### Phoenix JSON API application

Use when: The deliverable is an HTTP API with a separate client and does not need generated browser UI.

1. Use the runtime, Hex, Phoenix archive and PostgreSQL prerequisite checks from the browser starting point.
2. Generate into a new destination; configure the database, inspect the generated setup alias and run it from the project root.
3. Select mailer, dashboard, Ecto and other omissions separately from actual requirements. Do not remove persistence simply because the interface is JSON.

Working directory: parent directory of the new my_app directory

Generate an API skeleton without HTML views or asset build tools

```sh
mix phx.new my_app --database postgres --no-html --no-assets
```

- --no-html disables the generated LiveView setup; this is an alternative to the browser starting point.
- --no-ecto changes what resource generators can provide. Use it only when the application truly does not need Ecto; inspect --no-context handling for later generators.
- Browser authentication scaffolding is not an API-token or external identity implementation. Choose API authentication explicitly.

#### Plain Mix library or supervised OTP service

Use when: The project needs Elixir without a Phoenix web application. Choose the variant from process-lifecycle requirements.

1. Verify compatible Elixir/Erlang and Mix; choose a new source destination. Replace my_library or my_service with the selected snake_case name.
2. For a library with no owned supervision tree, use mix new. For an application that owns long-lived processes, use mix new --sup.
3. Run only the selected creation command. Enter its generated directory, preserve its scaffold and implement application behavior after generation.

Working directory: chosen local workspace

Inspect installed Mix generator options

```sh
mix help new
```

Working directory: parent directory of the new my_library directory

Generate a plain Elixir project without an application callback/supervisor

```sh
mix new my_library
```

Working directory: parent directory of the new my_service directory

Alternative: generate an OTP application callback and supervision tree

```sh
mix new my_service --sup
```

- --sup is conditional, not a universal Elixir requirement. Do not hand-write mix.exs, formatter, test helper or supervision boilerplate when Mix supplies the appropriate base.
- Use --umbrella only for a justified multi-application boundary; do not introduce it as a default.

### Conditional follow-up generators

#### Phoenix authentication

Use when: Application-owned browser accounts are required, after Phoenix setup.


Working directory: my_app project root (directory containing mix.exs)

Phoenix authentication

```sh
mix phx.gen.auth Accounts User users --live
```

- Run mix help phx.gen.auth first; substitute the context/schema/table deliberately. --live selects LiveView views; --no-live is the controller-view alternative.
- Follow the generated routing/configuration instructions, fetch new dependencies with mix deps.get, inspect migrations and apply them to the intended local database with mix ecto.migrate.
- Review delivery, scope and authorization requirements. Generated email authentication assumes email-account ownership; preserve its token-revocation and confirmation safeguards when customizing.
- Do not run multiple auth generators blindly: scopes and browser-pipeline assignments can conflict. Use external identity integration when that is the actual requirement.

#### LiveView resource

Use when: A new browser CRUD resource should follow Phoenix conventions.


Working directory: my_app project root (directory containing mix.exs)

LiveView resource

```sh
mix phx.gen.live Catalog Product products name:string
```

- Example names/fields are substitutions, not a domain prescription. Run mix help phx.gen.live and decide context boundaries before generating.
- This generates the context/schema/migration and LiveView files/tests. Apply the printed router changes and inspect/migrate the local database.
- Preserve configured scope behavior and add permission/domain checks. --no-context implies --no-schema and leaves implementation work, including failing generated tests, to complete.
- Use this or the other resource variants below; do not generate the same resource repeatedly with each variant.

#### Controller HTML resource

Use when: The resource uses conventional server-rendered controllers/templates rather than LiveView.


Working directory: my_app project root (directory containing mix.exs)

Controller HTML resource

```sh
mix phx.gen.html Catalog Product products name:string
```

- Alternative to phx.gen.live, requiring the HTML components omitted by --no-html. Run installed task help first.
- Review generated context, schema, migration, controller/templates and tests; complete the printed routing instructions and migration steps.

#### JSON API resource

Use when: The resource is exposed as JSON.


Working directory: my_app project root (directory containing mix.exs)

JSON API resource

```sh
mix phx.gen.json Catalog Product products name:string
```

- Alternative to HTML/LiveView resource generation. Run installed task help; review generated controller/JSON rendering, context, schema, migration and tests.
- Complete printed routing instructions and migrations. Add actual API authentication/authorization, validation and response-contract tests.

#### Domain context without web UI

Use when: The application needs a new domain resource/API boundary without generated HTTP or LiveView files.


Working directory: my_app project root (directory containing mix.exs)

Domain context without web UI

```sh
mix phx.gen.context Catalog Product products name:string
```

- Run installed task help and review context boundaries. The generator adds schema, migration and context tests.
- An existing context can be extended; inspect the merge prompt instead of blindly accepting it. Choose --no-schema only when intentionally supplying that implementation.

#### Ecto schema without context scaffolding

Use when: A schema and migration are needed within a deliberately maintained domain boundary.


Working directory: my_app project root (directory containing mix.exs)

Ecto schema without context scaffolding

```sh
mix phx.gen.schema Catalog.Product products name:string
```

- Run installed task help; choose attribute types, references, ID strategy and table names explicitly.
- Review changesets and migration constraints/indexes. This generator does not provide the enclosing context API or authorization.

#### Ecto migration

Use when: An existing persisted resource requires a schema change, without duplicating its resource generator.


Working directory: my_app project root (directory containing mix.exs)

Ecto migration

```sh
mix ecto.gen.migration add_product_status
```

- Requires an Ecto repository configured under :ecto_repos, or choose it with --repo. Run installed task help before use.
- Edit the generated timestamped migration; review reversibility, data and locking effects. Apply it to the intended local database, then test the changed behavior. Do not rewrite migrations already deployed to shared databases.

#### Phoenix release helpers

Use when: Release-based deployment has been selected.


Working directory: my_app project root (directory containing mix.exs)

Phoenix release helpers

```sh
mix phx.gen.release
```

- Run installed task help first. Review migration/server scripts and runtime configuration before building the release.
- Use --docker only when a container is required; inspect generated base-image/runtime versions and add any external asset package-manager steps.
- Generation/build success does not prove deployment, migrations, backup/restore or runtime compatibility.

### Preserve the generated foundation

- Keep generated mix.exs aliases, .formatter.exs, tests/helpers, configuration, runtime supervision and project documentation as the starting base; make deliberate, reviewable changes rather than recreating the scaffold by hand.
- Preserve the complete generated .gitignore and add project/platform entries such as .DS_Store as supplements. Do not claim every generator version already ignores macOS metadata.
- Retain dependency lockfiles for application reproducibility according to repository policy. Keep credentials, build outputs and dependency caches out of commits.
- Existing project conventions and maintained README-linked guidance remain authoritative; generator commands are for new projects or deliberate scoped additions, not destructive replacement.
- Record the generator command, versions, selected switches and reasons for deviations with the project setup evidence.

### Baseline and generation checks

- Before generation, inspect installed mix help for each selected task and check the chosen runtime/generator requirements against installed versions; unversioned documentation can describe a newer release.
- Inspect the generated files and pending repository diff, including hidden files. Check that formatter configuration, tests/helpers, ignore rules and required application supervision are present for the selected variant.
- Run mix format --check-formatted, mix compile --warnings-as-errors and mix test from the generated project root after dependency/database setup. Repair failures in place and record actual results.
- For Phoenix browser applications, run mix phx.server and inspect the actual local page and generated flows; for APIs, exercise the intended requests. A server process starting is not a completed interaction check.
- Use git status --short --untracked-files=all and git check-ignore -v .DS_Store _build deps to review the selected ignore rules. In a disposable copy or separate index, inspect what staging all files would include; never alter the user index merely to test hygiene.
- Confirm generated authentication/scopes and application operations reject unauthorized access; generated CRUD does not settle domain permissions.
- This record is documentation-reviewed only. No application generator, setup command, database operation, test suite or release build was executed for this research.

### Generation receipt

- Component and selected starting point, or the documented absence of a full application generator
- Generator/toolchain versions, exact commands or IDE template/settings, working directory and generated destination
- Generated files retained, deliberate deviations with reasons, and required supplemental ignore rules
- Baseline checks and later checks actually run, results and remaining prerequisites or untested behavior

### Generator sources

- [Mix new project task](https://hexdocs.pm/mix/Mix.Tasks.New.html)
- [Mix local Hex installer](https://hexdocs.pm/mix/Mix.Tasks.Local.Hex.html)
- [Phoenix prerequisites and generator installation](https://hexdocs.pm/phoenix/installation.html)
- [Phoenix first application and generated setup](https://hexdocs.pm/phoenix/up_and_running.html)
- [Phoenix new project task and switches](https://hexdocs.pm/phoenix/Mix.Tasks.Phx.New.html)
- [Phoenix authentication generator](https://hexdocs.pm/phoenix/Mix.Tasks.Phx.Gen.Auth.html)
- [Phoenix LiveView resource generator](https://hexdocs.pm/phoenix/Mix.Tasks.Phx.Gen.Live.html)
- [Phoenix HTML resource generator](https://hexdocs.pm/phoenix/Mix.Tasks.Phx.Gen.Html.html)
- [Phoenix JSON resource generator](https://hexdocs.pm/phoenix/Mix.Tasks.Phx.Gen.Json.html)
- [Phoenix context generator](https://hexdocs.pm/phoenix/Mix.Tasks.Phx.Gen.Context.html)
- [Phoenix schema generator](https://hexdocs.pm/phoenix/Mix.Tasks.Phx.Gen.Schema.html)
- [Ecto migration generator](https://hexdocs.pm/ecto_sql/Mix.Tasks.Ecto.Gen.Migration.html)
- [Ecto migration behavior](https://hexdocs.pm/ecto_sql/Ecto.Migration.html)
- [Phoenix release generator](https://hexdocs.pm/phoenix/Mix.Tasks.Phx.Gen.Release.html)
- [usage_rules configuration and dependency guidance](https://hexdocs.pm/usage_rules/readme.html)
- [usage_rules synchronization task](https://hexdocs.pm/usage_rules/Mix.Tasks.UsageRules.Sync.html)
- [Oban persistence and installation overview](https://hexdocs.pm/oban/Oban.html)
- [PhoenixTest.Playwright setup and scope](https://hexdocs.pm/phoenix_test_playwright/readme.html)
- [Phoenix release deployment guide](https://hexdocs.pm/phoenix/releases.html)

## Tools

### Web application: Phoenix + its generated HTTP/asset defaults

Coherent routing, contexts and generated application structure.

Limits and integration: Phoenix is unnecessary for a CLI or a service without HTTP; preserve existing architecture.


- https://hexdocs.pm/phoenix/Mix.Tasks.Phx.New.html
- https://hexdocs.pm/phoenix/json_and_apis.html

Alternatives: Phoenix API-only; Plain supervised Mix application for non-web services

### Dependency documentation and agent guidance: usage_rules for selected dependency guidance

Discover dependency documentation and synchronize selected upstream usage rules for agents

Limits and integration: Development-only tool; inspect installed-version options and review generated content. Preserve Phoenix-generated guidance by default. An explicit README-only repository may configure file: "docs/dependency-rules.md" in mix.exs and link it from README; this destination is an optional project convention, not an upstream default.


- https://hexdocs.pm/usage_rules/readme.html
- https://hexdocs.pm/usage_rules/Mix.Tasks.UsageRules.Sync.html

Alternatives: Installed-version HexDocs and maintained repository guidance

### Browser UI: LiveView + HEEx components

Shared server-side business operations and interactive screens suit connected forms, portals and collaboration.

Limits and integration: Offline-first state, high-frequency local interactions and rich canvas editors can justify a dedicated client. LiveView does not remove HTML/CSS or all JavaScript.


- https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html
- https://hexdocs.pm/phoenix_live_view/js-interop.html
- https://hexdocs.pm/phoenix/json_and_apis.html

Alternatives: Server-rendered Phoenix HTML; JavaScript hooks for isolated client behavior; Separate TypeScript browser application over Phoenix APIs

### Shared relational persistence: Ecto + PostgreSQL

Explicit queries, changesets and database transactions fit shared application data.

Limits and integration: Changeset validation is not a replacement for database constraints or authorization; database operations and migrations need operational ownership. Current Ecto documentation deprecates Repo.transaction/2 in favor of Repo.transact/2. Follow the installed-version API and callback/result semantics; do not mechanically rename an existing transaction without tests.


- https://hexdocs.pm/ecto/Ecto.html
- https://hexdocs.pm/ecto/Ecto.Repo.html#c:transact/2

Alternatives: Another Ecto adapter when an actual persistence requirement warrants it

### Accounts and access control: phx.gen.auth + scoped context authorization

Generated first-party authentication keeps application-owned code; contexts authorize operations.

Limits and integration: Check permission both on mount/navigation and each operation. Test revoked access and reconnect behavior; magic-link delivery needs a configured mail provider.


- https://hexdocs.pm/phoenix/mix_phx_gen_auth.html
- https://hexdocs.pm/phoenix_live_view/security-model.html

Alternatives: External identity integration for SSO requirements

### Durable background work: Oban with the existing Ecto/PostgreSQL database

Persist jobs and enqueue alongside domain changes in one transaction.

Limits and integration: Task is only for explicitly disposable work and does not satisfy crash-durable delivery. Oban engine support and guarantees must be checked against the selected version; Redis is not a shipped Oban persistence engine. Oban Pro is an optional licensed extension, not a replacement for persistence.


- https://hexdocs.pm/oban/Oban.html
- https://hexdocs.pm/oban/testing.html

Alternatives: Another supported Oban SQL engine after engine-specific qualification; retain the existing datastore when it meets requirements

### Behavior and persistence tests: ExUnit + Ecto SQL Sandbox + LiveViewTest

Test contexts, data invariants, denied access and server-side UI behavior.

Limits and integration: LiveViewTest does not establish browser JavaScript, accessibility or visual correctness. Inline/manual job tests are not a production recovery simulation.


- https://hexdocs.pm/ex_unit/ExUnit.html
- https://hexdocs.pm/ecto_sql/Ecto.Adapters.SQL.Sandbox.html
- https://hexdocs.pm/phoenix_live_view/Phoenix.LiveViewTest.html
- https://hexdocs.pm/oban/testing.html

Alternatives: Oban.Testing when jobs exist

### Real-browser checks: PhoenixTest.Playwright for critical browser flows

Exercise hooks, navigation, reconnects and actual browser behavior omitted by server-side tests.

Limits and integration: Adds Node/package-manager/browser binaries and sandbox configuration; verify supported wrapper features. It is an editorial extension, not a Phoenix generator default.


- https://hexdocs.pm/phoenix_test_playwright/readme.html
- https://hexdocs.pm/phoenix_live_view/Phoenix.LiveViewTest.html

Alternatives: A separately maintained Playwright suite

### Code quality: Mix formatter and compiler warnings; Credo when selected

Fast local feedback plus consistency checks; select checks appropriate to project size.

Limits and integration: Static analysis does not prove domain correctness. Dialyxir adds analysis/PLT maintenance and is not a mandatory starter dependency.


- https://hexdocs.pm/credo/overview.html
- https://hexdocs.pm/dialyxir/readme.html

Alternatives: Dialyxir for additional success-typing analysis

### Security checks: Hex audit + Sobelow, alongside permission tests

Hex reports retired packages and known advisories; Sobelow finds common risky code patterns.

Limits and integration: Use the installed Hex version’s behavior. Scan findings need review; configure a non-zero Sobelow exit threshold and do not blanket-suppress findings. Neither proves the application secure.


- https://hexdocs.pm/hex/Mix.Tasks.Hex.Audit.html
- https://hexdocs.pm/sobelow/readme.html
- https://hexdocs.pm/phoenix_live_view/security-model.html

### Deployment: Mix release + runtime configuration

Package application and runtime with explicit migration/server entry points.

Limits and integration: Build for the target OS/architecture and native libraries. Host choice, secrets, migrations, TLS, backups, restore and rollback remain separate responsibilities.


- https://hexdocs.pm/phoenix/releases.html

Alternatives: Containerized release when the host benefits

### Native mobile client boundary: Platform-native clients consuming Phoenix APIs

Preserve native UI/platform ownership while sharing server-side domain operations.

Limits and integration: Do not advertise Elixir as a complete native mobile default: LiveView Native’s inspected README uses release-candidate dependencies and platform-specific clients. Validate target support, offline behavior, accessibility and signing independently.


- https://hexdocs.pm/phoenix/json_and_apis.html
- https://github.com/liveview-native/live_view_native

Alternatives: Evaluate LiveView Native separately for an explicitly suitable connected client

### Project instructions: README navigation + generated Phoenix agent guidance

Keep generated stack conventions available to coding agents

Limits and integration: Preserve maintained repository rules; --no-agents-md is an optional project choice, not the Phoenix default.


- https://hexdocs.pm/phoenix/Mix.Tasks.Phx.New.html

Alternatives: Preserve an existing compatible project choice

### Transactional email: Swoosh + selected provider adapter

Mailer adapters and test delivery fit generated Phoenix account flows

Limits and integration: Configure adapter/client dependencies and sender credentials; keep test/local adapters in development only. Use Oban for required queued delivery; a Task has no durable retry guarantee.


- https://hexdocs.pm/swoosh/Swoosh.html

Alternatives: Preserve an existing compatible project choice

### Uploads: LiveView uploads

Built-in upload configuration and consumption fit connected forms

Limits and integration: Configure allow_upload limits and authorize attachment association; persist consumed files before temp cleanup. External storage integration and content validation remain application work.


- https://hexdocs.pm/phoenix_live_view/uploads.html

Alternatives: Preserve an existing compatible project choice

### Realtime application events: Phoenix.PubSub

Local/distributed publication updates connected views and channels

Limits and integration: Supervise PubSub and subscribe to scoped topics; authorize each subscription/action and test reconnect. PubSub is transient broadcast, not durable replay or a message queue.


- https://hexdocs.pm/phoenix_pubsub/Phoenix.PubSub.html

Alternatives: Preserve an existing compatible project choice

## Architecture and developer workflow

Phoenix web modules call application contexts; Ecto supplies persistence boundaries. LiveView maintains connected server-side interaction, while Channels expose a client-facing realtime protocol. Recommendation: model domain operations through contexts and supervised responsibilities rather than translating every old controller, global singleton or database serialization bottleneck literally.

Version scope: Fetched documentation: Phoenix 1.8.15, LiveView 1.2.12, PubSub 2.4.1, Plug 1.20.3, Ecto 3.14.2 / Ecto SQL 3.14.0, Oban 2.24.1, Exq 0.25.0 and OTP 29.1.1 ETS. Installed dependency compatibility is unqualified; pin the actual application before using version-specific APIs.
Reviewed: 2026-10-11 | Evidence: documentation-reviewed | Source record: inputs/research/migrations-server.json

### Architecture boundaries

- Recommendation: contexts own business operations, Ecto Repo owns database access and explicit transactions join related writes. A single GenServer around all queries is an application choice, not a Phoenix requirement.
- Phoenix PubSub has a distributed-Elixir adapter and a Redis adapter. Redis can remain appropriate when deployment or interoperability requires it. Recommendation: identify the required delivery boundary before selecting the topology.
- Oban requires an Ecto-backed supported SQL engine. Its installation documents PostgreSQL, SQLite and MySQL; selecting PostgreSQL is this catalogue's target composition, not a universal Oban prerequisite. Recommendation: preserve durable external effects through idempotency and recovery checks.

### Tools and feedback

- For a disposable target, mix phx.new PATH generates a Phoenix application with selectable database and HTML/LiveView options. In an existing project, inspect mix.lock, generated modules and maintained conventions before regenerating anything.
- When manually installing the selected Oban version, adapt mix ecto.gen.migration add_oban_jobs_table and mix ecto.migrate from its installation guide; configure the engine, Repo and supervised Oban child. Do not copy PostgreSQL settings into a SQLite or MySQL target.
- Use mix test for application tests and the generated Phoenix connection/channel fixtures. Recommendation: add mixed-version payload, authorization and restart scenarios; a passing formatter or compiler does not establish those contracts.
- For a release build, adapt MIX_ENV=prod mix assets.deploy and mix release from the Phoenix deployment workflow; runtime.exs owns runtime configuration. Recommendation: verify database migrations, job supervision and cluster/PubSub connectivity separately from HTTP startup.

### Translations to avoid

- Avoid replacing a durable queue with spawned tasks or an in-memory notification list while calling the change equivalent. Recommendation: explicitly accept the changed crash and retry behavior or retain a persistent queue.
- Avoid treating Exq's Resque/Sidekiq-compatible transport format as proof that Ruby Active Job wrappers, classes and serializers execute in Elixir. The exact consumer and payload contract still needs qualification.
- Avoid assuming Plug cookies decode Rails cookies: Plug exposes its own serializer, salts and cryptographic options. Avoid relying only on HTTP plugs for LiveView authorization; mount and events require checks.
- Avoid using ETS as a shared session or global lock store. Tables are local to their node and normally disappear with their owner unless an heir takes ownership. Recommendation: reserve ETS for explicitly reconstructible local state.

### Architecture sources

- [Phoenix Intro to Contexts](https://hexdocs.pm/phoenix/contexts.html): Contexts separate web features from application operations.
- [mix phx.new](https://hexdocs.pm/phoenix/Mix.Tasks.Phx.New.html): Phoenix generator syntax and selectable target options.
- [Ecto.Multi](https://hexdocs.pm/ecto/Ecto.Multi.html): Composes related database operations within a transaction.
- [Ecto.Migrator](https://hexdocs.pm/ecto_sql/Ecto.Migrator.html): Migration execution, repository connection and release migration concerns.
- [Oban Installation](https://oban.hexdocs.pm/installation.html): PostgreSQL, SQLite and MySQL engine setup; migrations, configuration and supervision.
- [Oban API](https://oban.hexdocs.pm/Oban.html): Transactional Ecto.Multi insertion and queue pause/resume APIs; uniqueness is an enqueue feature.
- [Exq README](https://exq.hexdocs.pm/readme.html): Redis persistence, retrying and Resque/Sidekiq-format compatibility.
- [Sidekiq Job Format](https://github.com/sidekiq/sidekiq/wiki/Job-Format): Job envelopes and Active Job wrapper/version-sensitive payload details.
- [Sidekiq Best Practices](https://github.com/sidekiq/sidekiq/wiki/Best-Practices): Idempotent jobs and at-least-once execution.
- [Rails Active Job Basics](https://guides.rubyonrails.org/active_job_basics.html): Active Job serializers/GlobalID, adapter abstraction and scheduled/retry execution.
- [Rails Security](https://guides.rubyonrails.org/security.html): Rails cookie/session contract and rotation considerations.
- [Plug cookie session store](https://hexdocs.pm/plug/Plug.Session.COOKIE.html): Cookie serializer, signing/encryption configuration and rotating options.
- [LiveView Security](https://hexdocs.pm/phoenix_live_view/security-model.html): Authorization on mount/events and stateful connection revocation.
- [Phoenix Channels](https://hexdocs.pm/phoenix/channels.html): Channel protocol, joins and at-most-once non-persistent client delivery with application catch-up options.
- [Phoenix PubSub](https://hexdocs.pm/phoenix_pubsub/Phoenix.PubSub.html): Distributed-Elixir and Redis adapters, pool configuration and migration.
- [OTP ETS](https://www.erlang.org/doc/apps/stdlib/ets.html): Node-local tables, owner/heir lifetime and table options.
- [Phoenix Testing](https://hexdocs.pm/phoenix/testing.html): mix test and generated web test helpers.
- [Phoenix Deployment](https://hexdocs.pm/phoenix/deployment.html): Runtime configuration, assets.deploy, release and production build responsibilities.

## Transition options

Proposed designs and checks; these are not executed compatibility results.

### Data and schema

**Inspect the source:** Inventory schema, constraints, record identifiers and callbacks previously triggered by writes. Ecto schemas and changesets must preserve the intended domain semantics, not simply the old table shapes.

**During coexistence:** Recommendation: keep the source application as the authoritative writer while Phoenix contexts read fixtures; move a tenant or domain operation with one named writer. Use additive schema changes and a single migration runner during shared-table operation.

**Target design:** Contexts calling Ecto Repo with explicit validation and transaction boundaries. Ecto.Multi composes related Repo operations in one database transaction; cross-store side effects require a separate delivery design.

**Rollback:** Recommendation: return the domain writer to the source while preserving additive schema and reconciling accepted new writes; delay destructive contractions until the rollback window closes.

**Benefits and prerequisites**

- Recommendation: a context boundary can expose one reusable domain operation to LiveView, controllers and workers. Requires: Resource authorization, constraints and side effects moved with that operation. Tradeoffs: Shared-schema coexistence limits schema changes; external effects do not become part of a database transaction.

**Checks before transfer**

- Write a fixture through each allowed writer and read it from both runtimes; compare IDs, enum/null values, timestamps and constraint failures.
- Fail the second operation in an Ecto.Multi and verify the first database operation is absent; prove old readers still accept successful new writes.

- https://hexdocs.pm/phoenix/contexts.html
- https://hexdocs.pm/ecto/Ecto.Multi.html
- https://hexdocs.pm/ecto_sql/Ecto.Migrator.html

### Jobs and schedules: Retain Ruby workers behind an interface

**Inspect the source:** Rails workers currently own Ruby job execution, including Active Job/GlobalID serializers and backend retry/scheduling behavior. Record the actual Redis-backed backend and every backlog state rather than inferring it from the word Rails.

**During coexistence:** Recommendation, retain/wrap path: keep Ruby workers and their broker; expose a narrow producer endpoint or durable outbox relay for Phoenix. Ruby remains the only consumer and scheduler for retained categories, and the interface names payload version, business idempotency key and enqueue acknowledgement.

**Target design:** Phoenix web/domain code with retained Ruby worker ownership is a valid permanent composition when queue interoperability or Ruby libraries remain necessary.

**Rollback:** Recommendation: restore the old web producer while retaining the same workers; reconcile accepted interface/outbox entries before disabling the relay.

**Benefits and prerequisites**

- Recommendation: the web layer can transfer before job execution without transforming the old backlog. Requires: Defined producer interface, monitored delivery and retained worker deployment. Tradeoffs: Two runtimes and the broker remain operated; domain write plus broker enqueue is not a shared SQL transaction.

**Checks before transfer**

- Submit a captured serializer/GlobalID case through the interface and confirm the intended Ruby class executes with its normal failure policy.
- Interrupt delivery after domain commit; recover it without duplicating a business effect. Verify only the Ruby scheduler owns the retained category.

- https://guides.rubyonrails.org/active_job_basics.html
- https://github.com/sidekiq/sidekiq/wiki/Job-Format
- https://github.com/sidekiq/sidekiq/wiki/Best-Practices

### Jobs and schedules: Keep Redis and qualify Exq consumers

**Inspect the source:** A retained Redis broker may carry Sidekiq/Resque-shaped jobs; framework wrappers, class names, serializer tags and version-sensitive timestamps are still part of the execution contract.

**During coexistence:** Recommendation, broker-retaining replacement path: qualify Exq for selected job types on isolated queues. Keep unsupported Ruby types on Ruby consumers; map only deliberately supported payload versions, and give each category one consumer family and schedule owner.

**Target design:** Selected Elixir workers using Exq's documented Redis-backed Resque/Sidekiq-compatible format. This is a candidate for qualification, not a claim that arbitrary Active Job payloads are interoperable.

**Rollback:** Recommendation: stop new consumption and return only backward-readable queued work to Ruby; preserve both consumers for payloads accepted during the transition.

**Benefits and prerequisites**

- Recommendation: selected job execution can move to Elixir while preserving the broker boundary. Requires: Fixture-tested serialization, queue isolation, retry mapping and scheduler ownership. Tradeoffs: Redis remains; compatibility and unsupported Ruby argument types require explicit maintenance.

**Checks before transfer**

- Replay ordinary arguments, an Active Job wrapper, serializer edge cases and scheduled/retry payloads; reject unsupported cases without consuming them silently.
- Crash after a business effect before acknowledgement and verify replay safety; confirm old and new consumers never race for an unqualified category.

- https://exq.hexdocs.pm/readme.html
- https://github.com/sidekiq/sidekiq/wiki/Job-Format
- https://guides.rubyonrails.org/active_job_basics.html

### Jobs and schedules: Run Oban SQL workers alongside legacy queues

**Inspect the source:** Legacy Redis jobs and a proposed SQL queue have distinct payload/storage formats and retry/schedule state. A backend change does not copy the backlog or the recurring schedule.

**During coexistence:** Recommendation, SQL replacement path: run Oban alongside the legacy broker and route selected categories exclusively to one system. Keep old ready, retry, delayed, failed and running work accounted for. Transfer each schedule once; use a recoverable relay/outbox while domain data and queue insertion span stores.

**Target design:** Oban workers on the chosen supported SQL engine. With the same Repo/transaction, Oban.insert in Ecto.Multi can join domain changes; a separate database cannot gain that atomicity merely from both databases being SQL.

**Rollback:** Recommendation: pause new producers/consumption, keep accepted Oban payloads executable, and reconcile effects before moving routing back. Do not blindly copy all rows into the old broker.

**Benefits and prerequisites**

- Atomic domain-write-and-job-insert is available within a shared transaction. Requires: One supported database transaction/Repo for both writes and business idempotency for execution. Tradeoffs: Queue load shares the database; SQL atomic insertion does not guarantee exactly-once external effects.
- Recommendation: broker retirement can reduce the operated service inventory. Requires: All Redis uses transferred, all backlog states reconciled and recovery/rollback checks passed. Tradeoffs: Redis plus SQL coexistence temporarily adds operational work; no service reduction occurs while Redis remains needed.

**Checks before transfer**

- Rollback the combined transaction and confirm neither domain change nor executable Oban job remains.
- Pause a selected Oban queue, reconcile running work and inspect retained backlog; resume without duplicated effects.
- Restart during a job and validate the selected engine's configured recovery policy, including a failure after an external side effect.

- https://oban.hexdocs.pm/installation.html
- https://oban.hexdocs.pm/Oban.html
- https://hexdocs.pm/ecto/Ecto.Multi.html

### Identity and authorization

**Inspect the source:** Record old cookie encoding, serializer, keys/salts, expiration and session revocation; shared account IDs alone do not establish cookie compatibility. Plug COOKIE defaults its serializer to external_term_format and exposes rotating cryptographic options.

**During coexistence:** Recommendation: retain the existing identity authority through a qualified session exchange or compatibility decoder. Map authorization rules into Phoenix contexts and LiveView mount/events; keep account and revocation ownership explicit.

**Target design:** Phoenix identity with the selected session store and LiveView authorization in mount/on_mount and actions. Recommendation: choose planned reauthentication when cookie compatibility is not worth maintaining.

**Rollback:** Recommendation: retain the old decoder/exchange until routing can return; never reverse revocation merely to restore traffic.

**Benefits and prerequisites**

- Recommendation: users can preserve access while a connected feature moves. Requires: Qualified decoder/exchange, shared revocation and event-level authorization. Tradeoffs: Long-lived sockets need explicit disconnect/recheck behavior when access changes; sharing secrets alone is insufficient.

**Checks before transfer**

- Login through the old runtime, access the target feature, revoke the account/session and confirm HTTP plus existing/reconnected LiveView access follows the required policy.
- Send a forged delete event for another tenant despite a hidden UI control; confirm the server rejects it.

- https://hexdocs.pm/plug/Plug.Session.COOKIE.html
- https://hexdocs.pm/phoenix_live_view/security-model.html
- https://guides.rubyonrails.org/security.html

### Realtime transport

**Inspect the source:** Action Cable, Phoenix Channels and LiveView are different protocols. Capture subscription identity, event envelope, authorization, ordering and missed-message recovery. Channels documents at-most-once client delivery without server persistence.

**During coexistence:** Recommendation: retain old client endpoints and bridge versioned domain events into each renderer. A room/tenant cohort owns its subscriptions and reconnects. Choose Redis PubSub or a qualified distributed-Elixir cluster deliberately; sharing Redis does not translate the wire protocol.

**Target design:** LiveView for connected server-owned screens or Channels for explicit realtime clients, with durable domain state and an application catch-up mechanism when missed events matter.

**Rollback:** Recommendation: preserve the old endpoint/event envelope and cohort routing through reconnects; rebuild UI from persisted state instead of duplicating broadcasts.

**Benefits and prerequisites**

- Recommendation: connected UI and domain operations can share Phoenix contexts. Requires: Authorized subscriptions, working multi-node fanout and persisted state/cursors for recovery requirements. Tradeoffs: Live protocol/client changes and cluster operations remain; PubSub does not supply a durable user-message history.

**Checks before transfer**

- Place old/new subscribers on separate nodes; commit through either permitted path and verify every authorized recipient converges once.
- Disconnect before an event, restart a node, reconnect with the chosen cursor/state mechanism and verify missed domain changes recover; test revocation while connected.

- https://hexdocs.pm/phoenix/channels.html
- https://hexdocs.pm/phoenix_pubsub/Phoenix.PubSub.html
- https://hexdocs.pm/phoenix_live_view/security-model.html

### Caching and shared state

**Inspect the source:** Classify every Redis use as cache, session, limiter, lock, job or PubSub. ETS tables are node-local and their ownership lifetime matters; they do not provide Redis's cross-node boundary.

**During coexistence:** Recommendation: move only reconstructible cache entries into supervised local ownership, with explicit TTL/invalidation and bounded memory. Keep shared identity, coordination, queues and broadcast infrastructure until their own transitions qualify.

**Target design:** ETS for deliberately local reconstructed values, or a retained shared cache where consistency across nodes is required. Recommendation: state stale-read tolerance and rebuilding behavior in the application contract.

**Rollback:** Recommendation: switch those reads back to the qualified shared store or authoritative data; retain Redis until every remaining capability is reconciled.

**Benefits and prerequisites**

- Recommendation: a local cache can remove a remote dependency from selected reads. Requires: Acceptable node-local semantics, bounded memory and verified invalidation/rebuild behavior. Tradeoffs: Each node maintains separate contents; owner/node failure loses local state. Performance benefit requires measurement.

**Checks before transfer**

- Warm two nodes, update the authoritative record and verify their documented staleness/invalidation policy.
- Terminate the table owner or restart the node; verify the application rebuilds and no durable job/session/lock state was stored there.

- https://www.erlang.org/doc/apps/stdlib/ets.html
- https://hexdocs.pm/phoenix_pubsub/Phoenix.PubSub.html

### Delivery and recovery

**Inspect the source:** Record endpoint, worker, scheduler, Repo, assets and cluster/PubSub ownership. Phoenix runtime configuration, release build and schema migrations have distinct deployment steps.

**During coexistence:** Recommendation: maintain both releases with stable cohort routing and a single schedule/writer owner per responsibility. Monitor queue age, retry effects, node connectivity and authorization failures against application-specific promotion thresholds.

**Target design:** A Phoenix release with runtime.exs configuration, built assets, named migration runner and supervised workers. Recommendation: make cluster formation, backups and restore ordering explicit instead of assuming VM startup establishes them.

**Rollback:** Recommendation: retain the previous release and compatible database reads; return cohort routing and role ownership separately, reconciling new jobs and external effects.

**Benefits and prerequisites**

- Recommendation: explicit supervised roles and release inputs make restart behavior reviewable. Requires: Configured children, deployment inventory and exercised recovery procedures. Tradeoffs: Durable recovery still depends on the chosen databases/queues; supervision alone cannot recreate lost external state.

**Checks before transfer**

- Start the actual release with a disposable restored database and confirm assets, authenticated routes, a queued job and cross-node broadcast work.
- Stop a worker/node, observe detection and recovery, and verify no second schedule owner activates during rollback.

- https://hexdocs.pm/phoenix/deployment.html
- https://oban.hexdocs.pm/installation.html
- https://hexdocs.pm/phoenix_pubsub/Phoenix.PubSub.html

Rewrite workflow: /rewrite/guide.md
Shared contracts and phases: /rewrite/contracts.json


## Setup
1. Complete the selected starting point and baseline checks in the Generators section first; then continue with the integration steps appropriate to the chosen component.
2. After completing the selected starting point, read its generated README, mix.exs, mix.lock and runtime pins. Preserve the chosen plain Mix or Phoenix architecture; the following Phoenix integrations apply only when Phoenix is present.
3. For a Phoenix application, inspect and complete the generated setup alias after configuring development/test database access. Keep credentials outside committed secrets; follow the generator output when a selected omission means an alias or integration is unavailable.
4. If dependency guidance synchronization is useful, add usage_rules as a development dependency, choose the relevant dependency rules in mix.exs and review mix usage_rules.sync output. Preserve maintained generated guidance; an explicit README-only policy may configure a README-linked alternate file such as docs/dependency-rules.md.
5. If Phoenix browser accounts are required, complete the authentication follow-up recipe, review its generated instructions and configure transactional email delivery. Keep local/test delivery adapters in their intended environments; verify scopes and permission checks for application operations.
6. If durable background jobs are required, follow the installed Oban version’s installation and migration instructions, supervise Oban and configure bounded queues. Use supported persistence and idempotent workers; test retry and duplicate-effect handling. A Task is suitable only for explicitly disposable work.
7. Add development and test checks selected for this project. Formatter, compiler warnings and ExUnit apply to plain Mix applications; Ecto SQL Sandbox, LiveViewTest, Sobelow and other Phoenix-specific checks require their corresponding dependencies and application architecture.
8. For Phoenix applications that need real-browser verification, install/configure PhoenixTest.Playwright or the selected browser suite with its matching JavaScript dependency and browser binaries. Configure the test endpoint and SQL sandbox as documented; server-side LiveView tests do not establish browser JavaScript or visual correctness.
9. Run the applicable verification commands and actual application flows, fixing failures in place and retaining evidence. Skip tools whose dependency was not selected rather than claiming their checks passed; do not regenerate over existing work to hide failures.
10. For deployment qualification, select the intended host and runtime configuration. In Phoenix applications follow the release-helper recipe; build production assets only when the selected application has assets. Build a release compatible with the target OS, architecture and native dependencies.
11. Before claiming production readiness, rehearse startup, migrations and any applicable reconnect/job-retry behavior on the selected host. Establish secrets, TLS, backups, restore and rollback ownership; a generated release or passing local tests do not establish those outcomes.
12. Completion: record exact runtime/dependency versions, the application lockfile, selected generation/integration steps, check results and observed flows in README-linked evidence. State any untested deployment or native-mobile paths explicitly.

## Verification
Commands below require the selected tools and project configuration. Replace example paths, schemes and IDs; distinguish tests from builds and interactive startup. These are instructions, not recorded passes.

```text
mix hex.audit
mix format --check-formatted
mix compile --warnings-as-errors
mix test
mix credo --strict  # only after installing/configuring Credo
mix sobelow --strict --exit low  # only after installing/configuring Sobelow; review findings
mix dialyzer  # optional, after Dialyxir/PLT configuration
mix phx.server  # interactive smoke check, not an automated assertion
MIX_ENV=prod mix assets.deploy  # release qualification, after production prerequisites
MIX_ENV=prod mix release  # after release configuration; not deployment proof
```

## Open questions
- Does the product fit connected server-owned UI, or need a separate offline/native client?
- Which account/tenant permissions and email recovery requirements apply?
- Which work needs durable retries and duplicate-effect protection?
- Which host, object storage, observability and backup/restore requirements apply?

## Sources
- [Phoenix application generator](https://hexdocs.pm/phoenix/Mix.Tasks.Phx.New.html)
- [Phoenix LiveView](https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html)
- [LiveView JavaScript interoperability](https://hexdocs.pm/phoenix_live_view/js-interop.html)
- [Ecto](https://hexdocs.pm/ecto/Ecto.html)
- [Phoenix authentication generator](https://hexdocs.pm/phoenix/mix_phx_gen_auth.html)
- [LiveView security model](https://hexdocs.pm/phoenix_live_view/security-model.html)
- [Oban](https://hexdocs.pm/oban/Oban.html)
- [Oban testing](https://hexdocs.pm/oban/testing.html)
- [ExUnit](https://hexdocs.pm/ex_unit/ExUnit.html)
- [LiveViewTest](https://hexdocs.pm/phoenix_live_view/Phoenix.LiveViewTest.html)
- [Ecto SQL Sandbox](https://hexdocs.pm/ecto_sql/Ecto.Adapters.SQL.Sandbox.html)
- [PhoenixTest.Playwright](https://hexdocs.pm/phoenix_test_playwright/readme.html)
- [Credo](https://hexdocs.pm/credo/overview.html)
- [Dialyxir](https://hexdocs.pm/dialyxir/readme.html)
- [Sobelow](https://hexdocs.pm/sobelow/readme.html)
- [Hex dependency audit](https://hexdocs.pm/hex/Mix.Tasks.Hex.Audit.html)
- [Phoenix releases](https://hexdocs.pm/phoenix/releases.html)
- [Phoenix JSON and APIs](https://hexdocs.pm/phoenix/json_and_apis.html)
- [LiveView Native source README](https://github.com/liveview-native/live_view_native)
- [Swoosh](https://hexdocs.pm/swoosh/Swoosh.html)
- [LiveView uploads](https://hexdocs.pm/phoenix_live_view/uploads.html)
- [Phoenix PubSub](https://hexdocs.pm/phoenix_pubsub/Phoenix.PubSub.html)
- [usage_rules README](https://hexdocs.pm/usage_rules/readme.html)
- [usage_rules sync task](https://hexdocs.pm/usage_rules/Mix.Tasks.UsageRules.Sync.html)
- [Ecto current transaction API and semantics](https://hexdocs.pm/ecto/Ecto.Repo.html#c:transact/2)

## Extended Elixir reference
Imported from https://elixir.menu/; each dataset retains its own review date. Original editorial owner: elixir.menu.

### Foundation

Source reviewed: 2026-10-06

Database-backed web products built by individuals and small teams

One default per job. Add a dependency when its job exists. Revisit a choice when a concrete requirement warrants it.

Documentation-based recommendations; verify the selected dependencies together in your application.

#### Application

##### Web framework: Phoenix

Stage: Start here

Overview: Routes, controllers, HTML and application conventions in one place.

Why: Start with one Phoenix application and its generated structure. Keep the standard HTTP server and asset setup until a measured requirement calls for a change.

Setup: Use the official getting-started guide and a supported Elixir/OTP pair. Commit the resolved dependency lockfile.

Limits: Phoenix does not choose every application policy for you. This guide supplies the next layer of defaults; it does not replace Phoenix.

- [Phoenix getting started](https://hexdocs.pm/phoenix/up_and_running.html)

##### Interactive interfaces: Phoenix LiveView

Stage: Start here

Overview: Build forms, dashboards and live updates alongside your Elixir code.

Why: Use HEEx and function components for markup, with LiveView for interactive screens. Start ordinary content pages as server-rendered HTML when they need no live process.

Setup: Keep business rules in contexts; use LiveView for interaction and presentation.

Limits: Offline-first products, rich canvas editors and heavy local interaction can justify a dedicated client application. Add small JavaScript hooks for isolated browser behavior.

- [LiveView documentation](https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html)

##### Styling and components: Tailwind CSS + HEEx components

Stage: Start here

Overview: Own a small set of reusable components and the visual language around them.

Why: Use Tailwind for styling and HEEx function components to share markup and behavior. Keep theme tokens and application components in your project, where you can shape them around the product.

Setup: Define the product’s type, spacing and color rules, then build the components repeated across its screens.

Limits: Phoenix 1.8 includes daisyUI, but its generators do not require it. Keep daisyUI when its component classes and themes save useful work; it is optional, not the design system every product must adopt.

- [Phoenix 1.8 release](https://phoenixframework.org/blog/phoenix-1-8-released)
- [daisyUI customization](https://daisyui.com/docs/customize/)

##### Database and queries: PostgreSQL + Ecto

Stage: Start here

Overview: One durable store, explicit queries, changesets and migrations.

Why: Use Ecto for data access and changesets, backed by PostgreSQL. Database constraints enforce invariants; transactions keep related writes together.

Setup: Use Ecto.Multi for multi-step transactions. Inspect slow queries and their plans before adding caches.

Limits: Ecto is not Active Record: queries and persistence remain explicit. SQLite is reasonable for a genuinely embedded or single-file application, outside this web-product default.

- [Ecto documentation](https://hexdocs.pm/ecto/Ecto.html)
- [Ecto.Multi](https://hexdocs.pm/ecto/Ecto.Multi.html)

##### Business logic: Phoenix contexts

Stage: Start here

Overview: Plain Elixir modules around the language of your product.

Why: Give related business operations a clear public API. Both LiveViews and controllers should call that API instead of implementing separate versions of the same rules.

Setup: Define public operations around the application’s domain. Call those operations from controllers, LiveViews and workers; keep database access behind the context boundary.

Limits: A context is an organizational boundary, not a process. Do not turn ordinary CRUD or pure business logic into a GenServer.

- [Phoenix contexts](https://hexdocs.pm/phoenix/contexts.html)

#### Accounts and permissions

##### Accounts and sign-in: phx.gen.auth

Stage: When needed

Overview: Start with Phoenix’s generated authentication.

Why: Use the authentication generator for a first-party web application. Phoenix 1.8 includes magic-link authentication and sudo-mode conventions; the generated code lives in your application.

Setup: Read the generated code and current security guidance. Configure real email delivery before relying on magic links.

Limits: Authentication is not authorization. Enterprise SSO, external identity or complex organization requirements need their own deliberate integration.

- [Authentication generator](https://hexdocs.pm/phoenix/mix_phx_gen_auth.html)

##### Authorization: Scopes + context checks

Stage: When needed

Overview: Carry the actor into business operations and constrain data access.

Why: Pass the authenticated scope through context functions. Apply ownership and permission rules to reads and writes; test denied access as deliberately as the successful path.

Setup: Pass the current scope into context operations. Test that another user cannot read or modify the protected resource, including through direct context calls.

Limits: Scopes carry identity and context; they are not an automatic policy engine. Hidden buttons and client parameters are never sufficient access control.

- [Phoenix scopes](https://hexdocs.pm/phoenix/scopes.html)

#### Jobs and integrations

##### Durable background jobs: Oban

Stage: When needed

Overview: Retries and persistent jobs using the database you already run.

Why: Use Oban with PostgreSQL for work that must survive a process or application restart. Insert related jobs and domain changes within the same transaction.

Setup: Use separate queues for distinct workloads and monitor retries. An ordinary Task is suitable for disposable concurrent work, not a durable queue.

Limits: Jobs may be retried. Make side effects idempotent; uniqueness is not an exactly-once guarantee. Some advanced orchestration features belong to paid Oban Pro.

- [Oban documentation](https://hexdocs.pm/oban/Oban.html)

##### Recurring tasks: Oban Cron

Stage: When needed

Overview: Put scheduled work in the same queue as other durable jobs.

Why: Use Oban.Cron for periodic job insertion. Keep execution, retries and operational visibility in the job system.

Setup: Set the intended timezone, check daylight-saving behavior where applicable, and keep workers idempotent.

Limits: A schedule is not a catch-up policy for time when the app is down. Define missed-run behavior explicitly; dynamic scheduling has different requirements.

- [Oban.Cron](https://hexdocs.pm/oban/Oban.Cron.html)

##### Transactional email: Swoosh

Stage: When needed

Overview: Compose mail in Elixir and send through a delivery adapter.

Why: Use Swoosh, included in generated Phoenix applications, for account mail and product notifications. Use Oban when delivery needs durable retries.

Setup: Keep development mail local. Test message content and recipient selection before enabling production delivery.

Limits: Swoosh is a library, not an email delivery service. The provider, verified domain and deliverability setup are separate operational choices.

- [Swoosh documentation](https://hexdocs.pm/swoosh/Swoosh.html)

##### Outgoing HTTP: Req

Stage: When needed

Overview: A readable client for calling external APIs.

Why: Use Req for request construction, response handling and client features rather than assembling a new HTTP abstraction for each integration.

Setup: Wrap each external service behind a small module. Use Req.Test for deterministic request tests.

Limits: Timeouts, retries and error handling are part of the integration design. A retried payment or other side effect needs an idempotency strategy.

- [Req documentation](https://hexdocs.pm/req/Req.html)
- [Req.Test](https://hexdocs.pm/req/Req.Test.html)

##### Realtime notifications: Phoenix PubSub

Stage: When needed

Overview: Broadcast changes to connected parts of your application.

Why: Use Phoenix.PubSub to notify subscribed LiveViews or processes of a change. Persist important facts in PostgreSQL and load their current state when clients reconnect.

Setup: Use Presence only when you actually need to track who is connected.

Limits: PubSub is not a persistent message log. Multiple nodes require a suitable cluster or adapter configuration.

- [Phoenix.PubSub](https://hexdocs.pm/phoenix_pubsub/Phoenix.PubSub.html)

##### File uploads: LiveView uploads

Stage: When needed

Overview: Progress, validation and direct-to-cloud upload support.

Why: Start with LiveView’s upload flow. For durable production attachments, pair it with object storage and store ownership and file metadata in PostgreSQL.

Setup: Set size/type limits, authorize downloads, and implement the storage provider’s documented signing flow.

Limits: An upload widget does not supply permanent storage. Ephemeral application disks are not a durable attachment store; client metadata does not establish file safety.

- [LiveView uploads](https://hexdocs.pm/phoenix_live_view/uploads.html)

#### Queries and APIs

##### Product text search: PostgreSQL full-text search

Stage: When needed

Overview: Search your product’s data before operating another service.

Why: For ordinary application search, start with PostgreSQL text-search features and an appropriate index. Keep the query and ranking logic close to your data model.

Setup: Build representative search cases and inspect query plans; avoid claiming that an unindexed text scan will scale.

Limits: Advanced relevance, typo tolerance or specialist search scale can justify a dedicated engine. Evaluate against actual queries and user expectations.

- [PostgreSQL text search](https://www.postgresql.org/docs/current/textsearch-intro.html)

##### Filtering and pagination: Flop

Stage: When needed

Overview: Validated filter, sort and page parameters for Ecto queries.

Why: Use Flop when product lists need reusable sorting, filtering and pagination. Keep the allowed fields explicit and restrict the base query to authorized records first.

Setup: Use cursor pagination when the list and ordering warrant it; add Flop Phoenix only for the corresponding UI helpers.

Limits: For one simple bounded list, an explicit Ecto query may be enough. Pagination does not replace tenant or ownership checks.

- [Flop documentation](https://hexdocs.pm/flop/readme.html)

##### Local read caching: ETS

Stage: After measuring

Overview: Use the runtime’s in-memory tables for disposable cached data.

Why: First measure and improve database queries. When a local cache earns its keep, ETS provides concurrent in-memory storage without another service.

Setup: Define table ownership, expiry and invalidation. Shared durable state requires a different design.

Limits: ETS is node-local, loses data when its owner dies, and does not supply an automatic TTL or invalidation policy. It is never the source of truth.

- [ETS documentation](https://www.erlang.org/doc/apps/stdlib/ets.html)

##### JSON APIs: Phoenix controllers

Stage: When needed

Overview: Expose your existing contexts through explicit HTTP endpoints.

Why: Use Phoenix controllers and JSON rendering when a mobile client, partner or external integration needs an API. Share the business API with your web interface.

Setup: Define authentication, authorization, error shapes, pagination and versioning as part of the API contract.

Limits: Do not build an API simply to connect LiveView to its own server. Add GraphQL only when clients need that query model; Absinthe is the established Elixir option.

- [Phoenix JSON and APIs](https://hexdocs.pm/phoenix/json_and_apis.html)

#### Testing and deployment

##### Application tests: ExUnit + LiveViewTest

Stage: Start here

Overview: Test business behavior, persistence and server-driven interaction.

Why: Use ExUnit and Phoenix’s generated test setup. Test contexts with the database sandbox and interactive screens with Phoenix.LiveViewTest.

Setup: Prioritize permission boundaries, data invariants, job behavior and core user journeys.

Limits: Server-side LiveView tests do not execute browser JavaScript or prove the final visual layout. Avoid asserting incidental markup when behavior is the contract.

- [ExUnit](https://hexdocs.pm/ex_unit/ExUnit.html)
- [LiveViewTest](https://hexdocs.pm/phoenix_live_view/Phoenix.LiveViewTest.html)

##### Browser integration tests: PhoenixTest.Playwright

Stage: When needed

Overview: Exercise the small set of flows that need a real browser.

Why: Use the Playwright-backed PhoenixTest driver for JavaScript hooks, browser navigation and integrations that server-side tests cannot cover.

Setup: Cover representative critical flows and keep browser tests focused on observable behavior.

Limits: This adds browser tooling and setup cost. Keep most application tests in ExUnit; this is an editorial extension, not a Phoenix-generated default.

- [PhoenixTest.Playwright](https://hexdocs.pm/phoenix_test_playwright/readme.html)

##### Instrumentation: Telemetry + Logger

Stage: Start here

Overview: Expose timings, failures and structured operational events.

Why: Use Telemetry events and Logger as the instrumentation foundation. Track request latency, database time, job failures and the product operations that matter.

Setup: Make logs useful without exposing secrets. Establish alerts and retention before calling the production system operationally complete.

Limits: Instrumentation is not a hosted monitoring backend. Choose collection, storage and alerting separately; restrict any production LiveDashboard access.

- [Telemetry](https://hexdocs.pm/telemetry/readme.html)
- [Logger](https://hexdocs.pm/logger/Logger.html)

##### Deployment artifact: Mix releases

Stage: When shipping

Overview: Package the application and runtime in a repeatable release.

Why: Use Mix releases with runtime configuration. A container is a practical transport when the chosen host supports it; Phoenix documents the release and Dockerfile path.

Setup: Choose a host that fits the team. Rehearse migrations and restoration, and keep secrets out of the build artifact.

Limits: A release is not a hosting platform. Database backups, migrations, TLS, monitoring and rollback remain production responsibilities.

- [Phoenix releases](https://hexdocs.pm/phoenix/releases.html)

### Optional libraries

Source reviewed: 2026-10-11

Choose and configure each library against its installed-version documentation.

Select an optional tool only when the application's requirements match its use case. Explain the selection, check compatibility with the project's lockfile, and follow its installed-version documentation. Do not install the whole menu.

#### Accounts and product controls

##### Social login and OIDC: Assent

Use when: Users need to sign in with Google, GitHub, Apple or an OpenID Connect provider.

Usage: Integrate provider authentication with the application's existing accounts and sessions.

Limits: Account linking, session management and permissions remain application concerns. SAML is a separate requirement.

- [Assent](https://github.com/pow-auth/assent)

##### Rate limiting: Hammer

Use when: Login attempts, API calls, uploads or expensive actions need limits.

Usage: Define limits by actor, operation and time window; choose a backend that matches the deployment.

Limits: A node-local counter does not automatically enforce a cluster-wide quota. Choose the algorithm's burst behavior deliberately.

- [Hammer](https://hexdocs.pm/hammer/readme.html)

##### Feature flags: FunWithFlags

Use when: Features need gradual rollout, per-customer access or an operational off switch.

Usage: Choose an Ecto or Redis persistence adapter and configure synchronization between nodes.

Limits: Keep permission checks separate from rollout flags. Remove expired flags and restrict the management interface.

- [FunWithFlags](https://hexdocs.pm/fun_with_flags/readme.html)

#### Files and documents

##### Object storage: ExAws.S3

Use when: Uploads need to live in an S3 or compatible object store.

Usage: Use ExAws with its S3 service module for object operations and signed URLs. In a LiveView app, connect it to the upload flow.

Limits: The storage service, credentials, access rules and lifecycle policy are separate. Check which operations a compatible service actually supports.

- [ExAws.S3](https://hexdocs.pm/ex_aws_s3/ExAws.S3.html)

##### Image processing: Image

Use when: The product needs thumbnails, resized uploads, image conversion or watermarks.

Usage: Process images through the libvips-backed Image API; use Oban for work that needs retries.

Limits: Vix/libvips introduces native runtime requirements. Check the deployment target and required codecs, and limit input dimensions and processing work.

- [Image](https://hexdocs.pm/image/readme.html)

##### Markdown parsing and rendering: MDEx

Use when: The application needs CommonMark parsing, rendered Markdown content or transformations over a Markdown document tree.

Usage: Use MDEx to parse and transform a document or render HTML. Choose extensions and syntax highlighting deliberately; reserve HEEx components and expressions for trusted application-owned content.

Limits: Treat user-authored Markdown as untrusted input: configure and verify HTML sanitization, link handling and size limits. Never evaluate its HEEx expressions. MDEx uses native Rust code; verify precompiled artifact support or a Rust build toolchain for the deployment target.

- [MDEx](https://github.com/leandrocp/mdex)

##### PDF generation: ChromicPDF

Use when: Invoices, reports or other HTML documents need downloadable PDFs.

Usage: Render application-owned HTML and CSS through a managed Chrome process.

Limits: Chrome is an additional runtime dependency; PDF/A conversion also uses Ghostscript. Isolate rendering and control access to external resources.

- [ChromicPDF](https://hexdocs.pm/chromic_pdf/ChromicPDF.html)

##### CSV import and export: NimbleCSV

Use when: Users need bulk uploads, data exports or integrations through CSV files.

Usage: Parse and write streams; validate each imported row through the application's business rules.

Limits: CSV parsing does not validate field types or business rules. Define malformed-row handling and spreadsheet formula escaping for exports.

- [NimbleCSV](https://hexdocs.pm/nimble_csv/NimbleCSV.html)

#### APIs and collaboration

##### Documented HTTP APIs: OpenApiSpex

Use when: External consumers need an OpenAPI contract for the Phoenix API.

Usage: Describe operations and schemas, validate requests, and test responses against the specification.

Limits: A schema does not enforce ownership or authorization. Keep the published contract aligned with application behavior.

- [OpenApiSpex](https://hexdocs.pm/open_api_spex/readme.html)

##### GraphQL APIs: Absinthe

Use when: Clients specifically need GraphQL queries, mutations or subscriptions.

Usage: Expose the existing business layer through a schema; use Dataloader where batching is needed.

Limits: Resolvers still need authorization and query-cost limits. Ordinary JSON endpoints remain simpler when GraphQL adds no client benefit.

- [Absinthe](https://hexdocs.pm/absinthe/overview.html)

##### Who is online: Phoenix Presence

Use when: Chat, collaborative screens or live rooms need connected-user state.

Usage: Track presence metadata and broadcast joins and leaves through Phoenix's existing realtime infrastructure.

Limits: Presence is ephemeral and eventually consistent. It is not a durable audit trail, access-control system or editing-conflict resolver.

- [Phoenix Presence](https://hexdocs.pm/phoenix/Phoenix.Presence.html)

#### Languages, locales and money

##### Translated interface text: Gettext

Use when: The application needs interface copy in multiple languages.

Usage: Use the Gettext integration already present in typical Phoenix projects; maintain translation catalogs and plural forms.

Limits: It does not translate user-authored content automatically. Dates, amounts and units need locale-aware formatting too.

- [Gettext](https://hexdocs.pm/gettext/Gettext.html)

##### Localized dates and numbers: Localize

Use when: Dates, numbers, currencies and units must follow the user's locale.

Usage: Use CLDR-based formatting and parsing. For new projects, evaluate Localize as the documented successor to the ex_cldr family.

Limits: Existing ex_cldr applications need a planned migration. Check runtime requirements and package locale data for deployment.

- [Localize](https://hexdocs.pm/localize/readme.html)
- [ex_cldr migration notice](https://hexdocs.pm/ex_cldr/readme.html)

##### Currency amounts: Money (ex_money)

Use when: Prices, invoices or balances need explicit currencies and decimal arithmetic.

Usage: Represent amount and currency together and make rounding rules explicit.

Limits: This is not payment processing, tax calculation or an accounting ledger. The package is ex_money; check its major-version migration notes.

- [Money](https://hexdocs.pm/ex_money/readme.html)

#### AI features

##### Calling language models: ReqLLM

Use when: The product needs text generation, streaming, structured outputs, embeddings or model tool calls through supported provider APIs.

Usage: Use a common Elixir interface to supported providers, including schema-constrained output and embedding generation. Keep provider-specific settings explicit; store embeddings separately when retrieval needs persistence.

Limits: Provider and model capabilities differ. Start here for direct model calls; add an agent framework only when orchestration needs it. Define application validation, permissions and representative evaluations separately.

- [ReqLLM](https://github.com/agentjido/req_llm)

##### Tool-using AI agents: Jido.AI 2.x

Use when: A language model must select tools, keep agent state or run a bounded multistep reasoning loop.

Usage: Add Jido.AI to a Jido agent and use ReqLLM for provider access. Define tools as actions, and keep model selection, timeouts and tool policy explicit.

Limits: Model output is untrusted and nondeterministic. Restrict tool permissions and side effects, set cost and step limits, require approval for high-risk operations, and test representative tasks.

- [Jido.AI documentation](https://hexdocs.pm/jido_ai/readme.html)
- [Jido ecosystem](https://jido.run/ecosystem)

##### Validated structured extraction: InstructorLite

Use when: The main requirement is extracting typed fields from text into Ecto schemas, with casting, validation and retries.

Usage: Define an instruction with an Ecto schema and use changeset validation to check the returned fields. Choose this alternative when its Ecto integration fits better than ReqLLM structured output.

Limits: It is not an agent runtime and does not provide response streaming. Valid fields can still contain incorrect facts; handle failed validation, retry limits and domain checks explicitly.

- [InstructorLite](https://github.com/martosaur/instructor_lite)

##### Conversational chains and tool loops: LangChain for Elixir

Use when: The application is organized around message history, model responses and chained tool calls, or already uses the Elixir LangChain abstractions.

Usage: Compose messages, model adapters and tools through LLMChain. Use its callbacks for streaming and inspect tool-call trajectories when evaluating a conversation workflow.

Limits: This is an alternative orchestration approach, not an extra layer every ReqLLM or Jido application needs. Bound tool loops, authorize actions and implement persistence and retry behavior for the actual product.

- [LangChain for Elixir](https://github.com/brainlid/langchain)

##### AI features for Ash applications: Ash AI

Use when: An application already uses Ash resources and needs to expose selected actions as model tools or MCP tools, generate structured outputs or maintain embeddings.

Usage: Add Ash AI to the existing Ash domains and resources. Select the actions to expose and carry the authenticated actor and tenant into their execution; configure model access only for features that require it.

Limits: Choose Ash as an architecture first. Ash AI does not justify migrating an ordinary contexts application by itself. Test authorization for every exposed action and verify embedding updates, retrieval quality and model costs.

- [Ash AI](https://github.com/ash-project/ash_ai)

##### Vector similarity search: pgvector

Use when: Embeddings are useful for semantic retrieval or recommendations alongside existing PostgreSQL data.

Usage: Enable the PostgreSQL vector extension and use the Elixir pgvector integration with Ecto or Postgrex.

Limits: The library does not generate embeddings. Verify database-extension support, dimensions, indexes and retrieval quality against representative queries.

- [pgvector for Elixir](https://hexdocs.pm/pgvector/readme.html)

##### Running pretrained models: Bumblebee + Nx

Use when: Inference should run on infrastructure you control, using a supported pretrained model.

Usage: Load supported model architectures with Bumblebee and serve predictions through Nx.Serving.

Limits: Plan model memory, a suitable numerical backend and hardware. Model compatibility and licensing need to be checked individually.

- [Bumblebee](https://hexdocs.pm/bumblebee/Bumblebee.html)

#### Data processing and machine learning

##### Message ingestion pipelines: Broadway

Use when: The application consumes a stream from Kafka, RabbitMQ, SQS or another supported source.

Usage: Build concurrent processing stages with batching, acknowledgements and back-pressure.

Limits: The source connector determines delivery behavior. Keep handlers safe to retry; ordinary application jobs still fit Oban.

- [Broadway](https://hexdocs.pm/broadway/Broadway.html)

##### Tabular data analysis: Explorer

Use when: Imports, analytics or reports need dataframe transformations over CSV, Parquet or similar datasets.

Usage: Use typed series and dataframes for grouping, joining and transforming tabular data.

Limits: The default Polars backend uses native code. Check deployment support and memory use; routine application queries still belong in Ecto.

- [Explorer](https://hexdocs.pm/explorer/Explorer.html)

##### Building and training neural networks: Axon + Nx

Use when: The project needs to define or train a neural network in Elixir rather than only run a supported pretrained model.

Usage: Use Axon to build models and training loops on Nx, with a numerical compiler/backend suited to the target hardware. Use Bumblebee when loading a supported pretrained model meets the requirement.

Limits: Check native backend support, hardware, memory and training data. Validate on held-out data and measure deployment behavior; adding Axon does not establish model quality or a performance advantage.

- [Axon](https://github.com/elixir-nx/axon)

#### Performance and scaling

##### Custom demand-driven pipelines: GenStage

Use when: Producers and consumers need a custom event pipeline with demand-driven backpressure.

Usage: Model stages around runtime concurrency and data transfer; keep business steps in functions.

Limits: You own buffering, subscriptions and failure behavior. Use Task.async_stream for simpler bounded parallel work, or Broadway for its ingestion features.

- [GenStage](https://hexdocs.pm/gen_stage/GenStage.html)

##### Parallel dataset transformations: Flow

Use when: A large enumerable needs parallel mapping, partitioned grouping, aggregation or windows.

Usage: Build a Flow pipeline and choose partition keys, stages and windows for the workload.

Limits: Coordination has overhead; small inputs can favor Enum or Task. Partitioning affects grouping and order; bound accumulating state.

- [Flow](https://hexdocs.pm/flow/Flow.html)

##### Compare code performance: Benchee

Use when: A measured hot path has alternative implementations to compare.

Usage: Benchmark representative inputs with warmup, runtime, memory and reduction measurements.

Limits: Microbenchmarks do not establish application throughput or production latency. Check correctness and end-to-end behavior separately.

- [Benchee](https://hexdocs.pm/benchee/readme.html)

##### Locate runtime bottlenecks: Mix + OTP profilers

Use when: The application is slow and you need to locate expensive calls or repeated work.

Usage: Use the supported mix profile task or OTP profiler for the question; combine findings with the existing Telemetry events.

Limits: Check installed runtime support for tprof, eprof and fprof. Tracing can change timing and add overhead; profile a representative bounded workload.

- [Mix + OTP profilers](https://hexdocs.pm/mix/Mix.Tasks.Profile.Tprof.html)

##### Managed in-memory caching: Cachex

Use when: A node-local cache needs expiration, eviction or fallback loading beyond a small ETS implementation.

Usage: Configure cache limits, expiration and loading behavior around the data lifecycle.

Limits: Define invalidation and stale-data policy. A local cache is not a durable source of truth or a cluster-wide consistency guarantee.

- [Cachex](https://hexdocs.pm/cachex/Cachex.html)

##### Native computation and Rust integration: Rustler

Use when: Profiling identifies CPU-heavy work suited to native code, or the product must call an existing Rust library.

Usage: Expose a narrow NIF interface and select normal versus dirty scheduling appropriate to the work.

Limits: Native faults can crash the VM. Validate target builds, scheduler impact and boundary-copying costs; consider a separate OS process when fault isolation is required.

- [Rustler](https://hexdocs.pm/rustler/readme.html)

##### Compiled tensor computation: EXLA + Nx

Use when: Nx numerical work needs a compiled backend on supported CPU or accelerator hardware.

Usage: Use EXLA as the Nx compiler/backend and select the supported target, precision and memory settings.

Limits: Compilation, data transfer and native dependencies have costs. Verify hardware/toolchain support and measure representative workloads; it is not a general accelerator for arbitrary Elixir functions.

- [EXLA + Nx](https://hexdocs.pm/exla/EXLA.html)

##### Elastic remote execution: FLAME

Use when: Bursty expensive work should run on additional ephemeral nodes, such as media processing or model inference.

Usage: Configure a bounded runner pool and an appropriate backend. Start only required application children and size runner database pools deliberately.

Limits: Boot latency, network transfer and capacity costs matter. FLAME supplies compute execution, not a durable job queue; pair it with Oban when jobs must persist.

- [FLAME](https://hexdocs.pm/flame/FLAME.html)

#### Development tools

##### Module dependency rules: Boundary

Use when: Domains or layers need explicit, compiler-checked dependencies and public module exports. Useful for agent-maintained applications as well as human-maintained code.

Usage: Declare each boundary in its root module with use Boundary, explicit deps and a small exports list. Add the compile-time dependency and compiler below. A boundary always exports its root module; prefer explicit exports over exports: :all. Keep allowed calls aligned with the architecture.

Limits: Violations are compiler warnings unless compilation uses --warnings-as-errors. External OTP application calls are allowed by default; opt into selected app checks or strict mode when required. Dynamic calls such as apply/3 are not checked. Boundary enforces static module references; it does not isolate an agent’s files, processes or network access. Libraries can limit the compiler to dev/test as the compiler documentation describes.

- [Boundary reference](https://boundary.hexdocs.pm/Boundary.html)
- [Boundary installation](https://boundary.hexdocs.pm/readme.html)
- [Compiler and CI enforcement](https://boundary.hexdocs.pm/Mix.Tasks.Compile.Boundary.html)

##### AI-assisted Phoenix development: Tidewave

Use when: A coding agent needs runtime context from a Phoenix application during development.

Usage: Add the Tidewave Phoenix integration as a development-only dependency and plug. Connect your coding agent to inspect logs, evaluate code, query the development database and read installed-version documentation.

Limits: This gives the agent access to the running development application. Use a trusted local environment and keep the dependency and endpoint out of production; this is tooling for building the app, not an AI feature for its users.

- [Tidewave Phoenix](https://github.com/tidewave-ai/tidewave_phoenix)

#### A different application architecture

##### Declarative business applications: Ash

Use when: Resources, actions, policies and derived APIs form a substantial part of the application.

Usage: Evaluate Ash early as the domain layer beneath Phoenix, with only the extensions the product needs.

Limits: This changes how business logic is modeled. It is an architectural choice, not a small utility to install beside an unchanged contexts design.

- [What is Ash?](https://hexdocs.pm/ash/what-is-ash.html)

##### Stateful agent workflows: Jido 2.x

Use when: The application needs cooperating agents that choose or coordinate steps, share reusable actions and react to routed signals.

Usage: Model the system with agents, actions, signals and directives, and run long-lived agents through Jido's supervised runtime. AI is optional; add Jido.AI only when decisions need a language model.

Limits: Prefer a plain GenServer, durable Oban jobs or an explicit function pipeline when behavior is fixed and simple. Supervision and in-memory state alone do not preserve progress across restarts; choose and verify persistence and resume behavior.

- [Jido documentation](https://hexdocs.pm/jido/readme.html)
- [Jido ecosystem](https://jido.run/ecosystem)

#### Embedded devices and firmware: Nerves


#### Audio, video and streaming pipelines: Membrane


### OTP and performance

Source reviewed: 2026-10-06

Built-in Elixir and Erlang tools need no extra package. Follow the installed Elixir/OTP documentation; node-local memory and supervision do not provide durable storage.

Start with functions. Add processes for state ownership, concurrency or lifecycle. Choose shared storage by its read/write pattern; measure before changing the architecture.

#### Computation and process state

##### Ordinary computation: Functions + Enum

Use when: The work is business logic or a transformation that needs no independent lifecycle.

Limits: Keep it in functions. Adding a process adds messaging and coordination costs; it does not make a function faster.

- [Functions + Enum documentation](https://hexdocs.pm/elixir/Enum.html)

##### Lazy processing: Stream + File.stream!

Use when: A file or collection should be processed incrementally, without building every intermediate result in memory.

Limits: Streams are lazy: enumerate them to run the work. They are not parallel; collecting all results can still exhaust memory.

- [Stream + File.stream! documentation](https://hexdocs.pm/elixir/Stream.html)

##### One concurrent operation: Task

Use when: Short-lived work can run alongside its caller, such as fetching independent inputs.

Limits: Task.async links failures to the caller. Await the result and define timeout/cleanup behavior. Tasks do not survive node restarts as durable jobs.

- [Task documentation](https://hexdocs.pm/elixir/Task.html)

##### Supervised concurrent work: Task.Supervisor

Use when: Tasks need an application-owned supervisor or must fail independently of the requesting process.

Limits: async still links to the caller; choose async_nolink when isolation is required and handle results/exits. max_children rejects excess starts; it is not a waiting queue or a rate limiter.

- [Task.Supervisor documentation](https://hexdocs.pm/elixir/Task.Supervisor.html)

##### Bounded parallel batches: Task.async_stream

Use when: Independent items can be processed concurrently with a bounded number of tasks.

Limits: Enumerate the stream; set concurrency and timeout policy. ordered: false avoids buffering for input order when order is unnecessary. Task.Supervisor.async_stream_nolink adds supervised, unlinked task execution.

- [Task.async_stream documentation](https://hexdocs.pm/elixir/Task.html#async_stream/3)

##### Simple shared process state: Agent

Use when: One process needs to hold a small value accessed through get/update functions.

Limits: This is Elixir Agent, not an AI agent. Operations run serially inside its process. Choose GenServer for messages, timers or a richer lifecycle; ETS for concurrent table access.

- [Agent documentation](https://hexdocs.pm/elixir/Agent.html)

##### State and coordination: GenServer

Use when: A long-lived process owns state or coordinates a resource, for example a connection or session.

Limits: Callbacks execute serially. Keep slow work out of callbacks when responsiveness matters; call timeouts do not cancel server work. In-memory state needs a separate persistence strategy.

- [GenServer documentation](https://hexdocs.pm/elixir/GenServer.html)

##### Explicit runtime transitions: :gen_statem

Use when: A protocol or connection has distinct states, state-specific events and transition/timeout rules.

Limits: Use functions or a data model for ordinary business statuses. The behaviour models a running process; supervision does not make its state durable.

- [:gen_statem documentation](https://www.erlang.org/doc/apps/stdlib/gen_statem.html)

#### Lifecycle, naming and coordination

##### Application lifecycle: Application + Supervisor

Use when: Long-running children must start in order and recover according to their dependencies.

Limits: Choose restart and shutdown policies deliberately. Restarts do not restore lost state, and terminate callbacks are not a durability guarantee. Slow child initialization delays later children.

- [Application + Supervisor documentation](https://hexdocs.pm/elixir/Supervisor.html)

##### Workers created at runtime: DynamicSupervisor

Use when: The application starts and stops workers as demand changes, such as one worker per active room.

Limits: Use Registry for discovery. A restarted supervisor does not remember the former dynamic child set; reconcile it from an authoritative source when required.

- [DynamicSupervisor documentation](https://hexdocs.pm/elixir/DynamicSupervisor.html)

##### Find local processes: Registry

Use when: Processes need names based on runtime keys, such as tenant/session IDs, or local duplicate-key dispatch.

Limits: Use :via tuples rather than creating atoms from user input. Registry is node-local; it is neither cluster discovery nor durable storage.

- [Registry documentation](https://hexdocs.pm/elixir/Registry.html)

##### Reduce supervisor contention: PartitionSupervisor

Use when: Measurements show one process, such as a DynamicSupervisor or Task.Supervisor, bottlenecking concurrent starts.

Limits: Route work across partitioned children. This reduces contention in that layer; it does not parallelize a single worker or distribute work across nodes.

- [PartitionSupervisor documentation](https://hexdocs.pm/elixir/PartitionSupervisor.html)

##### Observe failure and schedule messages: Process monitors + timers

Use when: A process must observe another process exiting or receive a delayed message.

Limits: Monitors report DOWN without coupling failures; links couple lifecycles. Process.send_after schedules a message, not a durable job. Account for stale timer messages and mailbox growth.

- [Process monitors + timers documentation](https://hexdocs.pm/elixir/Process.html)

##### Inspect a running process: :sys + Process.info

Use when: A running server has unexpected state, memory growth or a growing mailbox.

Limits: Use :sys for OTP process state and bounded debugging; Process.info reports process memory and queue length. Inspecting full state can expose sensitive values and allocate large results. These tools diagnose behavior; they do not repair it.

- [OTP sys](https://www.erlang.org/doc/apps/stdlib/sys.html)
- [Process.info](https://hexdocs.pm/elixir/Process.html#info/2)

#### Shared data and hot paths

##### Mutable shared tables: :ets

Use when: Many processes need concurrent lookups or updates to node-local in-memory data.

Limits: Choose table type, ownership and access rights. Tune read/write concurrency against measurements. The table normally dies with its owner; TTL, invalidation and durability are separate.

- [:ets documentation](https://www.erlang.org/doc/apps/stdlib/ets.html)

##### Read-mostly shared values: :persistent_term

Use when: Many processes repeatedly read a value that changes rarely, such as a static lookup or a stable resource reference. A stable :counters reference can be stored once while the counter array itself is updated.

Limits: Reads avoid locks and copying the value onto the caller heap. Writes copy the key table; replacing/deleting complex terms triggers a node-wide GC scan. Avoid request-time updates and expiring caches. Persistent means VM lifetime, not disk durability.

- [:persistent_term documentation](https://www.erlang.org/doc/apps/erts/persistent_term.html)

##### Frequent shared increments: :counters

Use when: Many processes update numeric metrics without routing each increment through one server.

Limits: write_concurrency favors add/sub throughput with weaker read consistency. Choose atomics mode when those semantics do not fit. Fixed-width integers wrap; this is node-local memory, not an accounting ledger.

- [:counters documentation](https://www.erlang.org/doc/apps/erts/counters.html)

##### Atomic numeric coordination: :atomics

Use when: An integer operation needs an atomic result or compare-and-exchange, such as claiming a numeric slot.

Limits: Individual operations are atomic and mutually ordered. A sequence of operations is not a transaction. Integers wrap on overflow, and these values are not cluster-wide.

- [:atomics documentation](https://www.erlang.org/doc/apps/erts/atomics.html)

##### FIFO data structure: :queue

Use when: A process holds a FIFO buffer and repeated list appends would be costly.

Limits: A queue is a data structure, not a worker, backpressure mechanism or persistent job system. Bound its size and define overload behavior.

- [:queue documentation](https://www.erlang.org/doc/apps/stdlib/queue.html)

##### Build output from fragments: iodata

Use when: Output combines many byte fragments and its destination accepts iodata.

Limits: Keep binaries and byte lists nested until a binary is required. Avoid repeated copying; benchmark the actual construction because BEAM binary appends can also be optimized.

- [iodata documentation](https://hexdocs.pm/elixir/IO.html#module-io-data)

##### Control retained binary memory: :binary

Use when: Small slices of large payloads live in process state or another long-lived store.

Limits: Inspect referenced_byte_size. Copy selected retained slices when they pin a much larger binary; copying every binary adds allocation and work.

- [:binary documentation](https://www.erlang.org/doc/apps/stdlib/binary.html)

- {'title': 'Choose durability separately', 'body': 'Use Task for disposable work and Oban for application jobs that need persistence and retries. GenStage and Broadway regulate ingestion; source acknowledgements and retry-safe handlers determine delivery behavior.', 'sources': [['Oban', 'https://hexdocs.pm/oban/Oban.html']]}
- {'title': 'Measure the limiting resource', 'body': 'Track latency, throughput, memory, mailbox growth, database queries and pool waits on representative traffic. Extra tasks can overload a database or an upstream API. Use Benchee for code comparisons and profilers to find where work accumulates.', 'sources': [['Benchee', 'https://hexdocs.pm/benchee/readme.html'], ['OTP profiling', 'https://www.erlang.org/doc/apps/tools/tprof.html']]}
- {'title': 'Stream database exports deliberately', 'body': 'Use Ecto.Repo.stream for incremental row processing when the adapter supports it. SQL adapters require enumeration inside a transaction. Long streams occupy a database connection; batching and collecting results can change memory use.', 'sources': [['Ecto.Repo.stream', 'https://hexdocs.pm/ecto/Ecto.Repo.html#c:stream/2']]}
### Other Elixir starting points

Source reviewed: 2026-10-11

#### Command-line tool

Developer tools, local automation and terminal applications.

Foundation: Mix + OptionParser

Starting command: `mix new my_tool`

Keep command parsing separate from the modules that perform the work. OptionParser handles flags; the application owns help text, subcommands, output and exit codes.

Limits: An escript needs Erlang/OTP on the target machine. Evaluate Burrito when distributing a bundled executable to users without that runtime, and test each supported OS and architecture.

- [Mix projects](https://hexdocs.pm/mix/Mix.Tasks.New.html)
- [OptionParser](https://hexdocs.pm/elixir/OptionParser.html)
- [Escript packaging](https://hexdocs.pm/mix/Mix.Tasks.Escript.Build.html)
- [Burrito](https://hexdocs.pm/burrito/readme.html)

#### Library

Reusable modules used by other Elixir applications.

Foundation: Mix

Starting command: `mix new my_library`

Define a small public module API, examples and tests. Generate documentation with ExDoc; publish to Hex if the package is intended for reuse outside the project. Add a supervision tree only if the library owns long-lived processes.

Limits: Choose supported Elixir/OTP versions and dependency constraints for consumers. A library does not need an HTTP server or database unless that is its purpose.

- [Mix projects](https://hexdocs.pm/mix/Mix.Tasks.New.html)
- [ExDoc](https://hexdocs.pm/ex_doc/readme.html)
- [Publishing to Hex](https://hexdocs.pm/hex/Mix.Tasks.Hex.Publish.html)

#### Background service

Workers, integrations and processes that keep running.

Foundation: Mix + OTP supervision

Starting command: `mix new my_service --sup`

Use supervision for process lifecycles and recovery. Keep calculations and business operations in ordinary modules; introduce stateful processes where they are needed.

Limits: Supervision does not persist work. Choose durable storage or a queue when recovery requires it. Add Plug + Bandit for a small HTTP interface if needed; use Mix releases for deployment.

- [Supervision](https://hexdocs.pm/elixir/Supervisor.html)
- [Bandit](https://hexdocs.pm/bandit/Bandit.html)
- [Mix releases](https://hexdocs.pm/mix/Mix.Tasks.Release.html)

#### Web application or API

Browser products, customer portals and HTTP APIs.

Foundation: Phoenix

Starting command: `mix phx.new my_web_app`

Use Phoenix for routing, controllers and web application conventions. Add LiveView for server-driven interactive screens; an API-only product does not need a browser UI.

Limits: Choose persistence from the product's needs. PostgreSQL + Ecto is our recommendation for shared relational web data, not a prerequisite for every Elixir program. Review generator options for API-only or database-free applications.

- [Phoenix generator options](https://hexdocs.pm/phoenix/Mix.Tasks.Phx.New.html)
- [Phoenix application guide](https://elixir.menu/#stack)
- [Phoenix setup recipe](https://elixir.menu/setup.md)

#### Data analysis or machine learning

Notebooks, data transformations and numerical models.

Foundation: Livebook; Mix for the application

Use Livebook for interactive exploration, Explorer for tabular data, and Nx for numerical computation. Add Axon when defining or training neural networks is the requirement. Move reusable work into a Mix application when it needs a maintained API, tests or a service lifecycle.

Limits: Hosted model calls, local inference and training are different requirements. Check native backends, memory and hardware before selecting a deployment environment.

- [Livebook](https://hexdocs.pm/livebook/readme.html)
- [Nx](https://hexdocs.pm/nx/Nx.html)
- [Explorer](https://hexdocs.pm/explorer/Explorer.html)
- [Axon](https://github.com/elixir-nx/axon)

#### Embedded device

Hardware products, sensors and deployed Linux devices.

Foundation: Nerves

Start from the Nerves installation and project guides for the target hardware. Build firmware with the system and libraries that the device requires.

Limits: Hardware support, firmware updates and access to the device determine the setup. A web interface can be added when useful; it does not define the device application.

- [Nerves getting started](https://hexdocs.pm/nerves/getting-started.html)

#### Audio or video system

Streaming, transcoding and realtime media processing.

Foundation: Membrane + an OTP application

Build media pipelines with the source, processing and output elements needed for the product. Phoenix may provide a separate control interface if there is a web UI.

Limits: Protocols, codecs and native dependencies determine the pipeline and deployment. Ordinary file uploads do not require a media framework.

- [Membrane](https://membrane.stream/)

#### Decisions

- {"title": "Choose the interface", "body": "A CLI, reusable library, running service and web application have different starting points. Keep reusable business operations independent of the interface."}
- {"title": "Choose persistence when needed", "body": "Files can suit local configuration. SQLite can suit local relational data; PostgreSQL can suit a shared database. Ecto can be used independently of Phoenix. Disposable caches and process state are separate decisions."}
- {"title": "Choose the deployment target", "body": "A developer script, downloadable executable, deployed service and firmware image need different packaging. Decide which runtimes and native libraries can be present on the target."}
#### Agent steps

- {"title": "Read the existing project", "body": "First read https://elixir.menu/agents.md for direct Markdown and JSON retrieval. In the application, start with README.md, mix.exs, mix.lock and runtime pins. Preserve its architecture and follow its maintained workflow. Do not regenerate an existing project."}
- {"title": "State the application requirements", "body": "Identify the interface, whether work must keep running, persistence needs, and deployment target. Choose one of the starting points above; a product may combine more than one. Do not assume Phoenix or PostgreSQL."}
- {"title": "Check the environment", "body": "Check elixir --version and mix --version. Follow the official Elixir installation guide if prerequisites are missing; respect existing version management. Install a web generator, database or specialist toolchain only for the selected path."}
- {"title": "Generate in an empty destination", "body": "Use the selected starter and its current documentation. The commands above are scaffolding examples, not complete applications. For the Phoenix web path, follow setup.md; for Nerves and Membrane, follow their own project guides."}
- {"title": "Select libraries by requirement", "body": "Read runtime.md for built-in state, concurrency and storage choices. Read optional.md and add only tools whose use cases match the product. Check versions, native dependencies and deployment constraints. Record the reasons and setup in the project’s maintained documentation. Preserve its existing agent-guidance conventions."}
- {"title": "Verify the actual application", "body": "Run formatting, compilation and relevant tests. Exercise the real interface: CLI help, output and exit codes; service startup and recovery; HTTP behavior; or the target device. Verify the packaged artifact on the intended target and report what remains untested."}
#### Shared checks

- title
- body
- sources
#### Dependency guidance for agents

Use usage_rules in any Mix project to collect dependency-authored instructions and find documentation. Follow the project’s existing conventions for where agents read guidance, keep Phoenix’s generated guidance when using its default setup, and refresh dependency rules when versions change.

[usage_rules documentation](https://hexdocs.pm/usage_rules/readme.html)

Keep the project README current and link the selected guidance; preserve existing project instructions.
