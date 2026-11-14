# Rust CLI + TUI

Portable command-line tools with explicit memory and resource control.

Language: Rust | Reviewed: 2026-10-10 | Evidence: documentation-reviewed research input

Source record: menu/inputs/research/go-rust.json.

Core guidance checked: 2026-10-13. Review sources are listed below. /research-freshness.json describes the imported research packet; this record retains its own evidence scope. These recipes and selected dependency combinations need qualification in the actual project.

## Application role
Components: cli
UI: terminal
Deployment: binary

## Use cases
- Fast native developer tools
- parsers and analyzers
- shipped terminal applications

## Fit
- Need native performance or reuse of Rust libraries
- Want ownership/type checks around complex transformations

## Choose something else when
- Disposable automation would be simpler in Python or shell
- Build latency and cross-toolchains outweigh runtime needs

## Agent workflow
- Read README, dependency manifests, lockfiles, runtime pins and the maintained project workflow before changing anything. Preserve an existing stack unless reconsidering it is part of the request.
- For a new component, read the Generators section before writing application files. Use its appropriate official initializer and retain its generated baseline; follow-up generators are conditional on the selected feature.
- Use this guide to select tools by requirement. Resolve compatible versions from official and installed-version documentation; record the actual lockfile and runtime versions.
- Create a plan for schema changes, identity, authorization, external effects and deployment. A library choice does not complete its integration.
- Run relevant checks after configuration. Exercise the real interface, failure paths and packaged artifact on the intended target. Report commands, versions, results and untested behavior.
- On failure, retain the command and diagnostic, fix the failing prerequisite and resume there. Do not regenerate over existing work or suppress failures to make a check green.

## Best practices
- Keep parsing separate from domain behavior. Test malformed input, pipes, errors and exit codes.
- Use interactive UI only when a terminal is available and the user has requested it.
- Bound resource use and retain error context rather than panicking on expected failures.
- Build with the committed lockfile and verify each supported release target.

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

#### Cargo binary package

Use when: A new Rust CLI needs a new directory.

1. Install the chosen Rust toolchain. Replace /path/to/workspace with the actual local source parent; choose the real package name.
2. Generate a binary package; use --lib only for a reusable library rather than an executable.

Working directory: /path/to/workspace (existing local source parent)

Generate the executable package baseline.

```sh
cargo new project --bin
```

- A Cargo package is not a full framework application. Preserve generated defaults and add only selected dependencies.

#### Cargo in an existing directory

Use when: An existing source directory has no Cargo.toml and must become a package; choose this instead of cargo new.

1. Inspect existing files and parent VCS before initialization; preserve existing code.

Working directory: /path/to/workspace/project (existing directory without Cargo.toml)

Initialize a binary package in place.

```sh
cargo init --bin
```

- Use --lib for a library target. Do not run cargo init over an already initialized package.

#### Ratatui maintained templates

Use when: Interactive terminal UI is selected at project creation; use this alternative to the plain Cargo starter, rather than overlaying a template onto an existing app.

1. Install the selected Rust toolchain; set CARGO_GENERATE_VERSION to a chosen published version and ensure Cargo binaries are on PATH.
2. Run the maintained template selector from the intended parent. Choose the simplest suitable template and real app name; record template choice, resolved repository revision and answers.
3. Review generated dependencies, license and terminal setup before extending the application.

Working directory: /path/to/workspace (existing local source parent)

Install the chosen template generator.

```sh
cargo install cargo-generate --version "${CARGO_GENERATE_VERSION:?Set the selected cargo-generate version}" --locked
```

Working directory: /path/to/workspace (parent of the new app; Git available)

Choose and generate a maintained Ratatui template interactively.

```sh
cargo generate ratatui/templates
```

- These are Ratatui-maintained templates, not a universal Rust CLI scaffold. Their shape depends on the selected template; resolve and retain its revision for repeatability.
- Preserve terminal restoration and error/panic handling; add clap only when the generated template does not already satisfy argument parsing.

### Conditional follow-up generators

#### dist release setup

Use when: Only when dist is selected for shipping binaries and no equivalent release owner exists.


Working directory: /path/to/workspace/project (Rust toolchain installed)

Install the selected dist release from its cargo-dist package.

```sh
cargo install cargo-dist --version "${DIST_VERSION:?Set the selected dist package version}" --locked
```

Working directory: /path/to/workspace/project (application package/workspace root)

Generate release settings and selected CI.

```sh
dist init
```

- Set DIST_VERSION to a chosen published version; ensure Cargo binaries are on PATH. Review target list, metadata, installers, hooks and generated CI before adopting it.
- Release configuration generation does not publish. Test each supported target and installer separately.

#### SQLx migrations and checked-query metadata

Use when: Only when SQLx is selected and owns schema migrations; metadata applies when checked query macros are used.


Working directory: /path/to/workspace/project (matching sqlx-cli installed)

Create an editable migration file.

```sh
sqlx migrate add initial
```

Working directory: /path/to/workspace/project (DATABASE_URL targets a disposable database; migration SQL reviewed)

Apply migrations to the disposable database.

```sh
sqlx migrate run
```

Working directory: /path/to/workspace/project (checked query macros and matching disposable schema available)

Generate offline query metadata.

```sh
cargo sqlx prepare
```

- Install a selected sqlx-cli release compatible with the application and selected database/TLS features. Set DATABASE_URL through the environment or an untracked local file.
- Preserve migrations and commit .sqlx metadata for offline builds. Run cargo sqlx prepare --check after changes; pass workspace/feature/target options matching the project.

### Preserve the generated foundation

- Preserve Cargo.toml, generated source structure and Cargo.lock after dependency resolution for shipped applications. Record the chosen Rust toolchain and generator versions.
- Retain the VCS ignore baseline when generated, including build-output exclusions, and add project-specific OS metadata/secret rules. Cargo VCS behavior depends on parent repository and configuration; inspect actual output.
- Record and justify changes from the same-version generator baseline instead of recreating its files from memory.
- Preserve selected Ratatui template structure, terminal cleanup and license notices; keep generated dist configuration and reviewed CI synchronized.

### Baseline and generation checks

- In the actual application, compare a fresh output from the recorded toolchain/options with the initial project and explain intentional differences.
- After initial dependency resolution, run cargo fmt --all -- --check, cargo test --locked and cargo build --locked from the package root; run the project-selected Clippy checks.
- In a disposable copy, inspect git add --dry-run -A and confirm source/manifests/lockfile are included while target/, credentials and .DS_Store are excluded.
- Test command help, exit codes, piped input/output, interruption and terminal restoration; a successful build is not proof of terminal behavior.

### Generation receipt

- Component and selected starting point, or the documented absence of a full application generator
- Generator/toolchain versions, exact commands or IDE template/settings, working directory and generated destination
- Generated files retained, deliberate deviations with reasons, and required supplemental ignore rules
- Baseline checks and later checks actually run, results and remaining prerequisites or untested behavior

### Generator sources

- [Cargo new](https://doc.rust-lang.org/cargo/commands/cargo-new.html)
- [Cargo init](https://doc.rust-lang.org/cargo/commands/cargo-init.html)
- [Cargo package and first build](https://doc.rust-lang.org/cargo/guide/creating-a-new-project.html)
- [Ratatui templates documentation](https://ratatui.rs/templates/)
- [Ratatui maintained template repository](https://github.com/ratatui/templates)
- [dist installation](https://axodotdev.github.io/cargo-dist/book/install.html)
- [dist release setup and generated CI](https://github.com/axodotdev/cargo-dist)
- [SQLx CLI migrations and prepare](https://github.com/transact-rs/sqlx/blob/main/sqlx-cli/README.md)

## Tools

### Command parsing: clap

Typed commands plus a mature terminal widget/rendering ecosystem.

Limits and integration: Keep domain code separate from rendering and support non-TTY output; restore terminal on errors and interruption.


- https://docs.rs/clap/latest/clap/
- https://ratatui.rs/

Alternatives: A simple std::env argument parser for tiny internal tools

### Terminal UI: Ratatui only for interactive screens

Typed commands plus a mature terminal widget/rendering ecosystem.

Limits and integration: Keep domain code separate from rendering and support non-TTY output; restore terminal on errors and interruption.


- https://docs.rs/clap/latest/clap/
- https://ratatui.rs/

Alternatives: Line-oriented output when no interactive screen is needed

### HTTP client: reqwest

Reusable typed HTTP client APIs.

Limits and integration: Choose blocking or async deliberately; configure timeouts, TLS and response bounds. Never call blocking client inside an async runtime indiscriminately.


- https://docs.rs/reqwest/latest/reqwest/

Alternatives: No network dependency for offline tools

### Persistence and migrations: None for stateless tools

Start without a database; add schema ownership only for persistent products.

Limits and integration: SQLite feature/driver and migration setup require target testing; durable local state is not shared distributed workflow state.


- https://docs.rs/sqlx/latest/sqlx/
- https://github.com/transact-rs/sqlx/blob/main/sqlx-cli/README.md

Alternatives: SQLx with SQLite when local relational state is a real requirement

### Configuration: Serde-backed settings + config

Typed settings plus structured events/spans.

Limits and integration: Set precedence explicitly; validate semantics; install a tracing subscriber; never log secrets.


- https://docs.rs/config/latest/config/
- https://doc.rust-lang.org/std/env/fn.var.html
- https://docs.rs/tracing/latest/tracing/

Alternatives: std::env for a small fixed settings set

### Application logging: tracing + configured subscriber

Typed settings plus structured events/spans.

Limits and integration: Set precedence explicitly; validate semantics; install a tracing subscriber; never log secrets.


- https://docs.rs/config/latest/config/
- https://doc.rust-lang.org/std/env/fn.var.html
- https://docs.rs/tracing/latest/tracing/

### Tests and static checks: cargo test; rustfmt; Clippy; cargo audit

Compiler, style, behavior and known-advisory checks complement each other.

Limits and integration: Audit coverage is advisory-driven; compile success does not establish behavior or security. Test supported feature combinations rather than blindly enabling incompatible features.


- https://doc.rust-lang.org/cargo/commands/cargo-test.html
- https://github.com/rust-lang/rustfmt
- https://doc.rust-lang.org/clippy/usage.html
- https://rustsec.org/
- https://docs.rs/assert_cmd/latest/assert_cmd/

### Executable behavior tests: assert_cmd

Tests real exit codes, stdout/stderr and command contracts.

Limits and integration: Snapshot changes need review; also test actual error and side-effect behavior.


- https://docs.rs/assert_cmd/latest/assert_cmd/
- https://docs.rs/clap/latest/clap/

Alternatives: clap-linked snapshot tools for stable help output

### Durable work: Delegate to a durable service; retain resumable job identity

CLI lifetime does not own remote work lifetime.

Limits and integration: Checkpoint schema, atomic persistence and external idempotency must be designed; async execution alone adds no durability.


- https://docs.rs/restate-sdk/latest/restate_sdk/

Alternatives: Local checkpoints for explicitly local resumable work

### Distribution: dist (formerly cargo-dist) + Cargo release builds

Generates multi-platform release pipelines and installers.

Limits and integration: Review generated CI before tags can publish; test installers and target-native dependencies. Signing and notarization are separate platform work.


- https://github.com/axodotdev/cargo-dist
- https://doc.rust-lang.org/cargo/commands/cargo-build.html

Alternatives: Manual artifacts for one internal target

### Machine-readable output: serde_json

Stable JSON output lets scripts consume commands without parsing terminal text

Limits and integration: Add an explicit --json/output mode and document schema/exit codes; reserve stdout for results, stderr for diagnostics, and disable interactive/color output for pipelines.


- https://docs.rs/serde_json/latest/serde_json/

Alternatives: Preserve an existing compatible project choice

### Cancellation and shutdown: Tokio signal handling for async commands

User interrupts should cancel outbound work and leave terminal/files usable

Limits and integration: Propagate cancellation through work; bound cleanup time and test interrupts during writes. Avoid adding an async runtime to a synchronous Rust CLI solely for signals.


- https://docs.rs/tokio/latest/tokio/signal/index.html

Alternatives: Existing synchronous shutdown strategy in synchronous Rust tools

## Architecture and developer workflow

Recommendation: clap derives/parses a stable command interface, domain operations return Result, and the entry point converts errors to streams/status after cleanup. Serde owns a versioned machine format; Ratatui is an optional terminal client. Cargo/dist prepare artifacts for explicitly supported targets and update channels.

Version scope: Reviewed clap 4.6.7 and Rust std 1.99.0 documentation; Serde, Ratatui and current axodotdev cargo-dist book. Pin rust-toolchain.toml/Cargo.lock and dist version/config. The older opensource.axo.dev book path failed; no target install or release workflow was executed.
Reviewed: 2026-10-11 | Evidence: documentation-reviewed | Source record: inputs/research/migrations-systems.json

### Architecture boundaries

- Recommendation: use a library crate or modules for application operations and a thin binary adapter. Keep clap parsing errors separate from business errors; prefer explicit main ExitCode mapping when the contract requires more than generic failure.
- Recommendation: Serde input/output types carry schema versions. Separate strict user configuration from forward-compatible result reading; deny_unknown_fields is an intentional policy, not universal compatibility.
- Recommendation: encapsulate raw-mode/alternate-screen lifetime and restore the terminal on errors and panics. Share domain operations between Ratatui and a noninteractive JSON mode; interactive render state is not durable application state.
- Recommendation: bounded Rayon/Tokio work is selected by CPU versus I/O needs, with explicit cancellation and effect receipts. A compiled binary reduces interpreter deployment needs but does not remove database, TLS or platform dependencies.

### Tools and feedback

- Recommendation: start from existing Cargo manifest, consumers and rust-toolchain.toml. For a new local package, cargo new tool and cargo add clap --features derive are optional initial steps; add serde --features derive and serde_json only when a machine/config format is required.
- Recommendation: cargo fmt --check, cargo clippy --all-targets -- -D warnings and cargo test --locked verify source checks in the selected feature matrix. Exercise subprocess stdout/stderr/status and panic/interrupt terminal restoration on supported OSs.
- Recommendation: cargo build --release --locked builds one selected target. Inspect its native/TLS dependencies and execute on clean target hosts; --target compilation alone does not qualify distribution.
- Recommendation: with a pinned dist tool, run dist init and review generated configuration/workflows before committing; init can overwrite manual workflow edits. dist plan --output-format=json previews artifact/announcement intent; actual target builds, installers and upgrade/downgrade checks remain required.

### Translations to avoid

- Avoid treating debug-formatted Result errors as a stable machine API; define error codes and schema deliberately.
- Avoid process::exit in cleanup-sensitive paths; terminal restoration and destructors need normal control flow.
- Avoid enabling raw terminal mode for piped/noninteractive invocations; they need predictable streams and no prompts.
- Avoid hand-editing generated dist workflows without recording how customization survives regeneration.

### Architecture sources

- [clap 4.6.7](https://docs.rs/clap/latest/clap/): Parser/derive command definition supports a typed command boundary.
- [clap errors](https://docs.rs/clap/latest/clap/error/struct.Error.html): Usage errors generally print to stderr with code 2; help-like output uses stdout and success.
- [Rust ExitCode](https://doc.rust-lang.org/std/process/struct.ExitCode.html): ExitCode can be returned by main; arbitrary numeric code meanings are platform-specific.
- [Serde container attributes](https://serde.rs/container-attrs.html): deny_unknown_fields rejects unknown inputs and is incompatible with flatten; version policy is application-owned.
- [Ratatui panic hooks](https://ratatui.rs/recipes/apps/panic-hooks/): Terminal restoration must be arranged around error/panic paths.
- [Tokio shutdown](https://tokio.rs/tokio/topics/shutdown): Track/notify/await tasks for planned completion.
- [Tokio blocking tasks](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html): Started blocking tasks cannot be aborted; capacity is a separate concern.
- [dist simple application guide](https://axodotdev.github.io/cargo-dist/book/workspaces/simple-guide.html): init generates config/workflows, can overwrite manual edits, and plan previews artifacts.
- [dist configuration reference](https://axodotdev.github.io/cargo-dist/book/reference/config.html): Targets, installers and CI/download/update settings are configured explicitly.
- [Cargo build](https://doc.rust-lang.org/cargo/commands/cargo-build.html): Locked and target-specific builds have defined semantics; build success is not target execution.

## Transition options

Proposed designs and checks; these are not executed compatibility results.

### CLI and pipe contracts

**Inspect the source:** Record current commands, option defaults, exit codes, stdout/stderr, JSON field names and shell completions consumed by callers.

**During coexistence:** Recommendation: keep an old command adapter and explicit schema version while migrating parsing to clap. Preserve old names/aliases and map new domain errors into the established protocol.

**Target design:** Recommendation: clap plus typed result/error JSON and main ExitCode mapping. clap usage failures use status 2 while help/version uses success; application failures need their own documented policy.

**Rollback:** Recommendation: return consumers to the previous binary/schema while retaining old option adapters. Keep version selection explicit so a rollback does not silently alter JSON meaning.

**Benefits and prerequisites**

- Typed parsing and a stable output envelope make command automation explicit. Requires: Contract fixtures cover old callers; result schemas and error/status mapping are versioned; help/completion behavior is checked. Tradeoffs: Parser defaults can change compatibility; numeric status meanings are not universal across platforms; Rust error types do not define the public protocol.

**Checks before transfer**

- Verify help/version succeed and invalid arguments use the intended stream/code without effects.
- Execute legacy scripts and compare stdout/stderr/status exactly where promised.
- Validate empty, partial and failed JSON results against the advertised schema.

- https://docs.rs/clap/latest/clap/
- https://docs.rs/clap/latest/clap/error/struct.Error.html
- https://doc.rust-lang.org/std/process/struct.ExitCode.html

### Data and schema

**Inspect the source:** Inventory configuration file locations, schema versions, defaults, permissions and old binaries' ability to read newer files.

**During coexistence:** Recommendation: read old config into a versioned internal model and migrate only through an explicit command with backup. Keep concurrent writer ownership explicit; read-only startup must not silently rewrite files.

**Target design:** Recommendation: Serde-tagged/versioned configuration and documented unknown-field handling. Validate a temporary representation before replacing the live file; platform atomicity, permissions and crash behavior require implementation checks.

**Rollback:** Recommendation: restore the preserved old config and binary as a pair. Reconcile new-only fields before using an old reader; avoid destructive in-place downgrade guesses.

**Benefits and prerequisites**

- Explicit config migration decouples executable upgrades from accidental data loss. Requires: Old/new fixtures and semantic transforms exist; backup/restore works; unsupported versions fail before write. Tradeoffs: Strict Serde unknown-field rejection can prevent mixed-version use; deny_unknown_fields does not compose with flatten; replacing a file is not a complete durability protocol.

**Checks before transfer**

- Load old config and compare effective settings after migration.
- Verify unsupported versions and malformed values leave the source unchanged.
- Downgrade the binary with its preserved config and confirm paths/permissions on each target OS.

- https://serde.rs/container-attrs.html

### Jobs and schedules

**Inspect the source:** Preserve ordering, per-item effects, timeout and interrupt semantics for batch/network subcommands.

**During coexistence:** Recommendation: retain sequential mode while qualifying bounded parallel work using dry-run/fixtures. Store item operation IDs and completion receipts before enabling resume against live systems.

**Target design:** Recommendation: a bounded executor selected for CPU or async I/O with cooperative stop, tracked joins and cleanup. Started blocking work needs its own stop protocol or process boundary; do not label a task timeout as effect cancellation.

**Rollback:** Recommendation: use sequential mode with the same receipt format and reconcile unknown outcomes. A previous executable must be able to read checkpoint versions or an explicit converter is required.

**Benefits and prerequisites**

- Bounded parallel execution can overlap independent work without unlimited task creation. Requires: Independent item semantics; capacity/budget limits; stable effect IDs; tested cancellation and resume contract. Tradeoffs: Speed is unmeasured; running blocking tasks may continue; a cancelled remote write can have an ambiguous outcome.

**Checks before transfer**

- Interrupt a batch and verify no new items start, joins are bounded and terminal state restores.
- Simulate a remote success with a lost acknowledgement; resume reconciles rather than duplicating the effect.
- Verify CPU tasks cannot starve I/O and the executor respects the declared capacity.

- https://tokio.rs/tokio/topics/shutdown
- https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html
- https://ratatui.rs/recipes/apps/panic-hooks/

### Delivery and recovery

**Inspect the source:** Capture existing target triples, libc/native dependencies, install path, package metadata and update/downgrade contracts.

**During coexistence:** Recommendation: prepare dist artifacts beside the previous release; review generated CI and installers, and use a prerelease or test channel for target qualification. Do not promise all platforms merely because dist generates a matrix.

**Target design:** Recommendation: pinned dist configuration and Cargo.lock with release artifacts/installers for exercised targets. Keep signing/attestation, system dependency baselines and update channel ownership explicit.

**Rollback:** Recommendation: restore the previous verified package/update channel and retain older installers/checksums. Review data/config compatibility before allowing downgrade; never change a public channel based only on a plan.

**Benefits and prerequisites**

- Generated release plans coordinate binary artifacts and installers across targets. Requires: dist version is pinned; generated workflow is reviewed; native dependencies and every advertised target are exercised. Tradeoffs: dist init may replace generated workflows; OS signing and Linux libc compatibility remain separate obligations; a plan is not build/publication evidence.

**Checks before transfer**

- Inspect dist plan --output-format=json for expected target triples and artifact names.
- Install downloaded artifacts on clean target hosts, including the oldest promised Linux baseline.
- Exercise upgrade/downgrade, PATH behavior, checksum verification and preserved versioned config.

- https://axodotdev.github.io/cargo-dist/book/workspaces/simple-guide.html
- https://axodotdev.github.io/cargo-dist/book/reference/config.html
- https://doc.rust-lang.org/cargo/commands/cargo-build.html

Rewrite workflow: /rewrite/guide.md
Shared contracts and phases: /rewrite/contracts.json


## Setup
1. Complete the selected starting point and baseline checks in the Generators section first; then continue with the integration steps appropriate to the chosen component.
2. After the selected Cargo or Ratatui template baseline, add typed clap arguments when needed with cargo add clap --features derive; preserve equivalent argument parsing already supplied by the chosen template.
3. Resolve Ratatui and its supported terminal backend only when interactive rendering is required; preserve the selected template's compatible setup. Add reqwest only when network access is needed, deliberately selecting blocking or async behavior.
4. Implement typed commands, validated settings, stable output/exit codes and domain logic independent of terminal rendering; propagate cancellation and support non-TTY consumers.
5. Add executable behavior tests with cargo add --dev assert_cmd; cover missing files, invalid input, stdin, cancellation, stdout/stderr and terminal cleanup. Run the profile verification checks.
6. When dist is selected, follow its release generator instructions and review target list and generated CI. Lock dependencies/toolchain, qualify native dependencies and installers, and preserve Cargo.lock. No application setup, release tags or publication were executed.

## Verification
Commands below require the selected tools and project configuration. Replace example paths, schemes and IDs; distinguish tests from builds and interactive startup. These are instructions, not recorded passes.

```text
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --locked -- -D warnings
cargo test --workspace --locked
cargo audit
cargo build --release --locked
```

## Open questions
- Which terminals, non-TTY consumers and OS/architectures must be supported?
- What output schema, cancellation and configuration precedence will consumers rely on?
- Which native dependencies, signing/notarization and update channels are required?

## Sources
- [clap](https://docs.rs/clap/latest/clap/)
- [Ratatui](https://ratatui.rs/)
- [reqwest](https://docs.rs/reqwest/latest/reqwest/)
- [SQLx](https://docs.rs/sqlx/latest/sqlx/)
- [SQLx CLI](https://github.com/transact-rs/sqlx/blob/main/sqlx-cli/README.md)
- [Rust config crate](https://docs.rs/config/latest/config/)
- [Rust environment variables](https://doc.rust-lang.org/std/env/fn.var.html)
- [Rust tracing](https://docs.rs/tracing/latest/tracing/)
- [Cargo test](https://doc.rust-lang.org/cargo/commands/cargo-test.html)
- [rustfmt](https://github.com/rust-lang/rustfmt)
- [Clippy usage](https://doc.rust-lang.org/clippy/usage.html)
- [RustSec](https://rustsec.org/)
- [assert_cmd](https://docs.rs/assert_cmd/latest/assert_cmd/)
- [Restate Rust SDK](https://docs.rs/restate-sdk/latest/restate_sdk/)
- [dist binary distribution](https://github.com/axodotdev/cargo-dist)
- [Cargo build](https://doc.rust-lang.org/cargo/commands/cargo-build.html)
- [Rust JSON API](https://docs.rs/serde_json/latest/serde_json/)
- [Rust signal API](https://docs.rs/tokio/latest/tokio/signal/index.html)

Keep the project README current and link the selected guidance; preserve existing project instructions.
