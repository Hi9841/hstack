# Vue 2

An application using Vue 2, including the final Vue 2.7 release. Vue 2 reached end of life on 2023-12-31. Vue 3 is a natural migration candidate when the application should stay in the Vue ecosystem; the source's plugins and APIs still require review.

Reviewed: 2026-10-23 | Evidence: documentation-reviewed | Classification: source-only

Source guidance based on public documentation. It does not certify compatibility or establish what is installed in a particular application. Inventory the actual source, versions, extensions, data and operational owners before planning a rewrite.

## Application role

Language: JavaScript / TypeScript
Components: web
Roles: Browser interface
UI: client-rendered Vue component tree; inspect Options API/Composition API usage, plugins, router and state management
Host: Often static browser assets plus separately owned APIs/services. Identify server rendering, server templates and deployment responsibilities separately.

## Responsibilities to inventory

- Browser interface: client-rendered Vue component tree; inspect Options API/Composition API usage, plugins, router and state management
- Vue components, directives, filters and reactive state
- Vue Router routes, navigation guards and history fallback where used
- Vuex or other shared state and persistence plugins where used
- Build tooling, single-file component compilation, polyfills and browser support
- Separately owned APIs, identity, persistence, background work and integrations
- Server runtime: inventory the actual API, identity, data, job, integration and hosting owners; the browser framework itself does not establish whether or how these exist.

## Lifecycle and version check

End of life; no new features, updates or fixes from the Vue team
End of life: 2023-12-31; final Vue 2 release: 2.7.16

- Read package.json and lockfiles to find Vue, vue-template-compiler, Vue CLI/Vite plugins, router and state-library versions.
- Identify whether the application uses Vue 2.7 Composition API support, custom render functions, filters, plugins or compiler options.
- Use the official Vue 3 migration guide and the migration build guidance against the actual feature set; recheck plugin compatibility at planning time.

## Application inventory before rewrite

Inventory the actual application before choosing a target. For every responsibility, record its owner and interface, then mark it kept, replaced or retired. A target match is not compatibility evidence.

- Map route names, URL patterns, navigation guards, forms, validation and browser-visible behavior.
- Trace global state, persistence, event buses, custom directives, filters and third-party component libraries.
- Record SSR/SSG behavior, build commands, asset paths, browser support and deployment routing.
- List API contracts, authentication, permissions, data owners and tests for critical journeys.

## Change options

- Keep Vue 2 only as a bounded transition or maintenance choice with a documented support and security plan.
- Upgrade within Vue to Vue 3, using the migration build or staged component conversion where appropriate and qualifying each dependency.
- Replace selected modules or routes incrementally while preserving APIs and data ownership.
- Choose another browser stack only when requirements or team constraints justify leaving Vue; do not force that outcome because another guide exists.

## Target research

Vue 3 is the natural first target to investigate for a Vue 2 source. Compare the official migration path, build tooling, component/library compatibility, router/state changes and required server behavior before considering a different framework.

## Caution

Vue 2 end of life does not make a migration automatic. Third-party packages and custom component behavior may be the largest constraints. Vue 3 is not guaranteed compatible with the installed Vue 2 ecosystem.

## Sources

- [Vue 2 Has Reached End of Life](https://v2.vuejs.org/eol/): Vue records the 2023-12-31 end-of-life date, no further Vue-team features/updates/fixes, final version 2.7.16 and recommends Vue 3 for new work.
- [Migration to Vue 2.7](https://v2.vuejs.org/v2/guide/migration-vue-2-7): Vue's final 2.7 release has selected Composition API and tooling support that can inform a staged migration.
- [Migration Build](https://v3-migration.vuejs.org/migration-build): The official Vue 3 migration build can expose compatibility warnings and support incremental migration, subject to its documented limits.

Lifecycle references: [https://v2.vuejs.org/eol/](https://v2.vuejs.org/eol/)
