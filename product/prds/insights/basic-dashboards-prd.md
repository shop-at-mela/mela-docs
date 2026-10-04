# Basic Analytics Dashboards PRD

## Document Information
- **Created**: 2026-10-02
- **Status**: 📝 Draft — for review. Partly built: `listing_view` / `brand_page_view` shipped 2026-10-02/03; a separate Looker report ("Mela Traffic & Engagement Overview", standalone, not a page on the Cross-Shop report) was started 2026-10-03 with Overview, Search and AI sources and Behavior pages. Tile corrections in §4.3 / §4.4 applied 2026-10-03.
- **Owner**: Product / Founder
- **Related docs**:
  - `product/prds/insights/crossshop-tracking-prd.md` (the instrumentation layer: `brand_clickout`, `entry_source`, `mela_session_id`, and the `saved_*` events in §14)
  - `product/prds/insights/shopper-visibility-reporting-prd.md` (site search tracking, Potential Shoppers Funnel, cross-shop Explorations, the existing `Mela Cross-Shop Dashboard`)
  - `mela-docs/technical/analytics/crossshop-tracking.md` (source of truth for event schemas, GTM objects, GA4 custom dimensions. Field names and click paths for this PRD's new events will be added there after review, and that doc wins on any disagreement)
  - `product/prds/add-to-cart-restoration-prd.md` (the Add to Cart / `/saved` surfaces this PRD reports on)

---

## Executive Summary

**Feature**: A standing "basics" view of Mela traffic and behavior, built by extending the GA4 + Looker Studio stack that already exists: how many people visit, the path they take, what they search, which products and brands they look at, how many add to cart, and how many click through to a brand's store.

**Target URL / Entry Point**: Internal. GA4 Explorations + Library collection, and a new "Basics" page on the existing `Mela Cross-Shop Dashboard` in Looker Studio. Two small web-client events are needed (listing view, brand page view).

**Target Users**: Internal (Founder/PM, social lead). No end-user-facing change.

**Business Objective**: Replace ad hoc GA4 digging with one glanceable place that answers the weekly questions, so the Sunday metrics ritual in `cold-start-checklist.md` and the OCTR baseline work in `storefront-validation-readiness-prd.md` §8 stop depending on reconstructing numbers by hand.

**Primary Success Metrics** (all baseline-only for 30 days, consistent with sibling PRDs):
- Time to answer "how many visitors, what did they look at, how many clicked out this week": from several GA4 sessions to **one dashboard page**.
- Share of the six asks below answerable from the dashboard without opening GA4: **6 of 6** (journey map is one link out, see §4).
- Every new event fires **exactly once** per qualifying view, confirmed in GA4 DebugView.

---

## 1. Problem Statement

### Current State

GTM, GA4 and Clarity have been live since 2026-07-19. A Looker Studio dashboard and three GA4 Explorations exist. Against the six things we want to track:

| Ask | Status today |
|---|---|
| Number of visitors | **Available.** GA4 native Users/Sessions. The Potential Shoppers Funnel defines a qualified visitor. No dashboard tile for the plain trend. |
| User journey map | **Not built.** No GA4 Path exploration exists. Depends on SPA `page_view` reaching GA4 reliably (see §8). |
| Search queries | **Available in GA4.** `view_search_results` with `search_term` shipped 2026-08-04. Not on the dashboard. No result count, so zero-result searches are invisible. |
| Products visited | **Not tracked as an event.** Only the generic `page_view`, so there is no clean "product viewed" count by product or brand. |
| Brands visited | **Not tracked as an event.** Same gap for brand pages. |
| Add to Cart | **Instrumented, unverified.** `saved_listing_toggle` with `source=add_to_cart_button`. GTM tags were wired 2026-08-23 and have not been verified end to end in GA4. |
| Shop brand CTA | **Available and verified.** `brand_clickout`. Already on the dashboard by brand. |

Two further limits: the product-view and brand-view gaps mean we can't compute view → add-to-cart → clickout rates per product or brand, and the journey map has no data source we have confirmed.

### User Pain Points

N/A for end users. Internally, each weekly review means rebuilding views in GA4 by hand, and several of the numbers asked for cannot be produced at all.

### Business Impact of Inaction

The OCTR baseline has an external deadline (`storefront-validation-readiness-prd.md` §8), and the cold-start social tracking still leans on Blotato click counts. Without product and brand view events, the funnel that tells us whether curation, listing pages, or the brand CTA is the weak step stays unmeasurable.

---

## 2. Goals & Non-Goals

### Goals
- One Looker Studio "Basics" page covering visitors, traffic sources, search terms, top products, top brands, add-to-cart, and shop-brand clickouts.
- A saved GA4 Path exploration as the journey map, linked from the dashboard.
- Close the product-view and brand-view event gaps with the minimum code needed.
- Define each metric precisely (numerator, denominator) so the numbers are reproducible.
- Verify delivery of existing events before any tile relies on them.

### Non-Goals
- No BigQuery export, custom-built dashboard, or new analytics vendor. Decision recorded 2026-10-02: extend GA4 + Looker Studio.
- No new shopper-facing UI or copy.
- No targets. Baseline for 30 days first.
- No session-scoped distinct-count metrics in Looker Studio (see §8). The multi-brand rate stays in the existing GA4 Exploration plus Sheets path.
- No individual user tracking or PII. Everything is session-level and anonymous.
- Server-side tagging, consent mode, and affiliate postback stay deferred per `crossshop-tracking.md` §8.

---

## 3. User Stories

| As a... | I want to... | So that... | Priority |
|---|---|---|---|
| Founder/PM | See visitors and sessions trending by day | I know whether traffic is growing and which social pushes moved it | P0 |
| Founder/PM | See the paths shoppers take through the site | I find where they drop off or loop | P0 |
| Founder/PM | See what shoppers search for | I learn demand the catalog doesn't cover | P0 |
| Founder/PM | See the most viewed products and brands | I know what to feature and which brands pull interest | P0 |
| Founder/PM | See view → add-to-cart → brand clickout counts together | I can tell which funnel step is weakest | P0 |
| Social lead | See visitors and clickouts by entry source | The Sunday ritual in `cold-start-checklist.md` is filled from real data | P1 |
| Founder/PM | See searches that returned nothing | I find catalog gaps directly | P1 |

---

## 4. Feature Requirements

### Must Have (P0)

**4.1 New events (the only code in this PRD)**

- **`listing_view`**: fires once when a listing page's data has loaded. Carries listing id, brand name, brand id, category. Uses the same field sourcing as `brand_clickout` (`publicData.brand`, author UUID as `brand_id`, most specific category level, `listing.id.uuid`) so the two events join cleanly on product and brand.
- **`brand_page_view`**: fires once when a brand page's data has loaded. Carries brand id and brand name.
- Both follow the existing `window.dataLayer.push` pattern, push explicit `null` for unavailable fields, and include `mela_session_id`.
- **Must not double fire** on re-render, back/forward navigation within the SPA, or data refetch. Fire once per page visit.
- Exact field names, GTM objects (Data Layer Variables, Custom Event triggers, GA4 Event tags) and GA4 custom dimensions are specified in `crossshop-tracking.md` once this PRD is approved, not here.

**4.2 Verification of what already exists (blocking)**
- Confirm a GA4 `page_view` fires on every SPA route change in the GTM-only setup. The legacy `GoogleAnalyticsHandler` is dormant (legacy GA ID unset, and must stay unset to avoid double counting), so this depends on a GTM History Change configuration. It has not been confirmed. The journey map and landing-page tiles depend on it.
- **Partial finding, 2026-10-02 (Chrome, `window.dataLayer` on production):** an in-app click from the homepage to a listing pushed `gtm.historyChange` and `gtm.historyChange-v2` (source `pushState`), so GTM does receive SPA route changes. No `listing_view` event exists, confirming gap 1. The tab title still showed the homepage title after navigation, confirming the stale-title issue. **Follow-up, same day (network):** after an in-app click to a listing, the browser sent a GA4 `g/collect` request with `en=page_view`, `dl` = the listing URL and `dr` = the homepage, about 10 seconds after the click. So a GTM tag does fire `page_view` on SPA route changes and the request leaves the browser. Both GA4 requests (initial and SPA) returned **HTTP 503** from this browser, the known issue in §8, so GA4 receipt is still **not confirmed**; check DebugView from a clean profile or phone. Correction: that request's `dt` carried the *new* listing title, so the stale-title behavior seen in the earlier tab-title read was not reproduced on the wire. Keep grouping by page path regardless, and re-test titles before relying on them.
- Live-verify `saved_listing_toggle`, `saved_page_view`, and `saved_recommendation_click` reach GA4 (flagged open in `crossshop-tracking.md` §3, 2026-08-23).

**4.3 GA4: journey map**
- Saved Path exploration `Journey Map`, using `Page path and screen class` for the path steps (never page title, which is stale on SPA navigation). Starts from the landing page, with native **Session source / medium** as the breakdown where the tool allows (corrected 2026-10-03 from the custom `Entry Source`, which was mostly "(not set)"; see `utm-attribution-restoration-prd.md`).
- Added to the existing `Cross-Shop Tracking` Library collection.
- Path exploration is not available in Looker Studio. The dashboard links to it.

**4.4 Looker Studio: "Basics" page** on the existing `Mela Cross-Shop Dashboard`, standard GA4 connector only:

| Tile | Shape | Source |
|---|---|---|
| Users, Sessions | Scorecards with prior-period comparison | GA4 native |
| Potential-shopper sessions | Scorecard | Sessions reaching a listing or brand page |
| Visitors over time | Time series, by day | GA4 native |
| Top landing pages | Table | **`Landing page`** × sessions (corrected 2026-10-03: `Page path and screen class` counts every page view, not entry pages. Never Page title) |
| Sessions by source | Bar/table | **Session source / medium** and **Session campaign** (corrected 2026-10-03: native GA4 attribution, now that `utm_*` reaches GA4. The custom `Entry Source` stays for `brand_clickout` joins only) |
| Top search terms | Table | `view_search_results` count by `search_term` |
| Top viewed products | Table | `listing_view` count by Product ID / brand |
| Top viewed brands | Table | `brand_page_view` count by Brand Name |
| Add to Cart count | Scorecard | `saved_listing_toggle`, `Save Toggle Source` = `add_to_cart_button`, `Is Saved` = true. **Check first (2026-10-03):** confirm the value format GA4 stores for `Is Saved` (`true`, `1` or `"true"`) before writing the filter. Not yet verified. Also see the `source` parameter issue below |
| Shop-brand clickouts | Scorecard + by brand + by surface | `brand_clickout`. Decision 2026-10-04: the clickout step is the `/saved` page "Shop on {brand}" CTA (`saved_surface` = `saved_item_card` or `saved_brand_group`); count and break down on `Saved Surface`. Out-of-stock PDP clickouts (`saved_surface` null) are the only other source and are shown separately. |
| Funnel comparison | Bar of three event counts | `listing_view` → add-to-cart → `brand_clickout` (event counts, not session-scoped, labeled as such) |
| Link to `Journey Map` | Link/text | GA4 Exploration |

### Should Have (P1)
- Search result count carried on the search event, so zero-result searches can be listed. Needs a code-side push once results settle, or a decision to skip (see §9).
- Visitors and clickouts broken down by Session source / medium and campaign for the social ritual (was `Entry Source`; corrected 2026-10-03).
- Clickouts split by `saved_surface` (existing param).

### Nice to Have (P2)
- BigQuery export, which is the only correct route for session-scoped metrics in Looker Studio (see `shopper-visibility-reporting-prd.md` §4 P2).

---

## 5. UX Requirements

None for shoppers. For the internal dashboard: one page, tiles ordered traffic → behavior → intent, plain titles that state the metric and its definition, and a visible "as of" date range. Labels on the funnel-comparison tile must say it compares event counts, not the same sessions.

---

## 6. Acceptance Criteria

**Events**
- [ ] `listing_view` fires exactly once per listing page visit with all params populated (or explicit `null`), including across in-app back/forward navigation and re-renders.
- [ ] `brand_page_view` fires exactly once per brand page visit under the same rules.
- [ ] Both events appear in GA4 DebugView, verified from a clean browser profile or phone (see §8), after waiting about 10 seconds for SPA events.
- [ ] No existing event's behavior changes (`brand_clickout`, `saved_*`, `view_search_results` counts do not shift).

**Verification of existing instrumentation**
- [ ] GA4 `page_view` confirmed on SPA route changes in the GTM-only setup, or the gap is documented with a fix proposed.
- [ ] The three `saved_*` events confirmed reaching GA4 end to end.

**GA4**
- [ ] `Journey Map` Path exploration saved and shows non-zero paths, added to `Cross-Shop Tracking`.
- [ ] Required custom dimensions registered, and any reused dimension (Brand Name, Category, Product ID, Mela Session ID) confirmed to resolve for the new events.

**Looker Studio**
- [ ] Every tile in §4.4 renders real, non-zero data.
- [ ] Each tile's definition matches §7.
- [ ] No session-scoped distinct-count calculated field on the standard connector.
- [ ] View-only link works in a logged-out browser.

---

## 7. Success Metrics & Measurement

| Metric | Definition | Source |
|---|---|---|
| Visitors | GA4 Users, date range stated on the tile | GA4 native |
| Potential shopper rate | Sessions reaching `/l/:slug/:id` or `/brands/:brandSlug` ÷ all sessions | Existing funnel definition |
| Listing view → add-to-cart rate | `saved_listing_toggle` (add_to_cart_button, saved) ÷ `listing_view`, event counts | New + existing event |
| Add-to-cart → clickout rate | `brand_clickout` ÷ add-to-cart events, event counts. Clickouts come from `/saved` (the intended path, `saved_surface` set) and, rarely, out-of-stock listings; the brand-page link was removed 2026-07-26 | Existing |
| OCTR | Sessions with `brand_clickout` ÷ all sessions, owned by `shopper-visibility-reporting-prd.md` | Existing, referenced only |
| Search → listing view | `listing_view` events following a `view_search_results`, tracked in the Path exploration, not a tile | GA4 Explorations |

Event-count ratios are an approximation of the true session funnel. They are good for trend and relative step strength, not for exact conversion claims. Exact session-scoped rates remain in GA4 Explorations or a future BigQuery setup.

---

## 8. Dependencies & Risks

- **GTM SPA page_view is unverified.** See §4.2. If it is not firing, the journey map and landing-page tiles are blocked until GTM is fixed. This is the highest-priority check.
- **Add to Cart is a save, not a real cart.** `saved_listing_toggle` records a save from the Add to Cart button. Label tiles "Add to Cart (saves)" so the number is not read as checkout intent.
- **Page title is stale on SPA navigation.** Path-based reports group by Page path; entry-page tiles use `Landing page`.
- **`source` event parameter may be read as traffic source (found 2026-10-03, unconfirmed).** Session source / medium shows `heart_icon` and `add_to_cart_button` rows, which match the `source` parameter on `saved_listing_toggle`. Investigation pending; a rename (e.g. `save_source`) is the likely fix.
- **Data-quality fixes 2026-10-04.** `view_search_results` was firing on every page and on filter changes (fixed in GTM Version 8; counts before ~2026-10-04 are inflated, so annotate that date on the search tiles). The `saved_listing_toggle` `source` parameter was polluting Session source / medium (now `save_source` in GTM Version 9; use the new `Save Source` dimension, and combine it with `Save Toggle Source` for history). `brand_clickout` and `brand_page_view` read zero for structural reasons: the brand-page outbound link was removed 2026-07-26 and in-stock Add to Cart replaced the PDP Shop button, so the Funnel tile's clickout step will stay near zero. Details in `crossshop-tracking.md` and `shopper-visibility-reporting-prd.md`.
- **Owner browser GA4 hits return HTTP 503** (`shopper-visibility-reporting-prd.md` §8). Absence of an event in DebugView from that browser is not evidence of a broken tag. Verify from a clean profile or phone.
- **SPA events arrive with about a 6 second delay.** Wait about 10 seconds before concluding an event did not fire.
- **Ad-blocker undercount (typically 10–30%).** Absolute counts are understated. Ratios hold up better.
- **Google Signals must stay off.** Turning it on activates identity thresholding and would blank low-volume rows, which are most of what this dashboard shows.
- **Custom dimensions take 24–48 hours** to populate in standard reports. Use DebugView/Realtime to verify immediately.
- **Double-counting risk.** Site search is already handled in GTM, so a code-side search event (P1) must not duplicate `view_search_results`. Listing and brand events must be guarded against re-render.
- **Looker Studio aggregates at query level**, so session-scoped distinct counts silently compute wrong. None are attempted here.
- **Custom dimension quota.** Reuse existing dimensions where the parameter name matches, as done for Product ID on 2026-08-23.

---

## 9. Open Questions

1. **Search result count (P1)**: is `results_count` worth a code change, or is GTM-only `search_term` enough for now?
2. ~~**`filter_applied` (P2)**: in scope for this round, or deferred?~~ **Resolved 2026-10-02: deferred.** Moved to §10.
3. **Event naming**: `listing_view` and `brand_page_view` are proposals. GA4 has recommended event names (`view_item`) that unlock built-in ecommerce reports. Worth choosing deliberately before building, since renaming later breaks history. Confirm preference.
4. **Where the dashboard page lives**: a new "Basics" page on the existing report (assumed here), or a separate report for sharing?
5. **Who verifies** on a clean profile or phone, given the owner-browser 503 issue?

---

## 10. Out of Scope / Future Considerations

- **`filter_applied` event** (filter key and value from the search filters). Deferred 2026-10-02.
- BigQuery export and SQL-based session metrics (multi-brand rate in Looker, true session funnels).
- Server-side tagging, consent mode, affiliate postback for confirmed purchases. `brand_clickout` measures intent, not revenue.
- Clarity-based qualitative analysis. Clarity remains the tool for session replays and heatmaps, and is not part of this dashboard.
- The two production findings already logged in `shopper-visibility-reporting-prd.md` §9 (CSP not enabled in production, www/apex mismatch) remain separate items.

---

## 11. Suggested Sequencing (proposal, nothing started)

| # | Step | Effort | Blocking? |
|---|---|---|---|
| 0 | Designate a clean verification profile or phone | 15 min | Yes. Every "event did not fire" check depends on it. |
| 1 | Verify GTM SPA `page_view` and the three `saved_*` events reach GA4 | ~30 min | Yes. Journey map and cart tiles depend on it. |
| 2 | Resolve §9 questions 1–3 | Discussion | Yes, for event naming |
| 3 | Code + GTM for `listing_view` and `brand_page_view`, register custom dimensions | Small | Blocks product/brand tiles |
| 4 | Build `Journey Map` and add to Library collection | ~20 min | No |
| 5 | Build the Looker "Basics" page | ~1 hr | No. Product/brand tiles wait for step 3 data and 24–48h dimension lag |
| 6 | Add schemas, GTM objects, dimensions and click paths to `crossshop-tracking.md` | ~1 hr | No |

Steps 0 and 1 are the only real blockers. Steps 3 and 6 follow only once this PRD is approved.
