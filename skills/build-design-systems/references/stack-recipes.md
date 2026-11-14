# Stack recipes

Each recipe maps the loop's parts to tools that exist on that stack. If the product uses a stack that is not
here, find the same five parts: token generator, gallery, script control, headless picture, picture compare.
Check the tool's current docs before you set it up; versions change.

## Web (React, Vue, Svelte, Solid)

- Tokens: Style Dictionary, or a small generator script in the repo, writes CSS variables (one block per theme)
  and a typed module.
- Gallery: Storybook (or Ladle, Histoire). Theme and reduced motion are globals; a story opens by URL
  (`iframe.html?id=<story-id>&globals=theme:dark`). A plain `/gallery?story=&theme=&bare=1` route also works.
- Pictures: Playwright. Set `reducedMotion: 'reduce'`, a fixed viewport and `deviceScaleFactor`, and wait for
  `document.fonts.ready`. Compare with `toHaveScreenshot` (`maxDiffPixelRatio`, `threshold`); update with
  `--update-snapshots`.
- One machine: run the pictures in the Playwright Docker image, so fonts and the renderer do not change.
- Lint: an Oxlint rule (anti-slop plugin) for colour and size literals; Stylelint for CSS files.

## Rust desktop (GPUI)

- Tokens: a generator crate writes a Rust module and the theme files; its tests fail when the output is stale.
- Gallery: its own binary crate. Environment variables pick the story, theme, bare mode, reduced motion, size
  and zoom.
- Pictures: a tool starts the gallery under Xvfb with Mesa's software Vulkan (lavapipe), takes the window, and
  trims it to what the story draws. Several stories run at once, each on its own display.
- Tests: GPUI's test context with `debug_bounds("<id>")` and simulated clicks find and press elements by id.
- Windows-only product: Xvfb does not exist. Try, in order: a gallery test that renders offscreen, a hidden
  window captured with `PrintWindow`, a visible window at 1x captured on one named PC. Prove the method twice
  (same bytes) before you build on it. Bundle the fonts: Windows system fonts differ between PCs.
- Reference build: Ace (`crates/ui`, `crates/gallery`, `tools/internal/commands/gallery`).

## iOS (SwiftUI)

- Tokens: a generator writes a Swift file (colours as assets per appearance, type styles, motion presets).
- Gallery: an app target that lists every view; launch arguments pick the story and appearance.
- Pictures: swift-snapshot-testing (`assertSnapshot(of:as: .image(...))`) on one pinned simulator model and OS
  version. Read `accessibilityReduceMotion` from the environment in each animation.

## Android (Jetpack Compose)

- Tokens: a generator writes Kotlin (a `ColorScheme` per theme, type styles, motion specs).
- Gallery: Showkase, or a debug activity that lists every composable with its states.
- Pictures: Paparazzi or Roborazzi render on the JVM with no device, so pixels stay the same.

## Flutter

- Tokens: a generator writes a `ThemeData` extension per theme.
- Gallery: Widgetbook.
- Pictures: golden tests (`matchesGoldenFile`, or Alchemist) on one pinned platform, with bundled fonts.
