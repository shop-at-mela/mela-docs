# BrandHeroCard — web-client PRD (new session)

**Status:** ✅ Shipped (2026-07-25). Self-contained for a fresh session.
**Scope:** web-client only (the React/Redux/Sharetribe app). Backend/data path is separate
(see "Dependency" below).
**Companion doc:** `mela-docs/product/prds/brand-hero-image-calibration.md` — the rubric and
all architecture decisions that produced this PRD (read §1a, §4, §7, §8, §9 for context).

---

## 1. Goal

Add an **image-forward** brand card for the homepage hero surface: a single large product
"hero image" with the brand's name/tagline overlaid, instead of the current logo + 2×2
product-grid treatment. The image is chosen at render time by **randomly picking one index**
from parallel Sharetribe profile arrays (2–3 pre-vetted heroes written upstream by the sharp
scorer) and resolving that index to a URL with a **Sharetribe-first, Shopify-fallback** rule:
prefer the Sharetribe-hosted image (`brandHeroImageIds[i]`); if it can't be resolved, fall back
to the Shopify URL at the same index (`brandHeroImages[i]`). See §3.

## 2. Non-goals / out of scope

- **No image scoring or selection logic in web-client.** The 2–3 vetted image references are
  already on `publicData.brandHeroImageIds`/`brandHeroImageListingIds` (written by the
  product-listing-integration pipeline). This component is a **reader** — its only "selection"
  is a random pick among the supplied
  array (see §4).
- **Do NOT modify `BrandCardHome.js` or its CSS.** It is shared by HeroSection,
  FeaturedBrandPartners, BrandsPage, and PartnerCTACard — changing it ripples into all four.
  Build a **new** component instead.
- No changes to the scraper, `shopify_brands.py`, or Sharetribe seeding (separate track).

## 3. Dependency (must be true for this to render anything)

Brand users in the target Sharetribe env carry these `publicData` fields (already **live in
dev** for 17 brands, pushed by `product-listing-integration/scripts/update-brand-hero-image.js`;
calibration §8.3). All are **parallel arrays** of length 2–3, **same index = same hero**:

- **`brandHeroImageIds`** — Sharetribe **image UUIDs** (preferred source).
- **`brandHeroImageListingIds`** — the Sharetribe **listing UUID** each image belongs to
  (needed to fetch/resolve the image).
- **`brandHeroImages`** — Shopify CDN URLs (the **runtime fallback**, same index).

**Render path — Sharetribe-first, Shopify-fallback (both verified to exist):** pick a random
index `i`, then:
1. **Prefer Sharetribe:** if `brandHeroImageIds[i]` and `brandHeroImageListingIds[i]` are
   present, fetch listing `brandHeroImageListingIds[i]` with `include:['images']` + the needed
   `fields.image` variants, find the image whose id === `brandHeroImageIds[i]`, and render
   `image.attributes.variants.<name>.url` (a stable `sharetribe.imgix.net` URL — Mela-controlled,
   imgix-optimized, consistent with the rest of the app). Piggyback on the brand page's existing
   listing fetches where possible.
2. **Fall back to Shopify:** if there's no id at index `i`, or the listing/image lookup fails or
   returns nothing, render `brandHeroImages[i]` (the raw Shopify CDN URL) directly.

This fallback also covers the **manual-entry case** (e.g. The Nesavu's hand-added offline image
in `shopify_brands.py`, which may have a URL but no Sharetribe image id) — it still renders via
the Shopify/manual URL. Treat the two arrays as index-aligned; if one is shorter, guard by index.

The web-client work can be built/unit-tested against fixtures **in parallel**. Optional audit
field: `data/hero-scores.json` (pipeline-side, not in publicData).

## 4. Component spec — `BrandHeroCard`

New component: `web-client/src/components/BrandHeroCard/` (`.js`, `.module.css`, `.test.js`),
exported via `components/index.js`.

**Props (mirror BrandCardHome where sensible):** `brand` (the brand user resource, with
`attributes.profile.{displayName, bio, publicData}`), plus whatever the hero slide needs for
the link target (brand slug/URL). Keep the prop shape close to BrandCardHome so it drops into
the same carousel slot.

**Reader contract & empty-state (decided):**
- **Randomly picks one index** across the parallel hero arrays (see §3), once per mount
  (`useMemo`/`useState` initializer) so the image is stable within a session and doesn't
  reshuffle on re-render; a fresh pick on the next page load is the intended variety.
- **Resolve with fallback (§3):** prefer `brandHeroImageIds[i]` → Sharetribe variant URL; if
  that id is absent or fails to resolve, use `brandHeroImages[i]` (Shopify URL). Never let a
  single failed resolution blank the slide when a fallback URL exists.
- **Skip-if-empty:** render **nothing** (return `null`) only when the brand has **no hero
  source at all** — i.e. both `brandHeroImageIds` and `brandHeroImages` are null/absent/empty.
  Do **not** fall back to logo/`profileImage`. A hero surface shows only brands with a real
  hero image; a brand without one is omitted.
- Consumers must also **filter these brands out of the carousel list** so there are no empty
  slides / dead dots (see §5).

**Visual spec:**
- **Aspect ratio: 1:1 square**, `object-fit: cover` (matches the catalog's dominant shape and
  BrandCardHome's existing `aspect-ratio: 1` tiles; minimizes crop — see calibration §3).
- **Text overlay:** brand name and/or tagline (first sentence of `bio`, same derivation
  BrandCardHome uses) over the image.
- **Gradient scrim:** a bottom-up dark gradient behind the text so **fixed white text** meets
  WCAG AA (≥4.5:1) over any image. The scrim is what makes contrast a non-issue regardless of
  the underlying photo (calibration §7.5).
- Keep the brand logo + craft-origin cue if they fit the image-forward layout; the hero image
  is the dominant element, not the 2×2 product grid.
- Theme-aware, responsive; reuse existing design tokens/CSS vars from BrandCardHome's module
  for consistency (copy the values; do not import/modify that file).

> Recommended first step in the new session: run the **`mockup`** skill to produce a visual
> for BrandHeroCard (image + scrim + overlaid name/tagline) before coding, then the
> **`ux-design`**/**`dev-lead`** skills to review. The 1:1 + scrim + white-text direction is
> decided; polish (type scale, logo placement, hover) is open.

## 5. Where it's used — HeroSection

`web-client/src/containers/MelaHomePage/sections/HeroSection/HeroSection.js` renders brands in
an auto-advancing carousel: `BrandCardHome` sits inside `.brandSlide` within `.brandCarousel`
(around line 284), driven by a `brandsWithProducts` list with per-slide dots/controls.

- **Swap** `BrandCardHome` for `BrandHeroCard` **in HeroSection only** (`showCta={false}`
  context). Leave BrandCardHome in FeaturedBrandPartners, BrandsPage, PartnerCTACard untouched.
- **Filter the carousel list** to brands with **at least one hero source** — i.e.
  `brandHeroImageIds` OR `brandHeroImages` is a non-empty array — so skip-if-empty never yields
  an empty slide or an orphaned carousel dot. Do this where the slide list is built (the
  `brandsWithProducts` derivation), not inside the card.
- **Curated-order interaction (flag for review):** brands with no hero image drop out of the
  hero — including, today, brands like The Nesavu (watermark-blocked) and Masilo (no source
  data), which are **first-fold** in the curated order (`configBrands.js`
  `CURATED_BRAND_SLUG_ORDER`, and `homepage-hero-prd.md` §12A.1). The carousel should keep the
  curated order for the brands that remain; note in the PR that first-fold coverage shrinks
  until those brands get images, so the curated order can be re-checked.

## 6. Acceptance criteria

1. `BrandHeroCard` renders a 1:1 image at a randomly-picked index (stable within a mount) with
   a bottom scrim and white brand name/tagline overlay meeting WCAG AA contrast — resolving
   `brandHeroImageIds[i]` to a Sharetribe variant URL, **falling back to `brandHeroImages[i]`**
   when the id is absent or fails to resolve.
2. When the brand has **no hero source** (both `brandHeroImageIds` and `brandHeroImages`
   empty/absent/malformed), `BrandHeroCard` renders `null` (no logo fallback).
3. HeroSection shows `BrandHeroCard` slides; brands with no hero source are absent from the
   carousel (no empty slides, no dead dots), and remaining brands keep curated order.
4. `BrandCardHome` and its four consumers are unchanged (diff touches only the HeroSection
   usage + the new component + barrel export).
5. Carousel a11y preserved (pause/play, dot count matches visible slides — WCAG 2.2.2).
6. Unit tests: `BrandHeroCard.test.js` — resolves+renders a Sharetribe id; **falls back to the
   Shopify URL when id resolution fails or is absent**; renders null when no source at all;
   picks an index — plus an updated `HeroSection.test.js` (filters out brands with no hero source).

## 7. Verification

Use the **`verify`** / **`run`** skills to drive the homepage hero in the real app with a dev
brand that has a non-empty `brandHeroImageIds` array and one that doesn't; confirm the first
renders an image-forward slide (and that reloading can surface a different image from the
array) and the second is absent from the carousel. Then `dev-lead` to check acceptance
criteria.

---

## Appendix — key files

- New: `web-client/src/components/BrandHeroCard/{BrandHeroCard.js,.module.css,.test.js}`
- Edit: `web-client/src/components/index.js` (export), `HeroSection.js` (swap + filter),
  `HeroSection.test.js`
- Reference only (DO NOT EDIT): `web-client/src/components/BrandCardHome/BrandCardHome.js` +
  `.module.css` (copy patterns/tokens), `web-client/src/config/configBrands.js` (curated order)
- Data fields (parallel, index-aligned, 2–3 each): `publicData.brandHeroImageIds` +
  `brandHeroImageListingIds` (Sharetribe UUIDs, **preferred**); `publicData.brandHeroImages`
  (Shopify URLs, **runtime fallback**). Audit lives pipeline-side in
  `product-listing-integration/data/hero-scores.json`.
