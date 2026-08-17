# Mela UXR Feedback Log

## Purpose
This log is the single source of truth for user feedback on Mela — what people said, what it means, and what we did about it. Every piece of feedback that informs a product decision should live here.

## How to add an entry
1. Copy any existing row and paste it at the bottom of the table.
2. Increment the ID (`F-001` → `F-002`, etc.).
3. Fill every column — leave no cell blank. Use `—` only if a field genuinely doesn't apply yet (e.g. Linked change before the fix is merged).
4. Update the **Current theme** section above the table if the new entry shifts or sharpens the synthesis.

**Status values:**
- `Planned` — acknowledged, a fix is scoped but not started
- `Actioned` — a concrete change was made
- `Watching` — noted; not acting now but tracking for signal strength
- `Ignored` — consciously deprioritized; reason must be in the Action column

---

## Current theme (updated 2026-07-06)

All three pieces of feedback converge on a single root cause: Mela presents as a generic product catalog rather than a curated cultural destination, and nothing on the homepage — layout, imagery, typography, or copy — signals that this is an Indian brand discovery experience. The problem operates at two levels: **structural** (a grid of listings without editorial curation or a discovery narrative) and **aesthetic** (no visual or typographic cues that anchor the brand in India). Until both levels are addressed, first-time visitors have no reason to stay, explore, or understand what makes Mela different from a standard marketplace.

**Update (2026-08-17) — first counter-signal on the render problem.** Jasmeet (F-008) — a first-gen Indian, 10+ years in the US, Bay Area/tech (the *same diaspora segment as F-001*, and Neha's demographic) — described the homepage *unprompted* as "Indian brands, their stories & the narratives behind them" and "very different — expected a search page or a homepage." That is the differentiation *rendering* — the opposite of what F-001–F-003 reported from the same kind of user, which is what makes it worth watching. It's one data point, so treat it as provisional; but if it repeats across cold respondents, the primary bottleneck moves **downstream of first impression to discovery completion**: catalog breadth for gifting (F-009), trust-eroding "best seller" labels on a thin catalog (F-010), and the absence of occasion/recipient-guided gifting that leaves the occasion-shopper in an unguided 5–10-min search before dropping off (F-011). Watch for repetition before re-scoping.

---

## Log

| ID | Date | Source | Verbatim feedback | Underlying theme | Status | Action taken / reason ignored | Linked change |
|----|------|--------|-------------------|-----------------|--------|-------------------------------|---------------|
| F-001 | 2026-07-06 | 1st-gen diaspora · Indian-brand shopper | "Too many product listings; no inspiration; a visitor doesn't know what to shop or how Mela differs from Amazon." | Catalog layout suppresses curation; no discovery narrative | Planned | Homepage redesign scoped to replace product grid with editorial/curated sections | — |
| F-002 | 2026-07-06 | Friend · US-market / US-brand behavior expert | "Landing page doesn't signal India — no brand, hero, or design cue; some products look like US-store items." | No visual India identity on first load | Planned | Hero section + brand-identity cues scoped for homepage redesign | — |
| F-003 | 2026-07-06 | Friend · 1st-gen diaspora · UX designer | "Font and design language don't feel Indian." | No typographic / aesthetic Indian identity | Planned | Typography and design-language audit scoped alongside homepage redesign | — |
| F-004 | 2026-08-11 | Vidhi · mom of 2, mid-30s, moved to US ~a decade ago after marriage | "Test adding 'add to cart' on the product page and route users to checkout from the cart instead of the product page — the product page feels too incomplete to test as-is." | Product page lacks a complete purchase flow; missing cart step breaks the test | Watching | Not yet actioned; flag for next purchase-flow test design | — |
| F-005 | 2026-08-11 | Vidhi · mom of 2, mid-30s, moved to US ~a decade ago after marriage | "Explore doing an Instagram-only discovery first using AI tools like Canva." | Social-first, AI-assisted discovery may be worth testing ahead of or alongside the web experience | Watching | Noted; relevant to ongoing social content workflow | — |
| F-006 | 2026-08-11 | Vidhi · mom of 2, mid-30s, moved to US ~a decade ago after marriage | "Add more demographic questions to the survey to build stories and understand how people shop." | Survey lacks demographic depth needed for shopper story-building | Planned | Survey question additions scoped | — |
| F-007 | 2026-08-11 | Jishu · male, mid-30s | "Add more familiar, well-known brands that connect with the shopper — other brands can be discovered once the shopper comes in for these well-known ones." | Familiar-brand anchor needed to draw shoppers in before cross-brand discovery | Watching | Noted; ties into brand-mix / acquisition strategy | — |
| F-008 | 2026-08-17 | Jasmeet · 1st-gen Indian (10+ yrs in US), male, married, mid/late-30s, Bay Area/SF, works in tech, expecting first child (to-be dad) | First screen read unprompted as "Learn more about Indian brands, their stories & the narratives behind them"; "very different — expected a search page or a homepage." | Render test PASSED — homepage read as Indian-brand discovery/storytelling, explicitly *not* a generic store; first counter-signal to F-001–F-003 | Watching | Positive signal for the homepage-redesign direction; watch whether it repeats across cold / first-gen respondents before easing the render-problem theme | — |
| F-009 | 2026-08-17 | Jasmeet · 1st-gen Indian (10+ yrs in US), male, married, mid/late-30s, Bay Area/SF, works in tech, expecting first child (to-be dad) | "Gift for mom and dad — but couldn't seem to find anything specific they might like. Needs bigger catalog." | Catalog breadth insufficient for gift-discovery intent; an occasional/gifting shopper leaves empty-handed | Watching | Reinforces F-007 and the discovery-vs-inventory probe; feeds brand-mix / catalog-growth priority | — |
| F-010 | 2026-08-17 | Jasmeet · 1st-gen Indian (10+ yrs in US), male, married, mid/late-30s, Bay Area/SF, works in tech, expecting first child (to-be dad) | "Forest Baby had everything as best seller so got me confused… smaller catalog, yet high best sellers — confusing." | "Best seller" labels lose credibility on a thin catalog — inflated social proof reads as untrustworthy | Planned | Gate / curate best-seller tags (cap per brand, or suppress until real sales data exists); scope trust-signal cleanup | — |
| F-011 | 2026-08-17 | Jasmeet · 1st-gen Indian (10+ yrs in US), male, married, mid/late-30s, Bay Area/SF, works in tech, expecting first child (to-be dad) | "I tend to shop for occasions — but need a more guided approach, like gifts for mom on Diwali, then top options. Will probably spend 5–10 mins searching then drop off." (Return: "Probably not"; recommend: "Probably no") | Unguided browse fails the occasion-gifting shopper → 5–10 min then drop-off; needs occasion / recipient-guided discovery | Planned | Occasion / recipient-guided gifting flow scoped as a discovery surface; ties to inspiration-first, occasion-led persona insight (Priya) | — |
