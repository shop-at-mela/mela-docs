# Mela UXR Feedback — Suggestions (ROI-ranked)

This is the Pass-2 (Opus) synthesis output of the two-pass LLM triage pipeline described in
`nimbalyst-local/plans/uxr-feedback-llm-triage.md` — Pass 1 (Sonnet) maps each feedback row to a
candidate target system and effort tier; Pass 2 groups entries that point at the same underlying fix,
scores Impact against the real codebases, and buckets everything into the impact/effort 2×2.
Generated 2026-09-05 against the complete 34-entry `mela-docs/UXR/feedback-log.md` (F-001–F-034).

Twenty-seven in-scope entries collapse into **14 suggestions**. Already-`Planned`/`Actioned` entries
(F-001, F-002, F-003, F-006, F-010, F-011, F-013) are not re-suggested, but F-011 and F-013 anchor
clusters that new feedback extends, so they carry `Planned` status through.

> **⚠️ Read this first — a catalog-health finding that outranks every UI item below.**
> Verifying F-020 against the production classified data surfaced something no single feedback entry
> reports: **10,312 of 28,232 products (37%) are marked `Out of Stock`**, and it is concentrated in the
> largest brands — Nicobar **72% OOS** (5,968 of 8,245, the biggest brand in the catalog by SKU),
> Isharya **79%** (2,106 of 2,674), SuperBottoms 39%, thenesavu_girls 25%, chidiyaa 24%.
> Ranjini's out-of-stock redirect (F-020) was not bad luck — it was a coin flip she was always likely
> to lose. This one fact plausibly underlies F-020, F-009 ("couldn't find anything specific"),
> F-019 ("only see two categories") and compounds F-010's trust problem. **S-001 addresses it.**

---

## 1. ROI-ranked suggestions

Sorted Quick win → Big bet → Fill-in → Reconsider/defer, with catalog-ops-routed items last.

| Suggestion ID | Linked feedback IDs | Target system | Suggested fix | Impact (1-5, why) | Effort (tier, why) | ROI bucket | Status |
|---|---|---|---|---|---|---|---|
| S-001 | F-020, F-009, F-010 | `web-client` + `catalog-data` | Suppress or clearly flag out-of-stock listings in browse/search, and show stock state on the card and listing page before the vendor redirect | 5 — 37% of the live catalog is OOS (Nicobar 72%, Isharya 79%); silently listing dead inventory wastes trips, and is the likely root cause behind F-020 and F-009 | small — `Stock Status` is **already captured** per product in the classified CSVs; this is a surfacing + filter-default decision, not new integration | **Quick win** | Watching |
| S-002 | F-021 | `prompt_engine.py` / taxonomy CSV | Add a `Jewelry & Accessories > Rings` branch to the category hierarchy and re-classify affected SKUs; harden the fallback so `Other > Everything Else` beats a lexically-similar cross-department leaf | 5 — **reproduced in production data**: 29 Isharya rings are tagged `Home & Kitchen > Rugs & Floor Coverings > Handwoven Rugs`; damage is two-sided (rings unbrowsable, rugs polluted) and visibly erodes catalog trust | small — one hierarchy-CSV edit + re-run; no architecture change | **Quick win** | Watching |
| S-003 | F-017, F-025 (discoverability half), F-026 | `web-client` | One left-sidebar IA pass: collapse the duplicated "All Categories" list + tab into a single entry, and add the missing Gifts entry — while **keeping the full category list visible**, per F-026 | 4 — three respondents touch the sidebar; nav is on every session, and today Gifts is effectively undiscoverable there | trivial — nav/IA change in one component | **Quick win** | Watching |
| S-004 | F-004, F-020 | `web-client` | Relabel the "Add to Cart" CTA to match what it does (saves to your list) and make the vendor hand-off explicit at the moment of intent, reusing the existing `RedirectTrustSheet` | 4 — two respondents; the primary purchase CTA promises a cart that does not exist, on every listing for every buyer | trivial/small — copy + i18n in `OrderPanel`; redirect-consent surface already exists | **Quick win** | Watching |
| S-005 | F-024 | `web-client` | Enable filter-by-brand and filter-by-price on category browse | 4 — core browse utility, and it becomes mandatory as catalog breadth (S-013) grows | small — `priceFilter` is **already configured** in `configSearch.js`; the `brand` field is commented out in `configListing.js` pending Console-based config, so this is hosted-config + a `search-schema/set` CLI step, not a build | **Quick win** | Watching |
| S-006 | F-018 | `web-client` | Raise/qualify the sentiment-popup trigger (gate on engagement, not raw dwell) and make the dismiss affordance obvious | 4 — fires on *every* page for *every* session during the evaluation window, degrading the first impression F-001–F-003 are trying to fix | trivial — `SHOW_DELAY_MS` is 15s in `SentimentSheet.js`; note it is a bottom sheet with an existing `×`, **not** a blocking modal, so the reported "won't let me click" is mobile occlusion + a missed dismiss, which lowers severity but not the fix | **Quick win** | Watching |
| S-007 | F-013, F-022, F-030 | `web-client` (pricing/total-cost display) | Show landed-cost clarity at price and pre-redirect — explicit "duties/shipping charged at vendor checkout" disclosure, or a true tariff-inclusive estimate | 5 — **three independent respondents, all unprompted** (tariff F-013, shipping F-022, duty-vs-India-price F-030); a stated purchase blocker, squarely Neha's total-cost-clarity trust need | medium — display is cheap, but real numbers need per-merchant shipping/duty terms; `UXR/merchant-policies-schema.md` is the natural home for that data | **Big bet** | Planned |
| S-008 | F-011, F-025, F-032 | `web-client` | Organize gift results by occasion and recipient, and add occasion-based category entry points | 5 — three respondents (F-011's shopper drops off after 5–10 min unguided); the entire occasion-gifting segment | medium — **data is not the blocker**: `prompt_engine.py` emits `occasion`/`gift_occasion`/`recipient` as enum-bounded fields and `configListing.js` already declares `pub_occasion`/`pub_gift_occasion`/`pub_recipient`; this is surfacing/IA plus the pending `search-schema/set` step | **Big bet** | Planned |
| S-009 | F-004, F-020 | `web-client` | Build a real in-marketplace cart and route checkout from the cart rather than the product page | 4 — two respondents; a complete purchase flow is a precondition for conversion and for testing the flow at all | large — per Sharetribe's cart architecture guide: cart state lives server-side in **user private data** keyed by provider, checkout uses a **parent/child transaction model** (one main transaction plus one child per listing for stock reservation, cross-linked via protected data), no hybrid "Buy now" once stock-managed children are in play; touches transaction processes, `OrderPanel`/AddToCart, checkout endpoints, transaction-display and email templates | **Big bet** | Watching |
| S-010 | F-005 | `other` (social/content ops) | Pilot an Instagram-first, AI-assisted discovery loop alongside the web experience | 3 — one respondent; top-of-funnel reach, not a product defect, though F-027's mobile-first/occasion cadence supports the channel | small — `social-launch`/`social-review` workflows and a live publishing cadence already exist; a calendar decision, not new build | **Fill-in** | Watching |
| S-011 | F-023 | `web-client` | Reduce information density on the cart/saved page | 2 — one respondent who explicitly said "not a big deal"; cosmetic | trivial — layout cleanup | **Fill-in** | Watching |
| S-012 | F-031 | `web-client` + `catalog-data` | Introduce a bundle/kit product type so curated gift hampers (e.g. small Diwali hampers) can be merchandised | 3 — one respondent, specific ask; distinct from generic breadth (S-013) in needing a new product type, not just more SKUs | medium/large — new listing type + Console config + curation workload | **Reconsider / defer** | Watching |
| S-013 | F-009, F-014, F-019, F-031 | `catalog-data` | Grow depth where intent dead-ends: gift-for-parents inventory (F-009), bedsheets in home (F-014), and the thin category coverage behind F-019 | 5 — three respondents; shoppers arriving with concrete intent leave empty-handed, which blocks conversion outright | large — brand sourcing and SKU onboarding, supply-bound not code-bound | **Big bet** | Watching |
| S-014 | F-007 | `catalog-data` | Sign familiar/anchor brands as an acquisition draw, on the theory that long-tail discovery follows | 3 — one respondent, and in live tension with the curation moat: F-012/F-015 rated brands "few or none" findable elsewhere as the *reason* to prefer Mela, though F-033 ("several" findable elsewhere) shows the moat is only partial | large — BD/partnership pipeline; re-opens brand-mix strategy | **Reconsider / defer** | Watching |

**Catalog-ops routing note:** S-013 and S-014 are brand-sourcing and catalog-ops work and belong in the
BD/partnerships backlog, not an engineering sprint — no `web-client` or `prompt_engine.py` change makes
either true. S-001 and S-012 straddle both lanes and need an owner in each.

**S-004/S-009 resolution (2026-09-05).** Found `product/prds/add-to-cart-restoration-prd.md` — shipped
2026-08-13, before Ranjini's session — which already ran a 5-expert panel on exactly the naming
question S-004 proposes reopening, and decided against it, and already ships the vendor-disclosure
copy S-004 asked for (via `RedirectTrustSheet`). **Relabeling the CTA was not done.** A `/uxr panel`
critique (Dr. Amara Osei et al.) pushed back hard on closing the underlying finding on that basis
alone: Ranjini's complaint has no naming language in it — she reports a process mismatch, not a bad
label, and "an internal panel already decided this" is unfalsifiable if used to wave off any future
complaint about the flow. **What shipped instead:** `AddToCartConfirmation` (the inline toast under
the CTA) now states the destination and next step — "Saved to your list — shop on {brand} when you're
ready" — which answers her actual report without reopening the naming decision. **Still open:** the
PRD's own instrumentation (`saved_listing_toggle` source-tagged `add_to_cart_button` vs `heart_icon`,
downstream `brand_clickout`) can settle whether the CTA is collecting purchase intent it can't
discharge — that query has not been run; it needs GA4/GTM access this pipeline doesn't have. If
`add_to_cart_button`-sourced saves convert to `brand_clickout` meaningfully worse than casual
heart-saves, the comprehension gap is real and bigger than a toast fixes. S-009 (real cart) stays
correctly deferred — its Sharetribe single-vendor-payout constraint was independently re-verified and
isn't affected by this.

---

## 2. No action needed / informational

- **F-008** (Jasmeet) — render test *passed*: homepage read unprompted as Indian-brand storytelling, "very different — expected a search page or a homepage." Validates the F-001–F-003 redesign direction.
- **F-012** (Cousin) — curation/authentication *passed*: "feels more authenticated and catered… includes reputed brands," explicitly favourable vs. Amazon and Etsy.
- **F-015** (Cousin) — strongest pro-bet data point: find-task succeeded, brands "few or none" findable elsewhere, definite return + referral intent. Ops action (early-tester recruit), not a fix.
- **F-016** (Ranjini) — positive top-line with an explicit caveat: "with some refinement it will be very user friendly." Frames her more critical entries below as refinement, not rejection.
- **F-026** (Ranjini) — counter-signal, and a **design constraint on S-003/S-008**: she wants all categories always visible in the sidebar and sees "year round use." Add occasion browse *alongside* full browse; do not replace it with occasion-only framing.
- **F-027** (Megha) — occasion-driven cadence, "Phone" as primary device. Raises the priority of mobile QA generally and of S-006 specifically (the sheet occludes the mobile viewport bottom).
- **F-028** (Megha) — differentiation landing for a 2nd-gen respondent: "very targeted and focused on only Indian based brands."
- **F-029** (Megha) — successful find-task with real purchase intent (handcrafted juttis, Fizzy Goblet).
- **F-033** (Megha) — weaker-signal caveat: brand findability mixed ("several" vs. "few or none"), return "Probably", referral "Maybe, if a specific need came up", triggered by "an occasion like Diwali or wedding." Lowers confidence in the curation-moat read relative to F-015 and partially supports S-014.
- **F-034** (Megha) — opted into the early-tester group. Ops recruitment, same pattern as F-015.

**Sampling caveat carried forward:** every respondent to date is warm (friend, cousin, wife's cousin, colleague) and in-segment Indian-diaspora. The log's own caveat stands — the cold, non-diaspora verdict is still missing and matters most.

---

## 3. Open questions carried forward

1. **F-019 still needs a data check before it can be scored with confidence** — "When I go to All Brands I only see two categories" remains ambiguous between a real catalog gap (`catalog-data`) and a `web-client` display/grouping bug undercounting existing categories. **New evidence shifts my best guess toward "partially real":** production-classified brand output exists in only 5 of 7 verticals, and brand count is heavily concentrated — fashion (14 brands) and baby/kids (12) against home (3), jewelry (2), beauty (1), with art_and_craft and food_and_gourmet at **zero**. That concentration plausibly *is* what she saw. But two categories still does not match five populated verticals, so a grouping/display bug may compound it. Verify against live production counts before assigning an owner. It is currently folded into S-013 on the catalog side.
2. **S-009's single-vendor-payout constraint needs a Product decision, not an engineering estimate.** Sharetribe's default Stripe integration pays out to **one provider per transaction**, so even a multi-brand cart checks out one vendor at a time underneath. Multi-brand carts are Mela's entire catalog model, so this is a genuine scope question — Product should sign off on the constraint before this bet is committed, not discover it mid-build.
3. **Why is stock so lopsided?** Nicobar at 72% OOS and Isharya at 79% versus Tarinika at 0.4% suggests a scraper/sync problem for specific brands as much as genuine stockouts. If it is a sync artefact, S-001 is even cheaper than scored; if it is real, it is a merchant-health conversation. Diagnose before shipping the suppression default, since suppressing 72% of the largest brand would visibly shrink the catalog. **Correction (2026-09-05):** `web-client` already re-checks stock on every `/saved` page load — `savedListings.duck.js` queries with `include: ['currentStock']` and `ListingCard.js` branches the "Shop on {brand}" CTA on it. So S-001 is not "add a missing recheck" — the client-side piece is a *display/suppress* decision on data that's already fetched. Any staleness (like Ranjini's F-020 out-of-stock hit) is upstream: Sharetribe's stored `currentStock` mirrors a periodically-scraped catalog, which can lag the vendor's live Shopify inventory. That makes this open question the actual blocker for S-001's real-world accuracy, not a separate concern — suppressing/flagging OOS in browse only helps if the underlying stock data is fresh enough to trust, and right now that isn't verified.
4. **Are `pub_occasion` / `pub_gift_occasion` / `pub_recipient` live in the Sharetribe search schema?** `configListing.js` carries ⚠️ comments that each still needs a `sharetribe-cli search-schema/set` call. If those were never run, S-008 (and S-005's brand filter) are blocked on a hosted-config step rather than on code — confirm before estimating.
5. **F-007 vs. F-012/F-015/F-033 is a real strategy conflict, not a scoring artefact.** Add familiar anchor brands, or lean on the unfamiliar-brand moat? F-033 shows the moat is only partial, which weakens the pure-moat case. This wants a product decision; flagged here, not resolved.
6. **Impact scores still rest on a thin, warm sample.** Repeat-count is doing real work in S-007 (3 respondents) and S-013 (3), on a base of six respondents total. Re-weight after the first cold, non-diaspora round.
