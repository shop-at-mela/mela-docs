# Shopper Visibility & Reporting PRD

## Document Information
- **Created**: 2026-08-04
- **Status**: 🟡 In progress — Phase 1 (site search tracking) ✅ shipped and live-verified 2026-08-04; Phase 2 (potential shopper funnel) in progress; Phases 3 and 4 not started.
- **Owner**: Product / Founder
- **Related docs**:
  - `product/prds/insights/crossshop-tracking-prd.md` (the instrumentation this PRD reports on; §13 there is superseded by Phase 3 here)
  - `mela-docs/technical/analytics/crossshop-tracking.md` (source of truth for event schema and GA4 setup)
  - `mela-docs/social/category-routing.yaml` (UTM schema feeding `entry_source`)
  - `mela-docs/social/metrics-log.md` (the "GA4 sessions (UTM)" column this PRD finally makes fillable)
  - `product/prds/storefront-validation-readiness-prd.md` (OCTR is that PRD's primary metric; Phase 2 here is how it gets measured)

---

## Executive Summary

**Feature**: A reporting layer on top of the already-shipped `brand_clickout` instrumentation that answers a question the current setup cannot: **how many potential shoppers visit shopatmela.com, and how far down the funnel do they get?**

**Target URL / Entry Point**: Internal. GA4 (Explorations + Library collection) and Looker Studio. One code-adjacent change, a GTM container tag, no web-client code.

**Target Users**: Internal (Founder/PM, social lead). No end-user-facing behavior changes.

**Business Objective**: Replace "sessions" as the working traffic number with a qualified **potential shopper** count, and make OCTR readable on demand rather than reconstructible once a month. Without this, `metrics-log.md` and the Sunday ritual in `cold-start-checklist.md` continue running on Blotato click counts alone.

**Primary Success Metrics**:
- Potential shopper rate (sessions reaching a listing or brand page ÷ all sessions): **baseline**, target TBD after 30 days
- OCTR (sessions with `brand_clickout` ÷ all sessions): **baseline required before any P1 storefront work ships**, per `storefront-validation-readiness-prd.md` §8
- Time to answer "what are people searching for": from **impossible** to **one saved report**

---

## 1. Problem Statement

### Current State

GTM, GA4, and Clarity have been live since 2026-07-19, and `brand_clickout` carries seven params including `mela_session_id`. The raw material is there. What is missing is any assembled view of it.

Three concrete gaps as of 2026-08-03:

1. **"Visitors" is the only available number, and it is the wrong one.** GA4's native Sessions metric counts bots, single page bounces, and accidental hits identically to a shopper who browsed four listings. Nobody can currently say how many visitors were plausibly shopping.
2. **Site search was invisible.** Mela's search writes a `keywords` query parameter (`SearchPage.shared.js:121`). GA4's Enhanced measurement site search only looks for `q, s, search, query, keyword`, so the plural form was never detected and no `view_search_results` event ever existed. Confirmed live on 2026-08-04: the search results `page_view` reached GA4 carrying the full URL, and no search event was generated alongside it.
3. **The two cross-shop hypothesis reports from `crossshop-tracking-prd.md` §13.1 were specced but never built**, and the documented click path for one of them turns out not to be buildable as written (see §8 Risks).

### User Pain Points

N/A for end users. The internal pain is that every weekly metrics review is currently an argument about whether a traffic number means anything.

### Business Impact of Inaction

`storefront-validation-readiness-prd.md` §8 flags a sequencing risk: the OCTR baseline must be captured **before** any P1 storefront work ships, otherwise post-P1 changes cannot be distinguished from noise. Every week without a standing OCTR report is a week that window narrows. Separately, the "Clicks to Mela" north-star in `cold-start-checklist.md` Week 3 stays proxied through Blotato rather than measured directly.

---

## 2. Goals & Non-Goals

### Goals

- Define "potential shopper" as a reproducible funnel stage, not a vibe.
- Capture site search terms as a first-class GA4 event.
- Produce four saved, named reports that answer the standing questions without being rebuilt each time.
- Make the reports shareable with someone who does not have GA4 access.

### Non-Goals

- No new web-client code. Every item here is GA4 or GTM configuration. If something turns out to need app code, it moves to its own PRD rather than expanding this one.
- No new user-facing UI, copy, or behavior.
- No targets. Everything is baseline-only for 30 days, consistent with `search-page-optimization-prd.md` precedent.
- Server-side tagging, consent mode, and affiliate postback stay deferred per `crossshop-tracking.md` §8.
- Fixing the ad-blocker undercount (see §8). Measured, acknowledged, not solved here.

---

## 3. User Stories

| As a... | I want to... | So that... | Priority |
|---------|-------------|------------|----------|
| Founder/PM | See how many sessions reached a product or brand page, not just landed | I have a traffic number that means something | P0 |
| Founder/PM | Read OCTR on demand | I can capture the pre-P1 baseline before the window closes | P0 |
| Founder/PM | See what shoppers search for | I learn demand signal the catalog does not yet cover | P0 |
| Founder/PM | Compare funnel completion by `entry_source` | I know which channels send qualified traffic vs. bounces | P1 |
| Social lead | Fill the "GA4 sessions (UTM)" column in `metrics-log.md` | The Sunday ritual stops running on Blotato clicks alone | P1 |
| Founder/PM | Share a view-only dashboard link | I can show traction without granting GA4 access | P2 |

---

## 4. Feature Requirements

### Must Have (P0)

**Phase 1 — Site search tracking** ✅ shipped 2026-08-04
- GTM variable `URL - keywords` (URL type, Component Type Query, Query Key `keywords`).
- GTM triggers `Search - initial load` (Page View) and `Search - in app` (History Change), both conditioned on `URL - keywords` matches RegEx `.+`.
- GTM tag `GA4 - view_search_results` (GA4 Event, `G-1H78QV7C6G`, event name `view_search_results`, parameter `search_term` = `{{URL - keywords}}`), attached to both triggers.
- Enhanced measurement **Site search** turned off so the two mechanisms cannot double count.

**Phase 2 — Potential shopper funnel**
- A saved GA4 Funnel exploration named `Potential Shoppers Funnel`, open funnel, with steps: `session_start` → `page_view` on a listing or brand page → `view_search_results` or category browse (optional step) → `brand_clickout`.
- Step 2 condition uses the **native** `Page path and screen class` dimension with regex `^/l/[^/]+/[^/]+$|^/brands/[^/]+$`, deliberately excluding `/checkout`, `/make-offer`, and `/request-quote`.
- `Entry Source` applied as the breakdown dimension.
- Elapsed time enabled between steps.

**Phase 3 — Cross-shop explorations** (supersedes `crossshop-tracking-prd.md` §13.1)
- `Cross-Shop: Multi-Brand Clickout Rate` Free Form exploration, rows `Mela Session ID` with `Brand Name` nested, filtered to `brand_clickout`, Show rows raised to 500.
- The multi-brand rate computed by CSV/Sheets export, **not** by an in-GA4 segment (see §8).
- `Cross-Shop: Entry vs Exit` Free Form exploration per `crossshop-tracking-prd.md` §13.1 Step 2, which is buildable as written.
- All explorations plus the Phase 2 funnel pinned into a GA4 **Library** collection named `Cross-Shop Tracking`.

### Should Have (P1)

**Phase 4 — Looker Studio dashboard**
- Report `Mela Cross-Shop Dashboard` on the standard GA4 connector, with the tiles from `crossshop-tracking.md` §13.2 plus three new ones: potential shoppers scorecard, OCTR scorecard, top search terms table.
- View-only sharing enabled.

### Nice to Have (P2)

- BigQuery export enabled on the GA4 property, which removes the Sheets step in Phase 3 and is the only correct way to put the multi-brand rate into Looker Studio. Free at current volume.

---

## 5. UX Requirements

None. No user-facing surface. The only observable change from Phase 1 is an additional analytics event on search, which is invisible to shoppers.

---

## 6. Acceptance Criteria

**Phase 1**
- [x] `URL - keywords` resolves to the typed search term on both a direct `/s?keywords=...` landing and an in-app search. — ✅ 2026-08-04
- [x] `GA4 - view_search_results` fires exactly once per search, from both triggers, with no double count. — ✅ 2026-08-04
- [x] `view_search_results` reaches GA4 with a populated `search_term`. — ✅ 2026-08-04, verified after rebuilding all four GTM objects (see §8).
- [ ] Enhanced measurement Site search is turned **off**, and Page views plus its "browser history events" sub setting are left **on**.

**Phase 2**
- [ ] `Potential Shoppers Funnel` is saved and returns non-zero data at every step.
- [ ] Step 2 uses `Page path and screen class`, not a custom definition on the raw `page_path` parameter (which is never sent and would be permanently blank).
- [ ] Step 1 → step 2 completion rate is recorded as the potential shopper baseline, with date range noted.
- [ ] Step 1 → step 4 completion rate is recorded as the **OCTR baseline**, timestamped, before any P1 storefront work ships.

**Phase 3**
- [ ] Both explorations saved under their exact names.
- [ ] Multi-brand rate computed once end to end via export, with the method written down.
- [ ] `Cross-Shop Tracking` Library collection published and visible in the GA4 left nav.

**Phase 4**
- [ ] Dashboard renders all tiles with real data.
- [ ] View-only link tested in a logged-out browser.
- [ ] No session-scoped distinct-count metric attempted on the standard connector.

---

## 7. Success Metrics & Measurement

| Metric | Definition | Where it lives |
|---|---|---|
| Potential shopper rate | Sessions reaching `/l/:slug/:id` or `/brands/:brandSlug` ÷ all sessions | Phase 2 funnel, step 1 → 2 |
| OCTR | Sessions with `brand_clickout` ÷ all sessions | Phase 2 funnel, step 1 → 4 |
| Search demand | Top `search_term` values by event count | Phase 4 tile, or GA4 standard report |
| Multi-brand clickout rate | Sessions with 2+ distinct `brand_name` ÷ sessions with any clickout | Phase 3, via export |
| Entry ≠ exit rate | Per `crossshop-tracking.md` §5b | Phase 3 exploration |

All baseline-only for 30 days. The OCTR baseline is the one with a hard deadline attached.

---

## 8. Dependencies & Risks

- **Correction to `crossshop-tracking-prd.md` §13.1 and `crossshop-tracking.md` §5a**: both instruct building a GA4 segment on "Brand Name count distinct ≥ 2". GA4's segment builder offers condition matching and sequences but **no distinct-count aggregation over a dimension**, and the Explore metric picker has no count-distinct metric. The documented click path is not buildable. Phase 3 uses CSV export instead; BigQuery is the durable fix. Both source docs need this correction.

- **Every GA4 collect hit from the owner's primary browser returns HTTP 503** while Clarity returns 204 and all other hosts return 200, observed consistently on 2026-08-03 and 2026-08-04. Cause is most likely a DNS-level blocker or privacy extension on that machine. **Consequence**: absence of an event in DebugView from that browser is not evidence of a broken tag. All verification must happen from a clean profile or a phone. This invalidates nothing already verified, but it made Phase 1 debugging materially slower and should be resolved before Phase 2 verification.

- **GTM preview proved unreliable during Phase 1.** The tag was absent from Tag Assistant across multiple restarts despite existing in the workspace with triggers attached; deleting and recreating all four objects resolved it with no configuration difference identified. If Phase 2 or 3 hits a similar wall, rebuild before spending more time diagnosing.

- **SPA page views arrive with roughly a 6 second delay** (measured: `tfd=33387` for the search page view vs. `tfd=5374` for the initial one). Any live verification must wait ~10 seconds before concluding an event did not fire.

- **Page titles are stale on SPA navigation.** The `page_view` fires before React updates `document.title`, so GA4 records the *previous* page's title. All reports must group by **Page path**, never Page title. Not fixed here; flagged so no future report silently uses the wrong dimension.

- **Ad-blocker undercount.** GA4 misses blocked traffic entirely, typically 10 to 30 percent. Absolute counts are understated; ratios like OCTR hold up better since numerator and denominator are affected together. Server-side tagging remains the deferred fix.

- **Google Signals must stay off.** Enabling it to clear the `non_personalized_ads=1` user property would activate GA4 identity thresholding, which withholds low-volume report rows. At current traffic that would blank out the exact rows this PRD exists to read.

---

## 9. Out of Scope / Future Considerations

Two production bugs were surfaced while debugging Phase 1. Both are real, neither belongs in this PRD, and both should be tracked separately:

1. **CSP is not enabled in production.** `REACT_APP_CSP` is unset, so `server/csp.js` never runs and Mela serves with no Content Security Policy. The `clarity.ms` allowlist work recorded as done in `crossshop-tracking-prd.md` §8 is correct in code but inert in production. Security item, not analytics.
2. **www/apex mismatch.** `REACT_APP_MARKETPLACE_ROOT_URL` is set to `https://shopatmela.com` while the site serves from `https://www.shopatmela.com`, so the PWA manifest fetch fails CORS (`Page.js:34`). Verified that the apex → www redirect **does** preserve query strings, so UTM attribution is unaffected.

Also deferred: BigQuery export beyond the P2 note, server-side tagging, consent mode, and a paid-campaign `entry_source` convention (`utm_medium=paid_social`), which stays unconfirmed until a first paid test exists.

---

## 10. Suggested Sequencing

Ordered by dependency and by which findings invalidate later work if skipped.

| # | Phase | Effort | Blocking? |
|---|---|---|---|
| 0 | Resolve the 503 on the owner's browser, or designate a clean verification profile | 15 min | **Yes.** Until this is done, every "the event did not fire" observation is untrustworthy, and Phase 1 already lost hours to it. |
| 1 | Site search tracking | ✅ done | Was blocking the funnel's optional step 3 |
| 1b | Turn Enhanced measurement Site search off; confirm Page views history sub setting stays on | 5 min | Yes for data integrity. Double counting starts the moment the setting propagates. |
| 2 | Potential shopper funnel, and **record the OCTR baseline with a timestamp** | ~30 min | **Yes, and time-sensitive.** `storefront-validation-readiness-prd.md` §8 requires this before P1 storefront work ships. |
| 3 | Cross-shop explorations + Library collection | ~1 hr | No |
| 3b | BigQuery export | ~15 min setup, 24 hr to first data | No, but do it before Phase 4 if the multi-brand rate is wanted on the dashboard |
| 4 | Looker Studio dashboard | ~45 min | No |

Phase 0 and Phase 2 are the only two with real urgency. Phase 0 because it silently corrupts every subsequent debugging session, and Phase 2 because its baseline has an external deadline attached to it. Phases 3 and 4 are durable convenience work and can wait for a quiet week.
