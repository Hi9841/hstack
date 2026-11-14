# Create React App

A React application bootstrapped and built with Create React App (CRA). React deprecated CRA for new applications in February 2025; existing applications can keep React while changing the build or application framework.

Reviewed: 2026-10-23 | Evidence: documentation-reviewed | Classification: source-only

Source guidance based on public documentation. It does not certify compatibility or establish what is installed in a particular application. Inventory the actual source, versions, extensions, data and operational owners before planning a rewrite.

## Application role

Language: JavaScript / TypeScript
Components: web
Roles: Browser interface
UI: client-rendered React; inspect routing, rendering, state and browser APIs in the actual app
Host: Typically emits static assets for a web server or CDN. Any separately owned API, authentication, jobs and data services remain outside CRA and must be inventoried independently.

## Responsibilities to inventory

- Browser interface: client-rendered React; inspect routing, rendering, state and browser APIs in the actual app
- React component and page behavior
- CRA scripts, webpack/Babel configuration and environment variables
- Routes, client state, forms and browser-side validation
- Static asset paths, public files, service workers and deployment rewrites
- Any separately owned API, identity, persistence, jobs and integrations
- Server runtime: inventory the actual API, identity, data, job, integration and hosting owners; the browser framework itself does not establish whether or how these exist.

## Lifecycle and version check

Deprecated for new applications; existing applications remain in maintenance mode
Deprecation announced 2025-02-14; CRA continues to work in maintenance mode

- Read package.json and the lockfile for react-scripts, React, Node and related tooling versions.
- Record custom webpack overrides, eject status, Babel/Jest configuration and installed scripts.
- Check CRA's official deprecation guidance and the target tool/framework's migration documentation at planning time; versions and ecosystem support can change.

## Application inventory before rewrite

Inventory the actual application before choosing a target. For every responsibility, record its owner and interface, then mark it kept, replaced or retired. A target match is not compatibility evidence.

- Map route behavior, authentication boundaries, browser storage, analytics, service worker and asset URL assumptions.
- List every API and service owner; record endpoints, request/response shapes, credentials and error behavior.
- Capture test, lint, build and deploy commands, environment variables, browser support and direct-route behavior.
- Identify build-time assumptions such as proxy configuration, public URL and imported environment variables.

## Change options

- Keep CRA temporarily while making a scoped dependency or application change, with an explicit maintenance and security plan.
- Retain React and replace CRA tooling with a build tool such as Vite, Parcel or Rsbuild when the app remains a client application; explicitly recreate required routing, testing, environment and deployment behavior.
- Move to a React framework when its routing, server rendering or full-stack capabilities match actual requirements; server rendering is not mandatory for every migration.
- Partially replace routes or isolated UI while preserving API, identity and data owners.

## Target research

React can remain the UI ecosystem. Compare the maintained React framework or build-tool paths against server-rendering, routing, deployment, API ownership and team requirements. A target guide is a starting point, not proof that its framework replaces every source responsibility.

## Caution

Do not equate CRA deprecation with React deprecation. A tooling change can alter routing, asset paths, environment variable conventions, service-worker behavior and build outputs. Verify each against the deployed app.

## Sources

- [Sunsetting Create React App](https://react.dev/blog/2025/02/14/sunsetting-create-react-app): React deprecated CRA for new apps, says existing apps continue in maintenance mode, and describes migration to a framework or build tool; client-side rendering can still be appropriate.
- [Creating a React App](https://react.dev/learn/creating-a-react-app): Current official React guidance describes framework and build-tool choices.

Lifecycle references: [https://react.dev/blog/2025/02/14/sunsetting-create-react-app](https://react.dev/blog/2025/02/14/sunsetting-create-react-app)
