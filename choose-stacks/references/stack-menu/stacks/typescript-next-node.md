# Next.js

React interfaces with server rendering, routes and application logic.

Language: TypeScript | Reviewed: 2026-10-10 | Evidence: documentation-reviewed research input

Source record: menu/inputs/research/typescript.json.

Core guidance checked: 2026-10-13. Review sources are listed below. /research-freshness.json describes the imported research packet; this record retains its own evidence scope. These recipes and selected dependency combinations need qualification in the actual project.

## Application role
Components: web, api
UI: full
Deployment: node

## Use cases
- Authenticated web products
- Server-rendered React interfaces
- Browser applications with owned APIs and relational data

## Fit
- Shared TypeScript contracts and React UI are useful
- Server rendering or a web-facing backend is required
- Team accepts explicit server/client and cache boundaries

## Choose something else when
- Only static editorial content is required
- Existing API already owns all backend responsibilities and SSR is unnecessary
- Native mobile or desktop UI is the deliverable

## Agent workflow
- Read README, dependency manifests, lockfiles, runtime pins and the maintained project workflow before changing anything. Preserve an existing stack unless reconsidering it is part of the request.
- For a new component, read the Generators section before writing application files. Use its appropriate official initializer and retain its generated baseline; follow-up generators are conditional on the selected feature.
- Use this guide to select tools by requirement. Resolve compatible versions from official and installed-version documentation; record the actual lockfile and runtime versions.
- Create a plan for schema changes, identity, authorization, external effects and deployment. A library choice does not complete its integration.
- Run relevant checks after configuration. Exercise the real interface, failure paths and packaged artifact on the intended target. Report commands, versions, results and untested behavior.
- On failure, retain the command and diagnostic, fix the failing prerequisite and resume there. Do not regenerate over existing work or suppress failures to make a check green.

## Best practices
- Keep database imports and secrets in server-only modules. Treat Server Actions and route handlers as authenticated entry points.
- Validate external input with schemas and authorize access close to the data. A page redirect is not an access-control boundary.
- Commit reviewed SQL migrations. Generate the Better Auth schema into Drizzle's migration path.
- Test async Server Components through browser journeys. Exercise logged-out and two-tenant cases, including cached pages.

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

#### create-next-app

Use when: A new full-stack React/Next.js application; do not rerun over an existing application.

1. Select a supported Node LTS and the repository package manager. Inspect the current CLI help before generation; examples below use npm.
2. Run the official scaffolder in the parent directory. Review its current prompts for styling, Cache Components, agent instructions and optional feedback instead of accepting saved preferences blindly; use --reset-preferences if you need to clear saved choices.
3. Record resolved generator/runtime/framework versions and chosen options in the root README; retain the lockfile.

Working directory: A local source-workspace parent outside synchronized storage; my-app must not already exist

Check the selected runtime.

```sh
node --version
```

Working directory: A local source-workspace parent outside synchronized storage; my-app must not already exist

Inspect the currently resolved scaffolder options.

```sh
npx create-next-app@latest --help
```

Working directory: A local source-workspace parent outside synchronized storage; my-app must not already exist

Generate the TypeScript App Router baseline while leaving styling, cache, instruction and feedback preferences available for interactive selection.

```sh
npx create-next-app@latest my-app --ts --eslint --app --src-dir --use-npm --disable-git
```

- Replace my-app with the intended unused project name. @latest is a scaffold-time lookup; record the resolved version and use locked dependencies afterward.
- The CLI's recommended defaults currently include TypeScript, ESLint, Tailwind CSS, App Router, Cache Components, AGENTS.md and agent feedback; customize these for the actual project. Cache Components are a framework behavior choice, not a required scaffold feature. Tailwind is the default styling option, but choose it only if it fits the product's styling approach.
- The agent-instructions option is project-local. If the repository owner requires README-only guidance, pass --no-agents-md and, for Next versions supporting it, set agentRules: false in next.config before next dev so Next does not create/update its managed AGENTS.md block. Do not impose this repository-specific choice on all users or projects.
- Agent feedback is optional and separate from agentRules. It prepares anonymized Next.js issue-report drafts for owner review; opening the review form does not send or publish them. Keep it off unless the project owner wants this review flow and understands its telemetry requirement.
- Do not handwrite package.json, tsconfig, framework config or ignore rules as a replacement for this scaffold.

### Conditional follow-up generators

#### Drizzle migration generation

Use when: Only after this application has selected PostgreSQL/Drizzle, installed compatible drizzle-orm/driver/drizzle-kit dependencies, and configured a schema and drizzle.config.ts.


Working directory: The generated my-app directory

Generate SQL migration files from the configured schema changes.

```sh
npx drizzle-kit generate
```

Working directory: The generated my-app directory

Apply reviewed migrations to the configured development database after checking its connection.

```sh
npx drizzle-kit migrate
```

- Inspect local drizzle-kit help first; do not install a second ORM merely to run these examples. Review SQL and migration metadata before applying; production application needs its own release procedure.
- Next.js has no general built-in model/controller/component generator analogous to Rails. Follow its installed-version route/file conventions; do not invent a next generate command.

### Preserve the generated foundation

- Generated ignore rules, package scripts, strict TypeScript configuration, Next configuration, application/layout conventions and lockfile; document intentional changes.
- Generated README setup information, supplemented with project purpose/navigation; honor repository instruction ownership and record the chosen local agent-rule/feedback behavior.

### Baseline and generation checks

- Run generated development server and inspect a real route in a browser.
- Run the generated build and lint scripts separately; Next build is not a lint check. Check generated script names rather than assuming next lint exists.
- Verify intended generated files and documented deviations; a successful scaffold does not prove authentication, authorization or database integration.

### Generation receipt

- Component and selected starting point, or the documented absence of a full application generator
- Generator/toolchain versions, exact commands or IDE template/settings, working directory and generated destination
- Generated files retained, deliberate deviations with reasons, and required supplemental ignore rules
- Baseline checks and later checks actually run, results and remaining prerequisites or untested behavior

### Generator sources

- [Next.js managed agent rules and disabling generated instruction blocks](https://nextjs.org/docs/app/api-reference/config/next-config-js/agentRules)
- [Next.js agent feedback draft/review flow and telemetry behavior](https://nextjs.org/docs/app/api-reference/config/next-config-js/agentFeedback)
- [create-next-app CLI](https://nextjs.org/docs/app/api-reference/cli/create-next-app)
- [Next.js installation and runtime requirements](https://nextjs.org/docs/app/getting-started/installation)
- [Drizzle Kit generate](https://orm.drizzle.team/docs/drizzle-kit-generate)
- [Drizzle Kit migrate](https://orm.drizzle.team/docs/drizzle-kit-migrate)
- [Next.js agentRules configuration and README-only opt-out](https://nextjs.org/docs/app/api-reference/config/next-config-js/agentRules)
- [Better Auth installation and schema CLI](https://better-auth.com/docs/installation)
- [Better Auth Drizzle adapter package and schema generation](https://better-auth.com/docs/adapters/drizzle)

## Tools

Current correction reviewed 2026-10-23: TanStack Start 1.0 became stable on 13 October 2026; the imported 10 October RC observation is historical. Consider Start when its typed routing and server-function model fit the project, after checking the selected adapter and integrations. Web UI is not native UI; no framework supplies business correctness.
Evidence: documentation-reviewed; no TanStack Start application integration executed
- [TanStack Start 1.0 is stable](https://tanstack.com/blog/tanstack-start-1-0)
- [TanStack Start overview](https://tanstack.com/start/latest/docs/framework/react/overview)


### runtime and dependency management: Node LTS + npm lockfile

LTS production policy and reproducible dependency install

Limits and integration: Pin resolved runtime/dependencies; latest is a scaffold-time lookup, not a CI dependency strategy


- https://nodejs.org/en/about/previous-releases
- https://nextjs.org/docs/app/getting-started/installation

Alternatives: Preserve existing pnpm; Bun after compatibility validation

### application framework: Next.js App Router + React + strict TypeScript

Full-stack React with version-matched agent documentation

Limits and integration: TanStack Start 1.0 became stable on 13 October 2026; the imported 10 October RC observation is historical. Consider Start when its typed routing and server-function model fit the project, after checking the selected adapter and integrations. Web UI is not native UI; no framework supplies business correctness.


- https://nextjs.org/docs/app/getting-started/installation
- https://nextjs.org/docs/app/guides/ai-agents
- https://vite.dev/guide/
- https://tanstack.com/start/latest
- https://docs.astro.build/en/guides/typescript/
- https://tanstack.com/blog/tanstack-start-1-0
- https://tanstack.com/start/latest/docs/framework/react/overview

Alternatives: React/Vite for API-backed SPA; TanStack Start for typed route loaders/server functions; Astro for editorial sites

### project instructions: README navigation + generated version-matched agent guidance

Keep repository instructions and installed framework documentation discoverable

Limits and integration: Honor existing instruction ownership. Optional README-only policy: scaffold with --no-agents-md and set agentRules:false before next dev; neither is required by this stack.


- https://nextjs.org/docs/app/api-reference/cli/create-next-app
- https://nextjs.org/docs/app/api-reference/config/next-config-js/agentRules
- https://nextjs.org/docs/app/guides/ai-agents

Alternatives: README-only workflow when the repository explicitly chooses it

### Agent runtime inspection: Next.js development MCP endpoint with real browser inspection

Combine version-matched framework context, compilation errors, routes and runtime logs with the actual rendered application.

Limits and integration: Development only. Inspect the installed Next.js and next-devtools-mcp versions before configuring tools. Some runtime inspection requires an open browser session; Turbopack compilation tools have their own constraints. Framework tools do not replace authorization tests or real browser verification. Do not install optional skills or enable automatic upgrades merely to read this reference.


- https://nextjs.org/docs/app/guides/mcp
- https://nextjs.org/docs/app/guides/ai-agents

Alternatives: Existing development logs and browser tooling when MCP is unavailable

Setup: Follow the installed-version MCP guide to connect a selected agent client to the existing dev server; keep the endpoint and development credentials private. Use the project-selected browser verification route.

### validation: Zod

Runtime schemas with inferred TypeScript types

Limits and integration: Validate requests/environment/external results; shape checks do not establish permission or truth


- https://zod.dev/

Alternatives: Existing compatible runtime schema library

### database and migrations: PostgreSQL + Drizzle + reviewed SQL migrations

Typed schema with inspectable SQL history

Limits and integration: Configure schema paths and target environment; apply migration once; rehearse fresh DB and forward compatibility


- https://orm.drizzle.team/docs/get-started-postgresql
- https://orm.drizzle.team/docs/migrations

Alternatives: Existing database/ORM conventions

### identity: Better Auth + Drizzle PostgreSQL adapter

Integrated session/provider support without designing password/session primitives

Limits and integration: Auth schema generate then Drizzle migrations; direct Better Auth migrate is Kysely-only; configure origin/secrets/recovery; authorize near data


- https://better-auth.com/docs/installation
- https://better-auth.com/docs/integrations/next
- https://nextjs.org/docs/app/guides/authentication

Alternatives: Existing identity provider or auth library matching requirements

### background work: Inngest durable workflows when required

Checkpointed steps, retries and waits

Limits and integration: Idempotent effects and authorized approvals required; use outbox for DB/event consistency; avoid beta durable endpoints as default


- https://www.inngest.com/docs/durable-execution
- https://www.inngest.com/docs/durable-execution/quick-start
- https://www.inngest.com/docs/durable-execution/concepts

Alternatives: Omit for request-local work; Existing durable queue/workflow service

### Static typing: TypeScript strict

Independent deterministic checks for generated edits

Limits and integration: Next build does not run lint; never ignore build/type errors to satisfy a check


- https://nextjs.org/docs/app/getting-started/installation
- https://nextjs.org/docs/app/api-reference/cli/next

Alternatives: Preserve an existing TypeScript configuration after checking its guarantees

### Linting: ESLint

Independent deterministic checks for generated edits

Limits and integration: Next build does not run lint; never ignore build/type errors to satisfy a check


- https://nextjs.org/docs/app/getting-started/installation
- https://nextjs.org/docs/app/api-reference/cli/next

Alternatives: Biome when project has selected it

### Domain tests: Vitest

Run isolated domain behavior checks with a configured test environment

Limits and integration: Install/configure Vitest and DOM environment for UI tests. Next async Server Components require browser/integration coverage instead.


- https://vitest.dev/guide/

Alternatives: Existing suitable test suite

### Component tests: React Testing Library

Test rendered components through user-visible DOM behavior

Limits and integration: Install @testing-library/react and its @testing-library/dom peer; configure the test runner/DOM environment. This is a component utility library, not a test runner.


- https://testing-library.com/docs/react-testing-library/intro/

Alternatives: Existing suitable test suite

### Browser tests: Playwright

Exercise critical journeys in actual browser engines

Limits and integration: Install @playwright/test and matching browsers; configure an isolated test server/data and test session expiry, routing and authorization failures.


- https://playwright.dev/docs/intro

Alternatives: Existing suitable test suite

### deploy: Project-selected Node or Docker host

Documented full Next feature support with Node/Docker

Limits and integration: Adapters vary; verify chosen host, secrets, DB connections, sessions, migrations and restore; Cloudflare needs separate compatibility review


- https://nextjs.org/docs/app/getting-started/deploying

Alternatives: Verified adapter; Static export for compatible static subset

### Server state cache: TanStack Query for client-owned remote state

Queries, mutations and invalidation support interactive API screens

Limits and integration: Install @tanstack/react-query and provide QueryClient. Define tenant-aware keys, staleTime/retry policy and clear session data on sign-out; in Next prefer server loading until a client cache has a job.


- https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults

Alternatives: Next server loading for server-owned data; Router loaders for simple route data

### Forms: React Hook Form for complex client forms

Separates client form state and validation from page components

Limits and integration: Install react-hook-form only where needed; wire existing runtime schemas deliberately. Render accessible labels/errors; validate and authorize submissions on the server.


- https://github.com/react-hook-form/react-hook-form

Alternatives: Native HTML forms for simple submissions

### Styling: Tailwind CSS when utility styling fits the project

Reusable styling without a runtime component dependency

Limits and integration: For Vite install tailwindcss and @tailwindcss/vite, add the plugin and CSS import. Use the framework-specific installation path for Next; retain established styles when present.


- https://tailwindcss.com/docs/installation/using-vite

Alternatives: CSS Modules or existing CSS design system

### Accessible UI primitives: Radix Primitives for complex controls

Provides focus and keyboard behavior for common interaction patterns

Limits and integration: Install only used components. Authors still supply names, contrast and meaningful composition; verify keyboard and assistive-technology behavior.


- https://www.radix-ui.com/primitives/docs/overview/accessibility

Alternatives: Semantic native HTML controls

### Accessibility checks: axe-core through Playwright + manual keyboard review

Automated audits identify common accessibility defects in real pages

Limits and integration: Install @axe-core/playwright; scan representative states and use a screen reader/keyboard. Passing automated rules is not complete accessibility evidence.


- https://playwright.dev/docs/accessibility-testing

Alternatives: Preserve an existing compatible project choice

### Transactional email: Nodemailer with project-selected SMTP provider

SMTP transport avoids coupling email templates to a hosting vendor

Limits and integration: Install nodemailer; configure server-only transport, verified sender and TLS. Test locally, queue required delivery, handle ambiguous results and bounces; SMTP acceptance is not inbox delivery. Verify the resolved Nodemailer release supports the pinned Node runtime and preserves TLS certificate validation.


- https://github.com/nodemailer/nodemailer

Alternatives: Provider-supported SDK when API-specific features are required

### Uploads and object storage: AWS SDK for JavaScript v3 S3 client

Object storage separates durable files from ephemeral application disks

Limits and integration: Install @aws-sdk/client-s3; authorize object keys, restrict size/type and configure lifecycle. Keep credentials server-side; add presigner only for direct uploads and validate provider compatibility.


- https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/javascript_s3_code_examples.html

Alternatives: Preserve an existing compatible project choice

### Live server updates: EventSource for one-way server events

Browser-standard streaming suits status/progress feeds

Limits and integration: Backend owns authenticated stream and event IDs. Test reconnect, replay and proxy buffering; EventSource is one-way and its constructor offers no arbitrary authorization-header option. Confirm long-lived connection support on host.


- https://html.spec.whatwg.org/multipage/server-sent-events.html

Alternatives: WebSocket service for bidirectional collaboration; Polling for infrequent updates

## Architecture and developer workflow

A Next application contains server rendering and browser interactivity with an explicit trust boundary. Recommendation: preserve an existing backend's domain ownership during UI adoption; for a new owned backend use server-only data access. Node/Docker and alternative adapters require separate runtime checks.

Version scope: Documentation reviewed 11 October 2026: current Next.js App Router docs label 16.4.0. Pin the installed Next, React, Node and database packages; distinguish cacheComponents:true from the previous caching model. This profile does not qualify a lockfile or hosting adapter.
Reviewed: 2026-10-11 | Evidence: documentation-reviewed | Source record: inputs/research/migrations-clients.json

### Architecture boundaries

- Server Components load server-owned data; Client Components own interaction and browser APIs. Keep the client boundary near interactive leaves and pass minimal serializable DTOs.
- Recommendation: one domain writer and migration owner per responsibility. Existing REST/GraphQL services remain authoritative during coexistence; a new server-only DAL can own validation, authorization and transactions after transfer.
- Choose server, browser and CDN caches deliberately. Session-dependent output, invalidation and multiple instances require independent policies; adding a framework cache does not migrate a shared session or queue.
- Recommendation: durable jobs and realtime run behind explicit service contracts when required. A render, Server Action or browser promise is not an execution backlog.

### Tools and feedback

- Start in the external source checkout. Read README and inspect package.json, lockfile, next.config, current API ownership, schema and runtime. Record whether Cache Components are enabled before selecting examples.
- For an existing npm project run npm ci; use its scripts. With Next installed, npx next typegen then npx tsc --noEmit checks generated route types and TypeScript. Run the configured ESLint/Biome command separately; the build is not a substitute for lint.
- Run npm run dev for iteration and npm run build for production compilation; use npm run start only if its script runs the selected production server. Configure Playwright's isolated backend/data first, then npx playwright test for mixed-version journeys.
- Recommendation: deploy the same built artifact to all instances, record build/deployment identifiers, cache coordination, migrations, secrets and adapter support. Reproduce cold/warm loads, sign-out, old-tab actions and rollback on a staging topology.

### Translations to avoid

- Marking the root tree use client brings imported dependencies into the browser bundle and broadens the secret/exposure surface.
- Passing whole ORM records to Client Components exposes fields unrelated to presentation; enforce authorization and DTO filtering on the server.
- UI-hidden buttons or Proxy redirects cannot replace authorization at the mutation/data boundary.
- Copying pre-16 cache defaults into a Cache Components app silently changes freshness behavior; identify the installed model.
- Treating an old browser build as gone after deployment ignores existing tabs, prefetched payloads and action identifiers.

### Architecture sources

- [Next.js Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components): Pages/layouts default to server components; browser interaction and APIs require client boundaries.
- [Next.js Data Security](https://nextjs.org/docs/app/guides/data-security): Existing HTTP APIs or a new server-only DAL provide explicit data ownership; mutations require validation/authorization and minimal DTOs.
- [Next.js Authentication](https://nextjs.org/docs/app/guides/authentication): Authentication, session management and authorization are separate responsibilities; optimistic redirects do not replace secure checks.
- [Next.js Caching with Cache Components](https://nextjs.org/docs/app/getting-started/caching): Current caching guide applies when cacheComponents is enabled.
- [Next.js Caching and Revalidating (Previous Model)](https://nextjs.org/docs/app/guides/caching-without-cache-components): The alternative caching guide applies without Cache Components; defaults and APIs must match that model.
- [Next.js Self-Hosting](https://nextjs.org/docs/app/guides/self-hosting): Multi-instance cache coordination, action encryption keys, deployment identifiers and old-client version skew need deployment design.
- [Next.js Installation](https://nextjs.org/docs/app/getting-started/installation): Framework setup and deterministic lint/type/build checks have separate tooling.
- [Next.js CLI](https://nextjs.org/docs/app/api-reference/cli/next): next typegen, build and production server commands are qualified by installed framework and scripts.
- [Inngest Durable Execution](https://www.inngest.com/docs/durable-execution): Completed steps are checkpointed and workflows can retry/resume; durable endpoints are separately marked beta.

## Transition options

Proposed designs and checks; these are not executed compatibility results.

### Data and schema

**Inspect the source:** Existing REST/GraphQL behavior, DTOs, authorization, transactions and one schema owner.

**During coexistence:** Recommendation: Adopt server-rendered routes that call the old API; keep its writer and migration authority. Compare read-only fixtures without replaying real side effects.

**Target design:** Recommendation: Retain the API permanently if appropriate, or transfer a bounded domain to a server-only DAL with minimal DTOs after mixed-version checks.

**Rollback:** Route the cohort back while old-compatible schema remains; reconcile writes before any writer reversal.

**Benefits and prerequisites**

- Server loading can reduce client waterfalls; an owned DAL centralizes authorization. Requires: Server-reachable API or reviewed database ownership; measurable user journeys. Tradeoffs: A new domain writer requires schema/transaction review; framework adoption alone changes neither.

**Checks before transfer**

- Old and new UI decode identical success/error/empty fixtures.
- Forged resource IDs remain denied on both mutation paths.
- An acknowledged write is readable through the old interface.

- https://nextjs.org/docs/app/guides/data-security
- https://nextjs.org/docs/app/getting-started/server-and-client-components

### Identity and authorization

**Inspect the source:** Existing session issuer, cookie/token format, expiry, revocation, tenant membership and CSRF behavior.

**During coexistence:** Recommendation: Retain the issuer behind an adapter and authorize data/mutations in both implementations; inventory origin/domain/cookie differences before sharing.

**Target design:** Recommendation: Use an explicitly selected issuer and server-side authorization boundary; transfer session contracts or require a controlled sign-in when compatibility cannot be preserved.

**Rollback:** Restore old routes/issuer acceptance only while its keys and session semantics remain supported; do not resurrect revoked sessions.

**Benefits and prerequisites**

- One identity authority can support gradual UI/backend replacement. Requires: Validated issuer integration and old/new expiry/revocation fixtures. Tradeoffs: Session sharing is format/security work; sign-in continuity is not guaranteed by using cookies.

**Checks before transfer**

- Revoked and expired sessions fail in old/new paths.
- Cross-tenant direct action requests are denied.
- Sign-out clears browser remote-state caches and back navigation reveals no protected data.

- https://nextjs.org/docs/app/guides/authentication
- https://nextjs.org/docs/app/guides/data-security

### Caching and shared state

**Inspect the source:** Actual enabled caching model, personalized response policy, keys, freshness, invalidation and shared-instance behavior.

**During coexistence:** Recommendation: Keep the prior policy while converting one route/data category; separate old/new cache namespaces and observe stale/account-crossing outcomes.

**Target design:** Recommendation: Choose Cache Components or version-matched previous-model APIs explicitly; keep user-specific data outside shared public entries and coordinate shared invalidation when deployed across instances.

**Rollback:** Disable the new cache path and purge its namespace; keep source data unchanged and retain old invalidation until transfer completes.

**Benefits and prerequisites**

- Repeated eligible work can be reused without refetching each time. Requires: A documented freshness tolerance, safe keys and working invalidation. Tradeoffs: Coordination/storage adds operations; freshness and cost gains require measurement.

**Checks before transfer**

- A write refreshes affected reads through every serving instance.
- Account A cannot read cached output for account B.
- Cold, warm and forced-refresh responses agree with the selected policy.

- https://nextjs.org/docs/app/getting-started/caching
- https://nextjs.org/docs/app/guides/caching-without-cache-components
- https://nextjs.org/docs/app/guides/self-hosting

### Jobs and schedules

**Inspect the source:** Existing job producer/consumer payloads, ready/scheduled/retry/failed/in-flight states and external-effect idempotency.

**During coexistence:** Recommendation: Keep existing workers; move a named job type behind a versioned event contract. Reconcile backlog and retain one consumer owner per item.

**Target design:** Recommendation: Use selected durable execution such as Inngest for required workflows; a transactional outbox is a proposed design when domain commit and event submission are separate systems.

**Rollback:** Stop new producers for the transferred type, account for active runs and resume old workers with compatible payloads; reconcile irreversible effects first.

**Benefits and prerequisites**

- Checkpointed completed steps allow retry/resume without starting every step again. Requires: Selected service/SDK integration, stable step IDs, replay-safe external effects and delivery reconciliation. Tradeoffs: Operating a workflow service adds dependency/cost; checkpoints do not supply business exactly-once effects.

**Checks before transfer**

- Crash after an external effect but before step acknowledgement; retry causes one intended business effect.
- Domain commit with event-send failure is eventually reconciled.
- Old scheduled/retry work is drained or deliberately transformed.

- https://www.inngest.com/docs/durable-execution

### Delivery and recovery

**Inspect the source:** Current hosting/runtime, static assets, open-tab state, prefetched payloads and Server Function compatibility.

**During coexistence:** Recommendation: Keep old assets and compatible API routes; promote one built artifact per deployment and rehearse an old tab against the new deployment.

**Target design:** Recommendation: Use version-matched deploymentId support and infrastructure routing as needed; same-build instances share required action keys and cache coordination.

**Rollback:** Restore the prior artifact and routing while compatible assets/data remain; do not claim traffic rollback reverses schema or external effects.

**Benefits and prerequisites**

- Explicit rollout handling reduces missing-chunk/navigation mismatches. Requires: A qualified host, retained assets and tested old-client behavior. Tradeoffs: Hard navigation can lose component state; same encryption key does not make old action IDs compatible.

**Checks before transfer**

- Open an old tab, deploy, navigate and submit an old form; observe success or a controlled update path.
- Preserved drafts survive any required full reload.
- All instances serve matching build/deployment identifiers.

- https://nextjs.org/docs/app/guides/self-hosting

Rewrite workflow: /rewrite/guide.md
Shared contracts and phases: /rewrite/contracts.json


## Setup
1. Complete the selected starting point and baseline checks in the Generators section first; then continue with the integration steps appropriate to the chosen component.
2. From the generated project root, extend README with purpose, commands, environment variable names and links to the installed framework documentation. Confirm strict TypeScript and honor the selected instruction-file policy; README-only repositories need agentRules:false before next dev.
3. Install only selected integrations: Zod for runtime validation; drizzle-orm plus pg and development drizzle-kit/@types/pg when PostgreSQL/Drizzle is required; Better Auth and its installed-version Drizzle adapter only when application-owned identity is selected. The current adapter guide uses @better-auth/drizzle-adapter. Mark database/auth modules server-only; add dotenv only if the chosen config loader needs it.
4. When database/auth features are selected, configure the Drizzle schema/config and ignored development DATABASE_URL, then auth secret/base URL and Next route/client integration. For Better Auth with Drizzle, inspect the compatible auth CLI, run npx auth@latest generate, include generated schema in Drizzle paths, then follow the reviewed SQL generation/application procedure. Better Auth direct migrate is for its Kysely adapter, not the Drizzle path.
5. Configure tests appropriate to the application: Vitest and a DOM environment/React Testing Library for synchronous client components or domain logic, plus Playwright for critical browser flows and async Server Components. Install matching browser binaries with npx playwright install only after selecting Playwright. Add required aliases/plugins and a production-build webServer configuration.
6. Test invalid inputs, resource/tenant ownership and session boundaries where applicable. Add Inngest only for required durable workflows; configure its endpoint/worker and exercise retries and duplicate events.
7. For database-backed applications, rehearse migrations on a fresh test database. Run the generated build, separate lint/type checks and selected tests. Configure the chosen host, secrets and a single migration job; verify deployed browser/session behavior and rollback compatibility as part of an authorized release.

## Verification
Commands below require the selected tools and project configuration. Replace example paths, schemes and IDs; distinguish tests from builds and interactive startup. These are instructions, not recorded passes.

```text
npm ci
npx next typegen
npx tsc --noEmit
npx eslint .
npx vitest run
npm run build
npx playwright test
```

## Open questions
- Does the product require server-rendered routes, client-owned state, or both?
- Which identity providers, account recovery and SSO requirements must be supported?
- Which host, database connection budget and migration/restore process will own production?
- Which workflows need retries, email, object storage or persistent realtime connections?

## Sources
- [Node.js release policy](https://nodejs.org/en/about/previous-releases)
- [Next.js installation](https://nextjs.org/docs/app/getting-started/installation)
- [create-next-app CLI](https://nextjs.org/docs/app/api-reference/cli/create-next-app)
- [Next.js agentRules](https://nextjs.org/docs/app/api-reference/config/next-config-js/agentRules)
- [Next.js AI coding agents](https://nextjs.org/docs/app/guides/ai-agents)
- [Next.js CLI](https://nextjs.org/docs/app/api-reference/cli/next)
- [Next.js deployment](https://nextjs.org/docs/app/getting-started/deploying)
- [Vite getting started](https://vite.dev/guide/)
- [TanStack Start](https://tanstack.com/start/latest)
- [Astro TypeScript](https://docs.astro.build/en/guides/typescript/)
- [Zod](https://zod.dev/)
- [Drizzle PostgreSQL](https://orm.drizzle.team/docs/get-started-postgresql)
- [Drizzle migrations](https://orm.drizzle.team/docs/migrations)
- [Better Auth installation](https://better-auth.com/docs/installation)
- [Better Auth Next.js integration](https://better-auth.com/docs/integrations/next)
- [Next.js authentication](https://nextjs.org/docs/app/guides/authentication)
- [Inngest durable execution](https://www.inngest.com/docs/durable-execution)
- [Inngest quickstart](https://www.inngest.com/docs/durable-execution/quick-start)
- [Inngest concepts](https://www.inngest.com/docs/durable-execution/concepts)
- [Next.js Vitest](https://nextjs.org/docs/app/guides/testing/vitest)
- [Next.js Playwright](https://nextjs.org/docs/app/guides/testing/playwright)
- [TanStack Query important defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults)
- [React Hook Form repository](https://github.com/react-hook-form/react-hook-form)
- [Tailwind Vite installation](https://tailwindcss.com/docs/installation/using-vite)
- [Radix accessibility](https://www.radix-ui.com/primitives/docs/overview/accessibility)
- [Playwright accessibility testing](https://playwright.dev/docs/accessibility-testing)
- [Nodemailer maintainer repository](https://github.com/nodemailer/nodemailer)
- [AWS JavaScript S3 examples](https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/javascript_s3_code_examples.html)
- [HTML EventSource standard](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [Vitest guide](https://vitest.dev/guide/)
- [Playwright installation](https://playwright.dev/docs/intro)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Next.js development MCP and runtime tools](https://nextjs.org/docs/app/guides/mcp)

Keep the project README current and link the selected guidance; preserve existing project instructions.
