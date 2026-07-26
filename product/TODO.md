# Mela Dev TODO

Running log of shipped work and next actions. Newest entry at top.

---

## 2026-07-26

### Shipped
- `fix(brand-hero-card)` — correction to the 2026-07-25 BrandHeroCard ship (`brand-hero-card-webclient-prd.md`, still ✅ Shipped — no status change, this is a correctness fix on an already-shipped feature). Two issues found during a follow-up dev-lead review and fixed:
  - **P0 — the hero carousel was silently broken end-to-end.** The new `fetchHeroBrands` thunk requested each brand's profile image but only kept the user entity from the response, dropping the accompanying image entity. That left a dangling relationship reference in the store; resolving it inside `getHeroBrands` threw synchronously on every render, and with no error boundary around `HeroSection`, React quietly gave up re-rendering it — leaving the loading skeleton frozen on screen forever while the Redux store kept updating correctly underneath. Looked identical to a stuck network fetch from the outside; the actual crash was several layers deeper (traced via live Redux/React-fiber inspection in the running dev app, then confirmed against a browser console trace). Fixed by capturing the response's `included` image entities, matching the pattern already used by the two sibling fetch thunks in the same file.
  - **Scope-correctness gap:** hero-carousel eligibility no longer requires bestseller/configured products (the card renders no products at all, so that requirement was silently dropping brands with a real hero image and nothing else), and candidate coverage expanded from the first 10 curated brands to all curated brands, via a dedicated `fetchHeroBrands` thunk/`getHeroBrands` selector kept fully separate from `fetchFeaturedBrands` (which `FeaturedBrandPartners` still depends on unchanged).
  - Also fixed the focus-ring color (`--marketplaceColorLight`, already used elsewhere for a light purple, silently defeated the marigold fallback) — now points at `--colorAccent`, the actual marigold token.
- Verified all four fixes live against the dev Sharetribe API across multiple hard reloads (not just unit tests): hero cards render correctly, image varies per mount, keyboard focus ring is marigold, zero console errors. Full suite: 134/134 test suites, 2207/2207 tests passing.

### Next
- (carried from 2026-07-25, still open) The Nesavu and Masilo have no hero image source and are absent from the hero carousel — re-check the curated first-fold order once they get `brandHeroImageIds`/`brandHeroImages`

---

## 2026-07-25

### Shipped
- `feat(hero-section)` — BrandHeroCard (`brand-hero-card-webclient-prd.md`), status now ✅ Shipped: new image-forward hero card (1:1 product image, bottom gradient scrim, white brand name/tagline overlay) replaces `BrandCardHome` in the homepage hero carousel only — `BrandCardHome.js`/`.module.css` untouched, still shared by BrandsPage/FeaturedBrandPartners/PartnerCTACard. Resolves `publicData.brandHeroImageIds[i]` to a Sharetribe variant URL (preferred), falls back to `brandHeroImages[i]` (Shopify URL) on absence or runtime load failure; brands with no hero source at all are filtered out of the carousel (no logo fallback, no dead dots). Mobile carousel rebuilt as a scroll-snap track (88%-width slides with next-card peek) instead of the prior single-slide index swap, per user's mobile-first direction; desktop keeps a single 340px slide. Design direction (serif name + logo chip hybrid) landed via `/mockup` + `/ux-design` + `/uxr` + persona passes before implementation.
- Caught and fixed a real WCAG AA gap during the dev-lead acceptance pass: the initial scrim gradient and a marigold-tinted eyebrow color only held 4.5:1 contrast for the *average* case — a 2-line-wrapped brand name or tagline over a near-white product photo measured 4.22–4.28:1. Widened the scrim's opaque plateau to cover the tallest realistic text stack and reverted all overlay text to solid white (verified 4.97:1 at the worst-case point via direct sRGB luminance calculation, not visual inspection).
- Also fixed, incidentally: a test-pollution bug in the new `BrandHeroCard.test.js` where a failed assertion mid-test skipped `jest.spyOn` cleanup, corrupting every subsequent test in the file — root cause was a fresh `configureStore()` on every `rerender()` call rather than RTL's `wrapper` option reusing one store instance.

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
- `feat(analytics)` — Cross-shop / entry-exit attribution tracking (`crossshop-tracking-prd.md`): GTM + GA4 (via GTM) + Microsoft Clarity install (env-var gated), `entrySource.js` (first-touch UTM/referrer capture, session-persisted), `brandClickout.js` (`brand_clickout` dataLayer event + `openBrandStorefront()`), wired into all three Shop-from-Brand CTA surfaces (`OrderPanel`, `ProductOrderForm`, `InquiryWithoutPaymentForm`) via a single `onShopNow` path — also closes a pre-existing gap where two of those surfaces bypassed `RedirectTrustSheet`. Spec at `web-client/docs/analytics/crossshop-tracking.md`.

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
