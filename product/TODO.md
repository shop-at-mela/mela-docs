# Mela Dev TODO

Running log of shipped work and next actions. Newest entry at top.

## 2026-08-25

### Shipped
- `feat(analytics)` — `entry_source` (+ session id) attached to every `page_view`, including the first automatic gtag one; `utm_*` stripped from the visible URL post-capture. gifting-festival-traffic-prd.md Day 2 Phase 0.
- `feat(gifting)` — New `/gifts` + `/occasions/:slug` landing pages (one `GiftingPage` container, delegates to `SearchPage.duck`'s `loadData`, no new reducer), with price-band and recipient filter chips, and opt-in occasion chips on `ListingCard`. Day 2 Phase 1.
- `refactor(occasion-strip)` — `isDiwaliSeason()` → `getActiveSeasonOccasion(date)`: OccasionStrip now selects 2-3 relevant panels from the full near-term festival sequence (Raksha Bandhan → Navratri → Karva Chauth → Diwali → Bhai Dooj → wedding season) instead of always showing the same 2. `BrandOccasionModule` updated to match (still shows every occasion with qualifying inventory, unlike OccasionStrip, since it has no extra fetch cost). Day 2 Phase 2.
- `feat(search)` — Gifting/occasion-context searches default to a bestseller-aware sort (`pub_isBestseller,createdAt`, centralized in one `GIFTING_DEFAULT_SORT` constant) instead of `createdAt`; general search and explicit user sorts unaffected. Day 2 Phase 3.
- All 4 commits unit-tested (151/151 suites, 2406 tests green repo-wide) and live-verified in a browser (entry_source in sessionStorage, clean canonical under a chip filter, chip routing, bestseller-first grid ordering).

### Next
- [ ] **Console listing-fields sync** — the app's runtime only reads Console-hosted `listingFields` (`configHelpers.js` `mergeListingConfig`, `shouldMerge` hardcoded `false`), not local `configListing.js` edits, unless a field is `localOnly`. New `occasion` enum values (`raksha_bandhan`, `diwali`, `navratri`, `karva_chauth`, `bhai_dooj`, `wedding`, etc.) and the new `gift_occasion`/`recipient` fields need adding in Console, or they're silently stripped client-side by `sanitizeMultiEnum` even when the backend already returns them — confirmed live (Raksha Bandhan's OccasionStrip panel had 4 matching API results, rendered 0 cards).
- [ ] `flex-cli search set` for `gift_occasion` and `recipient` still not run in dev or QA/prod (pre-existing gap, restated for visibility now that Day 2 code depends on it).
- [ ] Day 3 (gifting-festival-traffic-prd.md) — social calendar/boards, brand sourcing, ads-readiness gate. Not started.
- [ ] Live-verify `/gifts`/`/occasions/:slug` OG tags via `curl` against true SSR (`yarn dev-server`, port 4000 — the :3000 dev server used for this verification is client-rendered only) and real FB/Pinterest validators once a public URL exists.

## 2026-08-23

### Shipped
- `docs(analytics)` — Found and fixed a real gap while wiring up `add-to-cart-restoration-prd.md`'s GA4 reporting: `saved_listing_toggle`/`saved_page_view`/`saved_recommendation_click` were pushing to `dataLayer` correctly but had zero GTM wiring, so none ever reached GA4 despite prior "live-verified" notes (which only confirmed the dataLayer push). GTM `GTM-5JSJ54C2` published as Version 6 with the missing Data Layer Variables, Custom Event triggers, and GA4 Event tags; also added the missing `saved_surface` param mapping to the existing `brand_clickout` tag.
- Registered 8 new GA4 custom dimensions (Save Toggle Source, Saved Listing ID, Is Saved, Saved Surface, Recs Brand ID, Saved Entry, Recs Shown, Brand Group Count) under `Mela | Brands from India`; deliberately skipped a duplicate "Recs Product ID" dimension since `Product ID` already covers that parameter.
- Discovered `Cross-Shop: Multi-Brand Clickout Rate`, `Cross-Shop: Entry vs Exit`, and `Potential Shoppers Funnel` GA4 Explorations, plus the `Mela Cross-Shop Dashboard` in Looker Studio, already existed and were undocumented — corrected the stale "not started" status in `shopper-visibility-reporting-prd.md` and `PRD_TRACKER.md`. Added `Saved Surface` as a breakdown dimension to the clickout-rate Exploration, and 4 new tiles to the dashboard for the add-to-cart funnel.
- `docs(prd)` — Updated `crossshop-tracking.md`, `crossshop-tracking-prd.md`, `shopper-visibility-reporting-prd.md`, and `PRD_TRACKER.md` to record the gap, the fix, and the corrected status.

### Next
- [ ] **Live-verify the newly-wired GA4 tags end-to-end** — real click → GTM Preview → GA4 DebugView, for all four events (`saved_listing_toggle`, `saved_page_view`, `saved_recommendation_click`, `brand_clickout`'s `saved_surface`). Everything shipped 2026-08-23 is configured and published but unverified against real traffic; all 4 new Looker Studio tiles currently show "No data" as a result.
- [ ] **`saved_recommendation_click` Exploration** — small event-count breakdown by `Product ID` (reuse existing dimension) to answer whether the `/saved` recs rail drives discovery. Not built yet, blocked on real traffic per the item above.

## 2026-08-19

### Shipped
- `docs(prd)` — New `search-ranking-relevance-prd.md` (rev 2, search-engineering panel): native stored **tiered `melaScore`** + `boostTier` to replace age-based default sort; keyword/diaspora vocabulary via `text`-schema fields; pipeline integration + A–E rollout. Added to `PRD_TRACKER.md`.
- `feat(pipeline)` — `searchKeywords` `text` field in `listing-model.js` (joined brand+category+synonyms; arrays can't be ES-indexed as text). `searchKeywords` + `metaDescription` `text` search schemas registered via CLI.
- `feat(classifier)` — Split classify/enrich OpenAI models (`CLASSIFY_MODEL`/`ENRICH_MODEL`, env-overridable). Enrichment now on **`gpt-5.6-luna`** (probe-confirmed working); `LLMClient` adapts GPT-5.x param contract (`max_completion_tokens`, drops non-default `temperature`). Classification stays on `gpt-4o-mini`.
- `feat(classifier)` — Enrichment prompt now requires a real US↔Indian synonym/transliteration pair (kurta/tunic, jhula/swing) in `search_synonyms`.

### Next
- [ ] **Populate + verify `searchKeywords`** — run `create-listings.js --batch` to write the field to live listings, then confirm a diaspora query (`kurta`, `jhula`) returns the expected English-labeled listings. Until this runs, the registered schemas index nothing new.
- [ ] **`melaScore`/`boostTier` scorer (search PRD Phase A)** — catalog-aware pass in `create-listings.js` + `--rescore` mode + backfill-before-flip. Not started.
- [ ] **Enrichment quality check on Luna** — verify `gpt-5.6-luna` output quality vs. `gpt-4o-mini` on a sample (extraction runs at default temperature now, not 0.1 — watch for less-consistent "extract only what's stated" behavior); run `evals/title_eval.py`.
- [ ] **Tariff / landed-cost transparency (from UXR F-013)** — A first-gen diaspora survey respondent found a product she'd realistically buy (House of Chikankari kurti) and the *only* thing stopping her was not knowing whether tariff/duty is included; she's been burned by surprise duties on another site ("the loom site"). This is a conversion blocker, not a discovery one, and maps to Neha's total-cost-clarity trust need. Backlog: show duty/tariff-inclusive (DDP) pricing, or an explicit "tariff included / not included" line at the price + (future) checkout, so there's no surprise at the border.
  - **Vendor to evaluate: Xportel (xportel.com, contact@xportel.com)** — cross-border logistics + customs-clearance for Indian D2C brands (India→US), advertises duty optimization / customs documentation / compliance across Textiles, Handicrafts, Jewelry, Beauty. Not a confirmed shopper-facing landed-cost/DDP product — evaluate whether they (or a brand's own logistics) can enable duty-paid shipping or a reliable landed-cost quote Mela could surface. First-check done 2026-08-19; not yet contacted.
  - **Cross-ref:** ties directly to the still-open 2026-08-06 items below — `OrderPanel`'s `priceConvertedDisclaimer` copy ("US brand price includes shipping & import costs") may overclaim, since neither the ingestion-time nor live-rate FX conversion adds import/duty margin. Resolve the copy-accuracy question and this tariff-transparency question together. Relevant PRD: `trust-conversion-signals-prd.md`.

## 2026-08-14

### Shipped
- `feat(home)` — Hero headline reframed from story-led ("The makers and stories behind India's best brands") to product/brand-led ("Modern brands, rooted in India's rich, regional culture"); subheadline updated to keep a maker/craft mention while leading with shoppability. Decided via `/ux-design panel` + `/uxr personas` review (both consensus, no dissent) rather than the PMF-survey route originally planned. `HeroSection.test.js` updated to match; `web-client` commit `7cc46fdf2`.
- `docs(prd)` — `PRD_TRACKER.md` UXR/Copy Debt row for "Hero headline reframe" marked done, noting the panel/UXR-consensus path taken instead of PMF-survey gating.

### Next
- [ ] None new from this change — the 3 mockup variants in `homepage-redesign.html` (Story-led/Discovery-led/Heritage-led) are now superseded; no action needed unless a future redesign revisits them.

## 2026-08-13

### Shipped
- `feat/fix(add-to-cart-restoration)` — §12+§13 follow-up round (9 scoped fixes, 6 commits): CTA text centering; header "Saved" link + numeric count badge visible for anonymous shoppers too; inline Add-to-Cart confirmation (new `AddToCartConfirmation` component, `aria-live="polite"`, ~4s auto-dismiss, shares `SavedItemsBanner`'s `AUTO_DISMISS_MS`); `SavedPage` content reordered (item-count + grid above `SavedPageSignupPush`) with a combined total-saved/ready-to-shop count; keyboard focus returns to the triggering Shop button when `RedirectTrustSheet` closes (WCAG 2.4.3); `RedirectTrustSheet`'s 1.5s Continue-button delay announced via `aria-live`; fallback affordance for saved cards with no qualifying Shop CTA.
- `fix(saved-listings)` — Two additional blocking bugs found via manual browser QA and fixed in the same round: `/saved` route was `auth: true`, silently bouncing anonymous shoppers to `/login` before any of the above fixes could ever reach them; `SavedPage` only ever fetched/rendered the grid from the authenticated `savedListingIds` list, so anonymous shoppers saw "Nothing saved yet" with real saved items and a correct header badge count. Fixed via new `selectEffectiveSavedListingIds` selector (`savedListings.duck.js`) unifying both auth states as the grid's data source.
- `docs(prd)` — `add-to-cart-restoration-prd.md` §12.4/§13.3 acceptance criteria checked off, status marked ✅ Shipped in `PRD_TRACKER.md`; §13.5 build note documents the two additional bugs and how they were found.
- `feat(saved-page)` — §14 follow-up (marketplace-UX competitor review): restructured `/saved` from a flat `ListingCard` grid into a multi-brand cart. New `SavedBrandGroup` component groups saved items by `publicData.brand` (first-seen order; brand-less items collect into a trailing "More saved" group), each with a real `<h2>` heading in a labelled `<section>`, item count, `formatMoney`-based subtotal (suppressed on mixed/missing currency), and a "Shop {brand} →" group CTA (first in-stock item, routes through the existing `handleShopNow` → `RedirectTrustSheet` → `openBrandStorefront` pipeline, omitted when nothing in the group is shoppable). New `SavedPageRecommendations` component (modeled on `NewFromIndia.js`: `homepageSdk` query, `capPerBrand`, excludes already-saved ids, self-hides when empty) renders as a "Popular on Mela" entry point in the empty state and a "You might also like" rail at the bottom of a populated page.
- `feat(analytics)` — `brand_clickout` gains a `saved_surface` param (`'saved_brand_group' | 'saved_item_card' | null`) disambiguating the two `/saved` CTA surfaces; new `saved_recommendation_click` event on recs-rail clicks; `saved_page_view` gains `recs_shown`/`brand_group_count`, now fired once data has settled (`hasListings || !fetchInProgress`) instead of unconditionally on mount, fixing a flash/possible-never-fires edge case found during implementation (see PRD §14.5 build note). Schema + GA4 custom-dimension setup documented in `crossshop-tracking.md`.
- `docs(prd)` — `add-to-cart-restoration-prd.md` §14.3 and `crossshop-tracking-prd.md` §14.4 acceptance criteria checked off, both marked ✅ Shipped in `PRD_TRACKER.md`; build note added with anon-path live-verification details (real dev Sharetribe data, House of Chikankari + Tarinika); `shopper-visibility-reporting-prd.md` gets a follow-up note flagging the new fields for its Phase 3 GA4 Explorations (not built — manual Console work, out of scope here).

### Next
- [ ] Authenticated-path live verification of §14 was not done this session (logic is shared with the anon path and covered by `isAuthenticated: true` unit tests, but not re-verified live in-browser).
- [ ] `shopper-visibility-reporting-prd.md` Phase 3 GA4 Explorations still need a manual Console update to add `Saved Surface` as a breakdown dimension and a `saved_recommendation_click` exploration — flagged as a follow-up note in that PRD, not built.

---

## 2026-08-12

### Shipped
- `feat(saved-listings)` — `toggleSaveListing` now tags every save/unsave with a `source` (`add_to_cart_button` | `heart_icon`) and fires a new `saved_listing_toggle` analytics event; anonymous `SavedItemsBanner` toast suppressed for Add-to-Cart-sourced saves.
- `feat(pdp)` — Restored "Add to Cart" CTA on all three PDP order-form surfaces (`ProductOrderForm`, `OrderPanel` mobile sticky bar, `InquiryWithoutPaymentForm`) for in-stock brand+productUrl listings, replacing the direct "Shop from {brand}" redirect. New `SavedListingButton` `variant="cta"`. Out-of-stock path unchanged.
- `feat(saved-page)` — Relocated the brand redirect + `RedirectTrustSheet` trust/feedback modal from the PDP to `/saved`, triggered per-item via a new opt-in `onShopNow` prop on `ListingCard`. Added `SavedPageSignupPush` (early-access copy, swappable) and an item-count line.
- `docs(prd)` — Added `add-to-cart-restoration-prd.md`, marked ✅ Shipped in `PRD_TRACKER.md`, cross-referenced in `pre-redirect-sentiment-prd.md` / `saved-items-pasand-prd.md`, and documented `saved_listing_toggle` in `crossshop-tracking.md`.

### Next
- [ ] Live browser QA of the Add-to-Cart/SavedPage flow was not done this session (only unit tests) — founder has follow-up implementation feedback to work through.
- [ ] `SavedPageSignupPush`'s traffic-split mechanism (PRD §8) is still an open PMM question — no A/B framework exists yet, ships as a simple `copyVariant` prop only.
- [ ] Unrelated bug found while testing: two independent Sharetribe SDK client instances (`src/index.js`, `src/util/homepageSdk.js`) defaulted to the same cookie-backed token store, racing on concurrent anonymous-token refreshes and throwing "Unknown token type: undefined" on homepage/`/brands` public queries. Fix drafted (`index.js` now imports the single shared instance from `homepageSdk.js`) but **left uncommitted** — still being verified in-browser, not yet confirmed fully resolved.

---

## 2026-08-08

### Shipped
- `feat(brands)` — Fixed Sharetribe Dev 429 rate limits (support-confirmed: 847 listings.query / 428 users.show over 7 days). Bestsellers now batch-fetch by cached `configBrands.bestsellerProductIds` pools in one chunked `listings.query({ ids })` (brands without a pool fall back to the live `author_id + pub_isBestseller` query — production path preserved); brand profiles share a TTL(15m) promise cache; `mapWithConcurrency` caps the `users.show` fan-out at 5. Wired into `fetchBrands`/`fetchFeaturedBrands`/`fetchHeroBrands`. 20 new tests, full suite (2351) green.

### Next
- [ ] Run `web-client/scripts/harvest-bestseller-ids.js` against the Dev env to populate the `bestsellerProductIds` pools (until then all brands use the throttled `author_id` fallback — correct, just not yet reduced).
- [ ] (Optional, long tail) Apply the same `brandProfileCache` + `mapWithConcurrency` to `CategoryPage.duck.js`'s carousel and the `BrandSpotlight`/`NewFromIndia` local-state re-fetchers.

---

## 2026-08-06

### Shipped
- `feat(pricing)` — `web-client` now computes the displayed USD price from `publicData.priceInINR` (when present) using a live INR→USD rate fetched client-side (`src/util/liveInrRate.js`, Frankfurter API, 12h localStorage cache, static `1/83` fallback on any failure), instead of the frozen rate baked in at CSV ingestion (`product-listing-integration/scripts/lib/utils/price-utils.js`, hardcoded `1 USD = 83 INR`). Wired into `ListingCard`, `ListingCardMini`, and `OrderPanel` (product page) via a shared `useDisplayPrice` hook. Listings sourced already in USD (no `priceInINR`) are unaffected.
- `fix(listing-card-mini)` — `ListingCardMini`'s `showPrice` now defaults to `false` (was `true`); compact brand-grid cards (`BrandCard`, `BrandCardHome` on the homepage) no longer show price chrome at all. Opt in explicitly where price is wanted.

### Next
- [ ] **Important (pre-checkout gap):** the live-rate price above is render-only and was explicitly scoped that way because Mela has no checkout yet — nothing is actually charged against `price.amount` today. Before checkout ships, this needs a real end-to-end fix: either (a) a scheduled job re-prices `price.amount` in Sharetribe from `priceInINR` × live rate on a cadence, so the checkout amount always matches what was displayed, or (b) checkout is built to charge off a freshly-computed INR-based amount rather than the stored `price.amount`. Do not ship checkout against the current frozen `price.amount` while the display price has diverged from it via live-rate computation — that's a real bait-and-switch risk (see 2026-08-06 conversation with founder).
- [ ] Also worth resolving then: `OrderPanel`'s `priceConvertedDisclaimer` copy ("US brand price includes shipping & import costs") implies the USD figure has markup beyond a straight FX conversion, but neither the ingestion-time `1/83` conversion nor the new live-rate conversion add any margin — confirm with whoever owns CSV sourcing whether markup is baked into the source INR number upstream, or fix the copy.

---

## 2026-07-31

### Shipped
- `feat(homepage)` — built the approved homepage-redesign sections into `web-client` (from `mockups/homepage-redesign.html` + founder feedback):
  - **Hero copy** → story-led "Option A": headline "The makers and stories behind India's best brands.", global-shipping subheadline (`SectionMelaHero.heroHeadline`/`heroSubheadline`). Hero trust badges flipped US→global ("Ships Worldwide" / "Secure Checkout"). CTA unchanged ("Explore Brands"); **no "Shop Gifts" CTA** yet (see Next).
  - **CategoryTiles** (`src/components/CategoryTiles/`) — new reusable compact 6-tile category grid reusing `CategoryIcon` SVG glyphs; replaces the Fashion/Baby product carousels on the homepage (`CategoryShowcase` render swapped in `MelaHomePage.js`).
  - **OccasionCard** (`src/components/OccasionCard/`) — extracted the colored occasion panel (festive/gifting themes) into a reusable component; `OccasionStrip` now renders it.
  - **BrandPhotoCard** (`src/components/BrandPhotoCard/`) + **EarnedItsPlace** section (`sections/EarnedItsPlace/`) — "Every Brand Here Earned Its Place" now SHOWN: big primary photo + thumbnail filmstrip (hover desktop / tap mobile swap, no swipe), why-line derived from `brandCraft`/`brandTagline`/bio. Reuses the FeaturedBrandPartners data path (`getFeaturedBrandsWithProducts`); replaces the "Trusted by Parents" grid on the homepage.
  - **TrustAssurance** retitled "Every Brand Here Earned Its Place" → **"Shop with Confidence"** (certs + FAQ kept). Avoids duplicate titles.
  - Tests: 4 new suites + updated HeroSection/CategoryShowcase/MelaHomePage tests. 115 passing across the homepage tree.

### Next
- [ ] **P1** — Bring back a **"Shop Gifts"** primary CTA in the hero (and the deferred Gifts nav entry) once a real **Gifting landing page** exists. Deferred per founder (2026-07-31): no Shop-Gifts CTA until the destination is good. Ties to the dedicated Gifting page item in `PRD_TRACKER.md` "UXR / Copy Debt".
- [ ] **Featured Edit / "The naming-ceremony edit"** — deferred (2026-07-31). Build later as a **rotating, multi-occasion** editorial edit (not just naming ceremony), once the occasion/gift-suitability enrichment (below + `prompt_engine.py` TODO) gives products the tags to populate it. Demonstrated in `mockups/homepage-redesign.html`.
- [ ] **Positioning consistency (flag):** the hero now says "shipped worldwide" but `VettingStrip` ("Ship to all 50 states"), the `TrustAssurance` FAQ, and the `MelaHomePage` meta description remain US-specific (US cards, $800 de minimis). Decide whether to globalize the rest or keep US-diaspora framing everywhere except the hero.

---

## 2026-07-30

### Next
- [ ] **P1** — Add "Gifts" to the top nav + mobile hamburger, pointing to the Gifting-occasion filtered search (`?pub_occasion=has_any:gifting`) as an **interim** destination. A dedicated Gifting page is a separate, larger item (see PRD_TRACKER "UXR / Copy Debt"). Surfaced by the homepage-redesign mockup feedback pass (`mockups/homepage-redesign.html`).
- [ ] Design specs (not engineering-ready yet, tracked in `PRD_TRACKER.md` "UXR / Copy Debt"): BrandCardHome redesign (big photo + hover/tap thumbnails), homepage certification education surface, occasion merchandising (inspiration + product-peek hybrid), and the 3 culture/story/heritage hero-copy variants. All demonstrated in `mockups/homepage-redesign.html` (Redesign view).
- [ ] Pipeline (`prompt_engine.py`): occasion enrichment expansion + a separate gift-suitability aspect — a `# TODO` block is now in `create_enrichment_prompt`; gated on richer product understanding, cross-linked to `enrichment-pipeline-stage2-update-prd.md`.

---

## 2026-07-29

### Shipped
- `fix(seo)` — **P0**: category-mismatched product metadata, confirmed via external AEO/Gemini audit (`mela-docs/engineering/done/seo-optimization-summary.md` → Phase 2). `ListingPageCoverPhoto.js` and `ListingPageCarousel.js` hardcoded `"Authentic Indian Baby Products"` into every listing's title tag, meta description, and JSON-LD seller/audience fields — regardless of the listing's actual category. A House of Chikankari kaftan or a Kaunteya mug shipped with baby-product metadata, which reads as miscategorized/low-quality data to semantic-search crawlers (Gemini) and undercuts Mela's multi-category positioning. Fixed by deriving `categoryDisplayName` from `config.categoryConfiguration.categories` via the existing `findCategoryById` helper already used for category chips in both files — no new data model, just wiring in what already existed. Also generalized the JSON-LD `audience` block (`audienceType: 'Parents'` → `'Shoppers'`) since it was baby-specific across all categories. 50/50 ListingPage test suites still passing (no test had covered the old string — that's how it shipped unnoticed).
- Confirmed, not fixed: `SearchPage.shared.js`'s `isCategoryPage`/`isBrandPage` branches in `createSearchResultSchema` (lines ~534-571) contain the same hardcoded "Baby Products"/"Baby Brand" strings, but tracing `routeConfiguration.js` shows `/categories/*` routes to `CategoryPage` and `/brands/:brandSlug` routes to `ProfilePage` — SearchPage is never reached at those paths anymore. This is dead code left over from before the dedicated components shipped, not a live bug. Left untouched (removal is a separate cleanup decision); noted below.

### Next
- [ ] **Critical** — Google Merchant Center product feed: no Content API / Shopping feed integration exists at all (confirmed — only a stray JSON-LD comment referencing "Google Shopping" on the price field). Net-new engineering scope: map existing `publicData` fields (`brand`, `material`, `itemAspects`, `sku`) into a Merchant Center feed with explicit `"Ships to US"` shipping attributes. Worth its own PRD rather than a quick add. See `seo-optimization-summary.md` Phase 2 §2.
- [ ] **Critical** — `aggregateRating`/`review` is completely absent from the Product JSON-LD (`ListingPageCoverPhoto.js` schema object has no rating/review keys). Already flagged as P2 in `seo-aeo-category-brand-pages-prd.md` §5B, but blocked on a real precondition: Mela has no review/rating data model yet. Needs a product decision — build reviews before AEO can use them, or defer AEO rating schema indefinitely.
- [ ] Housekeeping (not urgent): remove the dead `isCategoryPage`/`isBrandPage` branches in `SearchPage.shared.js` `createSearchResultSchema` (~lines 534-571) — unreachable now that `CategoryPage`/`ProfilePage` own those routes, but left in place and could confuse a future editor into "fixing" schema that never runs.
- [ ] Digital PR (co-mentions) and the informational content hub are tracked as content workstreams, not engineering, in `mela-docs/social/aeo-next-steps.md`.

---

## 2026-07-26

### Shipped
- `fix(brand-hero-card)` — hero carousel was silently broken (P0): a dropped `included` image entity in `fetchHeroBrands` left a dangling relationship, `getHeroBrands` threw on every render, and with no error boundary around `HeroSection`, React silently stopped re-rendering it — loading skeleton frozen forever, no console error, store updating fine underneath. Fixed by capturing `included` per-brand, matching `fetchBrands`/`fetchFeaturedBrands`.
- `fix(brand-hero-card)` — hero eligibility no longer requires products (the card renders none) and now covers all curated brands, not just the first 10; new `fetchHeroBrands`/`getHeroBrands` kept separate from `fetchFeaturedBrands` (`FeaturedBrandPartners` unaffected)
- `fix(brand-hero-card)` — focus ring now uses `--colorAccent` (real marigold token); `--marketplaceColorLight` was already a different color elsewhere, silently defeating the intended fallback
- Verified live against dev Sharetribe across multiple hard reloads, not just unit tests. Full suite: 134/134 test suites passing
- `feat(brand-storefront)` — P1.1 brand page hero band (`storefront-validation-readiness-prd.md`): banner image with gradient fallback, "Vetted by Mela" pill gated on `publicData.melaVetted`, inline story summary + craft chip, outbound "Visit Store" CTA wired through the existing `RedirectTrustSheet`/`openBrandStorefront` flow. Also excludes $0 promo SKUs and sorts bestsellers first in the brand-page grid; "About" tab renamed "About & Story". All new fields degrade gracefully for the 14 brands without seeded hero data — verified live on `/brands/fizzy-goblet` (sparse real data) plus 26 passing tests.
- `fix(trust-debris)` + `feat(homepage)` + `feat(category-page)` — remaining P0/P1.2/P1.3 of `storefront-validation-readiness-prd.md` (8 commits): positioning copy applied everywhere per `positioning-copy.md`; P0.2 debris sweep ($0 SKUs, certifications role-gating, search placeholder — footer copyright/listing-link left alone, that's Sharetribe Console content, not fixable from web-client); P0.1 vetting strip (live-verified, both analytics events fire); P1.2 category-page brand-diversity cap + price-heuristic demotion + interleaved brand tiles (`categoryMerchandising.js`, `CategoryPage.duck.js` extension); P1.3 three new homepage editorial modules (Brand Spotlight, New from India, Craft Stories) + full section reorder, all live-verified against seeded dev data. Caught and fixed a real bug: `NamedLink` silently drops `onClick`, so two modules' click analytics needed a `display:contents` wrapper fix. Full suite: 140/140 test suites, 2264 tests passing.
- Fixed same session: `BrandStorefront.js`'s story-summary derivation was looking for a `publicData.brandStory` field the seeder never populates (it concatenates story into the native `bio` field instead) — summary now derives from `bio` minus the tagline sentence, live-verified showing real content for Fizzy Goblet/Kaunteya.

### Next
- (still open) The Nesavu and Masilo have no hero image source — re-check the curated first-fold order once they get `brandHeroImageIds`/`brandHeroImages`
- [ ] Brand-storefront hero band was only visually verified at desktop viewport this session — a browser-automation tool limitation prevented forcing a true 390px mobile viewport (`resize_window` didn't change `window.innerWidth`). Mobile-first CSS was hand-reviewed against the mockup but not screenshot-verified; do a real on-device or working resize-tool pass before calling P1.1's mobile AC done.
- [ ] P1.1a's "outbound store link above the grid" AC is superseded — hero-band CTA relocated to a plain "Brand website" link in the About & Story tab per the inline 2026-07-26 decision (no-affiliate-tracking rationale: an above-the-fold exit door with no tracking is a pure loss). PRD §6 AC text has been updated to match (see the REWORK note under P1), but flagging here too since it reverses what P1.1a's mockups show.
- [ ] Homepage length reduction measured at 15.4% (8,526px vs. 10,073px baseline), short of the PRD's ≥25% target — the 3 new P1.3 modules are heavier than the spec's projection assumed. Options: trim module density further, or accept 15.4% + the much-earlier vetting-strip placement as sufficient and revisit the number later.
- [ ] `/categories/Fashion`'s first page is 100% one brand (House of Chikankari) — P1.2's diversity-cap code is correct and tested, but has nothing to diversify against on this specific page. Supply-side gap (more Fashion brands with inventory), not a UI fix — matches the PRD's own §8 risk note.
- [ ] No AC above has been verified at a true 390px mobile viewport — same browser-automation tooling limitation as the P1.1 pass (`resize_window` doesn't change `window.innerWidth` in this session's environment).

---

## 2026-07-25

### Shipped
- `feat(hero-section)` — BrandHeroCard ships (`brand-hero-card-webclient-prd.md`, ✅ Shipped): image-forward hero card (1:1 photo, bottom gradient scrim, white name/tagline) replaces `BrandCardHome` in the homepage hero only; `BrandCardHome` itself untouched. Resolves `brandHeroImageIds[i]` → Sharetribe variant URL, falls back to `brandHeroImages[i]` (Shopify); brands with no hero source are filtered out (no dead dots). Mobile carousel is now a scroll-snap track (88% width + peek) instead of a single-slide swap.
- Caught and fixed a WCAG AA gap during dev-lead review: scrim/text only held 4.5:1 for the average case — a 2-line-wrapped name/tagline over a near-white photo measured 4.22–4.28:1. Widened the scrim and switched overlay text to solid white (verified 4.97:1 at the worst-case point).
- Fixed a test-pollution bug in `BrandHeroCard.test.js`: a failed assertion skipped `jest.spyOn` cleanup, corrupting later tests — root cause was a fresh `configureStore()` per `rerender()` instead of RTL's `wrapper` option.

### Next
- [ ] The Nesavu and Masilo have no hero image source (brand-wide watermark; no CSV yet, respectively) and are absent from the hero carousel — re-check the curated first-fold order (`configBrands.js`) once they get `brandHeroImageIds`/`brandHeroImages`
- [ ] Full `npm test` run flagged one pre-existing, unrelated failure (`LandingPage.test.js` error-fallback test) — not touched by this work, left as-is

---

## 2026-07-19

### Shipped
- `verify(analytics)` — Cross-shop tracking (`crossshop-tracking-prd.md`) **fully live-verified end-to-end** on shopatmela.com, status now ✅ Shipped: GTM container (`GTM-5JSJ54C2`) published, GA4 (`G-1H78QV7C6G`) receiving data (confirmed in Realtime), Microsoft Clarity (`xoozbmshor`) recording sessions, four GA4 custom dimensions registered. `entry_source` capture confirmed live (first-touch set correctly from UTM params, persisted unchanged across navigation, present on the fired event). `brand_clickout` confirmed firing with all six params on both CTA surfaces reachable in the current catalog (`OrderPanel.js` main CTA, `ProductOrderForm.js` quantity/delivery form CTA — tested at mobile viewport). `InquiryWithoutPaymentForm.js` (inquiry-only CTA) is implemented via the same shared path but has no live listing to test against today — not a gap, just no qualifying data yet.
- Root-caused a red herring along the way: GTM Preview's repeated "no debuggable Google tag" / connection-timeout errors were caused by browser-side tracker-blocking (DuckDuckGo extension in Chrome, native Enhanced Tracking Protection in Firefox) interfering with Google's `/debug/bootstrap` handshake — not a code, CSP, or container problem. Testing in a clean/private browser profile resolved it.
- Noted, unrelated to this work: a 404 seen while testing the mobile CTA traced to an out-of-stock/inventory issue on that specific listing, not a routing or tracking bug — no action needed here.

### Next
- [ ] Confirm the `brand_id` proposal (listing author/brand-user UUID, not a real schema field today) — see PRD §5b
- [ ] If/when an inquiry-type listing goes live, verify `brand_clickout` fires from `InquiryWithoutPaymentForm.js` too
- [ ] Once 30 days of real data exist, build the two Explore reports (multi-brand-clickout rate, entry≠exit) per `crossshop-tracking.md` §5 and set real targets (currently baseline-only)

---

## 2026-07-18

### Shipped
- `feat(analytics)` — Cross-shop / entry-exit attribution tracking (`crossshop-tracking-prd.md`): GTM + GA4 (via GTM) + Microsoft Clarity install (env-var gated), `entrySource.js` (first-touch UTM/referrer capture, session-persisted), `brandClickout.js` (`brand_clickout` dataLayer event + `openBrandStorefront()`), wired into all three Shop-from-Brand CTA surfaces (`OrderPanel`, `ProductOrderForm`, `InquiryWithoutPaymentForm`) via a single `onShopNow` path — also closes a pre-existing gap where two of those surfaces bypassed `RedirectTrustSheet`. Spec at `mela-docs/technical/analytics/crossshop-tracking.md`.

---

## 2026-07-16

### Next
- [ ] Instrument `/brands` brand-order reorder: track rank-position CTR (click rate by card position) + category-section CTR per brand once the anchor+rotation ordering ships, so the curated order can actually be checked against the random-shuffle baseline it replaces instead of being another unmeasured heuristic swap (from `/brands` brand-order UX panel critique, 2026-07-16; builds on `homepage-hero-prd.md` §12A/§12A.1)
- [ ] Decide and document the `/brands` anchor-tier visibility tradeoff: curation is currently planned to stay invisible to users (no "Featured"/"Most Authentic" badge, to avoid an authenticity-hierarchy read) — write down that reasoning explicitly as a considered tradeoff against opaque-algorithmic-ranking disclosure norms, rather than leaving it as an undocumented default (from `/brands` brand-order UX panel critique, 2026-07-16)

---

## 2026-07-12

### Shipped
- `feat(homepage-hero)` — Cold-load value-prop hero (homepage-hero-prd Tier 0/1 + refinements): standalone why-line carrying the model-set message, demoted+labeled category pills with new `CategoryIcon` glyphs (replacing emoji), warm cream surface tokens across hero/brands/trust, curated carousel order (`getCuratedBrandIds`) with price/heart chrome hidden + "Handcrafted in … India" cue, threshold-gated breadth signal, carousel pause/play + reduced-motion, ComingSoonSection removed
- `chore(deps)` — Pinned `shimmer` (runtime dep of Sentry/OpenTelemetry instrumentation that yarn wasn't hoisting; server threw "Cannot find module 'shimmer'")

### Next
- [ ] Supply: ingest Suta, Isharya, Kaunteya, House of Chikankari (top of the 2026-07-12 onboarding priority, §12A) and publish Fizzy Goblet listings in QA so the curated hero carousel actually leads with them
- [ ] Update `getCuratedBrandIds` (`configBrands.js`) to follow the full §12A onboarding order as those brands land

---

## 2026-06-21

### Shipped
- `refactor(identity)` — Removed all marketplace-giveaway UX & URL patterns: "Sharetribe" brand name, "Join our marketplace" copy, provider signup CTAs (replaced with mailto:shopatmela@gmail.com), "About the listing author" → "About the Brand"; `/u/:brand-uuid` now redirects to `/brands/:slug`; listing canonical `/l/:id` redirects to `/l/:slug/:id`; Avatar, BrandStorefront tabs, ProfileSettingsPage all use BrandPage route; added `BrandPageVariant` route
- `chore(config)` — Added The Nesavu brand (UUID 697b81ea) to configBrands.js to match .env.dev; fixed `Vilvah-store` → `vilvah-store` slug casing
- `feat(config)` — `isBestseller` listing field (boolean, `localOnly: true`) + `SCHEMA_TYPE_BOOLEAN` case in FilterComponent; `configHelpers.js` always merges `localOnly` fields regardless of Console config
- `fix(listings)` — `create-listings.js` now detects listings with stale CSV image IDs (live Sharetribe listing has zero images) via the existing bulk listings fetch and re-uploads from source URLs instead of silently reusing dead IDs; added `staleImagesFixed`/`staleImagesUnfixable` stats + per-listing-ID logging so runs are auditable
- `feat(scripts)` — `seed-brand-profiles.js` pushes curated `brandTagline`/`brandStory` from `brand_content.json` to matching brand users via the Sharetribe Integration API
- `feat(scraper)` — Added 3 new Shopify brands to scrape list (Daughters of India, Gauri and Nainika, Comet); refreshed Pluchi, Gado Living, My First Crayons product CSVs

### Next
- [ ] Build `bestseller-tagger.js` script in product-listing-integration — sets `publicData.isBestseller = true` on top 20% by orders per L1 category (PRD: trust-conversion §3.2)
- [ ] "Ships to US · US cards · Sold by [Brand]" static line on ListingPage near OrderPanel CTA (~30 min, PRD: trust-conversion §3.3a)
- [ ] Add production brand UUIDs to `configBrands.js` (currently empty — all URL redirects fall back to `/u/:id` in prod)
- [ ] Organization JSON-LD, BreadcrumbList JSON-LD, ItemList JSON-LD on `/brands/:brandSlug` (PRD: seo-aeo brand storefront ACs)
- [ ] `sitemap-brands.xml` — all brand slugs indexed
- [ ] 404 for unknown `brandSlug` (currently renders empty page)

### Blockers
- Production brand UUIDs not yet in configBrands.js — `/u/:id` → `/brands/:slug` redirect is dev-only until populated
