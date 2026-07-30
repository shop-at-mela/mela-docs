# Mela Dev TODO

Running log of shipped work and next actions. Newest entry at top.

---

## 2026-07-29

### Shipped
- `fix(seo)` — **P0**: category-mismatched product metadata, confirmed via external AEO/Gemini audit (`mela-docs/engineering/done/seo-optimization-summary.md` → Phase 2). `ListingPageCoverPhoto.js` and `ListingPageCarousel.js` hardcoded `"Authentic Indian Baby Products"` into every listing's title tag, meta description, and JSON-LD seller/audience fields — regardless of the listing's actual category. A House of Chikankari kaftan or a Kaunteya mug shipped with baby-product metadata, which reads as miscategorized/low-quality data to semantic-search crawlers (Gemini) and undercuts Mela's multi-category positioning. Fixed by deriving `categoryDisplayName` from `config.categoryConfiguration.categories` via the existing `findCategoryById` helper already used for category chips in both files — no new data model, just wiring in what already existed. Also generalized the JSON-LD `audience` block (`audienceType: 'Parents'` → `'Shoppers'`) since it was baby-specific across all categories. 50/50 ListingPage test suites still passing (no test had covered the old string — that's how it shipped unnoticed).
- Confirmed, not fixed: `SearchPage.shared.js`'s `isCategoryPage`/`isBrandPage` branches in `createSearchResultSchema` (lines ~534-571) contain the same hardcoded "Baby Products"/"Baby Brand" strings, but tracing `routeConfiguration.js` shows `/categories/*` routes to `CategoryPage` and `/brands/:brandSlug` routes to `ProfilePage` — SearchPage is never reached at those paths anymore. This is dead code left over from before the dedicated components shipped, not a live bug. Left untouched (removal is a separate cleanup decision); noted below.

### Next
- [ ] **Critical** — Google Merchant Center product feed: no Content API / Shopping feed integration exists at all (confirmed — only a stray JSON-LD comment referencing "Google Shopping" on the price field). Net-new engineering scope: map existing `publicData` fields (`brand`, `material`, `itemAspects`, `sku`) into a Merchant Center feed with explicit `"Ships to US"` shipping attributes. Worth its own PRD rather than a quick add. See `seo-optimization-summary.md` Phase 2 §2.
- [ ] **Critical** — `aggregateRating`/`review` is completely absent from the Product JSON-LD (`ListingPageCoverPhoto.js` schema object has no rating/review keys). Already flagged as P2 in `seo-aeo-category-brand-pages-prd.md` §5B, but blocked on a real precondition: Mela has no review/rating data model yet. Needs a product decision — build reviews before AEO can use them, or defer AEO rating schema indefinitely.
- [ ] Housekeeping (not urgent): remove the dead `isCategoryPage`/`isBrandPage` branches in `SearchPage.shared.js` `createSearchResultSchema` (~lines 534-571) — unreachable now that `CategoryPage`/`ProfilePage` own those routes, but left in place and could confuse a future editor into "fixing" schema that never runs.
- [ ] Digital PR (co-mentions) and the informational content hub are tracked as content workstreams, not engineering, in `mela-docs/social/aeo-next-steps.md`.

---

## 2026-07-26

### Shipped
- `fix(brand-hero-card)` — hero carousel was silently broken (P0): a dropped `included` image entity in `fetchHeroBrands` left a dangling relationship, `getHeroBrands` threw on every render, and with no error boundary around `HeroSection`, React silently stopped re-rendering it — loading skeleton frozen forever, no console error, store updating fine underneath. Fixed by capturing `included` per-brand, matching `fetchBrands`/`fetchFeaturedBrands`.
- `fix(brand-hero-card)` — hero eligibility no longer requires products (the card renders none) and now covers all curated brands, not just the first 10; new `fetchHeroBrands`/`getHeroBrands` kept separate from `fetchFeaturedBrands` (`FeaturedBrandPartners` unaffected)
- `fix(brand-hero-card)` — focus ring now uses `--colorAccent` (real marigold token); `--marketplaceColorLight` was already a different color elsewhere, silently defeating the intended fallback
- Verified live against dev Sharetribe across multiple hard reloads, not just unit tests. Full suite: 134/134 test suites passing
- `feat(brand-storefront)` — P1.1 brand page hero band (`storefront-validation-readiness-prd.md`): banner image with gradient fallback, "Vetted by Mela" pill gated on `publicData.melaVetted`, inline story summary + craft chip, outbound "Visit Store" CTA wired through the existing `RedirectTrustSheet`/`openBrandStorefront` flow. Also excludes $0 promo SKUs and sorts bestsellers first in the brand-page grid; "About" tab renamed "About & Story". All new fields degrade gracefully for the 14 brands without seeded hero data — verified live on `/brands/fizzy-goblet` (sparse real data) plus 26 passing tests.
- `fix(trust-debris)` + `feat(homepage)` + `feat(category-page)` — remaining P0/P1.2/P1.3 of `storefront-validation-readiness-prd.md` (8 commits): positioning copy applied everywhere per `positioning-copy.md`; P0.2 debris sweep ($0 SKUs, certifications role-gating, search placeholder — footer copyright/listing-link left alone, that's Sharetribe Console content, not fixable from web-client); P0.1 vetting strip (live-verified, both analytics events fire); P1.2 category-page brand-diversity cap + price-heuristic demotion + interleaved brand tiles (`categoryMerchandising.js`, `CategoryPage.duck.js` extension); P1.3 three new homepage editorial modules (Brand Spotlight, New from India, Craft Stories) + full section reorder, all live-verified against seeded dev data. Caught and fixed a real bug: `NamedLink` silently drops `onClick`, so two modules' click analytics needed a `display:contents` wrapper fix. Full suite: 140/140 test suites, 2264 tests passing.
- Fixed same session: `BrandStorefront.js`'s story-summary derivation was looking for a `publicData.brandStory` field the seeder never populates (it concatenates story into the native `bio` field instead) — summary now derives from `bio` minus the tagline sentence, live-verified showing real content for Fizzy Goblet/Kaunteya.

### Next
- (still open) The Nesavu and Masilo have no hero image source — re-check the curated first-fold order once they get `brandHeroImageIds`/`brandHeroImages`
- [ ] Brand-storefront hero band was only visually verified at desktop viewport this session — a browser-automation tool limitation prevented forcing a true 390px mobile viewport (`resize_window` didn't change `window.innerWidth`). Mobile-first CSS was hand-reviewed against the mockup but not screenshot-verified; do a real on-device or working resize-tool pass before calling P1.1's mobile AC done.
- [ ] P1.1a's "outbound store link above the grid" AC is superseded — hero-band CTA relocated to a plain "Brand website" link in the About & Story tab per the inline 2026-07-26 decision (no-affiliate-tracking rationale: an above-the-fold exit door with no tracking is a pure loss). PRD §6 AC text has been updated to match (see the REWORK note under P1), but flagging here too since it reverses what P1.1a's mockups show.
- [ ] Homepage length reduction measured at 15.4% (8,526px vs. 10,073px baseline), short of the PRD's ≥25% target — the 3 new P1.3 modules are heavier than the spec's projection assumed. Options: trim module density further, or accept 15.4% + the much-earlier vetting-strip placement as sufficient and revisit the number later.
- [ ] `/categories/Fashion`'s first page is 100% one brand (House of Chikankari) — P1.2's diversity-cap code is correct and tested, but has nothing to diversify against on this specific page. Supply-side gap (more Fashion brands with inventory), not a UI fix — matches the PRD's own §8 risk note.
- [ ] No AC above has been verified at a true 390px mobile viewport — same browser-automation tooling limitation as the P1.1 pass (`resize_window` doesn't change `window.innerWidth` in this session's environment).

---

## 2026-07-25

### Shipped
- `feat(hero-section)` — BrandHeroCard ships (`brand-hero-card-webclient-prd.md`, ✅ Shipped): image-forward hero card (1:1 photo, bottom gradient scrim, white name/tagline) replaces `BrandCardHome` in the homepage hero only; `BrandCardHome` itself untouched. Resolves `brandHeroImageIds[i]` → Sharetribe variant URL, falls back to `brandHeroImages[i]` (Shopify); brands with no hero source are filtered out (no dead dots). Mobile carousel is now a scroll-snap track (88% width + peek) instead of a single-slide swap.
- Caught and fixed a WCAG AA gap during dev-lead review: scrim/text only held 4.5:1 for the average case — a 2-line-wrapped name/tagline over a near-white photo measured 4.22–4.28:1. Widened the scrim and switched overlay text to solid white (verified 4.97:1 at the worst-case point).
- Fixed a test-pollution bug in `BrandHeroCard.test.js`: a failed assertion skipped `jest.spyOn` cleanup, corrupting later tests — root cause was a fresh `configureStore()` per `rerender()` instead of RTL's `wrapper` option.

### Next
- [ ] The Nesavu and Masilo have no hero image source (brand-wide watermark; no CSV yet, respectively) and are absent from the hero carousel — re-check the curated first-fold order (`configBrands.js`) once they get `brandHeroImageIds`/`brandHeroImages`
- [ ] Full `npm test` run flagged one pre-existing, unrelated failure (`LandingPage.test.js` error-fallback test) — not touched by this work, left as-is

---

## 2026-07-19

### Shipped
- `verify(analytics)` — Cross-shop tracking (`crossshop-tracking-prd.md`) **fully live-verified end-to-end** on shopatmela.com, status now ✅ Shipped: GTM container (`GTM-5JSJ54C2`) published, GA4 (`G-1H78QV7C6G`) receiving data (confirmed in Realtime), Microsoft Clarity (`xoozbmshor`) recording sessions, four GA4 custom dimensions registered. `entry_source` capture confirmed live (first-touch set correctly from UTM params, persisted unchanged across navigation, present on the fired event). `brand_clickout` confirmed firing with all six params on both CTA surfaces reachable in the current catalog (`OrderPanel.js` main CTA, `ProductOrderForm.js` quantity/delivery form CTA — tested at mobile viewport). `InquiryWithoutPaymentForm.js` (inquiry-only CTA) is implemented via the same shared path but has no live listing to test against today — not a gap, just no qualifying data yet.
- Root-caused a red herring along the way: GTM Preview's repeated "no debuggable Google tag" / connection-timeout errors were caused by browser-side tracker-blocking (DuckDuckGo extension in Chrome, native Enhanced Tracking Protection in Firefox) interfering with Google's `/debug/bootstrap` handshake — not a code, CSP, or container problem. Testing in a clean/private browser profile resolved it.
- Noted, unrelated to this work: a 404 seen while testing the mobile CTA traced to an out-of-stock/inventory issue on that specific listing, not a routing or tracking bug — no action needed here.

### Next
- [ ] Confirm the `brand_id` proposal (listing author/brand-user UUID, not a real schema field today) — see PRD §5b
- [ ] If/when an inquiry-type listing goes live, verify `brand_clickout` fires from `InquiryWithoutPaymentForm.js` too
- [ ] Once 30 days of real data exist, build the two Explore reports (multi-brand-clickout rate, entry≠exit) per `crossshop-tracking.md` §5 and set real targets (currently baseline-only)

---

## 2026-07-18

### Shipped
- `feat(analytics)` — Cross-shop / entry-exit attribution tracking (`crossshop-tracking-prd.md`): GTM + GA4 (via GTM) + Microsoft Clarity install (env-var gated), `entrySource.js` (first-touch UTM/referrer capture, session-persisted), `brandClickout.js` (`brand_clickout` dataLayer event + `openBrandStorefront()`), wired into all three Shop-from-Brand CTA surfaces (`OrderPanel`, `ProductOrderForm`, `InquiryWithoutPaymentForm`) via a single `onShopNow` path — also closes a pre-existing gap where two of those surfaces bypassed `RedirectTrustSheet`. Spec at `mela-docs/technical/analytics/crossshop-tracking.md`.

---

## 2026-07-16

### Next
- [ ] Instrument `/brands` brand-order reorder: track rank-position CTR (click rate by card position) + category-section CTR per brand once the anchor+rotation ordering ships, so the curated order can actually be checked against the random-shuffle baseline it replaces instead of being another unmeasured heuristic swap (from `/brands` brand-order UX panel critique, 2026-07-16; builds on `homepage-hero-prd.md` §12A/§12A.1)
- [ ] Decide and document the `/brands` anchor-tier visibility tradeoff: curation is currently planned to stay invisible to users (no "Featured"/"Most Authentic" badge, to avoid an authenticity-hierarchy read) — write down that reasoning explicitly as a considered tradeoff against opaque-algorithmic-ranking disclosure norms, rather than leaving it as an undocumented default (from `/brands` brand-order UX panel critique, 2026-07-16)

---

## 2026-07-12

### Shipped
- `feat(homepage-hero)` — Cold-load value-prop hero (homepage-hero-prd Tier 0/1 + refinements): standalone why-line carrying the model-set message, demoted+labeled category pills with new `CategoryIcon` glyphs (replacing emoji), warm cream surface tokens across hero/brands/trust, curated carousel order (`getCuratedBrandIds`) with price/heart chrome hidden + "Handcrafted in … India" cue, threshold-gated breadth signal, carousel pause/play + reduced-motion, ComingSoonSection removed
- `chore(deps)` — Pinned `shimmer` (runtime dep of Sentry/OpenTelemetry instrumentation that yarn wasn't hoisting; server threw "Cannot find module 'shimmer'")

### Next
- [ ] Supply: ingest Suta, Isharya, Kaunteya, House of Chikankari (top of the 2026-07-12 onboarding priority, §12A) and publish Fizzy Goblet listings in QA so the curated hero carousel actually leads with them
- [ ] Update `getCuratedBrandIds` (`configBrands.js`) to follow the full §12A onboarding order as those brands land

---

## 2026-06-21

### Shipped
- `refactor(identity)` — Removed all marketplace-giveaway UX & URL patterns: "Sharetribe" brand name, "Join our marketplace" copy, provider signup CTAs (replaced with mailto:shopatmela@gmail.com), "About the listing author" → "About the Brand"; `/u/:brand-uuid` now redirects to `/brands/:slug`; listing canonical `/l/:id` redirects to `/l/:slug/:id`; Avatar, BrandStorefront tabs, ProfileSettingsPage all use BrandPage route; added `BrandPageVariant` route
- `chore(config)` — Added The Nesavu brand (UUID 697b81ea) to configBrands.js to match .env.dev; fixed `Vilvah-store` → `vilvah-store` slug casing
- `feat(config)` — `isBestseller` listing field (boolean, `localOnly: true`) + `SCHEMA_TYPE_BOOLEAN` case in FilterComponent; `configHelpers.js` always merges `localOnly` fields regardless of Console config
- `fix(listings)` — `create-listings.js` now detects listings with stale CSV image IDs (live Sharetribe listing has zero images) via the existing bulk listings fetch and re-uploads from source URLs instead of silently reusing dead IDs; added `staleImagesFixed`/`staleImagesUnfixable` stats + per-listing-ID logging so runs are auditable
- `feat(scripts)` — `seed-brand-profiles.js` pushes curated `brandTagline`/`brandStory` from `brand_content.json` to matching brand users via the Sharetribe Integration API
- `feat(scraper)` — Added 3 new Shopify brands to scrape list (Daughters of India, Gauri and Nainika, Comet); refreshed Pluchi, Gado Living, My First Crayons product CSVs

### Next
- [ ] Build `bestseller-tagger.js` script in product-listing-integration — sets `publicData.isBestseller = true` on top 20% by orders per L1 category (PRD: trust-conversion §3.2)
- [ ] "Ships to US · US cards · Sold by [Brand]" static line on ListingPage near OrderPanel CTA (~30 min, PRD: trust-conversion §3.3a)
- [ ] Add production brand UUIDs to `configBrands.js` (currently empty — all URL redirects fall back to `/u/:id` in prod)
- [ ] Organization JSON-LD, BreadcrumbList JSON-LD, ItemList JSON-LD on `/brands/:brandSlug` (PRD: seo-aeo brand storefront ACs)
- [ ] `sitemap-brands.xml` — all brand slugs indexed
- [ ] 404 for unknown `brandSlug` (currently renders empty page)

### Blockers
- Production brand UUIDs not yet in configBrands.js — `/u/:id` → `/brands/:slug` redirect is dev-only until populated
