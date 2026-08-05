# Insights PRDs

Measurement and reporting work: instrumentation that captures behavioral data, and the reports built on top of it.

## What belongs here

A PRD belongs in this folder if its deliverable is **knowledge rather than a shopper-facing capability**. The test: if it ships and no shopper could tell the difference, it is an insights PRD.

- Analytics instrumentation (dataLayer events, GTM/GA4/Clarity configuration)
- Reports, dashboards, and saved explorations
- Attribution and funnel definitions

## What does not

- Anything with a UI, even when its purpose is partly measurement. `pre-redirect-sentiment-prd.md` stays in `prds/` because `RedirectTrustSheet` is a real interstitial shoppers see and react to, and it is referenced elsewhere as a UX precedent. It happens to also emit a webhook.
- Technical specs. Event schemas and Console setup steps live in `mela-docs/technical/analytics/`, not here. PRDs state the problem, goals, and acceptance criteria; the technical docs are the source of truth for field names and click paths, and win on any disagreement.

## Contents

| PRD | Covers |
|---|---|
| [crossshop-tracking-prd.md](crossshop-tracking-prd.md) | The `brand_clickout` event, `entry_source` capture, GTM/GA4/Clarity install. The instrumentation layer. |
| [shopper-visibility-reporting-prd.md](shopper-visibility-reporting-prd.md) | Site search tracking, the potential shopper funnel, cross-shop explorations, Looker Studio. The reporting layer on top. |

Read them in that order. The first defines what is captured, the second defines what is asked of it.

## Companion technical docs

- `mela-docs/technical/analytics/crossshop-tracking.md` — event schema, `entry_source` normalization rules, GA4 Console setup, verification checklist.

## Status

Tracked in [`mela-docs/product/PRD_TRACKER.md`](../../PRD_TRACKER.md) alongside everything else. That table is deliberately flat, so this folder does not fragment the single-glance view.
