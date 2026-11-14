# WooCommerce

A WooCommerce store running within WordPress. WooCommerce remains a supported commerce system; this source entry covers commerce-specific responsibilities and refers to the shared WordPress source for CMS, roles, themes, plugins and hosting inventory.

Reviewed: 2026-10-23 | Evidence: documentation-reviewed | Classification: source-only

Source guidance based on public documentation. It does not certify compatibility or establish what is installed in a particular application. Inventory the actual source, versions, extensions, data and operational owners before planning a rewrite.

## Application role

Language: PHP / JavaScript
Components: web
Roles: Browser interface, Server runtime, Publishing, Plugins and custom behavior, Orders, Payments, Commerce operations
UI: Storefront product/category pages, cart and checkout plus WordPress/WooCommerce administration; the actual theme, blocks and extensions shape the customer and operator experience.
Host: A WordPress PHP/database deployment plus WooCommerce storage and operational integrations. Payment gateways, tax/shipping services, email, inventory, fulfillment and hosting can have independent owners; inspect their actual configuration.

## Responsibilities to inventory

- Browser interface: Storefront product/category pages, cart and checkout plus WordPress/WooCommerce administration; the actual theme, blocks and extensions shape the customer and operator experience.
- Shared WordPress core, content, users/roles, theme/plugin/custom code and hosting responsibilities: see the WordPress source record at [WordPress source guide](/rewrite/sources/wordpress/).
- Products, variations, attributes, categories, stock, downloadable/virtual products, coupons and reviews
- Cart, checkout, customer accounts, addresses, order lifecycle, refunds and order communications
- Payment gateway configuration and event/webhook flows; never assume payment secrets or provider behavior are contained in the theme
- Tax, shipping, subscriptions/memberships, inventory, fulfillment, fraud, analytics and other extension-specific behavior
- WooCommerce version, data storage mode/tables, scheduled actions/cron, APIs and integrations
- Server runtime: inventory the actual API, identity, data, job, integration and hosting owners; the installed platform and its extensions own server-side behavior; inspect their actual configuration and owners.

## Lifecycle and version check

Supported platform; compatibility and support depend on installed WooCommerce, WordPress, PHP, theme, gateway and extension versions
No end-of-life claim; check current official WooCommerce compatibility/update guidance for the installed versions

- Record WooCommerce, WordPress, PHP and database versions and whether High-Performance Order Storage (HPOS) is enabled/compatible.
- Export payment, shipping, tax, subscription, membership, inventory, checkout and fulfillment extensions with exact versions and account owners.
- Check each extension and gateway's current compatibility and migration documentation; a core compatibility claim does not certify a custom store.
- Stage updates and migration rehearsal with backups of both the database and wp-content files, including uploads, themes and extensions.

## Application inventory before rewrite

Inventory the actual application before choosing a target. For every responsibility, record its owner and interface, then mark it kept, replaced or retired. A target match is not compatibility evidence.

- Use the shared WordPress inventory for CMS content, users/roles, theme/plugin/custom code, hosting, media, URL and editorial responsibilities.
- Map catalogue structure, SKUs, variations, stock ownership, pricing, promotions, downloads and product-specific metadata.
- Map cart/checkout paths, payment methods, gateway callbacks/webhooks, tax rules, shipping zones/rates, coupons and fraud controls.
- Record customer/order history, statuses, refunds, subscriptions, renewals, privacy/retention constraints, emails and fulfillment handoffs.
- Identify order/product database storage and custom metadata, API consumers, scheduled actions, webhooks, reconciliation and rollback requirements.
- Set a migration cutover strategy for concurrent order writes, stock updates, payment settlement, customer access and reconciliation; validate with real representative records.

## Change options

- Keep WooCommerce as the commerce owner while replacing a storefront or integration layer through explicit supported APIs and boundaries.
- Upgrade WooCommerce/WordPress or replace selected extensions after compatibility and staged workflow checks.
- Partially replace catalog, checkout, fulfillment or integration capabilities only after identifying the new system of record and bidirectional synchronization rules.
- Fully replace the store platform only when catalogue, accounts, orders, payments, tax/shipping, subscriptions, fulfillment, communications and operations each have a named destination or explicit retirement decision.

## Target research

First establish whether the scope is storefront, integration or the full commerce system. Investigate target capability against actual catalogue, customer, order, payment, tax, shipping, subscription and fulfillment needs. A custom frontend does not require replacing the commerce backend, and a generic web application framework is not itself a commerce implementation.

## Caution

Do not treat product export as a complete store migration. Orders, customer data, extensions, live order writes, stock, subscriptions, gateway events and operational processes can need separate transfer and validation. This source record does not certify any target's compatibility with WooCommerce data or plugins.

## Sources

- [How to update WooCommerce](https://woocommerce.com/document/how-to-update-woocommerce/): WooCommerce recommends a current backup and staging where possible, identifies both database and wp-content data, and calls out customer-critical workflow tests.
- [Installed Database Tables](https://woocommerce.com/document/installed-database-tables/): WooCommerce documents core tables for orders, products, customers and related operational data.
- [Managing WooCommerce Data Stores](https://developer.woocommerce.com/docs/best-practices/data-management/data-stores): Developer documentation describes CRUD data classes and data-store boundaries, including core post-based and custom-table storage.
- [Migrating products between sites](https://woocommerce.com/document/migrating-products-between-sites/): Official guidance describes product data transfer options and limitations; product migration alone does not establish full store migration.

Lifecycle references: [https://woocommerce.com/document/how-to-update-woocommerce/](https://woocommerce.com/document/how-to-update-woocommerce/), [https://woocommerce.com/document/installed-database-tables/](https://woocommerce.com/document/installed-database-tables/)
