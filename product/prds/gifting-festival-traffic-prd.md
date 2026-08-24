# Gifting & Festival Social-Traffic Engine — PRD (day-split execution)

**Status:** 🔲 Ready — spec complete, not started
**Priority:** P0 (gifting is the near-term social-traffic wedge)
**Created:** 2026-08-23
**Owner:** PM + Developer

> **How to execute:** This PRD is **self-contained** — each Day below can be run cold in a fresh
> session with no prior chat context. Execution is **split across 3 days to spread token usage**;
> **Day 1 (pipeline/structured-data) is independent and can run in parallel** with everything else.
> Fills the gifting-landing-page gap flagged in `PRD_TRACKER.md` (UXR/Copy Debt table).

---

## Executive Summary

**Feature:** A gifting-focused social-traffic engine (Instagram + Pinterest) pointed at a purpose-built, measurable web destination, anchored on a **full festival sequence** (Raksha Bandhan → Navratri → Karva Chauth → Diwali → Bhai Dooj → wedding season).

**Full-stack scope:** data pipeline (`prompt_engine.py`) → CSV `Item_Aspects` string → `product-listing-integration` → Sharetribe `publicData` → `web-client` (gifting landing, filters, sort, attribution) → social content/calendar/boards → brand sourcing.

**Objective:** Drive qualified social traffic and reach **high confidence that posts AND the web destination convert** before any ad spend. Gifting is the wedge (maps to how diaspora shoppers use Pinterest — plan occasions early — and to Mela's inspiration-first positioning).

**Success metrics:** Pinterest outbound CTR rising off its ~0 floor; social→brand-clickout rate on the gifting landing; GA4 sessions attributable by platform+campaign. Ads only after the §Gate clears.

**Relates to / extends (consolidation, not duplication):** `enrichment-pipeline-stage2-update-prd.md` (new Stage-2 increment beyond its meta/synonyms scope); `brand-storefront-occasion-module-prd.md` (reuses `occasion` field + `OccasionStrip`; extends the enum it froze at 2); `search-ranking-relevance-prd.md` (sort aligns with `melaScore`); `dev-to-production-migration-prd.md` (schema/config hazards); `homepage-redesign-prd.md` §10 (delivers the deferred `/occasions/*`).

---

## Shopper-behavior model (the strategic core)

| | **Pinterest** | **Instagram** |
|---|---|---|
| Mode | **Search + planning.** Arrives with intent, searches weeks ahead, saves to boards. | **Discovery + trust.** Served via Reels/Explore; rarely searches. |
| Funnel role | **Primary gifting traffic + conversion.** | **Reach + brand recognition** that makes clicks convert. |
| Link target | Specific **listing** or **gifting landing** page. | **Brand page** / link-in-bio **gifting landing**. |
| Gifting leverage | Occasion/recipient boards built **6–8 wks ahead**; keyword gift-guide pins. | 4–5 Reels/wk w/ payoff; occasion-in-America; gift-guide carousels → landing. |

**One line:** *Pinterest carries gifting traffic; Instagram builds the brand so it converts; both point at one measurable gifting destination.*

**Timing (verify dates vs a panchang):** Raksha Bandhan ~Aug 28 2026 (*this week — no runway, light-touch only*), Navratri ~Oct 11, Karva Chauth ~Oct 29, Diwali ~Nov 8, Bhai Dooj ~Nov 10, wedding season Nov–Feb. Pinterest lead time ⇒ **Diwali/Navratri pins start now**; first fully-run festival = Navratri/Diwali.

---

## Data-flow reference (read before Day 1)

1. **`prompt_engine.py`** `create_enrichment_prompt()` emits one `item_aspects` **string** per product: `Field Name|field_key: Label|value_code|benefit; …`. Occasion already rides *inside* this string (there is **no** separate `Occasion` CSV column). New fields `gift_occasion` and `recipient` ride the same way.
2. **`product-listing-integration`** `scripts/lib/models/listing-model.js` `parseItemAspects()` splits that string, reads each field's schema from a **listing-fields config fetched from GitHub = `web-client/src/config/configListing.js`** (`getFieldConfig`), validates values against `enumOptions`, and writes `result[field_key]` → `publicData[field_key]`. Unknown values are logged to `scripts/unmapped-item-aspect-options.json` and passed through.
3. **`web-client/src/config/configListing.js`** is therefore the **single source of truth** for enum values. A value must exist there (and in the Sharetribe search schema via CLI) to be filterable.
4. Field-key → publicData key is verbatim: `gift_occasion` → `publicData.gift_occasion` → filter `pub_gift_occasion`. Match existing lowercase `occasion` style; do not camelCase.

---

# DAY 1 — Structured-data pipeline (independent; run in parallel)

**Repos:** `Mela-scrapper-integrations`, `product-listing-integration`, `web-client` (config only), Sharetribe CLI. **Model:** Opus for the `gift_occasion` prompt design (bounded inference is hard); Sonnet for the config/CSV/CLI mechanics.

### 1A. `prompt_engine.py` — broaden `occasion` (wear/use)

In `create_enrichment_prompt()` VALID VALUES, replace the occasion block (~line 241–244) with — keep the **strict "only if explicitly named"** rule:
```
occasion (multi) — the occasion the item is WORN/USED at; tag ONLY if explicitly named in the description:
  diwali, holi, eid, pongal, navratri, onam, raksha_bandhan, karva_chauth, bhai_dooj,
  wedding, mehendi, haldi, naming_ceremony, baby_shower, housewarming, birthday,
  mothers_day, fathers_day
  → Do NOT infer from "festive"/"ethnic"; omit if none named. (gift-suitability is a SEPARATE field below.)
```
Also update the Task-2 SEO-title occasion word-scan list (~line 310) to the same set.

### 1B. `prompt_engine.py` — NEW `gift_occasion` (gift-suitability, bounded inference)

Add a FIELD KEY (`Gift Occasion → gift_occasion`) and this VALID-VALUES block. **This is the key insight: "right to wear for X" ≠ "right to gift for X"** — an everyday romper isn't festive but IS a great naming-ceremony gift.
```
gift_occasion (multi) — occasions this product is a SUITABLE, PRESENTABLE GIFT for, even if not named:
  diwali, raksha_bandhan, karva_chauth, bhai_dooj, wedding, anniversary, navratri, holi,
  eid, pongal, onam, naming_ceremony, baby_shower, housewarming, birthday, mothers_day,
  fathers_day, general_gifting
  RULES (bounded — do NOT blanket-tag):
   1. Tag only if the item is a plausible, giftable object (quality/craft/presentation), NOT a
      basic utility/refill/consumable-basic.
   2. Judge fit by category + craft + price + who receives it. Tag the 1–3 BEST-fitting occasions only.
   3. general_gifting = broadly giftable but no specific occasion stands out.
  EXAMPLES:
   - Organic cotton romper → naming_ceremony, baby_shower, general_gifting
   - Kansa (Bronze) dinner set → housewarming, wedding, diwali
   - Silver jhumka (drop earrings) → diwali, karva_chauth, wedding
   - Ayurvedic skincare hamper → diwali, general_gifting, mothers_day
```

### 1C. `prompt_engine.py` — NEW `recipient` (bounded inference)

Add FIELD KEY (`Recipient → recipient`) and:
```
recipient (multi) — who the product is naturally for/gifted to (infer from category, age_group, gender, description):
  for_mom, for_dad, for_him, for_her, for_kids, for_baby, for_new_parents, for_couple, for_host, for_self
  RULE: tag the 1–3 most natural recipients; do not force all.
  EXAMPLES: baby romper → for_baby, for_new_parents; jhumka → for_her, for_mom;
            kansa dinner set → for_couple, for_host, for_new_parents
```

### 1D. `prompt_engine.py` — NEW glossing rule (from user: comprehensibility for US audience)

Add to Task 1 (material), Task 2 (SEO title), Task 3 (meta description):
```
GLOSSING RULE — when the product name or a material/craft term is a regional Indian word a
US audience may not recognize, KEEP the Indian term and add the widely-recognized English
equivalent in parentheses on first use, e.g. "Kansa (Bronze) Snack Plate", "Bandhani (Tie-Dye)
Dupatta (Scarf)". Use only established equivalents from the glossary below (or an equally
well-known one); NEVER invent. Do NOT gloss terms already common in the US (sari, henna).
GLOSSARY: kansa→Bronze; pital→Brass; jutti/mojari→handcrafted flat shoe; dhurrie→flat-woven rug;
  bandhani/bandhej→tie-dye; ikat→resist-dyed weave; kalamkari→hand-painted cotton;
  chikankari→shadow hand-embroidery; phulkari→floral hand-embroidery; jhumka→drop earrings;
  kada→cuff bangle; potli→drawstring pouch; urli→wide bowl; diya→oil lamp; dupatta→scarf;
  lehenga→skirt set; anarkali→flared dress; thali→platter; kadai→wok; handi→pot.
```
> **⚠️ Kansa accuracy flag:** Kansa is technically **bronze / bell metal** (copper+tin); *brass* is copper+zinc = *pital*. Kaunteya markets Kansa as "bronze." Glossary uses **kansa→Bronze**. If you (the user) prefer "Brass" for search familiarity, change one line in the glossary — the rule is otherwise identical. **Confirm before running the batch.**

### 1E. Update the OUTPUT example + system prompt

In `create_enrichment_prompt()` OUTPUT JSON example, ensure `item_aspects` shows the new keys, e.g. append `; Gift Occasion|gift_occasion: Housewarming|housewarming|Great housewarming gift, Wedding|wedding|Wedding-worthy; Recipient|recipient: For Host|for_host|For hosts, For Couple|for_couple|For couples`. Add a one-line mention of `gift_occasion`, `recipient`, and the glossing rule to `create_enrichment_system_prompt()`.

### 1F. Register the new fields in `web-client/src/config/configListing.js` (source of truth)

- Expand the existing `occasion` field's `enumOptions` to the 1A set. Migrate `diwali-festivals`→`diwali` but keep `diwali-festivals` recognized (legacy tagged listings). Consider `group: 'primary'`.
- Add two new fields mirroring `occasion`'s shape (`schemaType: 'multi-enum'`, `scope: 'public'`, `searchMode: 'has_any'`): **`gift_occasion`** (1B options) and **`recipient`** (1C options). `group: 'primary'` for gifting visibility.
- Keep `CategoryShowcase.js` `OCCASIONS` labels in sync for any occasion surfaced in a strip.

### 1G. Sharetribe search schema (gates filtering — run per environment)

QA = pseudo-production (`dev-to-production-migration-prd.md`). Run in **dev, then QA/prod**:
```
flex-cli search set --key occasion      --scope public --type multi-enum -m <MARKETPLACE_ID>
flex-cli search set --key gift_occasion --scope public --type multi-enum -m <MARKETPLACE_ID>
flex-cli search set --key recipient     --scope public --type multi-enum -m <MARKETPLACE_ID>
```
Until this runs, `has_any` filters on new values are silently ignored (returns unfiltered).

### 1H. Backfill existing inventory

**Runner:** `single_file_classifier.py <csv>` (per brand CSV). **Verified behavior:** it always runs the 2-request pipeline (category → enrichment); on a normal re-run, already-classified products are **served from cache and skipped** (`classify_products` + `filter_new_products`), so a plain re-run will NOT add the new fields to existing products. **There is no Stage-2-only mode today.** Two backfill options:

- **(A) No-code (default):** `single_file_classifier.py <csv> --force-reclassify` per brand CSV. Ignores cache and re-runs both stages. Stage-1 (category) is the cheap request (batch 20, tiny output); the expensive Stage-2 enrichment has to re-run anyway to emit the new fields. Minor risk: a product's category could re-map — spot-check.
- **(B) Small build (~1 hr, cleaner) — CHOSEN:** add an `--enrich-only` flag to `single_file_classifier.py`. **Per-row behavior (not per-run):**
  - **Existing/classified rows** (row already has a `Mapped_Category` in the classified CSV): skip Request 1, reuse the stored `Mapped_Category`, run **only Request 2** (enrichment) + `ItemAspectsFormatter`. This is the backfill path — no Stage-1 re-run, no category churn.
  - **New/unclassified rows** (not yet in the classified file, or no `Mapped_Category`): fall through to the **normal full 2-request pipeline** (category → enrichment).
  This makes `--enrich-only` safe to run on any CSV: it re-enriches everything, re-using category only where it already exists. Implementation: gate the Request-1 loop in `_classify_two_request` (or in `classify_products`/`process_csv_file`) on whether a stored category is available for each row; bypass cache for enrichment so existing rows actually get the new fields. Matches the enrichment PRD's should-have; prefer for the full catalog (5k+ rows).

Without backfill, festival-specific pages are empty. After enrichment, re-run `product-listing-integration` create/update so `publicData` is populated; spot-check `scripts/unmapped-item-aspect-options.json` for values that didn't validate (= a `configListing.js` enum mismatch).

> **No new CSV column / dataclass change:** `gift_occasion` and `recipient` ride *inside* the existing `item_aspects` string, so `response_parser.py`, `models.py`, and the classified-CSV schema are **unchanged**. The only classifier file edited is `prompt_engine.py`.

### Day 1 acceptance
- [ ] 10 sample products → valid JSON; `gift_occasion`/`recipient` present, 1–3 values each, **no over-tagging**; glossing applied ("Kansa (Bronze)…"); existing `item_aspects`/`seo_title`/`meta_description`/`search_synonyms` unchanged.
- [ ] `configListing.js` declares expanded `occasion` + `gift_occasion` + `recipient`; `flex-cli search set` run dev→QA/prod.
- [ ] After ingest, `publicData.gift_occasion` / `publicData.recipient` are arrays in Sharetribe Console; `pub_gift_occasion=has_any:diwali` returns tagged listings.
- [ ] Backfill run; `unmapped-item-aspect-options.json` shows no new occasion/gift/recipient leakage.

---

# DAY 2 — Web gifting merchandising

**Repo:** `web-client`. **Model:** Opus for merchandised-sort logic; Sonnet for scaffolding/chips. Depends on Day 1 enums only for Phase-2 filtering; Phase 0/1 are independent.

### Phase 0 — Attribution (ship first; no schema)
- `src/analytics/handlers.js` `GoogleAnalyticsHandler.trackPageView`: include `entry_source: getEntrySource()` (+ session id) from `src/util/analytics/entrySource.js`. **Gotcha:** the first landing `page_view` is auto-sent by the gtag snippet — also set the param in the gtag config in `src/util/includeScripts.js`, or only SPA nav carries it. Register `entry_source` as a GA4 custom dimension (Console).
- After `captureEntrySource()`, strip `utm_*` via `history.replaceState`; ensure landing pages set a query-less `canonicalURL` (`Page.js` supports the override).

### Phase 1 — Shareable gifting landing (no schema)
- Create `src/containers/GiftingPage/{GiftingPage.js, GiftingPage.duck.js, GiftingPage.module.css, giftingContent.js}` serving **`/gifts`** and **`/occasions/:occasionSlug`** from one container. Model on `CategoryPage.js`/`CategoryPage.duck.js`; delegate grid data to `SearchPage.duck` `loadData`; reuse `state.SearchPage` (no new reducer).
- Custom SEO/OG via `Page.js` `socialSharing={{title,description,images1200,images600}}` + `canonicalURL` → good unfurls (SSR already generic in `server/renderer.js`; **no renderer change**). Per-occasion copy + OG image URLs live in `giftingContent.js` (**no inline env literals**).
- Register routes in `src/routing/routeConfiguration.js` + loader in `src/containers/pageDataLoadingAPI.js`.
- **Gift filter chips (presentational):** price bands ("Under $25/$50/$100") reuse the built-in `price` filter; recipient chips link to `?pub_recipient=has_any:<v>` (lights up after Day 1 CLI).
- **Occasion chips on cards:** opt-in `showOccasionChips` prop on `src/components/ListingCard/ListingCard.js` (follow the `TrustBadges` pattern; handle string-or-array `publicData.occasion`; slug→label map imported from `CategoryShowcase.js`); enable in `SearchResultsPanel/SearchResultsPanel.js` + GiftingPage.

### Phase 2 — Occasion strip generalization
- Generalize `isDiwaliSeason()` → `getActiveSeasonOccasion(date)` in `CategoryShowcase.js`; `OccasionStrip` shows only the 2–3 in-season occasions (7 panels is too many). Preserve the existing client-side occasion-tag guard (protects against unset index / string-vs-array tags).

### Phase 3 — Merchandised sort
- `src/containers/SearchPage/SearchPage.duck.js` `sortSearchParams()`: for gifting/occasion context (e.g. `pub_occasion`/`pub_gift_occasion` present, or a flag GiftingPage passes), default to a bestseller-aware order instead of `createdAt` — **without** changing the general default or user-selected sorts. Centralize the "gifting default sort" in one helper so it's a one-line switch to `-pub_melaScore` when `search-ranking-relevance-prd.md` ships. Do NOT build query-time scoring.

### Phase 4 — Optional
- Promote `occasion`/`gift_occasion` to `group:'primary'` on SearchPage if data shows demand (partly done in 1F).

### Day 2 acceptance
- [ ] `entry_source` on `page_view` (incl. first landing) in GA4 DebugView; `utm_*` stripped; canonical clean.
- [ ] `/gifts` + `/occasions/:slug` render curated products with correct OG/canonical (SSR-verified via `curl` + FB/Pinterest validators).
- [ ] Price + recipient + occasion chips route/render correctly (both tag formats).
- [ ] Gifting-context sort bestseller-aware; general `/s` still newest (no regression). `yarn test` green for SearchPage/ListingCard/CategoryShowcase/SearchResultsPanel.

---

# DAY 3 — Social content, brand sourcing, measurement gate

**Repo:** `mela-docs` (+ Pinterest/Blotato manual steps). **Model:** Sonnet (docs/copy); Opus only for festival-angle strategy calls.

### 3A. Social docs
- New `mela-docs/social/gifting-festival-playbook.md` — the shopper model applied to gifting; cross-platform funnel; reusable per-festival campaign template. Links to (doesn't restate) `hook-engineering.md`, `pinterest-playbook.md`, `visual-style-guide.md`.
- New `mela-docs/social/festival-calendar.yaml` (machine-readable for `/social-launch`) — per festival: dates, Pinterest live-by, angle, product categories, target board, hook hypotheses, destination URL pattern, persona.
- Gift-guide format spec added to `hook-engineering.md`/`visual-style-guide.md` (save-worthy "X gifts for Y" pin + IG carousel — targets the ~0 save rate).
- Recipient keyword taxonomy added to `pinterest-playbook.md` §4 (recipient × occasion × category).

### 3B. Pinterest boards
- Create + map (in `category-routing.yaml`): Diwali Gifting (overdue), Navratri, Karva Chauth, Bhai Dooj, Wedding Guest, Raksha Bandhan. (Manual Pinterest create + Blotato board-list refresh.)

### 3C. Brand sourcing (from the 57-row tracking sheet)
**⚠️ H-1B constraint (`founder_immigration_status`):** you cannot personally sign affiliate agreements / earn side income. "Contact for collaboration" below = **feature-permission / relationship-building / international-shipping confirmation only**, NOT affiliate contracts. **Verify US fulfillment before ingesting any brand** (sheet's shipping columns are mostly blank).

**ADD to pipeline now (US-capable + strong gifting fit, not in QA):** Curio Cottage (jewelry), Suta (sarees), Needledust (juttis), Vilvah (beauty hampers), Malabar Baby, Skillmatics, Chidiyaa / Payal Singhal (festive fashion). *Jewelry/home/beauty lead — highest gifting value; only Tarinika+Isharya jewelry live today.*

**CONTACT (permission/relationship):** *Warm — live in QA but never contacted:* Kaunteya (home décor, prime Diwali), The Nesavu (festive kidswear), House of Chikankari, Polite Society. *High fit, needs a conversation:* Daughters of India (has US store), Baby Jalebi (global store), Bipha Ayurveda (gift sets), Gado Living. *India-only — contact re: intl shipping first:* Neemans, ModiToys, fabric pandit, KG Label, Erode.

### 3D. Measurement / ads-readiness gate → add to `metrics-log.md`
| Signal | Source | Bar (tune to baseline) |
|---|---|---|
| Every post UTM-tagged | `/social-launch` | 100% (untagged = defect) |
| Pinterest outbound CTR | Pinterest | Rising, clears platform floor (>~0.2%) |
| Pinterest save rate | Pinterest | Above account median, trending up |
| Social sessions (`entry_source`) | GA4 | Non-trivial, attributable by platform+campaign |
| Landing → brand-clickout rate | GA4 `brand_clickout` | Meaningful on the gifting landing |

**Rule:** ads only once posts are UTM-clean, the gifting landing converts organic traffic, and social→clickout is measurable and positive.

### 3E. Wrap-up
- Register this PRD in `PRD_TRACKER.md`; append shipped items to `product/TODO.md`. Social Workstream can start Diwali/Navratri pins from Day 1 using existing `gifting`/`diwali-festivals` values (don't wait on schema).

---

## Risks

| Risk | Mitigation |
|---|---|
| `gift_occasion` over-tags | Tight bounded rules + examples + 20-product spot-check; Opus-authored prompt |
| Kansa mislabeled | Flag resolved with user before batch (Bronze vs Brass) |
| Occasion schema dev-only | `flex-cli search set` in QA/prod before ship; client guard covers wrong-product (not sort) |
| Thin tagging → empty pages | `gifting`/`general_gifting` broad-match + Day-1 backfill before promoting festival pages |
| Brands can't ship to US | Verify fulfillment before ingest |
| `configBrands` prod stub | Carousels sparse in prod until populated; no hardcoded brand UUIDs |
| Affiliate framing vs H-1B | Collaboration = feature-permission only |

## Critical files (quick index)
**Day 1:** `Mela-scrapper-integrations/.../classifier/prompt_engine.py` (+ `response_parser.py`, `models.py` if a field is added); `product-listing-integration/scripts/lib/models/listing-model.js` (verify only — config auto-syncs); `web-client/src/config/configListing.js`; `web-client/src/containers/.../CategoryShowcase.js`; Sharetribe CLI.
**Day 2:** `handlers.js`, `includeScripts.js`, `entrySource.js`, `SearchPage.duck.js`, `SearchResultsPanel.js`, `ListingCard.js`, `CategoryShowcase.js`, `routeConfiguration.js`, `pageDataLoadingAPI.js`; create `containers/GiftingPage/*`.
**Day 3:** create `social/gifting-festival-playbook.md`, `social/festival-calendar.yaml`, this PRD; update `category-routing.yaml`, `hook-engineering.md`, `pinterest-playbook.md`, `visual-style-guide.md`, `metrics-log.md`, `PRD_TRACKER.md`, `TODO.md`.
