# Brand Hero Image — Part 1 Calibration Rubric

**Status:** Draft for human review (2026-07-22). Open questions in §7 have been
**resolved with judgment calls** (bias: easy to execute); they're marked ✅ DECIDED and
are still overridable in review. **Gate:** Part 2 (scoring pipeline +
`update-brand-hero-image.js` write-back) does **not** start until this rubric is signed off.

**Purpose:** Define, from real scraper output, what makes a bestseller product photo
suitable as a homepage brand **hero image** — the image a **new** web-client component
reads from `publicData.brandHeroImage`. This is a *rubric*, not a final brand→image mapping.

> **Architecture correction (2026-07-22):** do **not** modify `BrandCardHome.js`. It is
> shared by HeroSection, FeaturedBrandPartners, BrandsPage, and PartnerCTACard — changing
> its image logic would ripple into all four. Instead, add a **new component** (e.g.
> `BrandHeroCard`) used only where the hero treatment is wanted. `BrandCardHome` stays
> untouched. Scoring lives entirely in product-listing-integration; the new component is a
> pure reader.
>
> **Empty-state contract (2026-07-22):** `BrandHeroCard` **skips the brand entirely when
> `publicData.brandHeroImage` is null/empty** — it does *not* fall back to logo/`profileImage`.
> A hero carousel should show only brands with a strong image; a brand without one is
> omitted, not shown degraded. **Consequence:** brands with no qualifying hero (masilo — no
> CSV; the-nesavu — watermark-blocked, §9; any brand whose candidates all fail the gates)
> drop out of the hero surface, which can pull a *first-fold* brand out of the curated
> order (`homepage-hero-prd.md` §12A.1). Flag those to the reviewer so the curated order can
> be re-checked; they still render normally in the non-hero `BrandCardHome` surfaces.

---

## 1. Scope & method

- **Source:** `Mela-scrapper-integrations/scrapper_csvs/{category}/classified_products_prod/{brand}_classified.csv`,
  read with `csv.DictReader` (column-name access — `isBestseller` sits in different
  positions across files, so positional indexing is unsafe).
- **Qualifier:** a row is a candidate iff `isBestseller == 'True'` **and**
  `Stock Status == 'In Stock'` (exact strings). Empty-string stock = **not** qualifying
  (flagged, not guessed).
- **Images:** `Product Image URL` is a `', '`-delimited list of CDN URLs; split on `', '`.
- **Universe:** only brands live in `web-client/src/config/configBrands.js`
  `brandConfigurations` (dev env — QA is pseudo-production). 19 live brands, mela-admin
  test account excluded. Non-live CSVs present but skipped: malabarbaby, myfirstcrayons,
  tibertaber, chidiyaa, needledust, pastelsandpop, saphed.
- **Sample size:** 3–5 qualifying items per brand (calibration only — not the full set).
- **Categories scanned:** baby_and_kids, fashion, jewelry_and_accessories,
  home_and_kitchen, beauty_and_wellness. (art_and_craft, food_and_gourmet have no data.)

### 1a. Filename → slug mapping (explicit; flags called out)

Filenames do **not** reliably equal slugs — an explicit map was built, not assumed:

| configBrands slug | category (config) | CSV file | Match note |
|---|---|---|---|
| baby-forest | baby_and_kids | baby_forest_products_classified.csv | underscore vs hyphen |
| aagghhoo | baby_and_kids | aagghhoo_products_classified.csv | exact |
| choosekind | baby_and_kids | choosekind_classified.csv | **no `_products`** in name; Brand Name casing varies (`ChooseKind`/`Choosekind`) → matched case-insensitively |
| superbottoms | baby_and_kids | superbottoms_products_classified.csv | exact |
| pluchi | baby_and_kids | pluchi_products_classified.csv **+** pluchi_fashion_products_classified.csv | **MULTI-CSV** (see §2) |
| gullylabs | fashion | gullylabs_products_classified.csv | exact |
| the-nesavu | baby_and_kids | thenesavu_girls_products_classified.csv | slug `the-nesavu` ≠ file `thenesavu_girls` |
| banjaaran-studio | fashion | banjaaranstudio_products_classified.csv | hyphen dropped in file |
| polite-society | fashion | politesociety_products_classified.csv | hyphen dropped |
| vilvah-store | beauty_and_wellness | vilvah_products_classified.csv | file `vilvah`, slug `vilvah-store` |
| the-alternate-india | fashion | thealternate_products_classified.csv | file `thealternate` |
| fizzy-goblet | fashion | fizzygoblet_products_classified.csv | hyphen dropped |
| isharya | jewelry_and_accessories | isharya_products_classified.csv | exact |
| nicobar | fashion | nicobar_products_classified.csv | exact |
| tarinika | jewelry_and_accessories | tarinika_products_classified.csv | exact |
| kaunteya | home_and_kitchen | kaunteya_products_classified.csv (home) **+** (baby) | **MULTI-CSV** (see §2) |
| house-of-chikankari | fashion | houseofchikankari_products_classified.csv | hyphens dropped |
| ankid | baby_and_kids | ankid_products_classified.csv | exact |
| **masilo** | baby_and_kids | — | **NO SOURCE DATA** (see §2) |

> Because filename↔slug is irregular, the Part 2 pipeline **must** carry an explicit
> map (not a `slug→filename` transform) and fail loudly on any unmapped file.

---

## 2. Data-quality & gap report (handled explicitly, never silently)

| Brand | State | Handling |
|---|---|---|
| **masilo** | `NO_SOURCE_DATA` — live in config, no CSV exists yet | Emit explicit "no source data" state; Part 2 leaves `brandHeroImage` unset → `BrandCardHome` falls back to logo/profileImage. Do **not** error the run. |
| **banjaaran-studio** | `FALLBACK_NO_BESTSELLER` — 0 rows with `isBestseller=='True'` (no bestseller collection configured in `shopify_brands.py`); 53 In-Stock rows exist | **Fallback rule applied:** sample from any `In Stock` row. Mark the pick `source: "instock_fallback"` in the audit record so it's visibly weaker than a true bestseller. Better long-term fix: configure a bestseller collection for this brand in `shopify_brands.py`. |
| **choosekind** | 20 rows with **empty** `Stock Status` | Flagged as a data-quality gap in that brand's report; those rows excluded (13 legit qualifiers remain). Do not guess stock. |
| **pluchi** | MULTI-CSV: baby_and_kids + fashion | **Rule applied: use only the CSV whose category == the brand's `configBrands.js` category** (baby_and_kids) — the hero should represent how the brand is positioned on Mela. Pooling across both CSVs is the documented alternative → **§7 open question**. |
| **kaunteya** | MULTI-CSV: home_and_kitchen + baby_and_kids | Same rule → use home_and_kitchen (config category). |

### 2a. Qualifier counts (calibration scan)

```
brand                 status                  qualifying  bestseller_true  empty_stock
masilo                NO_SOURCE_DATA          0
baby-forest           OK                      34          40               0
aagghhoo              OK                      11          17               0
choosekind            OK                      13          13               20  ← flagged
superbottoms          OK                      33          48               0
pluchi                OK (baby CSV only)      951         951              0
gullylabs             OK                      21          22               0
the-nesavu            OK                      749         789              0
banjaaran-studio      FALLBACK_NO_BESTSELLER  0           0                0
polite-society        OK                      22          24               0
vilvah-store          OK                      30          30               0
the-alternate-india   OK                      289         383              0
fizzy-goblet          OK                      67          67               0
isharya               OK                      88          90               0
nicobar               OK                      95          105              0
tarinika              OK                      722         726              0
kaunteya              OK (home CSV only)      29          34               0
house-of-chikankari   OK                      263         263              0
ankid                 OK                      37          40               0
```

---

## 3. Structural finding that shapes everything: almost nothing is native landscape

Pixel dimensions of the sampled candidates:

| Shape | Examples (sampled) |
|---|---|
| **Landscape** (rare) | aagghhoo 2160×1440 & 2880×1920 (3:2 lifestyle flat-lays) |
| **Square 1:1** (most product/studio shots) | tarinika, isharya, kaunteya, fizzy-goblet, vilvah, gullylabs, superbottoms, baby-forest, the-alternate-india |
| **Portrait 4:5 – 2:3** (all on-model shots) | nicobar 1372×1716, house-of-chikankari 1080×1440, the-nesavu 1533×2299, banjaaran 3221×4295, polite-society 2000×3000, ankid, pluchi |

**Implication:** a wide hero slot means **every image gets cropped**, so *where the
negative space and the subject sit* matters more than the raw file. A square studio
shot with the subject centered and white margins (tarinika) crops safely; a full-frame
on-model portrait (the-nesavu) crops badly (decapitation / loss of garment). The rubric
therefore weights **crop-safety + overlay zone** heavily and treats raw aspect ratio as
secondary.

---

## 4. The rubric (objective / testable checklist)

Each criterion is tagged by who can score it:
**[S]** = `sharp` programmatic · **[V]** = vision-model call · **[H]** = human judgment.

> **Gate-priority note (after the §7.5 scrim decision):** because the hero renders with a
> gradient scrim behind fixed white text, the contrast criteria **B2/B3 drop from gates to
> tie-breakers** — a scrim guarantees AA. The dominant gates become, in order: **C** (no
> watermark/promo), **B0** (subject-fill / legibility), **A** (crop-safety). This is what
> the deep-dive in §9 is scored against.

### A. Crop fit — *gate*
- **A1 [S]** Resolution after cropping to the hero target aspect must be ≥ target px on
  both axes (reject upscaling). `sharp.metadata()` → width/height.
- **A2 [S/H]** Subject safe-margin: the salient subject must not run to the frame edges
  on the axis being cropped, or the landscape crop clips it. `sharp` can approximate
  subject center-of-mass via per-tile edge density/variance; edge cases need **[H]**.
- **A3 [S]** Reject aspect ratios that can't reach the hero ratio without >40% content
  loss on the long axis (tall 2:3 portraits are high-risk). Computed from metadata.

### B. Subject-fill & overlay-text zone — *scored*
- **B0 [S] Subject-fill / bounding-box coverage** *(added from the §9 deep-dive).* The
  product/subject should occupy a healthy share of the frame. Penalize (a) tiny centered
  products drowning in white (tarinika solitaire studs) and (b) faceless partial crops
  (nicobar waist-down pants). `sharp`: threshold the background, compute the non-background
  bounding-box area as a fraction of frame; also flag subjects whose box sits entirely in
  the lower/upper edge (partial-crop signal). Higher coverage → better thumbnail legibility.
- **B1 [S]** There exists a contiguous low-detail region (low luminance variance /
  entropy) large enough for a headline, in a predictable zone (top band, or left/right
  third). Tile the image, compute per-tile stdev/entropy via `sharp` region `stats()`.
- **B2 [S]** WCAG AA (≥4.5:1) is achievable in that zone: mean luminance of the zone vs
  the intended overlay text color yields ≥4.5:1. Fully computable once text color is
  fixed (or per-zone light/dark chosen).
- **B3 [S]** Reject "no viable zone": globally high-key (near-white everywhere, e.g.
  vilvah milk-splash) or globally busy (full-frame print, e.g. the-nesavu) — histogram
  from `sharp.stats()`. These need a scrim to carry text, i.e. they fail as-is.

### C. Baked-in text / promo — *gate (disqualifying)*
- **C1 [V]** Watermark / brand-URL overlay anywhere in frame → **disqualify**
  (the-nesavu carries `www.thenesavu.com`). OCR/vision only — `sharp` cannot read text.
- **C2 [V]** Promotional graphics — "SALE", "% OFF", price bursts, festival badges →
  **disqualify**.
- **C3 [V/H]** *Nuance:* product-integral text (a product **label** like vilvah "Milk
  Drops"; an **embroidered brand name** like gullylabs "GULLYLABS") is **not**
  auto-disqualifying, but it competes with the overlay headline → **downgrade**, and let
  a human decide. Vision detects the text; a human/vision classifier decides
  product-integral vs promo.

### D. Background type — *flag, not a gate*
- **D1 [S]** Classify studio/white vs lifestyle: sample corner regions for uniformity +
  high luminance via `sharp`. White-catalog shots score *well* on B (easy contrast) but
  read clinical/off-brand.
- **D2 [H]** Mela's editorial default is bright / warm / lifestyle. Pure clinical
  white-catalog (tarinika, banjaaran fallback) is functional but stylistically off-brand
  → surface the tension (§6), don't silently prefer or reject.

### E. Legibility as a *brand* hero — *human / vision-assisted*
- **E1 [V/H]** At thumbnail scale, is the product/category obvious? Extreme editorial
  crops (isharya ear cuff) fail — you can't tell it's jewelry. Reject for hero use.
- **E2 [S, informational]** Dominant color/tone harmony with Mela palette
  (navy `#2D2D7B`, marigold `#F0A030`): `sharp.stats()` dominant color → distance to
  palette. Informational tie-breaker, not a gate.

> **Do NOT re-derive brand-level India-shout in the image scorer.** `configBrands.js`
> already encodes `BRAND_SCORES` (indiaShout / aspiration / diasporaPull) per brand.
> The hero-image rubric is strictly *image-level suitability* (crop, overlay zone, no
> promo, legibility). Brand identity is an existing constant — keep the two layers
> separate.

---

## 5. Annotated examples (good / borderline / rejected)

11 examples across all 5 populated categories. Coordinates/URLs are the exact sampled
rows (clickable for review).

### ✅ GOOD

**1. aagghhoo — "Happy Jingles – Sensory Baby Toys (Set of 2)"** · baby_and_kids · 2160×1440 (3:2)
[url](https://cdn.shopify.com/s/files/1/0138/1593/9130/products/IMG_6943.jpg?v=1597832196)
Native landscape lifestyle flat-lay; handcrafted patchwork/embroidery = craft India-shout;
generous soft-gray negative space bottom-left → clean dark-text overlay zone (B1/B2 pass).
The rare candidate that needs almost no crop. **Programmatic pass on A, B, D1.**

**2. house-of-chikankari — "HOC Rayon Chikankari Solid Kurta – Black"** · fashion · 1080×1440 (3:4)
[url](https://cdn.shopify.com/s/files/1/0561/7926/1589/files/HOC575_4d706a4b-d12c-4d17-b166-5aed3a63003a.jpg?v=1767871144)
Top-tier: chikankari craft India-shout, warm terracotta backdrop (on-brand editorial),
model with face, strong black-on-peach contrast, clean warm wall = top overlay band.
Portrait → needs a top-crop but the subject sits low enough to survive it.

**3. fizzy-goblet — "Masai Mara : Vegan Sliders"** · fashion · 1024×1024 (1:1)
[url](https://cdn.shopify.com/s/files/1/0274/8586/4013/products/Global-cover-_0002_Fizzy01109.jpg?v=1736745526)
Lifestyle on-foot shot, embroidered detail (craft), warm cream floor for text bottom-right.
Editorial + warm = squarely Mela's default aesthetic.

**4. kaunteya — "Dasara – Coffee Mug"** · home_and_kitchen · 1600×1600 (1:1)
[url](https://cdn.shopify.com/s/files/1/0560/0198/6604/products/01-1_d5e6ce53-3b9c-4adb-a1e9-fbc50326a007.jpg?v=1642073998)
Mughal-miniature motif (gold + turquoise) = unmistakable India-shout; soft gradient
studio background gives a top overlay band. Bright/studio-lit — matches current default.

### ⚠️ BORDERLINE

**5. tarinika — "Zarina CZ Pink Drop Earrings"** · jewelry · 1500×1500 (1:1)
[url](https://cdn.shopify.com/s/files/1/2026/1561/files/TPE0027XPS.jpg?v=1725093955)
Pure white studio, huge negative space → **best-in-class programmatic overlay contrast
(B pass)**, temple-inspired earrings = decent India-shout. *But* clinical catalog look,
product small in frame → weak at thumbnail (borderline E1). Great B/D1 score, off-brand D2.

**6. nicobar — "Mistari Shirt – Charcoal Dot Printed"** · fashion · 1372×1716 (4:5)
[url](https://cdn.shopify.com/s/files/1/0508/8906/4628/files/NBI050109_1.jpg?v=1780554785)
Clean editorial on-model, light-gray studio, negative space upper-left. Technically strong
hero. Tension: reads as generic contemporary US-DTC (config `indiaShout:2`) — see §6.

**7. banjaaran-studio — "Maati बोम्बर Sneakers" (INSTOCK FALLBACK)** · fashion · 3221×4295 (3:4)
[url](https://cdn.shopify.com/s/files/1/0723/2398/9662/files/Maati_03_2ff2a142-3df1-4f31-9525-cb9d8601c4f5.jpg?v=1762780428)
Side-profile product on off-white studio, large top negative space (B pass). Flagged
`source: instock_fallback` — no bestseller signal. Plain e-comm studio shot, no visual
India-shout on its own. Acceptable stopgap; not a confident hero.

### ❌ REJECTED

**8. the-nesavu — "Party Wear Gown … Red Floral Print"** · baby_and_kids · 1533×2299 (2:3)
[url](https://cdn.shopify.com/s/files/1/0072/1987/1829/files/GFC1589A.jpg?v=1782563450)
Visually lovely (kalamkari-style floral, strong India-shout) **but carries a baked-in
watermark** top-right (`the Nesavu / www.thenesavu.com`) → **C1 disqualify**. Also full-
frame subject + tall 2:3 = bad crop (A3) and no clean overlay zone (B3). *Only vision
catches the watermark — `sharp` would pass this.*

**9. vilvah-store — "Milk Drops Brightening Serum 40ml"** · beauty · 1080×1080 (1:1)
[url](https://cdn.shopify.com/s/files/1/0702/1130/5689/files/Milk_Drops_40ml_1.jpg?v=1767677463)
Dramatic milk-splash — striking, but **near-white across the whole frame → no zone hits
AA for dark text without a scrim (B3 reject)**, and a dense product **label** (product-
integral text, C3) competes with any headline. Good illustration that "visually strong"
≠ "hero-suitable."

**10. isharya — "Gold Melon Ear Cuff"** · jewelry · 1200×1200 (1:1)
[url](https://cdn.shopify.com/s/files/1/0640/5167/5359/files/E2467-63-710_2.jpg?v=1758831717)
Extreme editorial crop of a model's ear. Beautiful, but **illegible as a brand hero
(E1 reject)** — you can't tell it's jewelry at thumbnail, no India-shout, further
landscape cropping tightens it. Global-editorial styling (config demotes Isharya for
exactly this "reads generic without copy" reason).

### 🟡 EDGE — craft-strong but carries product-integral text

**11. gullylabs — "GL001 Buransh Red for Women"** · fashion · 2080×2080 (1:1)
[url](https://cdn.shopify.com/s/files/1/0693/2385/0012/files/DSC09462_4.jpg?v=1773902596)
Handwoven ikat/kilim textile sneaker + coin charms = strong craft India-shout, pure white
bg with a large top overlay band (B pass). *But* the shoe carries **embroidered brand
text** ("GULLYLABS") — product-integral, **not** a promo (C3): downgrade + human call,
don't auto-reject. Vision flags "text present"; a human confirms it's on the product.

---

## 6. Aesthetic-tension flags (surfaced, not resolved)

Mela's current editorial default is **bright / warm / lifestyle / maximalist**. These
candidates are visually strong but **stylistically divergent** — reported here rather
than silently filtered out:

- **nicobar (#6)** and **tarinika (#5)** / **banjaaran (#7)**: clean, minimal,
  cool-studio / global-editorial. They score *well* programmatically (great contrast,
  safe crops) but read closer to generic US-DTC than to craft-forward India. Leaning on
  them as heroes risks the "how is this different from Amazon?" problem the hero PRD
  (§12A.1) is explicitly trying to avoid.
- Decision needed (§7): does the image scorer apply a **style-fit penalty** toward the
  warm/lifestyle default, or stay style-neutral and let the human override per brand?

---

## 7. Decisions (were open questions; resolved 2026-07-22 — overridable in review)

Judgment calls taken with a bias toward **easy to execute**. Each is still open to a
reviewer veto.

1. **Multi-CSV rule (pluchi, kaunteya) → ✅ config-category CSV only.** Deterministic and
   represents how the brand is positioned on Mela. Pooling stays a documented fallback if
   a brand's config-category CSV ever yields too few candidates.
2. **Style-fit penalty → ✅ none; neutral scorer + manual override.** The §9 deep-dive
   shows style tension (nicobar) is *brand-inherent*, not fixable by picking another image —
   so encoding an automated warm/lifestyle penalty would wrongly demote whole brands and is
   subjective to tune. Keep the scorer objective; use the manual-override field for taste.
3. **Hero slot aspect ratio → ✅ 1:1 square.** Matches the card's existing convention
   (`BrandCardHome.module.css` product tiles are `aspect-ratio: 1`), and the catalog is
   dominated by square/portrait so square minimizes crop loss (see §3). A wider hero would
   force bad crops on nearly everything and is a separate design decision.
4. **Overlay text color → ✅ fixed white text on a gradient scrim.** One code path, works
   over almost any image, and makes B2 contrast math trivial.
5. **Scrim → ✅ yes, always** (bottom-up gradient behind the headline). Biggest execution
   simplifier: it demotes B2/B3 from gates to tie-breakers (§4 gate-priority note) so the
   pipeline rarely has to reject on contrast alone.
6. **banjaaran-studio → ✅ accept In-Stock fallback now;** backlog "configure a bestseller
   collection in `shopify_brands.py`." Per §9 the fallback pool contains genuinely strong
   craft-forward heroes — select for subject-fill + color, not the first row.
7. **masilo → ✅ omitted from the hero surface until its CSV lands.** Per the empty-state
   contract `BrandHeroCard` skips brands with no `brandHeroImage`; masilo simply doesn't
   appear in the hero until it has source data. No special-casing needed.

8. **Where the hero URL is sourced/stored → ✅ `shopify_brands.py` is the source of truth**
   (full flow in §8.1). It already holds every brand-profile field, and an existing Python
   exporter (`export_brand_content.py`) bridges it to JSON that the Node side reads — so the
   hero image rides the same rails: add `brand_hero_image_url` to `shopify_brands.py`, export
   it, push to Sharetribe `publicData.brandHeroImage`. The auto-scorer writes its pick *back
   into* `shopify_brands.py` (single-field, guarded), and a hand-entered value there is an
   override the scorer never clobbers.

**Net effect on Part 2:** with square crop + always-on scrim + white text, the pipeline's
hard gates collapse to essentially three programmatic/vision checks — **C** (no
watermark/promo, vision), **B0** (subject-fill, sharp), **A** (crop-safety, sharp) — plus a
human override. That's a deliberately small, buildable surface.

---

## 8. Scoring feasibility summary (for Part 2 architecture)

All scoring + the `publicData.brandHeroImage` write live in
**product-listing-integration** (owns the Integration SDK; **add `sharp` as a new dep**).
A **new** web-client component (`BrandHeroCard`, not `BrandCardHome` — see the header
architecture note) is a pure reader with fallback. Split:

| Layer | Criteria | Tool |
|---|---|---|
| **Fully programmatic** | A1, A3, B1, B2, B3, D1, E2 (color), dominant tone | `sharp` (`metadata`, `stats`, per-tile region `stats`) |
| **Vision-model call** | C1 watermark, C2 promo graphics, C3 text-type classification | vision/OCR — `sharp` **cannot** read text |
| **Human judgment / override** | A2 edge crops, D2 style-fit, E1 thumbnail legibility, §6 tension | manual override field in the audit record |

The Part 2 `brandHeroImageScore` record should store the per-criterion pass/fail (not
just the URL) so a pick is auditable and re-runnable on the normal ingestion cadence.

### 8.1 Data flow — `shopify_brands.py` is the source of truth

**Question:** should the hero image live in `shopify_brands.py` for the
product-listing-integration script to read? **Yes.** `shopify_brands.py` already holds every
brand-profile field (tagline, story, HQ, socials, bestseller collections), and the
brand-profile pipeline already bridges it to the Node side via a **Python exporter** — so
there is no "Node can't read Python" problem, and the hero image should follow the identical
path rather than inventing a side channel.

**Existing bridge (brand bio today):**

```
shopify_brands.py ──[export_brand_content.py]──▶ brand_content.json ──[seed-brand-profiles.js]──▶ Sharetribe
 (SOURCE OF TRUTH)   (Python exporter, scraper repo   (keyed by brand slug;   (Integration SDK,          publicData
  per-brand dicts)    scripts/); collapses to the      currently {bio})        sdk.users.updateProfile)   (.bio)
                      profile-bearing entry per slug
```

**Hero image rides the same rails — three small additions:**

1. **`shopify_brands.py`** — add `brand_hero_image_url` (and it's the human-override point:
   a value present here is authoritative). Written on the **profile-bearing entry** for each
   slug — the one that already carries `brand_tagline`/`brand_story` (multi-category brands
   like pluchi/kaunteya/nicobar have secondary entries without profile fields; those are
   skipped by the exporter, so the hero goes on the primary entry, sourced from that brand's
   config-category CSV per §2).
2. **`export_brand_content.py`** — emit `brand_hero_image_url` into `brand_content.json`
   alongside `bio`.
3. **push to Sharetribe** — write `publicData.brandHeroImage` from that field (via
   `update-brand-hero-image.js`, or by extending `seed-brand-profiles.js`; either uses the
   same `updateProfile` pattern). `web-client` `BrandHeroCard` reads only Sharetribe
   `publicData` — never the CSV or the Python registry.

**How the URL gets into `shopify_brands.py` — two sub-flows:**

- **Auto (common):** `update-brand-hero-image.js` reads the brand's config-category CSV,
  scores `Product Image URL` candidates with `sharp`, and **writes the winning
  `brand_hero_image_url` back into `shopify_brands.py`** — single-field insert/update per
  matched entry (stable key: `base_url` + `output_file`), **no freeform regex**, always
  `--dry-run` + printed diff first, explicit `--confirm` to write. (These guardrails from the
  original Part 2 spec are exactly right, precisely *because* `shopify_brands.py` is the
  source of truth: a malformed edit breaks the registry for every brand.)
- **Human override (exception — pin a specific Tarinika necklace, approve/deny a Nesavu
  shot, override a style call):** hand-edit `brand_hero_image_url` in `shopify_brands.py`.

**Clobber-safety:** the auto-writer **only fills empty `brand_hero_image_url` fields by
default**, so hand-entered overrides are never overwritten; `--recompute` is required to
re-score brands that already have a value. This satisfies "recompute on cadence" (new/unset
brands get scored every run) *and* makes human picks sticky.

**Audit record:** keep `shopify_brands.py` clean (just the URL — it's a human-facing
registry). Store the per-criterion `brandHeroImageScore` in Sharetribe `publicData` (per the
original spec) and/or a sidecar `data/hero-scores.json` report — not as a verbose dict inside
the Python registry.

> Also honor the original "repo path as config, not hardcoded" ask: `cli-utils.js:25`
> currently hardcodes an absolute `Mela-scrapper-integrations/scrapper_csvs` path — Part 2
> should take both the CSV root and the `shopify_brands.py` path from an env var / CLI flag.

### 8.2 Exact field placement for multi-entry brands (write-back stable key)

Several brands appear **more than once** in `SHOPIFY_BRANDS` (one dict per category/collection,
same `brand_name`). The write-back must target exactly the dict the exporter reads, or the
hero field lands on an entry that's silently ignored.

**Decisive constraint — `export_brand_content.py` dedup (verified in source):** it iterates
`SHOPIFY_BRANDS` and keeps the **first-in-list entry per `brand_name`**; if that first entry
has no `brand_tagline`/`brand_story` it marks the brand *missing* and **does not** look at
later entries. So the canonical dict for a brand is its **first occurrence**, which for every
current live brand is also the one carrying the profile fields **and** the one whose category
matches its `configBrands.js` category.

**Rule:** write `brand_hero_image_url` on the **first-in-list `SHOPIFY_BRANDS` entry for that
`brand_name`** (stable key = `base_url` + `output_file`). Source its candidate image from that
same entry's `output_file` CSV. If a future brand's first entry category ever diverges from its
`configBrands` category (or its first entry lacks a tagline), **surface it** — don't guess.

| brand_name | slug | entries (`output_file` · category · has profile) | ✍️ write target (`base_url`, `output_file`) | source CSV | notes |
|---|---|---|---|---|---|
| **Pluchi** | pluchi | `pluchi_products.csv` · baby_and_kids · ✅ **(1st)**<br>`pluchi_fashion_products.csv` · fashion · ✅<br>`pluchi_home_products.csv` · home_and_kitchen · ✅ | `(https://www.pluchi.com, pluchi_products.csv)` | `baby_and_kids/…/pluchi_products_classified.csv` | Profile is **duplicated** on all 3 entries, but only the 1st is exported → hero field only on the 1st; writing it to the fashion/home entries would be **silently ignored**. Config category = baby_and_kids ✓ |
| **Kaunteya** | kaunteya | `kaunteya_products.csv` · home_and_kitchen · ✅ **(only)** | `(https://kaunteya.in, kaunteya_products.csv)` | `home_and_kitchen/…/kaunteya_products_classified.csv` | Single registry entry. The stray `baby_and_kids/…/kaunteya_products_classified.csv` seen in the scan is **not registered** in `SHOPIFY_BRANDS` → orphaned/misclassified, never a write target (data-quality flag). |
| **Nicobar** | nicobar | `nicobar_products.csv` · fashion · ✅ **(1st)**<br>`nicobar_home_products.csv` · home_and_kitchen · — | `(https://global.nicobar.com, nicobar_products.csv)` | `fashion/…/nicobar_products_classified.csv` | 2nd entry has no profile → already ignored by exporter. Config category = fashion ✓ |
| **The Nesavu** | the-nesavu | `thenesavu_girls_products.csv` · baby_and_kids · ✅ **(1st)**<br>`thenesavu_boys_products.csv` · baby_and_kids · —<br>`thenesavu_baby_products.csv` · baby_and_kids · —<br>`thenesavu_fashion_products.csv` · fashion · — | `(https://www.thenesavu.com, thenesavu_girls_products.csv)` | `baby_and_kids/…/thenesavu_girls_products_classified.csv` | Field placement is on the 1st entry, but stays **empty** (watermark-blocked, §9) → brand skipped from hero. |

*(Same first-entry rule covers the other multi-entry brands — Masilo `masilo_products.csv`
[baby, but no CSV yet → empty], SuperBottoms `superbottoms_products.csv` [baby].)*

**Concrete edit (Pluchi, 1st entry) — single-field insert, everything else byte-identical:**

```python
    {
        "brand_name": "Pluchi",
        "base_url": "https://www.pluchi.com",
        "collection": "baby-and-kids",
        "bestseller_collection": "best-selling-collection",
        "output_file": "pluchi_products.csv",
        "category": "baby_and_kids",
        "brand_hero_image_url": "https://cdn.shopify.com/…/<winner>.jpg",   # ← inserted; auto-writer fills only if empty
        "brand_tagline": "Hand-finished knitwear for babies, women, and home. …",
        "brand_story": "Pluchi specializes in knitted essentials …",
        …
    },
```

**Exporter change (one line):** in `export_brand_content.py`, add the field to the emitted
dict — `content[slug] = {'bio': ' '.join(parts), 'brand_hero_image_url': entry.get('brand_hero_image_url')}`
— and omit/None it when empty so the seeder writes nothing and `BrandHeroCard` skips the brand
(empty-state contract).

### 8.3 OPEN — image URL source: Shopify CDN vs Sharetribe-hosted (resolve before relying on this)

**What shipped in the first run:** `brand_hero_image_urls` (and therefore
`publicData.brandHeroImages`) currently hold **raw Shopify CDN URLs**
(`cdn.shopify.com/…`), because the sharp scorer selects from the CSV's `Product Image URL`
column. `data/hero-scores.json` records these same Shopify URLs.

**Why that's a problem:** those URLs are **external and outside Mela's control** — a brand can
re-slug, resize, or delete the asset and the hero silently 404s; there's no imgix sizing/format
control; and it's inconsistent with the rest of the app, which renders **Sharetribe-hosted**
image variants (`image.attributes.variants.<name>.url`) that were already uploaded during
listing creation. Every product row already carries its Sharetribe copies in
**`Dev_Uploaded_Image_IDs`** (comma-separated image UUIDs) plus the listing in **`Dev_Listing_ID`**.

**The trap — do NOT map by position.** It is tempting to map "the Nth Shopify URL → the Nth
`Dev_Uploaded_Image_IDs`," but the two lists are **not reliably 1:1**. Measured on qualifying
rows: tarinika 260 aligned vs **456 mismatched**; fizzygoblet 34 vs 32; ankid 8 vs 28 (uploads
get skipped/deduped/capped, so indexes drift). Index-0 (the scorer always picks the first
image) is the *most* likely to line up but is still not guaranteed. A blind positional map will
put the wrong image on some brands.

**Options (decide before treating `brandHeroImages` as final):**
- **A — keep Shopify URLs.** Zero extra work; accept the external-hotlink fragility above.
  Fine as a stopgap for the dev/QA demo (which is where it is now).
- **B — store Sharetribe image IDs**, let `BrandHeroCard` resolve ID → variant URL via the
  Marketplace API. App-consistent, but adds an image fetch to the web-client.
- **C — resolve at pipeline time (recommended).** Two concrete sub-paths, both leaning on the
  fact that the scorer **already picks a specific row's *first* image** (`firstImage(row)`,
  index 0) — so the safe companion is that same row's **first** `Dev_Uploaded_Image_IDs` entry
  (leading images upload first, so index-0↔index-0 is the reliable pairing even though *trailing*
  indexes drift — that's the §8.3 mismatch):
  - **C1 (smallest change):** in `update-brand-hero-image.js`, alongside each pick capture
    `row['Dev_Uploaded_Image_IDs'].split(',')[0]` (the Sharetribe image UUID) and
    `row['Dev_Listing_ID']`. Store the **image ID** in `brand_hero_image_ids` (parallel to the
    URLs). `BrandHeroCard` then resolves ID → variant URL via the Marketplace API (Option B on
    the read side).
  - **C2 (dumb-reader):** same capture, then resolve the ID → a Sharetribe **variant URL** at
    pipeline time (`sdk.listings.show({ id: Dev_Listing_ID, include:['images'],
    'fields.image':['variants.…'] })`, find the matching image), and store that URL in
    `brand_hero_image_urls`. `BrandHeroCard` stays a dumb URL reader.

  Either way the sharp rubric is unchanged — the scorer still *scores* the fetchable image; only
  what gets *stored* changes. **Note:** the current `data/hero-scores.json` holds Shopify URLs
  only (not the IDs), so resolving now means either a re-run that captures the IDs, or re-joining
  each pick back to its CSV row by URL to read `Dev_Uploaded_Image_IDs[0]`.

**Impact on `BrandHeroCard`:** none functionally — it renders whatever URL array is in
`publicData.brandHeroImages`, Shopify or Sharetribe. Keep it **source-agnostic**. (Only caveat:
if a fixed render size is wanted, Sharetribe exposes named variants while Shopify accepts
`?width=` query params — a styling detail, not a contract change.)

> **Status — IMPLEMENTED (Option C1, 2026-07-24).** `update-brand-hero-image.js` now captures,
> per pick, the row's **first** `Dev_Uploaded_Image_IDs` (Sharetribe image UUID) + `Dev_Listing_ID`,
> writes all three parallel fields to `shopify_brands.py`
> (`brand_hero_image_ids` / `brand_hero_listing_ids` / `brand_hero_image_urls`), and **pushes them
> directly** to Sharetribe `publicData` as `brandHeroImageIds` / `brandHeroImageListingIds` /
> `brandHeroImages`. Candidates without an uploaded Sharetribe image are skipped (can't be a
> hero-by-id). The seed/export hero path was reverted — this script solely owns the hero push;
> `seed-brand-profiles.js` is bio-only again.
>
> **Resolution verified:** for a given `imageId`+`listingId`, fetch the listing with
> `include:['images']` and read `image.attributes.variants.<name>.url` — confirmed the pushed
> image IDs are present on their listings and resolve to real `sharetribe.imgix.net` variant URLs.
> `brandHeroImages` (Shopify URLs) is retained only as a transitional reference/fallback.
> `data/hero-scores.json` records `imageId`/`listingId`/`url`/`score` per pick for audit.

---

## 9. Deep-dive: tarinika · nicobar · banjaaran · the-nesavu

A wider pull (8 more qualifiers each; banjaaran from the In-Stock fallback) to test whether
these borderline/rejected brands are limited by *the brand's photography* or by *which image
we sampled*. Answer differs per brand — and it surfaced the **B0 subject-fill** criterion.

### the-nesavu → 🔴 BLOCKED (brand-wide watermark)
**Every** sampled image carries a baked-in `the nesavu` / `www.thenesavu.com` watermark, and
its **position varies** (top-right, dead-center over the model, bottom-right) — so no fixed
crop reliably removes it, and center-placed ones (outdoor bamboo shot) can't be cropped out
at all. This is not a bad-sample problem; it's the brand's entire product-photo pipeline.
- **Consequence:** The Nesavu fails **C1** catalog-wide → it gets **no** scraped hero, so
  under the empty-state contract it is **dropped from the hero surface entirely** (not shown
  with a logo). This matters because The Nesavu is a **first-fold** brand
  (`homepage-hero-prd.md` §12A.1 pulled it *up* into the fold) — dropping it leaves a
  first-fold hole the reviewer must reconcile against the curated order.
- **Recommended action (backlog):** ask the brand for clean, unwatermarked hero shots, or
  approve a watermarked hero as an explicit exception. **Not** solvable by the scorer.

### tarinika → 🟢 VIABLE, selection-sensitive
All white-studio, product-only, **no models, no watermark** — the clinical look is the whole
catalog, not one image. But **which** product is picked matters enormously:
- Prefer frame-filling, ornate, temple/kundan pieces and **necklace sets** —
  [Anmol Antique peacock bracelet](https://cdn.shopify.com/s/files/1/2026/1561/files/ABX2795XM.jpg?v=1730109567),
  [Maati oxidized jhumkas](https://cdn.shopify.com/s/files/1/2026/1561/products/IMGL4945copycopy.jpg?v=1656523513).
- Avoid isolated **solitaire studs** (tiny subject, generic) — the exact failure **B0** now
  catches. The earlier "Zarina pink drop" sample was mid-tier; better exists.

### nicobar → 🟡 VIABLE but style-inherent-generic
Uniformly clean cool-studio on-model editorial — the "generic US-DTC" tension (§6) is
**brand-wide**, confirming decision #2 (no automated style penalty; it'd nuke the brand).
Within that look, steer selection:
- Prefer the more colorful / India-adjacent silhouettes —
  [Banko watermelon kurta](https://cdn.shopify.com/s/files/1/0508/8906/4628/files/NBI045959_1.jpg?v=1752063405),
  [Astral printed kurta](https://cdn.shopify.com/s/files/1/0508/8906/4628/files/NBI050121_7.jpg?v=1781518663) —
  over generic shirts/pants.
- **Reject faceless waist-down crops** (e.g. Riverbank pants) — no face, ambiguous subject;
  another **B0** catch.

### banjaaran → 🟢 VIABLE fallback (my first sample was the *weakest* one)
The tan sneaker in §5 was the least interesting product in the pool. The In-Stock fallback
actually holds vivid, craft-forward, high-India-shout footwear:
- [Gaze folk-motif mules](https://cdn.shopify.com/s/files/1/0723/2398/9662/files/21_03.jpg?v=1762780401),
  [Gaja painted Mughal-miniature loafers](https://cdn.shopify.com/s/files/1/0723/2398/9662/files/06724_Banjaaran-04_05.jpg?v=1768380018),
  [Bageecha tapestry sneaker](https://cdn.shopify.com/s/files/1/0723/2398/9662/files/63_03_4aa78a5a-a875-4e28-b591-389dd026c3fc.jpg?v=1762815285).
- All white-studio, no watermark/promo. Selecting for **B0 subject-fill + color** yields a
  genuinely strong hero *despite* being a fallback — reinforcing that the fallback mechanism
  is fine; only the pick needs to be smart.

**Cross-cutting takeaway:** two of four "problem" brands (tarinika, banjaaran) were limited by
*sample choice*, not photography — exactly what **B0 subject-fill** now formalizes. One
(nicobar) is style-inherent (accept + steer). One (the-nesavu) is a hard data-quality block
the scorer can't fix and must escalate.

---

## Appendix — reproduction

Calibration scan is throwaway research tooling (not the Part 2 pipeline), kept in the
session scratchpad: `scan_candidates.py` (mapping + qualifier filter + sampling) →
`candidates.json`; the §9 deep-dive used an 8-per-brand re-sample + Pillow contact sheets
(`sheet_<brand>.jpg`) to eyeball each brand's range at once. Re-runnable against the CSVs to
refresh the sample. Part 2 will re-implement the qualifier + sharp scoring in
`scripts/update-brand-hero-image.js`.
