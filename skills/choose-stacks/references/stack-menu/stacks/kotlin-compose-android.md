# Kotlin + Compose

Native Android apps with platform UI, lifecycle and storage integration.

Language: Kotlin | Reviewed: 2026-10-10 | Evidence: documentation-reviewed research input

Source record: menu/inputs/research/native-mobile.json.

Core guidance checked: 2026-10-13. Review sources are listed below. /research-freshness.json describes the imported research packet; this record retains its own evidence scope. These recipes and selected dependency combinations need qualification in the actual project.

## Application role
Components: android
UI: native
Deployment: native

## Use cases
- Android phones, tablets and foldables
- Native Android integrations
- Accessible mobile clients for a shared service

## Fit
- Android-native UI and platform behavior are requirements
- The team can own an Android SDK, emulator/device and signed release pipeline

## Choose something else when
- The requirement is a single shared UI for Android and iOS
- No Android device or emulator verification can be performed

## Agent workflow
- Read README, dependency manifests, lockfiles, runtime pins and the maintained project workflow before changing anything. Preserve an existing stack unless reconsidering it is part of the request.
- For a new component, read the Generators section before writing application files. Use its appropriate official initializer and retain its generated baseline; follow-up generators are conditional on the selected feature.
- Use this guide to select tools by requirement. Resolve compatible versions from official and installed-version documentation; record the actual lockfile and runtime versions.
- Create a plan for schema changes, identity, authorization, external effects and deployment. A library choice does not complete its integration.
- Run relevant checks after configuration. Exercise the real interface, failure paths and packaged artifact on the intended target. Report commands, versions, results and untested behavior.
- On failure, retain the command and diagnostic, fix the failing prerequisite and resume there. Do not regenerate over existing work or suppress failures to make a check green.

## Best practices
- Expose immutable screen state from ViewModels and collect it with lifecycle awareness.
- Use lifecycle-owned coroutine scopes. Use WorkManager for eligible persistent, deferrable work.
- Test Room migrations and keep credential material protected by platform-backed keys.
- Check TalkBack, large text and real devices, then qualify the signed bundle through internal testing.

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

#### Android Studio Empty Activity template

Use when: Creating a new Kotlin/Jetpack Compose Android app with Android Studio, an installed compatible SDK/JDK and a new destination.

1. Record application ID/namespace, minimum SDK, target devices and release ownership. Choose a source workspace outside synchronized storage.
2. In Android Studio use New Project from the welcome screen or File > New > New Project. Select the phone/tablet Empty Activity template for Compose.
3. Set the app name, package, save location and required minimum SDK; use Kotlin. Finish the wizard and allow dependency resolution/Gradle sync to complete.
4. Record Android Studio/template version and generated options. Inspect the generated wrapper, Gradle scripts, version catalog if supplied, manifest, activity, resources and test source sets before adding app behavior.

- Preserve the generated compatible toolchain/dependency combination initially; verify the selected SDK and JDK. A fixed minimum SDK copied from a tutorial does not replace the product's support requirements.
- For existing projects, open/import the current project and inspect its modules and variants; do not run a new-project generator over it. gradle init --type kotlin-application creates a Kotlin/JVM command-line app, not an Android/Compose application.

#### Official Android CLI project templates

Use when: Creating a new Compose app without IDE interaction, when the current official Android CLI is installed and its create help/template listing confirms support.

1. Obtain the Android CLI from the official Android developer tools page, complete its documented SDK/JDK prerequisites and record its installed version.
2. Inspect create help and available templates. The reviewed reference documents an empty Compose activity default when no template is supplied; verify this in the installed release before creation.
3. Run creation into a new or empty destination using the agreed identity and minimum SDK. Inspect generated files and run the baseline checks before customizing.

Working directory: <new-project-parent>

Record the installed official Android CLI version after installation.

```sh
android --version
```

Working directory: <new-project-parent>

Verify current creation flags and default template behavior.

```sh
android create --help
```

Working directory: <new-project-parent>

List the installed official templates without creating a project.

```sh
android create --list
```

Working directory: <new-project-parent>

Create the documented default Compose template after confirming the installed CLI's default and replacing all placeholders.

```sh
android create --name='<App Name>' --application-id='<owned.application.id>' --namespace='<agreed.kotlin.namespace>' --min-sdk='<required-api-level>' --output='<new-project-directory>'
```

- The current official documentation offers this CLI route; it is distinct from obsolete Android SDK android commands. Never use --force to scaffold into an existing app.
- Reviewed pages differ in example template spelling, so this recipe uses the documented default and requires installed help/list verification instead of guessing a template identifier.
- If neither the official CLI nor Android Studio project wizard is accessible, report the missing prerequisite and request a generated baseline/operator handoff. Do not silently hand-scaffold Gradle and Android configuration.

### Conditional follow-up generators

#### Android Studio component and module templates

Use when: An existing project needs another compatible activity, Compose component, resource or module.


- Right-click the intended package/folder in the Project window and select New, or use File > New. Select an applicable template, configure it and inspect all generated changes after Gradle sync.
- Use New Module for a new app/library module only when the architecture requires it; do not create another activity for every Compose screen. Review manifest registrations, resource names and target module dependencies.

#### Generated wrapper verification

Use when: After project generation/sync, with a compatible JDK/SDK; discover the actual module and variant before substituting placeholders.


Working directory: <generated-project-root>

Verify the generated Gradle wrapper and active JVM; use gradlew.bat on Windows.

```sh
./gradlew --version
```

Working directory: <generated-project-root>

Discover actual modules before choosing the application module.

```sh
./gradlew projects
```

Working directory: <generated-project-root>

Discover tasks and variants before selecting build/test commands.

```sh
./gradlew tasks --all
```

Working directory: <generated-project-root>

Lint, unit-test and build the discovered debug application variant; adapt task suffixes for actual variants.

```sh
./gradlew :<actual-app-module>:lintDebug :<actual-app-module>:testDebugUnitTest :<actual-app-module>:assembleDebug
```

Working directory: <generated-project-root>

Run instrumentation/Compose tests after starting a compatible emulator or connecting an authorized device; adapt the variant.

```sh
./gradlew :<actual-app-module>:connectedDebugAndroidTest
```

- These commands consume the generated project; they are not app generators. Review task availability before running, especially with product flavors or nonstandard module names.
- Use the generated version catalog when present; when adding dependencies, centralize compatible versions and sync/build. A wrapper or catalog alone does not prove AGP/JDK/Kotlin/Compose compatibility.

### Preserve the generated foundation

- Keep generated gradlew/gradlew.bat and gradle/wrapper files, settings and module build scripts, gradle.properties, version catalog when present, and repository configuration; record intentional deviations.
- Keep the app manifest, Kotlin activity/Compose theme, resources and generated unit/instrumentation test setup until deliberate product changes replace them.
- Retain generated ignore rules and extend them for workspace needs; exclude local.properties, SDK paths, caches/build outputs, private signing keys and .DS_Store without ignoring the wrapper JAR or source/resources.

### Baseline and generation checks

- Record which official template and tool version created the project, its identity/minimum SDK choices, and the generated dependency/toolchain baseline.
- Confirm wrapper files and application source sets are included in version control; review Git's candidate file set and ignore behavior without changing an existing user's index.
- Run the discovered lint/unit/build tasks, then instrumentation tests with an emulator/device; inspect reports and distinguish missing environment prerequisites from failing app checks.
- Template generation and a debug build do not establish signed release readiness, production architecture or complete accessibility; complete the profile's product/device/release checks.

### Generation receipt

- Component and selected starting point, or the documented absence of a full application generator
- Generator/toolchain versions, exact commands or IDE template/settings, working directory and generated destination
- Generated files retained, deliberate deviations with reasons, and required supplemental ignore rules
- Baseline checks and later checks actually run, results and remaining prerequisites or untested behavior

### Generator sources

- [Android: Create a project](https://developer.android.com/studio/projects/create-project)
- [Android: Compose quick start](https://developer.android.com/develop/ui/compose/setup)
- [Android: Official CLI create command](https://developer.android.com/tools/agents/android-cli/commands/create)
- [Android: Agent tools and resources](https://developer.android.com/tools/agents)
- [Android: Add code from a template](https://developer.android.com/studio/projects/templates)
- [Android: Build your app from the command line](https://developer.android.com/build/building-cmdline)
- [Android: Migrate your build to version catalogs](https://developer.android.com/build/migrate-to-catalogs)
- [Gradle: Build Init Plugin (Kotlin/JVM scope)](https://docs.gradle.org/current/userguide/build_init_plugin.html)

## Tools

### UI and state: Jetpack Compose + Material 3; screen ViewModels exposing immutable StateFlow with lifecycle-aware collection

Unidirectional data flow separates user events and rendered state; repositories own data access

Limits and integration: ViewModels do not survive process death; persist important state and test restoration; add domain layers only for actual complexity


- https://developer.android.com/topic/architecture/recommendations

Alternatives: Android Views for existing apps or unsupported controls

### Structured local persistence: Room

Compile-time SQL checking, migrations and observable local data

Limits and integration: Choose compatible Room/KSP/Kotlin versions; test upgrades; neither Room nor DataStore automatically supplies encryption or backend sync


- https://developer.android.com/training/data-storage/room
- https://developer.android.com/topic/libraries/architecture/datastore

Alternatives: Direct SQLite only when Room cannot satisfy measured requirements

### Preferences: DataStore

Compile-time SQL checking, migrations and observable local data

Limits and integration: Choose compatible Room/KSP/Kotlin versions; test upgrades; neither Room nor DataStore automatically supplies encryption or backend sync


- https://developer.android.com/training/data-storage/room
- https://developer.android.com/topic/libraries/architecture/datastore

Alternatives: Existing supported preferences implementation with an explicit data migration

### Networking and API contract: Retrofit + OkHttp + kotlinx.serialization behind a repository

Typed HTTP interfaces with explicit DTOs and a replaceable client

Limits and integration: Pin compatible versions and converter; share schemas/fixtures with iOS rather than UI; test auth refresh, errors and cancellation


- https://github.com/lysine-dev/retrofit

Alternatives: Ktor Client when deliberate multiplatform business-code sharing justifies it

### Concurrency and background work: Coroutines/Flow in lifecycle-owned scopes; WorkManager for eligible persistent deferrable work

Cancellation follows lifecycle while scheduled local sync uses a persistent work system

Limits and integration: WorkManager is OS-constrained and not an exact scheduler; coroutine launch alone is not durable across process death


- https://developer.android.com/topic/architecture/recommendations
- https://developer.android.com/develop/background-work/background-tasks/persistent

Alternatives: Server-side durable jobs for long agent runs

### Credentials: Android Keystore-backed cryptographic keys protecting app-private credential material

Use OS key protection and explicitly scoped encrypted storage

Limits and integration: Keystore stores keys, not arbitrary bearer tokens; define encryption, backup exclusions and revocation; no backend provider secrets in APKs


- https://developer.android.com/privacy-and-security/keystore

Alternatives: In-memory sessions when no persisted credentials are needed

### Unit and integration tests: JUnit + coroutine test utilities; fake repositories/API; Room migration tests

Deterministically verify state, retries, decoding, migrations and process-restoration assumptions

Limits and integration: Host unit tests cannot prove Android framework/device behavior; emulator tests supplement them


- https://developer.android.com/topic/architecture/recommendations
- https://developer.android.com/training/data-storage/room

Alternatives: Established project test framework when compatible

### UI and accessibility: Compose UI tests + AndroidX accessibility checks; TalkBack and large-font/device review

Verify semantic actions, navigation and permission flows with the actual platform UI

Limits and integration: Automatic checks require supported test dependencies/API environment and do not replace screen-reader usability; test tablets/foldables if supported


- https://developer.android.com/develop/ui/compose/testing
- https://developer.android.com/develop/ui/compose/accessibility/testing

Alternatives: Espresso for mixed Views/Compose apps

### Build, CI and distribution: Android Studio + Gradle wrapper/Kotlin DSL; pinned JDK/SDK CI; signed Android App Bundle and Play internal testing

Reproduce build inputs and separate local tests, device tests and signed release artifacts

Limits and integration: AGP/Gradle/JDK/Kotlin/Compose must be compatible; release requires upload-key custody and Play account access; build success is not store publication


- https://developer.android.com/build/building-cmdline
- https://developer.android.com/studio/publish/app-signing

Alternatives: Managed device or device-farm testing where the project needs a broader matrix

### Navigation: Navigation Compose

Navigation host/controller handle screen back stacks and deep links

Limits and integration: Add compatible navigation-compose dependency; pass minimal route identifiers and test process recreation/back behavior. Preserve Fragment navigation during partial Compose migration.


- https://developer.android.com/guide/navigation

Alternatives: Preserve an existing compatible project choice

### Notifications: Android notification channels + runtime permission

Native notifications keep user delivery preferences under system control

Limits and integration: Declare/request POST_NOTIFICATIONS where required; create appropriate channels, handle denial and test release API levels. Remote transport/server enrollment is a separate integration.


- https://developer.android.com/develop/ui/compose/notifications/notification-permission

Alternatives: Preserve an existing compatible project choice

### Media selection: Android Photo Picker

System picker grants access to selected media

Limits and integration: Use Activity result contracts; handle fallback devices, URI access lifetime and upload size limits. Prefer selected access over requesting broad media-library permissions.


- https://developer.android.com/training/data-storage/shared/photo-picker

Alternatives: Preserve an existing compatible project choice

## Architecture and developer workflow

An installed Android client renders immutable screen state with lifecycle-aware collection and persists important data separately. Recommendation: repositories mediate Room/API data and WorkManager handles selected persistent work; backend services own privileged domain effects. Installed versions coexist through staged distribution.

Version scope: Documentation reviewed 11 October 2026. Use the project's minimum/target SDK, compatible Kotlin/Compose/AGP/Gradle/JDK/Room/WorkManager versions and version catalog. Current guidance is conditional on supported platform behavior; no APK, App Bundle, emulator or store release was tested.
Reviewed: 2026-10-11 | Evidence: documentation-reviewed | Source record: inputs/research/migrations-clients.json

### Architecture boundaries

- Android guidance recommends separate UI and data layers, repositories, unidirectional data flow and lifecycle-aware Flow collection. Add a domain layer only when complexity/reuse warrants it.
- Recommendation: keep API DTOs distinct from Room entities, and local observable data authoritative for offline screen reads while the backend owns shared-domain reconciliation.
- Room owns schema versions and migrations; DataStore serves preferences rather than a general relational substitute. Record durable user operations and acknowledgement state when offline writes are required.
- Coroutines serve lifecycle/in-process async work; WorkManager persists scheduled work across restart/reboot and remains subject to constraints and power policy.
- Recommendation: use Keystore-backed keys to protect separately stored app-private credentials. A Keystore key is not arbitrary token storage, nor a guarantee that a revoked backend session remains usable.

### Tools and feedback

- Start at the external source README, API and database fixtures, version catalog and Gradle wrapper. Record package identity, SDK/device matrix, signing owner and release track.
- Use ./gradlew --version and ./gradlew tasks --all; with an actual app module run ./gradlew :app:lintDebug :app:testDebugUnitTest :app:assembleDebug. Keep wrapper/JDK/SDK inputs reproducible.
- After adb devices identifies an authorized emulator/device, run ./gradlew :app:connectedDebugAndroidTest. Configure Room's migration testing/exported schemas; assertions must check preserved data as well as schema shape.
- Recommendation: use Android Studio profilers/inspection, coroutine fakes, Compose navigation/accessibility tests and physical-device reboot/offline checks. Build ./gradlew :app:bundleRelease only with reviewed signing, then verify an internal-track install/update before staged promotion.

### Translations to avoid

- Collecting Flow without lifecycle ownership can keep work running when a screen is stopped; repeating effects inside recomposition can duplicate requests.
- Treating a ViewModel or coroutine as disk persistence loses work on process death.
- Using destructive migration for user-created offline data deletes the only copy.
- Expecting WorkManager to execute at an exact wall-clock deadline ignores scheduling windows and power constraints.
- Halt rollout is not uninstall or downgrade; already-updated users stay on the new build.

### Architecture sources

- [Android Architecture Recommendations](https://developer.android.com/topic/architecture/recommendations): Separate UI/data layers, repositories, immutable state and lifecycle-aware collection are documented recommendations.
- [Android Offline-first Architecture](https://developer.android.com/topic/architecture/data-layer/offline-first): Local sources, queues, sync and conflict resolution need explicit policies; offline reads need not imply offline writes.
- [Migrate Your Room Database](https://developer.android.com/training/data-storage/room/migrating-db-versions): Migration testing should cover all paths; destructive fallback can permanently delete local table data.
- [Android WorkManager Task Scheduling](https://developer.android.com/develop/background-work/background-tasks/persistent): Work is persisted and rescheduled across reboots with constraints/retries; it is not an exact timer or all immediate work.
- [Android Keystore System](https://developer.android.com/privacy-and-security/keystore): Keystore protects cryptographic key material and usage constraints; arbitrary credentials need their own protected storage design.
- [Build Android Apps from the Command Line](https://developer.android.com/build/building-cmdline): Gradle wrapper build/test tasks and signed release artifacts require configured inputs.
- [Play Console Staged Rollouts](https://support.google.com/googleplay/android-developer/answer/6346149): Halting stops additional staged installs; already-updated users remain on that version.

## Transition options

Proposed designs and checks; these are not executed compatibility results.

### Browser and installed clients

**Inspect the source:** Supported installed APK versions/OS levels, DTOs/errors, auth, deep links and delayed old-client operations.

**During coexistence:** Recommendation: Deploy backward-compatible server behavior first; run old/new clients against it and retain contracts through explicit adoption/support gates.

**Target design:** Recommendation: Version API DTOs independently of Room entities and gate optional features by negotiated capability; keep backend authorization authoritative.

**Rollback:** Disable the new capability and preserve old/new APIs; repair already-installed clients with a compatible higher-version release when needed.

**Benefits and prerequisites**

- Client releases and backend changes can progress independently. Requires: Installed-version inventory, shared API fixtures and support ownership. Tradeoffs: Maintaining old contracts costs work; Compose adoption does not upgrade installed clients.

**Checks before transfer**

- Old/new builds decode missing/unknown fields and documented errors.
- A delayed old offline operation succeeds or returns the declared conflict.
- Deep links, session expiry and denied resources work across supported releases.

- https://developer.android.com/topic/architecture/recommendations
- https://support.google.com/googleplay/android-developer/answer/6346149

### Data and schema

**Inspect the source:** Room schema versions, exported schemas, all upgrade paths and user-owned unsynced records.

**During coexistence:** Recommendation: Add migrations without discarding old fields until adoption permits; include direct upgrades from every supported starting version.

**Target design:** Recommendation: Keep exported Room schemas and explicit migration tests; use automatic or manual migrations according to the actual change.

**Rollback:** Ship a forward repair when older code cannot read the new store; any restore requires reconciling writes made after upgrade.

**Benefits and prerequisites**

- Reviewed migrations preserve local user data across updates. Requires: Complete paths plus assertions on data/relationships/pending work. Tradeoffs: Schema validation alone does not establish value preservation; destructive fallback permanently deletes table data.

**Checks before transfer**

- MigrationTestHelper exercises each path and earliest-to-current upgrade.
- Assert unsynced rows, IDs and relationships remain meaningful.
- Verify intended downgrade behavior; prohibit destructive fallback for the only copy of user work.

- https://developer.android.com/training/data-storage/room/migrating-db-versions

### Caching and shared state

**Inspect the source:** Local source-of-truth reads, pending offline operations, revision/cursor/tombstone and conflict rules.

**During coexistence:** Recommendation: Use one repository and one reconciler for each data category; persist queued mutations with operation IDs before reporting success.

**Target design:** Recommendation: Use Room-backed local reads and a durable operation queue when offline writes are needed; select push/pull/hybrid sync and a domain-specific conflict policy.

**Rollback:** Stop the new synchronizer and retain its queue; map remaining operations/cursors to old semantics before resume.

**Benefits and prerequisites**

- Cached local data can keep required reads available and preserve offline intent. Requires: Server sync support, retry-safe writes and an explicit conflict policy. Tradeoffs: Offline-first reads do not imply offline writes; last-write-wins can discard intent and depends on metadata semantics.

**Checks before transfer**

- Two offline devices make conflicting changes and obtain the documented resolution.
- Kill process after local commit and before network send; operation survives.
- Repeat server-committed/unacknowledged mutation without duplication; honor deletes/tombstones.

- https://developer.android.com/topic/architecture/data-layer/offline-first

### Jobs and schedules

**Inspect the source:** Existing queued Worker class names, input Data versions, unique-work identities and external effects.

**During coexistence:** Recommendation: Retain readers/worker entry points for already-enqueued payloads; transfer one job category and prevent duplicate schedulers.

**Target design:** Recommendation: Use WorkManager for eligible persistent device work with constraints/backoff; keep server completion obligations in a backend durable job.

**Rollback:** Cancel new scheduling and account for pending/running work; keep compatibility workers until drained or safely transformed.

**Benefits and prerequisites**

- Scheduled work persists across restart and device reboot. Requires: Compatible worker payloads, stable unique names, replay-safe effects and documented constraints. Tradeoffs: Scheduling windows/power policy affect timing; unique work does not provide exactly-once remote effects.

**Checks before transfer**

- Reboot with queued work and verify it resumes when constraints permit.
- Update app with old queued input; the new worker decodes it.
- Crash after remote effect/before acknowledgement and confirm retry is safe.

- https://developer.android.com/develop/background-work/background-tasks/persistent
- https://developer.android.com/topic/architecture/data-layer/offline-first

### Identity and authorization

**Inspect the source:** Existing stored credential encryption, key alias/access constraints, backup exclusions, issuer expiry/revocation.

**During coexistence:** Recommendation: Retain the backend issuer and read old encrypted credential formats during a bounded transition; isolate account-local data.

**Target design:** Recommendation: Use Keystore-backed cryptographic keys with reviewed encrypted app-private credential storage and backend revocation.

**Rollback:** Retain compatibility decryption only while secure; require sign-in if the old format/key cannot be restored safely.

**Benefits and prerequisites**

- OS key protection can reduce key extraction exposure. Requires: Qualified device/API support, key invalidation handling and a reviewed storage/backup policy. Tradeoffs: Keystore stores keys rather than arbitrary tokens; device protection does not replace backend authorization.

**Checks before transfer**

- Key invalidation produces a controlled sign-in path.
- Backup/restore cannot silently expose unusable/plain credentials.
- Sign-out/account switch stops old-account queued work and backend revocation is enforced.

- https://developer.android.com/privacy-and-security/keystore

### Delivery and recovery

**Inspect the source:** Play tracks, signing/version codes, adoption, crash metrics and schema/API compatibility.

**During coexistence:** Recommendation: Verify an internal/closed-track update over supported old builds and preserve compatible backend behavior for the whole mixed-version population.

**Target design:** Recommendation: Use a staged rollout with explicit crash/data-loss thresholds and a higher-version compatible repair path.

**Rollback:** Halt additional rollout and disable the affected capability if safe; publish a compatible fixed build without assuming a downgrade of installed clients.

**Benefits and prerequisites**

- Percentage-based adoption can limit initial exposure. Requires: Signed build, account/track owner, telemetry and recovery artifact. Tradeoffs: Halting only prevents further rollout; users who already updated remain on that version.

**Checks before transfer**

- Install-over-old-build retains unsynced data and auth.
- Track failures by app/OS/schema version.
- Halt/recovery rehearsal keeps already-updated users functional.

- https://support.google.com/googleplay/android-developer/answer/6346149

Rewrite workflow: /rewrite/guide.md
Shared contracts and phases: /rewrite/contracts.json


## Setup
1. Complete the selected starting point and baseline checks in the Generators section first; then continue with the integration steps appropriate to the chosen component.
2. Record package/application identity, minimum and target SDKs, supported form factors, API contract, permissions and release owner; verify the generated toolchain matches these requirements.
3. Use the generated Gradle wrapper and record compatible JDK, SDK, Gradle, AGP, Kotlin and Compose versions. Maintain dependency/plugin versions in the project version catalog when present; introduce catalog changes deliberately in existing builds.
4. Implement screen state and ViewModels behind repositories. Add Room migrations, a typed HTTP client and deterministic fake data. Keep secrets out of version control and app resources.
5. Run discovered JVM test, lint and debug build tasks. Start a documented emulator or connect an authorized device, then run instrumentation and Compose checks.
6. Exercise process death, offline/reconnect, rotation, permission denial, TalkBack, large fonts and every supported form factor on appropriate devices.
7. Have the account owner establish package ownership, upload-key custody and Play App Signing. Follow the authorized release workflow to build a signed bundle and verify internal-track install/update; retain reports and distribution receipts. Build success is not store publication.

## Verification
Commands below require the selected tools and project configuration. Replace example paths, schemes and IDs; distinguish tests from builds and interactive startup. These are instructions, not recorded passes.

```text
./gradlew --version
./gradlew tasks --all
./gradlew :app:lintDebug :app:testDebugUnitTest :app:assembleDebug
adb devices
./gradlew :app:connectedDebugAndroidTest
./gradlew :app:bundleRelease
```

## Open questions
- What minimum/target API and phone/tablet/foldable matrix must be supported?
- Which offline/sync/conflict rules and API authentication contract apply?
- Which notification/media features and denied-permission flows are required?
- Who owns package identity, upload key and Play internal/release tracks?

## Sources
- [Android architecture recommendations](https://developer.android.com/topic/architecture/recommendations)
- [Room persistence](https://developer.android.com/training/data-storage/room)
- [DataStore](https://developer.android.com/topic/libraries/architecture/datastore)
- [Retrofit maintained repository; square/retrofit redirects here](https://github.com/lysine-dev/retrofit)
- [Persistent background work](https://developer.android.com/develop/background-work/background-tasks/persistent)
- [Compose testing](https://developer.android.com/develop/ui/compose/testing)
- [Compose accessibility testing](https://developer.android.com/develop/ui/compose/accessibility/testing)
- [Android command-line build](https://developer.android.com/build/building-cmdline)
- [Android app signing](https://developer.android.com/studio/publish/app-signing)
- [Android Keystore system](https://developer.android.com/privacy-and-security/keystore)
- [Android Navigation](https://developer.android.com/guide/navigation)
- [Android notification permission](https://developer.android.com/develop/ui/compose/notifications/notification-permission)
- [Android Photo Picker](https://developer.android.com/training/data-storage/shared/photo-picker)

Keep the project README current and link the selected guidance; preserve existing project instructions.
