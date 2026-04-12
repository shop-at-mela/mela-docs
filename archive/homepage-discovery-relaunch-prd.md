# Homepage Discovery Relaunch PRD

## Executive Summary
**Feature**: Homepage copy refresh + "Coming Soon" roadmap section  
**Target URL / Entry Point**: `/` (www.shopatmela.com)  
**Target Users**: Second-gen Indian American parents, mixed-heritage families, conscious parenting community  
**Business Objective**: Accurately set expectations that Mela is a brand discovery platform (not a direct checkout store), reduce bounce from misaligned expectations, and build trust + excitement around the roadmap  
**Primary Success Metrics**:
- BrandsPage CTR from homepage: +20%
- Homepage bounce rate: -10%
- Time-on-page: +15%

---

## 1. Problem Statement

### Current State
The homepage hero reads "Sustainable Indian Design for Growing Families" with a "Shop Now" CTA linking to the Search page. This positions Mela as a full e-commerce store. In reality, Mela is a **discovery and curation platform** — users browse here, then transact on each brand's own Shopify store. The TrustAssurance section already has honest "Transact on Brand Sites" language, but it comes too late and too low on the page to set expectations before users click.

There is also no section on the page that previews the end-to-end features (unified checkout, reviews, order tracking) coming in the near future — a missed opportunity to build excitement and explain why the current affiliate model is a stepping stone, not a limitation.

### User Pain Points
- Users clicking "Shop Now" expect a cart and checkout flow; they hit an external Shopify store and feel disoriented
- Second-gen Indian American parents (primary persona) value transparency and trust; ambiguity around the shopping model erodes confidence
- No visibility into product roadmap creates a "is this project alive?" question for early adopters

### Business Impact of Inaction
- High bounce rate from misaligned expectations
- Low BrandsPage engagement (missed discovery loop)
- Confusion around the affiliate model undermines brand partner confidence

---

## 2. Goals & Non-Goals

### Goals
- Reframe the hero to explicitly lead with "discover" language
- Route the primary CTA to BrandsPage (the core discovery surface)
- Add a "Coming Soon" section that previews the end-to-end roadmap
- Keep the honest "Transact on Brand Sites" language in TrustAssurance (do not remove)

### Non-Goals
- Building actual checkout, reviews, order tracking, or wishlists (out of scope)
- Redesigning the page layout or moving sections
- Homepage personalization or A/B testing infrastructure

---

## 3. User Stories

| As a... | I want to... | So that... | Priority |
|---------|-------------|------------|----------|
| First-time visitor | Understand immediately that Mela helps me discover and vet Indian brands | I know what the platform does before I scroll | P0 |
| Second-gen Indian American parent | Feel confident that Mela curates brands I can trust | I don't have to do my own brand research | P0 |
| Curious browser | See what features are coming | I understand this is a growing platform worth bookmarking | P1 |
| Brand partner | See that Mela clearly positions itself as a discovery platform | I understand how Mela will drive traffic to my Shopify store | P1 |

---

## 4. Feature Requirements

### Must Have (P0)
- Hero headline updated to lead with "Discover" + "Indian Brands"
- Hero subheadline sets expectation of curated discovery (not direct checkout)
- Primary CTA copy changed from "Shop Now" → "Explore Brands"
- Primary CTA route changed from SearchPage → BrandsPage
- FeaturedBrandPartners subtitle updated to reinforce curation-as-value-prop
- Meta description updated to reflect discovery positioning

### Should Have (P1)
- New "Coming Soon" section between FeaturedBrandPartners and TrustAssurance
- 4 feature teaser cards: Unified Checkout, Community Reviews, Order Tracking, Wishlists & Gift Registry
- Footer note in "Coming Soon" section honestly stating current affiliate model

### Nice to Have (P2)
- Email signup CTA within "Coming Soon" section for launch notifications
- Localized "Coming Soon" copy for Indian-American cultural moments (e.g. "before Diwali 2026")

---

## 5. UX Requirements

### Hero Section
- Headline must lead with action verb "Discover" — discovery is the product
- Subheadline should list the three main verticals (baby, home, fashion) and end on a trust signal
- Trust badges remain unchanged (GOTS Certified, Quality Verified, Made in India)
- Primary CTA visually dominant, linking to /brands

### "Coming Soon" Section
- Positioned below FeaturedBrandPartners, above TrustAssurance
- Background: warm off-white (#fdf8f4) to differentiate from white brand/category sections
- 4 cards in a 2×2 grid on mobile, 4-column row on desktop
- Each card: icon + title + 1-sentence description + "Coming Soon" badge (amber/warm color)
- Footer note in small italic text — honest, not apologetic

---

## 6. Copy Changes

| Location | Element | Old Copy | New Copy |
|----------|---------|----------|----------|
| en.json | `SectionMelaHero.heroHeadline` | "Sustainable Indian Design for Growing Families" | "Discover Quality Indian Brands for Your Family" |
| en.json | `SectionMelaHero.heroSubheadline` | "Discover premium organic clothing and accessories from innovative Indian designers. GOTS certified quality, traditional craftsmanship, delivered worldwide." | "Handpicked baby, home, and fashion brands from India — quality-verified, culturally rooted, delivered to your door." |
| en.json | `SectionMelaHero.shopNow` | "Shop Now" | "Explore Brands" |
| en.json | `SectionMelaHero.viewCategories` | "View Categories" | "Browse Categories" |
| en.json | `FeaturedBrandPartners.subtitle` | "Discover premium brands that meet our strict quality and safety standards" | "We vet every Indian brand so you don't have to — quality, safety, and cultural craft, all in one place." |
| MelaHomePage.js | `pageDescription` | "Discover GOTS certified organic baby clothes..." | "Mela curates the best Indian baby, fashion, and home brands for families in the US. Discover quality-verified brands, explore products, and shop directly on brand stores." |

---

## 7. Acceptance Criteria

- [ ] Hero headline reads "Discover Quality Indian Brands for Your Family"
- [ ] Hero subheadline references baby, home, and fashion verticals
- [ ] "Explore Brands" CTA navigates to `/brands`
- [ ] "Browse Categories" CTA navigates to `/categories`
- [ ] FeaturedBrandPartners subtitle reflects curation-as-value-prop
- [ ] ComingSoonSection renders between FeaturedBrandPartners and TrustAssurance
- [ ] All 4 feature cards display with icon, title, description, and "Coming Soon" badge
- [ ] Footer note is visible on mobile and desktop
- [ ] No regressions in existing sections (SavedItems, CategoryShowcase, TrustAssurance)
- [ ] Page meta description reflects discovery positioning

---

## 8. Success Metrics & Measurement

| Metric | Baseline | Target | How to Measure |
|--------|----------|--------|----------------|
| BrandsPage CTR from homepage | TBD | +20% | Analytics: homepage → brands click events |
| Homepage bounce rate | TBD | -10% | Analytics: session bounce rate on `/` |
| Time on homepage | TBD | +15% | Analytics: avg. session duration on `/` |
| Hero CTA click rate | TBD | Track | Click event on "Explore Brands" button |

---

## 9. Dependencies & Risks

- **BrandsPage must be live and functional** before changing the primary CTA to link there
- Sharetribe Flex routing: confirm `BrandsPage` named route exists in `routeConfiguration.js`
- No backend changes required — all changes are frontend copy and component additions

---

## 10. Out of Scope / Future Considerations

- Actual checkout integration (separate initiative)
- Community reviews system
- Order tracking infrastructure
- Wishlist/gift registry feature
- Email notification system for roadmap updates
