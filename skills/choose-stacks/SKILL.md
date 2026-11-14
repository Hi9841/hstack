---
name: choose-stacks
description: Pick the framework and tech stack for a new app, site or tool, using the owner's lean picks (Astro, Vite + React + Hono, SvelteKit, React Router v7) before Next.js, native GPU desktop options (GPUI, GPUI Kit, GPUI Fast, zgx, MyGo), and a local mirror of the Stack Menu library. Use when starting a project, comparing stacks, asking "which framework", reconsidering Next.js, or choosing a GUI framework for a Rust or Go desktop app.
---

# Choose Stacks

Pick the lightest stack that does the job, name the requirement behind the pick, and hand off to the right generator and guide.

## Workflow

1. **Read the context first.** Take requirements from the conversation and the repository (README, manifests, lockfiles). If a stack already exists or the user chose one, keep it and go to step 4. Ask only for the one missing fact that changes the pick.
2. **Name the main job.** Choose one: content site, web app, API or service, CLI or TUI, automation, mobile, or native desktop. When a product has parts with different jobs (for example a web frontend, an API and a desktop client), pick and answer per part, then say how the parts connect.
3. **Pick by job.**
   - Web or server: read [references/owner-picks.md](references/owner-picks.md). Its picks win over Stack Menu defaults.
   - Native desktop (GPUI, GPUI Kit, GPUI Fast, zgx, MyGo, others): read [references/native-desktop.md](references/native-desktop.md).
   - Any other job (Rails, Django, Phoenix, Go, Rust, FastAPI, Python workers, mobile): read `references/stack-menu/choose.md`, then `recommendations.json` for the primary and its conditional alternatives.
4. **Read the chosen guide.** Open one file from `references/stack-menu/stacks/` (layout and link map in [references/stack-menu/README.md](references/stack-menu/README.md)). Guides are 30-110 KB: list the headings with `grep -n "^## "`, then read Fit, Choose something else when, and the command lines in Generators (skip its workflow boilerplate). If the pick has no local guide, say so and read the official documentation. Native desktop has no guide: `native-desktop.md` is the guide, and the framework's own documentation supplies the setup.
5. **Generate, do not hand-write.** Use the guide's Generators section to choose the official initializer, check its installed-version help, and run it into an empty directory. `references/stack-menu/generators.json` holds the full records: search it by stack id, do not read it whole.
6. **Migration or rewrite:** read `references/stack-menu/rewrite/guide.md` and the source note. Compare "keep the stack", "replace one part" and "staged coexistence" before you recommend a full rewrite.

## Answer

Done means the answer holds four items, each in one or two lines:

- The pick, and the stated requirement that decided it.
- One drawback.
- The nearest alternative you rejected, and why.
- Unresolved evidence: untested OS, unmeasured speed or memory, unverified versions.

## Rules

- A language preference narrows the pick. It does not replace the job.
- Resolve versions from current official documentation. The mirror was reviewed in October 2026 and is not proof that a setup works.
- Quote a speed or memory number only if you measured it on the target machine.
- Do not switch a chosen stack silently. If a hard constraint breaks the pick, say so and ask.
