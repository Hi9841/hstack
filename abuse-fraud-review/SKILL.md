---
name: abuse-fraud-review
description: >-
  Threat-model and review fraud, business-logic abuse, account farming, resource
  exhaustion, and cost amplification across SMS, email, voice, AI, storage, payments,
  rewards, referrals, trials, bookings, publishing, and other sensitive business flows.
  Use after an abuse incident, when adding a cost-bearing or scarce operation, or
  whenever conventional vulnerability review would miss an attacker acting through
  valid-looking requests.
---

# Abuse and fraud review

Model how an attacker can profit, avoid payment, obtain value, cost the owner money,
exhaust capacity, manipulate attribution, or deny scarce resources while sending
syntactically valid requests.

## Orient

1. Identify every deployable and entry point that reaches the business flow.
2. Map the unit economics: provider charge, internal compute/storage, scarce inventory,
   reward, entitlement, refund, support load, or reputation impact per successful action.
3. Identify authoritative identities and weak correlators: account, tenant, phone, email,
   IP, device, payment instrument, provider identity, session, and anonymous browser.
4. Label evidence as `PROVEN FROM CODE`, `PROVEN FROM COMMITTED/CI`, `PROVEN LIVE`,
   `PROVEN FROM PROVIDER`, or `UNVERIFIED`.

Read [references/abuse-catalog.md](references/abuse-catalog.md) and select relevant
flows. When technical compromise is also in scope, use an available security review capability or inspect that attack path directly. A missing companion skill must not block the abuse review.

## Enumerate bypasses before controls

For each value- or cost-bearing action, enumerate:

- all first-party routes, legacy routes, mobile/web variants, provider-managed flows,
  callbacks, admin paths, retries, queues, and direct-provider possibilities;
- rotation across accounts, targets, devices, IPs, countries, tenants, and sessions;
- concurrency, race, replay, retry, cancellation, partial failure, and cache reset paths;
- identity laundering through disposable accounts, virtual numbers, referrals, coupons,
  shared payment instruments, or compromised credentials;
- provider-key or dashboard compromise outside the application.

Do not accept a per-IP or per-target limit as a complete control. Establish whether all
paths share an atomic global or tenant budget and whether provider-side restrictions and
alerts independently cap damage.

## Evaluate the control stack

Assess controls at each layer:

1. Eligibility and step-up verification before the costly action.
2. Per-source, per-target, per-account, per-device, per-tenant, and geographic limits.
3. Atomic global budgets across every equivalent entry point.
4. Idempotency, replay protection, reservation/commit semantics, and concurrency safety.
5. Provider country/product restrictions, spend caps, scoped keys, and account alerts.
6. Detection based on velocity, fan-out, failure ratio, novelty, cost, and graph patterns.
7. Kill switches, degraded modes, reviewer/test bypass isolation, and safe recovery.
8. Reconciliation that compares provider truth, application events, and billing records.

## Testing boundaries

- Default to read-only source/provider inspection and local fixtures.
- Do not send real SMS/email/voice, create real charges, consume production rewards,
  flood endpoints, or test stolen credentials without explicit authorization.
- Never print provider credentials, recipient PII, payment data, cookies, or headers.
- Keep provider mutations, key rotation, WAF changes, spend caps, and production kill
  switches as explicit current-request actions.

## Report

For each abuse case include:

- attacker goal, entry point, prerequisites, and scale strategy;
- evidence label and exact code/provider/live evidence;
- unit and aggregate impact without invented financial precision;
- controls present, bypasses, and the maximum damage they actually bound;
- detection signal, immediate containment, durable remediation, and settling test;
- residual risk, including direct-provider and credential-compromise exposure.

Finish with a flow inventory and identify any cost-bearing route not covered by a shared
budget, provider restriction, alert, and kill switch. Never claim abuse is impossible.
