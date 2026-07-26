# Homepage Editorial Modules (P1.3)

Created 2026‑07‑26 for `storefront-validation-readiness-prd.md` P1.3. Concepts, revised section order, and content sourcing for the homepage carousel consolidation. Mobile is the primary design surface; the companion mockup is `nimbalyst-local/mockups/homepage-editorial-modules-mobile.mockup.html`.

## The problem being solved

The homepage today runs eight near identical product carousels between the hero and the vetting story. The F‑001 complaint ("a wall of listings, no inspiration") survives directly below a curation first hero, and the strongest hypothesis evidence sits 7,500px down. The fix is not more products arranged differently. It is fewer product rows, interleaved with modules that only a curator could publish.

**Design principle:** every editorial module must run off data we already have. No CMS, no weekly content operations. Curation that maintains itself.

***

## Revised section order

| # | Section | Status | Notes |
|---|---------|--------|-------|
| 1 | Hero | keep | New positioning copy per `positioning-copy.md` |
| 2 | **Vetting strip** | new (P0.1) | One row: "19 brands · hand vetted · ship to all 50 states · US cards verified", anchor link to vetting section |
| 3 | **Brand Spotlight** | new editorial | See module A |
| 4 | Shop by Occasion | keep, move up | Strongest existing curation; was buried mid page |
| 5 | Category row: Fashion | keep | One of two surviving product carousels |
| 6 | Category row: Baby & Kids | keep | Second surviving carousel |
| 7 | **New from India** | new editorial | See module B |
| 8 | **Craft Stories strip** | new editorial | See module C |
| 9 | Brand cards + Explore All 19 Brands | keep | Existing |
| 10 | Every Brand Earned Its Place + How We Vet | keep | Now reachable far sooner |
| 11 | Shipping and payment FAQ, help, footer | keep | Footer copy per P0.2 |

**Removed:** Home & Kitchen carousel, Beauty & Wellness carousel (both reachable from category chips in the hero and View All Categories), the entire "Shop Baby by Age" block (Newborn, 6 to 12 months, etc.), which is a family era relic that contradicts the resolved positioning; it moves to the Baby & Kids category page where it belongs. Net effect: eight product carousels become two, and page length drops well past the 25% target.

***

## Module A: Brand Spotlight

**The pitch:** one brand, treated the way a magazine would treat it. This is the homepage's proof that Mela knows its brands rather than merely listing them.

**Composition (mobile order):**
1. Label: OUR BRANDS, WORTH KNOWING (marigold overline)
2. Banner image (first entry of the brand's `brandHeroImages`) with the Made in India chip
3. Brand name + craft chip (`publicData.brandCraft`)
4. One story sentence (first sentence of bio after the tagline)
5. Three featured products (existing hero listing data)
6. One action: "Explore {Brand} →" (brand page on Mela). No outbound link in the module (decision 2026‑07‑26: outbound happens at purchase intent only, via the listing level redirect flow)

**Rotation:** deterministic weekly rotation through the five flagships (week number modulo five). No CMS, no scheduling work, and returning visitors see a fresh brand.

**Data:** everything already seeded: `brandHeroImages`, `brandCraft`, bio, `brandStoreUrl`, hero listing IDs from `configBrands.js`.

## Module B: New from India

**The pitch:** recency as curation. Answers "why come back?", which no current module does.

**Composition:** section heading "New from India", one line of context ("Fresh arrivals from the brands we vet"), horizontal row of the 8 most recent listings across all categories, sorted by `createdAt`, capped at 2 per brand so one ingestion run cannot flood the row.

**Data:** listing `createdAt` plus the per brand cap. Entirely automatic.

## Module C: Craft Stories strip

**The pitch:** the craft chips we just wrote for all 19 brands, used as a discovery surface. Three tiles, each pairing a craft with its place, linking to the brand page. This is the module Amazon structurally cannot publish.

**Composition:** heading "The Crafts Behind the Brands", three tiles (image from the brand's `brandHeroImages`, craft line as tile text, brand name as attribution). Rotates a different trio daily (day of year modulo the eligible set), drawn from active brands with both a craft chip and hero images.

**Examples with today's data:** "Lucknow chikankari embroidered by hand" (House of Chikankari) · "Juttis and kolhapuris stitched by hand in Mumbai" (Fizzy Goblet) · "Ceramics painted by hand in Delhi" (Kaunteya).

**Data:** `brandCraft` + `brandHeroImages`, both live on dev as of today.

***

## Measurement (extends P0.6)

New events: `spotlight_view`, `spotlight_brand_click`, `new_from_india_click`, `craft_tile_click`. Success signal: sessions touching an editorial module should over index on downstream product level outbound (the redirect flow) relative to sessions that only touch the surviving category carousels. If editorial touched sessions convert to intent at a higher rate, the curation thesis is validated with data.

## Build notes

1. All three modules are read only compositions of existing components (ListingCard, BrandCardHome patterns, occasion panel styling) plus the seeded publicData fields. No new backend.
2. Rotation logic is pure frontend arithmetic on date; no persistence.
3. Mobile first per house rule; the mockup defines the mobile layout, desktop adapts to two or three column arrangements of the same blocks.
4. The removed "Shop Baby by Age" block should land on the Baby & Kids category page in the same release so no capability is lost, only relocated.
