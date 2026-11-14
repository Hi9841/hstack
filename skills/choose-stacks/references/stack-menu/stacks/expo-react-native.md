# Expo + React Native

A shared React Native project delivering separate iOS and Android applications.

Language: TypeScript | Reviewed: 2026-10-23 | Evidence: Documentation reviewed 23 October 2026. The explicit `default@sdk-58` template was generated with create-expo-app 5.1.5; npm install succeeded, Expo Doctor passed 20/20, and `expo export --platform ios` produced a JavaScript bundle. Generated lint and TypeScript checks failed; no native build, device/simulator behavior, application integration, signing or store release was qualified.

Source record: menu/curated/expo-react-native.json.

Core guidance checked: 2026-10-23. Review sources are listed below. /research-freshness.json describes the imported research packet; this record retains its own evidence scope. These recipes and selected dependency combinations need qualification in the actual project.

## Application role
Components: ios, android
UI: native
Deployment: native

## Use cases
- A single product team ships an iOS and Android client against a separately owned API
- The team can share most screens and application logic while retaining platform-specific behavior where needed
- The product needs native device features available through Expo SDK or compatible React Native modules

## Fit
- Both iOS and Android are required and sharing a TypeScript/React codebase is more useful than two platform-native UI codebases
- The team accepts per-platform native builds, permissions, credentials, testing and store releases
- Required native libraries support the selected Expo SDK and can be tested in a development build

## Choose something else when
- The product requires deeply platform-specific interfaces or capabilities that make most UI and behavior separate; choose SwiftUI and/or Kotlin with Compose
- The team cannot build or obtain representative iOS and Android development builds and test both platforms
- The project assumes Expo Go includes arbitrary native libraries or considers one shared codebase proof of equivalent platform behavior

## Agent workflow
- Read README, dependency manifests, lockfiles, runtime pins and the maintained project workflow before changing anything. Preserve an existing stack unless reconsidering it is part of the request.
- For a new component, read the Generators section before writing application files. Use its appropriate official initializer and retain its generated baseline; follow-up generators are conditional on the selected feature.
- Use this guide to select tools by requirement. Resolve compatible versions from official and installed-version documentation; record the actual lockfile and runtime versions.
- Create a plan for schema changes, identity, authorization, external effects and deployment. A library choice does not complete its integration.
- Run relevant checks after configuration. Exercise the real interface, failure paths and packaged artifact on the intended target. Report commands, versions, results and untested behavior.
- On failure, retain the command and diagnostic, fix the failing prerequisite and resume there. Do not regenerate over existing work or suppress failures to make a check green.

## Best practices
- Keep SDK-compatible dependencies and the generated lockfile; inspect exact template versions and baseline checks.
- Use development builds for custom native dependencies and qualify their SDK and both-platform support.
- Keep identity, authorization, data and durable work behind the separately owned backend.
- Verify each platform on representative devices, including accessibility, lifecycle, offline behavior and release signing.

## Generators: create the baseline first

Generator documentation reviewed: 2026-10-23. Evidence: Documentation reviewed; create-expo-app 5.1.5 `default@sdk-58` scaffold generated. npm install succeeded; Expo Doctor passed 20/20; `expo export --platform ios` produced a JS bundle. Generated `npm run lint` and direct TypeScript/lint checks exposed template errors; no native build or device/store qualification..

### Required workflow

- Before writing a new project's application files, read its profile's starting points and use the official framework or language initializer appropriate to the component. Do not hand-recreate a generated skeleton. Where no full application generator exists, use the documented module/package initializer and assemble only the missing application pieces.
- Choose one starting point per component. Check the installed generator's version and help, prerequisites, template, database, UI, test and runtime options. Commands are examples: replace names and paths, resolve compatible versions, and record the exact invocation and selected options. Do not blindly run every listed generator.
- Generate in a new empty destination. For an existing repository, preserve its conventions and use relevant incremental generators. If a baseline comparison is needed, generate a separate disposable reference with matching versions/options and reconcile deliberately; never regenerate over existing work.
- Keep applicable generated configuration, hidden files, formatter/linter settings, ignore rules, manifests, lockfiles, tests, wrappers and entry points. Extend them for the project instead of replacing them with abbreviated handwritten copies. A generator may initialize version control or offer a commit; respect the user's Git instructions.
- Run the generated baseline's documented checks before feature changes, then relevant checks after configuration and implementation. Inspect what version control would include, including hidden files, build output, local secrets and operating-system metadata. Add needed ignore rules explicitly: no generator guarantees that .DS_Store or every local artifact is ignored.
- Use follow-up generators only when their feature or tool is selected. Review generated changes and dependencies, apply required migrations in the intended environment, and exercise the generated behavior. Scaffolding does not establish authorization, safe retries, production readiness or every best practice.
- If the required generator, template or IDE is unavailable, report the missing prerequisite and the documented route. Do not silently substitute a handwritten scaffold. Keep documentation review, generator execution, baseline checks and application qualification as separate evidence.

### Choose a starting point

#### Official create-expo-app default template

Use when: A new Expo/React Native application targeting iOS and Android; use a new, absent project directory and review the current default template before accepting it.

1. Install a supported Node.js LTS and inspect the current create-expo-app help. During the SDK 58 transition, pin `--template default@sdk-58` when SDK 58 is intended: the current Expo docs say unqualified `@latest` creates SDK 57. Record the resolved CLI and generated Expo SDK/React Native versions; `@latest` is still a scaffold-time lookup, not a project dependency pin.
2. Run the initializer from a source-workspace parent into a destination that does not exist. The current CLI has --no-agents-md but no --no-git flag; the reviewed default created its own .git repository and initial commit. Decide repository ownership before placing it inside another checkout.
3. Pass --no-agents-md to avoid generating AGENTS.md and Claude settings. Inspect the generated README, app configuration, package scripts, route structure, app identifiers and Git state before adding product code.
4. Review whether the default universal template's web target is wanted. This profile covers the iOS and Android clients; a web surface needs its own rendering, hosting and browser requirements.
5. Install dependencies from the generated project root and keep the generated lockfile. Use the generator's SDK-compatible versions as the starting baseline; do not independently upgrade React Native or native modules without checking the Expo SDK matrix.

Working directory: A local source-workspace parent; no application files are changed

Inspect installed-version template choices and flags before creating a project. The 23 October 2026 CLI 5.1.5 help includes --no-agents-md and no --no-git option.

```sh
npx create-expo-app@latest --help
```

Working directory: A local source-workspace parent; mobile-app must not already exist

Generate the SDK 58 default Expo project while suppressing generated AGENTS.md and Claude settings. During the documented SDK 58 transition, explicitly pin `default@sdk-58`; inspect generated files and repository state. Defer dependency installation so the next step installs packages once from the generated project root.

```sh
npx create-expo-app@latest mobile-app --template default@sdk-58 --yes --no-agents-md --no-install
```

Working directory: The generated mobile-app directory

Install the generated package manifest and create the project's lockfile. Keep the resolved versions in that lockfile.

```sh
npm install
```

Working directory: The generated mobile-app directory

Check that installed Expo/React Native packages match the selected SDK; inspect installed-version help if the command differs.

```sh
npx expo install --check
```

- Observed 23 October 2026 with the explicit `default@sdk-58` template: create-expo-app 5.1.5 generated Expo SDK 58.0.17, React Native 0.88.0, React 19.3.0 and Expo Router 58.0.25 in package.json. npm install completed; Expo Doctor passed 20/20; `npx expo export --platform ios` emitted a JS bundle. Generated `npm run lint` failed with a version-check error despite ESLint 9.39.5 being installed; direct ESLint found a generated React Hooks rule violation, and `tsc --noEmit` found generated CSS/type compatibility errors. These checks do not establish native build/device compatibility.
- The reviewed `default@sdk-58` command with --no-install and --no-agents-md created .git/ with an initial commit. Current help exposed no --no-git option. For a monorepo, decide the intended Git root before generation and resolve nested Git ownership explicitly; never run the initializer over an existing application.
- Expo docs state that during the SDK 58 transition `create-expo-app@latest` without `--template` creates SDK 57; pin `--template default@sdk-58` when SDK 58 is the intended baseline. The pinned template was successfully generated in a disposable directory on 23 October 2026.
- The default template includes Expo Router, TypeScript and a web target. The existence of generated web files does not qualify a browser product or make this profile a web-stack recommendation.
- Expo Go is a limited playground with a fixed set of native libraries. Production development should use a development build; custom native code and native dependencies absent from Expo Go require one.
- Default CNG projects generate native iOS/Android directories from app config and plugins. Prefer config plugins for repeatable project configuration; direct edits to generated native directories can be overwritten by prebuild.
- `--no-install` can defer npm and native package installation when inspecting a disposable scaffold; install and verify the actual project's dependencies before developing.

### Conditional follow-up generators

#### Expo development build and native projects

Use when: The app needs a native module not bundled in Expo Go, custom native code, native configuration, app identity changes to verify, or representative production-like testing.

1. Check the selected library's iOS and Android support, config plugin, Expo SDK compatibility, minimum OS/SDK and required permissions.
2. Choose a local native toolchain or an explicitly selected EAS cloud build. Local iOS building requires macOS/Xcode; local Android building requires Android Studio, Android SDK and a compatible Java toolchain. Cloud builds move compilation to EAS but do not eliminate device tests, app-account ownership or store credentials.
3. Generate native directories/build a development client using the project's current Expo CLI and documented workflow. Review generated diffs; use config plugins for repeatable native configuration.
4. Install and exercise the development build on both platforms. Rebuild after changes to native dependencies, plugins or app configuration.

Working directory: The generated mobile-app directory

Generate native iOS and Android projects from the Expo app configuration when the project needs native project inspection or customization. Review the diff and use config plugins for repeatable changes.

```sh
npx expo prebuild
```

Working directory: The generated mobile-app directory on macOS with compatible Xcode and iOS platform support installed

Build and launch the iOS app locally for a simulator or configured device. This is not an App Store-signed release.

```sh
npx expo run:ios
```

Working directory: The generated mobile-app directory with a compatible Android SDK/JDK and emulator or device configured

Build and launch the Android app locally. Discover the actual variant/toolchain and inspect the generated Gradle project.

```sh
npx expo run:android
```

Working directory: The generated mobile-app directory

Diagnose app config, dependency compatibility and common project health issues; it does not replace native builds or device checks.

```sh
npx expo-doctor
```

- Expo Go cannot load arbitrary native code. Rebuild the development client when the native dependency set or native configuration changes.
- When using Continuous Native Generation, generated android/ios directories are normally regenerated from app config and plugins. Keep intentional platform customization reproducible and review source-control ownership before committing generated native projects.
- EAS Build is optional. Account linking, build credentials, signing, push credentials and store submission are separate project decisions; this guidance does not create accounts or establish release readiness.

#### App-local Expo native module

Use when: A requirement genuinely needs custom Swift or Kotlin native functionality and no maintained compatible module meets it; use a local module when only this application needs it.


Working directory: The generated mobile-app directory

Use Expo's documented local-module generator to create an app-local native module; inspect current CLI help and generated iOS/Android code before adopting it.

```sh
npx create-expo-module@latest --local
```

- A local module introduces native code and needs development builds plus testing on each supported platform. It is not needed for ordinary JavaScript/TypeScript application logic.
- The Expo Modules API creates Swift and Kotlin module code. Follow current official documentation and generated examples; do not hand-invent project integration or assume one platform implementation covers the other.

### Preserve the generated foundation

- Keep the generated package manifest, lockfile, Expo app configuration, route structure, TypeScript configuration, assets, scripts and SDK-compatible dependency set; record intentional changes.
- Preserve the selected Git repository boundary. The current create-expo-app CLI has no documented --no-git option and the reviewed scaffold created an initial Git repository and commit; inspect this before adding it to a monorepo or existing source tree.
- Keep platform identifiers, entitlements, permission descriptions, config plugins, native modules and app-version/build-number policy explicit and compatible with both targets.
- Do not commit signing keys, local credentials, generated caches or machine-specific SDK paths. Preserve the project lockfile, build configuration and any native project sources the team has chosen to maintain.

### Baseline and generation checks

- Record create-expo-app version, selected template, resolved Expo SDK/React Native/React versions, package manager and installed runtime; inspect the actual generated baseline before editing.
- Run the selected Expo compatibility check and Expo Doctor; retain output and resolve version/configuration warnings before native work.
- Build/install a development build for iOS and Android. Exercise the same core journeys with both platform navigation, permissions, lifecycle, offline/reconnect and accessibility behavior; a JavaScript bundle or Expo Go pass does not qualify these native targets.
- Test the oldest supported iOS/Android versions and current representative devices. Verify app links, push/permission flows and native SDK integrations only when included in the product scope.
- Before a release, verify bundle/application identifiers, signing ownership, version/build numbers, privacy declarations, store listing ownership and install/update behavior on both platforms. A local build or cloud build is not store publication.

### Generation receipt

- Component and selected starting point, or the documented absence of a full application generator
- Generator/toolchain versions, exact commands or IDE template/settings, working directory and generated destination
- Generated files retained, deliberate deviations with reasons, and required supplemental ignore rules
- Baseline checks and later checks actually run, results and remaining prerequisites or untested behavior

### Generator sources

- [Expo: create-expo-app and SDK 58 template selection](https://docs.expo.dev/more/create-expo/)
- [Expo: Create a project](https://docs.expo.dev/get-started/create-a-project/)
- [Expo CLI](https://docs.expo.dev/more/expo-cli/)
- [Expo: Develop an app with Expo](https://docs.expo.dev/workflow/overview/)
- [Expo: Add custom native code](https://docs.expo.dev/workflow/customizing/)
- [Expo: Development builds](https://docs.expo.dev/develop/development-builds/introduction/)
- [Expo: SDK and dependency troubleshooting](https://docs.expo.dev/build-reference/troubleshooting/)
- [Expo: Tools and Expo Doctor](https://docs.expo.dev/develop/tools/)
- [Expo: Local and cloud builds](https://docs.expo.dev/build/introduction/)
- [Expo: App submission](https://docs.expo.dev/submit/introduction/)
- [Expo: Unit testing](https://docs.expo.dev/develop/unit-testing/)
- [Expo Router](https://docs.expo.dev/router/introduction/)
- [React Native: Platform-specific code](https://reactnative.dev/docs/platform-specific-code)
- [React Native: Security](https://reactnative.dev/docs/security)
- [React Native: Accessibility](https://reactnative.dev/docs/accessibility)

## Tools

### Cross-platform UI and routing: React Native with the Expo SDK and the generated Expo Router baseline

One TypeScript project can share much of the UI and application logic across iOS and Android while using native UI components and platform APIs

Limits and integration: Shared source does not guarantee identical layout, accessibility, lifecycle or device behavior. Expo Router and the default template evolve with the selected SDK; preserve and verify the generated compatible versions.


- https://docs.expo.dev/get-started/create-a-project/
- https://docs.expo.dev/router/introduction/
- https://reactnative.dev/docs/platform-specific-code
- https://docs.flutter.dev/platform-integration

Alternatives: Platform-specific route files or native modules for behavior that must differ by operating system; Flutter is a conditional alternative when a team accepts Dart and needs a custom rendered interface across more platforms, not a default substitute

### Backend and API contract: A separately selected backend/API with versioned request and response contracts; use Fetch behind an injected client and validate untrusted responses at runtime

The native clients should share service contracts without moving data ownership, authorization or durable work into the installed app

Limits and integration: TypeScript types do not validate network data at runtime. The client is public and cannot keep provider credentials or backend secrets. Choose the backend separately from this mobile profile.


- https://reactnative.dev/docs/network
- https://fastapi.tiangolo.com/features/

Alternatives: Generate a TypeScript client from an owned OpenAPI schema only when generation and versioning are established in the actual project

### Remote state and local data: Keep server-owned data behind the API; add local persistence only for a stated cache or offline requirement

Separating remote authority from device storage makes offline behavior, retries and reconciliation explicit

Limits and integration: Local storage does not create synchronization, conflict resolution, cross-device truth or encryption by itself. Define offline reads and writes separately.


- https://docs.expo.dev/versions/latest/sdk/sqlite/
- https://docs.expo.dev/develop/data-fetching/

Alternatives: Expo SQLite for structured local data when query, retention and migration requirements justify it; a query cache only when remote loading and invalidation need it

### App credentials: expo-secure-store for small locally held session credentials when its platform behavior and backup policy fit

Sensitive user credentials need an operating-system-backed storage boundary rather than app preferences or source code

Limits and integration: SecureStore is not a backend secret vault or a general database. Define logout, expiry, revocation, device migration and backup behavior; server authorization remains authoritative.


- https://docs.expo.dev/versions/latest/sdk/securestore/
- https://reactnative.dev/docs/security

Alternatives: In-memory credentials when persistence is unnecessary; use platform security APIs through a reviewed library for a different storage requirement

### Device capabilities and native modules: Use the Expo SDK or a React Native library that explicitly supports both target platforms and the selected SDK

Expo config and development builds can include native capabilities while retaining the JavaScript development workflow

Limits and integration: Expo Go contains a fixed set of native libraries. A module with native code that is absent from Expo Go needs a development build; native support, permissions and version compatibility must be checked per platform.


- https://docs.expo.dev/workflow/customizing/
- https://docs.expo.dev/develop/development-builds/introduction/

Alternatives: A config plugin or local Expo module when an app-specific native extension is necessary

### Build and dependency compatibility: Use the Expo CLI included with the project, `npx expo install` for compatible native package versions, the committed lockfile and `npx expo-doctor`

React Native packages must match the Expo SDK's native dependency set; the doctor command checks common project and version issues

Limits and integration: A clean doctor report is not a successful iOS or Android build, device test or release. Re-run native builds when native dependencies, app configuration or plugins change.


- https://docs.expo.dev/more/expo-cli/
- https://docs.expo.dev/develop/tools/
- https://docs.expo.dev/build-reference/troubleshooting/

Alternatives: Keep generated native directories and use native IDE workflows only when the project adopts direct native changes or needs native debugging

### Native development and distribution: Development builds for real application work; build and verify iOS and Android separately. Use local Xcode/Android tooling or an explicitly chosen cloud build service.

Development builds include the project's actual native dependencies; EAS can perform cloud builds without a local native toolchain

Limits and integration: Local iOS builds require macOS and Xcode; local Android builds require Android Studio/SDK and a compatible Java toolchain. Cloud builds do not remove Apple/Google account, application identity, signing, credential custody, store policy, per-platform device testing or release ownership.


- https://docs.expo.dev/workflow/overview/
- https://docs.expo.dev/build/introduction/
- https://docs.expo.dev/submit/introduction/

Alternatives: Expo Go for initial experiments with only the native libraries it already includes; EAS Build is optional, not required by Expo itself

### Behavior and platform verification: Unit-test domain/API behavior; exercise navigation, permissions, lifecycle, offline/reconnect and accessibility in development builds on both platforms

The shared JavaScript code still runs inside two operating-system-specific native applications

Limits and integration: A simulator/emulator or Expo Go check does not qualify device hardware, signing, native-module behavior or store distribution. Test against the minimum supported OS and current supported OS versions.


- https://docs.expo.dev/develop/unit-testing/
- https://docs.expo.dev/develop/development-builds/introduction/
- https://reactnative.dev/docs/accessibility

Alternatives: Use simulators/emulators for broad repeatable checks and representative physical devices for hardware, permission and release behavior

## Architecture and developer workflow

One Expo project can share TypeScript/React UI and application logic across separately built iOS and Android clients. The app calls an independently selected backend for authoritative data, authorization, secrets and durable jobs. Each platform still has its own native libraries, permissions, app identity, signing, store update path and behavior. A shared project does not prove native equivalence or migration compatibility.

Version scope: Expo/React Native guidance reviewed 23 October 2026. The explicitly pinned create-expo-app 5.1.5 `default@sdk-58` scaffold declared Expo SDK 58.0.17, React Native 0.88.0 and React 19.3.0. npm install succeeded, Expo Doctor passed 20/20, and iOS JavaScript export succeeded. Generated lint and TypeScript checks reported template errors; no native build, device integration or migration was executed.
Reviewed: 2026-10-23 | Evidence: documentation-reviewed | Source record: migrations/expo-react-native.json

### Architecture boundaries

- Keep server-owned business rules, database transactions, user/resource authorization, provider credentials and durable jobs behind versioned API contracts. A client-side check or hidden control is not authorization.
- Keep API DTOs and domain behavior testable outside screen components. Validate network data at runtime; TypeScript annotations are removed at runtime.
- Use shared navigation and screens where platform behavior is genuinely alike. Add platform-specific files or native modules for real differences in back navigation, permissions, accessibility, lifecycle or system APIs.
- If offline access is in scope, name the device-side data owner, stale-read tolerance, queued writes, idempotency, conflict policy, sign-out cleanup and database migration. Local SQLite or a query cache is not a synchronization design.
- Expo Continuous Native Generation derives native project files from app configuration, plugins and dependencies. Keep native configuration reproducible with config plugins; direct edits to regenerated projects need explicit source-control ownership and regeneration checks.
- Expo Go has a fixed native library set. Use development builds with the actual native dependency set when a required module, app configuration or production behavior is outside that playground.

### Tools and feedback

- Start with the `default@sdk-58` project scaffold in an empty directory when SDK 58 is intended. During the current documented SDK 58 transition, unqualified `create-expo-app@latest` creates SDK 57. Inspect generated files, template and Git state before edits; the reviewed CLI had no `--no-git` flag and made its own repository and initial commit. Preserve existing repository contents and do not import generated Git history into an existing repository.
- Record the generated Expo SDK, React Native, React, Node and package-manager versions. Keep the generated lockfile; use `npx expo install` and `npx expo-doctor` to check native dependency compatibility, then inspect their actual output. On the pinned SDK 58 starter, `npm install` completed and Expo Doctor passed 20/20.
- Use the Expo development server for JavaScript iteration and development builds on both iOS and Android. Add native libraries only after confirming current SDK, platform and minimum OS compatibility.
- For local native builds, use macOS with Xcode for iOS and Android Studio/SDK plus a compatible Java toolchain for Android. EAS cloud builds can avoid local native tool installation but still need project configuration, credentials, physical-device checks and platform release ownership.
- Use unit tests for shared logic and API behavior; verify navigation, permissions, app lifecycle, native modules, accessibility, and install/update with both native targets. Record device/OS, build and scenario; no checks have been run for an application migration here.
- A JS-only `npx expo export --platform ios` succeeded on the pinned starter, but is not an iOS native build. The generated `npm run lint` failed at Expo CLI’s ESLint version check despite ESLint 9.39.5; direct ESLint flagged a generated hook rule, and `npx tsc --noEmit` reported generated CSS/React Native Web type errors. Resolve checks relevant to the actual product; do not present the starter as clean or native-qualified.

### Translations to avoid

- Do not treat a single JavaScript codebase as a single native deliverable or as evidence that two platforms have the same interactions and capabilities.
- Do not use Expo Go as proof for libraries that include native code, custom app configuration or production build behavior; its native library set is fixed.
- Do not put server/provider credentials or authoritative authorization in the installed app. Users can inspect and modify client code and requests.
- Do not introduce an offline database or optimistic write queue before defining stale reads, retries, account isolation, conflict resolution and migration policy.
- Do not hand-edit generated native project files without knowing whether CNG will regenerate them. Make repeatable changes in app config/config plugins or deliberately own native directories.
- Do not claim lower maintenance, faster delivery or successful migration without testing both targets and measuring the application's actual workflows.

### Architecture sources

- [Expo create-expo-app and SDK 58 template selection](https://docs.expo.dev/more/create-expo/): During the documented SDK 58 transition, unqualified create-expo-app@latest creates SDK 57; the explicit default@sdk-58 template selects SDK 58.
- [Expo development and build workflows](https://docs.expo.dev/workflow/overview/): Expo separates JavaScript development, development builds, generated native projects and local/cloud native compilation; a chosen build workflow still needs platform-specific verification.
- [Expo development builds](https://docs.expo.dev/develop/development-builds/introduction/): Development builds include the app's native dependency set; Expo Go is a fixed playground and cannot load arbitrary custom native modules.
- [React Native platform-specific code](https://reactnative.dev/docs/platform-specific-code): React Native supports platform-specific files and APIs where shared code needs platform distinctions.
- [Expo SecureStore](https://docs.expo.dev/versions/latest/sdk/securestore/): SecureStore provides local encrypted key-value storage with platform-specific behavior and limits; it is not the backend identity authority.
- [Expo SQLite](https://docs.expo.dev/versions/latest/sdk/sqlite/): Expo provides SQLite for device-side relational persistence; choosing it does not define synchronization or conflict policy.
- [EAS Build](https://docs.expo.dev/build/introduction/): EAS Build compiles Expo/React Native apps in a hosted workflow; app configuration, native behavior, credentials and device verification remain project responsibilities.
- [EAS Submit](https://docs.expo.dev/submit/introduction/): Store submission is a distinct workflow requiring selected platform accounts and project release configuration.
- [React Native networking](https://reactnative.dev/docs/network): The app can issue native Fetch requests; the server/API remains an explicit application component.

## Transition options

Proposed designs and checks; these are not executed compatibility results.

### Browser and installed clients: Two native clients to shared Expo clients

**Inspect the source:** Inventory both applications' supported OS versions, route/deep-link formats, screen behavior, local schema, API versions, permissions, push tokens, app identifiers, signing owners and release cadence. Record platform-specific features rather than assuming code similarity.

**During coexistence:** Recommendation: keep the existing SwiftUI and Compose clients as production owners while implementing a bounded journey in Expo. Use the same versioned API contract; route only an explicit tester cohort to each new build. Preserve store identities where continued install/update compatibility is required.

**Target design:** Recommendation: choose which screens and domain behavior are genuinely shareable. Retain platform-specific paths for native capabilities and interaction differences. Adopt Expo as the primary client only after both builds satisfy the same declared user journeys, accessibility needs and supported-device requirements.

**Rollback:** Halt the Expo cohort and continue serving the prior native clients. Preserve API compatibility and local-data export/migration; mobile releases already installed cannot be rolled back by reversing server routing.

**Benefits and prerequisites**

- Shared TypeScript/React code can reduce duplicate screen and client-domain implementation across iOS and Android. Requires: The two products have sufficiently similar journeys, required native modules work on both platforms, and both build/release pipelines are qualified. Tradeoffs: React Native adds a JS runtime, native dependency/configuration matrix and Expo/React Native upgrade coordination. Platform-specific code remains; shared code does not imply one release artifact or one test matrix.

**Checks before transfer**

- Run the same core journey on supported iOS and Android devices with matching API fixtures; record intentional platform differences.
- Install the Expo build over a prior supported version or preserve the prior native client in its store track; check app identity, deep links, authentication and local user data.
- Use accessibility inspection and screen readers on both targets; verify large text, focus order, back behavior and permission-denied recovery.
- Verify each native dependency, push/deep-link entitlement and app configuration against the selected Expo SDK on both platforms.
- Keep the old clients and backend compatibility while adoption is mixed; compare product outcomes and crash/error data before retiring either client.

- https://reactnative.dev/docs/platform-specific-code
- https://docs.expo.dev/workflow/overview/
- https://docs.expo.dev/develop/development-builds/introduction/

### Data and schema: Preserve a separate backend contract

**Inspect the source:** Inventory API paths, request/response/error schemas, authorization decisions, pagination, idempotency, data ownership, offline state and the oldest supported client versions across both native apps.

**During coexistence:** Recommendation: keep the current backend as the single authoritative writer while the Expo client is introduced. Add backward-compatible API fields/routes or versioned endpoints only where a reviewed contract requires it.

**Target design:** Recommendation: keep the backend separate after client adoption. Move an API or domain responsibility only as a separately scoped server migration with its own schema, authorization, worker and rollback plan.

**Rollback:** Route the test cohort back to the prior clients while keeping the existing API authoritative. Preserve any new optional response fields and never reverse an irreversible server data migration as part of a client rollback.

**Benefits and prerequisites**

- The existing backend can serve old and new mobile clients during gradual adoption. Requires: The server retains compatible APIs and authorization for the full installed-client support window. Tradeoffs: Old client releases persist in the field; a new shared UI does not remove API versioning, device data or store-update constraints.

**Checks before transfer**

- Run versioned request/response fixtures from both old clients and the Expo client against a staging API.
- Verify object/tenant authorization on every API operation, including forged identifiers and expired or revoked sessions.
- Drop and recover the network during reads/writes; prove retry behavior is idempotent and visible to the user.
- Confirm backend schema and job producers have one migration owner; client delivery does not enqueue durable work locally.

- https://reactnative.dev/docs/network
- https://docs.expo.dev/develop/data-fetching/

### Identity and authorization: Keep session and authorization authority on the server

**Inspect the source:** Record token/session issuer, audience, expiry, refresh, revocation, device enrollment, account switching, local token storage, API authorization and logout behavior in each existing client.

**During coexistence:** Recommendation: keep the same identity issuer during the Expo pilot and store only the minimum client credential through a reviewed secure-storage mechanism. Retain backend authorization and versioned refresh/revocation behavior.

**Target design:** Recommendation: transfer an identity contract only if changing client libraries or credential formats is an explicit requirement. Use controlled reauthentication when formats cannot be safely shared; do not copy sessions between iOS Keychain and Android Keystore storage by assumption.

**Rollback:** Keep the old clients and issuer acceptance active during transition. Require a controlled sign-in if an Expo credential cannot be reconciled; never revive revoked sessions to preserve a visual seamless migration.

**Benefits and prerequisites**

- A shared client can reuse the same issuer and server-side permission model without changing account authority. Requires: The issuer's mobile flow is supported on both platforms and refresh/revocation behavior is tested. Tradeoffs: Secure storage APIs and backup behavior differ by platform; one UI implementation does not make credentials portable or authorization equivalent.

**Checks before transfer**

- Exercise login, logout, expiry, refresh, revocation and account switching separately on iOS and Android.
- After logout/account switch, ensure protected cached data and queued operations from the previous user cannot reappear or execute.
- Verify an expired, revoked or cross-tenant credential is denied by the backend, not just hidden by the client.
- Inspect backup/restore behavior for local credentials and require reauthentication if secure state cannot be restored safely.

- https://docs.expo.dev/versions/latest/sdk/securestore/
- https://reactnative.dev/docs/security

### Caching and shared state: Migrate only the explicitly supported device cache

**Inspect the source:** Inventory each client's local database/preferences, schema version, cached ownership, pending writes, retention, encryption and account separation. Classify data as disposable, offline-readable or unsynchronized user work.

**During coexistence:** Recommendation: initially keep the Expo client cache isolated and treat the existing native client caches as untouched. Exchange authoritative data through the backend; do not assume two native clients share local storage.

**Target design:** Recommendation: migrate only required user data through a versioned export/import or backend-mediated transfer. Add conflict/version handling for unsynced edits and remove the old format only after verified adoption.

**Rollback:** Keep the old client and source local database intact while the Expo migration is opt-in. Restore/reinstall from a verified export or re-fetch server-owned data; do not erase unsynced user work during rollback.

**Benefits and prerequisites**

- An isolated new cache limits risk to users who install the Expo client first. Requires: The product can re-fetch authoritative state or has a validated migration for unsynced local work. Tradeoffs: Users may need to sign in/download again; server backup does not preserve unuploaded local edits.

**Checks before transfer**

- Test fresh install, app update, account switch, OS backup/restore and low-storage behavior.
- If migrating unsynced work, verify record counts, ownership, schema conversion and conflict outcomes before deleting the source copy.
- Verify a stale cache cannot disclose another account's data after logout or device sharing.

- https://docs.expo.dev/versions/latest/sdk/sqlite/
- https://docs.expo.dev/develop/data-fetching/

### Delivery and recovery: Transfer builds and releases as a separate change

**Inspect the source:** Record bundle/application identifiers, signing owners, supported OS versions, store tracks, version/build-number rules, privacy declarations, native credentials, push setup, crash telemetry and server compatibility policy.

**During coexistence:** Recommendation: establish a separate internal/beta channel and development build for the Expo client while prior app releases remain supported. Use a distinct app identity if replacement/update continuity is not yet established; preserve owned identities only with a planned store upgrade.

**Target design:** Recommendation: adopt one Expo source project only after both platform release procedures, key custody, EAS/local build configuration and install/update behavior have been rehearsed.

**Rollback:** Halt additional distribution, continue backend support for already installed versions and publish a compatible forward fix when required. Preserve the old apps' artifacts and API behavior for the declared support window.

**Benefits and prerequisites**

- A shared source tree can coordinate feature changes across mobile clients. Requires: Both app identities and release pipelines remain under explicit owners, with test builds for each target. Tradeoffs: There are still two native binaries, platform-specific signing, store review, staged adoption and device matrices. EAS is an optional build service and account integration, not release evidence.

**Checks before transfer**

- Build and install signed internal builds on both platforms using the selected local/cloud build configuration.
- Test update over the supported prior version and confirm existing local data, deep links, notifications and API behavior.
- Confirm signing/account access, bundle/application identity, privacy declarations and store capabilities with the actual owner.
- Exercise a staged release stop and forward-fix plan; installed mobile releases cannot generally be rolled back by server routing alone.

- https://docs.expo.dev/build/introduction/
- https://docs.expo.dev/submit/introduction/

### Jobs and schedules: Keep durable jobs behind the API

**Inspect the source:** Inventory client-triggered operations, request idempotency keys, server-side job payload versions, queue owner, retries, notifications and the client-visible status contract.

**During coexistence:** Recommendation: both old and new clients submit the same versioned API command while one backend owns enqueue, retry and result state.

**Target design:** Recommendation: keep long-running, billable, scheduled or retryable work on the separately selected backend. The app may show progress and send eligible user-initiated local work but is not a reliable durable queue owner.

**Rollback:** Keep the existing backend queue and API owner; disable only the new client submission route while reconciling accepted/in-flight jobs by stable operation ID.

**Benefits and prerequisites**

- A single backend job owner can serve mixed client versions and survive app suspension or device loss. Requires: The API exposes an authorized, idempotent submission/status contract. Tradeoffs: Background notifications and client progress are eventually delivered and need separate OS permissions and server delivery behavior.

**Checks before transfer**

- Submit a retried request from each client and verify duplicate requests do not duplicate business effects.
- Suspend, force-stop or lose network during an operation; verify the server job continues and the client recovers its status.
- Check notification denial, delayed delivery and account switching if notifications are included.

- https://reactnative.dev/docs/appstate
- https://docs.expo.dev/versions/latest/sdk/notifications/

Rewrite workflow: /rewrite/guide.md
Shared contracts and phases: /rewrite/contracts.json


## Setup
1. Complete the selected starting point and baseline checks in the Generators section first; then continue with the integration steps appropriate to the chosen component.
2. From the generated project root, record app identifiers, supported platforms/OS versions, runtime, Expo SDK, API contract, permissions and build owner in the project's README. Keep the actual generated lockfile.
3. Select the backend independently. Keep database writes, user/resource authorization, AI/provider secrets, email and durable work server-side. Define versioned API responses and controlled client error handling; a mobile app binary is inspectable.
4. Implement route/screen state and API access behind testable modules. Keep device UI and domain rules separated enough to test shared logic, but do not abstract away meaningful iOS/Android interaction differences.
5. Add a native dependency only for a stated capability. Check both-platform support, config plugin, SDK compatibility and minimum OS/API before adding it. Build a development client instead of expecting Expo Go to contain it.
6. If offline behavior is required, specify local sources, accepted stale data, queued operations, conflict resolution, account switching and data deletion before choosing storage libraries. Server remains the authority for protected/shared data.
7. Run shared unit/API tests and build/install both native targets. Test navigation/back, permission denial, app restart, expired/revoked sessions, network loss/recovery and accessibility with representative emulators/simulators and physical devices.
8. Separate development, preview and production application identifiers as needed. Establish account/credential ownership, app store policy and update compatibility before preparing signed builds. No integration, signing or release is implied by generation.

## Verification
Commands below require the selected tools and project configuration. Replace example paths, schemes and IDs; distinguish tests from builds and interactive startup. These are instructions, not recorded passes.

```text
npx create-expo-app@latest --help
npx create-expo-app@latest mobile-app --template default@sdk-58 --yes --no-agents-md
npx expo install --check
npx expo-doctor
npx expo start
npx expo run:ios
npx expo run:android
```

## Open questions
- Which iOS and Android versions, phone/tablet form factors and devices are actually supported?
- Does the product need offline reads, offline writes or conflict resolution, and what is the authoritative data owner?
- Which API, identity provider, native SDKs, app links, notifications and permission flows are required?
- Which custom native libraries/config plugins are required, and are exact versions supported by the selected Expo SDK on both platforms?
- Who owns Apple and Google application identities, developer accounts, signing credentials, build service access and store release?

## Sources
- [Expo: Create a project](https://docs.expo.dev/get-started/create-a-project/)
- [Expo Router introduction](https://docs.expo.dev/router/introduction/)
- [Expo SDK version reference](https://docs.expo.dev/versions/latest/)
- [Expo SQLite](https://docs.expo.dev/versions/latest/sdk/sqlite/)
- [Expo data fetching](https://docs.expo.dev/develop/data-fetching/)
- [Expo SecureStore](https://docs.expo.dev/versions/latest/sdk/securestore/)
- [React Native security](https://reactnative.dev/docs/security)
- [Expo: Add custom native code](https://docs.expo.dev/workflow/customizing/)
- [Expo development builds](https://docs.expo.dev/develop/development-builds/introduction/)
- [Expo CLI](https://docs.expo.dev/more/expo-cli/)
- [Expo tools and Expo Doctor](https://docs.expo.dev/develop/tools/)
- [Expo build troubleshooting and SDK compatibility checks](https://docs.expo.dev/build-reference/troubleshooting/)
- [Develop an app with Expo](https://docs.expo.dev/workflow/overview/)
- [EAS Build introduction](https://docs.expo.dev/build/introduction/)
- [EAS Submit introduction](https://docs.expo.dev/submit/introduction/)
- [Expo unit testing](https://docs.expo.dev/develop/unit-testing/)
- [React Native platform-specific code](https://reactnative.dev/docs/platform-specific-code)
- [React Native accessibility](https://reactnative.dev/docs/accessibility)
- [Flutter multi-platform support (conditional alternative)](https://docs.flutter.dev/platform-integration)
- [Expo: create-expo-app, template pinning and SDK 58 transition](https://docs.expo.dev/more/create-expo/)

Keep the project README current and link the selected guidance; preserve existing project instructions.
