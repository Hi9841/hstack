# Abuse and fraud catalog

## Identity and communications

- OTP/SMS/voice pumping, toll fraud, international routing, retry multiplication, and
  provider-managed signup bypasses.
- Account farming, credential stuffing, password-reset harassment, email bombing,
  verification enumeration, and disposable identities.
- Invitation spam, contact-import abuse, impersonation, and user-to-user harassment.

## Value and entitlement

- Free-trial cycling, referral rings, coupon stacking, reward replay, self-referral,
  promo arbitrage, family/share-plan abuse, and entitlement state desynchronization.
- Checkout manipulation, webhook forgery/replay, refund/cancellation races, chargeback
  externalities, underpayment, and client-asserted payment success.
- Marketplace, booking, reservation, waitlist, inventory, check-in, and ticket hoarding.

## Resource and provider cost

- AI token/image/video generation exhaustion, prompt amplification, recursive agents,
  expensive file parsing, and unbounded context or output.
- Upload/storage/egress abuse, decompression bombs, media-transcode amplification,
  signed-URL sharing, and orphaned objects.
- Search/scraping, export/report generation, PDF rendering, map/geocoding, analytics,
  and third-party API fan-out.
- Queue amplification, retry storms, webhook loops, cron duplication, and cache-bypass
  compute exhaustion.

## Publishing and reputation

- Unauthorized or duplicated social publication, message sends, campaign enrollment,
  content poisoning, link abuse, spam, and moderation evasion.
- Provider account suspension risk, sender reputation damage, carrier filtering, and
  domain/email deliverability degradation.

## Signals and controls

- Velocity by account, target, IP, device, tenant, country, provider, and payment instrument.
- Fan-out/fan-in, novelty, failure/success ratio, cost per conversion, and graph clusters.
- Atomic reservation before cost, commit after provider acceptance, release on known-safe
  failure, and reconciliation for ambiguous provider outcomes.
- Layered budgets, allowlists, step-up checks, proof-of-work/CAPTCHA where appropriate,
  provider restrictions, scoped keys, alerts, kill switches, and manual review.
