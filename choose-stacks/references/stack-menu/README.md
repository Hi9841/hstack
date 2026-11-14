# Stack Menu mirror

Local copy of the Stack Menu library (https://stack.menu/library/), fetched 2026-11-08. It holds 16 curated stack guides and the shared routing data. It does not update itself.

- Source: https://stack.menu/ (entry point: https://stack.menu/llms.txt, kept as `meta/llms.txt`).
- License: Copyright 2026 Optimum Tech, LLC, Apache-2.0. Keep `LICENSE-elixir-menu.txt` and `NOTICE-elixir-menu.txt` with the mirror.
- Review dates: guides were documentation-reviewed in October 2026 (`meta/research-freshness.json`). That is not execution evidence. Resolve installed versions from current official documentation before you build.
- Not mirrored: `llms-full.txt` (738 KB bundle of the same guides) and per-stack `record.json` files (JSON form of the same guides).

## Layout

```
stack-menu/
  choose.md             read first for a new stack: requirement checklist, task defaults
  recommendations.json  the same defaults as data, with conditional alternatives
  generators.json       official initializer records (180 KB: search by stack id, do not read whole)
  stacks/<id>.md        one guide per stack (30-110 KB: read the headings you need)
  rewrite/              migration guide, contracts, source-stack notes
  meta/                 site plumbing: coverage, index, freshness, routing endpoint, entry files
  LICENSE / NOTICE      required with the copy
```

## Reading a stack guide

Each guide has the same headings: Application role, Use cases, Fit, Choose something else when, Agent workflow, Best practices, Generators, Tools, Architecture and developer workflow, Transition options, Setup, Verification, Open questions, Sources. List them with `grep -n "^## "`. Read Fit, Choose something else when and Generators first. Read the rest only as the task needs.

## Link mapping

The files use root-relative links from the original site. Map them like this:

| Link in the file | Local file |
| --- | --- |
| `/stacks/<id>/guide.md` | `stacks/<id>.md` |
| `/choose.md`, `/recommendations.json`, `/generators.json` | same name in the mirror root |
| `/rewrite/...` | same path under `rewrite/` |
| `/agents/guide.md` | `meta/agent-guide.md` |
| `/agents/routing.md` | `meta/routing.md` |
| `/coverage.json`, `/selection-index.json`, `/research-freshness.json`, `/context.schema.json`, `/examples/...`, `/llms.txt` | same name under `meta/` |
| `/stacks/<id>/` and `/rewrite/sources/<name>/` (page links with a trailing slash) | `stacks/<id>.md` and `rewrite/sources/<name>.md` |
| `/route` (POST endpoint), `/llms-full.txt`, `/about/` | not mirrored; use `choose.md` instead |

## Stack ids

`astro-content`, `elixir-phoenix-liveview`, `typescript-next-node`, `typescript-react-vite-browser`, `rails-hotwire-postgresql`, `laravel-livewire-postgresql`, `python-django`, `go-service`, `rust-service`, `python-fastapi`, `go-cli`, `rust-cli`, `python-scripts-workers`, `swift-swiftui-ios`, `kotlin-compose-android`, `expo-react-native`.
