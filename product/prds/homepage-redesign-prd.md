# Homepage Redesign PRD

## Executive Summary
**Feature**: Multi-category homepage expansion + discovery platform expectation-setting
**Target URL / Entry Point**: `/` (www.shopatmela.com)
**Target Users**: All four Mela personas — Priya (Mixed Heritage), Arun (Second-Gen Indian American), Neha (First-Gen Immigrant), Sarah (Conscious American Parent)
**Business Objective**: Expand the homepage from a baby-clothing-centric surface to a multi-category discovery platform; simultaneously reset visitor expectations from "e-commerce store" to "discovery and curation layer" to reduce bounce and increase cross-category engagement
**Primary Success Metrics**:
- Homepage bounce rate: -15%
- BrandsPage CTR from homepage: +20%
- Non-baby category click-through from homepage: baseline → measurable (currently ~0)
- Time-on-page: +15%
- Session depth (pages per visit): +0.5 pages average

> **Supersedes**: `homepage-discovery-relaunch-prd.md` and `homepage-multi-category-prd.md` — both are archived.

---

## 1. Problem Statement

### Current State
The homepage was built around baby clothing and sends the wrong signals on two fronts:

**Wrong category scope:**
- H1: "Sustainable Baby Fashion with Indian Design Heritage"
- Hero trust badge: "Baby Safe"
- Hero quick-nav pills: Baby (0-24m), Toddler (2-5y), Organic, Accessories
- AgeNavigation title: "Shop by Baby's Age" (age groups Newborn → 18-24 months only)
- SEO title and meta are baby-only framed
- No occasion-based entry points

**Wrong model framing:**
- Hero CTA "Shop Now" links to SearchPage, implying a direct checkout store
- Mela is a discovery and curation platform — users browse here, then transact on each brand's own Shopify store
- The TrustAssurance section has honest "Transact on Brand Sites" language, but it appears too late and too low to correct the first impression

### User Pain Points
- **Sarah**: "Is this a real marketplace or just a pop-up?" — narrow vertical signals lack of scale
- **Priya**: Age nav stops at 18-24 months; her 6-year-old and Diwali shopping needs are invisible
- **Neha**: No path to women's clothing, ethnic wear, or home goods from the homepage
- **Arun**: No "Why India?" framing — cultural meaning behind Indian design is assumed, not explained
- **First-time visitors**: Click "Shop Now", hit an external Shopify store, and feel disoriented — expect cart and checkout, get a redirect

### Business Impact of Inaction
- Every non-baby-shopping visitor bounces with no fallback entry point
- Occasion-driven shopping (Diwali, gifting) — high-intent, high-AOV — has no homepage surface
- Bounce from model misalignment erodes trust with early adopters
- Confusion around the affiliate model undermines brand partner confidence

---

## 2. Goals & Non-Goals

### Goals
- Reframe the hero to explicitly lead with "Discover" language and route primary CTA to BrandsPage
- Open the homepage aperture to all Mela categories without removing baby as the primary vertical
- Add occasion-based navigation for cultural/seasonal shopping moments
- Add an editorial "Why Indian Design?" section to build trust with first-time visitors
- Update all baby-only language in SEO meta, trust signals, and navigation pills
- Add a "Coming Soon" section that previews end-to-end roadmap features honestly

### Non-Goals
- Building actual checkout, reviews, order tracking, or wishlists (out of scope — those are separate PRDs)
- Removing or deprioritising the baby & kids vertical — it stays the primary category
- Building new category pages (homepage links to existing SearchPage with filters)
- Redesigning the navigation bar or footer
- Homepage personalisation or A/B testing infrastructure

---

## 3. User Stories

| As a... | I want to... | So that... | Priority |
|---------|-------------|------------|----------|
| First-time visitor | Understand immediately that Mela helps me discover and vet Indian brands | I know what the platform does before I scroll | P0 |
| First-time visitor | See that Mela covers more than baby clothes | I don't immediately bounce if I'm shopping for something else | P0 |
| Second-gen Indian American parent | Feel confident that Mela curates brands I can trust | I don't have to do my own brand research | P0 |
| Priya (Mixed Heritage) | Find a "Diwali & Festivals" entry point on the homepage | I can shop for the whole family during cultural occasions | P0 |
| Neha (First-Gen) | See a "Fashion" category pill on the homepage | I know there's a path to ethnic wear beyond baby products | P0 |
| Sarah (Conscious Parent) | See "Quality Verified" instead of "Baby Safe" in trust badges | I understand these standards apply to all products, not just infant items | P1 |
| Arun (Second-Gen) | Read a brief editorial on why Indian design matters | I feel that Mela understands cultural meaning, not just commerce | P1 |
| Curious browser | See what features are coming | I understand this is a growing platform worth bookmarking | P1 |
| Brand partner | See that Mela clearly positions itself as a discovery platform | I understand how Mela will drive traffic to my Shopify store | P1 |

---

## 4. Feature Requirements

### Must Have (P0)
- **H1 copy update**: "Discover Quality Indian Brands for Your Family"
- **Subheadline update**: "Handpicked baby, home, and fashion brands from India — quality-verified, culturally rooted, delivered to your door."
- **Primary CTA**: "Explore Brands" → `/brands` (replaces "Shop Now" → SearchPage)
- **Secondary CTA**: "Browse Categories" → `/categories` (replaces "View Categories")
- **Hero trust badge**: "Baby Safe" → "Quality Verified" with category-agnostic description
- **Hero quick-nav pills**: Replace baby/toddler/organic/accessories with L0 categories: Baby & Kids, Fashion, Home & Kitchen, Gifts
- **FeaturedBrandPartners subtitle**: Updated to reflect curation-as-value-prop (see Copy Changes table)
- **OccasionStrip component**: New row above AgeNavigation — 4 occasions: Diwali & Festivals, New Baby, Everyday, Gifting
- **AgeNavigation title rename**: "Shop by Baby's Age" → "Shop Baby by Age" (scoped label, not primary framing)
- **Category section subtitle**: Replace "sustainable baby fashion" with "curated Indian design across categories"
- **SEO meta title**: Broadened — remove "Baby Clothes / Baby Fashion" as primary terms
- **SEO meta description**: Reflect discovery + multi-category positioning
- **Schema.org OfferCatalog**: Extended from "Baby Clothing & Accessories" to Baby & Kids, Fashion, Home & Kitchen

### Should Have (P1)
- **WhyIndia editorial section**: "Why Indian Design?" — 3 pillars (Centuries of Craft, Rooted in Sustainability, Bold Joyful Design) + CTA to SearchPage
- **WhyIndia merged with FeaturedBrandPartners**: Both in a single `<section>` wrapper in MelaHomePage
- **Coming Soon section**: Positioned below Indian Brands section, above TrustAssurance — 1 feature card: Wishlists & Gift Registry *(Unified Checkout, Community Reviews, Order Tracking removed 2026-05-25 — incompatible with directory positioning)*; footer note: "Checkout happens directly on each brand's Shopify store — we link you there securely."
- **TrustAssurance cert card**: "Baby Safe" → "Quality Verified / Independently Quality Tested"
- **TrustAssurance section title**: ~~"Why Families Should Trust Mela"~~ → "Every Brand Here Earned Its Place" *(updated 2026-05-25)*
- **TrustAssurance subtitle**: "We do the research so you don't have to." *(updated 2026-05-25)*
- **Hero trust model callout** *(UXR finding 2026-05-25)*: Add a single-line callout near the hero (below CTA buttons, above trust badges) that preempts the affiliate model surprise: `"You browse here — then shop directly on each brand's own store."` This removes the trust cliff before users reach TrustAssurance. Copy must not be apologetic or overly explanatory — one line, matter-of-fact. Particularly important for Sarah and Arun who have no prior relationship with Indian brand Shopify stores.
- **Featured artisan story in hero area** *(UXR finding 2026-05-25)*: Add one concrete artisan/brand callout adjacent to or beneath the hero headline — e.g., a rotating quote or single-line callout: `"Handwoven in Varanasi by Nizhoni Weavers"` paired with a product image. Even a static example converts trust for Sarah (conscious parent) and Arun (second-gen cultural reclaimer) better than all the badge infrastructure, because it makes the catalog feel real and specific rather than aggregated. This is not a full editorial section — it is a single line + image above the fold. WhyIndia (full editorial) is still needed below. Copy must use regional specificity, not "Indian handweaving" — see UXR Principle 8.

### Nice to Have (P2)
- Email signup CTA within "Coming Soon" section for launch notifications
- Localized "Coming Soon" copy for Indian-American cultural moments (e.g., "before Diwali 2026")
- WhyIndia section with real editorial image (brand photography, not stock)
- Occasion pills linked to curated landing pages rather than SearchPage filter params
- "Coming Soon: Women's Kurtas" placeholder card to signal roadmap
- **"New to Mela?" guided entry module** *(UXR finding 2026-05-25)*: A small discovery module for first-time visitors who don't know where to start. Arun (second-gen) navigates by need and occasion, not by category — he needs hand-holding that the category grid doesn't provide. The module offers 3-4 curated "start here" entry points by use-case: Gifting, Baby Shower, Diwali, First Piece for Home. Each links to a curated SearchPage filter combo. This is editorially maintained (not algorithmic) and can be a static component initially. Copy: `"Not sure where to start? We'll help."` — casual, inviting, not condescending. Do not use "New to Indian design" — see UXR cultural-framing principle.

---

## 5. UX Requirements

### Page Section Order (revised)
1. **HeroSection** — updated copy + Quality Verified trust badge + L0 category quick-nav + "Explore Brands" CTA
2. **CategoryShowcase** — OccasionStrip (new, above) + AgeNavigation (renamed) + category product grids
3. **Indian Brands Section** — FeaturedBrandPartners (updated subtitle) + WhyIndia (merged into same `<section>`)
4. **Coming Soon Section** — 4 feature teaser cards + honest affiliate model footer note
5. **TrustAssurance** — updated cert card + updated section title

### OccasionStrip
- Reuses `.ageFilterButton` visual pattern (icon + label pill cards) for design consistency
- 4 occasions: Diwali & Festivals (🪔), New Baby (🌸), Everyday (☀️), Gifting (🎁)
- Links to SearchPage with `pub_occasion` filter param
- Title: "Shop by Occasion"
- Placed above AgeNavigation, below the category section subtitle

### Hero Quick-Nav
- 4 pills: Baby & Kids (👶), Fashion (👗), Home & Kitchen (🏡), Gifts (🎁)
- Routes via `to={{ search: '?pub_categoryLevel1=...' }}` — consistent with existing SearchPage filter params

### WhyIndia
- 3-column card layout on desktop, single column on mobile
- Warm off-white background (`#f7f4ef`) to visually distinguish from white sections
- Each pillar: icon + bold title + 2-sentence description
- CTA: "Explore Indian Brands" → SearchPage
- Positioned after FeaturedBrandPartners within the same `<section>` in MelaHomePage

### Coming Soon Section
- Positioned below Indian Brands section, above TrustAssurance
- Background: warm off-white (#fdf8f4) to differentiate from white brand/category sections
- 4 cards in 2×2 grid on mobile, 4-column row on desktop
- Each card: icon + title + 1-sentence description + "Coming Soon" badge (amber/warm color)
- Footer note in small italic text — honest, not apologetic: current affiliate model stated plainly

### Edge Cases
- OccasionStrip: if `pub_occasion` filter returns 0 results, SearchPage handles empty state — OccasionStrip always renders
- WhyIndia: fully static, no loading state needed
- L0 quick-nav pills: if a category has no listings yet, SearchPage shows empty state — HeroSection does not conditionally hide pills
- Coming Soon section: fully static, no loading state

---

## 6. Copy Changes

| Location | Element | Old Copy | New Copy |
|----------|---------|----------|----------|
| en.json | `SectionMelaHero.heroHeadline` | "Sustainable Baby Fashion with Indian Design Heritage" | "Discover Quality Indian Brands for Your Family" *(UXR note 2026-05-25: this headline still leads with origin — "Indian Brands" — rather than with value. Consider an alternative for a later iteration that leads with craft or quality: e.g., "The craft behind the product. The story behind the brand." The category pills and subheadline handle the scope; the H1 can anchor on value instead of geography. Do not change in this sprint — validate with analytics first.)* |
| en.json | `SectionMelaHero.heroSubheadline` | "Discover premium organic clothing and accessories from innovative Indian designers. GOTS certified quality, traditional craftsmanship, delivered worldwide." | "Handpicked baby, home, and fashion brands from India — quality-verified, culturally rooted, delivered to your door." |
| en.json | `SectionMelaHero.shopNow` | "Shop Now" | "Explore Brands" |
| en.json | `SectionMelaHero.viewCategories` | "View Categories" | "Browse Categories" |
| en.json | `SectionMelaHero.trustBadge` | "Baby Safe" | "Quality Verified" |
| en.json | `CategoryShowcase.subtitle` | "Discover our carefully curated collection of sustainable baby fashion" | "Curated Indian design across categories" |
| en.json | `AgeNavigation.title` | "Shop by Baby's Age" | "Shop Baby by Age" |
| en.json | `FeaturedBrandPartners.subtitle` | "Discover premium brands that meet our strict quality and safety standards" | "We vet every Indian brand so you don't have to — quality, safety, and cultural craft, all in one place." |
| en.json | `MelaHomePage.trustTitle` | "Why Families Trust Mela" | "Every Brand Here Earned Its Place" *(updated 2026-05-25)* |
| en.json | `MelaHomePage.trustSubtitle` | "Your peace of mind is our priority - from quality to delivery" | "We do the research so you don't have to." *(updated 2026-05-25)* |
| en.json | `MelaHomePage.qualityGuarantees` | "Our Quality Promise" | "How We Vet Every Brand" *(updated 2026-05-25)* |
| en.json | `MelaHomePage.securityFeatures` | "Shopping with Confidence" | "Shopping on Brand Sites" *(updated 2026-05-25)* |
| en.json | `TrustAssurance.certCard` | "Baby Safe" | "Quality Verified / Independently Quality Tested" |
| MelaHomePage.js | `pageDescription` | "Discover GOTS certified organic baby clothes..." | "Mela curates the best Indian baby, fashion, and home brands for families in the US. Discover quality-verified brands, explore products, and shop directly on brand stores." |

---

## 7. Acceptance Criteria

### Hero
- [x] H1 reads "Discover Quality Indian Brands for Your Family"
- [x] Subheadline references baby, home, and fashion verticals
- [x] Hero trust badge shows "Quality Verified" (not "Baby Safe")
- [x] Hero quick-nav has category pills *(shipped with 6 pills — Baby & Kids, Fashion, Home & Kitchen, Jewelry, Beauty, Art — PRD spec of 4 broadened in implementation)*
- [x] Each quick-nav pill links to SearchPage with the correct `pub_categoryLevel1` param
- [x] "Explore Brands" CTA navigates to `/brands`
- [x] "Browse Categories" CTA navigates to `/categories`

### CategoryShowcase
- [x] OccasionStrip appears above AgeNavigation *(shipped with 2 occasions — Diwali & Festivals + Gifting — code comment: "Only two validated occasions for Mela's US diaspora audience"; New Baby + Everyday were dropped)*
- [x] AgeNavigation title reads "Shop Baby by Age" (not "Shop by Baby's Age")
- [x] Category section subtitle does not contain the word "baby"

### Indian Brands Section
- [x] FeaturedBrandPartners subtitle reflects curation-as-value-prop
- [ ] FeaturedBrandPartners and WhyIndia are inside the same `<section>` in MelaHomePage — ❌ WhyIndia not yet built (P1 remaining)
- [ ] WhyIndia renders 3 pillar cards with icon, title, and description — ❌ Not built
- [ ] WhyIndia "Explore Indian Brands" CTA links to SearchPage — ❌ Not built

### Coming Soon
- [x] ComingSoonSection renders below Indian Brands section, above TrustAssurance
- [x] Only Wishlists & Gift Registry card displays (Unified Checkout, Community Reviews, Order Tracking are commented out)
- [x] Footer note reads "Checkout happens directly on each brand's Shopify store — we link you there securely." (no "currently")

### TrustAssurance
- [x] TrustAssurance cert card reads "Quality Verified / Independently Quality Tested"
- [x] Section title reads "Every Brand Here Earned Its Place"
- [x] Section subtitle reads "We do the research so you don't have to."
- [x] Quality section heading reads "How We Vet Every Brand"
- [x] Security section heading reads "Shopping on Brand Sites"
- [x] "Mela Curation Promise" card is not present; 4 cards remain
- [x] First security card reads "Shop Directly With the Brand"

### SEO & i18n
- [x] SEO `<title>` does not contain "Baby Clothes" or "Baby Fashion" as primary terms
- [x] Page meta description reflects discovery + multi-category positioning
- [x] schema.org OfferCatalog contains at least 3 category entries (Baby & Kids, Fashion, Home & Kitchen)
- [x] All new i18n strings are present in `en.json` with matching `id` values in JSX
- [x] No regressions in existing sections (SavedItems, CategoryShowcase, TrustAssurance)

---

## 8. Success Metrics & Measurement

| Metric | Baseline | Target | Measurement Method |
|--------|----------|--------|--------------------|
| Homepage bounce rate | TBD | -15% | Google Analytics — sessions with 1 pageview / total sessions |
| BrandsPage CTR from homepage | TBD | +20% | Analytics: homepage → brands click events |
| Time on homepage | TBD | +15% | Analytics: avg. session duration on `/` |
| Hero CTA click rate | TBD | Track | GA4 event: `homepage_hero_cta_click` |
| Quick-nav click-through by category | TBD | Baseline | GA4 event: `homepage_quicknav_click` with `category` param |
| OccasionStrip click-through | TBD | Baseline | GA4 event: `homepage_occasion_click` with `occasion` param |
| WhyIndia CTA clicks | TBD | Track | GA4 event: `homepage_whyindia_cta_click` |
| Non-baby category browse sessions | TBD | Measurable (currently ~0) | GA4 — SearchPage sessions where `pub_categoryLevel1 != Baby-Kids` |
| Session depth (pages per visit) | TBD | +0.5 pages | GA4 avg pages/session on `/` entry sessions |

---

## 9. Dependencies & Risks

### Dependencies
- **BrandsPage must be live and functional** before changing primary CTA to `/brands`
- `pub_categoryLevel1` filter params must match Sharetribe configuration values exactly — coordinate with category taxonomy before linking
- `pub_occasion` is a new filter param; SearchPage must handle unknown filter values gracefully (show all results or empty state, not 500 error)
- `en.json` keys must stay in sync with JSX `id` props — missing keys render `defaultMessage` fallback silently
- Sharetribe Flex routing: confirm `BrandsPage` named route exists in `routeConfiguration.js`
- No backend changes required — all changes are frontend copy and component additions

### Risks
| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| L0 category pills link to empty SearchPage results (categories not yet populated) | Medium | Acceptable UX — SearchPage handles empty state; pills signal roadmap to users |
| `pub_occasion` filter not yet wired in SearchPage filter config | Medium | Link to SearchPage; SearchPage can ignore unknown params gracefully until occasion filter is added |
| WhyIndia editorial copy feels generic without real brand photography | Low | Copy is written for cultural resonance; image upgrade is P2 |

---

## 10. Out of Scope / Future Considerations

- Actual checkout integration (separate initiative)
- Community reviews system
- Order tracking infrastructure
- Wishlist/gift registry feature (see `saved-items-pasand-prd.md`)
- Email notification system for roadmap updates
- Occasion landing pages: `/occasions/diwali` dedicated pages with curated product grids
- Personalised homepage based on past browse behaviour
- Women's / Adult fashion homepage entry point — add once catalog is populated
- WhyIndia with real brand photography — once asset library is built
- A/B testing section order
