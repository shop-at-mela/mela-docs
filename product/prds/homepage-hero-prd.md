# Homepage Hero PRD (Cold-Load Value Prop)

## Executive Summary
**Feature**: Rework the homepage hero so it answers "What is this? / Why does it exist? / What do I do here?" in the first 5–10 seconds — including the guaranteed **cold-load state that renders before the async brand carousel arrives**.
**Target URL / Entry Point**: `/` (www.shopatmela.com) — `MelaHomePage` → `HeroSection`
**Target Users**: All four Mela personas, with the first-impression failure most acute for first-time visitors (Sarah, Arun) and diaspora shoppers evaluating "how is this different from Amazon?" (Neha, Priya).
**Business Objective**: Convert the first fold from a "clean baby SaaS catalog" first impression into a legible discovery value-prop, reducing bounce and lifting the primary hero → BrandsPage action.
**Primary Success Metrics**:
- Homepage bounce rate: **−10% to −15%** vs. current baseline
- Hero primary CTA click rate (`homepage_hero_cta_click`): **establish baseline → +15%**
- Cold-load parity: **no measurable bounce-rate delta** between sessions that saw the carousel and sessions where it was still loading/absent (today the cold-load state is materially weaker)

> **Relationship to `homepage-redesign-prd.md`**: This PRD **supersedes and subsumes** three still-unbuilt P1 items from that PRD — *Hero trust-model callout*, *Featured artisan story in hero area* (reframed as the Tier 0 "why" line + optional static brand callout), and the *hero portion* of WhyIndia. The **full WhyIndia below-fold section** and all category/occasion/Coming-Soon work remain owned by `homepage-redesign-prd.md`. Where the two touch, this PRD wins for the hero; that one wins below the fold.
>
> **Consolidation (2026-07-09):** hero strategy that had strayed into `homepage-redesign-prd.md` §11 in a later session — the **breadth/scale counter** (§4 T1-7), the **QA-pseudo-production env reality** (§12), **Bet-1/Bet-2 staging**, and **affiliate-native image sourcing** (§10) — is folded into this PRD. Redesign §11 is now a pointer here; its **Appendix A** retains the explored editorial-hero roster/picks as reference. The one unresolved content conflict from the merge — keep vs. drop the brand carousel — is logged in §0 Open Decisions.

> **Scope guard**: This PRD is **Tier 0 + Tier 1** of `mela-docs/uxr/homepage-hero-analysis-handoff.md`. Tier 2 (below-fold architecture) and Tier 3 (validation-gated typography/photography) are explicitly **out of scope** and listed in §10.

---

## 0. Status & Session Resume (read first)

**Last updated:** 2026-07-13 · **State:** Tier 0 + Tier 1 **built, shipped, and live-reviewed**; a post-build UX/panel **improvement pass** and a **copy-subtraction + India-signal refinement** are also shipped (see §4 *Built* + §13 changelog). **New (2026-07-12):** a multi-designer panel produced the **full 55-brand onboarding priority** (§12A, canonical); the brands sheet is re-sequenced to match. **New (2026-07-13):** a content-strategy + craft-legibility critique **refined the first-fold order** (§12A.1) — The Nesavu in, Baby Forest out of the fold, Nicobar demoted, Isharya re-justify-or-swap open; `configBrands.js` re-sequenced to match. Remaining: mobile-fold check at 375px + analytics baseline; hero-visual direction exploration (separate session — see §13 follow-ups).

### Done
- ✅ PRD drafted (Tier 0 + Tier 1), grounded in the roundtable handoff, current `HeroSection.js`/`.module.css`, and `homepage-redesign-prd.md`.
- ✅ **Dev-lead technical review complete** — see §11. Verdict: **complexity Low, scope S**, no Sharetribe/duck/SDK work; the hardest AC (cold-load standalone) is nearly free because the hero already uses shared `textTop`/`ctaBlock` consts across all render branches.
- ✅ **Hero brand selection complete** (UXR, `/uxr`) — see §12. Recommended carousel set + slide order + production-ingestion priority.
- ✅ **Tier 0 + Tier 1 BUILT & live-reviewed (2026-07-10)** — T0-1 why-line, T0-2 pill eyebrow, T0-3 cold-load, T1-4 trust callout, T1-5 warm gradient, T1-6 ComingSoon removal, T1-7 breadth counter. Verified at `localhost:3000`.
- ✅ **Post-build improvement pass SHIPPED (2026-07-10)** — a UX review + first-principles expert/PM panel found the built hero *over-composed* (redundant text stack, carousel contradicting the pitch, 2 AA gaps). Subtractive/curation fixes applied — see §13 changelog.
- ✅ **Copy-subtraction + India-signal refinement SHIPPED (2026-07-11)** — a second panel + founder feedback ("too much hero text; the brand card doesn't shout India"). Merged the why-line + trust callout into **one** line (deleted the redundant callout); added a **"Handcrafted in [City], India"** craft-origin line to the hero brand card. See §13.

### Decisions locked this session (do not re-litigate)
- **`heroSubheadline` key = repurpose, not new.** `SectionMelaHero.heroSubheadline` already exists in `en.json` (line ~640) but is **never rendered** — reuse it for the T0-1 "why" line. Zero live impact.
- **Error state = reuse the no-brands branch**, do not build a separate `fetchError` branch (§11 explains why; ACs in §7 updated accordingly).
- **Hero carousel brands — onboarding priority (canonical, 2026-07-12, §12A):** the full 55-brand ranking from the multi-designer panel; the brands sheet is re-sequenced 1→55 to match. Static hero imagery still draws from **Fizzy Goblet + Suta/Nicobar** first. *(The earlier QA-scoped Fizzy → Nicobar → Baby Forest → Banjaaran set is superseded — see §12B.)*
- **Hero first-fold order — refined (canonical for the fold, 2026-07-13, §12A.1):** **Fizzy Goblet → Suta → Isharya → The Nesavu → Nicobar → Kaunteya → Banjaaran Studio → House of Chikankari.** Refines the 2026-07-12 panel order: **The Nesavu** replaces **Baby Forest** in the fold (visual India-shout vs. invisible ayurveda story), **Nicobar** demoted #3→#5 (never the isolated lead slide), **Isharya** moved to the #3 jewelry slot (re-justify-vs-Tarinika **open** — see Open decisions #5). `configBrands.js` `CURATED_BRAND_SLUG_ORDER` re-sequenced to match. §12A's 55-brand *onboarding* ranking is unchanged; only the hero *display* fold moved.

### Open decisions
1. ~~**Warm gradient value**~~ — **RESOLVED & shipped:** `#fdfaf5 → #f7f1e8` (T1-5).
2. **T2-7 static brand callout** — held (not shipped); still the only item needing fresh weekly copy.
3. ~~**Brand carousel — keep / swipe-only / drop**~~ — **RESOLVED (2026-07-10): keep-but-simplify.** The post-build panel confirmed the carousel was contradicting the pitch (store chrome + wrong brands), so rather than drop it, the improvement pass **curated its order, stripped the store chrome (price/heart), and added a pause control + reduced-motion** (§13). Cold-load core still stands without it (T0-3). Revisit "drop for a single static image" only as the Bet-2 imagery test (§10).
4. **Mobile fold (open)** — at 375–414px the trimmed left column may still push the CTA below the fold; needs a real-device check (browser tooling couldn't constrain below the desktop breakpoint).
5. **Isharya vs. Tarinika for the first-fold jewelry slot (open, §12A.1)** — Isharya is global-editorial statement jewelry (LA HQ), which mismatches the §12A "kundan/gold close-up" rationale. Either re-justify Isharya on "bold *modern* Indian jewellery," or swap to **Tarinika** (temple-inspired → stronger traditional India-shout). Decide once one of them ingests with live product photography.

### Next steps (resume order)
1. **Step 3 — F-002 product-classification probe** against `Mela-scrapper-integrations/scrapper_csvs/` — confirm the craft-forward vs. US-styled split with real listing data (§12 predicts a "mix of (a) generic + (b) curation-fix"). Cheap; gates imagery spend.
2. **Step 4 — Generate static hero imagery** in Blotato from Fizzy Goblet + Nicobar listings (per IG visual guide).
3. **Step 5 — Build Tier 0 + Tier 1** per §4/§7 (single coherent revision).
4. **Supply action (parallel):** push the 4 hero brands to production; prioritize **Suta** (handloom saree) and **Isharya** (jewelry) into QA→prod to fill the two biggest first-impression gaps (§12).
5. Reconcile social docs to real palette `#262261`/`#f0a030` (docs-only; web + Console already done).

---

## 1. Problem Statement

### Current State
The hero (`HeroSection.js`) renders, in DOM order: `<h1>` → brand carousel (async) → trust badges + primary CTA → 6 category pills. Three structural facts make the first fold fail the value-prop test:

1. **No "why" anywhere in the hero.** `textTop` (HeroSection.js:136–145) renders *only* the `<h1>`. A `.subheadline` style exists (HeroSection.module.css:105) but **no JSX ever renders a subheadline**. Question 2 — *why does Mela exist / why are these brands invisible without it* — is answered nowhere above the fold. This is the core failure and the root of F-001 ("no inspiration; how is this different from Amazon?").
2. **The most India-signaling element loads async.** The brand carousel is the richest cue, but it is fetched on mount (`onFetchFeaturedBrands`) and is frequently still loading — or empty/errored — during the critical 5–10s window. The loading, no-brands, and (implicit) error branches all render **h1 + CTA + pills with no carousel and no "why"** — a bare "clean baby SaaS" surface. This is the fragile cold-load path.
3. **The visual register contradicts the copy.** The teal/aqua gradient (`#f8fffe → #f1f8f6`, HeroSection.module.css:5) reads as generic wellness/baby-SaaS, giving no orientation cue (F-002) and reinforcing "catalog, not curation."
4. **Q3 contradiction.** Six category pills teach Amazon-style "shop by department," undercutting the "curated" claim, and today sit in the same visual zone as the primary discovery CTA rather than clearly subordinate to it.

### User Pain Points
- **First-time visitor (Sarah)**: Lands, sees a clean grid-ish hero with no signal of what Mela *is for*; bounces before the carousel resolves.
- **Diaspora shopper (Neha / Priya)**: "This looks like any store — why would I use it over Amazon or going direct?" The differentiation (discovery of hard-to-find Indian brands) is never stated.
- **Second-gen (Arun)**: No reason-to-believe in the first fold; the pills push him toward department browsing he doesn't navigate by.
- **All personas on a slow connection / cold cache**: get the weakest version of the page precisely when first impressions form.

### Business Impact of Inaction
- The single highest-leverage surface (first fold, every session) keeps under-converting.
- Paid/organic acquisition is taxed by a bounce driven by a fixable copy+CSS gap, not a product gap.
- The affiliate model surprise (browse here, buy on brand site) stays unaddressed until far down the page, eroding trust with exactly the first-time visitors we spend to acquire.

---

## 2. Goals & Non-Goals

### Goals
- Make the hero answer all **three orientation questions in the first fold**, with the **"why" (Q2) promoted into the hero as durable copy** that renders in *every* state.
- Guarantee the **cold-load hero stands alone** — passes all three questions on a plain (warm) background with **zero async content**.
- Resolve the **Q3 pill contradiction** by clearly subordinating category pills to the primary discovery CTA and labeling them as curated entry points, not a department directory.
- Land the **minimum viable visual shift** (warmer register, CSS-only) and the **trust-model callout**, and remove the **Coming Soon** trust liability.
- Keep the committed brand system: **navy `#262261` + marigold `#f0a030`**; primary CTA navy, marigold as accent.

### Non-Goals
- **No hero photography / generated imagery in this PRD.** On-theme lifestyle imagery is a *later, separately-gated* enhancement (Tier 3, §10). The cold-load hero must pass on copy + CSS **alone**, so imagery can never become a load-bearing dependency.
- **No typography change** (Fraunces/Hind/Devanagari faces are Tier 3, Arun-gated).
- **No block-print motifs, photo-collage hero, or serif display** from the reference mockup.
- **No below-fold restructuring** (WhyIndia section, product-grid reorder, density 8→4) — those are `homepage-redesign-prd.md` / Tier 2.
- **No new backend, no Sharetribe config changes** — copy, one component's JSX, CSS, and `en.json`.
- **No palette re-litigation** — navy/marigold are locked; coral is retired and shipped.

---

## 3. User Stories

| As a... | I want to... | So that... | Priority |
|---------|-------------|------------|----------|
| First-time visitor | Understand *what Mela is and why it exists* in one glance, before anything loads | I don't bounce mistaking it for a generic store | P0 |
| First-time visitor (slow/cold load) | Get the full value prop even while the brand carousel is still loading | my first impression isn't the weakest version of the page | P0 |
| Diaspora shopper (Neha/Priya) | See stated plainly *why these brands are hard to find without Mela* | I understand the differentiation from Amazon | P0 |
| Any visitor | See one clear primary action, with category shortcuts visibly secondary | I'm guided to discovery, not dropped into department browsing | P0 |
| Sarah / Arun (no prior brand relationship) | Learn up front that I browse on Mela and buy on each brand's own store | I'm not surprised by the redirect and don't distrust it | P1 |
| Any visitor | Feel the page is warmer/more intentional than a SaaS template | I get a light orientation cue without exoticized clichés | P1 |
| Any visitor | Not see "coming soon" placeholders implying the platform is unfinished | my trust isn't undercut | P1 |

---

## 4. Feature Requirements

### Must Have (P0) — Tier 0
- **T0-1 — Hero "why" line (Q2), rendered in every state — now ALSO carries the model-set message (merged with T1-4, 2026-07-11).** A subheadline directly under the `<h1>` inside `textTop` (renders in loading, no-brands, error, *and* loaded branches). It states *why these brands are invisible in US stores + what Mela does + where you buy* in **one line** (founder feedback: shoppers don't read paragraphs). **Shipped copy (§6):** *"The best brands from India rarely reach US shelves. Discover them here — then buy on each brand's own store."* The tail ("buy on each brand's own store") now does T1-4's job, so the separate trust callout was removed. Affiliate-precision: "rarely reach," never "unavailable."
- **T0-2 — Resolve the Q3 pill contradiction.** Category pills must be (a) visually and positionally **subordinate to the primary CTA** (below it, lighter weight), and (b) **labeled** as curated shortcuts using the existing `.pillsLabel` hook — e.g. eyebrow text **"Or jump into a category"**. Pills stay functional and keep their current routes; this is a hierarchy + framing change, not a removal.
- **T0-3 — Cold-load hero stands alone (hard acceptance criterion).** In the loading, no-brands, and fetch-error states — i.e. with **no carousel and no async content** — the hero must still render h1 + the T0-1 "why" line + primary CTA + T1-4 trust callout, and must pass all three orientation questions on the warm static background. **Error handling reuses the existing no-brands branch** (when `fetchError` is set, `brandsWithProducts.length === 0`, so the hero already falls through to that branch) — a raw error must never be surfaced to a first-time visitor. No separate `fetchError` branch is required; see §11.

### Should Have (P1) — Tier 1
- **T1-4 — Trust-model callout (subsumes `homepage-redesign-prd.md` P1).** ~~One matter-of-fact line near the CTA: "You browse here — then shop directly on each brand's own store."~~ **MERGED INTO T0-1 (2026-07-11).** Shipped 2026-07-10 as a standalone line, then the 2026-07-11 refinement found it *redundant* with the why-line's tail ("…buy on each brand's own store") — so the separate callout was removed and its message folded into the single why-line. The model-set message still renders in every state (now via T0-1). `SectionMelaHero.trustModelCallout` key remains in `en.json`, unused/harmless.
- **T1-5 — Minimum viable warm palette shift (CSS-only).** Replace the teal gradient (`#f8fffe → #f1f8f6`) with a warm paper/cream register (proposed `#fdfaf5 → #f7f1e8`; final value is design's call in dev-lead/ux-design review) and update the two dependent hard-coded `#f1f8f6` references in the pill wrapper fade (HeroSection.module.css:333) and any matching stops. Navy/marigold tokens unchanged. **No** typography, motif, or layout change.
- **T1-6 — Remove ComingSoonSection.** The "coming soon" badge is a trust liability on first impression. Remove the section from `MelaHomePage` render (component may remain in repo, unmounted). Note: `homepage-redesign-prd.md` AC currently marks this section as shipped — this PRD reverses that decision; update that PRD's AC accordingly.
- **T1-7 — Breadth/scale signal: dynamic counter, NUMERIC-ONLY, threshold-gated (folded from redesign §11; revised in the 2026-07-10 improvement pass).** A live credibility line answering "is this a real marketplace or a pop-up?" (Sarah). Compute from `getAllBrandIds().length` (`configBrands.js`) + `getPopulatedCategoryCount()` — grows automatically as intake lands, no copy change. **Renders ONLY as a real number, once `showBreadthNumber` is true (≥25 brands AND ≥4 categories):** *"N+ brands across M categories · shipped across the US."* Below threshold it **does not render at all** — the panel found the earlier qualitative label (*"Handpicked Indian brands across baby, fashion & beauty"*) redundant with the H1 + why-line, so breadth below threshold is carried by the labeled category pills, not a third restatement. At today's 13-brand supply the line is absent. Reads the **live env config = `allBrandIdsByEnv.development`** (deploy overrides `REACT_APP_ENV=development`; QA/dev = pseudo-production — see §12); **no dependency on the empty `.production` array**. Renders in the standalone core, so it survives cold-load. **Affiliate-precision:** never imply "unavailable"; frame as discovery. *(The unused `SectionMelaHero.breadthQualitative` key remains in `en.json`, harmless.)*

### Nice to Have (P2)
- **T2-7 — Optional static brand/artisan callout** (the survivable, copy-only half of the redesign PRD's "Featured artisan story"): a single specific, regionally-precise line (e.g. *"This week: handwoven khadi from a 4th-generation Bagru workshop"*) rendered as **static text** in the standalone hero, independent of the async carousel. No image (imagery is Tier 3). Must use regional specificity, never "Indian handweaving," per UXR cultural-framing.
- **T2-8 — `prefers-reduced-motion` and contrast pass** — ✅ **shipped in the improvement pass** (§13): autoplay starts OFF under `prefers-reduced-motion`; muted trust text darkened `#718096 → #5a6472` to clear AA.

### Built — Post-build improvement pass (2026-07-10, from UX + panel review)
- **T3-1 — Curated carousel order (replaces random).** `getCuratedBrandIds(count)` (`configBrands.js`) returns brands in the §12 priority order (craft-legible first, Western-styled last); `BrandsPage.duck.js` now calls it instead of `getRandomBrandIds`. Prevents the hero leading with US-DTC-looking brands (F-001/F-002).
- **T3-2 — Strip store chrome from the hero card.** New `showProductMeta` prop on `BrandCardHome` → `showPrice`/`showSave` on `ListingCardMini`; hero passes `false` to hide product **prices ($/₹) and the heart/save icon** (they read "store," contradicting T1-4). Defaults preserve prices/hearts on BrandsPage + FeaturedBrandPartners.
- **T3-3 — Carousel pause/play control (WCAG 2.2.2)** + reduced-motion (see T2-8). Visible toggle beside the dots; pausing clears the resume timer.
- **T3-4 — Subtract redundancy.** T1-7 breadth line gated to numeric-only (removed the qualitative restatement); breadth below threshold carried by the pills alone.

### Built — Copy-subtraction + India-signal refinement (2026-07-11, panel + founder feedback)
- **T3-5 — Merge why-line + trust callout → one line.** Founder: "too much hero text; shoppers don't read." The two lines shared a clause ("…buy on each brand's own store"); merged into one why-line, standalone callout deleted (see T0-1/T1-4). Hero is now **H1 + one line + CTA**.
- **T3-6 — Craft-origin cue on the hero brand card ("shout India").** Founder: "the brand card doesn't shout India." New `showCraftOrigin` prop on `BrandCardHome` renders **"Handcrafted in [City], India"** (deep-marigold `#b26a00`, AA-safe) under the brand name, built from the existing `brandCity`/`brandOrigin` location config with an **India fallback** (every Mela brand is Indian, so it always resolves). Hero-only (prop defaults `false`); BrandsPage/FeaturedBrandPartners unaffected. *Data note:* brands lacking a `brandCity` in their profile read the bare "Handcrafted in India" — populate `brandCity` to get "[City], India."
- **Deferred to a separate session:** hero-visual direction exploration (SVG jaali motif / craft texture / real photo) — a 3-way mockup was produced; see §13 follow-ups for the handoff.

---

## 5. UX Requirements

### Hero content model (all states)
The hero's **standalone core** = `{ h1, why-line (T0-1, now including the model-set message), primary CTA }` *(+ the T1-7 breadth line only above threshold)*. This core renders identically across **loading**, **no-brands**, **error**, and **loaded** branches. The brand carousel and the category pills are **additive**, never required for orientation. *(The separate trust callout was merged into the why-line on 2026-07-11 — T3-5.)*

### State matrix
| State | Renders | Passes Q1/Q2/Q3 without carousel? |
|---|---|---|
| Loading (fetch in progress) | standalone core + skeleton + pills | **Must = yes** |
| No brands configured | standalone core + pills | **Must = yes** |
| Fetch error (make explicit) | standalone core + pills (no carousel, no error UI dumped on user) | **Must = yes** |
| Loaded | standalone core + carousel + pills | yes (carousel is bonus) |

### Hierarchy (top → bottom, mobile DOM order)
1. `h1` (Q1)
2. **why-line** (Q2 + model-set) — one line
3. primary CTA "Explore Brands" → BrandsPage (Q3 primary action) *(+ breadth line above CTA only when T1-7 threshold met)*
4. brand carousel (loaded state only; social proof — with craft-origin cue T3-6, no price/heart, pause control)
5. **eyebrow label + category pills** (T0-2) — visibly secondary, below the primary CTA

> On desktop the existing 2-col grid (`headline`/`cta` left, `carousel` right) is preserved; the why-line and trust callout attach to the left column with the CTA. Pills remain full-width below the grid.

### Edge cases
- Long localized "why" copy must not push the CTA below the fold on a 360×640 viewport — cap to ~2 lines / ~160 chars; validate on smallest supported mobile.
- Trust callout and why-line must degrade gracefully to `defaultMessage` if `en.json` keys are missing (no blank space).
- Warm gradient must not reduce contrast of navy h1 text below WCAG AA.
- Removing ComingSoonSection must not leave a double-margin gap between the sections that flanked it.

---

## 6. Copy Changes

| Location (i18n key) | Element | Old | New (draft — confirm in review) |
|---|---|---|---|
| `SectionMelaHero.heroSubheadline` *(repurposed)* | Hero why-line (T0-1, +model-set) | "Handpicked baby, home, and fashion brands from India…" *(never rendered)* | **SHIPPED 2026-07-11:** "The best brands from India rarely reach US shelves. Discover them here — then buy on each brand's own store." |
| `SectionMelaHero.trustModelCallout` | Trust callout (T1-4) | — | ~~"You browse here — then shop directly on each brand's own store."~~ **Retired from render 2026-07-11** (merged into the why-line). Key remains, unused. |
| `SectionMelaHero.categoryPillsLabel` | Pills eyebrow (T0-2) | *(none; `.pillsLabel` unused)* | "Or jump into a category" *(shipped)* |
| `BrandCardHome.craftOrigin` *(new, T3-6)* | Craft-origin cue on hero card | — | **SHIPPED 2026-07-11:** "Handcrafted in {locale}" → e.g. "Handcrafted in India" / "Handcrafted in Jaipur, India" |
| `SectionMelaHero.brandCalloutWeekly` *(P2, not shipped)* | Static brand callout (T2-7) | — | "This week: handwoven khadi from a 4th-generation Bagru workshop" |

> **H1 is intentionally unchanged** in this PRD. The existing headline debate (value-led vs. origin-led) is logged in `homepage-redesign-prd.md` §6 and should be validated with analytics before any change — not bundled here.

---

## 7. Acceptance Criteria

### Cold-load / standalone hero (the whole ballgame)
- [x] With the brand fetch **loading**, the hero renders h1 + why-line (incl. model-set message) + primary CTA + pills; all three orientation questions answerable from that state alone.
- [x] With the brand fetch returning **zero brands**, same as above.
- [x] With the brand fetch **erroring**, the hero renders the same standalone core (via the existing no-brands branch) — no blank hero, no raw error, no carousel.
- [x] The why-line (which now carries the model-set message) is present in the DOM in **all** branches, not only the loaded branch. *(Trust callout merged into it — T3-5.)*

### Tier 0 content
- [x] A subheadline "why" line renders directly under the h1 in `textTop`.
- [x] The why-line uses discovery framing ("rarely make it to US shelves") and contains **no** "unavailable" phrasing.
- [x] Category pills render **below** the primary CTA and carry a visible eyebrow label ("Or jump into a category"); not peer to the CTA.
- [x] Pills retain their existing routes and count (no routing regression).

### Tier 1
- [x] Model-set message ("buy on each brand's own store") renders in every state — now **within the merged why-line** (T3-5), no separate callout.
- [x] Hero background is the warm register (`#fdfaf5 → #f7f1e8`); pill-fade color updated to match; navy/marigold tokens unchanged.
- [x] `ComingSoonSection` no longer renders on `/`. *(Layout-gap regression: still verify visually.)*
- [x] `homepage-redesign-prd.md` AC for ComingSoonSection updated (2026-07-10) to reflect this PRD's ownership.

### Improvement pass (2026-07-10)
- [x] Breadth line absent at current supply (numeric-only; 13 < 25) — verified live.
- [x] Carousel driven by `getCuratedBrandIds` (curated order), not random — verified in code + live (leads with a craft brand, not a Western-styled one).
- [x] Hero product thumbnails show **no price and no heart** — verified live.
- [x] Carousel **pause/play** toggle works (❚❚ ↔ ►) and stops rotation — verified live; autoplay OFF under `prefers-reduced-motion`.
- [ ] Carousel literally **leads with Fizzy Goblet** — ❌ blocked: Fizzy Goblet's featured listings aren't live in QA, so it's filtered out and Baby Forest (rank 2) leads. **Supply action:** publish Fizzy Goblet listings in QA.
- [ ] No regression: BrandsPage + FeaturedBrandPartners still show prices/hearts — *spot-check pending* (defaults preserve behavior).

### Copy-subtraction + India-signal refinement (2026-07-11)
- [x] Hero is **H1 + one line + CTA** — why-line and trust callout merged into a single line; standalone callout removed — verified live.
- [x] Hero brand card shows **"Handcrafted in [City], India"** under the brand name (deep marigold) — verified live (Baby Forest → "Handcrafted in India").
- [ ] Brands with a populated `brandCity` render "[City], India" — *depends on profile data; verify once a city-bearing brand leads.*

### Quality / regression
- [x] Navy h1, subheadline, CTA pass AA on the warm gradient; muted trust text darkened `#718096 → #5a6472` (~5.4:1).
- [x] `prefers-reduced-motion` respected — autoplay starts OFF for those users.
- [x] All new `en.json` keys exist with matching `id`s (breadthCount, trustModelCallout, categoryPillsLabel, pauseRotation, playRotation); JSON validated.
- [x] No regression in the loaded-state carousel (autoplay, swipe, dots, hover-pause) — plus a new pause/play control.
- [ ] Smallest supported mobile (360×640): primary CTA above the fold with the longest why-line — **still to verify on a real device** (see §0 open decision 4).

---

## 8. Success Metrics & Measurement

| Metric | Baseline | Target | Method |
|---|---|---|---|
| Homepage bounce rate | TBD (capture pre-ship) | −10% to −15% | GA4 — 1-pageview sessions / total, `/` entry |
| Hero primary CTA click rate | establish | +15% | GA4 event `homepage_hero_cta_click` |
| Cold-load parity | establish | no material bounce delta | GA4 — segment sessions by whether carousel rendered (fire `hero_carousel_shown` on carousel mount) vs. not, compare bounce |
| Pills click-through (post-demotion) | current | no collapse (guardrail) | GA4 `homepage_quicknav_click` — demotion should not zero out pill use |
| Trust callout comprehension | qualitative | fewer "is this a store?" reactions | next persona/UXR round + F-00x follow-ups |

> **Instrumentation note**: add a lightweight `hero_carousel_shown` event so cold-load parity is measurable; without it we can't prove the standalone hero worked.

---

## 9. Dependencies & Risks

### Dependencies
- **BrandsPage live** (already true — primary CTA already routes there).
- `en.json` keys in sync with JSX `id`s (missing key → silent `defaultMessage`).
- Coordinated edit to `homepage-redesign-prd.md` AC (ComingSoonSection reversal + trust-callout/why ownership) so the two PRDs don't contradict.
- Warm gradient value should be confirmed in dev-lead + ux-design review before merge (design's call within navy/marigold system).
- No backend / Sharetribe changes.

### Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| "Why" copy reads generic/marketing-fluff and doesn't actually differentiate from Amazon | Medium | Lead with the *specific* mechanism ("rarely make it to US shelves… buy on each brand's own store"); validate wording in UXR/persona pass before ship |
| Warm gradient drifts toward the rejected mockup paper (`#FBF5EA`) and reads "beige SaaS" | Low | Keep it a subtle shift, review against navy/marigold; it's a *register* nudge, not a redesign |
| Demoting pills tanks category click-through | Low–Med | Guardrail metric; pills stay functional and labeled, just subordinate |
| Removing ComingSoonSection loses a roadmap-signal some users liked | Low | Trust liability outweighs; roadmap signaling can return elsewhere later |
| Scope creep into typography/imagery (Tier 3) | Med | §2 Non-Goals + §10 hold the line; imagery gated on the F-002 product-classification probe |

---

## 10. Out of Scope / Future Considerations
- **Hero lifestyle imagery** (Tier 3) — **source = a brand's own official product photography** (affiliate-native; scraper CSV `Product Image URL`), credited *"discovered on Mela,"* **one brand's image at a time** (avoids cross-brand style clash). **AI-composited scenes and multi-brand collages are rejected** (fold from redesign §11): AI craft-imagery reads as inauthentic to Mela's craft-fluent diaspora audience; a collage adds focal-point chaos + exoticization risk. **Rights caveat:** confirm per-brand image-use permission before publishing — the copy-only hero (Tier 0/1) carries zero rights exposure. Staged as **Bet 2**: only after the Tier 0/1 copy hero (Bet 1) ships and moves bounce, A/B a single real brand photo vs. no image; if the arms don't separate, the image doesn't move bounce — stop investing in hero art. Still **gated on the F-002 probe** and a first Arun-persona reaction, and must remain additive — never a cold-load dependency.
- **Indian-accent typography** (Tier 3) — Hind (Indian Type Foundry), not a Devanagari-script face; only if post-ship testing still shows a coherence gap. High cliché risk.
- **Full WhyIndia below-fold section**, product-grid reorder, density 8→4, brand-stories-above-grid — all **Tier 2**, owned by `homepage-redesign-prd.md`.
- **H1 value-led rewrite** — validate with analytics first (logged in redesign PRD §6).
- **A/B testing** of hero copy variants — no infra today.
- **Sidecar items** from the handoff (canonical URL `.env` fix; Sharetribe footer audit) — ship independently, not part of this hero effort.

---

## 11. Technical PRD Review (Dev Lead, 2026-07-08)

**Technical Complexity: Low** · **Estimated Scope: S** — one component (`HeroSection.js` + `HeroSection.module.css`), `en.json` string adds, and a 4-line deletion in `MelaHomePage.js`. No duck, no SDK call, no Sharetribe config, no new component.

### Feasibility
| Requirement | Feasibility | Notes |
|---|---|---|
| **T0-1** why-line in every state | ✅ Straightforward | `textTop` is a **shared const** (`HeroSection.js:136`) reused by loading, no-brands, and loaded branches. Adding `<p className={css.subheadline}>` inside it propagates to all branches for free. `.subheadline` CSS already exists (`HeroSection.module.css:105`). |
| **T0-2** demote + label pills | ✅ Straightforward | Pills are **already positioned below the CTA** — `categoryPills` renders as a sibling after `heroContent` (`HeroSection.js:268`). Real work = add the unused `.pillsLabel` eyebrow (`.module.css:347`) + copy. Lower effort than PRD body implies. |
| **T0-3** cold-load standalone | ✅ Straightforward | Same shared-const mechanism: `ctaBlock` (`HeroSection.js:149`) is reused across branches, so the trust callout propagates too. Error handled by reusing the no-brands branch (see below). |
| **T1-4** trust callout | ✅ Straightforward | One line into `ctaBlock`; auto-renders everywhere. |
| **T1-5** warm gradient | ✅ Straightforward | Exactly **two** color literals: `.hero` gradient (`.module.css:5`) + pill-fade `#f1f8f6` (`.module.css:333`). Navy tints are already `rgba(38,34,97,…)` tokens — untouched. |
| **T1-6** remove ComingSoonSection | ✅ Straightforward | Delete import (`MelaHomePage.js:13`) + the `<section>` block (`152–155`). |
| **T2-7** static brand callout | ⚠️ Needs care | Fine as static text; don't make it look dynamic. Genuinely P2. |

### Sharetribe / data
- **None.** Nothing touches listing fields, custom attributes, or the SDK. The carousel's `fetchFeaturedBrands` is untouched — we strengthen what renders *around* it. All new content is static copy in `en.json`.

### Architecture
- **Component-only.** Modify `HeroSection.js` (JSX), `HeroSection.module.css` (2 literals + spacing), `en.json` (strings), `MelaHomePage.js` (remove ComingSoonSection). New file: a test.
- The existing **shared-const pattern (`textTop`/`ctaBlock`) is why T0-3 is cheap** — the "standalone core" already exists as a code structure.

### Resolved blockers/risks (folded into §0 decisions + §7 ACs)
- **`heroSubheadline` key already exists, unrendered** → repurpose it (not a new key).
- **No `fetchError` branch today** → when `fetchError` is set, `brandsWithProducts.length === 0`, so it already falls through to the no-brands branch (`HeroSection.js:184`) which renders the standalone core. Making it "explicit" is unnecessary; surfacing a fetch error to a first-time visitor would be worse. AC softened accordingly.
- **ComingSoon removal gap** → verify `brandsSection → trustSection` spacing (`MelaHomePage.module.css` `comingSoonSection` wrapper margin) doesn't collapse/double.
- **Contrast** → navy `#262261` h1 on the warm gradient is safe; re-check muted `#718096` trust-badge text at AA.

### Verdict
**Ready to build.** Clean **S** with an unusually favorable existing structure. Build Tier 0 + Tier 1 together as one revision per the handoff; hold T2-7 unless copy is ready.

---

## 12. Hero Brand Selection (UXR, 2026-07-08; onboarding priority added 2026-07-12)

**Source data:** brands sheet (`gid=704623254`) — **55 brands across all 5 categories** (Baby 25, Fashion 23, Jewelry 3, Beauty 2, Home 2). **Supply reality corrected 2026-07-09:** QA/dev serves as **pseudo-production** (deploy overrides `REACT_APP_ENV=development`), so the live set is `allBrandIdsByEnv.development` = **13 brands live today**, growing as QA-ready brands land — *not* "0 in production." The old "0 in production" framing below is stale; the ~11 QA-listing brands are effectively live/near-live, and the "Listings in Production" sheet column is irrelevant while QA = live.

### 12A. Onboarding priority — full 55-brand ranking (multi-designer panel, 2026-07-12) ⭐ CANONICAL
**This is the source of truth for onboarding order.** A four-designer UX panel (craft-legibility, DTC-conversion, diaspora-cultural, and systems/sequencing lenses) ranked **all 55 brands, unconstrained by QA/production readiness**, to answer: *in what order should Mela onboard so the hero carousel proves the F-002 claim and keeps proving it as supply grows.* **The brands sheet has been re-sequenced 1→55 to match this ranking** (row 1 = Fizzy Goblet … row 55 = Italian Shoes Company). The older 4-brand set in §12B below is **retained but superseded** — it was scoped only to the *then-live QA* brands, whereas this ranking is the full onboarding pipeline.

**Scoring rubric (weighted):** (1) India-shout at a glance ×3 — the F-002 fix, non-negotiable · (2) aspiration / modern taste ×2 — elevated, never costume/kitsch · (3) category-coverage value ×2 — jewelry/home/beauty are gaps, baby is core · (4) diaspora identity pull ×1 · (5) needs-explanation penalty. **Principle unchanged from §12B:** the carousel carries no copy; its only job is visual proof of *"distinctive Indian-craft brands you won't find at Target/Amazon,"* so the rule is "which brand makes that self-evident in one glance," not "which is readiest."

**Hero first-fold slide order — original panel ranking (2026-07-12); SUPERSEDED for the first-fold order by §12A.1 below, retained for rationale:**

| # | Brand | Category | Why it earns the slot |
|---|---|---|---|
| 1 | **Fizzy Goblet** | Footwear | Embroidered juttis = universal "handmade, Indian, not at any US mall." The undisputed lead. |
| 2 | **Suta** | Textile | Handloom sarees, 17k artisans — single most legible "craft you can't get here." |
| 3 | **Nicobar** | Lifestyle | Anti-cliché taste reset; proves *modern* India (defuses exotic-kitsch fear). |
| 4 | **Isharya** | Jewelry | Kundan/gold close-up = proven thumb-stop; fills the biggest category gap. |
| 5 | **Baby Forest** | Baby | Core vertical + ayurveda = heritage you can't buy at Target. |
| 6 | **Kaunteya** | Home | 24k-gold Pichwai bone china; luxury heritage; fills the home gap. |
| 7 | **Banjaaran Studio** | Fashion | Artisanal textile/color depth; reinforces "artisan discovery." |
| 8 | **House of Chikankari** | Fashion | Chikankari embroidery = quintessential, unmistakable Indian craft. |

*Sequence rhythm (systems lens): footwear → textile → lifestyle → jewelry → baby → home → fashion → fashion. First fold spans 6 categories; no two adjacent categories repeat until the tail.*

### 12A.1 — First-principles refinement of the first-fold order (content-strategy + craft-legibility critique, 2026-07-13) ⭐ CANONICAL for the first-fold order

A first-principles critique stress-tested §12A's first-fold order against the one thing the carousel actually does: **visual proof, no copy, each slide seen in isolation** in a rotation. It leaves §12A's full 55-brand *onboarding* ranking intact and adjusts only the hero's *first-fold display* order (plus one swap: The Nesavu in, Baby Forest out of the fold).

**Revised first-fold slide order:**

| # | Brand | Category | Change vs §12A | Why |
|---|---|---|---|---|
| 1 | **Fizzy Goblet** | Footwear | — | Unchanged; undisputed universal lead. |
| 2 | **Suta** | Textile | — | Unchanged; a draped handloom saree is the single most unambiguous India-shout. |
| 3 | **Isharya** | Jewelry | ↑ from #4 | Jewelry fills the biggest category gap. **Open:** the §12A "kundan/gold close-up" rationale mismatches the actual brand (bold contemporary/statement, LA HQ). Re-justify on "bold *modern* Indian jewellery," or **swap to Tarinika** (temple-inspired → stronger traditional India-shout). See Open decisions #5. |
| 4 | **The Nesavu** | Baby/Kids | **NEW to fold** (was §12A Tier 2 #15) | Replaces Baby Forest as the baby slot. A silk pattu pavadai / half-saree on a child is an *instant visual* India-shout; a baby-oil bottle is not. |
| 5 | **Nicobar** | Lifestyle | ↓ from #3 | Demoted. Nicobar *deliberately doesn't shout India* (the "taste reset"), so it fails axis #1 in isolation. Kept in the fold as a rhythm-breaker but **never the isolated lead slide** — the §12A "sandwiched between craft brands" defense doesn't survive a rotating carousel where each slide is seen alone. |
| 6 | **Kaunteya** | Home | — | Unchanged; Pichwai bone china fills the home gap. |
| 7 | **Banjaaran Studio** | Fashion | — | Unchanged. |
| 8 | **House of Chikankari** | Fashion | — | Unchanged. |

**Baby Forest** leaves the first fold — its ayurveda=heritage pitch is a *story* the no-copy carousel can't render — but stays at §12A onboarding #5 and becomes the **lead breadth-builder** in the display order.

**The six critique findings:**
1. **Nicobar fails India-shout ×3 in isolation** → demote to #5, never first-seen. A visitor who lands on the Nicobar slide alone sees a generic linen shirt = the exact F-001 failure; the rotation breaks the "sandwich" defense.
2. **Isharya is miscast against its own rationale** → it's global-editorial statement jewelry (LA HQ), not the "kundan/gold close-up" §12A claims. Re-justify or swap to Tarinika. **Open decision #5.**
3. **Baby Forest ranks on an invisible story** → swap the hero's baby slot to The Nesavu (visual India-shout); keep Baby Forest as core supply, not first-fold visual proof.
4. **Fashion-skew vs. baby-heavy catalog** → 5 of 8 first-fold brands are wearable fashion, but supply (and today's live set) is baby-dominant. The hero promises "fashion-forward Indian craft"; the landing catalog delivers "baby + fashion." Real promise/delivery risk on the click-through — monitor bounce on the hero → BrandsPage hop.
5. **Onboarding order ≠ display order** → §12A is the *onboarding/supply* ranking; the carousel *display* order among **live** brands is a distinct list (`getCuratedBrandIds` / `CURATED_BRAND_SLUG_ORDER`). Today 5 of the 8 first-fold brands don't render (Suta, Kaunteya, House of Chikankari not ingested; Fizzy/Isharya/Nicobar have empty `featuredProductIds`), so the *live* lead is still whichever craft brand has loaded products — the 8-brand fold is aspirational until supply lands.
6. **Diaspora pull is under-weighted (×1)** → the order optimizes the cold non-Indian's "tasteful curation" read (aspiration ×2) over the diaspora's recognition pull. ModiToys (§12A #11, purest diaspora hook) is a candidate *targeted* first-fold slide for baby/diaspora audiences; revisit the weight via A/B once supply allows.

**Code:** `configBrands.js` `CURATED_BRAND_SLUG_ORDER` re-sequenced to match (config-present brands only, in refined rank order). No component change.

**Full onboarding tiers (all 55; sheet rows in parentheses):**

- **Tier 1 — onboard first (hero-leading; shout India + aspirational + modern):** Fizzy Goblet (1) · Suta (2) · Nicobar (3) · Isharya (4) · Baby Forest (5) · Kaunteya (6) · Banjaaran Studio (7) · House of Chikankari (8)
- **Tier 2 — onboard next (strong rotation + category range):** Chidiyaa (9) · Needledust (10) · **ModiToys** (11, diaspora identity hook) · Daughters of India (12) · Payal Singhal (13) · Tarinika (14, shoot modern) · The Nesavu (15) · Gundi Studios (16) · Jodi Life (17) · Malabar Baby (18) · Bipha Ayurveda (19, fills beauty gap) · Shobhitam (20)
- **Tier 3 — breadth builders (weaker first-fold India-shout or need a story):** Gully Labs (21) · Erode (22) · Little Muffet (23) · Curio Cottage (24) · gauri and nainika (25, glam gowns / Western silhouette) · Vilvah Store (26) · Shumee (27) · Tiber Taber (28) · Aagghhoo (29) · Saphed Fashion (30) · Saphed Kids (31) · KG Label (32) · Masilo (33, soft eco-baby, low India-shout) · The Alternate India (34) · Pastels & Pop (35) · Gado Living (36) · Earthy Tweens (37) · My First Crayons (38) · Little West Street (39) · MiDulce Anya (40) · Aplito (41) · Ankid (42) · Baby Jalebi (43)
- **Tier 4 — onboard late / keep OFF the hero (Western-styled → featuring reinforces F-002):** SuperBottoms (44) · Pluchi (45) · ChooseKind (46) · Polite Society (47) · Neemans (48) · Comet (49) · Skillmatics (50) · Smartivity (51) · Brainsmith (52) · Kicks and Crawl (53) · MeeMee (54) · **Italian Shoes Company (55) — name literally contradicts "brands from India"; never hero**

**Key debates resolved by the panel:**
- **Nicobar top-3 (not demoted):** the craft lens worried it's "too Westernized to prove you-can't-find-this"; conversion + systems lenses won — it's the *taste reset* that tells Sarah "curated, not a cultural gift shop." Kept top-3, sandwiched between two craft brands so it reads "modern India."
- **gauri and nainika → Tier 3 (not hero) despite max thumb-stop:** glam gowns have Western silhouette and fail axis #1 (India-shout). Desirability without India-shout doesn't earn a hero slot; rubric weight #1 > #2.
- **ModiToys → Tier 2, flagged "diaspora hero":** Krishna/Ganesha plush is the purest identity hook for a diaspora parent but too narrow for a cold non-Indian first-timer as rank-1. Onboard early; use as a *targeted* first-fold slide for baby/diaspora audiences.
- **Category monotony guard:** onboarding interleaves categories so the first fold isn't 4 fashion brands in a row — which is why Isharya (jewelry) and Kaunteya (home) are pulled up despite thinner category supply.

**Photography caveat (diaspora lens):** Tarinika and Baby Forest can tip into cliché if shot on saffron/mandala backdrops. This ranking assumes each brand's own official product photography (per §10 affiliate-native image rule); legibility depends on it.

### 12B. Original QA-scoped recommendation (2026-07-08) — SUPERSEDED by §12A, retained for rationale
> *The set below was scoped to the then-live QA brands only (4-brand carousel). §12A is the full unconstrained onboarding priority and is now canonical; the first-fold order changed (Suta, Isharya, Kaunteya, House of Chikankari now rank above the original 4th slot). Kept here because the per-brand reasoning and the F-002 split still hold.*

### The selection principle: the carousel choice *is* the F-002 fix
The carousel carries no copy; its only job is **visual proof** of one claim — *"distinctive Indian-craft brands you won't find at Target/Amazon."* So the selection rule is "which brands make that claim self-evident in one glance," **not** "our most operationally-ready brands." Through that lens the 11 QA brands split:
- **Unmistakably Indian-craft at a glance** (prove the value prop): Fizzy Goblet, Nicobar, Baby Forest, Banjaaran Studio.
- **Visually indistinguishable from a US DTC brand** (⚠️ featuring these in the first fold *confirms* F-002): SuperBottoms, Pluchi, ChooseKind, Polite Society.

**Key finding:** do **not** lead the hero with the Western-styled brands, even though several are the readiest. The hero is a curation statement; the wrong four brands here cause the exact "how is this different from Amazon?" reaction (F-001).

### Recommended carousel set + slide order
1. **Fizzy Goblet** (footwear) — the universal hook: embroidered juttis = instant "handmade, Indian, not at any US mall." Aspirational, modern-not-costume, global store.
2. **Nicobar** (modern lifestyle) — the **anti-cliché** brand; elevated contemporary "modern India" that answers F-003 without saffron/mandala clichés. Signals taste + curation. Ideal for Arun + Sarah.
3. **Baby Forest** (baby, ayurvedic) — best baby representative for the "why": ayurveda = heritage you literally can't buy at Target. Anchors the core vertical + Sarah's ingredient lens + heritage for Priya/Arun.
4. **Banjaaran Studio** (artisanal fashion) — textile/craft depth + color; reinforces "artisan discovery," adds range.

**Order rationale:** open with the most arresting craft object → immediately prove modern taste (defuse the exotic-cliché landmine) → ground the baby core with a heritage story → close on artisan richness. The four span footwear → lifestyle → baby → craft, so the carousel visually answers Q1 + Q2 on its own.

### Ranking of the full QA set
| Rank | Brand | Verdict |
|---|---|---|
| 1 | Fizzy Goblet | Lead — universal hook |
| 2 | Nicobar | Anti-cliché + breadth |
| 3 | Baby Forest | Core baby vertical, heritage "why" |
| 4 | Banjaaran Studio | Artisan/textile depth |
| 5 | Gully Labs | Fusion story needs explanation; below-fold, not 5s hook |
| 6 | The Alternate India | Less distinctive at a glance |
| 7 | Aagghhoo | Quirky color-pop; supporting only |
| 8–11 | Polite Society, Pluchi, ChooseKind, SuperBottoms | ⚠️ Western-styled → reinforce F-002 in the hero; keep on category pages/below fold |

### Constraints & supply actions
- **Live carousel source + curated order (IMPLEMENTED 2026-07-10):** `getFeaturedBrandsWithProducts` reads the `.development` config (13 live brands), now ordered by **`getCuratedBrandIds`** (`configBrands.js`) — the §12 priority, craft-legible first: Fizzy Goblet → Baby Forest → Banjaaran Studio → Gully Labs → The Alternate India → Vilvah → … → (demoted) Polite Society, Pluchi, ChooseKind, SuperBottoms. Order is preserved through the duck's `Promise.all`. **Nicobar (rank 2) is omitted until ingested.**
- **⚠️ Supply gap — Fizzy Goblet not actually leading.** The carousel filters out brands with no loaded products; **Fizzy Goblet's featured listings aren't live in QA**, so it's dropped and **Baby Forest (rank 2) currently leads**. To lead with the strongest craft hook (juttis), **publish Fizzy Goblet's listings in QA.** *(Superseded framing: earlier "0 in production, carousel renders nothing" — no longer true under QA-as-pseudo-production.)*
- This set does double duty: it's also the **static hero imagery source** (Tier 3 / step 4) — generate from **Fizzy Goblet + Nicobar** first.
- **Two biggest first-impression gaps to fill via supply:** (1) **Suta** (handloom saree) — the single most legible "Indian craft you can't get here" visual, absent from QA; would outrank Banjaaran. (2) **Isharya** (jewelry) — a gold/kundan close-up is a proven hook; currently account-in-QA only. Prioritize both into QA→prod.

### Bridge to step 3 (F-002 probe)
The QA set already visibly splits into craft-forward vs. US-styled, so the probe's likely verdict is a **mix of (a) genuinely-generic and (b) curation-fix** — and the curation fix *is* this selection. Confirm against real listing data before any imagery spend.

---

## 13. Build & Improvement Changelog

### Tier 0 + Tier 1 build (2026-07-10)
Shipped T0-1…T1-7 per §4. Files: `HeroSection.js`, `HeroSection.module.css`, `translations/en.json`, `MelaHomePage.js` (ComingSoon removal), `configBrands.js` (`getPopulatedCategoryCount`). Live-reviewed at `localhost:3000`; §7 Tier-0/Tier-1 ACs pass.

### Post-build improvement pass (2026-07-10)
A live UX review + first-principles expert/PM panel found the built hero **feature-complete but over-composed**: (1) redundant text stack (H1/why-line/breadth line all restated "curated Indian brands"), (2) the carousel *contradicted* the pitch — product **prices + heart icons** read "store," and `getRandomBrandIds` surfaced the Western-styled brands §12 warns against, (3) two AA gaps (muted-gray contrast + auto-advance with no pause). Fixes shipped (T3-1…T3-4, T2-8):

| Change | Files |
|---|---|
| Breadth line → numeric-only (drop redundant qualitative label) | `HeroSection.js` |
| Curated carousel order `getCuratedBrandIds` (replaces `getRandomBrandIds`) | `configBrands.js`, `BrandsPage.duck.js` |
| Hide product price + heart in hero (`showProductMeta`→`showPrice`/`showSave`) | `BrandCardHome.js`, `ListingCardMini.js`, `HeroSection.js` |
| Carousel pause/play control + `prefers-reduced-motion` | `HeroSection.js`, `HeroSection.module.css`, `en.json` |
| Contrast: muted trust text `#718096 → #5a6472` | `HeroSection.module.css` |

*Scope note:* the improvement pass extended beyond §11's original "no duck / no shared-component change" review (it touched `BrandsPage.duck.js` + `BrandCardHome`/`ListingCardMini` with backward-compatible defaults) — §11 remains the Tier-0/1 review record.

### Copy-subtraction + India-signal refinement (2026-07-11)
A second panel + founder feedback: "too much hero text (shoppers don't read)" and "the brand card doesn't shout India." Shipped (T3-5, T3-6):

| Change | Files |
|---|---|
| Merge why-line + trust callout → one line; delete standalone callout | `HeroSection.js`, `translations/en.json` |
| Craft-origin cue "Handcrafted in [City], India" on hero card (`showCraftOrigin` prop, India fallback) | `BrandCardHome.js`, `BrandCardHome.module.css`, `HeroSection.js`, `translations/en.json` |

*Also explored (NOT built — moved to a separate session):* a 3-way hero-visual mockup — **(1) modern SVG jaali lattice, (2) subtle craft texture, (3) real craft photo (Bet 2)** — to make the hero "shout India" without cliché. Founder has additional ideas to explore. Mockup file: `mela-docs/scratchpad/hero-visual-directions.mockup.html`.

### Full onboarding priority (2026-07-12)
A four-designer UX panel (craft-legibility / DTC-conversion / diaspora-cultural / systems-sequencing lenses) ranked **all 55 sheet brands, unconstrained by QA**, into a canonical onboarding order — see **§12A**. The brands sheet (`gid=704623254`) has been **re-sequenced 1→55 to match**. First-fold order changed from the old QA-scoped 4-brand set to **Fizzy Goblet → Suta → Nicobar → Isharya → Baby Forest → Kaunteya → Banjaaran Studio → House of Chikankari** (§12B retained as superseded). No code change — this drives supply/intake order and, as brands land in QA, `getCuratedBrandIds` should follow §12A.

### First-fold refinement (2026-07-13)
A first-principles content-strategy + craft-legibility critique refined §12A's first-fold order — see **§12A.1**. Net: **The Nesavu** replaces **Baby Forest** in the fold (visual India-shout vs. invisible ayurveda story); **Nicobar** demoted #3→#5 (never the isolated lead slide); **Isharya** moved to the #3 jewelry slot with an open re-justify-or-swap-to-Tarinika decision (Open decisions #5). Also separated §12A's *onboarding* order from the carousel *display* order, and flagged the fashion-skew-vs-baby-catalog promise/delivery risk. `configBrands.js` `CURATED_BRAND_SLUG_ORDER` re-sequenced to match; no component change.

### Open follow-ups
- **Hero-visual direction (new session):** decide/prototype the visual treatment (jaali SVG / texture / photo + founder's own ideas). Recommendation on record: ship the rights-free **SVG jaali accent** (optionally on a texture base); keep the real photo as the A/B **Bet 2**.
- **Isharya vs. Tarinika (§12A.1 / Open decisions #5):** pick the first-fold jewelry brand once one ingests with live photography.
- **Supply:** publish **Fizzy Goblet** listings in QA so the carousel leads with it (currently Baby Forest leads — §12).
- **Mobile fold** at 375px (CTA above fold) — real-device check.
- **Regression spot-check:** BrandsPage/FeaturedBrandPartners still show prices/hearts.
- **Data:** populate `brandCity` on brand profiles so the craft-origin line reads "[City], India" (currently falls back to "India").
- **Deferred:** H1 "Quality" rewrite (analytics-gated); Bet-2 imagery; "Supper Bottoms" display-name data typo.
