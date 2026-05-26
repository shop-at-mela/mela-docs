# Mela Project Roadmap & Task List

**Last Updated:** 2026-04-11

This document tracks active projects, planned initiatives, and completed work across the Mela platform.

## 🚀 Pre-Production Blockers (Ship These First)

### 🔴 P0 — Launch Blockers

#### A. Footer Legalese (Terms of Service + Privacy Policy)
**Status:** Blocked on legal copy
**Owner:** PM (copy) → Developer (footer config in Sharetribe Console)
**PRD:** [footer-legalese-prd.md](./product/prds/footer-legalese-prd.md)

**Key constraint:** Mela is operated under personal name (no LLC, no business entity — H-1B visa restriction). ToS must reflect individual operator, no affiliate income, curated directory model.

**Tasks:**
- [ ] Generate ToS using `legal/terms-of-service-prompt.md` via Termly.io or ChatGPT (~1–2 hrs)
- [ ] Generate Privacy Policy using `legal/privacy-policy-prompt.md` via Termly.io (~30 min)
- [ ] Manually review both: remove any affiliate disclosure, entity/company references, or retailer language
- [ ] Add content to `/terms-of-service` and `/privacy-policy` CMS pages in Sharetribe Console
- [ ] Configure footer links in Sharetribe Console (Legal column)
- [ ] Add copyright + platform disclaimer to footer slogan field
- [ ] Confirm privacy@[domain] email is live

#### B. Sitemap & robots.txt Production Readiness
**Status:** Ready for development
**Owner:** Developer
**PRD:** [sitemap-prd.md](./technical/sitemap-prd.md)

**Tasks:**
- [ ] Fix `robots.txt` placeholder domain (`my.marketplace.com` → production domain)
- [ ] Add `/brands` and `/categories` to `sitemap-default.xml`
- [ ] Enumerate all category paths into `sitemap-default.xml`
- [ ] Build `sitemap-brands.xml` for brand profile pages (`/brands/:brandSlug`, `/u/:id`)
- [ ] Verify all sitemap URLs return 200 after deploy
- [ ] Submit `sitemap-index.xml` to Google Search Console

#### C. Pre-Redirect Sentiment Modal ("Was Mela Helpful?")
**Status:** Ready for development
**Owner:** Developer
**PRD:** [pre-redirect-sentiment-prd.md](./product/prds/pre-redirect-sentiment-prd.md)

**Tasks:**
- [ ] Build `ShopifyRedirectModal` React component
- [ ] Wire modal into `ProductOrderForm.js`, `OrderPanel.js`, `InquiryWithoutPaymentForm.js`
- [ ] Set up Airtable base + Make webhook for event capture
- [ ] Add Hotjar script tag to `public/index.html`
- [ ] Test mobile at 375px
- [ ] Add session deduplication (localStorage per listingId)

---

## 📋 Active Projects

### 🔴 High Priority

#### 0. SEO & AEO — Category Pages + Brand Storefront Pages
**Status:** Draft — Ready for Review
**Owner:** Developer + PM
**PRD:** [seo-aeo-category-brand-pages-prd.md](./product/prds/seo-aeo-category-brand-pages-prd.md)
**Depends on:** Sitemap PRD (Gap 3 & 4) must ship together

**Objective:** Build dedicated `CategoryPage` and `BrandStorefrontPage` React components behind existing routes (`/categories/:L0/:L1` and `/brands/:brandSlug`), with correct Schema.org markup (Organization, BreadcrumbList, CollectionPage, FAQPage) and AEO content blocks to capture organic and AI-engine search traffic.

**Key decisions resolved in PRD:**
- `brand-storefront-prd.md` supersedes UUID-based profile page — canonical URL moves to `/brands/:brandSlug`
- `brands-page-prd.md` scoped to `/brands` directory only (no overlap)
- Current `SearchResultsPage` schema on category/brand routes is incorrect and must be replaced
- Brand slug backfill required for ~10 curated brands before sitemap submission

**P0 Tasks:**
- [ ] Build `CategoryPage` component with editorial block, subcategory pills, product grid, BreadcrumbList + CollectionPage JSON-LD
- [ ] Add `slug` field to all ~10 brand entries in `configBrands.js`
- [ ] Wire `/brands/:brandSlug` route to 301-redirect → `/u/:uuid` (lookup slug→UUID from configBrands)
- [ ] Add `canonicalRootURL` to `ProfilePage.js` for provider users pointing to `/brands/:brandSlug`
- [ ] Replace `SearchResultsPage` schema in `SearchPage.shared.js` isCategoryPage path with correct `CollectionPage` type
- [ ] Coordinate sitemap URL enumeration (per `technical/sitemap-prd.md` Gap 3 & 4)

**P1 Tasks:**
- [ ] FAQ accordion blocks (3–5 Q&As per L0 category, 3 per brand) with `FAQPage` JSON-LD
- [ ] "About" section on brand storefront (crawlable `<p>` tag, not modal)
- [ ] Country of origin + founding year rendered on brand page header
- [ ] Featured brands section at bottom of category pages

**Success Metrics:**
- 📈 Category page organic impressions: 0 → 5,000+ (90 days post-index)
- 📈 Brand page organic impressions: +10,000 (90 days post-index)
- ✅ Google Rich Results Test passes for BreadcrumbList + Organization schemas

---

#### 1. Homepage Discovery Relaunch
**Status:** Ready for development
**Owner:** Developer
**PRD:** [homepage-discovery-relaunch-prd.md](./product/prds/homepage-discovery-relaunch-prd.md)

**Objective:** Reframe homepage as a brand discovery platform (not a checkout store); add "Coming Soon" roadmap section to set expectations and build excitement around end-to-end features.

**Tasks:**
- [ ] Update hero headline, subheadline, and primary CTA copy in `en.json`
- [ ] Update FeaturedBrandPartners subtitle in `en.json`
- [ ] Update MelaHomePage meta description
- [ ] Change primary hero CTA route from SearchPage → BrandsPage in `HeroSection.js`
- [ ] Build `ComingSoonSection` component (4 feature teaser cards)
- [ ] Wire `ComingSoonSection` into `MelaHomePage.js` between FeaturedBrands and TrustAssurance

**Success Metrics:**
- 📈 BrandsPage CTR from homepage +20%
- 📉 Homepage bounce rate -10%
- ⏱️ Time-on-page +15%

---

#### 2. Merchant Policies & Schema.org Enhancement
**Status:** Draft (Planning Complete)
**Owner:** Developer
**Deadline:** 4 weeks (Phased rollout)
**Plan Location:** [merchant-policies-implementation-plan.md](./product/merchant-policies-implementation-plan.md)
**Technical Docs:** [merchant-policies-data-model.md](./technical/merchant-policies-data-model.md)

**Objective:** Add merchant return policies and complete shipping details to product schema for improved Google Rich Results.

**Phases:**
- [ ] **Week 1:** Documentation & Data Model
  - [x] Create implementation plan
  - [x] Create technical data model documentation
  - [ ] Create UI/UX specification document
- [ ] **Week 2:** Backend Implementation
  - [ ] Add `defaultMerchantPolicies.js` config file
  - [ ] Create `merchantPolicyHelpers.js` utilities
  - [ ] Update ListingPage schema.org implementation
- [ ] **Week 3:** UI Component Development
  - [ ] Create `PolicyInformation` component
  - [ ] Create `PolicyAccordion` component
  - [ ] Integrate into OrderPanel
- [ ] **Week 4:** Migration & Testing
  - [ ] Create brand policy migration script
  - [ ] Test with Google Rich Results Test
  - [ ] User acceptance testing

**Success Metrics:**
- ✅ Google Rich Results Test passes with no warnings
- 📈 Improved search snippet display
- 📉 20% reduction in customer policy inquiries
- 🎯 100% brand policy coverage

---

## 🟡 Medium Priority

### SEO & Discovery Optimization
- [x] Item aspects parser integration ([itemAspectsParser-integration-guide.md](./ai-optimization/itemAspectsParser-integration-guide.md))
- [x] Homepage SEO optimization ([seo-optimization-summary.md](./product/homepage/seo-optimization-summary.md))
- [ ] Search page optimization (See [search-page-optimization-prd.md](./product/prds/search-page-optimization-prd.md))
- [ ] AI-ready product discovery (See [ai-ready-product-discovery-prd.md](./product/prds/ai-ready-product-discovery-prd.md))

### Brand Partner Experience
- [ ] Brand storefront implementation (See [brand-storefront-prd.md](./product/prds/brand-storefront-prd.md))
- [ ] Brands page (See [brands-page-prd.md](./product/prds/brands-page-prd.md))
- [ ] Affiliate onboarding improvements ([affiliate-onboarding.md](./strategy/brand-partnerships/affiliate-onboarding.md))
- [ ] Brand partnership landing page v2 ([landing-page-v2.md](./strategy/brand-partnerships/landing-page-v2.md))

---

## 🟢 Low Priority / Future

### Customer Experience
- [ ] Customer acquisition improvements (See [customer-acquisition-prd.md](./product/prds/customer-acquisition-prd.md))
- [ ] Enhanced product recommendations
- [ ] **Saved Items "Meri Pasand"** — heart/save listings, homepage module, `/pasand` page (See [saved-items-pasand-prd.md](./product/prds/saved-items-pasand-prd.md))

### Platform Improvements
- [ ] Remaining AI optimizations ([remaining-improvements-beyond-prompt-engine.md](./ai-optimization/remaining-improvements-beyond-prompt-engine.md))
- [ ] Performance monitoring & optimization
- [ ] Analytics dashboard enhancements

---

## ✅ Recently Completed

### January 2026
- [x] **Availability field fix** - Fixed missing "availability" field in Offer schema (2026-01-28)
- [x] **Merchant policies planning** - Created comprehensive implementation plan and technical docs (2026-01-28)
- [x] **ItemAspectsParser integration** - Enhanced product attribute parsing with benefits
- [x] **Homepage SEO optimization** - Improved structured data and meta descriptions

### Q4 2025
- [x] MVP validation ([mvp-validation-prd.md](./product/prds/mvp-validation-prd.md))
- [x] Category structure optimization ([category-structure-analysis.md](./product-data/category-structure-analysis.md))
- [x] Listing field definitions ([listing-field-definitions.md](./product-data/listing-field-definitions.md))

---

## 📚 Documentation Structure

### Product Documentation (`/product/`)
- PRDs (Product Requirements Documents)
- Implementation plans
- Feature specifications
- UI/UX guidelines

### Technical Documentation (`/technical/`)
- Data models and schemas
- API specifications
- Deployment guides
- Technical architecture

### Strategy Documentation (`/strategy/`)
- Market research
- Partnership strategies
- Growth plans
- Competitive analysis

### Product Data (`/product-data/`)
- Category structures
- Item aspects definitions
- Data analysis and insights

---

## 🎯 Q1 2026 Goals

1. **SEO Excellence**
  - ✅ Fix all Google Rich Results warnings
  - 🔄 Complete merchant policies implementation
  - 📋 Optimize search page for discovery

2. **Brand Partner Growth**
  - 📋 Launch brand storefront pages
  - 📋 Improve onboarding experience
  - 📋 Add policy management tools

3. **Customer Experience**
  - 📋 Enhanced product discovery
  - 📋 Improved search functionality
  - 📋 Better mobile experience

4. **Platform Stability**
  - 📋 Performance optimization
  - 📋 Analytics improvements
  - 📋 Error monitoring

---

## 📝 Notes

- Use this document to track all major initiatives
- Update status weekly
- Link to detailed plans and PRDs
- Archive completed items quarterly
- Keep high-priority items at the top

---

## 🔗 Quick Links

- [MELA_PITCH_DECK.md](./pitch/MELA_PITCH_DECK.md)
- [target-audience-market-research.md](./strategy/target-audience-market-research.md)
- [changelog.md](./technical/changelog/changelog.md)
- [render-deployment-guide.md](./technical/deployment/render-deployment-guide.md)
