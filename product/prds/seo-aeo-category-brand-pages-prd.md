# SEO & AEO — Category Pages + Brand Storefront Pages PRD

**Document Owner:** Product / SEO Team  
**Last Updated:** 2026-04-11  
**Status:** Draft — Ready for Review  
**Priority:** High — Organic acquisition foundation  
**Related PRDs:** `brand-storefront-prd.md`, `brands-page-prd.md`, `technical/sitemap-prd.md`

---

## Executive Summary

**Feature:** Permanent, SEO-optimized category URLs and fully-instrumented brand storefront pages, optimized for both traditional search engines (Google, Bing) and AI answer engines (Perplexity, ChatGPT Search, Gemini).  
**Target URLs:**
- `/categories/:L0` — e.g., `/categories/baby-clothing`
- `/categories/:L0/:L1` — e.g., `/categories/baby-clothing/rompers`
- `/brands/:brandSlug` — e.g., `/brands/masilo`

**Target Users:** Diaspora parents actively searching for Indian baby products by category or brand name.  
**Business Objective:** Own the long-tail search surface for Indian baby product categories and brand discovery; build sustainable organic acquisition that doesn't depend on paid media.

**Primary Success Metrics:**
- Organic impressions on category + brand queries: **+200% in 6 months**
- Google Rich Result eligibility for brand pages: **>80% of brand pages**
- AI answer engine citations (Perplexity, Gemini): **trackable via referrer logs**
- `/categories/*` pages indexed by Google: **100% within 30 days of launch**
- Category page bounce rate: **< 55%** (vs ~70% on generic `/s` SearchPage)

---

## 1. Problem Statement

### Current State

The category and brand URL infrastructure exists in routing but is technically served as generic search pages with no SEO differentiation:

| Route | Component | Schema Type | Problems |
|-------|-----------|-------------|----------|
| `/categories/:level1/:level2?` | SearchPage | `SearchResultsPage` | Wrong schema type; no breadcrumbs; no editorial content |
| `/brands/:brandSlug` | SearchPage | `SearchResultsPage` | Wrong schema type; no Organization entity; no brand content |
| `/u/:id` | ProfilePage | None documented | UUID-based URL — not indexable under human-readable slug |

**The `/brands/:brandSlug` route currently renders SearchPage.** A user visiting `/brands/masilo` sees a filtered product grid with no brand story, no certifications, no founder narrative — just a product list with a tab title. This is not a brand storefront; it's a search results page with a pretty URL.

**Category pages have no editorial content.** `/categories/baby-clothing` ranks as well as `/s?pub_categoryLevel1=baby-clothing` from Google's perspective because they render identical DOM. There is no H1 introducing the category, no descriptive text, no FAQ — nothing to differentiate the URL from a parameterized search.

### User Pain Points

- A parent searching "organic baby rompers India" lands on a product grid with no context — no trust signal that this is a curated category, not a generic search.
- A parent researching Masilo specifically lands on a filtered product list — no founder story, no certifications summary, no "why Masilo" narrative. The brand storefront PRD requirements are fully unimplemented at the `/brands/:brandSlug` URL.
- AI assistants (Perplexity, ChatGPT) cannot build entity-rich answers about Mela's brand roster because no structured `Organization` or `Brand` schema exists on brand pages.

### Business Impact of Inaction

- Every month without canonical category URLs is a month of crawl budget wasted on parameterized URLs.
- Competitors building equivalent category pages will claim the long-tail rankings Mela could own.
- Brand partners expect their brand page to represent them — the current `/brands/masilo` rendering SearchPage is a trust risk with brand partners.
- AI search (Perplexity, Gemini, ChatGPT Search) is becoming a significant discovery channel; pages without structured entity data are invisible to these systems.

---

## 2. PRD Consolidation Decision

There are currently two brand-related PRDs with significant scope overlap:

| PRD | Current Focus | Recommended Scope Post-Consolidation |
|-----|--------------|--------------------------------------|
| `brands-page-prd.md` | `/brands` directory + brand profiles | **Keep — scope to `/brands` directory only** |
| `brand-storefront-prd.md` | `/u/:id` profile page (conversion-focused) | **Supersede — expand scope to `/brands/:brandSlug` as the canonical brand storefront URL** |

**Decision:** `brand-storefront-prd.md` is the active storefront PRD. Add this SEO/AEO PRD's requirements as a new section in `brand-storefront-prd.md`. The profile page at `/u/:id` should serve as a **redirect target or secondary URL**, with `/brands/:brandSlug` as the canonical, indexable, human-readable URL.

> **Action for PM:** Add a note to `brand-storefront-prd.md` referencing this PRD for SEO/AEO requirements. The storefront page described there should be built at `/brands/:brandSlug`, not `/u/:id`.

---

## 3. Goals & Non-Goals

### Goals

- Permanent, human-readable, crawlable URLs for every category level (L0, L1, L2 where applicable).
- Dedicated `CategoryPage` React component — not SearchPage — with editorial content zone, structured data, and breadcrumb navigation.
- Dedicated `BrandStorefrontPage` React component at `/brands/:brandSlug` — not SearchPage — with brand entity schema, product list schema, and AEO content blocks.
- Canonical URL strategy: `/brands/:brandSlug` is canonical for brand pages; `/u/:id` redirects to slug or includes `rel=canonical`.
- Full Schema.org markup: `BreadcrumbList`, `ItemList`, `Organization`, `FAQPage` where applicable.
- Sitemap coverage: all category paths + all brand slug URLs in `sitemap-default.xml` and `sitemap-brands.xml` respectively (per `technical/sitemap-prd.md`).

### Non-Goals

- Dynamic search result pages (`/s?keywords=...`) — excluded; canonical content only.
- Buyer profile pages (`/u/:id` for non-sellers) — no SEO value.
- Restructuring the Sharetribe category data model — work with current `categoryLevel1/2/3` public data fields.
- Real-time category page content management via CMS — use config-driven editorial copy initially.

---

## 4. User Stories

| As a... | I want to... | So that... | Priority |
|---------|-------------|------------|----------|
| Diaspora parent | Search "Indian organic baby clothing" and land on a page with curated products, editorial context, and trust signals | I understand I'm on a discovery platform, not a generic e-commerce search | P0 |
| Brand partner | See my brand at `/brands/masilo` with my story, certifications, and products — not a SearchPage | I trust that Mela represents me professionally | P0 |
| SEO crawler | Traverse `/categories/baby-clothing` → `/categories/baby-clothing/rompers` via BreadcrumbList schema | I can build a topical authority graph for Mela | P0 |
| AI answer engine | Find Organization schema at `/brands/masilo` with name, description, certifications, and country of origin | I can include Masilo in an answer about "Indian baby brands with GOTS certification" | P1 |
| Parent researching a brand | Get answers to "Is Masilo safe?" "What certifications does Masilo have?" from the brand page | I don't need to leave Mela to verify brand credibility | P1 |
| Parent browsing categories | See subcategory links from `/categories/baby-clothing` to `/categories/baby-clothing/rompers` | I can narrow my search without guessing the URL | P1 |

---

## 5. Feature Requirements

### 5A — Category Pages (`/categories/:L0/:L1?/:L2?`)

#### Must Have (P0)

**Dedicated `CategoryPage` component** — not SearchPage.
- Accepts `level1`, `level2`, `level3` path params and maps to category config.
- Renders product grid using same data pipeline as SearchPage (`loadData` via SearchPage.loadData with pre-applied category filters).
- Does NOT show the search bar or filter panel prominently — this is a browse page, not a search page.

**Editorial content block (above product grid):**
- H1: Category display name (e.g., "Baby Clothing")
- Subtitle/description: 1–2 sentences of editorial copy, config-driven per category.
- Breadcrumb nav: Home > Category L0 > Category L1 (clickable, routes to parent category URLs).

**Structured data (JSON-LD):**
```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://mela.com/" },
        { "@type": "ListItem", "position": 2, "name": "Baby Clothing", "item": "https://mela.com/categories/baby-clothing" },
        { "@type": "ListItem", "position": 3, "name": "Rompers", "item": "https://mela.com/categories/baby-clothing/rompers" }
      ]
    },
    {
      "@type": "CollectionPage",
      "name": "Baby Clothing — Authentic Indian Baby Products",
      "description": "...",
      "url": "https://mela.com/categories/baby-clothing",
      "mainEntity": {
        "@type": "ItemList",
        "itemListElement": [ /* top N products as ListItem */ ]
      }
    }
  ]
}
```

**Canonical URL:** `<link rel="canonical" href="https://mela.com/categories/baby-clothing" />` — no query params in canonical.

**Meta tags:**
- `<title>`: `{CategoryName} — Authentic Indian Baby Products | Mela`
- `<meta name="description">`: Config-driven editorial description per category (not auto-generated from URL slug).

**Subcategory navigation links:**
- If on L0 page: render subcategory pills/cards linking to L1 URLs.
- If on L1 page: render sibling subcategory links.
- Purpose: internal link equity, user wayfinding, and AEO entity relationships.

**Sitemap inclusion (per `technical/sitemap-prd.md`):**
- All L0 and L1 category paths enumerated in `sitemap-default.xml`.
- `changefreq: weekly`, `priority: 0.8` for L0; `priority: 0.7` for L1.

#### Should Have (P1)

**FAQ block per category (AEO):**
- 3–5 hardcoded Q&As per L0 category (config-driven).
- Example for "Baby Clothing": "What certifications should I look for in Indian baby clothing?", "What is GOTS certification?", "Are Indian baby clothes safe for newborns?"
- Rendered as collapsible accordion (visible to user, not hidden).
- Marked up with `@type: FAQPage` + `@type: Question` / `@type: Answer` JSON-LD.
- **Rationale for AEO:** Perplexity and ChatGPT pull from FAQ schema to answer parenting product questions. This is the highest-leverage AEO tactic for category pages.

**Category-specific featured brands section:**
- Below product grid: "Brands in this category" — 3–4 brand cards linking to `/brands/:brandSlug`.
- Adds entity relationship signals: category → brand.

**"Related categories" footer links:**
- Cross-link to sibling or parent categories.
- SEO value: improves crawl connectivity; AEO value: helps AI engines understand taxonomy.

#### Nice to Have (P2)

**Dynamic editorial copy** via CMS (Sharetribe hosted pages) rather than config-driven static copy.  
**Category-level aggregate review schema** (when sufficient product review data exists).  
**Product count badge** in page header ("47 products").

---

### 5B — Brand Storefront Pages (`/brands/:brandSlug`)

> Note: This section defines SEO/AEO requirements. Conversion UX requirements (brand story, tabs, demographic-specific layouts) are defined in `brand-storefront-prd.md`. These requirements should be read together.

### Current State Correction

**The brand storefront is already fully built — it lives at `/u/:id` (ProfilePage → BrandStorefront component).** It includes certifications, brand story, mission, about/bio, Organization schema, AggregateRating, founder year, and logo. None of this needs to be rebuilt.

The SEO problem is simpler than it appears: **the content exists, but at a UUID URL that Google cannot meaningfully index.** The only work is connecting `/brands/masilo` to the existing page.

`/brands/:brandSlug` currently routes to SearchPage — a filtered product list with no brand content.

#### Must Have (P0)

**Redirect `/brands/:brandSlug` → `/u/:id`**

The simplest implementation that solves the SEO problem without rebuilding anything:

1. Add `slug` field to each brand entry in `configBrands.js` (alongside existing UUID config).
2. In the `/brands/:brandSlug` route handler: look up UUID from slug in config, then 301-redirect to `/u/:uuid`.
3. Result: `mela.com/brands/masilo` resolves to the existing fully-built brand storefront. Google indexes the slug URL.

```js
// configBrands.js — add slug to existing entries
'68ebd6d5-ffce-4cb9-9605-3b69f2b67152': {
  slug: 'masilo',          // ← add this field
  featuredProductIds: [...],
}
```

This approach requires **zero changes to BrandStorefront, ProfilePage, or any brand content components.**

**Canonical URL tag on ProfilePage (P0):**

Once the slug exists, add a canonical tag to `ProfilePage.js` for provider users so Google knows `/brands/masilo` is the authoritative URL — even when someone navigates directly to `/u/:uuid`:

```jsx
// In ProfilePage.js — for isProvider === true:
<Page
  title={schemaTitle}
  schema={schemaMarkup}
  canonicalRootURL={publicData?.brandSlug
    ? `${config.marketplaceRootURL}/brands/${publicData.brandSlug}`
    : undefined}
>
```

**Canonical URL strategy summary:**
- Canonical URL: `/brands/:brandSlug` — Google indexes this.
- `/u/:id` for brand users: includes `rel=canonical` pointing to `/brands/:brandSlug`.
- `/brands/:brandSlug`: 301 redirects to `/u/:id` (user ends up at working page; Google credits the slug URL).
- No content rebuild required.

**Structured data (JSON-LD):**
```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://mela.com/" },
        { "@type": "ListItem", "position": 2, "name": "Brands", "item": "https://mela.com/brands" },
        { "@type": "ListItem", "position": 3, "name": "Masilo", "item": "https://mela.com/brands/masilo" }
      ]
    },
    {
      "@type": "Organization",
      "name": "Masilo",
      "url": "https://mela.com/brands/masilo",
      "logo": "https://[cdn]/masilo-logo.jpg",
      "description": "...",
      "foundingLocation": { "@type": "Place", "addressCountry": "IN" },
      "hasCredential": [
        { "@type": "EducationalOccupationalCredential", "name": "GOTS Certified" }
      ],
      "sameAs": ["https://www.masilo.in"]
    },
    {
      "@type": "ItemList",
      "name": "Masilo Products on Mela",
      "itemListElement": [ /* top N products as ListItem */ ]
    }
  ]
}
```

**Meta tags:**
- `<title>`: `{BrandName} — Indian Baby Products | Mela`
- `<meta name="description">`: Brand tagline + top certification + "Shop authentic Indian baby products by {BrandName} at Mela."
- `<meta property="og:image">`: Brand hero/logo image.

**Sitemap inclusion (per `technical/sitemap-prd.md`):**
- All `/brands/:brandSlug` URLs in `sitemap-brands.xml`.
- `changefreq: weekly`, `priority: 0.9`.

#### Should Have (P1)

**AEO content blocks:**

1. **"About {BrandName}" section** (visible, not hidden):
   - 2–3 sentences drawn from brand profile bio.
   - Maps to `Organization.description` in JSON-LD.
   - AEO rationale: AI engines extract "about" content for entity summaries. This is how Perplexity builds its answer for "Tell me about Masilo."

2. **Certifications panel** (visible badges + text labels):
   - Maps to `Organization.hasCredential` in JSON-LD.
   - Each certification rendered as a named credential, not just a badge icon.
   - AEO rationale: "Which Indian baby brands are GOTS certified?" — AI engines answer this by reading credential entities.

3. **FAQ block per brand** (P1):
   - 3 hardcoded questions per brand or template questions:
     - "Is {BrandName} organic?" → answer from certifications data.
     - "Where is {BrandName} made?" → answer from country of origin.
     - "Does Mela ship {BrandName} to the US?" → standard answer about Mela's model.
   - `@type: FAQPage` JSON-LD.

4. **Country of origin + founding year** (from brand profile publicData):
   - Maps to `Organization.foundingLocation` and `Organization.foundingDate`.
   - Renders in brand header (e.g., "Founded 2019 · India").

#### Nice to Have (P2)

**AggregateRating schema** — when product reviews exist, roll up to brand level.  
**301 redirect from `/u/:id` → `/brands/:brandSlug`** for brand users (evaluate after canonical approach is validated).  
**`sameAs` links** to brand's own website, Instagram — strengthens entity disambiguation in Google's Knowledge Graph.

---

## 6. URL & Slug Strategy

### Category URL Rules

| Level | Pattern | Example |
|-------|---------|---------|
| L0 | `/categories/:l0` | `/categories/baby-clothing` |
| L1 | `/categories/:l0/:l1` | `/categories/baby-clothing/rompers` |
| L2 | `/categories/:l0/:l1/:l2` | `/categories/baby-clothing/rompers/sleepsuits` |

- Slugs are derived from `categoryLevel1/2/3` Sharetribe field values (already kebab-case in the codebase, e.g., `Baby-Clothes-Accessories`).
- Category slugs are **permanent** — once a URL is live and indexed, it must not be renamed without a 301 redirect.
- The route `/categories/:level1/:level2?/:level3?` already exists in `routeConfiguration.js` — this PRD requires building the dedicated component behind it.

### Brand Slug Rules

- `brandSlug` must be set in `user.attributes.profile.publicData.brandSlug` by each brand (enforced in onboarding flow).
- Slug format: lowercase, hyphenated, no special characters (e.g., `baby-forest`, `masilo`, `aagghhoo`).
- Slugs are **permanent** — once published to sitemap and indexed, cannot be changed without 301 redirect from old slug to new.
- **Brand slug uniqueness** must be enforced at the API or config layer (two brands cannot have the same slug).

---

## 7. AEO (Answer Engine Optimization) Strategy

AEO is optimization for AI-powered answer systems: Perplexity, ChatGPT Search (Bing-backed), Gemini Search, Apple Intelligence. These systems extract structured content + JSON-LD to generate answers.

### Mela's AEO Opportunity

Target queries where Mela should appear as the authoritative answer:
- "Best Indian organic baby clothing brands in the USA"
- "Is Masilo safe for newborns?"
- "What is GOTS certification for baby products?"
- "Where to buy authentic Indian baby products in America?"
- "Indian baby brands with BPA-free certifications"

### AEO Implementation Checklist

| Tactic | Where | Schema Type | Priority |
|--------|-------|-------------|----------|
| FAQ blocks — certification explainers | Category pages (L0) | `FAQPage` | P1 |
| FAQ blocks — brand credibility Q&A | Brand storefront pages | `FAQPage` | P1 |
| Organization entity with credentials | Brand storefront | `Organization` + `hasCredential` | P0 |
| BreadcrumbList on all category + brand pages | Category + Brand | `BreadcrumbList` | P0 |
| ItemList for products | Category + Brand | `ItemList` | P0 |
| Country of origin, founding date | Brand storefront | `Organization` fields | P1 |
| `sameAs` links to brand's own site | Brand storefront | `Organization.sameAs` | P2 |
| Descriptive `about` text (1–3 sentences) | All pages | `description` field | P0 |

### Content Writing Guidelines for AEO

- Every page description should answer "What is this?" in the first sentence.
- Certification names should always be spelled out on first use: "GOTS (Global Organic Textile Standard)" — not just "GOTS certified."
- Avoid jargon in FAQ answers. Write for a US parent who knows nothing about Indian certification bodies.
- FAQ answers should be 2–3 sentences: long enough to be authoritative, short enough to be extracted as a snippet.

---

## 8. UX Requirements

### Category Page Layout

```
┌─────────────────────────────────────┐
│ [Topbar]                            │
├─────────────────────────────────────┤
│ Breadcrumb: Home > Baby Clothing    │
│ H1: Baby Clothing                   │
│ Description: 1–2 sentence editorial │
│ Subcategory pills (if L0 page):     │
│   [Rompers] [Sleepwear] [Onesies]  │
├─────────────────────────────────────┤
│ Product Grid (12–24 products)       │
│ (same card component as SearchPage) │
├─────────────────────────────────────┤
│ Featured Brands in this category    │
│ [BrandCard] [BrandCard] [BrandCard] │
├─────────────────────────────────────┤
│ FAQ Accordion (P1)                  │
│ Q: What certifications...?          │
│ Q: What is GOTS?                    │
├─────────────────────────────────────┤
│ [Footer]                            │
└─────────────────────────────────────┘
```

**Key UX decisions:**
- No search bar on CategoryPage (distinguish from SearchPage — this is a curated browse, not ad-hoc search).
- Filter panel: minimal (Age Group, Certification only — not the full SearchPage filter set).
- Mobile: breadcrumb collapses to "< Baby Clothing" back-arrow pattern.
- Empty state: if no products in category, show "Coming Soon" with CTA to `/brands` page.

### Brand Storefront Page Layout

The layout is fully specified in `brand-storefront-prd.md`. SEO/AEO additions:

- Brand header must include: founding year, country of origin, certification badges with **text labels** (not icon-only — text is what gets indexed).
- "About" section must be a real `<p>` tag (not a modal, not a tooltip) so it's crawlable.
- FAQ accordion must be server-rendered (not client-only) for crawlability.
- All certification names must be spelled out in full at least once per page.

### States to Handle

| State | Category Page | Brand Storefront Page |
|-------|--------------|----------------------|
| Loading | Skeleton grid, breadcrumb placeholder | Skeleton header + grid |
| No products | "Coming soon" message + CTA to related category or `/brands` | "No products listed yet" + brand contact CTA |
| Invalid slug/category | 404 page | 404 page |
| Brand has no `brandSlug` in publicData | N/A | Fall back to `/u/:id` (canonical tag still required) |

---

## 9. Acceptance Criteria

### Category Pages

- [ ] `/categories/baby-clothing` renders `CategoryPage` component (not SearchPage).
- [ ] H1 on category page matches the category display name from config.
- [ ] Breadcrumb renders as: Home > [L0 name] > [L1 name] for nested categories.
- [ ] `BreadcrumbList` JSON-LD present in page `<head>` with correct URLs.
- [ ] `CollectionPage` JSON-LD with nested `ItemList` present in `<head>`.
- [ ] `<link rel="canonical">` points to the clean `/categories/:l0/:l1` URL (no query params).
- [ ] `<title>` tag = `{CategoryName} — Authentic Indian Baby Products | Mela`.
- [ ] `<meta name="description">` is editorial (config-driven), not auto-generated from URL.
- [ ] Subcategory pills render on L0 pages with correct links to L1 URLs.
- [ ] All L0 and L1 category paths appear in `sitemap-default.xml`.
- [ ] Category pages return HTTP 200 (not a redirect to `/s?pub_categoryLevel1=...`).
- [ ] FAQ block renders (P1): at least 3 Q&As per L0 category, marked up as `FAQPage` JSON-LD.
- [ ] Google Rich Results Test passes for BreadcrumbList on at least one category page.
- [ ] Mobile: breadcrumb navigation is functional and touch-friendly at 375px viewport.

### Brand Storefront Pages

- [ ] `configBrands.js` has a `slug` field for every curated brand (~10 brands).
- [ ] `/brands/masilo` 301-redirects to `/u/{masilo-uuid}` (the existing fully-built brand storefront).
- [ ] Brand storefront content (name, logo, tagline, certifications, about, brand story) already renders via existing `BrandStorefront` component — verify it still works after redirect.
- [ ] Certifications rendered as text labels (not icon-only) — verify existing implementation satisfies this.
- [ ] `Organization` JSON-LD present with: `name`, `url`, `logo`, `description`, `foundingLocation`, `hasCredential` (from certifications data).
- [ ] `BreadcrumbList` JSON-LD present: Home > Brands > {BrandName}.
- [ ] `ItemList` JSON-LD present for brand's products.
- [ ] `<link rel="canonical">` on `/brands/:brandSlug` points to itself.
- [ ] `<link rel="canonical">` on `/u/:id` (for brand users) points to `/brands/:brandSlug`.
- [ ] `<title>` = `{BrandName} — Indian Baby Products | Mela`.
- [ ] `<meta name="description">` includes brand tagline + top certification + Mela context.
- [ ] `<meta property="og:image">` set to brand logo or hero image.
- [ ] All brand slugs appear in `sitemap-brands.xml`.
- [ ] FAQ block renders (P1): 3 Q&As, marked up as `FAQPage` JSON-LD.
- [ ] Google Rich Results Test passes for Organization schema on at least one brand page.
- [ ] Invalid/unknown `brandSlug` returns 404 (not an empty product grid).

---

## 10. Success Metrics & Measurement

### SEO Metrics (Google Search Console)

| Metric | Baseline | 30-day target | 90-day target |
|--------|----------|---------------|---------------|
| Category page impressions | 0 (not indexed) | 500+ | 5,000+ |
| Brand page impressions | ~low (UUID URLs) | 1,000+ | 10,000+ |
| Pages indexed (category) | 0 | 100% of published categories | 100% |
| Pages indexed (brand) | ~partial | 100% of published brands | 100% |
| Average position — category queries | N/A | < 30 | < 15 |
| Average position — brand name queries | N/A | < 10 | < 5 |

### AEO Metrics

- Track referrer `perplexity.ai`, `bing.com/search` (ChatGPT), `bard.google.com` in analytics.
- Set up Google Search Console rich result monitoring for BreadcrumbList and FAQPage.
- Monitor Google Knowledge Panel creation for top 3 brands (Masilo, Baby Forest, etc.) — indicates entity disambiguation success.

### Analytics Events to Track

| Event | Trigger | Properties |
|-------|---------|------------|
| `category_page_view` | CategoryPage mount | `{ category_l0, category_l1, product_count }` |
| `brand_storefront_view` | BrandStorefrontPage mount | `{ brand_slug, product_count, source_url }` |
| `subcategory_click` | Click on subcategory pill | `{ from_category, to_category }` |
| `brand_card_click` | Click brand card on category page | `{ brand_slug, source_category }` |
| `faq_expand` | Open FAQ accordion item | `{ page_type, question_index }` |

---

## 11. Dependencies & Risks

### Technical Dependencies

| Dependency | Owner | Risk |
|------------|-------|------|
| `brandSlug` field in user `publicData` for all published brands | Brand onboarding flow | Medium — some brands may not have slug set; need fallback |
| Category config in `configListing.js` (or Sharetribe hosted assets) for display names + editorial copy | Developer | Low — already exists |
| Server-side rendering of JSON-LD schemas | Already implemented via `Page` component | Low |
| Sitemap generation of brand + category URLs | `technical/sitemap-prd.md` | Medium — dependent on sitemap PRD implementation |
| SDK query for brand's published listings | Same as ProfilePage today | Low |

### Risks

**Brand slug gaps:** If a brand user hasn't set `brandSlug` in their profile, `/brands/:brandSlug` has no target. Mitigation: audit all published brands in config, manually backfill slugs for the initial curated set (currently ~10 brands).

**Slug permanence enforcement:** If a brand changes their slug after indexing, all indexed URLs 404. Mitigation: treat `brandSlug` as immutable after first publication; surface a warning in brand profile settings.

**Category content quality:** Config-driven editorial copy will be generic initially. Mitigation: prioritize writing copy for the top 5 L0 categories before launch.

**SearchResultsPage schema on category/brand routes:** Currently, `/categories/*` and `/brands/*` return `@type: SearchResultsPage` (from `SearchPage.shared.js` L583). This is incorrect. The new dedicated components must emit the correct schema types. **The existing SEO logic in `SearchPage.shared.js` (isCategoryPage / isBrandPage) is a band-aid — it emits wrong schema and should be replaced, not extended.**

---

## 12. Sitemap PRD Relationship

This PRD defines the **page content and SEO requirements**. The `technical/sitemap-prd.md` defines the **URL discovery and indexing requirements**. Both must ship together for SEO impact:

- Sitemap PRD Gap 3 (brand URLs in `sitemap-brands.xml`) is a pre-requisite for brand page indexing.
- Sitemap PRD Gap 4 (category paths in `sitemap-default.xml`) is a pre-requisite for category page indexing.
- **Both sitemap changes are blocked until the dedicated page components exist** — submitting sitemap URLs that return SearchPage content wastes crawl budget and risks a thin-content penalty.

**Recommended sequencing:**
1. Build `CategoryPage` component + `BrandStorefrontPage` component (this PRD).
2. Implement sitemap changes (sitemap PRD) to submit new URLs.
3. Submit to Google Search Console.
4. Monitor indexing + impressions at 30/60/90 days.

---

## 13. Out of Scope / Future Considerations

- **CMS-driven category editorial copy** — Phase 2; start with config-driven copy.
- **Category-level blog posts / buying guides** — High AEO value, but requires content team capacity.
- **Brand comparison pages** (e.g., `/compare/masilo-vs-baby-forest`) — Future; powerful SEO/AEO target.
- **Programmatic SEO pages** (age-group × category × certification matrix) — e.g., `/categories/baby-clothing/newborn/organic` — Very high volume potential; evaluate after Phase 1 performance data.
- **`/u/:id` → `/brands/:brandSlug` 301 redirect** — P2; implement after canonical tag approach is validated in Search Console.
- **International SEO / hreflang** — Out of scope for current US-only focus.
