# Go CLI + TUI

Command-line applications and terminal interfaces distributed as binaries.

Language: Go | Reviewed: 2026-10-10 | Evidence: documentation-reviewed research input

Source record: menu/inputs/research/go-rust.json.

Core guidance checked: 2026-10-13. Review sources are listed below. /research-freshness.json describes the imported research packet; this record retains its own evidence scope. These recipes and selected dependency combinations need qualification in the actual project.

## Application role
Components: cli
UI: terminal
Deployment: binary

## Use cases
- Shipped command-line products
- infrastructure administration tools
- terminal dashboards

## Fit
- Want compiled distribution with Go ecosystem access
- Command structure and terminal UX matter more than tight low-level control

## Choose something else when
- Primarily a short disposable script
- Host SDK or native UI framework mandates another language
- Strict no-GC constraints

## Agent workflow
- Read README, dependency manifests, lockfiles, runtime pins and the maintained project workflow before changing anything. Preserve an existing stack unless reconsidering it is part of the request.
- For a new component, read the Generators section before writing application files. Use its appropriate official initializer and retain its generated baseline; follow-up generators are conditional on the selected feature.
- Use this guide to select tools by requirement. Resolve compatible versions from official and installed-version documentation; record the actual lockfile and runtime versions.
- Create a plan for schema changes, identity, authorization, external effects and deployment. A library choice does not complete its integration.
- Run relevant checks after configuration. Exercise the real interface, failure paths and packaged artifact on the intended target. Report commands, versions, results and untested behavior.
- On failure, retain the command and diagnostic, fix the failing prerequisite and resume there. Do not regenerate over existing work or suppress failures to make a check green.

## Best practices
- Keep command parsing separate from domain operations. Test help, exit codes, stdout and stderr.
- Respect cancellation, timeouts and non-interactive input; do not require a TUI for scripting.
- Skip persistence for stateless tools. Delegate long-lived work to a service with a durable job ID.
- Verify release binaries on each supported OS and architecture, including the required runtime dependencies.

## Generators: create the baseline first

Generator documentation reviewed: 2026-10-23. Evidence: documentation-reviewed; commands not executed.

### Required workflow

- Before writing a new project's application files, read its profile's starting points and use the official framework or language initializer appropriate to the component. Do not hand-recreate a generated skeleton. Where no full application generator exists, use the documented module/package initializer and assemble only the missing application pieces.
- Choose one starting point per component. Check the installed generator's version and help, prerequisites, template, database, UI, test and runtime options. Commands are examples: replace names and paths, resolve compatible versions, and record the exact invocation and selected options. Do not blindly run every listed generator.
- Generate in a new empty destination. For an existing repository, preserve its conventions and use relevant incremental generators. If a baseline comparison is needed, generate a separate disposable reference with matching versions/options and reconcile deliberately; never regenerate over existing work.
- Keep applicable generated configuration, hidden files, formatter/linter settings, ignore rules, manifests, lockfiles, tests, wrappers and entry points. Extend them for the project instead of replacing them with abbreviated handwritten copies. A generator may initialize version control or offer a commit; respect the user's Git instructions.
- Run the generated baseline's documented checks before feature changes, then relevant checks after configuration and implementation. Inspect what version control would include, including hidden files, build output, local secrets and operating-system metadata. Add needed ignore rules explicitly: no generator guarantees that .DS_Store or every local artifact is ignored.
- Use follow-up generators only when their feature or tool is selected. Review generated changes and dependencies, apply required migrations in the intended environment, and exercise the generated behavior. Scaffolding does not establish authorization, safe retries, production readiness or every best practice.
- If the required generator, template or IDE is unavailable, report the missing prerequisite and the documented route. Do not silently substitute a handwritten scaffold. Keep documentation review, generator execution, baseline checks and application qualification as separate evidence.

### Choose a starting point

#### Go module plus Cobra generator

Use when: A new command application selects Cobra; use the standard-library flag package for a deliberately smaller CLI without a Cobra scaffold.

1. Install the project-selected Go toolchain and create an empty project directory. Replace paths and module name with real values.
2. Initialize the module before Cobra. Set COBRA_CLI_VERSION to a selected published version (including v prefix); ensure the Go install bin directory is on PATH.
3. Generate the command skeleton, review author/license defaults and add application logic and tests.

Working directory: /path/to/workspace (existing local source parent)

Create a new CLI source directory.

```sh
mkdir project
```

Working directory: /path/to/workspace/project

Initialize module metadata.

```sh
go mod init example.com/project
```

Working directory: /path/to/workspace/project

Install the selected generator version.

```sh
go install github.com/spf13/cobra-cli@"${COBRA_CLI_VERSION:?Set the selected Cobra CLI version}"
```

Working directory: /path/to/workspace/project

Generate main.go and cmd/root.go using Cobra.

```sh
cobra-cli init
```

- Choose the actual project license and author; inspect ~/.cobra.yaml because it can alter output. Add --viper only if Viper is explicitly selected.
- If Cobra is not selected, go mod init remains required module initialization; flag and Bubble Tea do not require this Cobra scaffold.

### Conditional follow-up generators

#### Cobra subcommand

Use when: When adding commands to the generated Cobra application.


Working directory: /path/to/workspace/project (existing Cobra root)

Generate an example serve command for subsequent implementation.

```sh
cobra-cli add serve
```

- Replace serve with the intended command name; review generated command registration, help and error/exit behavior.

#### Optional Bubble Tea v2 terminal interface

Use when: Only when the CLI needs an interactive terminal user interface; a conventional command interface can stay with Cobra or the standard library.


Working directory: /path/to/workspace/project (module root)

Add Bubble Tea v2 using its current vanity module path.

```sh
go get charm.land/bubbletea/v2@latest
```

- Use the v2 import `tea "charm.land/bubbletea/v2"` and follow the v2 Model/View API: `View() tea.View`, not the v1 `View() string`. The v2 module path and API differ from `github.com/charmbracelet/bubbletea` v1; do not mix their examples or imports.
- Bubble Tea is a framework integration, not an application generator. Build it only when interactive screens are required; add related Charm v2 modules such as Bubbles or Lip Gloss only if selected and use their matching `/v2` module paths.

#### GoReleaser configuration

Use when: Only when GoReleaser is selected for this application and no release configuration exists.


Working directory: /path/to/workspace/project (module root; selected GoReleaser installed)

Generate .goreleaser.yaml.

```sh
goreleaser init
```

Working directory: /path/to/workspace/project

Validate the reviewed release configuration.

```sh
goreleaser check
```

- Install and record the project-selected GoReleaser release first. Review build entry points, targets, hooks and publishing settings; generation does not authorize a release.

### Preserve the generated foundation

- Preserve go.mod and go.sum when generated by dependency resolution; record the Go version and resolved generator versions.
- go mod init creates module metadata, not source files, tests, a service structure or .gitignore. Add project-specific ignores, including OS metadata, without claiming they came from Go.
- Keep generator-created files as the baseline; document deliberate changes and do not replace standard defaults with a handwritten approximation.
- Preserve Cobra command wiring and help/completion behavior; review generator license output before adopting it.

### Baseline and generation checks

- In the actual project, record generator versions and commands, then compare its initial files with a fresh output from the same versions and options.
- After source exists, run gofmt -l ., go test ./..., go vet ./... and go build ./... from the module root; a bare go.mod is not a runnable application.
- In a disposable copy, check candidate staging includes source and required manifests but excludes binaries, caches, local credentials and .DS_Store; inspect git add --dry-run -A before changing a real index.
- For Cobra, exercise go run . --help and generated command help, then test actual exit codes, stdout/stderr and noninteractive operation.

### Generation receipt

- Component and selected starting point, or the documented absence of a full application generator
- Generator/toolchain versions, exact commands or IDE template/settings, working directory and generated destination
- Generated files retained, deliberate deviations with reasons, and required supplemental ignore rules
- Baseline checks and later checks actually run, results and remaining prerequisites or untested behavior

### Generator sources

- [Go module creation tutorial](https://go.dev/doc/tutorial/create-module)
- [Bubble Tea v2 official README and tutorial](https://github.com/charmbracelet/bubbletea)
- [Bubble Tea v2 upgrade guide and module/API changes](https://github.com/charmbracelet/bubbletea/blob/main/UPGRADE_GUIDE_V2.md)
- [Go modules reference: go mod init](https://go.dev/ref/mod#go-mod-init)
- [Cobra generator documentation](https://github.com/spf13/cobra-cli/blob/main/README.md)
- [GoReleaser quick start](https://goreleaser.com/getting-started/quick-start/)

## Tools

### Command parsing: Cobra

Command/help/completion structure plus event-driven terminal UI.

Limits and integration: Keep noninteractive and machine-readable modes; test TTY absence, cancellation and terminal restoration.


- https://github.com/spf13/cobra
- https://github.com/charmbracelet/bubbletea
- https://pkg.go.dev/flag

Alternatives: flag for a small single command

### Terminal UI: Bubble Tea only for interactive screens

Command/help/completion structure plus event-driven terminal UI.

Limits and integration: Keep noninteractive and machine-readable modes; test TTY absence, cancellation and terminal restoration.


- https://github.com/spf13/cobra
- https://github.com/charmbracelet/bubbletea
- https://pkg.go.dev/flag

Alternatives: Line-oriented output when no interactive screen is needed

### HTTP client: net/http Client

Standard client with contexts and transport reuse.

Limits and integration: Set timeouts, bound responses and close bodies; retry only when operation semantics allow.


- https://pkg.go.dev/net/http

### Persistence and migrations: None for stateless tools

Avoid introducing a database into a command wrapper.

Limits and integration: Local durable state requires a separately selected storage/schema policy; never assume flat-file writes are atomic.


- https://pkg.go.dev/os

Alternatives: Use service API for shared state

### Configuration: Typed settings loaded with os.LookupEnv

Explicit startup validation and standard structured logs.

Limits and integration: Define precedence; reject malformed required values; redact secrets. Environment access alone is not validation or secret management.


- https://pkg.go.dev/os
- https://pkg.go.dev/flag
- https://pkg.go.dev/log/slog

Alternatives: flag for small command surfaces

### Application logging: log/slog

Explicit startup validation and standard structured logs.

Limits and integration: Define precedence; reject malformed required values; redact secrets. Environment access alone is not validation or secret management.


- https://pkg.go.dev/os
- https://pkg.go.dev/flag
- https://pkg.go.dev/log/slog

### Tests and static checks: testing; go vet; race detector; govulncheck

Standard toolchain feedback plus exercised concurrency and known-vulnerability checks.

Limits and integration: Race detector requires supported target/toolchain and exercised code; no scanner proves absence of vulnerabilities.


- https://pkg.go.dev/testing
- https://go.dev/doc/articles/race_detector
- https://golangci-lint.run/docs/welcome/quick-start/
- https://go.dev/doc/security/vuln/

### Durable work: Delegate long jobs to a service; persist its job ID

Work survives the terminal process only through an explicit durable owner.

Limits and integration: A goroutine or TUI background command dies with the process; reconnection needs a stable job identity.


- https://riverqueue.com/docs/transactional-enqueueing
- https://github.com/charmbracelet/bubbletea

Alternatives: River-backed Go service

### Distribution: GoReleaser

Target builds and release artifact automation.

Limits and integration: Review generated release actions, supported targets, signing and updater policy. cgo can complicate cross-building.


- https://goreleaser.com/getting-started/quick-start/

Alternatives: Manual go build for one internal target

### Machine-readable output: encoding/json/v2 on a supporting pinned Go toolchain

Stable JSON output lets scripts consume commands without parsing terminal text

Limits and integration: Add an explicit --json/output mode and document schema/exit codes; reserve stdout for results, stderr for diagnostics, and disable interactive/color output for pipelines. Confirm API availability on the pinned Go version; v2 changes encoding/decoding defaults, so test schema/null/omission compatibility before migrating.


- https://pkg.go.dev/encoding/json
- https://pkg.go.dev/encoding/json/v2

Alternatives: encoding/json for established output contracts or older supported toolchains

### Cancellation and shutdown: signal.NotifyContext

User interrupts should cancel outbound work and leave terminal/files usable

Limits and integration: Propagate cancellation through work; bound cleanup time and test interrupts during writes. Avoid adding an async runtime to a synchronous Rust CLI solely for signals.


- https://pkg.go.dev/os/signal

Alternatives: Preserve an existing compatible project choice

## Architecture and developer workflow

Recommendation: keep the command tree as an adapter over testable application functions. A noninteractive command is a versioned automation interface; a Bubble Tea view is an optional interactive client of the same functions. The executable owns stream, exit-status, cancellation and configuration contracts.

Version scope: Go 1.27 toolchain documentation, Cobra/pflag current guide, Bubble Tea upstream API and GoReleaser v2 documentation. Pin compatible module/tool versions; Bubble Tea major/module-path changes need explicit review. No release matrix was built.
Reviewed: 2026-10-11 | Evidence: documentation-reviewed | Source record: inputs/research/migrations-systems.json

### Architecture boundaries

- Recommendation: Cobra parses and validates arguments, then RunE calls domain operations that return typed results/errors. Formatters own text versus JSON output; diagnostics and progress go to stderr, leaving stdout usable by scripts.
- Recommendation: expose a schema/version field in machine-readable output and configuration. Centralize environment/flag/file precedence and secret redaction; preserve old names through an explicit deprecation period.
- Recommendation: use Bubble Tea Model/Update/View and commands for terminal interaction. Keep interactive state separate from persisted application configuration, and disable prompts/spinners for pipes or explicit noninteractive mode.
- Recommendation: use the established module workflow and GoReleaser target matrix for binary distribution. Native libraries, signing, notarization and OS behavior require per-target checks even when cross-compilation succeeds.

### Tools and feedback

- Recommendation: inspect existing flags, help output, scripts and configuration before changing the CLI. A new project can start with go mod init and Cobra CLI generation when desired; generation is optional, not an architecture.
- Recommendation: run gofmt, go vet ./... and go test ./...; add subprocess-level contract fixtures that capture stdout, stderr and exit status. Domain unit tests alone miss terminal and shell behavior.
- Recommendation: exercise --help, invalid flags, piped input, --output json (if implemented), interrupted work and no-TTY execution. Choose and document application exit codes; Cobra does not define every business error code.
- Recommendation: after installing a pinned GoReleaser v2, review .goreleaser.yaml, run goreleaser check and goreleaser release --snapshot --clean to prepare local artifacts. These are review commands, not a published release; verify clean-machine install and upgrade on the supported targets. Current GoReleaser OSS installation docs require Go 1.27 when installing the tool from source; a prebuilt tool or a compatible pinned older tool is a separate choice from the application minimum Go version.

### Translations to avoid

- Avoid logging or progress bars on machine-readable stdout; one extra line can break the calling script.
- Avoid os.Exit inside domain functions or cleanup scopes: os.Exit skips deferred calls. Map errors to a code after cleanup in the entry point.
- Avoid requiring a TTY for every command; automation needs explicit inputs and a prompt-free path.
- Avoid rewriting configuration in place without a version/backup; users may need to downgrade the executable.
- Avoid silently switching encoding/json to Go 1.27 encoding/json/v2 during a rewrite; changed serialization defaults require compatibility fixtures and an explicit protocol decision.

### Architecture sources

- [Cobra flag guide](https://cobra.dev/docs/how-to-guides/working-with-flags/): Flag scoping, validation, deprecation and optional configuration integration are explicit.
- [Bubble Tea upstream](https://github.com/charmbracelet/bubbletea): The TUI uses Model/Update/View with commands for effects.
- [Go JSON decoder](https://pkg.go.dev/encoding/json#Decoder.DisallowUnknownFields): Typed decoding and DisallowUnknownFields are available; schema policy is the application responsibility.
- [os.Exit](https://pkg.go.dev/os#Exit): Process exit skips deferred calls; exit-code meanings need an application contract.
- [errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup): Group limit and cancellation support bounded batch execution.
- [os/signal](https://pkg.go.dev/os/signal#NotifyContext): NotifyContext exposes signal cancellation.
- [GoReleaser workflow](https://goreleaser.com/getting-started/how-it-works/): Release configuration and build/package/publish workflow are described; snapshot behavior has its own source.
- [GoReleaser Go builds](https://goreleaser.com/customization/builds/go/): GOOS/GOARCH matrix and environment/CGO settings are configurable.
- [GoReleaser notarization](https://goreleaser.com/customization/sign/notarize/): Signing/notarization requires Apple credentials; the native package flow is Pro and uses Apple tools. Cross-platform binary notarization is a separate documented flow.
- [GoReleaser snapshots](https://goreleaser.com/customization/publish/snapshots/): Snapshot mode builds review artifacts without publishing to a release channel.
- [GoReleaser quick start](https://goreleaser.com/getting-started/quick-start/): goreleaser check validates config; release --snapshot --clean builds local review artifacts.
- [GoReleaser OSS installation](https://goreleaser.com/getting-started/install/oss/): Current source installation requires Go 1.27; verified prebuilt binaries are another documented installation method.
- [Go 1.27 release notes](https://go.dev/doc/go1.27): Introduces encoding/json/v2 with changed defaults; serializer replacement requires compatibility review.

## Transition options

Proposed designs and checks; these are not executed compatibility results.

### CLI and pipe contracts

**Inspect the source:** Capture scripts consuming current flags, positional arguments, stdout/stderr, exit codes and completion output.

**During coexistence:** Recommendation: retain old subcommands/aliases as thin adapters while introducing an explicit JSON mode. Mark renamed flags deprecated through Cobra instead of silently changing their meaning.

**Target design:** Recommendation: Cobra RunE plus centralized result/error mapping; versioned JSON on stdout and diagnostics on stderr. Freeze documented application codes for success, usage and operational failure.

**Rollback:** Recommendation: install the preceding binary and continue serving the old protocol. Keep newly introduced machine schemas behind explicit versions so callers can choose a compatible response.

**Benefits and prerequisites**

- A stable CLI protocol permits automation and humans to share one executable. Requires: Consumer fixtures cover streams/status; formatting and error categories are explicit; deprecation schedule preserves callers. Tradeoffs: Versioned output requires ongoing compatibility ownership; usage errors and remote failures may need different handling.

**Checks before transfer**

- Run old calling scripts against the new binary and compare all three output channels.
- Verify invalid flags perform no effects and produce the documented exit code.
- Pipe JSON to a parser; help/progress/logging must not contaminate its data.

- https://cobra.dev/docs/how-to-guides/working-with-flags/
- https://pkg.go.dev/encoding/json#Decoder.DisallowUnknownFields
- https://pkg.go.dev/os#Exit

### Data and schema

**Inspect the source:** Inventory config paths, default values, flag/environment precedence, secret fields and old readers.

**During coexistence:** Recommendation: parse both old and versioned schemas through adapters; display migration diagnostics on stderr and offer an explicit migration command with backup. Keep the old file untouched until conversion passes.

**Target design:** Recommendation: a typed versioned config decoded deliberately, with unknown-field policy and semantic validation. Write a same-directory temporary file, validate it and replace only after success; qualify filesystem/OS behavior and cross-process ownership.

**Rollback:** Recommendation: restore the backup and preceding executable together. Preserve old readable configuration throughout the downgrade window; do not roll back after newer-only values without an explicit mapping.

**Benefits and prerequisites**

- A versioned configuration contract makes upgrades and later rollback predictable. Requires: Old fixtures exist; migration preserves semantics and backups; one writer and tested replacement behavior are defined. Tradeoffs: Strict unknown-field rejection can hinder mixed-version use; atomic replacement does not establish crash durability or coordinate concurrent writers.

**Checks before transfer**

- Load representative old config, migrate and compare effective settings.
- Reject unknown unsupported schema versions before modifying files.
- Interrupt conversion and verify either the original or complete new file remains; test permissions on each target OS.

- https://pkg.go.dev/encoding/json#Decoder.DisallowUnknownFields
- https://cobra.dev/docs/how-to-guides/working-with-flags/

### Jobs and schedules

**Inspect the source:** Preserve per-item effects, retry decisions, ordering and interrupt behavior for batch commands; a process-local queue has no restart history.

**During coexistence:** Recommendation: keep the sequential executor available and compare the new bounded executor on fixture inputs. Route one operation class at a time; reuse stable operation IDs across retries.

**Target design:** Recommendation: signal.NotifyContext plus errgroup limit or a fixed worker pool. Pass context through clients, close resources after workers finish, and persist a checkpoint/receipt when interrupted effects need later recovery.

**Rollback:** Recommendation: return to sequential execution using the same checkpoint contract. Reconcile ambiguous outcomes first; restarting from item zero is not a safe general rollback.

**Benefits and prerequisites**

- Bounded fan-out can overlap independent I/O while maintaining a clear cancellation boundary. Requires: Concurrency quota and total deadline are set; downstream calls honor cancellation; completed and ambiguous effects can be reconciled. Tradeoffs: No throughput gain is measured; cancellation cannot undo effects; a retry can duplicate a write without provider or business idempotency.

**Checks before transfer**

- Interrupt midway through a batch and verify completed, pending and ambiguous items are reported separately.
- Simulate one failed item; verify the selected stop/continue policy and bounded parallelism.
- Resume using stable IDs and prove acknowledged effects are not repeated.

- https://pkg.go.dev/golang.org/x/sync/errgroup
- https://pkg.go.dev/os/signal#NotifyContext
- https://pkg.go.dev/os#Exit

### Delivery and recovery

**Inspect the source:** Preserve command name, install path, OS/architecture support, update channel and downgrade compatibility.

**During coexistence:** Recommendation: produce snapshot artifacts beside the old release and smoke-test them without changing the default download. Review generated package-manager changes and publish channels only after target verification.

**Target design:** Recommendation: pinned GoReleaser v2 matrix with metadata/checksums, OS-specific install tests and an explicit signing path. CGO dependencies and macOS signing/notarization need separate toolchain/credential setup; the documented native package notarization flow is Pro; qualify the chosen binary or package flow separately.

**Rollback:** Recommendation: repoint the owned download/package channel to the previous verified release and keep its artifacts available. Restore compatible configuration with the binary; do not silently overwrite unrelated install locations.

**Benefits and prerequisites**

- A repeatable artifact matrix reduces manual release assembly. Requires: Build inputs/tool versions are pinned; each promised target is installed and exercised; signing credentials and package metadata are owned. Tradeoffs: Cross-compilation is not execution evidence; CGO can require native toolchains; selected signing/notarization automation may require a paid tier.

**Checks before transfer**

- Install on clean Linux, macOS and Windows hosts for every advertised architecture.
- Verify version metadata, checksums, permissions and executable path.
- Upgrade from the old package and downgrade with preserved config; inspect macOS Gatekeeper behavior for the actual downloaded artifact.

- https://goreleaser.com/getting-started/how-it-works/
- https://goreleaser.com/customization/builds/go/
- https://goreleaser.com/customization/sign/notarize/
- https://goreleaser.com/customization/publish/snapshots/

Rewrite workflow: /rewrite/guide.md
Shared contracts and phases: /rewrite/contracts.json


## Setup
1. Complete the selected starting point and baseline checks in the Generators section first; then continue with the integration steps appropriate to the chosen component.
2. After the selected module/Cobra baseline, resolve dependencies and record tool versions; preserve the Cobra-generated main.go and cmd/root.go command wiring. Add Bubble Tea v2 (`charm.land/bubbletea/v2`) only when interactive screens are required, and use its v2 Model/View API rather than copying v1 examples.
3. Implement commands through the chosen command structure with injectable I/O, configuration validation, stable exit codes, cancellation and explicit noninteractive behavior. Keep application logic separate from terminal rendering.
4. Write command tests covering malformed input, stdin, stdout/stderr, cancellation and safe retries; use isolated temporary paths and test terminal restoration when a TUI is present.
5. When GoReleaser is selected, follow its configuration generator instructions and review/pin the generated configuration and target matrix. Preserve go.mod/go.sum; document installation, supported targets and rollback. No application setup or publishing has been executed.

## Verification
Commands below require the selected tools and project configuration. Replace example paths, schemes and IDs; distinguish tests from builds and interactive startup. These are instructions, not recorded passes.

```text
gofmt -l .
go test ./...
go test -race ./...
go vet ./...
govulncheck ./...
go build ./cmd/tool
goreleaser check
goreleaser build --snapshot --clean
```

## Open questions
- Which OS/architectures and terminals must be supported?
- What stable exit codes, JSON schema, configuration precedence and noninteractive behavior are required?
- Which signing, package managers and update mechanism will own distribution?

## Sources
- [Cobra](https://github.com/spf13/cobra)
- [Bubble Tea](https://github.com/charmbracelet/bubbletea)
- [Go flag](https://pkg.go.dev/flag)
- [Go net/http](https://pkg.go.dev/net/http)
- [Go os configuration primitives](https://pkg.go.dev/os)
- [Go structured logging](https://pkg.go.dev/log/slog)
- [Go testing](https://pkg.go.dev/testing)
- [Go data race detector](https://go.dev/doc/articles/race_detector)
- [golangci-lint quick start](https://golangci-lint.run/docs/welcome/quick-start/)
- [Go vulnerability management](https://go.dev/doc/security/vuln/)
- [River transactional enqueueing](https://riverqueue.com/docs/transactional-enqueueing)
- [GoReleaser quick start](https://goreleaser.com/getting-started/quick-start/)
- [Go JSON API](https://pkg.go.dev/encoding/json)
- [Go signal API](https://pkg.go.dev/os/signal)
- [Go JSON v2](https://pkg.go.dev/encoding/json/v2)

Keep the project README current and link the selected guidance; preserve existing project instructions.
