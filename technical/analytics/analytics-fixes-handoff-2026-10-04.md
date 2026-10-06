# Analytics Data-Quality Fixes: Handoff (2026-10-04)

**Status**: Search and `save_source` fixes are live. The `brand_clickout` problem is diagnosed as funnel volume, not tracking. Resume from "Open items" below.
**Related**: `crossshop-tracking.md` (schemas, GTM objects), `shopper-visibility-reporting-prd.md` (search tracking), `basic-dashboards-prd.md` (dashboard tiles), `utm-attribution-restoration-prd.md`.
**IDs**: GA4 property 546144789 (account 401593153), GTM `GTM-5JSJ54C2` (account 6366827557, container 258745015, workspace 8), Looker report "Mela Traffic & Engagement Overview" (id 536e8582-fe47-426a-a986-15259c804e23).

## What was found and fixed

| # | Issue | Cause | Fix | State |
|---|---|---|---|---|
| 1 | `heart_icon` / `add_to_cart_button` rows in Session source / medium | GTM tag `GA4 - saved_listing_toggle` sent an event parameter literally named `source`, which GA4 read as traffic source | Tag now sends `save_source`; GA4 dimension **Save Source** registered; dataLayer key `save_source` (GTM Version 9, then 10) | Live. Legacy `source` key removed on branch `chore/remove-legacy-source-key` (`6fc529806`): merge and deploy pending |
| 2 | Zero `brand_clickout` / `brand_page_view` in 28 days | Not a broken tag. The brand-page outbound link was removed 2026-07-26 (`f321e749e`); in-stock PDP Add to Cart replaced the Shop button 2026-08-12. Only out-of-stock PDP and `/saved` "Shop on" CTAs remain, and almost no one reaches them. `brand_page_view` shipped 2026-10-02 | Diagnosis only (see below) | Open product question |
| 3 | `view_search_results` fired on every page, plus once per filter change | Triggers `Search - initial load` and `Search - in app` used `URL - keywords matches RegEx .+`, which matches a missing value | Both triggers also need `Page URL matches RegEx [?&]keywords=[^&#]+`; `Search - in app` also needs `JS - keywords changed` = yes (uses `gtm.oldUrl` / `gtm.newUrl`) | Live (GTM Version 8). Verified live: search load 1 event with `search_term`, filter 0, `/brands` 0 |

GTM versions: 8 = search fix, 9 = `save_source`, 10 = `DLV - save_source` reads dataLayer key `save_source`. Rollback = publish the previous version in GTM → Versions.

## `brand_clickout` from `/saved` (decision recorded)

The clickout step is the `/saved` "Shop on {brand}" CTA (`saved_surface` = `saved_item_card` or `saved_brand_group`). Verified live 2026-10-04: save a listing → `/saved` → Shop → trust sheet → Continue fires `brand_clickout` with brand, product ID, session ID, destination and `saved_surface` set. It does not fire before Continue.

28-day GA4 data: 3 `saved_listing_toggle` events from 1 user, 2 `saved_page_view`. The funnel is intact; there is almost no volume at the top. Hypotheses (untested): the PDP offers only Add to Cart (four steps to leave: save, find `/saved`, Shop, Continue); the "View Saved" confirmation auto-dismisses; part of the traffic may be bot or crawler (about 290 of 318 users sent a search event). Also seen: a "NO IMAGE" placeholder on the first `/saved` item (cause unknown).

## Other state

- GA4 Internal Traffic filter: **Active** (was Testing). Data before 2026-10-04 includes team visits (about 50 of 92 weekly users were New York). Verify own tests in DebugView, not Realtime.
- `JS - entry_source` deleted from the GTM workspace. Workspace 8 has no pending changes.
- Looker: data source refreshed (475 fields), calculated field `Save Source (combined)` created (`CASE WHEN Save Source != "(not set)" THEN Save Source ELSE Save Toggle Source END`).
- `gtm.js` is cached by browsers for 15 minutes; re-test after a fresh fetch.
- Page title on `listing_view` is stale (SPA); identify listings by `product_id`.
- Tag fires on the legacy `gtm.historyChange` event only (one fire per change); this depends on that event name.

## Open items (in priority order)

1. Merge and deploy `chore/remove-legacy-source-key` (web-client). Then confirm in DebugView that `saved_listing_toggle` has `save_source` and no `source`.
2. In 24-48 hours, re-check GA4: `view_search_results` roughly equals real searches and has `search_term`; no new `heart_icon` / `add_to_cart_button` source rows.
3. Looker tiles still to build: Add to Cart scorecard (`saved_listing_toggle`, `Is Saved` = true, combined field = `add_to_cart_button`); retitle the funnel table "Event counts (not the same sessions)"; text note that search counts before 2026-10-04 are inflated; set the search tile's range to start 2026-10-04; top viewed products (Product ID, not page title) and brands.
4. GA4 chores: two annotations (internal filter Active; GTM v8/v9 fixes), consider the Developer traffic filter, add `tagassistant.google.com` as a referral exclusion.
5. Check for duplicate `page_view` per in-app navigation (2 requests seen in one automated test; unconfirmed). In GTM Preview, see whether two page_view hits fire on one history change.
6. Product decision: what OCTR should measure, given the clickout step is `/saved` and volume is near zero. Measure real saves per session for 1-2 weeks first.
7. Open the Cross-Shop Looker dashboard to see why it reports clickouts (property and date range not checked).
8. Optional: add `listing_title` to `listing_view` (code plus GTM plus a GA4 dimension) for readable product names.
9. Commit `social/metrics-log.md` (the attribution cutover note), still uncommitted.

## Not verified

- GA4 receipt of the Version 8/9/10 changes beyond a DebugView check from a clean profile.
- Why GA4 shows 714 `view_search_results` against 732 `page_view` (explained by the search bug, not independently reproduced for the initial-load trigger).
- The meaning of `tt=internal` in collect requests (the Internal Traffic filter showed only New York / Chrome hits in Testing).
