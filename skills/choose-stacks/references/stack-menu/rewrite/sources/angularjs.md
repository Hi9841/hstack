# AngularJS (1.x)

An application built on AngularJS 1.x, the original AngularJS framework. Official support ended in January 2022. AngularJS and modern Angular are distinct frameworks; migration requires mapping behavior and boundaries rather than assuming a version upgrade.

Reviewed: 2026-10-23 | Evidence: documentation-reviewed | Classification: source-only

Source guidance based on public documentation. It does not certify compatibility or establish what is installed in a particular application. Inventory the actual source, versions, extensions, data and operational owners before planning a rewrite.

## Application role

Language: JavaScript
Components: web
Roles: Browser interface
UI: client-rendered AngularJS directives, templates and scopes; determine whether the app uses single-page routing or embedded widgets
Host: Usually static browser assets plus separately owned APIs/services. Identify any server-side template or API responsibilities because they are not supplied by the browser framework.

## Responsibilities to inventory

- Browser interface: client-rendered AngularJS directives, templates and scopes; determine whether the app uses single-page routing or embedded widgets
- Controllers/components, directives, templates, scopes and digest-driven UI updates
- AngularJS module and dependency-injection graph
- Routes, forms, validation, filters and client-side HTTP behavior
- Build pipeline, polyfills, browser support and any custom framework extensions
- Separately owned authentication, APIs, databases, jobs and integrations
- Server runtime: inventory the actual API, identity, data, job, integration and hosting owners; the browser framework itself does not establish whether or how these exist.

## Lifecycle and version check

Official support ended
End of official support: January 2022

- Find exact angular.js/angular.min.js version, package lock entries and any locally patched or vendor-copied files.
- Inventory AngularJS modules and third-party directives, including their maintenance and license status.
- Consult official migration documentation for the exact 1.x APIs and breaking changes used; official support has ended, so verify current security and compatibility exposure separately.

## Application inventory before rewrite

Inventory the actual application before choosing a target. For every responsibility, record its owner and interface, then mark it kept, replaced or retired. A target match is not compatibility evidence.

- Map routes, templates, directives, controller/service interactions, watchers and global state.
- Record form validation, accessibility behavior, browser support, localization and deep-link behavior.
- Trace each HTTP call, authentication/session mechanism and server endpoint; note interceptors and error handling.
- Identify build and test commands, custom directives, direct DOM manipulation, plugins and deployment constraints.

## Change options

- Keep the source while stabilizing behavior and containing risk, with an explicit support and security plan.
- Use a staged/strangler migration: introduce a maintained target around selected routes or capabilities while old and new portions coexist behind explicit boundaries.
- Move the browser application to modern Angular if its architecture and team fit; plan component, dependency-injection, routing, forms and RxJS changes explicitly.
- Replace only a portion of the browser UI and keep existing APIs and data services under their current owners.

## Target research

Compare modern Angular and other browser targets against existing team knowledge, routing, forms, accessibility needs, API contracts and coexistence constraints. AngularJS support status does not by itself determine the target framework.

## Caution

AngularJS support ended, but that does not reveal the application's actual exposure or a safe migration path. Inventory exact versions, third-party modules and custom DOM behavior. Do not treat modern Angular as a drop-in version update.

## Sources

- [AngularJS Version Support Status](https://docs.angularjs.org/misc/version-support-status): The official AngularJS support policy records that support ended in January 2022.
- [Migrating an App to a newer version](https://docs.angularjs.org/guide/migration): Official migration documentation describes breaking changes across AngularJS releases and points to actively supported Angular separately.
- [UpgradeModule: AngularJS and Angular coexistence](https://angular.dev/api/upgrade/static/UpgradeModule): Angular documents bootstrapping a hybrid AngularJS/Angular application and sharing components and services through upgrade/static. Qualify this path against the actual versions and dependencies.

Lifecycle references: [https://docs.angularjs.org/misc/version-support-status](https://docs.angularjs.org/misc/version-support-status), [https://docs.angularjs.org/guide/migration](https://docs.angularjs.org/guide/migration)
