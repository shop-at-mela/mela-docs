# Cross-Shop & Entry/Exit Attribution Tracking PRD

## Document Information
- **Created**: 2026-07-18
- **Status**: Ready for dev
- **Owner**: Product / Dev
- **Related docs**:
  - `web-client/docs/analytics/crossshop-tracking.md` (source of truth for the event schema, GA4 setup steps, and reporting recipes — this PRD does not duplicate it)
  - `mela-docs/social/category-routing.yaml` (existing UTM schema this feature must interoperate with)
  - `product/prds/pre-redirect-sentiment-prd.md` (the existing pre-redirect interstitial this feature instruments)
  - `product/prds/trust-conversion-signals-prd.md` (documents the "Shop on {brand} →" CTA this feature instruments)

---

## Executive Summary

**Feature**: Instrument outbound "Shop from Brand" clicks with GTM + GA4 (+ Microsoft Clarity for qualitative session replay), to measure two hypotheses: (1) what share of sessions click out to **2+ distinct brands** ("cross-shop"), and (2) whether a session's **entry source** differs from the **brand(s) it exits to** (the "mutualization" signal — evidence that Mela's curation, not any single brand's own marketing, drove the click).

**Target URL / Entry Point**: Site-wide (GTM/GA4/Clarity load on every page); the instrumented event fires from the listing page's outbound CTA (`/l/:slug/:id`).

**Target Users**: Internal (Product/Founder) — this is measurement infrastructure, not a user-facing feature.

**Business Objective**: Prove or disprove that Mela's curation creates cross-brand discovery value beyond what any single brand's own ads/social would produce on their own — the core case for Mela's existence as a discovery layer rather than a single-brand storefront.

**Primary Success Metrics**:
- Multi-brand-clickout rate (sessions with 2+ distinct `brand_name` clickouts): **baseline**, target TBD after 30 days of data
- Entry≠exit rate (sessions where `entry_source` names a brand/platform different from any `brand_name` clicked): **baseline**, target TBD after 30 days of data
- `brand_clickout` event fires and survives the outbound click: **100% of clicks measured**, confirmed via DebugView (see verification checklist)

---

## 1. Problem Statement

### Current State
Mela has **no GTM/GA4/Clarity installed today** (confirmed: `REACT_APP_GOOGLE_ANALYTICS_ID` and `REACT_APP_PLAUSIBLE_DOMAINS` exist as Sharetribe-template hooks in `.env-template` but are unset in the live `.env` — see "Template Residuals" below). The only outbound-click signal that exists is the sentiment sheet's `pre_shopify_redirect` webhook event (Airtable, via `RedirectTrustSheet`), which captures qualitative thumbs up/down — not a structured, queryable clickstream.

Nobody today can answer: *does a shopper who lands on Mela via one brand's Pinterest ad go on to click into other, unrelated brands?* That's the entire thesis of "discovery marketplace vs. single-brand storefront," and right now it's unmeasured.

### User Pain Points
N/A — this is internal measurement infrastructure. No end-user-facing behavior changes as a direct result of this PRD (see Guardrails — no copy/UX changes beyond what's needed to fix an existing tracking gap).

### Business Impact of Inaction
Every week without this instrumentation is a week of unmeasurable traffic. The social team is already spending production time on UTM-tagged campaigns (`mela-docs/social/category-routing.yaml` → `tracking`) and manually cross-checking "GA4 sessions (UTM)" in `metrics-log.md` — but GA4 itself isn't installed, so that column has been unfillable since the tracking sheet was created (2026-07-13). This also blocks the “Clicks to Mela” metric that `cold-start-checklist.md` treats as the real north-star for the Month-1 social cold start (Week 3 gate: "Clicks to Mela — the real metric, > followers").

---

## 2. Goals & Non-Goals

### Goals
- Install GTM (single container) + GA4 (via GTM) + Microsoft Clarity, reading IDs from env vars, never hardcoded.
- Capture a normalized, first-touch `entry_source` per browser session, persisted once and never overwritten.
- Fire a complete `brand_clickout` event, with all required params, from **every** surface that opens a brand's Shopify store — not just the primary CTA (see §5, three click-out surfaces found in code).
- Fire the event so it reliably reaches GA4 given how the redirect actually works today (see §8 — the brief's original "beacon" premise needed correcting against real code).
- Document exact GA4 custom-dimension setup steps (event-scoped, not auto-created).
- Document how to build the two hypothesis reports in GA4 from raw event data.

### Non-Goals (this PRD)
- Server-side tagging / consent-mode / GDPR banner — logged in "Future roadmap" in the docs file, not built now.
- Affiliate-app postback / Tier-2 conversion tracking (actual purchase confirmation) — future roadmap.
- Fixing the pre-existing UX inconsistency where two of the three CTA surfaces bypass `RedirectTrustSheet` (see §5) is **in scope only to the extent required** to make `brand_clickout` fire from a single canonical point — see §5 for why this is unavoidable, not scope creep.
- New user-facing copy or UI. No strings change. Per house guardrail, any string this work *does* touch must attribute shipping/fulfillment to the brand, not Mela — but this PRD does not plan to touch any such string.
- A stable numeric/UUID `brand_id` field on the listing schema — **does not exist today** (see §5). This PRD proposes reusing the Sharetribe author (brand user) UUID, already used as the brand identifier internally in `configBrands.js`. Confirm this is acceptable before treating it as final.

---

## 3. User Stories

| As a... | I want to... | So that... | Priority |
|---------|-------------|------------|----------|
| Founder/PM | See what % of sessions click out to 2+ brands | I can prove/disprove the cross-shop discovery thesis | P0 |
| Founder/PM | See whether a session's entry brand differs from its exit brand(s) | I have evidence of "mutualization" (Mela's curation working, not pass-through traffic) | P0 |
| Founder/PM | Filter GA4 reports by `entry_source` | I can compare organic social, paid brand ads, SEO, and direct traffic cross-shop behavior | P0 |
| Social lead | Cross-check `metrics-log.md`'s "GA4 sessions (UTM)" column against real data | The Sunday tracking ritual (`cold-start-checklist.md`) is finally fillable | P1 |
| Dev | See the event fire in GA4 DebugView on a real click-through, not just in theory | I can trust the number before it's used to make decisions | P0 |

---

## 4. Feature Requirements

### Must Have (P0)
- GTM container + GA4 (via GTM) loaded via `REACT_APP_GTM_ID` / `REACT_APP_GA4_ID` env vars, added to `.env-template` with comments, never hardcoded.
- `window.dataLayer` initialized as early as the existing script-injection pattern allows (see §8 — matches the precedent already used for the dormant `REACT_APP_GOOGLE_ANALYTICS_ID` gtag.js hook in `src/util/includeScripts.js`).
- First-touch `entry_source` capture: UTM params + `document.referrer` → normalized string, written once to `sessionStorage['mela_entry_source']`, never overwritten on later pages within the same tab session.
- `brand_clickout` dataLayer event firing from **all** outbound click-out surfaces found in code (§5), with the full param set: `brand_name`, `brand_id`, `category`, `product_id`, `entry_source`, `destination`.
- GA4 custom dimensions registered (documented as manual Console setup steps — GA4 does not auto-create event-scoped custom dimensions from arbitrary event params).
- Microsoft Clarity loaded via `REACT_APP_CLARITY_ID`.
- CSP allowlist updated for `clarity.ms` (GTM/GA4 domains are already allowlisted — see §5 Template Residuals).

### Should Have (P1)
- A single shared `openBrandStorefront()` util (see §5) so all three click-out surfaces share one instrumented code path, instead of three copies of `dataLayer.push`.

### Nice to Have (P2)
- None identified for this MVP — see "Future roadmap" in the docs file for what's explicitly deferred.

---

## 5. Critical Findings From Codebase Research (read before estimating)

These are facts confirmed in `web-client/src/` — not assumptions. They change the shape of the implementation from what a first read of the brief would suggest.

### 5a. There are THREE outbound "Shop from Brand" click surfaces, not one
| Surface | File | Goes through `RedirectTrustSheet`? |
|---|---|---|
| Main sticky CTA | `src/components/OrderPanel/OrderPanel.js:595-608` | Yes, via `onShopNow` prop |
| Quantity/delivery form CTA (can render simultaneously with the above) | `src/components/OrderPanel/ProductOrderForm/ProductOrderForm.js:283-293` | **No** — calls `window.open` directly today |
| Inquiry-only listings CTA | `src/components/OrderPanel/InquiryWithoutPaymentForm/InquiryWithoutPaymentForm.js:28-34` | **No** — calls `window.open` directly today |

All three read `publicData.brand` (brand name) and `publicData.productUrl` (destination URL) — confirmed identical field names across all three files. `product_id` is the standard listing `id.uuid` (no separate custom field). `category` is `publicData.categoryLevel1/2/3` (existing pattern elsewhere in the codebase: use the most specific non-empty level, i.e. `categoryLevel3 || categoryLevel2 || categoryLevel1`).

**Why this matters**: instrumenting only the main CTA (`OrderPanel.js`) would silently miss clicks from the other two surfaces, undercounting `brand_clickout` on any purchase-type listing where the quantity form renders, and on any inquiry-only listing. To get complete data, either all three need their own `dataLayer.push`, or (recommended, §6) they share one call path.

### 5b. No stable `brand_id` field exists on the listing
Confirmed via grep across `configListing.js`, `types.js`, and the whole repo: brand is a free-text name only (`publicData.brand`). The one existing stable brand identifier in the codebase is the **Sharetribe author (brand user account) UUID**, already used as the canonical key in `src/config/configBrands.js` (`getBrandConfiguration(brandId)`, `getBrandScore(brandId)`, etc. — explicitly documented there as "Brand user UUID"). This PRD proposes using `listing.author.id.uuid` (available as `ensuredAuthor.id.uuid` in both `ListingPageCoverPhoto.js` and `ListingPageCarousel.js`) as `brand_id`. **This is a proposal, not a confirmed schema field — flagging per the "no invented facts" guardrail.**

### 5c. The redirect does NOT navigate the browser away from Mela — it opens a new tab
The brief's brief states: *"the click navigates the browser away from Mela, so a normal async GA hit can be killed mid-flight."* This is not what the code does. Every one of the three surfaces above calls:
```js
window.open(url, '_blank', 'noopener,noreferrer')
```
`_blank` opens the Shopify destination in a **new tab**; the original Mela tab is never unloaded. This means the "beacon or 150ms delay" mitigation described in the brief is solving a problem that doesn't exist in the current architecture — a same-tab `window.location` navigation would need it, `window.open('_blank', ...)` does not, because nothing in the Mela tab ever unloads. See the docs file's verification checklist and §8 below for what this changes about the implementation (still cheap to add defensively, but not the load-bearing fix the brief assumed).

### 5d. Two of the three surfaces bypass the pre-redirect trust sheet today
Per `pre-redirect-sentiment-prd.md`, `RedirectTrustSheet` is supposed to show once per session before the first outbound click. In practice, only the `OrderPanel.js` main CTA is wired to it (via `onShopNow`/`handleShopNow` in `ListingPageCoverPhoto.js` / `ListingPageCarousel.js`). `ProductOrderForm.js` and `InquiryWithoutPaymentForm.js` call `window.open` directly and never show the sheet. This looks like a pre-existing bug, separate from this PRD's scope — but making `brand_clickout` fire reliably from all three surfaces requires touching all three anyway (§6), so this PRD's implementation closes that gap as a side effect rather than leaving it in place. Flagging so it's a visible decision, not silent scope creep.

---

## 6. Recommended Architecture (dev-lead level, informing scope/estimate)

- New `src/util/analytics/entrySource.js` — capture + normalize + persist `entry_source`, called once per full page load in `src/index.js` (client-only branch). Because this file only executes once per hard navigation (not on in-app SPA route changes), it is naturally "first page of session," matching the requirement without extra routing logic.
- New `src/util/analytics/brandClickout.js` — exports `pushBrandClickout(params)` (pure `dataLayer.push`) and `openBrandStorefront(url, params)` (push, then `window.open`). All three click-out surfaces (and `RedirectTrustSheet`'s `onContinue`) call `openBrandStorefront` instead of `window.open` directly. This is the one change that both (a) gets complete coverage across all three surfaces and (b) fires the event at the moment of actual redirect rather than at button-press (avoiding false positives when a user dismisses the trust sheet without continuing).
- GTM script + Clarity script added to `src/util/includeScripts.js`, following the exact pattern already used there for the dormant `gtag.js`/Plausible hooks (external `<script src>` tags via `react-helmet-async`, gated behind env vars). **Not** added as a raw inline snippet in `public/index.html`, to avoid CSP nonce complications the existing gtag.js code already sidesteps (see docs file §"Template Residuals").
- CSP: add `clarity.ms` / `*.clarity.ms` to `connectSrc`/`scriptSrc`/`imgSrc` in `server/csp.js`'s customization block (not the `defaultDirectives`, per that file's own "do not edit defaults" comment). GTM/GA4 domains are already present.

Estimated scope: **M** (touches 5 existing files + 2 new util files + CSP + env template; no new UI, no new duck, no new container).

---

## 7. UX Requirements

None — no user-facing UI changes. The only observable behavior change is that `ProductOrderForm` and `InquiryWithoutPaymentForm`'s CTAs will now also show the pre-redirect trust sheet on a user's first click of a session (previously they bypassed it — see §5d), matching the main CTA's existing behavior.

---

## 8. Acceptance Criteria

- [ ] `REACT_APP_GTM_ID` and `REACT_APP_GA4_ID` (and `REACT_APP_CLARITY_ID`) are read from env vars, documented with comments in `.env-template`, never hardcoded.
- [ ] GTM container loads on every page; `window.dataLayer` exists before any listing page is interactive.
- [ ] On first landing in a browser session, `sessionStorage['mela_entry_source']` is set exactly once from UTM params (falling back to `document.referrer`, falling back to `'direct'`), and is never overwritten by subsequent page views in the same session.
- [ ] Clicking any of the three "Shop from Brand" surfaces (§5a) fires one `brand_clickout` dataLayer event with all six params populated (or explicitly `null` if genuinely unavailable, never silently dropped).
- [ ] The event is visible in GA4 DebugView, both on click and confirmed to still be present after the outbound tab opens (see docs file verification checklist — this is a "did it survive," not "did it fire" check, since §5c means survival is a much lower bar than the brief assumed).
- [ ] GA4 custom dimensions (`brand_name`, `category`, `entry_source`, `product_id`) are registered per the documented Console steps — dev does not assume they exist automatically.
- [ ] Microsoft Clarity loads and records a session, confirmed in the Clarity dashboard.
- [ ] No new user-facing string is added or changed. If review of the diff finds otherwise, it must attribute shipping/fulfillment to the brand, never Mela.
- [ ] `server/csp.js` updated for `clarity.ms`; existing Google Analytics / GTM CSP entries are left untouched (already sufficient).

---

## 9. Success Metrics & Measurement

Reporting lives entirely in GA4 — see `web-client/docs/analytics/crossshop-tracking.md` for the exact report-building steps. Summary:

| Metric | Definition | Report |
|---|---|---|
| Multi-brand-clickout rate | % of sessions with `brand_clickout` events naming 2+ distinct `brand_name` values | GA4 Explore, count distinct `brand_name` per session |
| Entry≠exit rate | % of sessions where `entry_source` names a brand/platform not equal to any `brand_name` clicked in that session | GA4 Explore, session-scoped comparison (see docs file) |

Both are **baseline-only** for this PRD — no target is set until 30 days of real data exists (consistent with `search-page-optimization-prd.md`'s precedent of shipping instrumentation before setting targets).

---

## 10. Dependencies & Risks

- **Dependency**: GTM container + GA4 property + Clarity project must be created in their respective consoles before env vars can be set (external, non-code setup — not blocking code review, blocking DebugView verification).
- **Risk**: `brand_id` (author UUID) proposal in §5b needs sign-off — if rejected, `brand_id` ships as `null` until a real field is defined, and cross-brand analysis falls back to `brand_name` string matching (works, but not collision-proof against near-duplicate brand names).
- **Risk**: Because two CTA surfaces currently bypass `RedirectTrustSheet` (§5d), fixing that as a byproduct of this work is a (small, positive) behavior change beyond pure instrumentation — flagged for visibility, not hidden in the diff.
- **No Sharetribe Console dependency** — this is entirely web-client code + external analytics consoles, no listing-field/extended-data changes needed for the MVP event schema.

---

## 11. Out of Scope / Future Considerations

See `web-client/docs/analytics/crossshop-tracking.md` → "Future roadmap" section (source of truth, not duplicated here): server-side tagging, consent-mode/GDPR, affiliate-app postback / Tier-2 conversion tracking, a real `brand_id` schema field if the author-UUID proposal is rejected.

---

## 12. Social Strategy Tie-In (requested alongside this PRD)

Reviewed `mela-docs/social/` end to end. Findings and recommendations:

1. **This closes an existing gap, it doesn't just add a new one.** `category-routing.yaml` → `tracking` already mandates UTM tags on every social destination URL (`utm_source`, `utm_medium=social`, `utm_campaign={brand_slug}_w{week}`), and `metrics-log.md` already has a "GA4 sessions (UTM)" column that's been unfillable since 2026-07-13 because GA4 was never installed. Shipping this PRD makes that column real for the first time.

2. **`entry_source` should be built to read the *existing* UTM schema, not a new one.** The brief's example values (`pinterest`, `instagram`, `seo`, `direct`) line up with `category-routing.yaml`'s `utm_source_values: {instagram, pinterest, reddit}`. The one brief example that does *not* have a documented source — `brand_ad:superbottoms` — implies a **paid**, brand-specific ad campaign. `category-routing.yaml` only documents *organic* social (`utm_medium: social`); there is no existing `utm_medium` convention for paid/brand-sponsored campaigns. **Flagging rather than inventing**: this PRD proposes `utm_medium=paid_social` (or `cpc`) as the signal that should map `utm_campaign`'s `{brand_slug}` into `brand_ad:{brand_slug}`, to be confirmed with whoever runs paid experiments (none appear to be running yet — `cold-start-checklist.md` Week 3 explicitly says "don't pay for ads — organic is proving the model").

3. **Additional goal worth considering**: once `brand_clickout` is live, the Sunday metrics ritual (`cold-start-checklist.md`) could replace its manual "Blotato clicks vs. GA4 sessions" cross-check with a direct GA4 view filtered by `utm_campaign`, and — new capability this PRD unlocks — **see whether a single week's IG/Pinterest push on Brand A also lifts clickouts to Brand B/C in the same sessions**. That's a direct, measurable version of the "wayfinding spine" bet the paused Instagram grid feature (`category-routing.yaml` → `grid.enabled: false`) is waiting on real profile-visit signal for — this data source is a faster, higher-fidelity proxy than Instagram Insights' own profile-visit count, and could inform the `grid.activation_gate` decision sooner than the currently-stated trigger.
4. **Reddit has no owned account** (participation-only, per `social/accounts.md`) — any `entry_source=reddit` sessions are necessarily organic mentions/link-shares, not a campaign Mela controls. Worth knowing before reading too much into that source's cross-shop numbers early on.
