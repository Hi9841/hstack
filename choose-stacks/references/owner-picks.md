# Owner picks: web and server

These picks override the Stack Menu editorial defaults. Stack Menu lists Next.js as one profile among many. The owner no longer uses it as the default for everything.

## Why

Next.js for every job costs build time and server memory. A small VPS feels this first. Pick the lightest stack that does the job. Move up one step only when a stated requirement forces it.

## Picks by job

| Job | Pick | Notes |
| --- | --- | --- |
| Landing page, docs, blog | Astro, static output | No server at run time. Host on any static host or CDN. |
| A handful of rarely edited pages | Plain HTML and CSS | Use Astro once shared layouts or a content workflow appear. |
| Content with a few dynamic parts | Astro with the Node adapter | Keep pages static. Make only the dynamic routes server-rendered. |
| Dashboard, SaaS | Vite + React frontend, Hono API | Two small parts, one deploy each or one process that serves both. |
| One framework for UI and server | SvelteKit, or React Router v7 | Choose SvelteKit when the team has no React need. Choose React Router v7 when the React ecosystem or existing React code matters. |
| Next.js | Only on a named requirement | Examples: an existing Next.js code base, or a library that needs it. Say which requirement. |

## Stack Menu profile to read per pick

| Pick | Closest local guide | Gap |
| --- | --- | --- |
| Astro static, Astro + Node adapter | `stack-menu/stacks/astro-content.md` | Read the server-rendering and adapter parts for the Node adapter. |
| Vite + React frontend | `stack-menu/stacks/typescript-react-vite-browser.md` | The guide covers the browser app only. |
| Hono API | None. Closest: `typescript-next-node.md` (API parts), `go-service.md` (service shape) | Read the current Hono docs for the runtime, validation and RPC client. Do not copy Next.js route patterns. |
| SvelteKit | None | Read the current SvelteKit docs and its `sv create` generator. |
| React Router v7 | None. Closest: `typescript-react-vite-browser.md` | Read the current React Router framework-mode docs. |

For picks with no local guide, say so in the answer and cite the official documentation you read. Do not invent a profile.

## Rules

- Start from the lowest row that meets the stated requirements. Name the requirement that forces each step up.
- Package manager: pnpm if `pnpm-lock.yaml` exists, else Bun.
- Run the official generator for the pick into an empty directory. Do not hand-write the framework skeleton. The Generators section of each Stack Menu guide lists the initializers for the profiles it covers.
- Measure before you claim a saving. "Faster builds" and "less RAM" are the reasons for the picks, not results. Time the build and read the resident memory of the real app (see the `benchmark-checklist` skill).
