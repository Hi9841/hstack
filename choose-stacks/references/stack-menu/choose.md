# Choosing a stack from requirements

Preserve an existing stack unless reconsidering it is requested. Separate the product into components; a web client, API and mobile client may have different owners.

## Gather requirements

- **Existing project:** Repository, chosen stack and conventions; whether a new stack is actually requested.
- **Target surfaces:** Browser, API, command line, automation, iOS, Android; a product may combine several.
- **Native platform UI:** Native controls and platform integration versus browser UI.
- **Offline behavior:** Read-only cache, offline edits, synchronization and conflict policy.
- **Required integrations:** Vendor SDKs, data/AI libraries, payments and platform APIs.
- **Runtime constraints:** Latency, throughput, concurrency, memory, persistent connections and background work.
- **Deployment:** Allowed host/runtime, data residency, OS, native toolchains and operational constraints.
- **Data and access:** Tenancy, authorization, durability, retention, backups and recovery.
- **Maintenance:** Team experience, delivery constraints, licensing, support and budget.

## Task-based starting points

Before building or rewriting, consider whether an existing service or specialized product already meets the need. If you intend to build or rewrite software, continue with the task below.

Task-based editorial defaults for new applications. The primary picks are reasoned editorial judgments from documented roles, not measured winners or a universal ranking. A use case identifies a strong starting profile for the stated job; it is not compatibility proof or authority to replace an existing stack.

Recommendations summarize documented framework roles and primary documentation. They do not establish application fit, dependency compatibility, capacity, migration safety, production readiness, or executed setup. Apply hard constraints first and qualify the actual project.

Choose the matching software task, then apply explicit ecosystem and platform constraints. A constraint selects the corresponding conditional primary; it does not create a separate task.

### Content website (`content-site`)

Primary profile: `astro-content`.

Astro is a focused default when the main job is publishing content as mostly static pages and the product does not need an application server for each visitor.

Tradeoff: Interactive islands and server endpoints add explicit client/runtime choices; a mostly static content site should not inherit a full application backend without a requirement.

Sources: [Astro content collections](https://docs.astro.build/en/guides/content-collections/); [Astro rendering modes](https://docs.astro.build/en/guides/server-side-rendering/)

Other scoped alternatives:
- Hugo content site: The site is a conventional static publication and the team specifically values Hugo's content organization and build model. Tradeoff: This is a conditional research lead without a curated Stack Menu profile; assess templates, content authoring and deployment for the actual site.
  Sources: [Hugo content organization](https://gohugo.io/content-management/organization/)
- Plain HTML and CSS: The site is small, rarely updated and has no need for a content workflow, component system or application behavior. Tradeoff: A manual page collection becomes harder to maintain as content, shared layouts or publishing needs grow.
  Sources: [MDN HTML basics](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax)
- Full web application framework `rails-hotwire-postgresql`: The site also needs accounts, database-backed workflows, staff operations or durable jobs that make it an application rather than primarily published content. Tradeoff: This adds an application server and product responsibilities; do not choose it solely to render mostly static content.
  Sources: [Getting Started with Rails](https://guides.rubyonrails.org/getting_started.html)

### Business web application (`web-product`)

Primary profile: `rails-hotwire-postgresql`.

Rails is a strong default for ordinary database-backed product work where server-rendered pages, forms, accounts, persistence and background jobs benefit from one cohesive application.

Tradeoff: It owns a running server and conventional server-rendered workflow; a client-heavy interface, a Python-centered team or a deliberate React full stack can justify another profile.

Ecosystem constraints: `python`, `php`, `ruby`, `elixir`, `react`.

When `ecosystem=python`, use `python-django`: A Python-centered team or ecosystem materially benefits the product, and Django’s integrated data and staff workflows fit.
Tradeoff: Django is broader than a narrow API and its admin does not replace product authorization.
Sources: [Django overview](https://docs.djangoproject.com/en/stable/intro/overview/)

When `ecosystem=php`, use `laravel-livewire-postgresql`: PHP expertise or a Laravel estate materially benefits the product and Laravel’s integrated conventions fit.
Tradeoff: Workers and scheduled jobs have separate runtime and deployment needs.
Sources: [Laravel starter kits](https://laravel.com/docs/starter-kits)

When `ecosystem=elixir`, use `elixir-phoenix-liveview`: The product is owned by an Elixir team or has a material need for Phoenix’s server-owned live interaction model.
Tradeoff: Connected state, authorization and capacity require representative workload qualification.
Sources: [Phoenix LiveView documentation](https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html)

When `ecosystem=react`, use `typescript-next-node`: The product explicitly requires a React full stack and Next.js fits its server/client and routing needs.
Tradeoff: Caching, server/client boundaries and deployment require deliberate choices.
Sources: [Next.js App Router](https://nextjs.org/docs/app)

Aliases: `react-fullstack` means this task with ecosystem=react.

Sources: [Getting Started with Rails](https://guides.rubyonrails.org/getting_started.html); [Active Record Basics](https://guides.rubyonrails.org/active_record_basics.html)

Other scoped alternatives:
- Python product application `python-django`: Python ecosystem integration, relational workflows, forms or built-in staff administration are central. Tradeoff: Django is a product framework choice, not an automatic alternative based only on language familiarity.
  Sources: [Django overview](https://docs.djangoproject.com/en/stable/intro/overview/)
- PHP product application `laravel-livewire-postgresql`: The team or existing system is PHP/Laravel-centered and the integrated Livewire/auth/queue conventions fit. Tradeoff: The web process, queue workers and scheduler have separate operating needs; browser/client-heavy work may need a distinct client.
  Sources: [Laravel starter kits](https://laravel.com/docs/starter-kits)
- Full-stack React application `typescript-next-node`: The interface is intentionally React-led and the team wants route handlers and server/client React composition in the same framework. Tradeoff: It has more server/client, cache and deployment choices than a conventional integrated CRUD workflow.
  Sources: [Next.js App Router](https://nextjs.org/docs/app)
- Separate browser client and API `typescript-react-vite-browser`: An API already owns identity, permissions and data, or the product has a clear independent frontend/backend boundary. Tradeoff: React + Vite is frontend-only and does not replace backend responsibilities.
  Sources: [React: Start a New React Project](https://react.dev/learn/start-a-new-react-project); [Vite guide](https://vite.dev/guide/)
- Live connected web application `elixir-phoenix-liveview`: Connected multiuser state, realtime interaction or Elixir/OTP operational fit is central. Tradeoff: Qualify authorization, reconnects, fanout, persistence and overload with representative workload; no capacity is implied.
  Sources: [Phoenix LiveView documentation](https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html)
- Full-stack Svelte application: The team has a concrete Svelte/SvelteKit ecosystem preference and wants its routing and server/client application model. Tradeoff: There is no curated Stack Menu profile here; validate the current adapter, rendering and server boundary before choosing it.
  Sources: [SvelteKit introduction](https://svelte.dev/docs/kit/introduction)
- Full-stack Vue application: The project or team is materially invested in Vue/Nuxt and wants an integrated full-stack application framework. Tradeoff: There is no curated Stack Menu profile here; validate the current Nuxt version, modules, deployment adapter and server/client boundary.
  Sources: [Nuxt tutorial](https://learn.nuxt.com/en)
- Typed React routing and server functions: Only when type-safe file-based routing or framework-provided server functions directly solve a stated requirement and the project owner wants a JavaScript/TypeScript alternative. Tradeoff: TanStack Start 1.0 is stable, but there is no curated Stack Menu profile. Check its runtime adapters, server boundary and documentation for the chosen version; it is a conditional research lead, not a default or a reason to migrate a healthy application.
  Sources: [TanStack Start 1.0 announcement](https://tanstack.com/blog/tanstack-start-1-0); [TanStack Start documentation](https://tanstack.com/start/latest/docs/framework/react/overview)

### Collaborative web application (`live-web`)

Primary profile: `elixir-phoenix-liveview`.

Phoenix and LiveView are a strong default when multiple connected users need server-owned live interface state and the product benefits from the Elixir process and PubSub model.

Tradeoff: Persistent connections, state ownership, authorization, reconnects, fanout, overload and deployment need deliberate design and workload qualification; this recommendation does not claim a capacity limit.

Ecosystem constraints: `elixir`.

Sources: [Phoenix LiveView documentation](https://phoenix-live-view.hexdocs.pm/); [Phoenix PubSub](https://hexdocs.pm/phoenix_pubsub/Phoenix.PubSub.html)

Other scoped alternatives:
- Integrated server-rendered application `rails-hotwire-postgresql`: The collaboration is primarily CRUD/workflow and ordinary server interactions are sufficient; live updates are a smaller feature rather than the product's central behavior. Tradeoff: Reassess if shared live state, frequent presence or high fanout is central.
  Sources: [Getting Started with Rails](https://guides.rubyonrails.org/getting_started.html)

### Data administration (`admin-web`)

Primary profile: `python-django`.

Django is a strong starting point when staff need to manage relational records through a model-based administration interface, forms and permissions. Its built-in admin reduces the amount of custom interface work for that job.

Tradeoff: The admin is intended for trusted staff and model-based workflows. A bespoke customer-facing workflow may fit a general web product better; substantial admin customization can also erase the initial advantage.

Ecosystem constraints: `python`, `php`, `elixir`, `react`, `ruby`.

When `ecosystem=python`, use `python-django`: Python is an explicit team or ecosystem requirement, and Django’s relational data, forms and staff administration fit the application.
Tradeoff: Django’s admin is a staff tool; product permissions and domain workflows still need deliberate design.
Sources: [Django overview](https://docs.djangoproject.com/en/stable/intro/overview/)

When `ecosystem=php`, use `laravel-livewire-postgresql`: PHP or an existing Laravel estate is a material constraint, and integrated Laravel workflows fit.
Tradeoff: The application process, workers and scheduler have separate operating needs.
Sources: [Laravel starter kits](https://laravel.com/docs/starter-kits)

When `ecosystem=elixir`, use `elixir-phoenix-liveview`: The application must fit an Elixir estate or benefits from Phoenix’s connected server-owned interaction model.
Tradeoff: Persistent connections, authorization, fanout and overload need workload-specific design.
Sources: [Phoenix LiveView documentation](https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html)

When `ecosystem=react`, use `typescript-next-node`: A React-led full stack is an explicit requirement and Next.js server/client composition fits the product.
Tradeoff: Server/client boundaries, caching and deployment add choices beyond an integrated CRUD workflow.
Sources: [Next.js App Router](https://nextjs.org/docs/app)

When `ecosystem=ruby`, use `rails-hotwire-postgresql`: The existing Ruby team or application can own the administration workflow within Rails rather than adding a separate Python application.
Tradeoff: Choose and qualify the administration interface and permissions explicitly rather than assuming a built-in Django-style admin.
Sources: [Getting Started with Rails](https://guides.rubyonrails.org/getting_started.html)

Sources: [Django admin site](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)

Other scoped alternatives:
- PHP product application `laravel-livewire-postgresql`: The team or existing system is PHP/Laravel-centered and the integrated Livewire/auth/queue conventions fit. Tradeoff: The web process, queue workers and scheduler have separate operating needs; browser/client-heavy work may need a distinct client.
  Sources: [Laravel starter kits](https://laravel.com/docs/starter-kits)
- Integrated server-rendered product application `rails-hotwire-postgresql`: A conventional integrated product matters more than Python-native data tooling or Django's administration workflow. Tradeoff: This is not the same as adopting Django's built-in admin; design product-facing authorization and workflows explicitly.
  Sources: [Getting Started with Rails](https://guides.rubyonrails.org/getting_started.html)
- Full-stack React application `typescript-next-node`: The interface is intentionally React-led and the team wants route handlers and server/client React composition in the same framework. Tradeoff: It has more server/client, cache and deployment choices than a conventional integrated CRUD workflow.
  Sources: [Next.js App Router](https://nextjs.org/docs/app)
- Separate browser client and API `typescript-react-vite-browser`: An API already owns identity, permissions and data, or the product has a clear independent frontend/backend boundary. Tradeoff: React + Vite is frontend-only and does not replace backend responsibilities.
  Sources: [React: Start a New React Project](https://react.dev/learn/start-a-new-react-project); [Vite guide](https://vite.dev/guide/)

### Web frontend for an existing API (`browser-client`)

Primary profile: `typescript-react-vite-browser`.

React with Vite is a strong default when the browser UI is the deliverable and an existing or separately owned API already handles identity, permissions, data and durable work.

Tradeoff: The profile is a frontend, not a backend. Routing, server state, authentication integration and offline synchronization remain separate choices and contracts.

Ecosystem constraints: `react`.

Sources: [React: Start a New React Project](https://react.dev/learn/start-a-new-react-project); [Vite guide](https://vite.dev/guide/)

### API or backend service (`api-service`)

Primary profile: `go-service`.

Go is a strong default for a standalone HTTP API or service when a small, explicit service boundary and straightforward binary deployment fit the team and operations model.

Tradeoff: Authentication, permissions, persistence conventions, administration and durable jobs require deliberate assembly; a product framework or Python integration ecosystem may reduce unrelated work.

Ecosystem constraints: `python`, `rust`.

When `ecosystem=python`, use `python-fastapi`: Python SDKs, data libraries or existing Python services are material, and typed HTTP contracts/OpenAPI fit.
Tradeoff: Authentication, persistence, migrations and durable work remain explicit integrations.
Sources: [FastAPI features](https://fastapi.tiangolo.com/features/)

When `ecosystem=rust`, use `rust-service`: Rust libraries, existing ownership or demonstrated resource constraints materially justify Rust.
Tradeoff: Runtime and type complexity require an experienced owner and measured reason.
Sources: [axum documentation](https://docs.rs/axum/latest/axum/)

Aliases: `python-api` means this task with ecosystem=python.

Sources: [Go net/http package](https://pkg.go.dev/net/http); [Writing Web Applications in Go](https://go.dev/doc/articles/wiki/)

Other scoped alternatives:
- Rust HTTP service `rust-service`: A measured resource or latency constraint, an existing Rust service boundary, or a required Rust library justifies the language and asynchronous service model. Tradeoff: The curated Rust service guide starts with Cargo and treats Axum, Tokio and database integrations as explicit composition choices. Measure the reason to accept their runtime and type complexity.
  Sources: [axum documentation](https://docs.rs/axum/latest/axum/)
- TypeScript API on Cloudflare Workers: The API is intentionally deployed to Cloudflare Workers and the team wants a Web Standards-based TypeScript routing layer. Tradeoff: Runtime APIs, storage, background work and limits are provider-specific; there is no curated Stack Menu profile for this deployment.
  Sources: [Hono on Cloudflare Workers](https://hono.dev/docs/getting-started/cloudflare-workers)
- Python data and API application `python-django`: The API is closely tied to relational product data, forms, staff administration or conventional Django workflows. Tradeoff: Django's product framework can be broader than a narrow stateless service needs.
  Sources: [Django overview](https://docs.djangoproject.com/en/stable/intro/overview/)
- Python API framework `python-fastapi`: The service specifically benefits from Python integrations, typed request/response models or OpenAPI generation. Tradeoff: Choose Go for a general standalone API when Python's ecosystem is not a material need; FastAPI still needs explicit auth, persistence and jobs.
  Sources: [FastAPI features](https://fastapi.tiangolo.com/features/)

### Command-line tool (`cli`)

Primary profile: `go-cli`.

Go is a strong default for a command-line product that should ship as a compiled binary across supported operating systems and architectures.

Tradeoff: Cross-compilation, platform behavior, packaging, terminal interaction and release signing still need target-specific verification; choose a script-oriented profile for bounded automation instead.

Ecosystem constraints: `rust`.

When `ecosystem=rust`, use `rust-cli`: A required Rust library, existing Rust ownership or demonstrated resource-control need materially justifies Rust.
Tradeoff: Rust adds language, tooling and cross-compilation complexity.
Sources: [The Rust Programming Language](https://doc.rust-lang.org/book/)

Sources: [Go command documentation](https://go.dev/doc/cmd); [Cobra documentation](https://cobra.dev/docs/)

Other scoped alternatives:
- Rust command-line product `rust-cli`: A Rust library or measured resource-control requirement materially benefits the product and the team can own Rust tooling and target verification. Tradeoff: Rust adds language, tooling and cross-compilation complexity; use Go for conventional compiled distribution when those constraints do not matter. An asynchronous runtime is an additional choice only when the workload needs it.
  Sources: [The Rust Programming Language](https://doc.rust-lang.org/book/)

### Automation or integration (`automation`)

Primary profile: `python-scripts-workers`.

Python is a strong default for scheduled scripts, provider integrations, data transformations and workers when its SDK and data ecosystem directly serve the task.

Tradeoff: Persistent work needs an operated worker or workflow platform, bounded retries and idempotent external effects; a one-off script should stay small.

Ecosystem constraints: `python`.

Sources: [Python tutorial](https://docs.python.org/3/tutorial/); [Python logging cookbook](https://docs.python.org/3/howto/logging-cookbook.html)

### Mobile app (`cross-platform-mobile`)

Primary profile: `expo-react-native`.

Expo is a useful starting point for a React/TypeScript mobile application, especially when one codebase should serve iOS and Android. Confirm the intended platforms and native capabilities before settling the client architecture.

Tradeoff: Native module compatibility, app lifecycle, platform-specific behavior, signing and store release need qualification on each intended platform; use a native profile when platform APIs or experience dominate.

If the mobile platform is omitted, this primary is provisional. Ask whether the client is shared or platform-specific; do not exclude suitable single-platform clients until that is known.

Mobile platform constraints: `shared`, `ios`, `android`.

When `mobile_platform=ios`, use `swift-swiftui-ios`: The application targets iOS specifically, or Apple platform APIs and native interaction define the client.
Tradeoff: Android requires a separately owned client; builds and distribution require Xcode and Apple platform ownership.
Sources: [Apple SwiftUI documentation](https://developer.apple.com/documentation/swiftui)

Alternatives for this platform choice:
- Flutter mobile application: Dart and Flutter fit the team's skills, UI needs and required capabilities on the intended mobile platforms. Tradeoff: There is no curated Stack Menu Flutter profile; verify plugin support, platform behavior, tooling and release paths for each intended platform.
  Sources: [Flutter multi-platform development](https://docs.flutter.dev/platform-integration)
- Expo + React Native `expo-react-native`: A React/TypeScript team wants a React Native client and its required native modules and interaction model fit the intended platform. Tradeoff: Qualify native APIs, platform behavior, builds and release ownership on every intended platform; using Expo does not require shipping an Android and an iOS client.
  Sources: [Expo documentation](https://docs.expo.dev/); [React Native: Get started with a framework](https://reactnative.dev/docs/getting-started-with-a-framework)

When `mobile_platform=android`, use `kotlin-compose-android`: The application targets Android specifically, or Android lifecycle, device APIs and native UX define the client.
Tradeoff: iOS requires a separately owned client; device diversity and release qualification remain Android-specific.
Sources: [Android Jetpack Compose documentation](https://developer.android.com/develop/ui/compose)

Alternatives for this platform choice:
- Flutter mobile application: Dart and Flutter fit the team's skills, UI needs and required capabilities on the intended mobile platforms. Tradeoff: There is no curated Stack Menu Flutter profile; verify plugin support, platform behavior, tooling and release paths for each intended platform.
  Sources: [Flutter multi-platform development](https://docs.flutter.dev/platform-integration)
- Expo + React Native `expo-react-native`: A React/TypeScript team wants a React Native client and its required native modules and interaction model fit the intended platform. Tradeoff: Qualify native APIs, platform behavior, builds and release ownership on every intended platform; using Expo does not require shipping an Android and an iOS client.
  Sources: [Expo documentation](https://docs.expo.dev/); [React Native: Get started with a framework](https://reactnative.dev/docs/getting-started-with-a-framework)

Aliases: `ios` means this task with mobile_platform=ios; `android` means this task with mobile_platform=android.

Sources: [Expo documentation](https://docs.expo.dev/); [React Native: Get started with a framework](https://reactnative.dev/docs/getting-started-with-a-framework)

Alternatives for shared or undecided mobile scope:
- Separate native iOS and Android clients: Both iOS and Android are required, and platform-first experience, native APIs or lifecycle behavior justify separately owned native clients. Tradeoff: This is a two-client composition with separate delivery and verification paths; compare it with a shared client only after confirming that both platforms are needed.
  Sources: [Apple SwiftUI documentation](https://developer.apple.com/documentation/swiftui); [Android Jetpack Compose documentation](https://developer.android.com/develop/ui/compose)
- Flutter mobile application: Dart and Flutter fit the team's skills, UI needs and required capabilities on the intended mobile platforms. Tradeoff: There is no curated Stack Menu Flutter profile; verify plugin support, platform behavior, tooling and release paths for each intended platform.
  Sources: [Flutter multi-platform development](https://docs.flutter.dev/platform-integration)

## Apply the recommendation

Use the job as an editorial starting point. Apply hard constraints before recommending its primary; explain a conflict rather than silently relaxing the requirement. Read /selection-index.json and the finalist's complete guide. The kind, ui and host fields describe curated compositions, not every theoretical use of a language. Static browser output does not supply a backend, and an offline client still needs storage, synchronization and conflict rules.

Explain the recommended composition, the requirements favoring it, its drawback and any conditional alternative whose stated trigger applies. Ask only unresolved questions that change the decision; use information already present in the conversation. For unknown or uncovered jobs, research beyond this catalogue. Existing healthy stacks remain valid for deliberate selection and rewrites; they are not obsolete because another profile is the task default.

Return requirements satisfied or unresolved, selected tools by actual job, current primary documentation and versions, checks actually executed and a representative qualification plan. No measured cross-stack ranking or guaranteed capacity is claimed.
