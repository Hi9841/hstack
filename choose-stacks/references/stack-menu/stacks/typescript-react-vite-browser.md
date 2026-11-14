# React + Vite

An interactive browser app connected to an existing or separate API.

Language: TypeScript | Reviewed: 2026-10-10 | Evidence: documentation-reviewed research input

Source record: menu/inputs/research/typescript.json.

Core guidance checked: 2026-10-13. Review sources are listed below. /research-freshness.json describes the imported research packet; this record retains its own evidence scope. These recipes and selected dependency combinations need qualification in the actual project.

## Application role
Components: web
UI: client
Deployment: static

## Use cases
- Interactive dashboards
- API-backed browser tools
- Client-rendered applications

## Fit
- Backend/identity already have owners
- SSR is not a product requirement
- Browser UI and API can be deployed independently

## Choose something else when
- Searchable server-rendered content is central
- The task requires native device UI
- Team expects the frontend scaffold to supply backend auth or persistence

## Agent workflow
- Read README, dependency manifests, lockfiles, runtime pins and the maintained project workflow before changing anything. Preserve an existing stack unless reconsidering it is part of the request.
- For a new component, read the Generators section before writing application files. Use its appropriate official initializer and retain its generated baseline; follow-up generators are conditional on the selected feature.
- Use this guide to select tools by requirement. Resolve compatible versions from official and installed-version documentation; record the actual lockfile and runtime versions.
- Create a plan for schema changes, identity, authorization, external effects and deployment. A library choice does not complete its integration.
- Run relevant checks after configuration. Exercise the real interface, failure paths and packaged artifact on the intended target. Report commands, versions, results and untested behavior.
- On failure, retain the command and diagnostic, fix the failing prerequisite and resume there. Do not regenerate over existing work or suppress failures to make a check green.

## Best practices
- Keep credentials, SQL access and authorization behind the API. Browser validation does not establish permission.
- Keep strict TypeScript and validate API responses where data crosses trust boundaries.
- Choose a router and server-state cache only when navigation and data complexity need them.
- Test production asset paths and direct navigation to nested routes. Offline use needs explicit storage, synchronization and conflict rules.

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

#### create-vite React TypeScript template

Use when: A new browser React application backed by an existing or separately owned API.

1. Choose a supported Node runtime and package manager; inspect create-vite help and template requirements.
2. Create in an unused local source directory with the official react-ts template, then install dependencies inside the generated project.
3. Record generator/runtime versions and template choice in README; use the generated lockfile for subsequent installs.

Working directory: A local source-workspace parent outside synchronized storage; my-app must not already exist

Check Node against the resolved Vite/template requirements.

```sh
node --version
```

Working directory: A local source-workspace parent outside synchronized storage; my-app must not already exist

Inspect current create-vite flags.

```sh
npm create vite@latest -- --help
```

Working directory: A local source-workspace parent outside synchronized storage; my-app must not already exist

Generate the React TypeScript template.

```sh
npm create vite@latest my-app -- --template react-ts
```

Working directory: The generated my-app directory

Install generated dependencies and create the npm lockfile.

```sh
npm install
```

- Replace my-app with the unused intended directory. Preserve an established package manager in existing work.
- This template creates the client application, not an API server, database, authentication service or production hosting setup. Do not put secrets or database credentials in browser code.

### Conditional follow-up generators

#### Feature generation boundary

Use when: Adding client components/routes or integrating the selected API after scaffolding.


- Vite does not provide a general component/model/controller generator. Use installed router/UI tooling only if the project has selected it; ordinary React components follow the generated module and TypeScript conventions.
- Database migration generators belong in the API/backend repository that owns the data. Do not add PostgreSQL/Drizzle tooling to a browser-only bundle.

### Preserve the generated foundation

- Generated .gitignore, index.html entry, Vite/React plugin setup, ESLint configuration, TypeScript project configuration and package scripts.
- Lockfile and runtime constraints; adapt sample components while retaining the working scaffold.

### Baseline and generation checks

- Run npm run build and the generated lint script; confirm build includes the template TypeScript check rather than relying on transpilation alone.
- Run npm run dev and inspect the actual browser UI; test API origins/authentication at the browser boundary.
- Review ignore behavior and generated-file deviations before adding project files.

### Generation receipt

- Component and selected starting point, or the documented absence of a full application generator
- Generator/toolchain versions, exact commands or IDE template/settings, working directory and generated destination
- Generated files retained, deliberate deviations with reasons, and required supplemental ignore rules
- Baseline checks and later checks actually run, results and remaining prerequisites or untested behavior

### Generator sources

- [Vite Getting Started and templates](https://vite.dev/guide/)

## Tools

### browser build and UI: React + Vite + TypeScript

Focused browser development without unnecessary server framework

Limits and integration: TypeScript compiles to JS; Vite is tooling, not a backend; keep HTML/CSS competence


- https://vite.dev/guide/
- https://tanstack.com/start/latest
- https://react.dev/learn/typescript

Alternatives: Next.js for full-stack/SSR; TanStack Start when routing/server integration is needed

### validation: Zod at API/client boundaries

Check external values and share explicit contracts

Limits and integration: Client checks never replace authoritative backend validation or authorization


- https://zod.dev/

Alternatives: Use the existing API's schema/code generation

### Identity ownership: Existing backend owns authentication and authorization

Avoid duplicating external-system ownership in browser code

Limits and integration: No database credentials/server secrets in browser; document API/session/CORS contract


- https://nextjs.org/docs/app/guides/authentication

Alternatives: Adopt full-stack Node record when backend is in scope

### Database ownership: Existing backend owns persistence and migrations

Avoid duplicating external-system ownership in browser code

Limits and integration: No database credentials/server secrets in browser; document API/session/CORS contract


- https://nextjs.org/docs/app/guides/authentication

Alternatives: Adopt full-stack Node record when backend is in scope

### Background work ownership: Existing backend owns durable jobs

Avoid duplicating external-system ownership in browser code

Limits and integration: No database credentials/server secrets in browser; document API/session/CORS contract


- https://nextjs.org/docs/app/guides/authentication

Alternatives: Adopt full-stack Node record when backend is in scope

### Static typing: Strict TypeScript; retain generated project-reference build

Static checks and user-visible browser behavior

Limits and integration: Configure router/API failure/session expiry tests; preserve scaffold-specific build scripts


- https://vite.dev/guide/
- https://nextjs.org/docs/app/guides/testing/vitest
- https://nextjs.org/docs/app/guides/testing/playwright

Alternatives: Preserve existing compatible tooling

### Linting: ESLint

Static checks and user-visible browser behavior

Limits and integration: Configure router/API failure/session expiry tests; preserve scaffold-specific build scripts


- https://vite.dev/guide/
- https://nextjs.org/docs/app/guides/testing/vitest
- https://nextjs.org/docs/app/guides/testing/playwright

Alternatives: Preserve existing compatible tooling

### Domain and component tests: Vitest

Run isolated domain behavior checks with a configured test environment

Limits and integration: Install Vitest; preserve Vite plugins or add a separate test configuration. Mock only external boundaries and test failure states.


- https://vitest.dev/guide/

Alternatives: Preserve existing compatible tooling

### Browser tests: Playwright

Exercise critical journeys in actual browser engines

Limits and integration: Install @playwright/test and matching browsers; configure an isolated test server/data and test session expiry, routing and authorization failures.


- https://playwright.dev/docs/intro

Alternatives: Preserve existing compatible tooling

### deployment: Static asset host chosen by project

Browser build can be independently served

Limits and integration: Configure deep-link fallback, API origins, cache invalidation and environment handling; preview is not production


- https://vite.dev/guide/

Alternatives: Server-rendered framework when justified

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

### Routing: TanStack Router

Typed navigation, route loading and search parameters suit application screens

Limits and integration: Install @tanstack/react-router; configure the chosen file-based plugin or code-based routes. Test deep links, not-found routes and browser back; route guards do not replace server authorization.


- https://tanstack.com/router/latest/docs/overview

Alternatives: React Router in established projects; No router for a single screen

### Live server updates: EventSource for one-way server events

Browser-standard streaming suits status/progress feeds

Limits and integration: Backend owns authenticated stream and event IDs. Test reconnect, replay and proxy buffering; EventSource is one-way and its constructor offers no arbitrary authorization-header option. Confirm long-lived connection support on host.


- https://html.spec.whatwg.org/multipage/server-sent-events.html

Alternatives: WebSocket service for bidirectional collaboration; Polling for infrequent updates

## Architecture and developer workflow

React/Vite builds browser assets. Recommendation: select it when an existing API owns persistence, authorization, email, durable jobs and other privileged effects; choose routing and remote-state tools deliberately. A client-only build has no protected server runtime.

Version scope: Documentation reviewed 11 October 2026: current React docs label 19.3; current Vite docs include migration from v7 and Rolldown build options. Preserve the project's resolved React/Vite/TypeScript/router versions and API schema. SPA guidance is not a claim that Vite supplies SSR or a backend.
Reviewed: 2026-10-11 | Evidence: documentation-reviewed | Source record: inputs/research/migrations-clients.json

### Architecture boundaries

- Views consume route-loaded or query-cached DTOs; one API client module defines credentials, errors, cancellation and runtime validation. Backend ownership remains independent of UI language.
- Recommendation: domain state stays on the server; transient form/navigation state stays in the browser. Use tenant-aware cache keys and an explicit account-switch/reset policy.
- Bundled VITE_ values are public configuration. Keep database, provider and signing credentials in the backend; a development proxy is only local routing.
- Recommendation: retain content-hashed old chunks during rollout, revalidate HTML and provide a guarded update path for stale tabs. Add service-worker storage/adoption policy only if offline operation is required.

### Tools and feedback

- Start at the source README, API schema and lockfile. For a new local prototype npm create vite@latest my-app -- --template react-ts creates a starter; record resolved versions before promoting it. Existing applications keep their package manager.
- Use npm ci, the configured TypeScript project check (for the standard scaffold npx tsc -b) and npm run build. npm run dev is local development; npm run preview previews a build and is not the production host.
- Configure routing, typed API boundaries, TanStack Query only where useful and its QueryClientProvider. Define loading, stale, denied and offline states before using retries.
- Recommendation: use browser network/debug tooling and React profiling for the actual slow interaction. Configure Playwright with old/new API fixtures; run npx playwright test only after installing its runner/browsers and setting an isolated webServer.

### Translations to avoid

- Bundling a secret as VITE_API_KEY publishes it to users; moving its string into a frontend module does not create a trust boundary.
- Rebuilding server authorization as React route guards allows direct unauthorized API calls.
- Independent fetching in nested effects creates waterfalls and duplicated state ownership; use route loaders or a selected remote-state cache where appropriate.
- Treating TanStack Query defaults as an application freshness contract overlooks refetch/retry behavior and account boundaries.
- Deleting old chunks on deployment breaks lazy imports in open tabs; repeated automatic reload can also discard unsaved work.

### Architecture sources

- [React Build an app from Scratch](https://react.dev/learn/build-a-react-app-from-scratch): A Vite client-only starter requires deliberate routing/data tools; SSR/RSC are additional architecture work.
- [Vite Getting Started](https://vite.dev/guide/): Scaffold command and runtime requirements must be checked against resolved Vite version.
- [Vite Environment Variables and Modes](https://vite.dev/guide/env-and-mode): VITE_ values are bundled into client code and must not contain secrets.
- [Vite Building for Production](https://vite.dev/guide/build): Deleted old chunks can fail dynamic imports; vite:preloadError and HTML cache policy support recovery design.
- [Vite Deploying a Static Site](https://vite.dev/guide/static-deploy): Build output needs a chosen production host; vite preview is for local preview.
- [TanStack Query Important Defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults): Staleness, mount/focus/reconnect refetch, garbage collection and retries require explicit application choices.
- [WHATWG Fetch Standard](https://fetch.spec.whatwg.org/): Cross-origin response sharing and credential handling are browser protocol rules, separate from application authorization.
- [WHATWG Server-sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html): EventSource provides reconnect and event IDs; constructor options include withCredentials, not arbitrary headers.

## Transition options

Proposed designs and checks; these are not executed compatibility results.

### Browser and installed clients

**Inspect the source:** Existing URLs, backend API DTOs, errors, permissions and navigation/deep-link semantics.

**During coexistence:** Recommendation: Replace one route/screen with React while keeping existing API ownership and deep links; contract fixtures cover old/new UI.

**Target design:** Recommendation: Keep a browser/API split with route loaders or a selected query client; adopt a server framework only when required rendering/backend features justify it.

**Rollback:** Restore old HTML/assets/routes while API compatibility remains; preserve submitted data and reconcile pending mutations.

**Benefits and prerequisites**

- An independently delivered browser client can evolve behind a stable API. Requires: Owned routing/hosting fallback and backward-compatible API. Tradeoffs: A SPA must own routing/data/loading infrastructure; SSR/RSC are additional architecture choices.

**Checks before transfer**

- Direct deep links and refresh work from the production host.
- Old/new clients decode success/error/unknown-field fixtures.
- Unauthorized direct API requests remain denied.

- https://react.dev/learn/build-a-react-app-from-scratch
- https://vite.dev/guide/static-deploy

### Identity and authorization

**Inspect the source:** Backend credential transport, allowed origins, cookies/CSRF, token expiry and account boundaries.

**During coexistence:** Recommendation: Keep the backend issuer; configure same-origin routing or narrowly allowed credentialed CORS and preserve old clients.

**Target design:** Recommendation: Centralize credential/error behavior in the API client; enforce authorization and any cookie CSRF protection in the backend.

**Rollback:** Restore the old browser artifact/origin policy only if existing credential handling remains secure; retain revocation history.

**Benefits and prerequisites**

- One backend authority reduces duplicated browser identity logic. Requires: Reviewed origin/credential policy and issuer behavior. Tradeoffs: CORS controls browser response access, not authorization; frontend guards remain presentation only.

**Checks before transfer**

- Credentialed requests succeed only for permitted origins.
- Expired credentials transition to sign-in without endless retries.
- Cross-tenant and CSRF probes are rejected by the backend.

- https://fetch.spec.whatwg.org/
- https://vite.dev/guide/env-and-mode

### Caching and shared state

**Inspect the source:** Current fetch/cache behavior, stale tolerance, retry limits and account-switch isolation.

**During coexistence:** Recommendation: Introduce query keys for a bounded remote-state category; keep transient form state separate and compare outcomes with the old fetch path.

**Target design:** Recommendation: Use explicit TanStack Query staleTime, retry, invalidation and account-clear policy where its remote-state cache serves a requirement.

**Rollback:** Return the category to the old loader and clear the new cache; do not discard durable pending user operations.

**Benefits and prerequisites**

- Shared queries can reuse data and refresh deliberately. Requires: A QueryClientProvider, stable tenant-aware keys and mutation invalidation. Tradeoffs: Default stale queries refetch on mount/focus/reconnect; retries can obscure application errors if left unspecified.

**Checks before transfer**

- A mutation refreshes affected list/detail views.
- Switching accounts cannot reuse the old account's records.
- Network restoration produces one coherent refresh; permission errors do not retry indefinitely.

- https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults

### Realtime transport

**Inspect the source:** Existing event envelope, authorization, IDs, reconnect behavior and replay/retention rules.

**During coexistence:** Recommendation: Keep a backend bridge producing the current event contract; move clients by stable subscription cohort rather than arbitrary per-request routing.

**Target design:** Recommendation: Use EventSource for one-way events when host/credentials fit, WebSocket for bidirectional needs; persist/replay events separately when delivery requires it.

**Rollback:** Restore old polling/transport using the same cursor domain; reconcile delivered events and keep bridge/history through the rollback window.

**Benefits and prerequisites**

- A standard browser event stream can replace bespoke polling for suitable feeds. Requires: Authenticated endpoint, event IDs, retention/replay contract and streaming host. Tradeoffs: EventSource reconnect does not create server event history; its constructor has no arbitrary header option.

**Checks before transfer**

- Disconnect after event N and reconnect; no required event is omitted or applied twice.
- Revocation terminates access and later reconnect is denied.
- Old/new envelopes decode during mixed-version rollout.

- https://html.spec.whatwg.org/multipage/server-sent-events.html

### Delivery and recovery

**Inspect the source:** Existing HTML/CDN/service-worker policy, lazy chunks and open-tab unsaved state.

**During coexistence:** Recommendation: Keep prior hashed assets and compatible APIs while serving new HTML to a cohort; include any existing service worker's activation/cache rules.

**Target design:** Recommendation: Revalidate HTML, retain old content-hashed chunks and handle vite:preloadError with a guarded refresh/update flow that preserves drafts.

**Rollback:** Restore the prior HTML and retained assets, roll service-worker changes through their actual lifecycle, and keep new-client API support.

**Benefits and prerequisites**

- Old tabs can continue loading their release's lazy chunks. Requires: Asset retention, correct base path and tested update UX. Tradeoffs: Retention costs storage; refresh may lose state, and reload loops do not fix a wrong CDN policy.

**Checks before transfer**

- After deployment an old tab lazy-loads its old route successfully.
- If a chunk is intentionally unavailable, the update path retains the draft and recovers once.
- Production HTML/cache headers and API compatibility match the rollout policy.

- https://vite.dev/guide/build
- https://vite.dev/guide/static-deploy

Rewrite workflow: /rewrite/guide.md
Shared contracts and phases: /rewrite/contracts.json


## Setup
1. Complete the selected starting point and baseline checks in the Generators section first; then continue with the integration steps appropriate to the chosen component.
2. Extend the generated README with API/session owners, API contract, run/check commands and environment variable names. Confirm strict TypeScript and add router/query tooling only when needed.
3. Add Zod when validating runtime input or external data is required, and configure the selected test tools. Implement error/loading/session-expiry states and verify authoritative authorization in the API that owns the data.
4. Build static assets, configure the chosen production host for deep links and API origins, and verify browser navigation plus authentication/session behavior against the deployed API during an authorized release.

## Verification
Commands below require the selected tools and project configuration. Replace example paths, schemes and IDs; distinguish tests from builds and interactive startup. These are instructions, not recorded passes.

```text
npm ci
npx tsc --noEmit
npx eslint .
npx vitest run
npm run build
npx playwright test
```

## Open questions
- Which API and identity owner defines schemas, cookies/tokens and CORS?
- Do routes need shareable URLs, offline behavior or server rendering?
- Which browser/device matrix and accessibility requirements must be met?
- Which static host supports route fallbacks and the selected API origins?

## Sources
- [Vite getting started](https://vite.dev/guide/)
- [TanStack Start](https://tanstack.com/start/latest)
- [Zod](https://zod.dev/)
- [Next.js authentication](https://nextjs.org/docs/app/guides/authentication)
- [Next.js Vitest](https://nextjs.org/docs/app/guides/testing/vitest)
- [Next.js Playwright](https://nextjs.org/docs/app/guides/testing/playwright)
- [React TypeScript](https://react.dev/learn/typescript)
- [TanStack Query important defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults)
- [React Hook Form repository](https://github.com/react-hook-form/react-hook-form)
- [Tailwind Vite installation](https://tailwindcss.com/docs/installation/using-vite)
- [Radix accessibility](https://www.radix-ui.com/primitives/docs/overview/accessibility)
- [Playwright accessibility testing](https://playwright.dev/docs/accessibility-testing)
- [TanStack Router overview](https://tanstack.com/router/latest/docs/overview)
- [HTML EventSource standard](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [Vitest guide](https://vitest.dev/guide/)
- [Playwright installation](https://playwright.dev/docs/intro)

Keep the project README current and link the selected guidance; preserve existing project instructions.
