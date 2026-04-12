# Homepage Multi-Category Expansion PRD

## Executive Summary
**Feature**: Expand the Mela homepage from a baby-clothing-centric layout to a multi-category discovery surface that reflects Mela's broader Indian design identity
**Target URL / Entry Point**: `/` (homepage)
**Target Users**: All four Mela personas — Sarah (Conscious American Parent), Priya (Mixed Heritage Family), Neha (First-Gen Immigrant), Arun (Second-Gen Indian American)
**Business Objective**: Increase homepage-to-browse conversion for non-baby categories; reduce bounce rate for visitors who arrive looking for fashion, home goods, or occasion-driven gifting
**Primary Success Metrics**:
- Homepage bounce rate: reduce by 15%
- Non-baby category click-through from homepage: baseline → measurable (currently ~0)
- Session depth (pages per visit): +0.5 pages average

---

## 1. Problem Statement

### Current State
The homepage was built exclusively around baby clothing and accessories:
- H1: "Sustainable Baby Fashion with Indian Design Heritage"
- Hero trust badge: "Baby Safe"
- Hero quick-nav pills: Baby (0-24m), Toddler (2-5y), Organic, Accessories
- Category subtitle: "Discover our carefully curated collection of sustainable baby fashion"
- AgeNavigation title: "Shop by Baby's Age" (age groups: Newborn → 18-24 months only)
- SEO title: "Organic Baby Clothes & Sustainable Baby Fashion | GOTS Certified | Mela"
- Trust section title: "Why Families Trust Mela" (all certifications baby-framed)
- No occasion-based entry points
- No editorial "Why India?" context for new visitors

### User Pain Points
- **Sarah**: "Is this a real marketplace or just a pop-up?" — narrow vertical signals lack of scale
- **Priya**: Age nav stops at 18-24 months; her 6-year-old and Diwali shopping needs are invisible
- **Neha**: No path to women's clothing, ethnic wear, or home goods from the homepage
- **Arun**: No "Why India?" framing — the cultural meaning behind Indian design is assumed, not explained

### Business Impact of Inaction
Every non-baby-shopping visitor bounces with no fallback entry point. Occasion-driven shopping (Diwali, gifting) — a high-intent, high-AOV use case — has no homepage surface. As Mela adds categories, the homepage becomes increasingly misleading.

---

## 2. Goals & Non-Goals

### Goals
- Open the homepage aperture to all Mela categories without removing baby as the primary vertical
- Add occasion-based navigation for cultural/seasonal shopping moments
- Add an editorial "Why Indian Design?" section to build trust with first-time visitors
- Update all baby-only language in SEO meta, trust signals, and navigation pills
- Merge the Indian Brands and editorial content into a single cohesive section

### Non-Goals
- Removing or deprioritising the baby & kids vertical — it stays the primary category
- Building new category pages (homepage links to existing SearchPage with filters)
- Redesigning the navigation bar or footer
- Adding personalisation or user-state-aware content

---

## 3. User Stories

| As a... | I want to... | So that... | Priority |
|---------|-------------|------------|----------|
| First-time visitor | See that Mela covers more than baby clothes | I don't immediately bounce if I'm shopping for something else | P0 |
| Priya (Mixed Heritage) | Find a "Diwali & Festivals" entry point on the homepage | I can shop for the whole family during cultural occasions | P0 |
| Neha (First-Gen) | See a "Fashion" category pill on the homepage | I know there's a path to ethnic wear beyond baby products | P0 |
| Arun (Second-Gen) | Read a brief editorial on why Indian design matters | I feel that Mela understands cultural meaning, not just commerce | P1 |
| Sarah (Conscious Parent) | See "Quality Verified" instead of "Baby Safe" in trust badges | I understand these standards apply to all products, not just infant items | P1 |

---

## 4. Feature Requirements

### Must Have (P0)
- **H1 copy update**: "Sustainable Indian Design for Growing Families" (replaces "Sustainable Baby Fashion with Indian Design Heritage")
- **Subheadline update**: Broadened to cover clothing and accessories, not baby-only
- **Hero trust badge**: "Baby Safe" → "Quality Verified" with category-agnostic description
- **Hero quick-nav pills**: Replace baby/toddler/organic/accessories with L0 categories: Baby & Kids, Fashion, Home & Kitchen, Gifts
- **Category section subtitle**: Replace "sustainable baby fashion" with "curated Indian design across categories"
- **OccasionStrip component**: New row above AgeNavigation with 4 occasions: Diwali & Festivals, New Baby, Everyday, Gifting
- **AgeNavigation title rename**: "Shop by Baby's Age" → "Shop Baby by Age" (scoped label, not primary framing)
- **SEO meta title**: Broadened to include families/fashion/home
- **SEO meta description**: Include Indian designers, organic, GOTS — not exclusively baby
- **Schema.org OfferCatalog**: Extended from "Baby Clothing & Accessories" to multi-category entries (Baby & Kids, Fashion, Home & Kitchen)

### Should Have (P1)
- **WhyIndia editorial section**: "Why Indian Design?" — 3 pillars (Centuries of Craft, Rooted in Sustainability, Bold Joyful Design) + CTA to SearchPage
- **WhyIndia merged with FeaturedBrandPartners**: Both sections share a single `<section>` wrapper in MelaHomePage (Indian Brands + Why India context belong together)
- **TrustAssurance certification update**: "Baby Safe" cert card → "Quality Verified / Independently Quality Tested"
- **Trust section title**: "Why Families **should** Trust Mela" — more inviting and action-oriented than the declarative original

### Nice to Have (P2)
- WhyIndia section with a real editorial image (brand photography, not stock)
- Occasion pills linked to curated landing pages rather than SearchPage filter params
- "Coming Soon: Women's Kurtas" placeholder card to signal roadmap

---

## 5. UX Requirements

### Page Section Order (revised)
1. HeroSection — updated copy + trust badges + L0 category quick-nav
2. CategoryShowcase — OccasionStrip (new) + AgeNavigation (renamed) + category product grids
3. Indian Brands Section — FeaturedBrandPartners + WhyIndia (merged into one `<section>`)
4. TrustAssurance — updated cert card + updated section title

### OccasionStrip
- Reuses `.ageFilterButton` visual pattern (icon + label pill cards) for design consistency
- 4 occasions: Diwali & Festivals (🪔), New Baby (🌸), Everyday (☀️), Gifting (🎁)
- Links to SearchPage with `pub_occasion` filter param
- Placed above AgeNavigation, below the section subtitle
- Title: "Shop by Occasion"

### WhyIndia
- 3-column card layout on desktop, single column on mobile
- Warm off-white background (`#f7f4ef`) to visually distinguish from white sections
- Each pillar: icon + bold title + 2-sentence description
- CTA button: "Explore Indian Brands" → SearchPage
- Positioned after FeaturedBrandPartners within the same `<section>` in MelaHomePage

### Hero Quick-Nav
- 4 pills replacing the previous 4 (same visual treatment, new labels/icons/routes)
- Baby & Kids (👶), Fashion (👗), Home & Kitchen (🏡), Gifts (🎁)
- Routes via `to={{ search: '?pub_categoryLevel1=...' }}` (consistent with existing SearchPage filter params)

### Edge Cases
- OccasionStrip: if a `pub_occasion` filter returns 0 results on SearchPage, SearchPage handles the empty state — OccasionStrip always renders
- WhyIndia: fully static, no loading state needed
- L0 quick-nav pills: if a category has no listings yet, SearchPage shows empty state — HeroSection does not conditionally hide pills

---

## 6. Acceptance Criteria

- [ ] H1 reads "Sustainable Indian Design for Growing Families" (not "Sustainable Baby Fashion")
- [ ] Hero trust badge shows "Quality Verified" (not "Baby Safe")
- [ ] Hero quick-nav has exactly 4 pills: Baby & Kids, Fashion, Home & Kitchen, Gifts
- [ ] Each quick-nav pill links to SearchPage with the correct `pub_categoryLevel1` param
- [ ] OccasionStrip appears above AgeNavigation with 4 occasion pills
- [ ] AgeNavigation title reads "Shop Baby by Age" (not "Shop by Baby's Age")
- [ ] Category section subtitle does not contain the word "baby"
- [ ] FeaturedBrandPartners and WhyIndia are inside the same `<section>` in MelaHomePage
- [ ] WhyIndia renders 3 pillar cards with icon, title, and description
- [ ] WhyIndia "Explore Indian Brands" CTA links to SearchPage
- [ ] TrustAssurance cert card reads "Quality Verified / Independently Quality Tested"
- [ ] TrustAssurance section title reads "Why Families should Trust Mela"
- [ ] SEO `<title>` does not contain "Baby Clothes" or "Baby Fashion" as primary terms
- [ ] schema.org OfferCatalog contains at least 3 category entries (Baby & Kids, Fashion, Home & Kitchen)
- [ ] All new i18n strings are present in `en.json` with matching `id` values in JSX

---

## 7. Success Metrics & Measurement

| Metric | Measurement method |
|--------|--------------------|
| Homepage bounce rate | Google Analytics — sessions with 1 pageview / total sessions |
| Quick-nav click-through by category | GA4 event: `homepage_quicknav_click` with `category` param |
| OccasionStrip click-through | GA4 event: `homepage_occasion_click` with `occasion` param |
| WhyIndia CTA clicks | GA4 event: `homepage_whyindia_cta_click` |
| Non-baby category browse sessions | GA4 — SearchPage sessions where `pub_categoryLevel1 != Baby-Kids` |

---

## 8. Dependencies & Risks

**Dependencies**
- `pub_categoryLevel1` filter params must match Sharetribe configuration values exactly — coordinate with the category taxonomy before linking
- `pub_occasion` is a new filter param; SearchPage must handle unknown filter values gracefully (show all results or empty state, not 500 error)
- `en.json` keys must stay in sync with JSX `id` props — missing keys render the `defaultMessage` fallback silently

**Risks**
| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| L0 category pills link to empty SearchPage results (categories not yet populated) | Medium | Acceptable UX — SearchPage handles empty state; pills signal roadmap to users |
| `pub_occasion` filter not yet wired in SearchPage filter config | Medium | Link to SearchPage; SearchPage can ignore unknown params gracefully until occasion filter is added |
| WhyIndia editorial copy feels generic without real brand photography | Low | Copy is written for cultural resonance; image upgrade is P2 |

---

## 9. Out of Scope / Future Considerations

- **Occasion landing pages**: `/occasions/diwali` dedicated pages with curated product grids — valuable once inventory supports it
- **Personalised homepage**: Showing different quick-nav or featured products based on past browse behaviour
- **Women's / Adult fashion section**: Homepage entry point for adult ethnic wear — add once catalog is populated
- **WhyIndia with photography**: Replace icon-only pillars with brand photography once asset library is built
- **A/B testing section order**: Test whether WhyIndia above FeaturedBrandPartners converts better than the current order
