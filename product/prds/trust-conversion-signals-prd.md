# Trust & Conversion Signals PRD

## Document Information
- **Created**: 2026-04-14
- **Last updated**: 2026-04-17
- **Status**: Active
- **Owner**: Product Team
- **Related Docs**:
  - `product/prds/homepage-redesign-prd.md`
  - `product/prds/ai-ready-product-discovery-prd.md`
  - `product/prds/brand-storefront-prd.md`
  - `product/prds/pre-redirect-sentiment-prd.md`

---

## Executive Summary

**Problem**: Mela sells from Indian brands to US shoppers — a cross-border trust gap that no major US marketplace has had to solve before. Shoppers arrive with a bundle of anxieties: *Do these ship to the US? Can I use my credit card? Are these products safe? Will I be able to return?* These doubts fire before any purchase intent forms. Without explicit signals that answer them, users bounce rather than explore.

**Solution**: A coherent system of trust and conversion signals — defined by surface area, signal type, data source, and SEO/AEO value — deployed consistently across the homepage, listing cards, product pages, and the pre-redirect moment.

**Scope**: This PRD covers signal design and placement. It does not cover the review system, order tracking, or wishlist features (separate PRDs). It catalogs what is live today and specifies what to build next.

---

## Build Status Summary *(updated 2026-04-17)*

| Item | Priority | Status |
|------|----------|--------|
| Pre-redirect trust moment (`RedirectTrustSheet`) | P0 | ✅ Shipped |
| ListingPage certification chips (`ListingTrustChips`) | P0 | ✅ Shipped |
| ListingPage occasion chips (from `itemAspects`) | P0 | ✅ Shipped |
| CTA copy: "Shop on {brand} →" | P0 | ✅ Shipped |
| ItemSpecifics true bottom sheet (mobile fix) | UX debt | ✅ Shipped |
| "Ships to US · US cards · Sold by [Brand]" static line near CTA | P0 | ❌ Not built |
| `isBestseller` pipeline automation | P0 | ❌ Not built |
| "Mela Verified" meta-badge | P1 | ❌ Not built |
| Return policy + shipping estimate on ListingPage | P1 | ❌ Not built |
| Brand tenure signal on BrandCardHome | P1 | ❌ Not built |

---

## 1. Signal Taxonomy

Signals fall into four types. Each type answers a different shopper question.

| Type | Shopper question answered | Examples |
|------|--------------------------|---------|
| **Trust** | "Is this brand/product legitimate?" | GOTS certified, Mela Verified, Quality Vetted |
| **Geographic** | "Does this work for me in the US?" | Ships to the US, US Cards on Brand Stores, De minimis threshold note |
| **Conversion** | "Should I act now?" | Bestseller, Low Stock, New Arrival |
| **Transparency** | "How does Mela work?" | Shop Directly With the Brand, Return Policies, Honest affiliate model note |

A well-designed signal surface uses all four types at the right moment. The rule: **Trust → Geographic → Conversion**. Establish credibility first, remove geographic anxiety second, then and only then apply urgency.

---

## 2. Current State (Signals Live Today)

### 2a. Listing Card — `ListingCard.js`

**TrustBadges** (overlaid on product image):
- `gots_certified` → "GOTS"
- `non_toxic_dyes` → "Non-toxic"
- `bpa_free` → "BPA Free"
- `ce_certified` → "CE"
- `bis_approved` → "BIS"
- Source: `publicData.certification[]`
- Max displayed: 2 (top priority)

**ConversionBadges** (priority-ordered, shows one):
- `isBestseller = true` → "Bestseller" badge (amber)
- `stockCount <= 5 && stockCount > 0` → "Only {n} left" (urgency/red)
- `isNew = true` (listing age < 30 days) → "New Arrival"
- Source: `publicData.isBestseller`, `currentStock.quantity`, `listing.attributes.createdAt`

**INR Price Equivalent**:
- Shows `₹{amount}` below USD price when `publicData.priceInINR` is set
- Reassures first-gen shoppers that the price is fair in Indian context

### 2b. Homepage Hero — `HeroSection.js`

Five trust badges rendered as emoji + text strip (wraps on mobile):
1. 🌱 GOTS Certified
2. ✅ Quality Verified
3. 🇮🇳 Made in India
4. 🇺🇸 Ships to the US *(added 2026-04-14)*
5. 💳 US Cards on Brand Stores *(added 2026-04-14)*

### 2c. Homepage TrustAssurance — `TrustAssurance.js`

**Section title**: "Every Brand Here Earned Its Place" *(updated 2026-05-25)*
**Section subtitle**: "We do the research so you don't have to." *(updated 2026-05-25)*

**How We Vet Every Brand** (3 cards) *(section renamed from "Our Quality Promise" 2026-05-25)*: Proven Track Record, Verified Indian Brands, Sustainably Made

**Safety Certifications** (4 badges): GOTS Certified, Organic Cotton, Oeko-Tex, Eco-Friendly

**Shopping on Brand Sites** (4 cards) *(section renamed from "Shopping with Confidence" 2026-05-25)*:
1. 🛍️ Shop Directly With the Brand *(renamed from "Transact on Brand Sites" 2026-05-25)*
2. 📦 Ships Directly to the US *(updated 2026-04-14)*
3. ↩️ Brand Return Policies
4. 💳 US Cards Accepted on Brand Stores *(added 2026-04-14)*
~~5. ✅ Mela Curation Promise~~ *(removed 2026-05-25 — curation story moved to section title)*

**US Shopper FAQ** *(added 2026-04-14)* — 5 static Q&A cards:
- Do Indian brands on Mela ship to the United States?
- Can I use my US credit card to shop on Mela?
- Are there customs duties or import taxes?
- What is the return policy for brands on Mela?
- How long does shipping from India to the US take?

**Customer Service CTA**: "Need Help? We're Here for You" → Contact Us + Help Center

### 2d. Homepage Schema — `MelaHomePage.js`

- `Store.areaServed: { Country: "United States" }` *(added 2026-04-14)*
- `Store.currenciesAccepted: "USD"` *(added 2026-04-14)*
- `FAQPage` JSON-LD with all 5 US Shopper FAQ Q&As *(added 2026-04-14)*
- Listing pages: `OfferShippingDetails` targeting `DefinedRegion: "US"`

### 2e. BrandCardHome — `BrandCardHome.js`
- Certification badges
- Establishment year
- Brand origin (India)

### 2f. ListingPage — `ListingPageCoverPhoto.js` + `ListingPageCarousel.js` *(added 2026-04-17)*

**`ListingTrustChips`** — `src/components/ListingTrustChips/ListingTrustChips.js`
- Renders `publicData.certification[]` as green pill chips (✓ GOTS Certified, Non-toxic, etc.)
- Renders occasion/use/season context from `publicData.itemAspects` as amber chips
- Placed above ItemSpecifics, below the product title — highest scan position
- Returns null when no data — backward-compatible

**`RedirectTrustSheet`** — `src/components/RedirectTrustSheet/RedirectTrustSheet.js`
- Combined pre-redirect trust context + sentiment collection in one bottom sheet
- Triggered on first "Shop on [Brand] →" CTA click per session (`mela_redirect_trust_shown` session key)
- Subsequent CTA clicks in same session skip the sheet and redirect directly
- Trust content: "You're visiting [Brand]'s official store" + 🔒 secure checkout + 🇺🇸 ships to US + ↩️ returns
- Sentiment: thumbs up/down → expands free-text + optional email (posts to webhook as `event: 'pre_shopify_redirect'`)
- "Continue to [Brand] →" button always pinned at bottom — accessible at all states
- Session key is separate from `SentimentSheet`'s 15-second timer (`mela_sentiment_shown`) — both can show in the same session
- `OrderPanel` gained `onShopNow` prop to intercept the CTA without touching Sharetribe's default flow

**CTA copy**: "Shop on {brand} →" (was "Shop from {brand}")

**ItemSpecifics "show more"**: Replaced full-screen `Modal` with native bottom sheet (slide-up, 75vh max, drag handle, backdrop) — `src/components/ItemSpecifics/`

---

## 3. Signal Gaps — What to Build Next

### P0 — Directly blocking conversion

#### 3.1 Pre-Redirect Trust Moment ✅ Shipped 2026-04-17
See §2f above. Full implementation in `RedirectTrustSheet`.

#### 3.2 `isBestseller` Flag — Data Pipeline Gap
**Surface**: ListingCard `ConversionBadges` (already built, badge is live but dead)
**Problem**: The `isBestseller` signal renders correctly when `publicData.isBestseller = true`, but there is no pipeline that sets this flag. It is currently set manually (if at all).
**Solution**: A weekly script `product-listing-integration/scripts/bestseller-tagger.js`:
- Query Shopify orders (last 90 days) per brand
- Rank listings by order count within each L1 category
- Tag top 20% as `isBestseller = true` via Sharetribe listing update API
- Clear the flag on listings that fall out of the top 20%
- Cap per category: max 3 listings tagged as Bestseller per L1 to avoid badge inflation

#### 3.3 Listing Page — Remaining Trust Signals
**Surface**: `ListingPageCoverPhoto.js`, `ListingPageCarousel.js`
**Status**: Certification + occasion chips ✅ shipped. Three signals remain:

**3.3a — "Ships to US · US cards · Sold by [Brand]" static line** ❌ Not built
- A single line of static copy between `ListingTrustChips` and `ItemSpecifics` (or above the OrderPanel CTA column)
- Copy: `🇺🇸 Ships to the US  ·  💳 US cards on brand's store  ·  ✅ Sold by [Brand]`
- Data: static copy + `publicData.brand`. No new fields needed.
- Effort: ~30 minutes. Inline JSX + 3 CSS lines.

**3.3b — Estimated shipping time** ❌ Not built (see §3.7)

**3.3c — Return policy** ❌ Not built (see §3.5)

### P1 — Meaningful uplift, no blockers

#### 3.4 "Mela Verified" Meta-Badge
**Surface**: `ListingTrustChips`, BrandCardHome, BrandStorefront (when built)
**Problem**: Individual certification badges (GOTS, BIS, etc.) require product knowledge to evaluate. Many US shoppers don't know what GOTS means. A single Mela endorsement badge carries more weight as a shortcut.
**Signal**: `✅ Mela Verified` — shown when a brand/listing meets Mela's curation bar
**Derivable today** — no new pipeline fields needed:
```javascript
const isMelaVerified = publicData.certification?.length > 0
  && daysSince(author.attributes.createdAt) >= 30;
```
**Criteria for the badge** (internal checklist, not shown to users):
- Minimum 1 safety certification (any of: GOTS, BIS, Oeko-Tex, CE, BPA Free)
- Brand has been active on Mela for ≥ 30 days
- No open quality complaints
**Where**: Add a `melaVerified` chip variant to `ListingTrustChips`; add to `BrandCardHome`
**AEO value**: A named badge ("Mela Verified") creates a citable entity that AI engines can reference in answers: *"Mela only features Mela Verified brands"*
**Schema**: Add as `additionalProperty` in Product JSON-LD

#### 3.5 Return Policy Surfacing
**Surface**: ListingPage, near the CTA
**Problem**: "Brand Return Policies" is acknowledged in the TrustAssurance section, but the specific policy for the brand a user is looking at is not visible until they're on the brand's Shopify.
**Signal**: Show the brand's return window on the listing page — e.g., "30-day returns" or "Exchange only"
**Data source**: `publicData.returnPolicy` — seed manually for initial brands via listing ingestion script
**Display**: Combine with §3.7 into a single `📦 Est. delivery 7–14 days · ↩️ 30-day returns` line
**Note**: Do not show this signal if return policy data is missing — a blank is worse than absent

#### 3.6 Brand Tenure Signal
**Surface**: BrandCardHome, BrandStorefront
**Signal**: "Mela Partner since [year]" — builds trust through longevity
**Data source**: `author.attributes.createdAt` (already available, no new field needed)
**Copy logic**:
- `< 1 year` → "Joined 2025"
- `≥ 1 year` → "Verified Partner since 2023"
- `≥ 3 years` → "3+ years on Mela"

#### 3.7 Shipping Estimate on Listing Page
**Surface**: ListingPage, near the CTA (combine with §3.5)
**Signal**: "Estimated delivery: 7–14 business days to the US"
**Data source**: `publicData.shippingTimeDays` (default `"7–14"` when not set)
**AEO value**: Pairs with the `OfferShippingDetails` schema already in place — the visible text reinforces the machine-readable signal for AI answer engines

### P2 — Nice to have, lower urgency

#### 3.8 "X people saved this" Social Proof Counter
**Surface**: ListingPage, ListingCard
**Signal**: When a listing has ≥ 5 saves in Mela's SavedItems system, show "❤️ {n} people love this"
**Data source**: Aggregate from `SavedItems` Sharetribe API
**Risk**: Small catalog means most products will show 0 — render only when count ≥ 5

#### 3.9 Brand Country-of-Origin Badge
**Surface**: ListingCard (secondary badge row)
**Signal**: "🇮🇳 Made in India" on each card (currently only in HeroSection)
**Data source**: `publicData.countryOfOrigin` or brand-level metadata

#### 3.10 Category-Level Trust Signals on SearchPage
**Surface**: SearchResultsPanel header / filter area
**Signal**: When browsing Baby & Kids, surface "All products GOTS-certified or better" when that filter is active
**AEO value**: Category-level trust copy is indexed and helps AI engines answer "are Mela baby products certified safe?"

---

## 4. Signal Placement Map *(updated 2026-04-17)*

| Surface | Trust | Geographic | Conversion | Transparency |
|---------|-------|------------|------------|--------------|
| Hero badges | GOTS Certified, Quality Verified | Ships to US | — | Made in India |
| ListingCard | TrustBadges (certs) | — | Bestseller, Low Stock, New Arrival | — |
| TrustAssurance | How We Vet Every Brand, Certifications | Ships to US (card), US Cards (card), FAQ | — | Shop Directly With the Brand, Return Policies |
| ListingPage | ✅ Cert chips (`ListingTrustChips`), ✅ Occasion chips, Mela Verified *(P1)* | ❌ Ships to US line *(P0 gap)*, Shipping estimate *(P1)* | — | ❌ Sold by [Brand] *(P0 gap)* |
| Pre-redirect | ✅ Trust context (`RedirectTrustSheet`) | ✅ Ships to US, US cards (`RedirectTrustSheet`) | — | ✅ Shopify checkout security |
| BrandCardHome | Mela Verified *(P1)*, Tenure *(P1)* | — | — | — |
| BrandStorefront | All brand trust *(future)* | Shipping from brand *(future)* | — | Brand story |

---

## 5. SEO / AEO / GEO Signal Coverage

| Signal | Visible HTML | JSON-LD schema | AI-extractable |
|--------|-------------|----------------|---------------|
| Ships to US | ✅ Hero badge, TrustAssurance card | ✅ `Store.areaServed` | ✅ |
| US cards on brand stores | ✅ Hero badge, TrustAssurance card | — (omitted — Mela doesn't process payments) | Partial |
| FAQ: ships to US? | ✅ TrustAssurance FAQ block | ✅ `FAQPage` JSON-LD | ✅ |
| FAQ: can I use US card? | ✅ TrustAssurance FAQ block | ✅ `FAQPage` JSON-LD | ✅ |
| FAQ: customs duties? | ✅ TrustAssurance FAQ block | ✅ `FAQPage` JSON-LD | ✅ |
| FAQ: return policy? | ✅ TrustAssurance FAQ block | ✅ `FAQPage` JSON-LD | ✅ |
| FAQ: shipping time? | ✅ TrustAssurance FAQ block | ✅ `FAQPage` JSON-LD | ✅ |
| Listing shipping to US | Via schema | ✅ `OfferShippingDetails` | ✅ |
| Bestseller | ✅ ListingCard badge | — | No (dynamic data) |
| GOTS certification | ✅ ListingCard badge + ✅ ListingTrustChips | ✅ `PropertyValue` in Product schema | ✅ |
| Occasion context | ✅ ListingTrustChips (amber chips) | — | No |
| Pre-redirect trust | ✅ RedirectTrustSheet | — | No (not indexed) |
| Mela Verified *(P1)* | Planned in `ListingTrustChips` | Planned as `additionalProperty` | Planned |

---

## 6. Data Model Requirements

| Signal | Data field | Where set | Current status |
|--------|-----------|-----------|----------------|
| Bestseller | `publicData.isBestseller` (boolean) | Weekly tagger script *(not yet built)* | Field exists, not automated |
| Low stock | `currentStock.quantity` | Sharetribe stock system | Live |
| New arrival | `listing.attributes.createdAt` | Auto (Sharetribe) | Live |
| Certifications | `publicData.certification[]` | Brand/product ingestion | Live |
| INR price | `publicData.priceInINR` | Shopify ingestion pipeline | Live |
| Certification chips | `publicData.certification[]` | Same as above | ✅ Live (rendered in `ListingTrustChips`) |
| Occasion chips | `publicData.itemAspects` (fieldId: occasion/use/season) | Enrichment pipeline | ✅ Live (rendered in `ListingTrustChips`) |
| Shipping time | `publicData.shippingTimeDays` | Brand metadata | Not yet set (falls back to "7–14") |
| Return policy | `publicData.returnPolicy` | Brand metadata (manual seed) | Not yet set |
| Brand tenure | `author.createdAt` | Auto (Sharetribe) | Live (derivable) |
| Mela Verified | Derived: `certification.length > 0` + `createdAt >= 30 days` | No new field needed | Derivable today |

---

## 7. User Stories

| As a... | I want to... | So that... | Priority |
|---------|-------------|------------|----------|
| US first-time visitor | See "Ships to the US" above the fold | I don't abandon because I assume they don't ship here | P0 |
| US shopper unsure about payment | See "US Cards on Brand Stores" | I know I can use my Visa without foreign transaction issues | P0 |
| Shopper clicking to a brand's Shopify | See a trust reassurance before redirect | I feel safe leaving Mela and don't feel tricked | P0 ✅ |
| Parent scanning search results | See a Bestseller badge on popular items | I can quickly shortlist without reading every description | P0 |
| Parent on a product page | See trust signals on the page (not just the card) | I feel confident at the exact moment I'm deciding to click through | P0 ✅ (partial) |
| Shopper with customs anxiety | Read a clear answer about import duties | I'm not surprised by unexpected charges at checkout | P1 |
| New visitor evaluating Mela | See "Mela Verified" on curated brands | I understand Mela has a vetting bar, not just a directory | P1 |
| Brand partner | See their tenure and certifications surfaced | I feel that Mela represents my brand fairly | P1 |

---

## 8. Acceptance Criteria

### P0 Items

**Pre-redirect trust moment:** ✅ Complete
- [x] `RedirectTrustSheet` shows on first CTA click per session
- [x] Brand name, trust signals (checkout security, ships to US, US cards, returns) visible
- [x] Sentiment collection embedded (thumbs → free text → submit/skip)
- [x] "Continue to [Brand] →" always accessible — never blocked by sentiment
- [x] Session key `mela_redirect_trust_shown` gates to once per session; subsequent clicks redirect directly

**ListingPage certification + occasion chips:** ✅ Complete
- [x] `ListingTrustChips` renders cert chips from `publicData.certification[]` (green)
- [x] `ListingTrustChips` renders occasion chips from `itemAspects` fieldIds `occasion/use/use_case/season` (amber)
- [x] Returns null when no data — no empty space rendered
- [x] Applied to both `ListingPageCoverPhoto` and `ListingPageCarousel`

**"Ships to US · US cards · Sold by [Brand]" line near CTA:** ❌ Outstanding
- [ ] Static line visible on ListingPage above or below the OrderPanel CTA
- [ ] Uses `publicData.brand`; no new data fields required

**Bestseller pipeline:**
- [ ] Weekly job sets `publicData.isBestseller = true` on top 20% of listings by orders per L1 category (last 90 days)
- [ ] Badge cap: no more than 3 listings per L1 tagged `isBestseller` at any time
- [ ] `ListingCard.ConversionBadges` renders "Bestseller" for those listings

### P1 Items

**Mela Verified badge:**
- [ ] Badge renders on `ListingTrustChips` when `certification.length > 0` AND brand join date > 30 days
- [ ] Badge renders on BrandCardHome under same criteria
- [ ] Described as `additionalProperty` in Product JSON-LD schema

**Return policy + shipping estimate:**
- [ ] `publicData.returnPolicy` field seeded for all active brands
- [ ] `publicData.shippingTimeDays` seeded for all active brands (default: `"7–14"`)
- [ ] Combined `📦 Est. delivery X days · ↩️ Y-day returns` line on ListingPage; suppressed if both fields null

**Brand tenure on BrandCardHome:**
- [ ] Tenure copy derived from `author.attributes.createdAt`; renders per copy logic in §3.6

---

## 9. Recommended Build Order

```
1. "Ships to US · US cards · Sold by [Brand]" static line    ← ~30 min, completes P0
2. Bestseller pipeline script                                 ← ~3 hrs, unlocks dead badge
3. Mela Verified chip (derive from existing data)             ← ~1 hr, high AEO value
4. Return policy + shipping estimate (seed data + display)    ← ~half day total
5. Brand tenure on BrandCardHome                              ← ~1 hr, after BrandStorefront PRD
```

---

## 10. Out of Scope

- Community reviews / ratings system (separate PRD)
- "X people are viewing this" live urgency (requires real-time infrastructure)
- Price-drop alerts
- Loyalty / repeat purchase signals
- Personalised trust signals based on user history
