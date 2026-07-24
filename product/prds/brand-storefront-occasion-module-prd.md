# Brand Storefront Occasion Module PRD

**Feature:** "Shop by Occasion" module on individual brand storefronts
**Status:** 🟡 Partial — UI shipped, analytics instrumentation pending
**Priority:** Medium — discovery-layer enhancement, not a conversion blocker
**Owner:** PM + Developer
**Created:** July 2026
**Last Updated:** July 2026 — UI/functional acceptance criteria shipped in `f721dad6f` (module + storefront ListingCard badge consistency fix). Analytics events not yet implemented.

---

## Executive Summary

**Feature**: Add a "Shop by Occasion" module to the brand storefront (`/brands/:brandSlug`) that surfaces the *current brand's own* Diwali & Festivals and Gifting inventory, when they have enough of it to show.
**Target URL / Entry Point**: `/brands/:brandSlug` (Products tab), between Featured Products and the full product grid — `src/containers/ProfilePage/BrandStorefront.js`
**Target Users**: Priya (occasion-led, mixed-heritage) and Neha (occasion-led, first-gen) primarily — both are documented as occasion-driven shoppers in `buyer-personas.md`. Sarah and Arun are secondary beneficiaries.
**Business Objective**: Increase products-per-session and click-through on brand storefronts by giving occasion-motivated visitors a fast, brand-scoped path to relevant inventory instead of forcing them back to global search.
**Primary Success Metrics**:
- Occasion module CTA click-through rate (clicks / module impressions): target ≥8%
- Product click-through rate from occasion module vs. from the general product grid, on the same storefront visit

---

## 1. Problem Statement

### Current State
- `occasion` (`diwali-festivals` | `gifting`) is already a real, indexed Sharetribe listing field (`src/config/configListing.js`) that brands tag their products with.
- A "Shop by Occasion" module (`OccasionStrip`, in `CategoryShowcase.js`) already exists and renders on the homepage and on `/categories`, scoped to category. It fetches its own data via a standalone SDK client call.
- The brand storefront (`/brands/:brandSlug`) has no occasion module today. A visitor who lands on a brand page during Diwali shopping, or specifically looking for a gift, must scroll the full product grid (or leave and use global search) to find relevant items — even when the brand has curated, tagged inventory for exactly that occasion.

### User Pain Points
- Priya's stated shopping trigger is occasion, not product type (`buyer-personas.md`, "Shopping trigger" row) — she's the least served by an undifferentiated product grid.
- Neha is described as most loyalty-building when supported with "occasion-based browsing" during inspiration mode (`buyer-personas.md` L281) — a brand storefront with no occasion cue misses that moment.
- `buyer-personas.md` L511 names "shop by occasion" explicitly as one of the discovery surfaces "where Mela wins" — currently that only exists on the homepage and category pages, not on brand storefronts, which is where a user often lands next after discovering a brand through one of those surfaces.

### Business Impact of Inaction
- Occasion-tagged inventory a brand has curated stays buried in an undifferentiated grid on their own storefront — undermining the brand's own merchandising effort.
- Missed opportunity to reinforce Diwali/gifting intent at the exact moment a user is already engaged with one brand (highest-intent point in the funnel), rather than only at the generic homepage/category level.

---

## 2. Goals & Non-Goals

### Goals
- Show a brand-scoped "Shop by Occasion" module on the Products tab of the brand storefront when that brand has ≥2 products tagged for a given occasion.
- Reuse the existing `occasion` visual language (panel design, copy, seasonal Diwali/Gifting ordering) from `OccasionStrip` so the pattern is recognizable across the site.
- Source data from the storefront's already-loaded `listings` prop — no new network fetch.

### Non-Goals
- Changing the `occasion` enum (still just `diwali-festivals` and `gifting` — no new occasions introduced by this feature).
- Adding an occasion module to the `/brands` directory page (out of scope — directory lists many brands, "occasion inventory from the brand" doesn't apply there; scoped explicitly to the single-brand storefront per stakeholder decision).
- Adding occasion filtering/tabs to the main product grid itself.
- A new Redux duck or SDK fetch — this reuses data already loaded by `ProfilePage.duck.js`'s `queryUserListings`.
- Retrofitting `OccasionStrip` itself to accept a "filter from props instead of fetch" mode (see Dev Lead architecture doc for why this is a new lightweight component, not an `OccasionStrip` extension).

---

## 3. User Stories

| As a... | I want to... | So that... | Priority |
|---------|-------------|------------|----------|
| Priya, browsing a brand storefront during Diwali season | See this brand's Diwali & Festivals picks without scrolling their whole catalog | I can quickly find something appropriate for the occasion I'm shopping for | P0 |
| Neha, gifting for a baby shower | See this brand's Gifting picks on their storefront | I don't have to guess which of the brand's products are gift-appropriate | P0 |
| A brand with no occasion-tagged inventory | Not see an empty or broken "Shop by Occasion" module | The storefront doesn't look unfinished or broken | P0 |
| A brand owner viewing their own storefront | See the same occasion module a visitor would see | I understand how my occasion-tagged products are being merchandised | P2 |

---

## 4. Feature Requirements

### Must Have (P0)
- Module renders only on the Products tab, positioned between "Featured Products" and "All Products" grid.
- Module renders per-occasion panels (Diwali & Festivals, Gifting), each showing up to 6 of the brand's own matching products.
- A panel is hidden if the brand has fewer than 2 products tagged with that occasion.
- The entire module is hidden if neither occasion panel qualifies (no empty-state UI — this is a bonus discovery module, not a core page section).
- Each panel has a CTA linking to `SearchPage` filtered by both this brand and the occasion (`?pub_occasion=has_any:<option>&<brand filter>`), so "view more" leads to a complete, correctly-scoped result set even beyond the 6 shown.
- Seasonal ordering matches the existing pattern: Diwali & Festivals first Oct 1–Nov 15, Gifting first the rest of the year.
- No additional network request — sourced from the `listings` array already passed into `BrandStorefront`.

### Should Have (P1)
- Visual consistency with `OccasionStrip`'s panel styling (festive/gifting color themes) so the pattern reads as the same feature across the site.

### Nice to Have (P2)
- Loading placeholder — likely unnecessary since data is synchronous (already-loaded props), but confirm with dev lead whether `listings` can arrive after initial render on this page (pagination/async listing loads) and needs a loading state.

---

## 5. UX Requirements

**Key flow**: Visitor lands on `/brands/:brandSlug` → Products tab (default) → scrolls past Featured Products → sees "Shop by Occasion" panel(s) for this brand only (if qualifying) → clicks a product or the panel CTA → lands on a pre-filtered `SearchPage` scoped to this brand + occasion.

**Edge cases**:
- Brand has 0 occasion-tagged products → module doesn't render at all (no heading, no empty state).
- Brand has 1 product tagged `gifting`, 0 tagged `diwali-festivals` → module doesn't render (below 2-item threshold for the only qualifying occasion... wait — if only 1 occasion has ≥2, that single panel should still show). *Clarify: module renders if **at least one** panel qualifies; only qualifying panels show.*
- Brand has exactly 2 products tagged for an occasion → panel shows both, no "view more" needed beyond the CTA.
- Own-profile view (`isOwnProfile`) → same rendering as any visitor; no owner-specific placeholder (unlike the other `BrandDataPlaceholder` sections) since this is inventory-driven, not a data-entry field a brand owner fills in directly.
- Mobile (≤768px) → panels stack vertically, matching `OccasionStrip`'s existing responsive behavior on `/categories`.

---

## 6. Acceptance Criteria

- [x] On a brand storefront where the brand has ≥2 products tagged `diwali-festivals`, the Diwali & Festivals panel renders with those products (up to 6) between Featured Products and All Products.
- [x] On a brand storefront where the brand has ≥2 products tagged `gifting`, the Gifting panel renders similarly.
- [x] On a brand storefront where the brand has <2 products for both occasions, no "Shop by Occasion" heading or module renders at all.
- [x] On a brand storefront where only one occasion qualifies, only that one panel renders (not both, not neither).
- [x] Panel CTA link navigates to `SearchPage` with both the occasion filter (`pub_occasion=has_any:<option>`) and a filter scoped to this brand's products only.
- [x] Module does not fire any additional API/SDK request beyond what `BrandStorefront` already receives via props.
- [x] Diwali & Festivals panel is ordered first when today's date is Oct 1–Nov 15; Gifting first otherwise.
- [x] Renders correctly at 375px width (mobile) with panels stacked, matching existing `OccasionStrip` mobile behavior.
- [x] About tab is unaffected — module only appears under the Products tab.

---

## 7. Success Metrics & Measurement

- **Primary**: Module CTA click-through rate (occasion panel CTA clicks ÷ module impressions).
- **Secondary**: Product-card click-through rate within the occasion module vs. the general product grid, same session — tells us whether occasion-scoped merchandising outperforms the undifferentiated grid.
- **Guardrail**: No increase in storefront page load time (module must not introduce a new network waterfall).
- **Analytics events needed**: `occasion_module_impression` (brand id, occasion, panel position), `occasion_module_cta_click` (brand id, occasion), `occasion_module_product_click` (brand id, occasion, listing id) — confirm existing analytics event naming convention with dev lead before implementation.

---

## 8. Dependencies & Risks

- **Depends on**: Brands actually tagging inventory with `occasion` in their listing publicData. If adoption is low, most storefronts simply won't show the module (acceptable — it's additive, not required).
- **Risk**: If `listings` passed to `BrandStorefront` is ever paginated/incomplete (not the full brand catalog), the occasion filter could under-count a brand's true occasion inventory. Dev lead to confirm `queryUserListings` always loads the full set before this ships.
- **Sharetribe constraint**: None new — reuses the existing `occasion` listing field already configured in Sharetribe Console.

---

## 9. Out of Scope / Future Considerations

- Occasion module on the `/brands` directory page (cross-brand, not brand-scoped) — separate PRD if prioritized later.
- Additional occasion values beyond Diwali & Festivals / Gifting.
- Brand-owner controls to manually curate/reorder which products appear in their occasion panels (currently fully derived from listing tags).
