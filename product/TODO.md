# Mela Dev TODO

Running log of shipped work and next actions. Newest entry at top.

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
