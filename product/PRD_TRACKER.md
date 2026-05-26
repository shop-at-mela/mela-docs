# PRD Tracker

**Last updated:** 2026-05-25  
**Purpose:** Single-glance status across all active PRDs. Update build status here whenever a PRD's status changes — do not let this drift from the individual files.

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
| [trust-conversion-signals-prd.md](prds/trust-conversion-signals-prd.md) | 🟡 Partial | P0 | `isBestseller` needs pipeline | "Ships to US · US cards · Sold by [Brand]" static line on ListingPage (~30 min); `isBestseller` tagger script |
| [pre-redirect-sentiment-prd.md](prds/pre-redirect-sentiment-prd.md) | ✅ Shipped | P0 | — | Hotjar script; zero-results text prompt (P1) |
| [saved-items-pasand-prd.md](prds/saved-items-pasand-prd.md) | 🟡 Partial | P1 | — | Verify auth gate tiers; verify Topbar "❤ Saved" nav link; verify localStorage migration on login |
| [footer-legalese-prd.md](prds/footer-legalese-prd.md) | ⛔ Blocked | P0 | Legal copy not written | Write ToS + Privacy Policy copy |
| [brands-page-prd.md](prds/brands-page-prd.md) | 🟡 Partial | P1 | — | Brand tenure signal; Mela Verified badge; brand storefront SEO (see seo-aeo PRD) |
| [brand-storefront-prd.md](prds/brand-storefront-prd.md) | 🔲 Ready | P1 | Depends on `brands-page-prd.md` | Full brand storefront at `/brands/:brandSlug` — Organization JSON-LD, brand story, certifications |
| [seo-aeo-category-brand-pages-prd.md](prds/seo-aeo-category-brand-pages-prd.md) | 🟡 Partial | P0 | Brand storefront blocked on `brand-storefront-prd.md` | Category pages ✅ done; brand storefront SEO entirely unbuilt |
| [search-page-optimization-prd.md](prds/search-page-optimization-prd.md) | 🟡 Partial | P1 | — | Scroll position preservation; analytics instrumentation; image lazy loading |
| [newsletter-login-nudge-prd.md](prds/newsletter-login-nudge-prd.md) | 🔲 Ready | P1 | Requires Beehiiv account | Newsletter email capture; save nudge redesign; Beehiiv integration |
| [enrichment-pipeline-stage2-update-prd.md](prds/enrichment-pipeline-stage2-update-prd.md) | 🟡 Partial | P1 | — | Web-client ✅ done; verify pipeline (`prompt_engine.py`) and ingestion outputs `metaDescription` + `searchSynonyms` |
| [shopify-api-ingestion-prd.md](prds/shopify-api-ingestion-prd.md) | 🔲 Ready | P1 | — | Replace per-brand HTML scrapers with generic Shopify JSON API ingester |
| [ai-ready-product-discovery-prd.md](prds/ai-ready-product-discovery-prd.md) | 📋 Draft | P2 | Depends on enrichment pipeline + SEO foundation | Schema.org entity coverage for AI answer engines |

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
| Hero headline reframe (value-first vs origin-first) | `homepage-redesign-prd.md` §6 note | Copy-only | After analytics baseline |
| ~~`SignupPage/ValueProposition` — fix headline + "Indian" user-layer copy~~ | `saved-items-pasand-prd.md` §8 | ✅ Done 2026-05-25 | — |
| Hero trust model callout (one-line affiliate model explainer near CTA) | `homepage-redesign-prd.md` P1 new item | Copy + JSX, ~1 hr | High |
| Featured artisan story in hero area | `homepage-redesign-prd.md` P1 new item | Requires brand photo + copy | Medium |
| "New to Mela?" guided entry module | `homepage-redesign-prd.md` P2 new item | New component | Low |
| Signup value prop reframe (discovery continuity vs bookmarking) | `saved-items-pasand-prd.md` §5.9 note | Copy-only | Medium |
