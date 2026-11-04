# Mela UX Patterns

Source of truth for recurring UI decisions. `/ux-design` reads this file first and appends to it after every panel or review that settles a decision.

**Entry format:** Rule, Why, Applies to, Web-client components (paths under `web-client/src/`), Decided (date and source), Status (`Adopted` | `Proposed` | `Inconsistent`).

Verify component paths and CSS values against the code before relying on them. Code wins; fix the entry.

---

## P-001 On-image label (tile photos)

**Rule:** Label text is always present, in a compact white chip, bottom-left of the photo, 8px inset. 12px bold, `5px 8px` padding, 8px radius, brand navy text, with a trailing `›` as the tap cue. An optional second line (subtitle) sits inside the chip.
**Why:** The photo is the product, so the label must not cover it. A chip uses less photo than a full-width scrim at 137px mobile tile width. Navy on white is a fixed contrast pair, so contrast does not depend on the photo.
**Applies to:** Photo-led navigation tiles (occasions, and any future category or collection tiles).
**Web-client components:**
- `containers/MelaHomePage/sections/CategoryShowcase/CategoryShowcase.js` (`OccasionMosaic`)
- `.mosaicLabel`, `.mosaicLabelText`, `.mosaicSubtitle` in `CategoryShowcase.module.css`
**Decided:** 2026-11-04, ux-design review of the occasion mosaic.
**Status:** Adopted for the mosaic. **Inconsistent** with P-002 and P-003 below (three different on-image treatments exist).

## P-002 On-image text over a scrim (story and editorial cards)

**Rule:** White text over a bottom gradient scrim, used where the card carries a title plus a sentence of story. White text only, never tinted (tinted marigold measured 2.7-3.2:1 and failed AA).
**Why:** Story cards need room for 2-3 lines, which a chip cannot hold.
**Applies to:** Editorial and brand-story cards.
**Web-client components:**
- `components/OccasionCard/` (`.scrim`: `linear-gradient(to top, rgba(0,0,0,.4), rgba(0,0,0,.02) 65%)`, `.etext`, `.title`, `.story`)
- `components/BrandHeroCard/` (`.overlay`, `.eyebrow`; contrast rationale is in its CSS comment)
**Decided:** Pre-existing (brand-hero-image-calibration PRD, decision #4). Recorded here 2026-11-04.
**Status:** Adopted.

## P-003 Index chip on image (brand initial or number)

**Rule:** A 34px solid navy square chip, top-left, 10px inset, with one display-font character.
**Applies to:** Brand photo cards in "Every Brand Earned Its Place".
**Web-client components:** `components/BrandPhotoCard/` (`.chip`), used by `containers/MelaHomePage/sections/EarnedItsPlace/EarnedItsPlace.js`.
**Decided:** Pre-existing. Recorded here 2026-11-04.
**Status:** Adopted. Different job from P-001 (identifies, does not label), so it is not a conflict, but keep it off tiles that use P-001.

## P-004 Overlay position map (so overlays never collide)

| Corner | Used for | Component |
|---|---|---|
| Top-left | Index chip | `BrandPhotoCard` |
| Bottom-left | Tile label chip, scrim text | `OccasionMosaic`, `OccasionCard`, `BrandHeroCard` |
| Bottom-right | Save heart | `ListingCard` (`.saveButton`), via `SavedListingButton` |

**Rule:** One overlay per corner. A new overlay takes a free corner or goes in a separate decision here first.

## P-005 Photo-led tile size and ratio

**Rule:** Portrait 4:5 tiles. Mobile: snap-scroll strip, 44% tile width. 768px and up: grid with columns equal to the tile count (max 4), row height `clamp(300px, 28vw, 400px)`.
**Why:** Portrait crops show apparel and kids' products; a fixed row height removes layout shift between loading and loaded.
**Applies to:** Occasion mosaic. Product cards use their own ratios (4:5, 3:4 at small widths).
**Web-client components:** `.mosaic`, `.mosaicTile` in `CategoryShowcase.module.css`; `ListingCard.module.css` (`aspect-ratio: 4 / 5`).
**Decided:** 2026-11-04.
**Status:** Adopted. Larger-than-this was considered and not adopted; revisit with click data.

## P-006 One category-navigation row per page

**Rule:** The homepage has one row of top-category links, the hero pills. Do not add a second row of the same destinations.
**Hero pills:** wrap at all widths (no sideways scroll, because hidden pills on mobile are undiscoverable). Pill style: tinted navy 5% background, 1px navy 15% border, 20px radius, icon plus label.
**Web-client components:**
- `containers/MelaHomePage/sections/HeroSection/HeroSection.js` (`TOP_CATEGORY_PILLS`) and `HeroSection.module.css` (`.categoryPill`)
- `components/CategoryIcon/`
- `components/CategoryChips/` is retained but unused on the homepage. Delete it or reuse it deliberately.
**Decided:** 2026-11-04.
**Status:** Adopted.

## Open consistency items

- Three on-image label treatments (P-001/P-002/P-003). Decide whether `OccasionCard` (already scrim-based, and a candidate for tile use) should adopt P-001 when it has no story text.
- Overlay values (8px inset, 12px radius, chip padding) are literals in CSS. Candidate for shared CSS variables.
