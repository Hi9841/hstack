# Native desktop: Rust GUI and Go GUI

Use this file when the product is a desktop application with GPU-drawn UI and no web view. Stack Menu does not cover desktop. This file does.

## Options

| Option | Language | What it is | Pick when |
| --- | --- | --- | --- |
| GPUI | Rust | Zed's GPU UI framework. crates.io has `gpui` 0.2.2, which is far behind Zed `main`. | You want the most proven GPU UI model and accept Zed-driven API changes. |
| GPUI Kit | Rust | A component and theme layer on GPUI (75+ components, 38 theme presets). | You want finished components on GPUI. Use the `build-gpui-apps` skill for the work. |
| GPUI Fast | Rust | A GPUI build consumed as `gpui = { package = "gpui-fast" }`. The zgx benchmarks call it the faster of two GPUI configurations. | The app is already on GPUI and needs more speed. Check the source and the license first: no public crate page was found on 2026-11-08. |
| zgx | Rust, or Luau scripts | Retained-mode GUI with fine-grained signals, wgpu renderer (Metal, Direct3D 12, Vulkan), flexbox and grid layout, Luau hot reload. MIT, repo `zeronsh/zgx`. Version 0.1: young, API still changes. | Idle cost and memory matter, you want hot reload, and you accept an early API. |
| MyGo | Go | Pure Go desktop framework, no cgo. Native UI is drawn on the GPU (Metal, Direct3D 11, OpenGL). A system web view is optional. MIT, repo `egoist/mygo`. | The team prefers Go, wants a single static binary, and the UI is not very large. |
| Rune | Rust | Retained tree on wgpu and winit, Taffy layout, Parley text. MIT, repo `anomalyco/rune`. | Only after a spike. The zgx comparisons pin it and apply a local patch, so check its maturity first. |
| Iced, egui, Slint, Qt 6 | Rust, Rust, Rust or C++/JS/Python, C++/QML | Established cross-platform toolkits. Retained or immediate model. | You need a mature toolkit with a visual tool (Slint, Qt) or the simplest immediate-mode tool UI (egui). |
| Tauri, Electron | Rust or JS + web UI | Web UI in a system web view or bundled Chromium. | The UI is already a web app, or web-only libraries are required. |

Facts above come from the zgx README and comparison docs (`zeronsh/zgx`), the MyGo README and package docs, and the GPUI Kit comparison page. Re-read them before you rely on a detail: all of these projects move fast.

## Decision order

1. **Existing app:** keep its framework. Changing the GUI framework is a rewrite. Run a spike first (one window, the heaviest real screen, the target OS) and judge the result before any port.
2. **Language:** Rust team or Rust core code leads to GPUI, GPUI Kit or zgx. Go team leads to MyGo. Do not pick across languages for speed alone.
3. **Platform:** list the required OSes first. Check that the framework has proven support for each one on that OS, not only a claim in the README. Windows needs its own check: some benchmark suites run on macOS only.
4. **Components:** if finished components, themes and docs matter most, choose GPUI Kit. If the framework is young (zgx, MyGo, Rune), plan to build missing controls.
5. **Cost profile:** if idle CPU, memory or battery matter, spike zgx or a retained design against GPUI with a real screen of the app.
6. **Risk:** a 0.x framework needs a pinned version, an upgrade budget and an exit path (keep UI-free core logic in a separate crate or package).

## Default

When no requirement decides: Rust team, finished components wanted, GPUI Kit. Go team, MyGo. Say the pick is a default, and name the spike that would change it (the heaviest real screen, on the target OS, measuring idle CPU and memory).

## Rules

- Benchmarks from a framework's own repository are vendor claims. The zgx comparisons are run by the zgx author on macOS. Reproduce on the target OS with the real screen before you quote a number (see the `benchmark-checklist` skill).
- Keep domain logic out of the UI layer so the GUI framework can change later.
- Name unresolved evidence in the answer: untested OS, untested IME or accessibility, unverified licenses, version drift.
- GPUI work: follow `build-gpui-apps`. Ask before adopting GPUI Kit.
