# WordPress

A WordPress site or application. WordPress remains a supported system; source coverage does not classify it as obsolete or recommend replacing it. Its real behavior can extend well beyond core through themes, plugins and custom code.

Reviewed: 2026-10-23 | Evidence: documentation-reviewed | Classification: source-only

Source guidance based on public documentation. It does not certify compatibility or establish what is installed in a particular application. Inventory the actual source, versions, extensions, data and operational owners before planning a rewrite.

## Application role

Language: PHP / JavaScript
Components: web
Roles: Browser interface, Server runtime, Publishing, Plugins and custom behavior
UI: Public theme/site pages plus WordPress administration and editor interfaces; block editor, classic editor or custom editorial interfaces depend on installation.
Host: A PHP runtime, database and web server or managed WordPress host, with files/media and operational services. Hosting, cache, search, email, backups and CDN may be external; inventory the actual topology.

## Responsibilities to inventory

- Browser interface: Public theme/site pages plus WordPress administration and editor interfaces; block editor, classic editor or custom editorial interfaces depend on installation.
- Pages, posts, taxonomies, custom post types, metadata, revisions, media and permalink behavior
- Administrator/editor/author/contributor roles, login, sessions and editorial permissions
- Theme templates, blocks, widgets, menus, styles and custom theme code
- Plugins, must-use plugins, custom plugins, hooks, shortcodes and integrations
- PHP and WordPress core versions, database, uploads, cron, cache, search, email and hosting/deployment
- SEO metadata, redirects, forms, analytics, consent, accessibility and public URL behavior
- Server runtime: inventory the actual API, identity, data, job, integration and hosting owners; the installed platform and its extensions own server-side behavior; inspect their actual configuration and owners.

## Lifecycle and version check

Supported platform; status of a particular installation depends on its core, PHP, theme and plugin versions
No end-of-life claim; inspect official release and support information for the installed versions at planning time

- Record WordPress core version, PHP version, database/server details, multisite status and hosting provider/runtime.
- Export the active and installed plugin/theme list with versions; identify premium, custom and must-use extensions and their owners.
- Check current WordPress, PHP, plugin and theme compatibility/support information directly with their maintainers; no broad platform label establishes the support state of this site.
- Check update/backup procedures and test recovery before changing or replacing the installation.

## Application inventory before rewrite

Inventory the actual application before choosing a target. For every responsibility, record its owner and interface, then mark it kept, replaced or retired. A target match is not compatibility evidence.

- Export database and files/media; map URL/permalink structure, redirects, canonical URLs, robots/sitemap and public page templates.
- Inventory users, roles, capabilities, editorial review, scheduled publishing, revisions and account recovery.
- For each plugin/theme/customization record purpose, data touched, hooks/APIs, owner, licensing, support and replacement decision.
- Identify forms, search, comments, localization, analytics, SEO, caching, email, backups, cron and external integrations.
- Record accessibility and content behavior checks; preserve content IDs/URLs or define redirects and migration mappings.

## Change options

- Retain WordPress and update or replace specific themes/plugins when that continues to meet product requirements.
- Refresh the presentation layer while WordPress remains the content/editorial owner; specify API, preview, authentication and cache boundaries.
- Partially replace a bounded capability while preserving WordPress content and administrative workflow.
- Fully replace WordPress only after assigning every retained publishing, identity, content, media, integration and operations responsibility to a named target or explicitly retiring it.

## Target research

Select a target from actual responsibilities: content model, editing workflow, permissions, integrations, media, URL/SEO behavior and hosting. A frontend framework alone does not supply WordPress publishing or plugin behavior. Do not infer PHP expertise or a Laravel fit from WordPress ownership.

## Caution

WordPress core documentation cannot enumerate this site's plugin/theme behavior. A frontend-only rewrite can silently lose content editing, roles, search, forms, SEO, redirects or integrations. Require an installed system inventory and assign each capability kept, replaced or retired before migration design.

## Sources

- [WordPress Features](https://wordpress.org/about/features/): WordPress describes publishing, user management, media, themes, plugins, custom content types and REST API capabilities; plugins can substantially extend core.
- [Updating WordPress](https://wordpress.org/documentation/article/updating-wordpress/): Official update guidance describes backups, core updates and the fact that custom core-file modifications can be overwritten.
- [Manage Plugins](https://wordpress.org/documentation/article/manage-plugins/): Official plugin guidance describes installed plugin management and recommends a current backup before updates.

Lifecycle references: [https://wordpress.org/about/features/](https://wordpress.org/about/features/), [https://wordpress.org/documentation/article/updating-wordpress/](https://wordpress.org/documentation/article/updating-wordpress/)
