# Swift + SwiftUI

Native iPhone and iPad apps using Apple's UI and platform APIs.

Language: Swift | Reviewed: 2026-10-10 | Evidence: documentation-reviewed research input

Source record: menu/inputs/research/native-mobile.json.

Core guidance checked: 2026-10-13. Review sources are listed below. /research-freshness.json describes the imported research packet; this record retains its own evidence scope. These recipes and selected dependency combinations need qualification in the actual project.

## Application role
Components: ios
UI: native
Deployment: native

## Use cases
- iPhone and iPad products
- Native Apple integrations
- Accessible mobile clients for a shared service

## Fit
- Apple-native UI and platform capabilities are requirements
- A Mac/Xcode build environment and Apple distribution ownership are available

## Choose something else when
- The requirement is a single shared UI across iOS and Android
- There is no supported macOS/Xcode build environment

## Agent workflow
- Read README, dependency manifests, lockfiles, runtime pins and the maintained project workflow before changing anything. Preserve an existing stack unless reconsidering it is part of the request.
- For a new component, read the Generators section before writing application files. Use its appropriate official initializer and retain its generated baseline; follow-up generators are conditional on the selected feature.
- Use this guide to select tools by requirement. Resolve compatible versions from official and installed-version documentation; record the actual lockfile and runtime versions.
- Create a plan for schema changes, identity, authorization, external effects and deployment. A library choice does not complete its integration.
- Run relevant checks after configuration. Exercise the real interface, failure paths and packaged artifact on the intended target. Report commands, versions, results and untested behavior.
- On failure, retain the command and diagnostic, fix the failing prerequisite and resume there. Do not regenerate over existing work or suppress failures to make a check green.

## Best practices
- Keep presentation state small and actor-isolated; inject service and API boundaries for tests.
- Use structured concurrency with cancellation and store credentials in Keychain.
- Treat offline storage and synchronization as separate decisions, with explicit conflict handling.
- Check Dynamic Type, VoiceOver and real-device behavior; a simulator pass does not establish background or distribution behavior.

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

#### Xcode iOS App template

Use when: Creating a new native iOS/iPadOS SwiftUI application in a new destination; requires macOS, compatible Xcode, iOS platform support and access to its project wizard.

1. Record product name, organization/bundle identity, minimum OS, supported devices and signing owner; use a source workspace outside synchronized storage.
2. In Xcode choose File > New > Project, use Choose Template if offered, select iOS and the App template. Select SwiftUI and Swift where the template offers these options.
3. Set the product and organization identifier. Choose storage deliberately: enable SwiftData only when required and compatible with the deployment target; record the choice. Select a signing team only when the relevant account is available.
4. Choose the testing option that provides Swift Testing unit tests and XCTest UI tests; retain established XCTest choices when required. If this template/version omits testing options, add the targets using the follow-up template workflow.
5. Create/save into a new destination, inspect the generated project, sources and assets, and share the app scheme for CI. Record the actual Xcode version, template, options and generated baseline before editing application code.

- This is an official IDE template workflow; xcodebuild builds and tests existing projects and is not an iOS app initializer. swift package init creates a Swift package, not the Xcode iOS App project required here.
- If the agent cannot access Xcode's wizard, report that prerequisite and request the template-generated project or an operator handoff. Do not silently substitute hand-written project files or an unreviewed third-party generator.
- For an existing app, open and inspect its project/workspace, targets and schemes; do not rerun new-project creation over it. Compare against a separate disposable template project only when investigating missing defaults.

### Conditional follow-up generators

#### Xcode test target and test file templates

Use when: The app needs an additional test bundle or test file; inspect existing targets first.


- Use File > New > Target, filter for Test, and choose Unit Testing Bundle or UI Testing Bundle; configure the intended app target and finish. Add the resulting targets to the relevant scheme/test plan.
- For a test file, use File > New > New File From Template and select Swift Testing Unit Test or XCTest Unit Test, assigning it to the intended test target.
- Swift Testing and XCTest tests can coexist in a target; use XCTest/XCUIAutomation for UI tests. Do not recreate existing test bundles merely to add Swift Testing.

#### Project and destination discovery before command-line verification

Use when: After the generated project exists and full Xcode with an appropriate simulator runtime is selected; substitute discovered values for every placeholder.


Working directory: <generated-project-root>

Record selected Xcode/toolchain version.

```sh
xcodebuild -version
```

Working directory: <generated-project-root>

Verify that the selected developer directory belongs to the required Xcode installation.

```sh
xcode-select -p
```

Working directory: <generated-project-root>

Discover the generated targets and schemes; use -workspace for a workspace-owned app.

```sh
xcodebuild -list -project '<actual-project>.xcodeproj'
```

Working directory: <generated-project-root>

Discover a supported installed simulator destination after choosing the actual scheme.

```sh
xcodebuild -showdestinations -project '<actual-project>.xcodeproj' -scheme '<actual-shared-scheme>'
```

Working directory: <generated-project-root>

Build and run the app's selected unit/UI tests and retain results; requires discovered targets and a simulator.

```sh
xcodebuild test -project '<actual-project>.xcodeproj' -scheme '<actual-shared-scheme>' -destination 'platform=iOS Simulator,id=<installed-simulator-UUID>' -resultBundlePath '<new-result-path>.xcresult'
```

- These commands inspect/build/test the generated app; they do not generate an app. Replace -project with -workspace consistently if that is the actual build owner.
- Apple's command-line FAQ is archived: check the selected Xcode's local help for supported flags. Device signing, archives and App Store publication require their separate project release workflow.

### Preserve the generated foundation

- Keep the generated Xcode project configuration, app entry point, asset catalog and selected test targets; document deliberate changes from the recorded template baseline.
- Preserve shared schemes, test plans, required build settings, deployment targets and the app's dependency resolution policy; do not replace them with a minimal handwritten project skeleton.
- Inspect repository ignore coverage separately: an IDE template is not evidence that .DS_Store, DerivedData, build outputs or personal xcuserdata cannot be staged. Preserve distributable source/assets and shared configuration.

### Baseline and generation checks

- Record template provenance and Xcode version; inspect the actual generated target membership, bundle ID, storage choice and signing configuration.
- Confirm the shared app scheme includes the intended test targets, discover a simulator destination and run tests with retained results before claiming the baseline works.
- Review Git's candidate file set and ignore behavior without modifying an existing user's index; ensure local caches and personal IDE state are excluded while project configuration and assets remain included.
- A simulator pass does not prove device capabilities, signing, accessibility or release readiness. Those require the profile's device and distribution checks.

### Generation receipt

- Component and selected starting point, or the documented absence of a full application generator
- Generator/toolchain versions, exact commands or IDE template/settings, working directory and generated destination
- Generated files retained, deliberate deviations with reasons, and required supplemental ignore rules
- Baseline checks and later checks actually run, results and remaining prerequisites or untested behavior

### Generator sources

- [Apple: Creating an Xcode project for an app](https://developer.apple.com/documentation/xcode/creating-an-xcode-project-for-an-app)
- [Apple: Adding tests to your Xcode project](https://developer.apple.com/documentation/xcode/adding-tests-to-your-xcode-project)
- [Apple: Building from the Command Line with Xcode FAQ (archived)](https://developer.apple.com/library/archive/technotes/tn2339/_index.html)
- [Swift.org: Build a Command-line Tool (SwiftPM package initialization scope)](https://www.swift.org/getting-started/cli-swiftpm/)

## Tools

### UI and state: SwiftUI + Observation; small @MainActor observable presentation models; explicit services

Native controls and platform conventions; keep domain and transport logic out of views

Limits and integration: SwiftUI/Observation availability must match the minimum OS; Observation is not persistence or automatic thread safety


- https://developer.apple.com/swiftui/
- https://developer.apple.com/documentation/swiftui/model-data

Alternatives: UIKit for unsupported UI or existing UIKit apps; ObservableObject for older deployment targets

### Structured local persistence: SwiftData

Framework-integrated models and persistence with a small dependency footprint

Limits and integration: Validate migrations, relationship behavior and deployment availability; local persistence does not implement cross-platform sync


- https://developer.apple.com/documentation/swiftdata/modelcontext

Alternatives: Core Data for established stores or older targets; explicit SQLite for requirements SwiftData does not meet

### Nonsecret preferences: UserDefaults

Framework-integrated models and persistence with a small dependency footprint

Limits and integration: Validate migrations, relationship behavior and deployment availability; local persistence does not implement cross-platform sync


- https://developer.apple.com/documentation/swiftdata/modelcontext

Alternatives: Existing explicit nonsecret preferences storage; structured databases have a separate persistence job

### Networking and API contract: URLSession + Codable behind an injected API client

Native HTTP client and async APIs; share API schemas and fixtures with Android

Limits and integration: Check status codes, cancellation, timeouts and decoding; do not put provider secrets in the client; server owns authorization


- https://developer.apple.com/documentation/foundation/urlsession

Alternatives: Generated Swift client from a versioned API contract when its generator is proven

### Concurrency and background work: Swift structured concurrency, cancellation and actor isolation; server for durable agent runs

Keep rendering responsive and avoid tying durable business work to a view lifetime

Limits and integration: async does not mean CPU work runs off the main actor; OS may suspend apps and does not guarantee exact background scheduling


- https://developer.apple.com/documentation/foundation/urlsession
- https://developer.apple.com/documentation/backgroundtasks

Alternatives: BackgroundTasks or background URLSession for eligible OS-managed local work

### Credentials: Keychain for app credentials

Use platform secret storage rather than preferences or database fields

Limits and integration: Define accessibility and logout/revocation behavior; backend service credentials never belong in app binaries


- https://developer.apple.com/documentation/security/keychain-services

Alternatives: In-memory credentials when persistence is unnecessary

### Unit and integration tests: Swift Testing for new domain/API tests; XCTest where needed

Test deterministic state transitions, fixtures, decoding, persistence and failures

Limits and integration: Do not mix Swift Testing and XCTest assertions inside a single test; simulator tests do not validate all hardware behavior


- https://developer.apple.com/documentation/xcode/testing

Alternatives: Keep established XCTest suites

### UI and accessibility: XCTest/XCUIAutomation; per-screen accessibility audits; VoiceOver and Dynamic Type review

Exercise navigation, permission states, keyboard/focus, screen-reader order and large text

Limits and integration: Automated audits cover the current screen and do not establish usability or complete accessibility; hardware checks remain necessary


- https://developer.apple.com/documentation/xcode/testing
- https://developer.apple.com/documentation/accessibility/performing-accessibility-audits-for-your-app

Alternatives: Accessibility Inspector for interactive audit

### Build, CI and distribution: Xcode + Swift Package Manager; xcodebuild on pinned macOS/Xcode CI; TestFlight before App Store

One reproducible toolchain, recorded test results, signed archives and beta verification

Limits and integration: Mac and compatible SDK/runtime required; signing team, bundle ID, profiles, capabilities, account access and store submission remain explicit handoffs; archive success is not publication


- https://developer.apple.com/xcode-cloud/
- https://developer.apple.com/library/archive/technotes/tn2339/_index.html

Alternatives: Xcode Cloud for managed Apple CI

### Navigation: SwiftUI NavigationStack

Platform navigation keeps back behavior and destinations in native UI

Limits and integration: Use on supported OS versions; keep route identities separate from loaded objects and test deep-link/session restoration. iOS 16+ availability requires a plan for older targets.


- https://developer.apple.com/documentation/swiftui/navigationstack

Alternatives: Preserve an existing compatible project choice

### Notifications: UserNotifications

Native notifications support reminders with explicit user permission

Limits and integration: Request authorization in context, handle denied/revoked permission and validate notification routes. Remote delivery adds APNs/server setup; delivery timing is not a durable job guarantee.


- https://developer.apple.com/documentation/usernotifications/asking-permission-to-use-notifications

Alternatives: Preserve an existing compatible project choice

### Media selection: PhotosUI PhotosPicker

Native picker lets users choose image/video assets

Limits and integration: iOS 16+; load selected representations with cancellation/error handling and bound file size before upload. Selection is not immediate local-file availability.


- https://developer.apple.com/documentation/photosui/photospicker

Alternatives: Preserve an existing compatible project choice

## Architecture and developer workflow

An installed iOS client persists across backend releases and is suspended or terminated under OS control. Recommendation: SwiftUI views render observable presentation state while repositories own URLSession DTOs and local persistence. Store rollout, API compatibility and local-store migration are separate adoption gates.

Version scope: Documentation reviewed 11 October 2026. SwiftUI Observation and SwiftData are iOS/iPadOS 17+; support older OS targets through compatible alternatives. Pin Xcode/SDK/Swift/package resolution and retain the minimum OS/device matrix. No simulator, archive or store-release check was executed.
Reviewed: 2026-10-11 | Evidence: documentation-reviewed | Source record: inputs/research/migrations-clients.json

### Architecture boundaries

- Use SwiftUI state/Observation according to minimum OS availability; keep view rendering separate from asynchronous repositories and business decisions. Observation is UI dependency tracking, not disk persistence.
- Recommendation: version API DTOs separately from SwiftData/Core Data entities; preserve old installed-client contracts and authorize all privileged operations on the backend.
- Use a versioned local schema and reviewed migration plan for SwiftData. Recommendation: store unacknowledged user intents durably before claiming an offline write succeeded; reconcile conflicts with an explicit server policy.
- Separate foreground structured concurrency, OS-scheduled refresh/processing, background URLSession transfers and server durable jobs. Each has different completion and cancellation semantics.
- Recommendation: Keychain stores credential material; isolate account-local data and clear/lock the appropriate state on account switch. Keep backend provider secrets out of the app bundle.

### Tools and feedback

- Start in the external Xcode source checkout. Read README, minimum OS, shared scheme, signing owner, capabilities, API fixtures and every persisted schema version.
- Record xcodebuild -version and xcode-select -p; use xcodebuild -list -project App.xcodeproj and xcodebuild -showdestinations -project App.xcodeproj -scheme App with the actual names. Resolve packages with xcodebuild -resolvePackageDependencies -project App.xcodeproj -scheme App. Check current flags with the pinned xcodebuild -help; the linked command-line FAQ is archived.
- After choosing an installed simulator UUID, run xcodebuild test -project App.xcodeproj -scheme App -destination 'platform=iOS Simulator,id=<UUID>' -resultBundlePath <new-path>.xcresult. Placeholders require substitution; simulator results do not establish device background behavior.
- Recommendation: use Instruments/network diagnostics, physical-device background checks, upgrade fixtures, VoiceOver and large text. Produce a signed archive/TestFlight update under the established release workflow; record exact old/new client builds and compatible backend revisions.

### Translations to avoid

- Assuming users update when the backend deploys strands old installed clients and offline requests.
- Assuming an older executable can read a migrated store confuses binary rollback with data rollback.
- Keeping pending offline writes only in view state loses work after suspension or termination.
- Using BGAppRefreshTask as an exact timer or unlimited durable worker ignores OS scheduling and expiration.
- Using phased release as install reversal overlooks manual downloads and devices already running the new version.

### Architecture sources

- [SwiftUI Managing Model Data](https://developer.apple.com/documentation/swiftui/managing-model-data-in-your-app): Observation connects model changes to UI and requires iOS/iPadOS 17+; it is not local persistence.
- [SwiftData SchemaMigrationPlan](https://developer.apple.com/documentation/swiftdata/schemamigrationplan): Versioned schemas and migration stages explicitly model local schema evolution; iOS/iPadOS 17+.
- [SwiftData VersionedSchema](https://developer.apple.com/documentation/swiftdata/versionedschema): A schema records a particular version and its model set.
- [Foundation URLSession](https://developer.apple.com/documentation/foundation/urlsession): Configured sessions own data/upload/download/WebSocket tasks, authentication callbacks and asynchronous transfer behavior.
- [Background Tasks](https://developer.apple.com/documentation/backgroundtasks): Register and schedule task handlers for eligible background processing; the framework has multiple task types.
- [Choosing Background Strategies](https://developer.apple.com/documentation/backgroundtasks/choosing-background-strategies-for-your-app): Select task strategy by workload, handle expiration and completion; the OS decides refresh/processing launch time.
- [Downloading Files in the Background](https://developer.apple.com/documentation/foundation/downloading-files-in-the-background): Background sessions require delegates/stable identifiers, support file-backed uploads and need completion-file lifecycle handling.
- [Keychain Services](https://developer.apple.com/documentation/security/keychain-services): Encrypted Keychain items can store small credential secrets.
- [App Store Connect Phased Release](https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases/): Automatic updates progress over seven days; manual downloads remain possible and phases can be paused.
- [Xcode Testing](https://developer.apple.com/documentation/xcode/testing): Swift Testing and XCTest/UI tests have complementary roles; testing is separate from distribution.
- [Archived Xcode Command-line FAQ](https://developer.apple.com/library/archive/technotes/tn2339/_index.html): Documents command shapes for scheme/project/destination tests and archives; recheck options with the pinned Xcode toolchain.

## Transition options

Proposed designs and checks; these are not executed compatibility results.

### Browser and installed clients

**Inspect the source:** Installed versions, minimum OS, URLSession DTOs/errors, deep links, auth expiry and old/offline writes.

**During coexistence:** Recommendation: Ship additive backend responses and versioned fixtures before the new client; retain old contracts until measured adoption and an explicit support policy permit retirement.

**Target design:** Recommendation: Separate API DTOs from local models and use capability negotiation for optional features; authorization remains backend-owned.

**Rollback:** Disable the new server feature and retain both API contracts; already-installed clients require a compatible forward fix when needed.

**Benefits and prerequisites**

- Independent backend/client deployment can preserve supported installations. Requires: Inventory of real installed versions, API fixtures and release/support owners. Tradeoffs: Long-lived version support costs maintenance; a new store release cannot force immediate adoption.

**Checks before transfer**

- Old and new builds run against the same new backend.
- Unknown optional fields and absent new fields do not break supported clients.
- A delayed old-client mutation receives the documented success/conflict/upgrade response.

- https://developer.apple.com/documentation/foundation/urlsession
- https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases/

### Data and schema

**Inspect the source:** Existing on-device store versions, entity meaning, relationships, pending local writes and upgrade paths.

**During coexistence:** Recommendation: Add compatible fields/stages before removing representations; migration fixtures include every supported historical store and unacknowledged operations.

**Target design:** Recommendation: Use SwiftData VersionedSchema and SchemaMigrationPlan when OS support permits; preserve the established Core Data/store choice if migration value is unproven.

**Rollback:** Prefer a compatible forward repair if downgrade is unqualified. Restore a pre-upgrade copy only under a reconciled policy that does not erase later local writes.

**Benefits and prerequisites**

- An explicit schema history makes upgrade behavior inspectable. Requires: Reviewed stages and fixtures proving values/relationships/pending writes survive. Tradeoffs: Forward migration does not establish older-binary readability; cross-store conversion is application work.

**Checks before transfer**

- Open each supported old store with the new build and compare user data and pending operations.
- Interrupt migration and verify recovery behavior.
- Attempt the intended rollback build against the migrated fixture; reject release rollback if unreadable.

- https://developer.apple.com/documentation/swiftdata/schemamigrationplan
- https://developer.apple.com/documentation/swiftdata/versionedschema

### Caching and shared state

**Inspect the source:** Local reads, pending offline changes, tombstones/cursors and server conflict semantics.

**During coexistence:** Recommendation: Keep the server as shared-domain reconciler; record each local mutation durably with a stable operation ID and schema version while old clients use the same conflict policy.

**Target design:** Recommendation: Use repository-owned local reads and a persistent operation log when offline writes are required; choose revision checks, merge or user resolution per domain instead of accidental timestamp wins.

**Rollback:** Stop the new synchronizer, retain pending operations and translate/reconcile them before returning to old logic; never clear the log as a rollback shortcut.

**Benefits and prerequisites**

- Users can retain local work through intermittent connectivity. Requires: Durable local storage, replay-safe backend, explicit conflict/tombstone protocol. Tradeoffs: This is a proposed application design; SwiftData does not automatically provide arbitrary backend synchronization.

**Checks before transfer**

- Two devices edit the same record offline; the declared policy preserves or exposes both intents.
- Disconnect after server commit but before acknowledgement; replay does not duplicate the effect.
- Restart/sign-out does not silently replay account A operations as account B.

- https://developer.apple.com/documentation/swiftdata/schemamigrationplan
- https://developer.apple.com/documentation/foundation/urlsession

### Jobs and schedules

**Inspect the source:** Foreground task cancellation, pending intents and any existing background task identifiers/handlers.

**During coexistence:** Recommendation: Retain old handler identifiers and persisted payload readers while new code is installed; use one owner per sync operation.

**Target design:** Recommendation: Choose BGAppRefreshTask/BGProcessingTask for eligible opportunistic device work, foreground tasks for interactive work and backend durable jobs for server completion obligations.

**Rollback:** Disable new task submission while preserving payload readers/handlers long enough to reconcile pending work; continue foreground sync or a server job where appropriate.

**Benefits and prerequisites**

- Eligible refresh/maintenance can execute while the app is backgrounded. Requires: Capabilities, registered handlers, durable checkpoints and expiration handling. Tradeoffs: The OS selects launch time; device scheduling does not satisfy a fixed backend completion SLA.

**Checks before transfer**

- Expire a task midway; it checkpoints/cancels and marks completion correctly.
- Suspend/terminate/relaunch and resume without a duplicated business effect.
- Offline, battery and permission constraints show honest pending state.

- https://developer.apple.com/documentation/backgroundtasks
- https://developer.apple.com/documentation/backgroundtasks/choosing-background-strategies-for-your-app

### Files and objects

**Inspect the source:** Existing upload/download IDs, authorized object keys, file hashes, task identifiers and completion acknowledgements.

**During coexistence:** Recommendation: Keep server upload endpoints/object ownership compatible; persist mapping from background task to logical operation and retain file-backed upload payloads.

**Target design:** Recommendation: Use an identified background URLSession for eligible HTTP(S) transfer; recreate it after system termination and move completed temporary downloads before delegate return.

**Rollback:** Stop creating new transfers, inspect/cancel or finish existing tasks and reconcile server objects; keep session callbacks until all retained tasks are accounted for.

**Benefits and prerequisites**

- Transfers can continue during suspension without holding the app process. Requires: Delegate lifecycle, stable session identifier, protected files and authorized retry/acknowledgement contract. Tradeoffs: Background uploads require files; scheduling is not exact and transfer completion differs from domain acceptance.

**Checks before transfer**

- Suspend during upload/download and restore the same session after system termination.
- Verify file integrity and durable location after completion.
- Retry an ambiguous response without producing duplicate owned objects.

- https://developer.apple.com/documentation/foundation/downloading-files-in-the-background

### Delivery and recovery

**Inspect the source:** Store release ownership, supported devices, adoption, crash reports and persisted-data compatibility.

**During coexistence:** Recommendation: Verify TestFlight install-over-existing fixtures; retain server compatibility through phased adoption and include manual downloads in risk assessment.

**Target design:** Recommendation: Use phased release with explicit crash/data-loss/compatibility stop criteria; assess adoption before retiring old API behavior.

**Rollback:** Pause further distribution and disable affected server capabilities if safe; ship a compatible repair rather than assuming an installed-version/store downgrade.

**Benefits and prerequisites**

- Gradual automatic-update distribution can limit initial exposure. Requires: Signed reviewed build, live telemetry and a compatible recovery release. Tradeoffs: Apple's seven-day phases cover eligible automatic updates; anyone can manually download, and pausing does not reverse installs.

**Checks before transfer**

- Verify real install/update preserves store, credentials and deep links.
- Track old/new build support and migration failures separately.
- Pause/recovery procedure leaves already-updated clients functional.

- https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases/

Rewrite workflow: /rewrite/guide.md
Shared contracts and phases: /rewrite/contracts.json


## Setup
1. Complete the selected starting point and baseline checks in the Generators section first; then continue with the integration steps appropriate to the chosen component.
2. Record minimum iOS/iPadOS versions, supported devices, capabilities, API schema and signing owner in the project documentation; confirm these choices against the generated baseline.
3. Pin package resolution and use only dependencies justified by a requirement. Separate SwiftUI views, observable presentation state, repositories and API DTOs; add migration fixtures, versioned network fixtures and a fake API for tests.
4. Run simulator checks and CI with the discovered shared scheme and actual destination. Verify representative physical devices, offline/reconnect, permissions, VoiceOver and large text.
5. Have the account owner establish team, bundle ID, capabilities and signing access. Follow the authorized release workflow to produce a signed archive and verify a TestFlight install; retain result bundles and release evidence. An archive is not publication.

## Verification
Commands below require the selected tools and project configuration. Replace example paths, schemes and IDs; distinguish tests from builds and interactive startup. These are instructions, not recorded passes.

```text
xcodebuild -version
xcode-select -p
xcodebuild -list -project App.xcodeproj
xcodebuild -showdestinations -project App.xcodeproj -scheme App
xcodebuild -resolvePackageDependencies -project App.xcodeproj -scheme App
xcodebuild test -project App.xcodeproj -scheme App -destination "platform=iOS Simulator,id=<installed-simulator-UUID>" -resultBundlePath <new-result-path>.xcresult
xcodebuild archive -project App.xcodeproj -scheme App -destination "generic/platform=iOS" -archivePath <new-archive-path>.xcarchive
xcodebuild -exportArchive -archivePath <archive-path>.xcarchive -exportPath <export-path> -exportOptionsPlist <reviewed-export-options>.plist
```

## Open questions
- What minimum OS versions, device matrix and Apple capabilities must be supported?
- Which offline/sync/conflict rules and API contract apply?
- Do notifications/media selection require permission-denied and degraded flows?
- Who owns bundle identity, signing and beta/release distribution?

## Sources
- [SwiftUI](https://developer.apple.com/swiftui/)
- [SwiftUI model data](https://developer.apple.com/documentation/swiftui/model-data)
- [SwiftData ModelContext](https://developer.apple.com/documentation/swiftdata/modelcontext)
- [URLSession](https://developer.apple.com/documentation/foundation/urlsession)
- [Testing with Xcode](https://developer.apple.com/documentation/xcode/testing)
- [Performing accessibility audits](https://developer.apple.com/documentation/accessibility/performing-accessibility-audits-for-your-app)
- [Xcode Cloud](https://developer.apple.com/xcode-cloud/)
- [Xcode command-line FAQ (archived; check local help)](https://developer.apple.com/library/archive/technotes/tn2339/_index.html)
- [Keychain services](https://developer.apple.com/documentation/security/keychain-services)
- [Background Tasks](https://developer.apple.com/documentation/backgroundtasks)
- [SwiftUI NavigationStack](https://developer.apple.com/documentation/swiftui/navigationstack)
- [Apple notification permission](https://developer.apple.com/documentation/usernotifications/asking-permission-to-use-notifications)
- [PhotosPicker](https://developer.apple.com/documentation/photosui/photospicker)

Keep the project README current and link the selected guidance; preserve existing project instructions.
