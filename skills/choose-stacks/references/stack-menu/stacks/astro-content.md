# Astro content site

Content-first websites that pre-render public pages and hydrate selected interactive islands.

Language: TypeScript | Reviewed: 2026-10-23 | Evidence: documentation-reviewed; disposable create-astro basics scaffold, install, build and local dev HTTP smoke check executed; no application integration tests run

Source record: menu/curated/astro-content.json.

Core guidance checked: 2026-10-23. Review sources are listed below. /research-freshness.json describes the imported research packet; this record retains its own evidence scope. These recipes and selected dependency combinations need qualification in the actual project.

## Application role
Components: web
UI: server
Deployment: static

## Use cases
- Documentation, guides, blogs, catalogs and marketing sites with repeatable authored content
- Content-first websites that need a few independent interactive widgets
- Public pages that can be generated at build time and served as static files

## Fit
- Most routes present content and should be available as generated HTML without a request-time application server
- Markdown or structured local data needs schema validation and generated routes
- Interactivity is limited to discrete components that can hydrate independently
- The team wants TypeScript templates while retaining ordinary HTML, CSS and browser APIs

## Choose something else when
- The site is a tiny stable page set with no recurring content or build workflow; plain HTML and CSS may be enough
- The main product is a sustained stateful browser application such as an inbox, dashboard or collaborative editor; choose a browser-app framework around that requirement
- Request-time identity, private personalized pages, mutations, APIs, database writes, durable jobs or transactional effects are required and no separately owned backend or selected Astro adapter is in scope
- Nontechnical editors need a managed editorial interface, preview, approval and media workflow; choose and qualify the CMS as content owner before selecting a presentation layer

## Agent workflow
- Read README, dependency manifests, lockfiles, runtime pins and the maintained project workflow before changing anything. Preserve an existing stack unless reconsidering it is part of the request.
- For a new component, read the Generators section before writing application files. Use its appropriate official initializer and retain its generated baseline; follow-up generators are conditional on the selected feature.
- Use this guide to select tools by requirement. Resolve compatible versions from official and installed-version documentation; record the actual lockfile and runtime versions.
- Create a plan for schema changes, identity, authorization, external effects and deployment. A library choice does not complete its integration.
- Run relevant checks after configuration. Exercise the real interface, failure paths and packaged artifact on the intended target. Report commands, versions, results and untested behavior.
- On failure, retain the command and diagnostic, fix the failing prerequisite and resume there. Do not regenerate over existing work or suppress failures to make a check green.

## Best practices
- Keep public content available in generated HTML; validate structured collections and create route templates explicitly.
- Keep static output public. Retain backend authorization for private or mutable data and qualify adapters for request-time pages.
- Use islands for defined interactions and test keyboard behavior; do not hydrate the whole page without a product reason.
- Verify routes, canonical URLs, sitemap, redirects, status codes and 404 behavior on the chosen host.

## Generators: create the baseline first

Generator documentation reviewed: 2026-10-23. Evidence: documentation-reviewed; disposable create-astro basics scaffold, install, build and local dev HTTP smoke check executed.

### Required workflow

- Before writing a new project's application files, read its profile's starting points and use the official framework or language initializer appropriate to the component. Do not hand-recreate a generated skeleton. Where no full application generator exists, use the documented module/package initializer and assemble only the missing application pieces.
- Choose one starting point per component. Check the installed generator's version and help, prerequisites, template, database, UI, test and runtime options. Commands are examples: replace names and paths, resolve compatible versions, and record the exact invocation and selected options. Do not blindly run every listed generator.
- Generate in a new empty destination. For an existing repository, preserve its conventions and use relevant incremental generators. If a baseline comparison is needed, generate a separate disposable reference with matching versions/options and reconcile deliberately; never regenerate over existing work.
- Keep applicable generated configuration, hidden files, formatter/linter settings, ignore rules, manifests, lockfiles, tests, wrappers and entry points. Extend them for the project instead of replacing them with abbreviated handwritten copies. A generator may initialize version control or offer a commit; respect the user's Git instructions.
- Run the generated baseline's documented checks before feature changes, then relevant checks after configuration and implementation. Inspect what version control would include, including hidden files, build output, local secrets and operating-system metadata. Add needed ignore rules explicitly: no generator guarantees that .DS_Store or every local artifact is ignored.
- Use follow-up generators only when their feature or tool is selected. Review generated changes and dependencies, apply required migrations in the intended environment, and exercise the generated behavior. Scaffolding does not establish authorization, safe retries, production readiness or every best practice.
- If the required generator, template or IDE is unavailable, report the missing prerequisite and the documented route. Do not silently substitute a handwritten scaffold. Keep documentation review, generator execution, baseline checks and application qualification as separate evidence.

### Choose a starting point

#### Official create-astro basics template

Use when: A new content-first site has repeatable pages, typed content or selective interactive components and can start with static output.

1. Use an unused source directory outside synchronized storage. Read project requirements and decide whether source content belongs in Git or an already-selected headless CMS.
2. Check current Astro Node requirements and inspect create-astro help before selecting flags. For the tested create-astro 5.3.1 CLI, the command below generated the basics template with no package installation, Git initialization or AI instruction files.
3. Install dependencies in the generated project with the selected package manager. Record resolved create-astro, Astro, Node and package-manager versions, commit the lockfile, and retain generated scripts and configuration.
4. Create explicit page routes for content. If a collection should produce one URL per entry, define a schema and a dynamic route using getStaticPaths; collection files alone do not create pages.
5. Review public routes, canonical site URL, trailing slashes, redirects, sitemap, 404 behavior and static asset paths before connecting the intended host.

Working directory: An unused local source-workspace parent outside synchronized storage; my-site must not already exist

Check Node against the current Astro installation requirement.

```sh
node --version
```

Working directory: An unused local source-workspace parent outside synchronized storage; my-site must not already exist

Inspect the currently resolved create-astro flags before scaffolding.

```sh
npm create astro@latest -- --help
```

Working directory: An unused local source-workspace parent outside synchronized storage; my-site must not already exist

Generate the official basics project without installing dependencies, initializing Git or creating AI instruction files.

```sh
npm create astro@latest my-site -- --template basics --no-install --no-git --no-ai --yes --skip-houston
```

Working directory: The generated my-site directory

Install the dependencies generated by the CLI and create the package lockfile.

```sh
npm install
```

- The tested CLI version was create-astro 5.3.1; it resolved Astro 7.4.2 from the template. The command-line `--no-ai` option came from the installed CLI help; confirm it remains supported before reusing this command.
- Replace my-site with the intended unused directory. `@latest` is a scaffold-time lookup; pin the selected runtime through project policy and use the generated lockfile for later installs.
- The disposable qualification used Node 24.21.0 and npm 11.19.0. It ran `npm ci`, `npm run build`, `npm run dev -- --host 127.0.0.1`, and fetched `/` with HTTP 200 and `text/html`. This only verifies the untouched basics starter, not an application, integration, CMS, adapter or production host.
- The project README remains the owner of purpose, start commands and content/workflow navigation. Do not create or rely on project AGENTS.md files.

### Conditional follow-up generators

#### Content Collections

Use when: Markdown or structured content needs a validated schema and generated pages; do not add a collection layer for a handful of stable one-off pages.

1. Define the content shape and source owner before writing a schema. Use local files for Git-reviewed content or fetch from the selected CMS without changing that CMS's editorial ownership.
2. Create the collection schema and an explicit route template. Call getCollection and getStaticPaths to create static URLs for entries; verify the final route names and content output.
3. Test malformed content at build time and check empty, draft and missing-route behavior. Preview/editor access is a separate CMS integration and authorization concern.

- Astro validates collection entries against schemas and generates TypeScript support, but collection entries do not become pages automatically.
- If editors need a visual workflow, select a headless CMS and define ownership for drafts, preview, approvals, publishing hooks and media. Astro itself is not that editorial interface.

#### Server adapter

Use when: A specific route needs request-time rendering, request cookies/headers or private personalization, and the selected host/runtime can operate the chosen adapter.


- Read the current adapter guide and the selected host's support limits before adding it. Astro's default output is static; on-demand rendering requires an adapter.
- This profile does not add database, authentication, API, email or durable-job ownership. Keep those responsibilities in their existing backend unless they are separately designed, migrated and tested.
- Qualify adapter behavior, secrets, cookies, headers, caching, redirects, cold starts and deployment independently. The static starter build does not establish any of these properties.

#### Interactive island integration

Use when: A content route has a defined widget whose stateful behavior justifies a component framework, and the team has selected that framework.


- Use semantic HTML and browser APIs first. Add only the chosen official Astro integration (for example, React, Svelte or Vue) and hydrate only the component that needs browser interaction.
- Keep content output usable as HTML. A client island does not supply backend authorization, persistence or offline synchronization.

### Preserve the generated foundation

- Generated package scripts, Astro configuration, TypeScript settings, project lockfile and ignore rules; record any intentional change in README.
- Content collection schemas, route templates, public URL policy and CMS/API ownership as editable project sources.
- Original media sources and attribution records; use src assets for processing or public assets for deliberate unprocessed direct URLs.

### Baseline and generation checks

- Run npm ci and npm run build with the committed lockfile; a successful untouched starter build does not qualify a site's content or integrations.
- Run npm run dev and inspect generated pages and routes. Check route HTML, collection entry URLs, missing pages, assets and browser behavior.
- Set the real site URL and verify canonical metadata and sitemap against production host configuration. Check redirect status and trailing-slash behavior at that host; static output may express redirects as HTML rather than an HTTP status.
- Verify image transformations and direct public asset URLs. If video is used, test its chosen streaming service and do not attribute video handling to Astro.
- If adding an adapter or CMS, test its actual preview, draft privacy, authorization, cookies, redirects, runtime APIs, cache behavior and production deployment separately. No application integration test or static regression suite was run for this record.

### Generation receipt

- Component and selected starting point, or the documented absence of a full application generator
- Generator/toolchain versions, exact commands or IDE template/settings, working directory and generated destination
- Generated files retained, deliberate deviations with reasons, and required supplemental ignore rules
- Baseline checks and later checks actually run, results and remaining prerequisites or untested behavior

### Generator sources

- [Install Astro and create-astro CLI](https://docs.astro.build/install-and-setup/)
- [Astro CLI commands](https://docs.astro.build/en/reference/cli-reference/)
- [Content Collections](https://docs.astro.build/en/guides/content-collections/)
- [On-demand rendering and adapters](https://docs.astro.build/en/guides/on-demand-rendering/)
- [Routing and redirects](https://docs.astro.build/en/guides/routing/)
- [Astro CMS integration](https://docs.astro.build/en/guides/cms/)
- [Astro image handling](https://docs.astro.build/en/guides/images/)

## Tools

### content site and rendering: Astro with static output and Content Collections where content is structured

Astro pre-renders pages by default and can validate Markdown and data collection entries; islands allow selected components to run in the browser without making the whole site a client application.

Limits and integration: Collections do not create routes automatically: define routes and getStaticPaths for generated content pages. Static output is public and cannot provide request-time user-specific authorization. On-demand rendering requires a host adapter; qualify that host separately.


- https://docs.astro.build/en/concepts/why-astro/
- https://docs.astro.build/en/concepts/islands/
- https://docs.astro.build/en/guides/content-collections/
- https://docs.astro.build/en/guides/on-demand-rendering/

Alternatives: Plain HTML and CSS for a tiny stable site; Hugo where the team needs its Go-based publishing workflow, multilingual support or taxonomy system; A headless CMS as editorial owner when editors need its workflow; Astro can remain the presentation layer

### authored content and editorial ownership: Markdown and typed local data in the project when code review and Git are the intended publishing workflow

Keeps the publishing owner explicit and lets collection schemas validate the content shape at build time.

Limits and integration: Astro supplies Markdown support, not a CMS authoring product. With a CMS, the CMS owns editing, workflow and source assets; this profile does not select a CMS or qualify preview, webhook, asset delivery or draft access behavior.


- https://docs.astro.build/en/guides/content-collections/
- https://docs.astro.build/en/guides/cms/

Alternatives: A selected headless CMS when editors need a separate visual authoring and collaboration interface

### browser interactivity: Semantic HTML and browser APIs; add an Astro framework integration only for a component that needs it

Keeps the ordinary content path rendered as HTML and makes the client-side boundary explicit per component.

Limits and integration: A client island does not make a static page an authorized backend. Browser-bundled configuration is public. Do not install a component framework or state library until a concrete widget requires it.


- https://docs.astro.build/en/concepts/islands/
- https://docs.astro.build/en/guides/client-side-scripts/

Alternatives: A separately owned API for private or mutable application data; React, Svelte or Vue components as explicit islands when an existing component ecosystem is a requirement

### routing and search metadata: File-based routes under src/pages; set the production site URL and use the sitemap integration when a sitemap is required

Route files become public URL paths, and the configured site URL supports canonical and sitemap generation.

Limits and integration: Check generated URLs, canonical links, sitemap, 404 behavior, trailing-slash policy and redirects against the selected host. Static redirects may be emitted as meta refresh; status semantics are host-dependent.


- https://docs.astro.build/en/guides/routing/
- https://docs.astro.build/en/guides/configuring-astro/
- https://docs.astro.build/en/guides/integrations-guide/sitemap/

Alternatives: Host-managed redirects when static HTML redirects cannot provide the required status or behavior

### media: Import local images from src/ for Astro image processing where supported

Makes the processing and URL choice explicit for each asset.

Limits and integration: Astro does not process files in public/. It has no built-in video optimization or streaming; choose and verify a hosted media service if needed. Check remote-image domains and license/attribution in the content owner.


- https://docs.astro.build/en/guides/images/

Alternatives: public/ for files that must keep a direct stable URL and should be copied without processing; A selected image or video CDN/service when its delivery workflow is required

### deployment and dynamic routes: Static host serving the generated dist directory for the static profile

Static publishing has no Astro request-time server to operate; request-time rendering is an explicit adapter and runtime choice.

Limits and integration: This record does not qualify any host, adapter, CMS or API integration. Keep database, authentication, mutation and durable-work ownership in an existing backend unless their transfer is separately designed and tested.


- https://docs.astro.build/en/guides/deploy/
- https://docs.astro.build/en/guides/on-demand-rendering/

Alternatives: Astro Node, Cloudflare, Netlify or Vercel adapter when specific pages need request-time rendering

## Architecture and developer workflow

Recommendation: use Astro as a content presentation site, statically pre-rendering public pages and optionally hydrating discrete interactive islands. A content collection is not a route until a page template creates it. The selected CMS may own authoring, drafts and assets; existing APIs and application backends remain their own data, identity, migration and side-effect authorities. Astro's request-time mode requires a separately selected and qualified adapter/runtime.

Version scope: Astro installation and content/routing docs checked 23 October 2026. The disposable official basics scaffold used create-astro 5.3.1, Astro 7.4.2, Node 24.21.0 and npm 11.19.0. It built and served its starter route. This is not application or adapter compatibility evidence.
Reviewed: 2026-10-23 | Evidence: documentation-reviewed | Source record: migrations/astro-content.json

### Architecture boundaries

- Inventory public content routes, source formats, existing URL and redirect contracts, canonical domain, sitemap and media. Define a collection schema only for structured content; define explicit routes and getStaticPaths for generated entry URLs.
- Recommendation: keep repository-authored content in reviewed Markdown/data, or name a headless CMS as the editorial owner. A CMS integration needs explicit draft/preview authorization, publish hook, media and failure behavior. Astro does not supply the CMS authoring interface.
- Static output is public build output. Do not place secrets, private drafts or authorization decisions in generated HTML or client JavaScript. Retain an existing API/backend as owner for identity, protected data, mutations, jobs and external effects until a separate transfer is designed.
- A client island is a browser UI boundary, not a backend. Add framework hydration only for the selected interaction and keep useful content in initial HTML.
- Use src image imports where processing is supported; public assets are copied without optimization. Astro has no built-in video streaming/processing. Keep original assets, licenses and delivery owner explicit.
- Static redirects may be emitted as HTML meta refresh and do not provide a portable HTTP redirect status. Check actual host rules, status codes, trailing-slash normalization, cache behavior and 404 response.
- Only enable request-time pages with a selected adapter and host that support needed cookies, headers, runtime APIs and caches. Rehearse deployment and secret handling for that exact target; this record does not qualify any adapter.

### Tools and feedback

- Start from the content owner, route/URL inventory and project README. Run the official generator in an unused local source directory, inspect installed create-astro help, install using the chosen package manager and preserve its lockfile.
- The disposable baseline used `npm create astro@latest astro -- --template basics --no-install --no-git --no-ai --yes --skip-houston`; installed create-astro was 5.3.1. Node was 24.21.0 and npm was 11.19.0. `npm ci` then `npm run build` passed on the untouched starter; `npm run dev -- --host 127.0.0.1` served `/` as HTTP 200 `text/html`. No application tests were run.
- For content routes, add the collection schema and route template, run the build, and inspect emitted URLs and malformed-entry failures. Keep generated routes synchronized with the authored/cms-owned content inventory.
- Set the production site URL; inspect canonical links, metadata, sitemap, direct route loads, missing pages and redirect behavior in generated output and the selected host. A local build does not establish host status codes, headers, indexing or production delivery.
- For a CMS, adapter, private preview or API, qualify its actual version, auth boundary, secrets, caching, webhooks and production runtime separately. Record commands and results for that application; do not inherit the starter's smoke check as proof.

### Translations to avoid

- Do not select Astro merely because it can import React, Vue or Svelte; use a rich browser-app framework when most routes require persistent client state and app-like interaction.
- Do not use static build output for account-specific content or pretend that a client island, hidden link or generated HTML protects data.
- Do not treat a Content Collection as CMS, route generation, search index or editorial preview; each requires explicit project-owned setup.
- Do not assume a redirect configured in Astro produces a production HTTP 301/302 on a static host. Verify the provider's routing rule and observed response.
- Do not assume public assets are optimized or that Astro streams video. Inspect the selected pipeline and delivery service.
- Do not infer that replacing a full-stack web application with Astro transfers its API, database, identity, migration or job responsibilities. Retain the current owners or define and qualify each transfer separately.

### Architecture sources

- [Astro Content Collections](https://docs.astro.build/en/guides/content-collections/): Schemas validate content entries, while explicit route templates create static URLs for collection records.
- [Astro Islands](https://docs.astro.build/en/concepts/islands/): Interactive components are separately hydrated with client directives while other page content remains HTML.
- [Astro On-demand Rendering](https://docs.astro.build/en/guides/on-demand-rendering/): Request-time pages need a server adapter; the static baseline has no request-time personalization runtime.
- [Astro CMS Guide](https://docs.astro.build/en/guides/cms/): A CMS owns separate authoring capabilities; Astro fetches and presents selected CMS content.
- [Astro Routing](https://docs.astro.build/en/guides/routing/): File-based routes and redirects need review against static output and the deployment host.
- [Astro Deployment](https://docs.astro.build/en/guides/deploy/): Static output is deployed from dist; on-demand output requires an adapter for the chosen runtime.
- [Astro Images](https://docs.astro.build/en/guides/images/): src images can be processed while public files are copied unprocessed; Astro does not provide video streaming.

## Transition options

Proposed designs and checks; these are not executed compatibility results.

### Browser and installed clients

**Inspect the source:** Inventory the current public and authenticated URLs, rendered HTML semantics, navigation, forms, interactive states, metadata, assets, API DTOs and error behavior. Identify which routes are content presentations versus application screens; a shared web label does not make those roles identical.

**During coexistence:** Proposed option: move a bounded public content route set to Astro while keeping existing API, authentication, data writer, migrations, jobs and external effects with their current owners. Route a small path/host cohort only after the old and new route maps, cookies and canonical URLs are explicit. Keep any authenticated or stateful application routes on their existing owner until separately planned.

**Target design:** Proposed option: statically render public content from reviewed local records or the named CMS, with optional islands for specific interactions. Preserve the route and semantic HTML contract where required. If the source role includes authenticated pages, mutations or private APIs, compose or retain that owner; static Astro alone does not cover those duties.

**Rollback:** Restore the previous route owner or host mapping while retaining the old content build and API compatibility. Reconcile any submitted forms or external effects through their existing backend owner; routing rollback does not undo writes or CMS publication.

**Benefits and prerequisites**

- Public content pages can be emitted as HTML at build time, with browser JavaScript scoped to explicitly hydrated widgets. Requires: Content can be available at build time; content routes and schema are identified; a static host serves the generated paths; any dynamic data/API stays explicitly owned. Tradeoffs: New content publication requires a build/deploy unless a chosen dynamic route or CMS delivery path is added. A static presentation change does not migrate application APIs, identity or persistence.

**Checks before transfer**

- Compare old/new direct route, trailing-slash, canonical, link, metadata, 404 and redirect behavior on the selected host; confirm actual response codes and route coverage.
- For every moved content type, verify generated entry URLs, required fields, draft visibility, media paths and sitemap membership; a malformed record must fail or be handled by the documented content policy.
- If a migrated route reads or changes private application data, verify that the existing backend still authenticates and authorizes direct requests; do not rely on static content or UI hiding.
- Exercise the selected island with JavaScript disabled/enabled as appropriate and verify accessible keyboard behavior; content remains understandable in the generated HTML.
- Rehearse publishing, cache invalidation and rollback while old assets and API contracts remain available; inspect deployed host headers and redirects.

- https://docs.astro.build/en/concepts/islands/
- https://docs.astro.build/en/guides/content-collections/
- https://docs.astro.build/en/guides/routing/
- https://docs.astro.build/en/guides/configuring-astro/

### Delivery and recovery

**Inspect the source:** Inventory current deploy artifact, route host rules, HTTP status and cache headers, redirects, generated sitemap, media/CDN paths, build-time environment and rollback retention.

**During coexistence:** Proposed option: publish Astro's dist output under a bounded route or host mapping while retaining the old artifact and host rules. Keep old and new redirects/canonical origins consistent during the cohort; preserve external API and CMS owners.

**Target design:** Proposed option: use a static deployment for static pages. If on-demand rendering is selected, add the host adapter and qualify its runtime, credentials and operations as a different deployment profile. Retain old public assets through the rollback window where existing pages may reference them.

**Rollback:** Restore the previous host mapping and deployment artifact, including old redirect and cache policy, then confirm the previous route set is served. Keep CMS/API/database ownership unchanged unless a separately reviewed transfer requires data reconciliation.

**Benefits and prerequisites**

- A static site artifact can be served from a static host without operating an Astro request-time server for those pages. Requires: Build command, dist output, route fallback/404 policy, redirects, headers, asset paths and canonical site URL are configured for the selected host. Tradeoffs: Host behavior is provider-specific; a static artifact cannot compute per-request session output, and dynamic pages introduce a runtime and adapter to operate.

**Checks before transfer**

- Build from a clean lockfile install and inspect generated static routes, assets, canonical links and sitemap.
- Request moved, missing and redirected URLs from the host; verify status codes, location, content type, cache headers and trailing slash behavior.
- Verify the selected CMS publish hook or API contract updates the intended pages without exposing preview secrets; test failed build/publish recovery if used.
- If an adapter is used, verify its exact host/runtime, cookies, headers, private data access, cache and deployment rollback; the static starter build is not evidence for these features.
- Rehearse restoration of the old route mapping/artifact and confirm retained assets and API compatibility allow rollback.

- https://docs.astro.build/en/guides/deploy/
- https://docs.astro.build/en/guides/on-demand-rendering/
- https://docs.astro.build/en/guides/routing/
- https://docs.astro.build/en/guides/images/

Rewrite workflow: /rewrite/guide.md
Shared contracts and phases: /rewrite/contracts.json


## Setup
1. Complete the selected starting point and baseline checks in the Generators section first; then continue with the integration steps appropriate to the chosen component.
2. From the generated project root, write README purpose, start commands, content source and editorial owner, public URL policy and navigation to installed Astro documentation. Preserve the user's existing repository instructions.
3. Create Content Collections only when structured Markdown/data needs schema validation; define the schema and explicit static page routes together. Keep static public content distinct from draft or account-specific content.
4. Document the content-route and URL map, canonical domain, trailing-slash rule, 404 behavior, redirects and the host setting that implements each. Confirm whether static redirect output provides the required response status; if not, configure a host redirect rule or select an adapter route and verify it.
5. Set the production site URL and generate a sitemap only when required. Review canonical URLs, duplicate routes, metadata, indexability and actual generated HTML; SEO metadata does not establish search indexing.
6. Assign media ownership explicitly. Use src image imports for supported processing, public files for unprocessed stable paths, and a selected external service for video streaming. Check license, alt text, dimensions, cache and delivery on the deployed host.
7. For a selected CMS, keep the CMS authoritative for editorial content, drafts and assets. Specify build/webhook ownership, preview and draft authorization before connecting it; do not leak preview tokens into client islands or static output.
8. Keep existing APIs, identity, database, migrations, jobs and external effects with their current owners. A static Astro client can consume public or authenticated API endpoints as designed, but static files cannot contain secrets or provide request-time permission checks. If a server-side page or new API is required, define a separate backend/adapter migration and its data ownership before implementation.
9. Run the project build and dev server; inspect generated route HTML, direct URLs, assets and not-found behavior. Against the intended host, verify redirect status, headers, cache, canonical URL and sitemap. This research did not run application tests, a CMS integration or an adapter deployment.

## Verification
Commands below require the selected tools and project configuration. Replace example paths, schemes and IDs; distinguish tests from builds and interactive startup. These are instructions, not recorded passes.

```text
node --version
npm create astro@latest -- --help
npm ci
npm run build
npm run dev -- --host 127.0.0.1
```

## Open questions
- Which pages are editorial content and which are application routes with private or mutable data?
- Who owns the source content: the repository or a selected CMS, and are draft preview, approval, webhooks and media management required?
- Which existing API, identity provider and database remain authoritative if the page needs account data or mutations?
- What are the intended URL, trailing-slash, redirect status, canonical, sitemap, 404 and cache policies on the selected host?
- Which images need transformation, which assets need stable direct URLs, and who owns video encoding and streaming?
- Does any route actually need request-time rendering, and does the selected adapter/host support the needed API, cookies, headers and runtime?

## Sources
- [Install Astro](https://docs.astro.build/install-and-setup/)
- [Why Astro?](https://docs.astro.build/en/concepts/why-astro/)
- [Islands architecture](https://docs.astro.build/en/concepts/islands/)
- [Content Collections](https://docs.astro.build/en/guides/content-collections/)
- [On-demand rendering](https://docs.astro.build/en/guides/on-demand-rendering/)
- [Use a CMS with Astro](https://docs.astro.build/en/guides/cms/)
- [Routing](https://docs.astro.build/en/guides/routing/)
- [Configuring Astro](https://docs.astro.build/en/guides/configuring-astro/)
- [@astrojs/sitemap](https://docs.astro.build/en/guides/integrations-guide/sitemap/)
- [Images](https://docs.astro.build/en/guides/images/)
- [Deploy your Astro Site](https://docs.astro.build/en/guides/deploy/)

Keep the project README current and link the selected guidance; preserve existing project instructions.
