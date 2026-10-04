# UTM Attribution Restoration PRD

## Document Information
- **Created**: 2026-10-03
- **Status**: ✅ P0 shipped and live 2026-10-03 (web-client `29770e2b6`). Verified live on a clean tab: first GA4 request carries `utm_*` in `dl=`; canonical and `og:url` clean. **Still open**: 24 to 48 hour check that a QA campaign appears under Session campaign, GA4 annotation, referral exclusions (`tagassistant.google.com`). **Done 2026-10-04:** Internal Traffic filter set to Active (verified in Testing first: labeled hits were New York / Chrome only; data before this date includes team visits), unused `JS - entry_source` deleted from the GTM workspace. `stripUtmParams` was deleted (answer to Open Question 1). Not yet checked live: SPA route-change `dl=`, and a Google-search reload sending no campaign.
- **Owner**: Product / Dev
- **Related docs**:
  - `product/prds/insights/crossshop-tracking-prd.md` (introduced `entry_source`; §12 ties UTMs to the social schema)
  - `product/prds/insights/basic-dashboards-prd.md` (the dashboard this unblocks; its Journey Map and source tiles depend on correct attribution)
  - `product/prds/gifting-festival-traffic-prd.md` (Day 2 shipped `stripUtmParams()`; line ~175)
  - `mela-docs/technical/analytics/crossshop-tracking.md` (event schema source of truth)
  - `mela-docs/social/category-routing.yaml`, `mela-docs/social/metrics-log.md` (the UTM schema and the "GA4 sessions (UTM)" column)

---

## Executive Summary

**Problem**: The app removes `utm_*` from the URL before GA4 reads it, so GA4's own source / medium / campaign attribution never sees Mela's tagged social links. UTM-tagged visits from sources with no referrer (common in in-app browsers) are recorded as "direct", and `utm_campaign` and `utm_content` (for example `banjaaranstudio_w1`) never reach GA4.

**Proposed fix**: Stop stripping UTMs on the client, and fix the canonical URL at its source so tracking parameters never appear in `<link rel="canonical">` or `og:url`. Let GA4's native attribution do the work.

**Target Users**: Internal (Founder/PM, social lead). No shopper-facing change except that a tagged landing URL keeps its UTMs in the address bar until the first in-app navigation.

**Business Objective**: Make per-platform and per-campaign acquisition reportable in GA4 and Looker Studio with no custom plumbing, so the "GA4 sessions (UTM)" column in `metrics-log.md` can finally be filled from real data.

**Primary Success Metrics** (baseline-only for 30 days):
- The first GA4 request on a UTM-tagged landing carries the UTMs in `dl=`: **confirmed on a clean device**.
- Tagged campaigns appear under Session campaign in GA4: **confirmed after 24 to 48 hours**.
- Canonical and `og:url` contain no tracking params in both server-rendered and client-rendered HTML: **confirmed by test**.

---

## 1. Problem Statement

### Current State (evidence)
- `src/index.js:133-136` runs `captureEntrySource()` and then `stripUtmParams()` synchronously, **before** the app renders and before GTM sends its first hit.
- **Live test, 2026-10-03** (clean tab, no referrer, URL `.../l/6a12840a-...?utm_source=pinterest&utm_medium=social&utm_campaign=banjaaranstudio_w1&utm_content=ikat_mules_coal`): the first GA4 collect request (`en=page_view`, `_ss=1`, about 1.7 s after load) had `dl=` **without any `utm_*`** and no `dr=` referrer. Native GA4 would attribute that session as direct.
- The custom `entry_source` (sessionStorage) is captured before the strip, so it works. But it only rides on `brand_clickout` events, and it keeps only `utm_source` (campaign survives only for paid mediums, none exist; `utm_content` is never kept).

### Why the strip exists
Commit `413beb6ee` (2026-08-25, gifting traffic work) added it to (1) keep campaign-tagged URLs out of shareable links and (2) keep UTMs out of the canonical URL. It was added with `entry_source` in mind; nobody checked that GA4 reads `page_location` later.

### The second reason does not hold (architect's code reading, to be confirmed by test)
- `canonicalRoutePath` appends the full query string unless `pathOnly` is set (`src/util/routes.js` ~154-157), and `pathOnly` is set only when a page passes a `referrer` prop (two pages). Most pages put the whole query string into the canonical (`Page.js` ~148, 200, 280) unless the caller overrides `canonicalURL` (Category, Gifting, Profile).
- The server renders `req.url` including the query, so **the server-rendered canonical and `og:url` already contain `utm_*`**. The client strip only cleans what the client rewrites after hydration. Crawlers and link-preview scrapers read the server HTML.
- Side effect of the strip: server and client see different URLs (SSR/CSR parity gap).

### Business Impact of Inaction
Per-campaign reporting (the point of UTM-tagging every post, `gifting-festival-traffic-prd.md`) is impossible, the Basics dashboard's source tiles and Journey Map breakdown are unreliable, and the Sunday metrics ritual keeps running on Blotato click counts.

---

## 2. Goals & Non-Goals

### Goals
- GA4 receives `utm_*` on the first hit, so native Session / First-user source, medium and campaign are correct.
- Canonical and `og:url` never contain tracking params, on server and client.
- One system of record for acquisition (native GA4); no second campaign taxonomy.
- Changes are small, covered by unit and server-render tests, and reversible in one revert.

### Non-Goals (explicitly not built now)
- Delaying the strip until after the first `page_view` (couples app correctness to GTM load speed; breaks silently on slow mobile or blocked GTM).
- Overriding `page_location` or sending `campaign_*` parameters from GTM (re-implements native behavior outside code review).
- Adding `entry_source` to every event (deferred to Phase 3, only if a need remains).
- Server-side or edge capture of UTMs.
- BigQuery export, paid-campaign conventions (`utm_medium=paid_social`), anything requiring more than about 1,500 sessions per 28 days to be meaningful.
- Treating campaign-level comparisons as significant: at about 350 sessions per 28 days, a 30-session campaign yields a handful of clickouts. Use attribution as "did the link work and get clicks", pooled by platform.

---

## 3. User Stories

| As a... | I want to... | So that... | Priority |
|---|---|---|---|
| Social lead | See sessions per platform and campaign (e.g. `banjaaranstudio_w1`) in GA4 | I can fill the "GA4 sessions (UTM)" column and tell whether a post's link worked | P0 |
| Founder/PM | Trust Session source / medium in the Basics dashboard | Source tiles and the Journey Map reflect reality | P0 |
| Dev | Keep canonical and `og:url` free of tracking params | Crawlers and link previews see clean URLs, and server and client agree | P0 |
| Founder/PM | Keep `entry_source` for cross-shop joins | Existing `brand_clickout` analysis keeps working | P1 |

---

## 4. Feature Requirements

### Must Have (P0), one PR in `web-client`
- Remove the `stripUtmParams()` call from `src/index.js`. Keep `captureEntrySource()` before render, unchanged. Update the stale comment in `entrySource.js` and the `GiftingPage.js` comment that references the strip.
- In `canonicalRoutePath` (`src/util/routes.js`), drop tracking params (`utm_*`, `fbclid`, `gclid`, `igshid`, `ttclid`) from the search string and keep all other params. **Do not** switch to path-only: that would change canonical behavior for search and filter pages.
- Tests:
  - Unit: `canonicalRoutePath` for listing and non-listing routes, with and without UTMs and other params.
  - Server-render: a request to `/l/slug/id?utm_source=x&foo=1` yields a canonical and `og:url` without `utm_*` (extend the renderer tests or add an app render test).
  - Redirect: `/l/:id?utm_…` keeps the UTMs through the canonical-slug redirect on the client.
- Decide whether to keep or delete `stripUtmParams` and its tests (it becomes unused).

### Should Have (P1)
- Looker Studio "Basics" page: one table of Session source / medium / campaign × Sessions (and clickouts), pooled per platform, in place of the PRD's Entry Source × Sessions tile.
- Journey Map: switch the breakdown from the custom Entry Source to native Session source.
- Annotate the go-live date in GA4, and add a line to `metrics-log.md`.

### Nice to Have (P2 / Phase 3, only if a need remains)
- Add `entry_source` as a shared event parameter on the Google tag (Custom JavaScript variable reading `sessionStorage['mela_entry_source']`) for cross-shop joins. Label it tab-scoped, not "session source". Note the GA expert's warning: never feed campaign values from sessionStorage, because a later full page load in the same tab would replay an old campaign.
- Normalize `utm_source=chatgpt.com` to `ai_search` in `normalizeEntrySource` so UTM and referrer paths agree.

---

## 5. Acceptance Criteria

**Code**
- [ ] `stripUtmParams()` is no longer called on load; UTMs are present in the address bar on a tagged landing.
- [ ] `canonicalRoutePath` removes tracking params and preserves other params; unit tests pass.
- [ ] Server-rendered HTML for a UTM URL has a canonical and `og:url` with no `utm_*`; test passes.
- [ ] The slug redirect still preserves the query string; test passes.
- [ ] Full web-client suite passes.

**Live verification (clean device or phone; the owner browser's GA4 hits return 503, but the request URLs are still readable)**
- [ ] First `collect` request (`en=page_view`, `_ss=1`) has `dl=` with the UTMs.
- [ ] Later in-app `page_view`s have `dl=` for the real path; route changes work.
- [ ] A reload after arriving via Google search in the same tab sends no campaign.
- [ ] After 24 to 48 hours, `banjaaranstudio_w1` (or a QA campaign) appears under Session campaign in GA4 Traffic acquisition and in Looker.
- [ ] `<link rel="canonical">` on the live page contains no tracking params (view source).

**Reporting**
- [ ] GA4 annotation added for go-live; `metrics-log.md` notes the cutover (earlier data stays "direct").

---

## 6. Success Metrics & Measurement

| Metric | Definition | Source |
|---|---|---|
| UTM landing capture | First `collect` hit carries `utm_*` on tagged landings | Network inspection on a clean device |
| Campaign visibility | Named campaigns present under Session campaign | GA4 Traffic acquisition / Looker |
| Unattributed share | (Unassigned) or self-referral as % of sessions | GA4; investigate if above 20% |
| Canonical cleanliness | Tracking params in canonical or `og:url` | Unit + server-render tests |

All baseline-only for 30 days.

---

## 7. Dependencies & Risks

- **Not retroactive**: past UTM visits stay "direct". Annotate the cutover and avoid comparing across it.
- **Shared landing URLs keep their UTMs**: a copied landing URL will self-attribute. Judged negligible at about 80 users per week, and arguably correct.
- **Crawlers**: they already see UTMs in the server HTML today. The canonical fix addresses this; verify with a server-render test and a live view-source check.
- **GTM-only page_view path**: `src/analytics/handlers.js` needs `window.gtag`, which the GTM-only setup does not define. A route-change `page_view` was observed leaving the browser on 2026-10-02 (via GTM), but the code path is **unverified**. Check in GTM Preview.
- **Unwanted referrals / internal traffic**: add `tagassistant.google.com` and any auth or checkout domains to GA4's referral exclusions, and set the internal-traffic filter to Active (it ships in Testing).
- **Unverified (from the expert panel, not Google docs)**: how GA4 handles a campaign change mid-session; exact `campaign_*` wire parameter names (not needed under this plan); whether link scrapers use `og:url`.
- **Panel disagreement, recorded**: the GA4 expert recommended keeping the strip and sending `campaign_*` via GTM from a page-load-only variable. They did not evaluate simply dropping the strip. Their cited facts (GA4 derives all source values from UTMs when any are present) support this PRD's approach. That route remains the documented fallback if an SEO audit or a business need requires clean landing URLs.
- **When to rethink**: GA4 still shows UTM visits as direct after the change (check GTM or consent, not the app), unassigned or self-referral above 20%, or a paid campaign launches (then add `utm_campaign` handling to `entry_source`).

---

## 8. Open Questions

1. Keep or delete `stripUtmParams` and its tests once unused?
2. Which tracking params beyond the five listed should the canonical drop?
3. Do we want the `ai_search` normalization (P2) now or with the paid-campaign work?

---

## 9. Sequencing and Handoff (proposal, nothing started)

| # | Step | Notes |
|---|---|---|
| 1 | Implement the P0 PR on a new `web-client` branch with tests | Do not deploy or merge without review |
| 2 | Deploy, then verify on a clean device (Section 5, live verification) | GTM Preview to confirm route-change `page_view` |
| 3 | GA4: annotation, referral exclusions, internal-traffic filter to Active | Manual Console steps |
| 4 | Looker "Basics": Session source / medium / campaign table; Journey Map breakdown to native source | After 24 to 48 hours of data |
| 5 | Update `crossshop-tracking.md` (strip removed; canonical rule) and the `basic-dashboards-prd.md` tile corrections | Doc follow-ups |

**Cleanup from this session (not done):** the GTM workspace has an unsaved Google tag edit (discard) and a saved, unpublished `JS - entry_source` Custom JavaScript variable (keep for Phase 3 or delete). The `Journey Map` GA4 exploration exists with a custom Entry Source breakdown that is mostly "(not set)".
