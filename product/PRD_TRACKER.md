# PRD Tracker

**Last updated:** 2026-08-19  
**Purpose:** Single-glance status across all active PRDs. Update build status here whenever a PRD's status changes — do not let this drift from the individual files.

**Folders:** PRDs live flat in `prds/`, except measurement and reporting work, which is bucketed in [`prds/insights/`](prds/insights/README.md). This table stays flat and lists everything regardless of folder.

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| ✅ Shipped | All P0 ACs done; in production |
| 🟡 Partial | Core shipped; P1/P2 items remain |
| 🔲 Ready | Spec complete; not started |
| ⛔ Blocked | Cannot start — external dependency |
| 📋 Draft | Spec not finalized |

---

## All PRDs at a Glance

| PRD | Status | Priority | Blocking / Blocked By | Remaining Work (P0) |
|-----|--------|----------|-----------------------|---------------------|
| [homepage-redesign-prd.md](prds/homepage-redesign-prd.md) | 🟡 Partial | P0 | — | WhyIndia editorial section (P1) |
| [trust-conversion-signals-prd.md](prds/trust-conversion-signals-prd.md) | 🟡 Partial | P0 | `isBestseller` needs pipeline | "Ships to US · US cards · Sold by [Brand]" static line on ListingPage (~30 min); `isBestseller` tagger script (field + filter now built) |
| [pre-redirect-sentiment-prd.md](prds/pre-redirect-sentiment-prd.md) | ✅ Shipped | P0 | — | Hotjar script; zero-results text prompt (P1) |
| [saved-items-pasand-prd.md](prds/saved-items-pasand-prd.md) | 🟡 Partial | P1 | — | Verify auth gate tiers; verify Topbar "❤ Saved" nav link; verify localStorage migration on login |
| [add-to-cart-restoration-prd.md](prds/add-to-cart-restoration-prd.md) | ✅ Shipped | P1 | — | None — §14 multi-brand cart grouping + inspiration-first recs shipped and browser-verified 2026-08-13 (see PRD §14.5 build note), on top of §12+§13's follow-up fixes shipped the same day |
| [footer-legalese-prd.md](prds/footer-legalese-prd.md) | ⛔ Blocked | P0 | Legal copy not written | Write ToS + Privacy Policy copy |
| [brands-page-prd.md](prds/brands-page-prd.md) | 🟡 Partial | P1 | — | Brand tenure signal; Mela Verified badge; brand storefront SEO (see seo-aeo PRD) |
| [brand-storefront-prd.md](prds/brand-storefront-prd.md) | 🔲 Ready | P1 | Depends on `brands-page-prd.md` | Full brand storefront at `/brands/:brandSlug` — Organization JSON-LD, brand story, certifications |
| [seo-aeo-category-brand-pages-prd.md](prds/seo-aeo-category-brand-pages-prd.md) | 🟡 Partial | P0 | — | Category pages ✅; canonical URLs + `/u/:id` redirect ✅; JSON-LD (Org, BreadcrumbList, ItemList), sitemap, 404 for bad slugs still needed |
| [search-page-optimization-prd.md](prds/search-page-optimization-prd.md) | 🟡 Partial | P1 | — | Scroll position preservation; analytics instrumentation; image lazy loading |
| [search-ranking-relevance-prd.md](prds/search-ranking-relevance-prd.md) | 🟡 Partial | P1 | analytics instrumentation (gates metrics) | Keyword/diaspora groundwork landing (`searchKeywords`/synonym `text` fields + schemas; classifier model split → enrichment on gpt-5.6-luna); **core not started**: `melaScore`/`boostTier` scorer + default-sort flip + backfill |
| [newsletter-login-nudge-prd.md](prds/newsletter-login-nudge-prd.md) | 🔲 Ready | P1 | Requires Beehiiv account | Newsletter email capture; save nudge redesign; Beehiiv integration |
| [enrichment-pipeline-stage2-update-prd.md](prds/enrichment-pipeline-stage2-update-prd.md) | 🟡 Partial | P1 | — | Web-client ✅ done; verify pipeline (`prompt_engine.py`) and ingestion outputs `metaDescription` + `searchSynonyms` |
| [shopify-api-ingestion-prd.md](prds/shopify-api-ingestion-prd.md) | 🔲 Ready | P1 | — | Replace per-brand HTML scrapers with generic Shopify JSON API ingester |
| [ai-ready-product-discovery-prd.md](prds/ai-ready-product-discovery-prd.md) | 📋 Draft | P2 | Depends on enrichment pipeline + SEO foundation | Schema.org entity coverage for AI answer engines |
| [crossshop-tracking-prd.md](prds/insights/crossshop-tracking-prd.md) | ✅ Shipped | P0 | — | `InquiryWithoutPaymentForm` CTA is implemented but untestable until an inquiry-type listing exists in the catalog (not a gap in the work). 2026-08-23: found and fixed a real gap — `saved_listing_toggle`/`saved_page_view`/`saved_recommendation_click` were pushing to `dataLayer` correctly (as the 2026-08-13 browser verification confirmed) but had no GTM triggers/tags at all, so none of the three ever reached GA4; GTM `GTM-5JSJ54C2` published as Version 6 with the missing wiring, not yet live-verified end-to-end |
| [shopper-visibility-reporting-prd.md](prds/insights/shopper-visibility-reporting-prd.md) | 🟡 Partial | P0 | Blocks P1 storefront work — OCTR baseline must be captured first (`storefront-validation-readiness-prd.md` §8) | Phase 1 site search ✅. 2026-08-23 correction: the "two cross-shop Explorations" and "Looker Studio dashboard" items previously listed here were stale — both already existed (owner Sanjot Sawhney), just undocumented; `Saved Surface` breakdown added to the clickout-rate Exploration and 4 new add-to-cart tiles added to the dashboard. Still genuinely open: turn Enhanced measurement Site search off; build Potential Shoppers Funnel + record OCTR baseline; BigQuery-dependent tiles (multi-brand rate, potential-shoppers/OCTR/search-terms scorecards) |
| [brand-hero-card-webclient-prd.md](prds/brand-hero-card-webclient-prd.md) | ✅ Shipped | P1 | — | First-fold coverage shrinks (The Nesavu, Masilo absent from hero) until those brands get `brandHeroImageIds`/`brandHeroImages` |
| [dev-to-production-migration-prd.md](prds/dev-to-production-migration-prd.md) | 📋 Draft | — | No production Sharetribe environment confirmed provisioned yet | `configBrands.js` production brand-ID map is empty (biggest item); social-share image re-upload; 5 other open questions (see PRD §8) — not started |

---

## Dependency Map

```
footer-legalese ←── [BLOCKED: legal copy]

enrichment-pipeline-stage2 (pipeline side)
    └── ai-ready-product-discovery

brand-storefront-prd
    └── seo-aeo (brand storefront SEO layer)
        └── brands-page-prd (Mela Verified badge, tenure)

shopify-api-ingestion
    └── enrichment-pipeline (feeds richer product data)

saved-items-pasand (verify remaining gaps)
    └── add-to-cart-restoration (extends SavedPage; also depends on pre-redirect-sentiment's RedirectTrustSheet)
newsletter-login-nudge ←── [BLOCKED: Beehiiv account]
```

---

## Recommended Build Order

Based on current state, ROI per effort, and dependencies:

### Now (unblocked, high ROI, short effort)
1. **Trust signals — "Ships to US" static line** (`trust-conversion-signals-prd.md` §3.3a) — ~30 min, completes the last P0 gap on ListingPage
2. **Saved items verification** (`saved-items-pasand-prd.md`) — audit auth gate tiers + Topbar link; close out any gaps before it's treated as shipped
3. **Enrichment pipeline verification** (`enrichment-pipeline-stage2-update-prd.md`) — run a test product through `prompt_engine.py`, confirm output fields; web-client is ready

### Next (medium effort, unlocks downstream)
4. **Brand storefront** (`brand-storefront-prd.md`) — dedicated `/brands/:brandSlug` component with Organization JSON-LD; unlocks brand SEO and SEO/AEO PRD completion
5. **isBestseller tagger script** (`trust-conversion-signals-prd.md` §3.2) — ~3 hrs; activates the Bestseller badge that's been dead since launch
6. **WhyIndia section** (`homepage-redesign-prd.md` P1) — editorial section; highest conversion value for Sarah and Arun personas

### When unblocked
7. **Footer legalese** (`footer-legalese-prd.md`) — launch blocker once legal copy is written; < 1 day dev effort
8. **Newsletter / Beehiiv** (`newsletter-login-nudge-prd.md`) — once Beehiiv account is active

### Later
9. **Shopify API ingester** (`shopify-api-ingestion-prd.md`) — reduces scraper maintenance; do when onboarding next batch of brands
10. **Search page optimization** (`search-page-optimization-prd.md`) — analytics instrumentation first, then use data to prioritize remaining items
11. **AI-ready discovery** (`ai-ready-product-discovery-prd.md`) — schema foundation needs to be solid first; do after brand storefront SEO is live

---

## UXR / Copy Debt (not in any PRD yet)

Items flagged during the 2026-05-25 UXR + UX design content analysis that need a home:

| Item | Flagged In | Effort | Priority |
|------|-----------|--------|----------|
| ~~Hero headline reframe (value-first vs origin-first)~~. **Update 2026-08-14:** shipped directly via `/ux-design panel` + `/uxr personas` consensus instead of waiting on the PMF-survey route — headline moved from story-led ("The makers and stories behind India's best brands") to product/brand-led ("Modern brands, rooted in India's rich, regional culture"), answering Priya's/Arun's "not costume-y / too traditional" trust need and applying the already-decided "living culture, not heritage" voice. The 3 mockup variants (Story-led/Discovery-led/Heritage-led) in `mockups/homepage-redesign.html` were superseded, not chosen from. | `homepage-redesign-prd.md` §6 note; homepage-redesign mockup | Copy-only | ✅ Done 2026-08-14 |
| Dedicated Gifting / occasion landing page (occasion is only a filter/module today — `brand-storefront-occasion-module-prd.md`; `/occasions/*` deferred in `homepage-redesign-prd.md` §10). Likely warrants its own small PRD. Interim nav link tracked in `TODO.md` 2026-07-30. | homepage-redesign mockup (pt 1) | New PRD + page | Med — validation wedge |
| BrandCardHome redesign: big primary photo + thumbnail filmstrip, **hover-to-swap desktop / tap mobile** (no swipe → no gesture conflict with the horizontal brand row; watch perf — card renders many times per row). Demonstrated in mockup. | homepage-redesign mockup (pt 7); `brand-hero-card-webclient-prd.md` | Component + spec | Med |
| Homepage certification education: keep condensed chips but teach on demand (tap/hover definitions — `CertificationBadge` already supports `showTooltip`); move deep education to a "How we vet" / sustainability surface. | homepage-redesign mockup (pt 8); `TrustAssurance` | Copy + progressive-disclosure | Low–Med |
| Occasion merchandising: inspiration + engagement hybrid (styled editorial scene + curated 2-product peek with why-line + CTA), rotated seasonally. | homepage-redesign mockup (pt 5); `homepage-redesign-prd.md` §5 | Copy + component | Med |
| ~~`SignupPage/ValueProposition` — fix headline + "Indian" user-layer copy~~ | `saved-items-pasand-prd.md` §8 | ✅ Done 2026-05-25 | — |
| Hero trust model callout (one-line affiliate model explainer near CTA) | `homepage-redesign-prd.md` P1 new item | Copy + JSX, ~1 hr | High |
| Featured artisan story in hero area | `homepage-redesign-prd.md` P1 new item | Requires brand photo + copy | Medium |
| "New to Mela?" guided entry module | `homepage-redesign-prd.md` P2 new item | New component | Low |
| Signup value prop reframe (discovery continuity vs bookmarking) | `saved-items-pasand-prd.md` §5.9 note | Copy-only | Medium |
