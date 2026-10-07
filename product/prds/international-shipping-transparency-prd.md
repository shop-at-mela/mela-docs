# International Shipping Transparency PRD

## Document Information
- **Created**: 2026-10-06
- **Status**: 📋 Draft, reviewed 2026-10-06 by /dev-lead, /ux-design, /uxr, and the `/ux-design panel` P1 gate (all folded in; see §11)
- **Owner**: Product Team
- **Source**: UXR F-013, F-015, F-022, F-030, F-036 (`UXR/feedback-log.md`); per-brand US shipping audit in `shopify_brands.py` (Mela-scrapper-integrations `6fcec40`, checked 2026-10-04); code read of web-client on 2026-10-06
- **Related Docs**:
  - `product/TODO.md` (F-013 tariff transparency item; 2026-10-04 `us_*` wiring item; 2026-10-06 Isharya critical fix; 2026-09-25 quarterly review trigger)
  - `product/prds/trust-conversion-signals-prd.md` (§3.3a static "Ships to US" line: **superseded by this PRD**, see P0.7)
  - `product/prds/storefront-validation-readiness-prd.md` (no-affiliate legal constraint; brand template v2; P1.1b data contract this PRD extends)
  - `product/prds/homepage-faq-geo-signals-prd.md`, `product/prds/seo-aeo-category-brand-pages-prd.md` (visible-FAQ + JSON-LD + last-reviewed conventions reused here)
  - `product/prds/dev-to-production-migration-prd.md` (prod seeding steps added, see Rollout)
  - `technical/analytics/crossshop-tracking.md`, `technical/analytics/analytics-fixes-handoff-2026-10-04.md` (event schema, current volume)

> **Verification legend.** "Verified in code" means read in the repo on 2026-10-06. "Unverified" means not checked in code, data, or a browser. No claim in this PRD was checked in a live browser unless it says so.

---

## Executive Summary

**Feature**: Show each brand's own US shipping cost and duty terms on product pages, the pre-redirect trust sheet, and brand pages; remove the shipping and duty claims that are false today; publish the same facts as quotable, dated brand-page copy and matching structured data.

**Target URL / Entry Points**: `/l/:slug/:id` (OrderPanel, ListingTrustChips, RedirectTrustSheet), `/saved` (RedirectTrustSheet), `/brands/:brandSlug` (hero meta line + new "Shipping to the US" section), `/` (FAQ, vetting strip, meta description).

**Target Users**: Neha (needs total-cost clarity before she commits) and Sarah (distrusts international shipping). Priya and Arun benefit from the same facts but did not drive the requirements.

**Business Objective**: Total-cost and duty uncertainty is the most repeated downstream blocker in UXR (F-013, F-022, F-030). Answer it with each brand's real policy, and stop Mela making claims that are false today: the "no surprises at your door" FAQ is false for the 8 live DDU brands, "ships to all 50 states" is false for Pluchi and Isharya, and "price includes shipping & import costs" is false for all 19, since the USD price is a straight currency conversion.

**Primary Success Metrics** (detail in §7):
- Next feedback round: zero respondents who reach a product page say they could not tell the shipping cost or whether duties are included.
- Copy comprehension test: at least 4 of 5 participants correctly answer "Will you pay anything when this arrives?" for each duty state.
- RedirectTrustSheet "helpful" share, split by DDP vs DDU brand: directional only (volume is near zero today, see §7).

**Guardrail**: clickout rate on DDU brands does not drop more than 20% relative to its pre-launch baseline, evaluated only once the volume floor in §7 is met.

> **Legal constraint (roadmap §P0-A, restated in `storefront-validation-readiness-prd.md`)**: Mela is a curated directory under a personal name with **no affiliate income**. Every string and every structured-data field in this PRD must describe the **brand's** policy. Nothing may imply that Mela sells, ships, collects duties, or sets prices.

---

## Build Status Summary *(updated 2026-10-06)*

| Item | Priority | Status | Notes |
|------|----------|--------|-------|
| Per-brand `us_*` data for 25 brands | P0 input | ✅ In repo, not exported | `shopify_brands.py` `6fcec40`: 6 DDP, 12 DDU, 7 unknown (verified by loading the module 2026-10-06) |
| Isharya repoint to isharya.co | Prerequisite | ❌ Not started | 🔴 Tracked separately (TODO 2026-10-06). Isharya's `us_*` data describes isharya.co; it must not be shown until listings link there |
| P0.1 to P0.7 false-claim removal | P0 | ❌ Not started | Seven false or unverifiable claims found, four more than the brief listed (§4 P0 inventory) |
| P0.8 Pluchi | P0 | ❌ Decision made, not executed | Delist (see P0.8) |
| P0.9 exporter + seeder (existing fields) | P0 | ❌ Not started | Note: seeding "dev" changes the live site; shopatmela.com runs on the dev Sharetribe app |
| P1 data additions (fee, currency, checked date, ships from) | P1 dependency | ❌ Not started | Filled from notes + one re-check; 9 brands need a re-check (§4 P1.1) |
| Brand outreach (7 unknown duty terms) | P1 dependency | ❌ Not started | Send before P1 ships; do not wait for replies to ship |
| Copy comprehension test (5 people) | P1 gate | ❌ Not started | 3 recruits named in UXR; 2 more needed |
| Mockup (mobile first) + `/ux-design panel` | P1 gate | 🟡 Panel run 2026-10-06; two device checks left | `nimbalyst-local/mockups/international-shipping-transparency-mobile.mockup.html`: product page (6 states + longest name), tooltip, trust sheet collapsed + expanded, brand page DDU + DDP. Panel decisions in §11. Still open before build: live product page fold check at 375 × 667 (P1.2) and trust sheet with the on-screen keyboard on a real phone (P1.5). Desktop 1440px and loading states not drawn |
| P1 per-brand display, brand page section, analytics, SEO fixes | P1 | ❌ Not started | |
| P2 `offers.shippingDetails` | P2 | ⛔ Blocked | On P1.9 seller decision shipping + price-accuracy gate |

---

## 1. Problem Statement

### Current State

**Shoppers ask about total cost and Mela either says nothing or says something false.**

Three of the UXR respondents raised shipping or duties without being asked:
- **F-013** (1st-gen, 20+ years in the US): "Your prices are good but wanna know if tariff [is] included." She had paid tariff on an order from another site ("the loom site"); she did not say whether it was charged at checkout or at the door. In the same session she found a House of Chikankari kurti she would "realistically buy" (F-015). House of Chikankari is DDU: its own US rate is named "Standard Shipping (Duties Excluded)", so the courier collects duties at her door.
- **F-022**: "If it's going to be exorbitant that would deter me from buying the item." She never reached a brand checkout, so she never saw a shipping cost.
- **F-030**: "Pricing compared to cost to purchase in India, duty?"

Since the US ended the $800 de minimis exemption in August 2025, DDU means duties are due on small orders too, so "it's under $800" no longer protects a shopper.

**What Mela tells shoppers today (verified in code 2026-10-06):**

| # | Where | Current copy | Why it's wrong |
|---|-------|--------------|----------------|
| 1 | `OrderPanel.priceConvertedDisclaimer` (en.json:891), desktop OrderPanel only | "Estimated from Indian retail price · US brand price includes shipping & import costs" | False for the DDU brands (8 live, 12 of 25 total), and the USD figure is a straight FX conversion with no shipping or duty added (TODO 2026-08-06 entry). Also uses "Indian" on the user layer |
| 2 | `RedirectTrustSheet.trustShipping` (en.json:1872), every brand | "Ships to the US · US cards accepted" | Pluchi ships nowhere outside India. Isharya's linked store (isharya.com) returns no US rates |
| 3 | `VettingStrip.shipping` (en.json:636), homepage | "Ship to all 50 states" | False while Pluchi and Isharya are live |
| 4 | `BrandStorefront.metaShipping` (en.json:1048), **every brand page hero**. Not in the brief | "Ships to all 50 US states" | Same; shown on Pluchi's own page |
| 5 | Homepage FAQ Q1 (`MelaHomePage.js:38`, visible + FAQPage JSON-LD). Not in the brief | "Every brand featured on Mela ships directly to US addresses, to all 50 states." | Same. "Directly" is also wrong for Daughters of India (US warehouse) |
| 6 | Homepage FAQ Q3 (`MelaHomePage.js:48`, visible + JSON-LD). Not in the brief | "Each brand's own checkout will calculate and display any applicable duties or import taxes before you pay, so there are no surprises at your door." | **The most harmful claim on the site.** For the DDU brands (8 live, 12 of 25 total), duties are not shown at checkout; the courier collects them at the door. This is the kind of surprise F-013 is wary of |
| 7 | Homepage meta description (`MelaHomePage.js:65`). Not in the brief | "...Ships to all 50 states." | Same as #3, in search results |

Related, lower severity (handled in P0.6 and P1.9):
- Hero copy "shipped to your door worldwide" and "shipped worldwide" (`SectionMelaHero.heroSubheadline`, `breadthCount`, en.json:650/654) reads as Mela shipping, and "worldwide" is unverified for every brand.
- Homepage FAQ Q4 says "Mela vets all partners for fair return terms." Per the brief, Nicobar, Polite Society, Needledust and Saphed don't accept returns from abroad (**unverified**: this is not in `shopify_brands.py` notes).
- Product JSON-LD names Mela as `offers.seller` (`ListingPageCarousel.js:413`), which asserts Mela sells the product.
- The unused `coverPhoto` listing layout (`ListingPageCoverPhoto.js:453`) emits a blanket US `shippingDetails` for every brand. `configLayout.js` selects `carousel`; whether the hosted layout config overrides that is **unverified**.

**Where the price context actually renders (verified in code, not in a browser):** below 1024px the OrderPanel's full price block (USD, INR line, disclaimer) sits inside `ModalInMobile`, which stays closed for brand listings because their CTA is Add to Cart, not the order modal. The mobile sticky bar shows only the USD price (`PriceMaybe` with `showCurrencyMismatch`). So on phones, shoppers see no INR line, no disclaimer, and no shipping information of any kind on the product page. Claim #1 only reaches desktop users. Any mobile shipping line in this PRD is a new in-page element, not an edit to an existing one.

*Correction (`/ux-design panel`, 2026-10-06):* phones do already see an INR figure before the product page. Brand and search grid cards show "~₹3,600" under the USD price (`ListingCard` `showInrPrice` defaults to true; homepage modules pass false). Verified in code, not in a browser. The INR line is new on the mobile **product page** only.

**The trust sheet reaches few shoppers (verified in code + analytics docs):** `RedirectTrustSheet` opens only on the first outbound click per session (`shouldShowRedirectTrust`). In-stock product pages no longer link out (Add to Cart saves instead, since 2026-08-12), so the sheet appears on `/saved` "Shop on" clicks and out-of-stock product pages only. GA4 had 0 `brand_clickout` events from Sep 5 to Oct 2 and 3 `saved_listing_toggle` events in 28 days (`analytics-fixes-handoff-2026-10-04.md`). **The product page is the surface that has to carry the shipping and duty facts.** The trust sheet is a second chance, not the main one.

### User Pain Points (persona lens)
- **Neha**: her stated trust need is "What's the total cost including shipping?" and she rejects "vague shipping estimates" (`buyer-personas.md`). Today she gets no number on mobile and a false "includes shipping & import costs" on desktop.
- **Sarah**: "International shipping usually means long waits and high $." The persona doc's Known Gaps notes her distrust of international shipping is never answered with a trust signal. A blanket "Ships to all 50 states" that turns out false for a brand she clicks confirms the distrust.
- **Talia (F-036, non-diaspora, no persona yet)**: assumes everything comes "straight from India to me." Three brands ship partly or wholly from US stock (Tarinika, Hemant & Nandita, Daughters of India).

### Business Impact of Inaction
- A shopper like F-013's respondent, buying the House of Chikankari kurti she picked, would get the duty bill at her door after Mela's FAQ (claim #6) promised no surprises. That is the trust failure the curation model cannot recover from, and she is the kind of shopper who shares in WhatsApp groups.
- Validation data stays contaminated: Pluchi clickouts can never convert, and Isharya clickouts land on a store that cannot sell to the US.
- Mela's structured data and FAQ state facts that are false, which is a search-quality risk as well as a trust one.

---

## 2. Goals & Non-Goals

### Goals
1. Remove every false or unverifiable shipping, duty, and seller claim listed in §1 (P0).
2. On every product page and brand page, state the brand's own US shipping cost and whether US import duties are included, using only structured data fields (P1).
3. Never imply Mela ships, collects duties, sells, or sets prices.
4. Give answer engines one quotable, dated, self-contained "Shipping to the US" passage per brand, with FAQPage JSON-LD that exactly matches the visible copy (P1).
5. Keep the data true over time: named owner, re-check cadence, and a fail-closed rule for stale data.

### Non-Goals
- **Closing the price gap vs buying in India (F-037, F-041).** This PRD does not address it. A shipping line does not close that gap and can widen it for Neha: "$34 shipping, duties extra" on top of a USD price she already compares to Myntra makes the gap larger and more visible. That is acceptable because hiding it is worse, but it means this PRD should not be expected to move price objections. Track them separately.
- Duty amount estimates (HS codes, rates, per-product duty).
- A landed-cost calculator.
- A "duties included" search filter or sort. (This is the only reason duty data would ever need copying onto listings; see §8.)
- Computing whether a specific item or cart ships free.
- International returns policy display (open question, §8).
- Changing which listings or prices Mela shows, other than the Pluchi delisting.

---

## 3. User Stories

| As a... | I want to... | So that... | Priority |
|---------|-------------|------------|----------|
| Any shopper | never be told something about shipping or duties that turns out false | I can trust the rest of what Mela says | P0 |
| Neha | see what the brand charges to ship to the US and whether duties are included, on the product page | I can work out the total before I leave Mela | P1 |
| F-013's shopper (Neha) | be told plainly when duties are paid at the door | I'm not surprised by a courier bill again | P1 |
| Sarah | see that the brand, not an unknown middleman, handles shipping, and when Mela last checked | I can judge whether to trust a cross-border order | P1 |
| Any shopper | see a free-shipping threshold as the brand states it | I can decide whether to add more from that brand | P1 |
| Shopper about to leave for the brand's store | see that brand's shipping and duty terms one more time | the brand's checkout matches what Mela said | P1 |
| Shopper asking an AI assistant "does House of Chikankari ship to the US?" | get Mela's dated answer quoted | I find Mela as the source | P1 |
| PM | split behavior by DDP vs DDU brands | I can see whether honest disclosure changes clickouts | P1 |

---

## 4. Feature Requirements

### Copy rules (apply to every phase)
- **Brand as subject.** "Nicobar includes duties in its US prices." "Suta ships to the US for $20." Never "we ship", "shipping is", or anything without the brand's name or "its/the brand's" nearby.
- **Name the brand once per block** (from the mockup, 2026-10-06). The first sentence carries the brand name; any second sentence in the same line or answer uses "It" or "Its" ("It adds US duties at checkout..."). This saves about 15 characters per state at 375px and keeps the brand as the subject. Exception: brand-page passages and FAQ answers stand alone when quoted, so they repeat the name where a sentence could be lifted out on its own.
- **No DDP/DDU terms shown to shoppers.** Explanations go in a tooltip (P1.4).
- **House rules** (`shopify_brands.py` docstring): no dash characters (no hyphen, en dash, or em dash in copy; use commas, colons, or separate sentences), US spelling, "hard to find" never "unavailable", and "Indian" stays off the user layer ("India price", not "Indian retail price").
- **Never parse `us_shipping_note`.** Every shopper-facing string is a template filled from structured fields only.
- **Unknown stays unknown.** A missing field produces the "unknown" copy, never a guess and never the old blanket claim.

### Must Have (P0): remove false claims *(target: ship first, mostly copy-only)*

P0 is copy plus the existing three `us_*` fields. It does not wait for the comprehension test, the mockup, or the P1 data additions, because every P0 string is either neutral or a deletion.

**P0.1: `OrderPanel.priceConvertedDisclaimer`**
- Replace with: **"Estimated from the India price. {brand} sets the final price at checkout."** (Passes `brand` as a value; the component already has `publicData.brand`.)
- Drops the false "includes shipping & import costs" and the user-layer "Indian".
- P1.2 later merges this into the single estimate line; P0 is the immediate text swap.

**P0.2: `RedirectTrustSheet.trustShipping`**
- Split into two list items driven by the brand's `publicData.brandUsShipping` (P0.9). Until P1 adds fee data, P0 shows method and duties only:
  - Shipping item: "{brand} ships to the US" (any method except `none`). If no data: **"{brand} sets shipping at its checkout"**.
  - Duties item: DDP "{brand} includes US import duties"; DDU "US import duties are paid on delivery"; unknown or no data "{brand} doesn't say if US duties are included".
- "US cards accepted" moves onto the checkout item: "Secure checkout on {brand}'s store · US cards accepted". (Card acceptance was not tested per brand; **unverified**. Keep the existing claim; do not extend it.)
- **Spike first (dev-lead):** no listing-page code reads `author.attributes.profile.publicData` today. Confirm on one dev listing that the included author carries `profile.publicData.brandUsShipping` before building anything on it.
- The sheet needs the brand's profile. On the listing page this is `ensuredAuthor` (already loaded via `include: ['author', ...]`, verified in `ListingPage.duck.js:70`). On `/saved`, `savedListings.duck.js:252` includes `author` (verified); confirm the author entity carries `profile.publicData` in that response (**unverified**, same SDK shape as the listing page, so expected).

**P0.3: `VettingStrip.shipping`**
- Remove the item now. Restore it as **"Every brand ships to the US"** only after Pluchi is delisted (P0.8) and Isharya is repointed. "All 50 states" is not restored: no brand was tested beyond a New York 10001 address.

**P0.4: `BrandStorefront.metaShipping`**
- Replace the hard-coded hero fact with the brand's own short fact (same data as P0.2): "Ships to the US" when method is known and not `none`; omit the item when there is no data. "Duties included" is appended for DDP brands only in P1.6.

**P0.5: Homepage FAQ (`FAQ_ITEMS` in `MelaHomePage.js`) and meta description**
- Q1 answer: "Every brand on Mela ships to US addresses from its own store. Shipping costs and delivery times are set by each brand; each brand page shows that brand's US shipping cost and whether its prices include import duties." (Ship this only after P0.8 and the Isharya fix; until then drop the first sentence.)
- Q3 answer: "It depends on the brand. Some brands include US import duties in their prices. For others, the courier collects duties before delivery, and since August 2025 that can apply to orders of any value. Each brand page and product page says which applies." (Replaces the false "no surprises at your door".)
- Meta description: drop "Ships to all 50 states."
- Bump `HOMEPAGE_LAST_UPDATED`. Remove dash characters from all four answers while editing (current Q1 and Q3 contain "7–10", "3–7", and "Possibly —").

**P0.6: Related claims**
- Hero `heroSubheadline` / `breadthCount`: replace "shipped to your door worldwide" / "shipped worldwide" with wording that names the brands as shippers (e.g. "...from brands that ship to the US"). Exact strings go through `/ux-design` with P0; they are positioning copy.
- Homepage FAQ Q4: replace "Mela vets all partners for fair return terms" with "Each brand sets its own return policy, including whether it accepts returns from the US. Check the brand's policy before you buy." (Does not depend on the unverified four-brand list; true either way.)

**P0.7: Supersede the static "Ships to US" line**
- `trust-conversion-signals-prd.md` §3.3a ("🇺🇸 Ships to the US · 💳 US cards · ✅ Sold by [Brand]", P0 ❌ not built) and the PRD_TRACKER "Now #1" recommendation to build it are **superseded**: a static line would recreate claim #2 on every product page. Update both docs to point here.

**P0.8: Pluchi (decision: delist)**
- Options considered:
  - *Hide the claim, keep listing*: every Pluchi clickout is still a guaranteed dead end, and it corrupts OCTR.
  - *Label it* ("Pluchi doesn't ship to the US yet"): honest but it turns Mela into a showcase of products a US shopper can't buy, the opposite of "brands that already export".
  - *Delist* ✅: close Pluchi's listings and remove it from the active brand set in `configBrands.js` (dev block) until its policy changes. Closing listings is reversible.
- Closing listings and removing Pluchi from `configBrands.js` still leaves `/u/:id` and possibly `/brands/pluchi` reachable with an empty grid. Return 404 for `/brands/pluchi` (consistent with the "404 for bad slugs" item in `seo-aeo-category-brand-pages-prd.md`) and noindex the `/u/:id` profile.
- Add to the `shopify_brands.py` ACTIVATION CHECKLIST: **`us_shipping` must not be `"none"`**. This makes the vetting claim structurally true for future brands.
- Code fallback (defense in depth): if a profile ever has `method: "none"`, product and brand pages show "{brand} doesn't ship to the US yet" and the trust sheet shows the same line before Continue.
- **Owner confirmation needed before execution** (it removes a live brand).

**P0.9: Export + seed the existing three fields**
- `export_brand_content.py`: export `us_duties`, `us_shipping`, `us_free_shipping_over_usd` into `brand_content.json` as `usShipping: { duties, method, freeOverUsd }`, omitting empty or `None` values.
- `seed-brand-profiles.js`: write `publicData.brandUsShipping` (one nested key). Map `"DDP"`→`"ddp"`, `"DDU"`→`"ddu"`; omit `duties` when `""`.
- **Shallow-merge caveat (verified in seeder):** Sharetribe merges `publicData` one level deep, so writing `brandUsShipping` replaces the whole nested object. That is the desired behavior (a removed sub-field disappears). But if a brand's export has **no** `usShipping` at all, the seeder skips the key and the old object stays. The seeder must write `brandUsShipping: null` for brands whose export has no shipping data, so stale data cannot survive.
- **Isharya guard:** skip Isharya's `usShipping` (or write `null`) until its `base_url` is `https://isharya.co`. Its data describes isharya.co, and listings still link to isharya.com.
- The exporter takes the first entry per `brand_name`. Today all six multi-entry brands (Masilo, SuperBottoms, Pluchi, Nicobar, Saphed, The Nesavu) have the primary entry first (verified 2026-10-06). Add an assertion that fails the export if a brand's `us_*` fields appear on a non-first entry.
- **Seeding "dev" is seeding the live site.** shopatmela.com runs on the dev Sharetribe app (`dev-to-production-migration-prd.md` §1). Run `--dry-run` first and spot-check 3 brands via the Integration API.

### Should Have (P1): per-brand display

**P1.1: Data additions** *(dependency for P1.2 onward)*

New fields in `shopify_brands.py`, on the primary entry only, documented in the module docstring:

| Field | Type | Rule |
|-------|------|------|
| `us_shipping_fee` | number or None | The flat US rate below any threshold, in the store's currency. Set only for `flat_rate` and `flat_rate_free_over_threshold`. None for `calculated_*` (weight based; no single number exists) and `free` |
| `us_shipping_fee_currency` | `"USD"` \| `"INR"` | Currency the store charges in. Required when `us_shipping_fee` is set |
| `us_free_shipping_over_currency` | `"USD"` \| `"INR"` | **New, not in the brief.** Thresholds stated in INR are converted at ~₹88/$ today and shown as exact dollars. The UI must prefix INR-sourced thresholds with "about". Store the source currency so it can |
| `us_shipping_checked` | ISO date | Date of the last policy + cart check. Today it exists only inside the note |
| `us_ships_from` | `"india"` \| `"us_warehouse"` \| `"mixed"` \| omitted | Optional. From notes: Tarinika `mixed`, Hemant & Nandita `mixed`, Daughters of India `us_warehouse`. The brief said all three ship from US warehouses; the notes say two of them ship from India or the US |
| `us_duties_collected` | `"in_price"` \| `"at_checkout"` | **New, not in the brief.** DDP only. Vilvah adds a fixed $10 duty at checkout rather than including it in prices, so "Vilvah includes duties in its US prices" would be false. Default `in_price` |

Exported and seeded as `publicData.brandUsShipping`:
```
{ duties: 'ddp'|'ddu', dutiesCollected: 'in_price'|'at_checkout',
  method: 'free'|'flat_rate'|'flat_rate_free_over_threshold'|
          'calculated_at_checkout'|'calculated_free_over_threshold'|'none',
  fee: number, feeCurrency: 'USD'|'INR',
  freeOver: number, freeOverCurrency: 'USD'|'INR',
  shipsFrom: 'india'|'us_warehouse'|'mixed',
  checkedAt: 'YYYY-MM-DD' }
```
Every key is optional. Unknown values are left out, never guessed. (`freeOverUsd` from P0.9 is replaced by `freeOver` + `freeOverCurrency`; the P1 seed overwrites the whole object, so no migration is needed.)

**INR values are converted at export, not at render** (dev-lead review). The exporter also writes `feeUsd` and `freeOverUsd`, rounded to whole dollars, plus `approx: true` on either when the source is INR. The UI reads only the USD fields and adds "about" when `approx` is set. Why: `util/liveInrRate.js` fetches the live rate only in the browser and falls back to 1/83 during SSR, so converting at render would give different text on the server and the client (hydration mismatch), and the brand-page JSON-LD would no longer equal the visible FAQ. One documented export rate (currently ~₹88/$, the rate the notes use) keeps every surface identical. Note that listing prices are converted at 1/83 at ingestion; the two rates are knowingly different and both are labeled as estimates.

**Re-check required before display** (from the notes; one pass, record `us_shipping_checked`):

| Brand | Issue in note |
|-------|---------------|
| Isharya | After the repoint: policy says $20 below $250, cart test returned $25 at $100 |
| Vilvah Store | Banner says $10 fixed duty over $59; older policy text says customer pays duties; unknown below $59 |
| Nicobar | Threshold stored as $150, but $30 was charged at exactly $150 and free only seen at $200 |
| Daughters of India | Policy Economy $12; cart test $17.25 to $43.13. Also adds state sales tax. Fit decision still open (TODO 2026-10-04) |
| Hemant & Nandita | Rate below $199 not verified (rate limited) |
| ChooseKind | Policy says free over $150; cart showed free at $96 and $115 |
| Saphed | Tested on an empty cart only; made to order, 15 to 20 working days |
| Suta | Free threshold not published (charged at $119, free at $182) |
| Polite Society | Banner says free over $500; cart at ~$557 still charged |
| Needledust | Policy pages state the threshold as both $200 and $250 |

Until a brand's re-check is done, show its shipping item without the threshold (and Vilvah's duty line as unknown).

**P1.2: Product page price context (OrderPanel desktop + new mobile block)**

One shared component (working name `ListingShippingTerms`) renders in two places from the same props, so desktop and mobile can't drift:
- **Desktop (≥1024px):** inside OrderPanel's `PriceMaybe` full block, under the USD price, replacing the separate INR and disclaimer lines.
- **Mobile (<1024px):** a new in-page block directly under the H1 in `ListingPageCarousel.js`, above `ListingTrustChips`. It shows the USD price plus the same lines. The sticky bottom bar is unchanged (price + Add to Cart). (Reason: on mobile the existing price block is never rendered, see §1.)

**Layout decision: at most two logical lines of grey text under the price, and at most three visual lines at 375px.** The five-line stack (INR, disclaimer, shipping, threshold, duties) is rejected. On mobile the price appears twice (in the page and in the sticky bar); that is intended, since the in-page price anchors the grey lines.

```
375px, DDU brand, INR store, flat rate:

  $41.00
  House of Chikankari ships to the US for about $34.       ← shipping line (may
  Import duties are extra, paid on delivery ⓘ                wrap to a 2nd visual line)
  Estimated from the ₹3,600 India price ⓘ                 ← estimate line

375px, DDP brand, USD store, threshold:

  $180.00
  Nicobar ships to the US for $30, free on orders over $150.   ← shipping line only
  [✓ Duties included]   ← positive chip, in ListingTrustChips under the H1
```

**Order (decided at the `/ux-design panel`, 2026-10-06): price, then shipping and duties, then the estimate.** The shipping line comes directly after the price on every breakpoint (one component, one order). Why: in the mockup at 375 × 667, the block starts about 550px down and the sticky bar starts at 595px, so with the estimate first, the shipping and duty facts loaded under the sticky bar while the India price was visible. Even with the new order, the shipping line's second visual line can still sit under the bar on a 667px phone; the live check below decides whether more is needed.

- **Shipping line (shipping, then duties):** one sentence for shipping, then one short sentence for duties unless duties are shown as a chip. May wrap to two visual lines; never three at 375px.
- **Estimate line:** "Estimated from the {inrPrice} India price ⓘ". Shown only when the price was converted from INR (`formattedINRPrice`), as today. Tooltip: "{brand} sets the final US price at its own checkout, and it can differ from this estimate." This merges today's INR line and the P0.1 disclaimer into one line. Kept on mobile (panel decision): grid cards already show the INR figure (§1 correction), so hiding it here would make it disappear between the card and the product page. The label "India price" is tested with a non-diaspora reader (§7).
- **Line limit is a build check, not a runtime fallback** (panel). The component can't measure wraps during server rendering. Measured in Chrome at 375px (327px text width, 13px/18px Hanken Grotesk), the shipping line wraps to a third visual line at 108 to 116 characters depending on the words. A unit test over every seeded brand asserts the shipping line is **at most 100 characters**, leaving room for device font differences. Over budget, the product page drops the threshold clause (e.g. "Fizzy Goblet ships to the US for $15. Import duties are extra, paid on delivery"); the threshold stays on the brand page and the trust sheet. Fizzy Goblet's full sentence is 105 characters, so it already uses the fallback.
- **Tooltip near the sticky bar:** the ⓘ popover opens upward when there isn't room above the sticky bar, and the page scrolls the trigger into view before opening.
- **Live check before build:** open a live product page at 375 × 667 and record where the shipping line lands on first load. The mobile gallery has no fixed height and is sized by the photo (`ListingImageGallery.module.css`, verified in code), so portrait photos may push the block lower than the mockup's 380px placeholder.
- Order is fixed: price, shipping, duties, estimate.
- **DDP on desktop (ux-design review):** the chip sits in the left column, away from the OrderPanel price, so on desktop only line 2 also ends with "Duties included." On mobile the block sits directly above the chip row, so no extra text is needed.
- Styling: existing `marketplaceTinyFontStyles`, `--colorGrey500`. Duties-not-included uses the same grey as everything else. No warning color, icon, or weight change.

**Implementation (dev-lead):** one helper module, e.g. `util/brandShipping.js`: `getDutiesType(usShipping)`, `isShippingStale(checkedAt, now)` (with `now` injected so tests are deterministic), and sentence builders that compose a few small en.json keys. Avoid one large nested ICU `select`. The product block, trust sheet, brand hero, brand passage, brand FAQ and JSON-LD all call this module.

**Shipping sentence templates** (en.json keys, filled from `brandUsShipping`; `{fee}` and `{threshold}` formatted as USD, prefixed "about" when the source currency is INR, rounded to whole dollars for INR):

| `method` | Template |
|----------|----------|
| `free` | "{brand} ships free to the US." |
| `flat_rate` | "{brand} ships to the US for {fee}." |
| `flat_rate_free_over_threshold` | "{brand} ships to the US for {fee}, free on orders over {threshold}." If threshold unknown: "{brand} ships to the US for {fee}. Larger orders may ship free." **If fee unknown** (e.g. Vilvah until re-checked; gap found in the mockup): "{brand} ships free to the US on orders over {threshold}." with no below-threshold clause. If both are unknown: "{brand} ships to the US." |
| `calculated_at_checkout` | "{brand} ships to the US. Its checkout shows the shipping cost." |
| `calculated_free_over_threshold` | "{brand} ships free to the US on orders over {threshold}. Below that, its checkout shows the cost." |
| `none` | "{brand} doesn't ship to the US yet." |
| no data / stale (P1.10) | "{brand} sets shipping and duties at its checkout." (no duty sentence) |

Thresholds are text about the brand's whole order. Never compare them with this item's price, never say "this item ships free", never show progress toward a threshold.

**Duty sentence / chip:**

| State | Product page | Tooltip (ⓘ) |
|-------|-------------|-------------|
| DDP, `in_price` | Chip "✓ Duties included" in `ListingTrustChips` (no sentence) | Chip tooltip: "{brand} includes US import duties in its prices, so nothing is due when your order arrives." |
| DDP, `at_checkout` | Sentence: "It adds US duties at checkout, so nothing is due on delivery." | none |
| DDU | Sentence: "Import duties are extra, paid on delivery ⓘ" (wording is a test candidate, P1.11) | "{brand}'s prices don't include US import duties. The courier collects them before delivery. Since August 2025 this can apply to orders of any value. Mela can't estimate the amount." |
| Unknown, shipping cost known | Sentence: "It doesn't say if US duties are included." (test candidate; see UXR note below) | none |
| Unknown, shipping cost **not** known (`calculated_*` below threshold, or fee unknown) | **Merged with the shipping sentence** (gap found in the mockup: two separate sentences took 4 visual lines for Masilo): "{brand} ships to the US. It doesn't list its shipping cost or say if duties are included." | none |

> UXR note for the test: the brief's unknown copy was "Check duties at [brand]'s checkout". If the brand is actually DDU, its checkout will not show duties at all, so that wording can reassure falsely. The candidates above state the gap and drop "check at checkout". Test the brief's wording against them.
>
> Line counts measured in the mockup (Chrome, 375px, 24px gutters, 13px Hanken Grotesk, 2026-10-06): every state is at or under 3 visual lines once the two fixes above are applied. Not checked on a real iOS or Android device. Character budget and fallback: see the line limit rule above.

**P1.3: ListingTrustChips**
- Accept a new optional prop (e.g. `usShipping`) and render the DDP chip before certification chips. Same `certChip` styling (positive). No chip for any other state.
- **Guardrails (panel, 2026-10-06):** the chip states a real difference in what the shopper pays, so it stays, but it is not a ranking signal. It appears on the product page and brand page only, never on grid cards, and it is never used as a sort, filter or ranking input without a new review. The DDP vs DDU split is read through `duties_type` (P1.11). The brand outreach email tells brands how duty terms are displayed. Whether the chip makes brands without it look worse is a copy test question (§7).

**P1.4: Tooltip pattern**
- Follow `CertificationBadge`'s `showTooltip` content pattern (bold label + one short paragraph), **but** CertificationBadge's tooltip is CSS `:hover` on a non-focusable `div` (verified in code), so it does not work on touch or keyboard. The new ⓘ must be a `<button>` with an accessible name, open on tap and focus, close on outside tap and Escape, and connect via `aria-describedby`. Fixing CertificationBadge itself is out of scope but should reuse this.

**P1.5: RedirectTrustSheet with full data**
- Same two items as P0.2, now with fee and threshold. The sheet heading already names the brand ("You're visiting {brand}'s official store"), so items drop the repeated name (ux-design review): "Ships to the US for $15, free on orders over $100", "US import duties are paid on delivery", "Duties are included in the price" (DDP `in_price`; no chip in the sheet). The brand-as-subject rule is met by the heading.
- At 375 × 667px, with 4 items and the sentiment row expanded, Continue must stay visible without scrolling. **Measured (mockup frame H, built from `RedirectTrustSheet.module.css`, Chrome 2026-10-06):** the expanded sheet's natural height is 569px against the 85% cap of 567px, so the feedback area gives up 2px and scrolls inside itself, and Continue stays fully visible. There is no spare room: a fifth item or a shorter viewport makes the feedback area scroll (Continue still stays visible). **Not checked:** the on-screen keyboard (the textarea takes focus on expand, and a fixed bottom sheet can end up behind the keyboard on iOS Safari) and Safari's visible height with toolbars showing. Check both on a real phone before build.
- **"US cards accepted"** (panel): shown on the checkout item only for brands whose payment page was checked in the P1.1 re-check pass. Brands not checked by P1 ship show "Secure checkout on {brand}'s store" without it. Richer card and payment signal: separate TODO (2026-10-06).
- Item order: checkout + cards, shipping, duties, returns ("Returns handled by {brand}" unchanged pending §8).
- Hosts: `ListingPageCarousel.js`, `ListingPageCoverPhoto.js`, `SavedPage.js`. Each passes the brand's `brandUsShipping`.

**P1.6: Brand page hero meta line** (`BrandStorefront.js` `heroMetaStatic`)
- `{N} products · Ships to the US · Duties included · Shipping details ↓` (the last item is an anchor link to P1.7)
- **"US cards accepted" is removed from the hero** (panel, 2026-10-06): it was never checked per brand, and the meta row is the densest row on the page. With it removed, the row still wraps to 2 lines at 375px for a DDP brand (measured in the mockup).
- "Duties included" for DDP (either collection mode) only. No duty item for DDU or unknown (the section below carries it). No fee or threshold in the hero.

**P1.7: Brand page "Shipping to the US" section**
- Placement: on the Products tab (the canonical `/brands/:brandSlug` URL), **after the Featured row and `BrandOccasionModule`, before All Products** (confirmed at the panel; matches the render order in `BrandStorefront.js`). Not after the grid: All Products loads 12 at a time on scroll (`loadMoreRef` in `BrandStorefront.js`, verified), so for a 308-product brand like Fizzy Goblet anything after the grid can't be reached (ux-design review). This deviates from the category-page "after main content" rule for that reason. Not on the About tab, which is a separate route.
- The hero meta line gets a "Shipping details" anchor link to this section (P1.6).
- **Height (decided at the panel, 2026-10-06): passage always visible, every FAQ item collapsed by default.** Measured at 375px: 382px for a DDU brand with 2 FAQ items (down from 438px with the first item open), 407px for a DDP brand with 3 items, and 502px if the duty answer is opened. "Read more" is rejected because the cut would fall before the duty sentence, the fact most likely to change the purchase. About 382px before All Products is accepted as a known tradeoff. Alternatives considered: the About tab (separate route, rarely opened) and a hero disclosure (the hero is already the densest block). Escalated, not blocking: a single cross-brand shipping page for "which brands include duties" queries.
- Content, in order:
  1. `<h2>` "Shipping to the US"
  2. **Passage**: 40 to 60 words, self-contained (names the brand, says it ships to US addresses, the cost, the duty terms, that checkout happens on the brand's store), always visible. Built from the same templates as P1.2 plus fixed connective sentences, never hand-written per brand. Examples in Appendix A.
  3. **FAQ**: collapsed-by-default `<details>` items reusing the category page's accordion markup and styles (`CategoryPage.js:439`, `css.faqAccordion`). **Correction to the brief:** the homepage `FAQSection` is not an accordion; it renders always-open cards under a hard-coded "Shipping, Payment & Returns for US Shoppers" heading (verified in code). Use the category pattern, or generalize `FAQSection` to take a heading and an accordion option.
     - "Does {brand} ship to the US?" → shipping sentence + ships-from sentence when `shipsFrom` is set (see §8 open question) 
     - "Will I pay import duties on {brand} orders?" → duty sentence in full (tooltip text included, since there's no tooltip in an answer). Openers by state (panel; the earlier "Yes, usually." put the hedge on whether you pay, when the real uncertainty is how much):

       | State | Answer |
       |-------|--------|
       | DDP `in_price` | "No. {brand} includes US import duties in its prices, so nothing is due when your order arrives." |
       | DDP `at_checkout` | "Yes, at checkout. {brand} adds US import duties to its order total, so nothing is due on delivery." ("No." would be false: the shopper pays them.) |
       | DDU | "Yes. {brand}'s prices don't include US import duties, so the courier collects any duty owed before delivery. Since August 2025 this can apply to orders of any value. Mela can't estimate the amount." |
       | Unknown | "{brand} hasn't confirmed whether its prices include US import duties. Since August 2025, US duties can apply to orders of any value." No yes or no opener. Wording is a copy test candidate (§7). |
     - "Does {brand} offer free shipping to the US?" → only when a threshold or `free` is known
  4. **Byline**: "Shipping details checked {Month D, YYYY} · Curated by the Mela team". The date is `checkedAt`, shown here only, never on product pages. No date shown → no section (fall back to the neutral passage without a date).
- Brands with no data: the section shows the neutral passage ("{brand} sets its own US shipping costs and duty terms, shown at its checkout...") and only the first FAQ item.

**P1.8: Brand page structured data**
- Add a `FAQPage` node to the brand page schema. `ProfilePage.js:431` builds a single Organization object today; change it to pass an array `[organization, faqPage]`, which `Page.js:223` already wraps into `@graph` (verified). Questions and answers must be **character-identical** to the visible FAQ: build both from one function (e.g. `buildBrandShippingFaq(brandName, brandUsShipping, intl)`), the same single-source pattern as `FAQ_ITEMS` on the homepage.
- `author`/`publisher` reference the existing Organization `@id` (`${marketplaceRootURL}#organization`), per `homepage-faq-geo-signals-prd.md` §3.
- Note: Google limits FAQ rich results to a small set of authoritative sites, so the value here is answer-engine readability, not a SERP feature. Do not set a rich-result target for FAQPage.

**P1.9: Product JSON-LD corrections** (`ListingPageCarousel.js`)
- **Seller (decision): make the seller the brand.** `offers.seller` becomes `{ '@type': 'Organization', name: brandName }` (plus `url: brandStoreUrl` when present). Mela as seller states that Mela sells the product, which breaks the no-retailer rule regardless of shipping. Drop the `description` "...Marketplace for US Indian Diaspora".
- Keep `offers.url` as the Mela page for now (**unverified** whether Google prefers the brand's product URL for a third-party offer; /dev-lead to check against Google's merchant listing docs during the Rich Results Test).
- **Audience:** remove `audience: "Indian Diaspora Shoppers in USA"` and the `additionalProperty` "Target Market: US Indian Diaspora Families". Both contradict "Indian brand discovery for everyone" (positioning decision 2026-07-26). The fallback `generateSEODescription` ("...for Indian diaspora families... Trusted Indian brands delivered to USA") has the same problem plus a delivery claim; replace it.
- Apply the same to `ListingPageCoverPhoto.js` and **remove its blanket `shippingDetails`** (false for any brand without US rates).
- Verify with Google's Rich Results Test on 3 listings (one DDP, one DDU, one unknown); record results in this PRD.

**P1.10: Freshness**
- **Owner**: the brand pipeline owner (founder), who owns `shopify_brands.py`.
- **Cadence**: every quarter, as part of the existing quarterly review trigger (`trig_01DSghwC4tntP5eFdKqKhDGZ`, Jan/Apr/Jul/Oct, TODO 2026-09-25). Extend its checklist: re-run the policy + cart test for any brand whose `us_shipping_checked` is older than 90 days, then export + seed.
- **Event triggers**: a shopper or brand reports a mismatch; a brand is onboarded; a brand changes store domain (Isharya).
- **Fail closed**: if `checkedAt` is older than 180 days or missing, every surface shows the "no data" copy. Stale facts are never shown as current.
- **Legal claim in copy** (panel): "Since August 2025 this can apply to orders of any value" describes US de minimis policy, not brand data. Add it to the quarterly checklist: confirm it still holds before the review closes. Its current status was not checked for this PRD (**unverified**).

**P1.11: Analytics**
- Add `duties_type` (`'ddp' | 'ddu' | 'unknown' | 'none'`) to `brand_clickout` (`util/analytics/brandClickout.js`), set from the brand's `brandUsShipping`. `'unknown'` means the brand profile loaded and duties aren't stated (or data is stale). Send `null` when the event's surface has no brand profile at all (e.g. a heart icon on a search grid card), so missing data is not counted as unknown duties.
- **Also add it to `listing_view` and `saved_listing_toggle`.** With in-stock product pages no longer firing `brand_clickout`, those two events carry nearly all product-page intent. (Extends the brief, which named `brand_clickout` only.)
- GTM: new `DLV - duties_type`, add the parameter to the three GA4 tags, publish a new version; GA4: register Event-scoped custom dimension **Duties Type**. `duties_type` is not a reserved name (checked against the `session_id` lesson in `crossshop-tracking.md` §3); confirm in DebugView anyway.
- Update `crossshop-tracking.md` §3 schema and the handoff doc's open items.
- **Optional (panel):** a `brand_shipping_faq_open` event (`brand`, `question`) when a brand-page FAQ item is expanded. It's the only way to learn whether the collapsed FAQ is ever opened; cheap, and not a P1 blocker.

**P1.12: UTM leak in product JSON-LD**
- `productURL` in `ListingPage.shared.js:259` includes `location.search` and `location.hash` (verified), so `offers.url` carries UTM parameters into structured data. Use the canonical path only. Coordinate with `utm-attribution-restoration-prd.md`, which is changing how UTMs are handled.

### Nice to Have (P2): offer-level structured data

**P2.1: `offers.shippingDetails`** ⛔ blocked
- **Why it's blocked:** with `offers.seller` = Mela and `offers.url` = Mela's page (today), shippingDetails would assert that Mela ships the product. That breaks the no-retailer rule and risks a mismatch in Google's product listings, because Mela's price is "Estimated from Indian retail price" and won't match the brand's checkout.
- **Unblock conditions** (all three):
  1. P1.9 seller = brand shipped and passing the Rich Results Test.
  2. A price-accuracy check: for USD-priced brands, Mela's displayed price matches the brand's US store price (a sample of 10 listings per brand, within 2%). INR-converted brands stay excluded until a decision on price display.
  3. Brand has a re-checked `checkedAt` within 90 days.
- **Shape:** `OfferShippingDetails` with `shippingDestination` US, `shippingRate` from `fee`/`feeCurrency` (flat only), and a separate free-shipping threshold only if Google's schema supports it for this case (**unverified**). Never add `deliveryTime` (not collected).
- If the price-accuracy check fails, the decision is final for v1: keep the Offer without shipping details.

**P2.2: `/saved` brand group threshold text**
- `SavedBrandGroup` header can show the brand's threshold as text ("Nicobar ships free on orders over $150"). Never compare it to the group's saved total. Depends on the comprehension test showing thresholds help rather than add anxiety.

---

## 5. UX Requirements

- **Process gate:** a mobile-first mockup (375px primary, 1440px adaptation) and a `/ux-design panel` review before any P1 build. P0 copy changes go through a lighter `/ux-design` copy check only.
- **Mockup must show all six display states** on the product page at 375px: DDP in-price (chip), DDP at-checkout (Vilvah), DDU flat INR (House of Chikankari), DDU threshold USD (Fizzy Goblet), unknown calculated (Masilo), no data / stale. Plus the brand page section for DDP, DDU, unknown.
- **Longest-string check:** "Hemant & Nandita" and "House of Chikankari" in line 2 at 375px.
- **Two grey lines max** under the price (§4 P1.2): the shipping line (at most two visual lines, enforced by the 100-character test) then the estimate line, so at most three visual lines at 375px. Anything else the design needs goes in a tooltip or on the brand page.
- **Order:** price, shipping and duties, estimate (§4 P1.2).
- **Neutral tone for DDU:** same grey, same weight, no icon other than ⓘ. Never warning color.
- **Positive tone for DDP:** chip only, in the existing trust-chip row.
- **Unknown never implies an answer:** no "probably", no "usually", no default to DDP or DDU.
- **No "last checked" date on product pages** (brand page only).
- **Thresholds are text about the brand's order.** No cart math, no "this item ships free", no progress bars.
- **Tooltips work on touch and keyboard** (P1.4). Tooltip text must also be reachable by screen readers. The ⓘ hit area is at least 24 × 24px (WCAG 2.2 target size) even though the glyph is small. On mobile the popover is full width minus 16px gutters and never renders under the sticky bottom bar.
- **Empty and loading:** while the author entity loads, render nothing in the shipping slot (no layout shift beyond one line; reserve the line height on desktop). Never flash the "no data" copy before data arrives.
- **Copy owner:** every new string lives in en.json (or the shared FAQ builder), reviewed by `/uxr` for Neha and Sarah before P1 ships.
- **Hosted translations:** Console-hosted translations override en.json (`AGENTS.md`). Check the hosted translations asset for the changed keys; if present, edit them in Console too, or the en.json fix won't show (**unverified** whether they're present).

---

## 6. Acceptance Criteria

**P0**
- [ ] P0-1: No rendered page contains "includes shipping & import costs", "Ship to all 50 states", "Ships to all 50 US states", "to all 50 states", "no surprises at your door", "shipped to your door worldwide", or "Indian retail price" (grep built HTML of `/`, one brand page, one listing page, `/saved`; and grep en.json + JS sources).
- [ ] P0-2: The homepage FAQPage JSON-LD and the visible FAQ match character for character after the rewrite (existing test pattern).
- [ ] P0-3: `RedirectTrustSheet` for Fizzy Goblet (DDU) shows "Fizzy Goblet ships to the US" and "US import duties are paid on delivery"; for Nicobar (DDP) shows "Nicobar includes US import duties"; for Ankid (unknown) shows "Ankid doesn't say if US duties are included"; for a brand with no `brandUsShipping`, shows "{brand} sets shipping at its checkout". Unit tests cover all four. Verified once live on `/saved` and on an out-of-stock listing.
- [ ] P0-4: Pluchi listings are closed; Pluchi absent from `/brands`, homepage brand modules, and search; `/brands/pluchi` returns 404 and its `/u/:id` page is noindex. `shopify_brands.py` ACTIVATION CHECKLIST includes the `us_shipping != "none"` rule. (After owner confirmation.)
- [ ] P0-5: `VettingStrip` shipping item is removed; restored as "Every brand ships to the US" only after P0-4 and the Isharya fix are both live.
- [ ] P0-6: Every brand page hero shows "Ships to the US" only when `brandUsShipping.method` is set and not `none`.
- [ ] P0-7: Export + seed: `--dry-run` output shows `brandUsShipping` for 17 live brands (19 minus Pluchi and Isharya), with `null` for Isharya until it is repointed; three brands spot-checked via the Integration API; a brand with no data has `brandUsShipping: null`.
- [ ] P0-8: The exporter fails loudly if any brand's `us_*` fields are on a non-first entry.
- [ ] P0-9: `trust-conversion-signals-prd.md` §3.3a and PRD_TRACKER "Now #1" marked superseded by this PRD.
- [ ] P0-10: No dash characters in any string changed under P0.

**P1**
- [ ] P1-1: `shopify_brands.py` has the six P1.1 fields documented in the docstring and filled for all 25 brands where known; the 10 re-checks in P1.1 are done and dated.
- [ ] P1-2: All six display states render per the approved mockup at 375px and 1440px, in the order price, shipping and duties, estimate; at most two logical / three visual grey lines under the price at 375px with "House of Chikankari" and "Hemant & Nandita"; a unit test asserts every seeded brand's shipping line is at most 100 characters (threshold clause dropped when over); ⓘ hit area ≥24 × 24px; the popover opens upward near the sticky bar.
- [ ] P1-2b: Live product page checked at 375 × 667 before build, with where the shipping line lands on first load recorded here.
- [ ] P1-3: Desktop and mobile use the same component; a unit test renders each `method` × `duties` combination and asserts the exact string, including the fee-unknown fallback (Vilvah) and the merged unknown sentence (Masilo).
- [ ] P1-4: No template ever reads `us_shipping_note` or `brand_content.json` free text (grep).
- [ ] P1-5: INR-sourced fees and thresholds display with "about"; USD-sourced do not. Server-rendered HTML and the hydrated page show the same dollar amounts (no client-side conversion).
- [ ] P1-6: No string compares a threshold to an item or cart value (code review + grep for threshold math).
- [ ] P1-7: A brand with `checkedAt` older than 180 days (test fixture) shows the "no data" copy on every surface.
- [ ] P1-8a: The brand page section renders after the Featured row and `BrandOccasionModule`, before All Products, with every FAQ item collapsed by default; the hero "Shipping details" link scrolls to it; the hero has no "US cards accepted".
- [ ] P1-8: Brand page "Shipping to the US" passage is 40 to 60 words for every live brand (unit test over all seeded brands' data), names the brand, and appears in server-rendered HTML (view-source, not just DOM).
- [ ] P1-9: Brand page FAQPage JSON-LD equals the visible FAQ text exactly (test asserts equality from the shared builder).
- [ ] P1-10: "Last checked" date appears on brand pages and does not appear on product pages.
- [ ] P1-11: Product JSON-LD: `offers.seller.name` is the brand; no `audience`, no "Target Market" property; `offers.url` has no query string or hash. `ListingPageCoverPhoto.js` has no `shippingDetails`. Rich Results Test passed on 3 listings, screenshots linked here.
- [ ] P1-12: Tooltips open on tap (iOS Safari, Android Chrome) and on keyboard focus, close on Escape and outside tap, and are announced by VoiceOver.
- [ ] P1-13: `duties_type` reaches GA4 on `brand_clickout`, `listing_view`, and `saved_listing_toggle` (DebugView, one event each from a DDP and a DDU brand); schema doc updated.
- [ ] P1-14: Copy comprehension test done before P1 ships, chosen wordings recorded in this PRD.
- [ ] P1-15: Outreach emails sent to the 7 unknown-duty brands; replies folded into `shopify_brands.py`.
- [ ] P1-16: Every AC above verified mobile first at 375px, then 1440px, in a real browser (state which device or emulator).

**P2**
- [ ] P2-1: Unblock conditions met and documented; `shippingDetails` only on eligible brands; Rich Results Test clean.

---

## 7. Success Metrics & Measurement

**Reality check on volume.** In the 28 days before 2026-10-04, GA4 recorded 3 `saved_listing_toggle` events from 1 user and 0 `brand_clickout` events, and the internal-traffic filter only became active on 2026-10-04. No quantitative metric below will be statistically meaningful for weeks or months. The qualitative measures are primary for that reason.

| Metric | Type | Baseline | Target | Instrument |
|--------|------|----------|--------|------------|
| Total-cost objections in the next feedback round | Primary | 3 respondents raised shipping/duty cost unprompted (F-013, F-022, F-030). Count price-vs-India (F-037, F-041) separately; it is a non-goal | Of respondents who reach a product page, zero say they couldn't tell the shipping cost or whether duties are included | Same survey + feedback log tagging |
| Copy comprehension | Primary (P1 gate) | n/a | ≥4 of 5 correct on "Will you pay anything when this arrives?" for DDU, DDP and unknown; median anxiety rating no worse for the chosen DDU wording than the current copy | §Research |
| RedirectTrustSheet "helpful" share, DDP vs DDU | Secondary, directional | Current thumbs-up share | No target; report only. **Caveat:** the sheet's question is "Did you find what you were looking for?", which measures finding, not shipping clarity | Existing sentiment webhook + `duties_type` join |
| Clickout rate on DDU brands | Guardrail | 4-week baseline starting at P0 ship (post internal-traffic filter) | Does not drop more than **20%** relative to baseline. Evaluate only once each segment (DDP, DDU) has ≥100 product-page sessions with a save or clickout; until then report "insufficient volume" | `listing_view` → `saved_listing_toggle` → `brand_clickout`, split by `duties_type` |
| Shipping data freshness | Health | n/a | 100% of live brands with `checkedAt` within 120 days | Quarterly review |

**Segmenting:** every metric above is split by `duties_type` (DDP, DDU, unknown). A lower clickout rate on DDU brands after honest disclosure is acceptable and expected; a drop on DDP brands would be a signal that the new block itself hurts.

**Decision rule:** if the guardrail trips on DDU brands, do not revert to hiding duties. Test the alternate DDU wording from the comprehension study first.

### Research (before P1 ships)
- **Five-person copy comprehension test.** Participants: F-013/F-015's respondent (same person; she was charged duties before, so she is the most important tester), F-034 (Megha, opted into the early-tester group), F-042 (Talia; the log calls her a "strong browse-along recruit" but does not record an explicit opt-in, **unverified**), plus two more, at least one non-diaspora shopper with no family tie to the team (the missing cold verdict).
- Show static mockups of the product page block for one DDP, one DDU, one unknown brand. Test 2 to 3 DDU wordings, e.g.:
  - A: "Import duties are extra, paid on delivery"
  - B: "US import duties are paid to the courier on delivery"
  - C: "{brand}'s prices don't include US import duties"
- And 2 unknown wordings: "{brand} doesn't say if US duties are included. Check at its checkout." vs "Check duties at {brand}'s checkout."
- **Order of questions (uxr review: avoid priming):** first an open task, "What would it cost you, in total, to get this to your door?", with no mention of duties. Then probe: "Will you pay anything when it arrives, and to whom?", "Who decides the shipping cost?" (expected: the brand), and a 1 to 5 anxiety rating.
- **Vocabulary variants to include:** "duties" vs "tariffs" (F-013 said "tariff", F-030 "duty"; US news since 2025 says "tariffs"); "courier" vs "delivery company" ("courier" is Indian English usage; a Sarah-type reader says "carrier").
- **Unknown variant to add:** "{brand} hasn't confirmed whether its prices include US duties." "Doesn't say" can read as blaming the brand (supply-side respect).
- **Line 1 check:** ask a non-diaspora participant what "Estimated from the ₹3,600 India price" means to them. It is new on mobile and may read as "this is sold in India, not here".
- **Duties chip (panel):** show one brand with the "Duties included" chip next to one without and ask which they'd rather buy from and why. Only users can tell whether the chip reads as "the other brand is worse".
- **FAQ opener (panel, low priority):** does "Yes." followed by "any duty owed" read as more certain than it should?
- **Ask, don't claim:** whether participants have paid a carrier processing or brokerage fee on top of duties. Plausible for DDU shipments but **unverified**, so it stays out of copy unless confirmed.
- **Sample rule:** at least one participant who is non-diaspora and has never ordered from India (the Sarah gap: none of the 3 named recruits fits). Screen every participant for prior duty experience and record it next to their results.

---

## 8. Dependencies & Risks

**Dependencies**
- 🔴 **Isharya repoint** (TODO 2026-10-06, `a301f8c`): this PRD must not show Isharya's US terms until listings link to isharya.co. The exporter guard in P0.9 enforces it.
- **Data pipeline (decided):**
  1. `scripts/export_brand_content.py` adds the `us_*` fields to `brand_content.json` (P0.9, P1.1).
  2. `product-listing-integration/scripts/seed-brand-profiles.js` writes `publicData.brandUsShipping` (one nested key), with `null` for brands without data.
  3. Read path: product pages read the brand profile (`ListingPage.duck.js` already loads `include: ['author', ...]`); `/saved` likewise (`savedListings.duck.js`). No copy onto listings. Copying onto listings (`create-listings.js`) becomes relevant only for a "duties included" filter, a v1 non-goal.
  4. Production: not seeded. Steps added to `dev-to-production-migration-prd.md` §3d.
- **Brand outreach** to the 7 unknown-duty brands (Masilo, Pluchi, Aagghhoo, Baby Forest, ChooseKind, The Alternate India, Ankid) before P1 ships. Ask: who pays US duties (in price, at checkout, on delivery); whether they accept returns from the US; where US orders ship from. P1 ships with "unknown" copy for any brand that hasn't answered. (Pluchi: ask whether US shipping is planned.)
- **Mockup + `/ux-design panel`** before P1 build; **comprehension test** before P1 ship.
- **Hosted translations** in Console may override en.json keys (§5).

**Risks**
| Risk | Mitigation |
|------|-----------|
| Data goes stale (brands change rates, Vilvah's own pages already disagree) | Owner + quarterly cadence + 180-day fail-closed (P1.10); brand-page date is visible so shoppers see the age |
| INR conversion drift (~₹88/$ fixed in notes) | INR-sourced values show "about"; store source currency (P1.1) |
| Honest DDU disclosure lowers clickouts | Accepted (§7); guardrail splits DDP/DDU so a DDP drop is caught |
| Shipping line widens price-vs-India gap for Neha (F-037, F-041) | Accepted and stated in Non-Goals; tracked separately |
| Wording implies Mela ships or collects duties | Brand-as-subject rule; `/uxr` review; P0-1 grep |
| Seeding dev = changing the live site | `--dry-run`, Integration API spot-check, and `null` for no-data brands |
| "Check duties at checkout" falsely reassures for brands that are really DDU | Test alternate wording (§7 Research) |
| Google treats Mela's offer as a merchant listing with a mismatched price | P1.9 seller = brand; P2 gated on price accuracy |
| Returns: "Returns handled by {brand}" implies returns exist | Open question below; P0.6 FAQ rewrite is true either way |

**Data limits (state in any public copy review):** INR thresholds converted at ~₹88/$; three brands have partly unverified notes per the brief (Hemant & Nandita below $199, Saphed, ChooseKind), and the re-check list in P1.1 adds seven more.

**Open questions**
1. **International returns.** Per the brief, Nicobar, Polite Society, Needledust and Saphed don't accept returns from abroad. This is not in `shopify_brands.py` and is **unverified**. Should a `us_returns` field be collected in the same re-check pass, and shown in the trust sheet in place of "Returns handled by {brand}"? Recommendation: collect it now (cheap during the re-check), decide display after the comprehension test.
2. **Ships-from.** Surface `shipsFrom` to shoppers? It answers F-036's "straight from India" assumption, but "ships from a US warehouse" may read as less authentic to some shoppers. Recommendation: include it only in the brand-page FAQ answer for v1 (no product-page line), and add a ships-from question to the comprehension test.
3. **Daughters of India** fit decision (TODO 2026-10-04) and its state sales tax: if activated, does the passage mention sales tax? Recommendation: yes, one clause, since it changes the total.
4. ~~**"US cards accepted"** is kept but was never tested per brand.~~ **Resolved at the panel (2026-10-06):** removed from the brand hero; on the trust sheet only for brands checked in the re-check pass (P1.5). A richer card and payment signal, plus the homepage "US cards verified" claim, is a separate TODO (2026-10-06).

---

## 9. Rollout

**Order:**
1. **Prerequisite:** Isharya repoint (separate 🔴 item).
2. **P0 copy** (P0.1, P0.3, P0.5, P0.6 neutral versions, P0.7 doc updates), one PR. Owner confirmation on Pluchi, then P0.8.
3. **P0.9 export + seed** to dev (= live) with `--dry-run` first; then P0.2 and P0.4 per-brand.
4. **Restore** the VettingStrip item and the full homepage FAQ Q1 once Pluchi is delisted and Isharya is live.
5. **In parallel:** brand outreach emails; P1.1 data re-check pass; recruit and run the comprehension test; mockup + `/ux-design panel`.
6. **P1 build:** P1.2 to P1.12. P1.9 and P1.12 (JSON-LD fixes) can ship independently and early; they don't depend on the mockup.
7. **Measure:** baseline window starts at P0 ship; report at 4 weeks with the volume caveat.
8. **P2:** only if unblock conditions are met.

**Production (when the prod Sharetribe environment exists):** run the exporter, then `NODE_ENV=production node scripts/seed-brand-profiles.js --dry-run`, then the real run; verify `brandUsShipping` on 3 prod brand profiles; confirm Pluchi is not in the prod `configBrands.js` map. Added to `dev-to-production-migration-prd.md` §3d.

**Rollback:** copy changes revert with the PR. Data: re-seed with `brandUsShipping: null` for every brand, which drops all surfaces to the neutral "no data" copy (never the old false claims).

---

## 10. Out of Scope / Future Considerations
- Landed-cost calculator and duty estimates (would need HS codes and per-product data).
- "Duties included" filter or sort (requires copying data onto listings via `create-listings.js`).
- Price display changes to address price vs India.
- Brokered DDP via a logistics partner (Xportel, TODO F-013 item): would change what brands can offer, not what Mela displays.
- Delivery-time display (not collected; Neha's "vague shipping estimates" trust signal remains open).
- Fixing `CertificationBadge` tooltips for touch (reuse P1.4 when done).

---

## 11. Review Log (2026-10-06)

All three reviews ran on the draft and are folded in above.

**/dev-lead** (pipeline, schema, structured data). Complexity medium, scope M.
- Converting INR at render would break SSR/client parity (live rate is browser-only, SSR falls back to 1/83) and break FAQ/JSON-LD equality → convert at export (P1.1).
- No listing-page code reads the author's profile publicData yet → spike first (P0.2).
- `saved_listing_toggle` from grid cards may lack brand data → `null`, not `unknown` (P1.11).
- Delisted brand pages stay reachable → 404 `/brands/pluchi`, noindex `/u/:id` (P0.8).
- Use one helper module, not one big ICU select; `ProfilePage.js` must pass a schema array (P1.2, P1.8).

**/ux-design** (placement, mobile).
- Brand grid scrolls infinitely, so "after the grid" can't be reached → section moved above All Products, plus a hero anchor link (P1.6, P1.7).
- On desktop the DDP chip is far from the price → line 2 adds "Duties included." on desktop (P1.2).
- "Two lines" clarified as 2 logical / 3 visual; ⓘ hit area 24 × 24px; popover never under the sticky bar (§5).
- Trust sheet items drop the repeated brand name (heading carries it); Continue stays visible at 375 × 667 (P1.5).

**/uxr** (copy, personas, evidence).
- Example passages said "from India" without data → removed; origin only from `shipsFrom` (Appendix A).
- F-013 citation overstated (she didn't say the charge came at the door) → softened (§1).
- Test design: open total-cost task before any duty question; add "tariffs" and "delivery company" variants, a brand-neutral unknown variant, a line 1 check, and a non-diaspora participant (§7 Research).

**Mobile mockup** (`nimbalyst-local/mockups/international-shipping-transparency-mobile.mockup.html`, line counts measured in Chrome).
- `flat_rate_free_over_threshold` had no template for an unknown fee (Vilvah) → fallback added (P1.2).
- Unknown duties plus unknown shipping cost took 4 visual lines (Masilo) → one merged sentence (P1.2).
- Brand named once per block, second sentence uses "It" (copy rules).
- Brand page section is about 440px tall → options and recommendation for the panel (P1.7). Expanded trust sheet not measured (P1.5).

**/ux-design panel** (P1 gate, 2026-10-06; mockup updated and measured in Chrome at 375px).
1. Brand page section height: passage always visible, FAQ collapsed (382px, down from 438); no "Read more" (P1.7).
2. Placement kept, after Featured and `BrandOccasionModule`; cross-brand shipping page escalated (P1.7).
3. "US cards accepted" removed from the brand hero; on the trust sheet only where checked (P1.5, P1.6, §8 Q4).
4. "Duties included" chip kept with guardrails: no grid cards, no sort or filter input, `duties_type` split, brands told in outreach (P1.3).
5. Mobile estimate line kept: grid cards already show the INR figure (§1 correction).
6. Line and pronoun rules kept; the line limit becomes a 100-character unit test with a drop-the-threshold fallback (P1.2).
7. Duty FAQ openers per state; "usually" dropped; "Yes, at checkout." for Vilvah-type brands (P1.7).
8. Expanded trust sheet measured: Continue stays visible, no spare room; keyboard not checked (P1.5).
- New finding: at 375 × 667 the shipping line loaded under the sticky bar while the estimate line was visible. **Owner decision (2026-10-06): shipping and duties come directly after the price, then the estimate** (P1.2). Live page check still required.
- Copy fixes: Appendix A Nicobar ("Shipping is" broke the brand-as-subject rule) and Ankid ("check the total at checkout", flagged by /uxr) passages.

**Not yet done (required before build):** the live product page fold check (P1-2b), the trust sheet with the on-screen keyboard on a real phone (P1.5), the desktop 1440px adaptation, and loading states.

---

## Appendix A: Example passages (40 to 60 words)

Generated from templates; shown here to size the copy and check tone. Origin ("from India", "from a US warehouse") appears only when `shipsFrom` is set; it is known for 3 brands only (uxr review caught an earlier draft stating "from India" without data). Numbers come from the 2026-10-04 notes and must be re-checked where P1.1 says so.

**Nicobar (DDP, USD, threshold; threshold pending re-check)** (43 words)
> Nicobar ships to US addresses for $30 per order, free on orders over $150. Nicobar includes US import duties in its prices, so nothing is due when your order arrives. You pay on Nicobar's own store, which sets the final price and shipping cost.

**House of Chikankari (DDU, INR, flat)** (50 words)
> House of Chikankari ships to US addresses for about $34 per order. Its prices don't include US import duties: the courier collects them before delivery, and since August 2025 that can apply to orders of any value. You pay on House of Chikankari's own store, which sets the final cost.

**Ankid (unknown, INR, flat)** (42 words)
> Ankid ships to US addresses for about $28 per order. Ankid hasn't confirmed whether its prices include US import duties. Since August 2025, US duties can apply to orders of any value. You pay on Ankid's own store, which sets the final cost.

## Appendix B: Brand data snapshot (from `shopify_brands.py`, checked 2026-10-04)

| Brand | Live? | Duties | Method | Fee | Free over | Notes for display |
|-------|-------|--------|--------|-----|-----------|-------------------|
| Masilo | Live | unknown | calculated | — | — | Outreach |
| SuperBottoms | Live | DDU | calculated | — | — | |
| Pluchi | Live | unknown | none | — | — | Delist (P0.8) |
| Aagghhoo | Live | unknown | calculated | — | — | Outreach |
| Baby Forest | Live | unknown | calculated | — | — | Outreach; high rates ($51 to $116) |
| ChooseKind | Live | unknown | calculated, free over | — | $150 | Outreach; threshold re-check |
| Gully Labs | Live | DDP | flat | ₹6,000 (~$68) | — | |
| The Alternate India | Live | unknown | flat | ₹2,000 (~$23) | — | Outreach |
| Banjaaran Studio | Live | DDP | free | — | — | |
| Fizzy Goblet | Live | DDU | flat, free over | $15 | $100 | |
| Tarinika | Live | DDU | flat, free over | $7.99 | $99 | Ships from US or India |
| Isharya | Live | DDU | flat, free over | $20 | $250 | Blocked on repoint; re-check |
| Vilvah Store | Live | DDP (at checkout) | flat, free over | re-check | $69 | Re-check; conflicting policy |
| Nicobar | Live | DDP | flat, free over | $30 | $150 | Threshold re-check |
| The Nesavu | Live | DDU | flat | ₹3,487 (~$40) | — | |
| House of Chikankari | Live | DDU | flat | ₹2,950 (~$34) | — | F-013/F-015 brand |
| Kaunteya | Live | DDU | flat, free over | ₹4,500 (~$51) | ₹33,000 (~$350 to $375) | Threshold source currency INR |
| Polite Society | Live | DDU | flat | ₹2,500 (~$28) | — | Banner threshold contradicted by cart |
| Ankid | Live | unknown | flat | ₹2,500 (~$28) | — | Outreach |
| Suta | Next wave | DDU | flat, free over | $20 | unknown | |
| Little Muffet | Next wave | DDU | flat, free over | $20 | $200 | |
| Needledust | Next wave | DDU | flat, free over | ₹4,000 (~$45) | ₹20,000 (~$227) | Policy states $200 and $250 |
| Saphed | Next wave | DDU | free | — | — | Empty-cart test only |
| Daughters of India | Next wave | DDP | flat, free over | $12 (policy) | $380 | US warehouse; sales tax; fit decision |
| Hemant & Nandita | Next wave | DDP | calculated, free over | — | $199 | Ships from India or US |
