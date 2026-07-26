# Storefront Validation Readiness PRD

## Document Information
- **Created**: 2026-07-26
- **Status**: Draft — pending review
- **Owner**: Product Team
- **Source**: Design review of `/`, `/brands`, `/brands/:brandSlug`, `/categories`, `/categories/:level1` (2026-07-26, desktop 1440px) against `UXR/feedback-log.md` F-001/F-002/F-003 and the 0→1 validation hypothesis
- **Related Docs**:
  - `product/prds/homepage-redesign-prd.md` (shipped hero — this PRD builds on it)
  - `product/prds/trust-conversion-signals-prd.md` (signal system — this PRD surfaces it)
  - `product/prds/brand-storefront-prd.md` + `brands-page-prd.md` (brand surfaces)
  - `product/prds/pre-redirect-sentiment-prd.md` + `crossshop-tracking-prd.md` (measurement)
  - `UXR/feedback-log.md` (F-001, F-002, F-003)

---

## Executive Summary

**Feature**: A validation-readiness pass across homepage, brand pages, and category pages so the storefront gives Mela's core hypothesis a fair test — that a global shopper will choose a curated marketplace of proven Indian brands over Amazon, brand DTC sites, Instagram, and Google search.

**Target URL / Entry Points**: `/`, `/brands`, `/brands/:brandSlug`, `/categories/:level1`

**Target Users**: All four personas (Sarah, Priya, Neha, Arun) — this PRD deliberately serves the broad "Indian brand discovery" positioning (decision 2026-07-26, see §2).

**Business Objective**: Remove the three classes of noise that currently corrupt validation data — buried reason-to-choose, template/trust debris, and forfeited brand-page comparisons — so outbound clicks measure *preference*, not confusion.

**Positioning decision (resolved 2026-07-26)**: Mela is **Indian brand discovery for everyone** — brands that have grown up in India's domestic market and already have experience exporting globally. Family/baby is one category among equals, not the wedge. All copy, title tags, and category ordering align to this.

**Primary Success Metric**:
- **Outbound click-through rate (OCTR)**: % of sessions with ≥1 click out to a brand store. Baseline measured for 2 weeks post-instrumentation-verify; success = **+30% relative lift** post-P0/P1 ship, sustained over 2 weeks.

**Secondary Metrics**:
- Homepage → vetting-strip interaction rate (new event): ≥15% of homepage sessions
- Brand page → product-level outbound (redirect flow) rate on the 5 flagship brands: 2× the non-flagship average
- Bounce rate on `/brands/:brandSlug`: −20%
- Pre-redirect sentiment "helpful" share (existing modal): directional ≥70%

> **Legal constraint (roadmap §P0-A)**: Mela operates as a curated directory under a personal name — **no affiliate income**. OCTR is a validation/engagement metric, not a revenue metric. No copy in this PRD's scope may imply retailer status or commission relationships.

---

## Build Status Summary *(updated 2026-07-26)*

| Item | Priority | Status | Notes |
|------|----------|--------|-------|
| P1.1a brand template v2 mockups (mobile primary + desktop) | P1 | ✅ Design approved | `nimbalyst-local/mockups/brand-storefront-v2-fizzy-goblet-mobile.mockup.html` (+ desktop, + current-page replica) |
| P1.1b data contract + seeding scripts | P0/P1 | ✅ Shipped to dev | Exporter + seeder updated; **19 brand profiles seeded on dev** with `brandCity/Country/StoreUrl/Social/Craft` + `melaVetted`; prod not yet seeded |
| Flagship + active-brand content | P1 | ✅ Done (1 gap) | All 19 active brands: dash-free taglines/stories + craft chips in `shopify_brands.py`; chips tightened + payload-only, **reseeded to dev 2026-07-26** (API-verified); content pack in `product/content/flagship-brand-content.md`; **open: Ankid `brand_hq`** |
| P0.3 brand-name fix | P0 | ✅ Done on dev | "Fizzy Globlet" → "Fizzy Goblet" (displayName + lastName) via `scripts/temp/fix-fizzy-goblet-name.js`; full 19-name audit not yet formalized |
| P0.5 positioning copy | P0 | ✅ Strings approved | `product/content/positioning-copy.md`; **not yet applied** to en.json / MelaHomePage.js / CategoryPage.js |
| P0.4 SEO title templates | P0 | ⚠️ Specified | New strings live in positioning-copy.md §3–4; application pending |
| P0.1 vetting strip · P0.2 debris sweep · P0.6 OCTR verify | P0 | ❌ Not started | Frontend/build work |
| P1.1 brand page hero band build | P1 | ✅ Shipped to dev (reworked) | Built, then the outbound CTA reworked same-day per the no-exit-door decision (see P1.1 + REWORK ACs); 27/27 tests passing; live-verified `/brands/fizzy-goblet` |
| P1.2 category merchandising | P1 | ❌ Not started | Build work |
| P1.3 homepage editorial modules | P1 | ✅ Concepts approved / ❌ build | Spec `product/content/homepage-editorial-modules.md` + mobile mockup; data contract in P1.3b; build pending |

---

## 1. Problem Statement

### Current State
The 2026-07 design review found the shipped hero (per `homepage-redesign-prd.md`) has substantially answered F-002 above the fold: 3-second India signal, honest wedge copy ("The best brands from India rarely reach US shelves… then buy on each brand's own store"), trust chips, editorial typography. But the hypothesis test is rigged against itself in three ways:

1. **The proof is buried.** The vetting story ("Every Brand Here Earned Its Place," "How We Vet Every Brand," US-shipping/US-card FAQ) sits ~7,500px down a 10,073px homepage. The core reason-to-choose vs. all four defaults is invisible on first load, while ~8 undifferentiated product carousels (the exact F-001 "wall of listings") fill the space between.
2. **Trust debris contaminates the signal.** Sharetribe template leftovers — footer "© 2024 Your marketplace," "Post a new listing" link, "Search listings…" placeholder — plus an internal "🏆 Add certifications" admin CTA rendered on every public brand card, mismatched SEO title templates (Fashion page titled "Authentic Indian Baby Products"; `/brands` titled "Organic Baby Brands | GOTS Certified"), and a misspelled flagship brand ("Fizzy **Globlet**") on the hero and brand page. Visitors who bounce on credibility produce data indistinguishable from visitors who prefer Amazon.
3. **Brand pages forfeit the hardest comparison.** `/brands/:brandSlug` is where Mela must beat the brand's own Shopify store, and it currently offers strictly less: pixelated logo, one-line tagline, 308 products in a flat grid, story hidden behind an About tab, no vetting badge, no visible bridge to the brand's own store despite that being the model. Category grids compound this: `/categories/Fashion` is ~90% one brand with $3 utility items ranked high, reading as a thin single-brand outlet.

### User Pain Points (persona lens)
- **Sarah (Conscious American Parent)**: needs the vetting/safety story before anything else; it's the last thing she'd scroll to. Template debris reads as scam-risk → instant bounce.
- **Priya / Arun (Mixed-heritage & second-gen)**: want the discovery narrative and brand stories — the thing Instagram gives them loosely and Mela should give them curated. Flat grids give them neither.
- **Neha (First-gen immigrant)**: already knows some brands; misspelled brand names and one-brand category grids destroy the "they know Indian brands better than I do" claim.

### Business Impact of Inaction
Every week of traffic against the current storefront produces unusable validation data: we cannot distinguish "rejected the hypothesis" from "bounced on a template footer." The homepage-redesign and trust-signal investments already shipped are not being measured fairly.

---

## 2. Goals & Non-Goals

### Goals
1. Make the reason-to-choose legible within the first viewport of every entry page.
2. Eliminate every identified trust-debris item (template leftovers, admin leaks, SEO template mismatches, brand-name typo).
3. Ship a brand-page template that adds curation value over the brand's own DTC page; fully populate 5 flagship brands.
4. Fix category merchandising so assortment reads as multi-brand and curated.
5. Align all copy/meta to the resolved positioning: *proven Indian brands, export-ready, discovered in one place*.
6. Verify OCTR instrumentation end-to-end so the validation metric is trustworthy from day one.

### Non-Goals
- No new hero redesign (shipped hero is working; we extend, not replace).
- No review system, wishlist expansion, or order tracking (separate PRDs).
- No mobile-breakpoint redesign this cycle (audit blocked by tooling; tracked in §8 Risks).
- No monetization changes of any kind (legal constraint).
- No full population of all 19 brand pages (template + 5 flagships only; rest inherit template with existing one-liners).

---

## 3. User Stories

| As a... | I want to... | So that... | Priority |
|---------|-------------|------------|----------|
| First-time visitor (any persona) | understand within one screen why Mela beats the stores I already use | I have a reason to explore instead of bounce | P0 |
| Sarah | see how brands are vetted before I see products | I trust the assortment enough to browse | P0 |
| Any visitor | never encounter placeholder/admin UI | the site feels like a real, cared-for destination | P0 |
| Priya | read a brand's story, craft, and India origin on its Mela page | Mela adds context I can't get from the brand's own store | P1 |
| Neha | see brand names spelled correctly and assortment beyond one brand per category | I believe Mela actually knows these brands | P0 (typo) / P1 (merchandising) |
| Arun | jump from a brand page to the brand's own store with clear expectations | the discovery→brand-store model feels intentional, not broken | P1 |
| PM | trust outbound-click data | validation decisions are grounded | P0 |

---

## 4. Feature Requirements

### Must Have (P0) — "Clean the test tube" *(target: ship first)*

**P0.1 — Vetting strip on homepage, above the fold**
- Compressed trust band directly under the hero (before the first product carousel): "19 brands · hand-vetted · ship to all 50 states · US cards verified" with anchor-link to the existing vetting section.
- Reuses copy/data from the shipped "How We Vet Every Brand" section — no new claims.
- Analytics: impression + click events (`vetting_strip_view`, `vetting_strip_click`).

**P0.2 — Trust-debris sweep**
- Footer: replace "© 2024 Your marketplace" with correct Mela copyright; remove "Post a new listing" from buyer-facing footer (align with `footer-legalese-prd.md` work, don't duplicate it).
- Search placeholder: "Search listings…" → "Search Indian brands & products".
- Remove/role-gate "🏆 Add certifications" CTA on public `/brands` cards (visible only to brand-owner/admin roles).
- Remove $0 promo SKUs (e.g., "Limited Edition FREE Bag") from all public grids.

**P0.3 — Brand-name data fix**
- Correct "Fizzy Globlet" → "Fizzy Goblet" in brand record (hero card, brand page H1, title tag).
- One-pass audit of all 19 brand names/slugs/taglines against the brands' own sites.

**P0.4 — SEO title-template repair**
- Per-page-type title templates: category pages interpolate the category ("Fashion — Curated Indian Brands | Mela"), `/brands` reflects the full directory (drop "Organic Baby"/"GOTS" claims unless verifiably true), homepage aligns to positioning (drop "Sustainable … for Families").
- Ties into `seo-aeo-category-brand-pages-prd.md`; this PRD only covers correcting false/mismatched templates, not the full SEO build-out.

**P0.5 — Positioning copy alignment**
- Hero H1/subhead, homepage meta title/description, `/brands` H1 kept, and `/categories` intro copy audited against the resolved positioning: Indian brands, proven domestically, export-experienced, all categories equal.
- "for Your Family" framing removed from hero H1 (family remains a category entry, not the promise).
- **Approved strings for every surface live in `mela-docs/product/content/positioning-copy.md`** (added 2026-07-26): exact current→new mapping per en.json key and file line, including the CategoryPage title fix that closes the P0.4 bug, unverifiable-claim removals (GOTS/organic/"10,000+ parents"), and HeroSection.js defaultMessage drift fixes.

**P0.6 — OCTR instrumentation verification**
- End-to-end verify outbound-click tracking (existing `crossshop-tracking-prd.md` events + pre-redirect modal) fires on every outbound path: product-card redirect flow (`category`/`product_id` populated — primary OCTR signal) and the About-tab "Brand website" link (`category`/`product_id` both `null` — the existing brand-level shape, reported separately; no new tracking field needed since there is exactly one brand-level trigger post-rework).
- Define OCTR dashboard query; capture 2-week baseline before P1 ships.

### Should Have (P1) — "Win the comparisons"

**P1.1 — Brand page template v2** (`/brands/:brandSlug`)
- Above the grid: brand hero band — high-res logo, lifestyle/banner image, brand one-liner, **story summary inline** (first ~2 paragraphs of About, no tab required), "Mela Vetted" badge (per `trust-conversion-signals-prd.md` §3.4), India-origin/craft line, and an **on-Mela primary CTA** ("Browse {N} Products ↓") with expectation-setting microcopy.
- **Decision (2026-07-26): no outbound store link in the hero band or anywhere above the product grid.** Outbound happens at *purchase intent only* — the existing listing-level redirect flow through the pre-redirect trust sheet. Rationale: a brand-page exit door trains shoppers to bypass Mela and go direct (fatal with no affiliate tracking and a future marketplace model); product-level outbound is also the cleaner OCTR signal (intent, not ambiguity). `brandStoreUrl` remains seeded and is consumed only as a small "Brand website" link inside the About & Story tab, alongside `brandSocial`.
- Grid below retains Featured / occasion rows / All Products, but All Products defaults to curated sort (hero products first, accessories/basics demoted).
- Template ships for all 19 brands (graceful with existing data); **5 flagship brands fully populated** with story copy + imagery. Flagships: Fizzy Goblet (footwear), House of Chikankari (fashion), Ankid (baby/kids), Vilvah Store (beauty), Kaunteya (home). **Approved copy for all five lives in `mela-docs/product/content/flagship-brand-content.md`** (taglines, hero summaries, craft chips, About tab stories, plus execution notes for folding copy into `shopify_brands.py` and a proposed `publicData.brandCraft` field). 
- Supersedes the `/u/{user-id}`-era assumptions in `brand-storefront-prd.md` where they conflict; that PRD's storytelling/trust modules are the content spec.

**P1.1a — Approved mockups** *(added 2026-07-26; design source of truth for build)*

Mockups live in `nimbalyst-local/mockups/` with a pixel replica of the current page in `nimbalyst-local/existing-screens/brand-storefront-page.mockup.html` for before/after comparison. **Mobile is the primary design surface; desktop is the adaptation.**

| File | Surface |
|------|---------|
| `brand-storefront-v2-fizzy-goblet-mobile.mockup.html` | **Primary — mobile 390px** |
| `brand-storefront-v2-fizzy-goblet.mockup.html` | Desktop 1280px |

Hero band composition (mobile order, top → bottom):
1. Full-bleed banner image, ~235px tall — first entry of `publicData.brandHeroImages` — with "Made in India" chip (bottom-right, indigo `rgba(26,26,78,.85)`) and 64px brand logo chip overlapping the banner's bottom-left edge
2. "Vetted by Mela" pill — indigo `#262261` bg, white uppercase 11px, check icon
3. Brand name — Fraunces 28px/600 `#1a1a4e` (desktop: 42px)
4. Tagline — Hanken Grotesk 15px `#636369`
5. Meta row — 12.5px `#7c7c83`, bullet-separated: `{city}, {country}` · `{N} products` · `Ships to all 50 US states` · `US cards accepted`
6. Story summary — 14px/1.65, left border 3px marigold `#f0a030`, first ~2 paragraphs of bio, inline "Read the full story →" link to About tab
7. Craft line chip — marigold-tint bg `rgba(240,160,48,.12)`, `✦ The craft: …` 12px/600
8. CTA (full-width on mobile, 48px min-height): single primary indigo **"Browse {N} Products ↓"** anchor to the grid. No outbound store link in the band (decision 2026-07-26, see P1.1) — `brandStoreUrl` surfaces only as a small "Brand website" link in the About & Story tab
9. Expectation microcopy — 12px centered: "**How Mela works:** browse and save here. When you buy, checkout happens securely on the brand's own store. US cards accepted, ships to all 50 states."

Below the band: tab bar (rename "About" → "About & Story"), Featured scroll, occasion panels (unchanged), All Products with curated-order note ("Curated order — hero products first, basics follow") and $0 promo SKUs excluded (P0.2). Hero band bg is warm cream `#fdfaf5`; all tokens from `marketplaceDefaults.css` (Fraunces/Hanken Grotesk, indigo `#262261`, marigold `#f0a030`, grid/card specs unchanged from `ListingCard`).

**P1.1b — Profile data contract & seeding** *(added 2026-07-26)*

The hero band reads from the brand user's Sharetribe profile. Pipeline updated to supply the new fields — run order (owner runs in a separate session):

```
1. python "Mela-scrapper-integrations/scrapper and classifiers/product scrappers/scripts/export_brand_content.py"
2. NODE_ENV=dev node product-listing-integration/scripts/seed-brand-profiles.js --dry-run   # verify
3. NODE_ENV=dev node product-listing-integration/scripts/seed-brand-profiles.js             # then --prod
```

| publicData field | Source (`shopify_brands.py`) | Consumed by |
|------------------|------------------------------|-------------|
| `brandCity` / `brandCountry` | `brand_hq` (parsed "Mumbai, India") | Hero meta row (BrandStorefront already destructures these) |
| `brandStoreUrl` | `base_url` | "Brand website" link in About & Story tab only (decision 2026-07-26; never above the grid) — **new frontend read** |
| `brandSocial` `{instagram,facebook,twitter,youtube}` | `brand_instagram` etc. | Hero/About social links — **new frontend read** |
| `melaVetted: true` | set by seeder for every seeded brand | "Vetted by Mela" badge — **new frontend read** |
| `brandCraft` | `brand_craft` (filled for all 19 active brands; placeholder `""` on inactive) | Craft chip in hero band — **new frontend read**; chip hidden when empty |
| `brandHeroImages` | `brand_hero_image_urls` | Banner image (already seeded by `update-brand-hero-image.js` — unchanged) |
| `bio` (native profile field) | `brand_tagline + brand_story` | Tagline (first sentence) + story summary (existing fallback chain) |

Verified 2026-07-26: export produces 54 brands — 54 with `storeUrl`, 43 with `country`; seeder passes syntax check and only writes fields present in `brand_content.json` (shallow merge; hero images and certifications untouched).

**P1.2 — Category merchandising rules** (`/categories/:level1`)
- Brand-diversity constraint: no more than N consecutive cards from one brand (N=4 proposed) when multiple brands exist in category.
- Ranking demotion for utility/basic items (e.g., inners, blanks) below hero products.
- Interleaved brand-tile module every ~2 grid rows: brand logo + one-liner + "See brand" link (reuses `BrandCardHome`).
- Keep and extend "Shop by Occasion" (Gifting / Diwali & Festivals) — identified as the strongest existing F-001 answer.

**P1.3 — Homepage carousel consolidation**
- Replace 2–3 of the 8 product carousels with editorial modules: brand spotlight (rotates flagships), "New from India this month," occasion entry. Net homepage length reduction target: ≥25%.

**P1.3a — Approved module concepts** *(added 2026-07-26; design source of truth)*
- Concept spec: `mela-docs/product/content/homepage-editorial-modules.md` — revised 11-section order, three editorial modules (A: Brand Spotlight with weekly flagship rotation; B: New from India recency row with per-brand cap; C: Craft Stories strip built from `brandCraft` + `brandHeroImages`), removal list (Home & Kitchen and Beauty carousels; "Shop Baby by Age" relocates to the Baby & Kids category page), and five new analytics events extending P0.6.
- Mobile mockup: `nimbalyst-local/mockups/homepage-editorial-modules-mobile.mockup.html` (includes the P0.1 vetting strip).
- Key constraint honored: all modules run off already-seeded data (rotation is date arithmetic) — zero CMS/content-ops burden.
- Section order confirmed as specified (2026-07-26): editorial-before-catalog stands; hero category chips carry the "shop by category" job, only Fashion + Baby & Kids product rows survive, Occasion stays high.

**P1.3b — Module C (Craft Stories) data contract** *(added 2026-07-26)*
- Tile title: `publicData.brandCraft`, used verbatim. The field is **payload only** (e.g. "juttis stitched by hand in Mumbai") — it carries no label; any "The craft:" label is UI text added by the component that wants it (brand-page chip: yes; Craft Stories tiles: no). No hand-written tile copy anywhere. Fallback safety rule: truncate at a word boundary near 45 characters with an ellipsis (should never trigger — see next line).
- All 19 active `brand_craft` strings were tightened for tile display on 2026-07-26 (≤45 chars, one unfamiliar craft noun max, always anchored by a place or plain-English verb; material jargon like "georgette" removed). Source of truth: `shopify_brands.py`, field spec in its header docstring.
- ✅ **Reseed done on dev (2026-07-26):** exporter + seeder rerun; 19 profiles updated, 0 failures; Fizzy Goblet spot-checked via Integration API (`brandCraft: "juttis stitched by hand in Mumbai"`, city/country/storeUrl/vetted all present). **Prod seeding still pending** — run with the rest of the prod rollout.
- Tile attribution: profile `displayName`. Tile image: `brandHeroImages[0]`. Tile link: brand page via `configBrands.js` slug.
- Eligibility: active brands with non-empty `brandCraft` AND ≥1 hero image; daily trio rotation by day-of-year over the eligible set.

### Nice to Have (P2)
- Lazy-load image placeholders (branded skeleton, not gray void) + eager-load first two rows.
- Fix carousel scroll-trap (vertical wheel captured by horizontal rows).
- Occasion modules on brand pages (per `brand-storefront-occasion-module-prd.md`).
- Feedback widget ("How's your Mela experience?") repositioned so it never overlaps carousel content.

---

## 5. UX Requirements

- **Vetting strip**: single row, no carousel, must not push hero CTA below fold at 1280×720; links smooth-scroll to vetting section.
- **Brand hero band**: must render acceptably with minimal data (logo + one-liner only) — no broken/empty modules for the 14 non-flagship brands.
- **Outbound store link**: always visually distinct from in-Mela navigation; passes through the existing pre-redirect trust sheet/sentiment modal; opens brand store in new tab.
- **Empty/loading states**: product grids show branded skeletons; no blank gray cards on first paint.
- **Copy tone**: confident curator, not retailer ("We vetted…", "Discover…", never "Buy from us").
- **Mobile-first**: mobile (~390px) is the primary design surface for all new components — design, build, and verify mobile before desktop. Desktop is the adaptation (see P1.1a mockups). Formal on-device audit remains a follow-up (§8).

---

## 6. Acceptance Criteria

**P0**
- [ ] Vetting strip visible without scroll at 1440×900 and 1280×720; both analytics events fire.
- [ ] Zero instances of "Your marketplace," "Post a new listing" (buyer UI), or "Search listings…" in rendered output.
- [ ] "Add certifications" absent from `/brands` for logged-out and buyer sessions; present for brand-owner role.
- [ ] "Fizzy Goblet" spelled correctly everywhere it renders; 19-brand name audit logged.
- [ ] `/categories/Fashion` title contains "Fashion" and no baby-product claims; `/brands` title makes no GOTS/organic claim; homepage title reflects resolved positioning.
- [ ] Hero H1 contains no family-first framing; meta description matches.
- [ ] $0 SKUs excluded from all public grids.
- [x] Test outbound click on: product redirect flow and About-tab "Brand website" link → both fire `brand_clickout`, distinguished by `category`/`product_id` (populated vs. `null`); OCTR dashboard query documented (product-level redirects = primary OCTR; brand-level reported separately). Verified 2026-07-26 (`crossshop-tracking.md` §3).

**P1**
- [x] All 19 `/brands/:brandSlug` pages render template v2 without empty-module artifacts (band degrades gracefully when `brandHeroImages`, `brandCity`, or `brandStoreUrl` are absent).
- [ ] 5 flagship pages show story summary, banner imagery, vetted badge, and the on-Mela "Browse {N} Products" primary CTA above the grid, matching the updated mockups (P1.1a).
- [x] **REWORK (decision 2026-07-26), done same day**: outbound store link/CTA removed from the hero band — a prior pass had implemented it there and checked this AC off; it has now been undone. Hero band's sole CTA is the on-Mela "Browse {N} Products" anchor. `brandStoreUrl` renders only as a plain "Brand website" link in the About & Story tab (new tab), still routed through `openBrandStorefront`/`RedirectTrustSheet`. Product-level redirect flow is unchanged and remains the only purchase-path outbound. Test suite updated and passing (27/27, 2 pre-existing skips unrelated to this change).
- [ ] Seeding run completed: `brandCity`/`brandCountry`/`brandStoreUrl`/`brandSocial`/`melaVetted` present on all seeded brand profiles (spot-check 5 flagships via Integration API).
- [ ] Fashion category first 24 cards contain ≥3 distinct brands (when inventory allows) and zero utility-basic items in the first 8.
- [ ] Homepage total scroll height reduced ≥25% from 10,073px baseline; vetting section reachable ≤2 viewports sooner.
- [ ] Every AC above verified **mobile-first at 390px** (primary surface), then desktop 1440px.

---

## 7. Success Metrics & Measurement

| Metric | Baseline | Target | Instrument |
|--------|----------|--------|------------|
| OCTR (primary) | measure 2 wks post-P0.6 | +30% relative post-P1, sustained 2 wks | crossshop events + dashboard |
| Vetting strip interaction | n/a (new) | ≥15% of homepage sessions view; ≥4% click | new events |
| Flagship brand-page outbound rate | n/a | 2× non-flagship average | crossshop events segmented by slug |
| `/brands/:brandSlug` bounce | current GA | −20% | GA |
| Pre-redirect sentiment "helpful" | current | ≥70% directional | existing modal + Airtable |

**Decision rule**: if post-P1 OCTR lift <10% after 4 weeks with clean instrumentation, treat as hypothesis signal (not execution noise) and escalate to strategy review before further storefront investment.

---

## 8. Dependencies & Risks

- **Sharetribe constraints**: footer links/copyright partially live in Sharetribe Console (coordinate with `footer-legalese-prd.md` owner; legal copy is itself a launch blocker). Role-gating the certifications CTA depends on how brand-owner roles are modeled in Flex.
- **Content lift**: 5 flagship brand stories + imagery need sourcing from brand partners — longest lead-time item; start outreach at P0 kickoff. (Supply-side respect: request, don't scrape.)
- **Merchandising data**: brand-diversity and demotion rules require category inventory metadata (product type flags); may need enrichment-pipeline support (`enrichment-pipeline-stage2-update-prd.md`).
- **Mobile audit gap**: 2026-07-26 review could not exercise true mobile breakpoints (browser-zoom tooling limitation). Risk: mobile-specific trust debris unreviewed. Mitigation: responsive dev-tools pass in AC; schedule device audit as follow-up.
- **Single-brand categories**: diversity rules can't fix genuinely thin categories; if Fashion remains ~1 brand after rules, that's a supply problem — flag to brand-partnerships, not more UI.
- **Baseline contamination**: P0 trust fixes will themselves move OCTR; baseline must be captured *after* P0 ships, before P1 (sequencing matters).

---

## 9. Execution Runbook (for the build session)

All design/content/data decisions are made; this section is the build order. Sources of truth: `product/content/positioning-copy.md` (strings), `product/content/flagship-brand-content.md` (brand copy), `product/content/homepage-editorial-modules.md` (P1.3 spec), `nimbalyst-local/mockups/*` (visual specs, mobile primary), P1.1b/P1.3b (data contracts). Dev Sharetribe is fully seeded and API-verified as of 2026-07-26 — no data work before building.

**Order (dev):**
1. **Apply positioning strings** — en.json keys, `MelaHomePage.js:20/23`, `CategoryPage.js:181`, plus the two `HeroSection.js` defaultMessage drift fixes. Exact current→new mapping in positioning-copy.md §1–5 (closes P0.4 + P0.5).
2. **P0.2 debris sweep** — footer copyright, "Post a new listing" removal (buyer UI), search placeholder, role-gate "Add certifications" on `/brands`, exclude $0 SKUs from grids.
3. **P0.1 vetting strip** — copy and layout in the P1.3 mockup (top band); events `vetting_strip_view`/`vetting_strip_click`.
4. **P0.6 OCTR verification** — exercise all outbound paths, document the dashboard query, **start the 2-week baseline clock** (baseline must begin after steps 1–3, before any P1 ships).
5. **P1.1 brand template v2** — build against the mobile mockup + P1.1b fields (`brandStoreUrl`, `melaVetted`, `brandCraft`, `brandCity/Country`, `brandSocial`); graceful degradation for the 14 non-flagship brands.
6. **P1.2 merchandising rules** — brand-diversity cap (N=4 proposed), utility-item demotion, interleaved `BrandCardHome` tiles.
7. **P1.3 editorial modules** — build A/B/C per spec + P1.3b; verify ≥25% homepage length reduction; five new events.
8. Verify all ACs (§6) mobile-first at 390px, then 1440px.

**Prod rollout checklist (after dev validation):**
- [ ] Seed prod profiles: `export_brand_content.py` → `NODE_ENV=production node scripts/seed-brand-profiles.js --dry-run` → real run
- [ ] Fix "Fizzy Globlet" on **prod** (`NODE_ENV=production node scripts/temp/fix-fizzy-goblet-name.js` → `--apply`; dev-only so far)
- [ ] Deploy web-client changes

**Open facts (not blockers, resolve when known):**
- Ankid `brand_hq` city — confirm with brand, fill in `shopify_brands.py`, reseed
- Formal 19-brand name audit against brands' own sites (only Fizzy Goblet verified so far)

---

## 10. Out of Scope / Future Considerations

- Full mobile-first redesign pass (follow-up after device audit).
- Review/rating system, saved-items expansion (`saved-items-pasand-prd.md`).
- Editorial content program (stories/journal) — natural next step if OCTR validates.
- Populating the remaining 14 brand pages to flagship depth (post-validation).
- A/B testing hero framings — positioning was decided, not tested; revisit only if validation fails cleanly.
- Occasion-module expansion beyond existing surfaces.
