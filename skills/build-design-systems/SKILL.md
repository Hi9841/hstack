---
name: build-design-systems
description: Set up a product's design system as one checked loop - a gallery app that shows every UI state and that a script opens on one story and theme, headless screenshots, committed reference pictures of the key pages, one token source, a component package that takes plain data, and guard tests and ratchets behind one check command. Use when a product needs a component gallery or Storybook, a way to see and test every UI state, design tokens or themes, visual regression or golden screenshots, or "the same UI system as Ace" for another app.
---

# Build design systems

Build the loop, not only the parts. A design system works when an agent changes a component, sees it in the
*gallery*, takes a picture of it with no screen, and gets a red check when it breaks a rule or moves a page.
Value comes from the gallery first: the person sees every UI state in one window. Ace (Rust and GPUI) is the
reference build; read it when you can reach it, but use the product's own stack.

## Workflow

Order sets what you build first, not what you tell the user: report a finding that changes the plan at once.

1. **Read the product.** Find the renderers, the UI code, the theme or colour file, the test runner, the CI,
   the target platforms, and what exists already: a preview mode, frozen states, fixtures, a Storybook,
   snapshot tests, a screenshot habit. Pick the stack recipe in
   [references/stack-recipes.md](references/stack-recipes.md). If its headless method does not fit the
   product's platform, mark the picture method as unproven.
   Done when you can list what exists for each part of the loop, with file paths.

2. **Gallery window first.** This is the first thing you ship, before pictures, tokens or guards. With no
   restructure, build a window that lists every state the product can already show (reuse its preview mode
   and fixtures) and draws the one the person picks; a script opens it on one story with no clicks. A plain
   list is enough; groups and search come in step 5.
   Done when the user can open the window and click through every existing state.

3. **Tracer bullet for pictures.** One picture of one story, taken twice with the same bytes; one committed
   reference that goes red when a colour of that story changes. If the picture method is unproven, prove it in
   a scratch folder; the gallery from step 2 does not wait on it. If no method works, say so and keep the
   gallery.
   Done when the three checks ran red and green.

4. **Ask before you restructure.** Moving UI into its own package, making a workspace, adding a theme, adding
   a token generator, or replacing an existing preview system changes the product's layout. Show the user
   what it gives and what it costs, and do it only with a yes. Never put it in the tracer bullet.

5. **Widen the gallery.** A story for every component and screen, in every state: empty, loading, long
   text, many items, error, disabled, picked. Stories sit in groups, with search, and a theme picker when the
   product has more than one theme. Script
   control: story, theme, bare (no sidebar), reduced motion, size, zoom, open menus. Fixed fixtures: no clock,
   no network, no random value.
   Done when a test fails if a screen or state the product can show has no story.

6. **Pictures and references.** Commands: one story (`shot STORY THEME OUT.png`), every story
   (`shots THEME DIR`), and a short video for motion. Commit references for the pages a person looks at, in
   each theme the product ships. Compare with a tolerance (share of pixels moved by more than a small channel
   step); fail on a missing picture, a changed size or a move; `--update` writes them in the same commit.
   Done when a change to one token turns a page red, and a clean run is green twice.

7. **One token source.** Every colour, size, radius, type style (size, line, weight and face as one named
   style) and motion preset has one owner. Size it to the product: one renderer can keep its theme file as
   the owner; a JSON file with generators earns its cost only when two or more renderers or a design tool
   read the tokens. Add a theme only when the user wants it.
   Done when no colour or size is set outside the owner, or a ratchet counts the ones left.

8. **Guards.** Add the guards in [references/guards.md](references/guards.md) that this product needs.
   Done when each guard was broken on purpose, went red, and was reverted.

9. **One check command and the rules.** One command runs the tests, the gallery build and its tests, the
   guards and the references; it runs only what a change can affect and builds from the commit. Write the
   rules in the repo's agent file: build UI from the shared parts; colours and sizes come from the token
   owner; a new component gets a story; a change that moves pixels updates the references in the same commit;
   ratchets only go down.

## Rules

- Ask the user only what the repo cannot answer (which machine writes the pictures, a new theme, a
  restructure). Decide the rest yourself and state your choice.
- Measure before you cite a number. A count that justifies a guard or a ratchet comes from the exact
  pattern the guard will use, run on the repo, not from an estimate.
- Extend what exists. A preview mode becomes the gallery's source of stories; do not delete it until the
  gallery covers it and the user agrees.
- A ratchet lets old code stay while new code cannot add more. Never block the loop on a full clean-up.
- Flaky pictures come from motion, a blinking caret, the clock, late fonts, GPU drivers and screen scale. Fix
  the source (reduced motion, fixtures, bundled fonts, a software renderer, one named machine at 1x); never
  raise the tolerance to hide it. If CI cannot match the picture machine, the picture check runs locally, and
  you tell the user.
- Stories obey the product's rules: no hand-set colour or size in a story.

## Done

Done when the user has the gallery with script control, the picture commands, the committed references, the
guards each proven red once, the one check command and the written rules, plus each restructure the user
approved. Report each part with its command, in 2-4 lines.
