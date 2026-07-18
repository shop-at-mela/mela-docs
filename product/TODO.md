# Mela Dev TODO

Running log of shipped work and next actions. Newest entry at top.

---

## 2026-07-18

### Shipped
- `feat(analytics)` — Cross-shop / entry-exit attribution tracking (`crossshop-tracking-prd.md`): GTM + GA4 (via GTM) + Microsoft Clarity install (env-var gated), `entrySource.js` (first-touch UTM/referrer capture, session-persisted), `brandClickout.js` (`brand_clickout` dataLayer event + `openBrandStorefront()`), wired into all three Shop-from-Brand CTA surfaces (`OrderPanel`, `ProductOrderForm`, `InquiryWithoutPaymentForm`) via a single `onShopNow` path — also closes a pre-existing gap where two of those surfaces bypassed `RedirectTrustSheet`. Spec at `web-client/docs/analytics/crossshop-tracking.md`.

### Next
- [ ] Create the GTM container, GA4 property, and Clarity project; set `REACT_APP_GTM_ID` / `REACT_APP_GA4_ID` / `REACT_APP_CLARITY_ID`; configure the GA4 Event tag in GTM for `brand_clickout`
- [ ] Run the verification checklist in `crossshop-tracking.md` §6 (GTM Preview, GA4 DebugView, Clarity dashboard) end-to-end before trusting any report — PRD ACs stay unchecked until this passes
- [ ] Register the four GA4 custom dimensions (`brand_name`, `category`, `entry_source`, `product_id`) once the first real `brand_clickout` event has fired in DebugView
- [ ] Confirm the `brand_id` proposal (listing author/brand-user UUID, not a real schema field today) — see PRD §5b

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
