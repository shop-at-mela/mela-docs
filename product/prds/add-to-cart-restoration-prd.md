# Add to Cart Restoration + SavedPage Shop CTA PRD

**Status:** ✅ Shipped (2026-08-13) — §12+§13's nine follow-up fixes are code-complete, tested, and browser-verified (see §13.5 build note for two additional bugs found and fixed during that verification). `SavedPageSignupPush`'s traffic-split mechanism (§8) remains a separate open PMM follow-up.

## Executive Summary
**Feature**: Restore an "Add to Cart" CTA on the product page (PDP), replacing the current "Shop from {brand}" direct-redirect button for in-stock brand listings. Adding an item no longer sends the shopper to Shopify immediately — it saves the listing (reusing the existing Saved/wishlist mechanism) and the actual brand redirect + trust/feedback modal move to `/saved`, where each saved item gets its own "Shop on {brand} →" CTA. `/saved` also gets a new early-access sign-up push.
**Target URL / Entry Points**: Product page (`/l/:slug/:id`) — `ProductOrderForm`, `OrderPanel` mobile sticky bar, `InquiryWithoutPaymentForm`. Destination: `/saved` (`SavedPage`).
**Target Users**: All four personas — this is a PDP-and-cart-flow structural change, not persona-specific. Most directly responsive to Vidhi (F-004, feedback-log.md): "the product page feels too incomplete to test as-is" without a cart step.
**Business Objective**: Make the PDP→purchase flow feel complete (address F-004) while preserving the pre-redirect trust/feedback modal that `pre-redirect-sentiment-prd.md` shipped, and use the relocation as a new sign-up surface with "coming soon" framing — without making an unfulfillable checkout promise.
**Primary Success Metrics**:
- Add-to-Cart click-through rate on brand+productUrl in-stock listings (new `saved_listing_toggle` event, `source: 'add_to_cart_button'`)
- SavedPage → "Shop on {brand}" click-through rate (existing `brand_clickout`, now sourced from `/saved` in addition to the PDP out-of-stock path)
- Anonymous sign-up conversion from the new `SavedPageSignupPush` (early-access copy variant vs. control)

---

## 1. Problem Statement

### Current State
The PDP shows "Shop from {brand}" (in stock) / "View on {brand}" (out of stock) instead of Add to Cart / Buy Now whenever a listing has `publicData.brand` + `publicData.productUrl` — i.e. on essentially every affiliate listing. Clicking it opens `RedirectTrustSheet` (trust copy + thumbs-up/down feedback, shipped under `pre-redirect-sentiment-prd.md`) once per session, then redirects straight to the brand's Shopify page via `openBrandStorefront()`. There is no intermediate step — no cart, no "ready to shop" review — between "I'm interested" and "I've left Mela."

### User Pain Points
- **F-004 (Vidhi, feedback-log.md, 2026-08-11)**: "Test adding 'add to cart' on the product page and route users to checkout from the cart instead of the product page — the product page feels too incomplete to test as-is." Logged as `Watching`, not yet actioned.
- More broadly: shoppers comparing multiple items across brands have no way to "stage" purchase intent before committing to leave Mela — every click is a one-way door.

### Business Impact of Inaction
- The PDP reads as unfinished to shoppers used to a cart step, which undermines the moderated-test usefulness of the page (F-004's own framing) and, per the marketing/GTM review below, forgoes a credible way to signal "Mela is building toward a real marketplace" without over-promising.
- No natural moment exists today to ask an anonymous shopper to sign up beyond the generic wishlist nudge.

---

## 2. Goals & Non-Goals

### Goals
- Restore "Add to Cart" as the primary PDP CTA for in-stock brand+productUrl listings.
- Move the brand redirect + `RedirectTrustSheet` trust/feedback modal from the PDP to `/saved`, triggered per-item.
- Add a per-item "Shop on {brand} →" CTA to `SavedPage`'s listing cards (doesn't exist today).
- Add an early-access-framed sign-up push to `SavedPage`, as a swappable copy variant (not a hardcoded final choice — no A/B framework exists yet, see §8).
- Tag save-toggle analytics events with a `source` (`add_to_cart_button` vs. `heart_icon`) so purchase-intent and wishlist signal can be separated later.
- Suppress the existing anonymous `SavedItemsBanner` toast specifically for Add-to-Cart-sourced saves, so an anon shopper isn't nudged to sign up twice in one flow.

### Non-Goals
- **No real shopping cart.** Sharetribe has no built-in cart (confirmed against Sharetribe's own dev-blog series — building one requires a new `CartPage.duck.js`, a custom stock-reservation transaction process, checkout/transaction-page rework, none of which exists in this codebase or is in scope here). "Add to Cart" writes to the existing saved-listings list; it does not create a second, parallel cart data structure.
- **No rename of `/saved` to "Cart."** Route, component, duck, and translation-key names all stay "Saved" — see §3 for why.
- **No real A/B testing framework.** The sign-up copy variant switch (§8) is a simple prop/constant, not a new experimentation system.
- Out-of-stock brand listings' PDP behavior is unchanged (still direct "View on {brand}" redirect + trust sheet, same as today).
- Legacy non-brand "Buy now" listings (real Sharetribe checkout, no `productUrl`) are untouched.

---

## 3. Naming Decision — Why `/saved` Is Not Renamed "Cart"

This was resolved via a 5-expert first-principles panel (marketplace PM, design-systems engineer, diaspora-studies researcher, accessibility/ethics consultant, information architect) plus a separate marketing-lead/GTM/PMM review, both run against this specific question.

**Panel synthesis:**
1. F-004 is a single `Watching`-status data point from one moderated session — not a rename mandate. The reuse decision (Add to Cart writes to the same list as the heart icon) means every heart-tap and Add-to-Cart-tap write identically; tag `source` at write time (§7) so the signal can be split later even though the list stays unified.
2. "Cart" is the single most generic, Amazon-coded e-commerce term available — reaching for it to fix "feels incomplete" risks reinforcing the *exact* root-cause diagnosis already logged in `feedback-log.md`'s own synthesis ("Mela presents as a generic product catalog... no reason to understand what makes Mela different from a standard marketplace," F-001–F-003). `buyer-personas.md` (lines 515, 530) frames Mela as "a curated discovery experience that happens to have checkout" with "checkout as the conclusion of an inspirational journey, not the purpose of a search session" — checkout language belongs at the end of a curated journey, not as a bolt-on generic cart icon.
3. Every path off `/saved` still ends in a redirect to the brand's own Shopify checkout, never a Mela-processed order. `RedirectTrustSheet`'s existing disclosure copy is what keeps "Add to Cart" honest given that constraint — it must survive the relocation unmodified (§6).
4. If "Cart" ever becomes the real, durable identity, the underlying primitives (`SavedPage.js`, `savedListings.duck.js`, `SavedListingButton`, all `SavedPage.*`/`SavedListingButton.*` translation keys) need to be renamed too, or the codebase accrues a permanent "UI says Cart, code says Saved" translation tax for every future engineer.

**Marketing-lead/GTM/PMM review, given the explicit rationale for renaming ("sell that full-stack marketplace is coming soon, Mela is not just a forever affiliate site"):**
- A silent page rename isn't a GTM move — it implies a capability (real checkout) with no owned narrative behind it (no waitlist, no roadmap post, no comms plan). If a shopper or partner asks "wait, is checkout real?", there's nothing to point them to.
- The audiences who'd actually register "is this just affiliate?" (investors, press, brand partners) aren't reached by a wishlist-page label — that's a narrative told through founder updates and partner conversations, not UI copy.
- "Cart" spends brand-vocabulary distinctiveness (working against the "living culture, not heritage" copy direction) to buy a feeling of completeness that a more distinctive label (e.g. "Your Shortlist") could deliver without importing generic-cart baggage.
- **The real GTM lever is the sign-up offer, not the page name.** Put the "coming soon" signal into the sign-up CTA's copy (early-access framing), which converts on its own merits and earns the "we're building toward marketplace" signal honestly — see §7.

**Decision**: `/saved` keeps its identity everywhere in code and copy. Cart-flavored language is allowed narrowly in item-count copy ("3 items ready to shop"). The "coming soon" narrative lives entirely in the sign-up push's copy, shipped as a testable variant, not asserted via a page rename.

---

## 4. User Stories

| As a... | I want to... | So that... | Priority |
|---------|-------------|------------|----------|
| Shopper browsing a brand listing | Click "Add to Cart" without immediately leaving Mela | I can keep browsing and decide when to actually go to the brand's site | P0 |
| Shopper with items added | See a per-item "Shop on {brand}" CTA on `/saved` | I control exactly when I leave Mela for each item | P0 |
| Shopper clicking Shop on {brand} for the first time this session | See the same trust/context modal as before | I still get the same reassurance and can give feedback | P0 |
| Anonymous shopper who adds an item to cart | Not be nudged to sign up twice (toast + page push) in one flow | The experience doesn't feel naggy | P0 |
| Anonymous shopper on `/saved` | See a sign-up prompt framed around what's coming, not just "create an account" | I understand there's more value in creating an account | P1 |
| PM / analytics | Distinguish Add-to-Cart saves from heart-icon saves in the data | I can tell purchase-intent signal from casual wishlist signal | P1 |

---

## 5. Feature Requirements

### Must Have (P0)
- PDP: in-stock brand+productUrl listings show "Add to Cart" (writes to `savedListings.duck.js`, `source: 'add_to_cart_button'`); no redirect, no trust sheet fires from this action.
- PDP: out-of-stock brand+productUrl listings unchanged — "View on {brand}", direct redirect + trust sheet, same as today.
- PDP: inquiry-type brand+productUrl listings also switch to Add to Cart (consistency; no separate cart-completion step exists for inquiries, but the CTA language should still match).
- All three PDP CTA call sites (`ProductOrderForm.js`, `OrderPanel.js` mobile sticky bar, `InquiryWithoutPaymentForm.js`) change together — they currently duplicate the same conditional and must not drift into an inconsistent desktop-vs-mobile state.
- `SavedPage`: each saved item with `brand` + `productUrl` gets a "Shop on {brand} →" / "View on {brand} →" CTA (stock-aware).
- `SavedPage`: clicking Shop routes through the same `handleShopNow` → `RedirectTrustSheet` (first click of session) → `openBrandStorefront` pipeline as the PDP does today — same trust copy, same thumbs feedback, same 1.5s continue-delay, same session-level dedupe (global, not per-brand).
- Anonymous `SavedItemsBanner` toast is suppressed for `source: 'add_to_cart_button'` saves; still fires normally for heart-icon saves.
- `savedListings.duck.js`'s `toggleSaveListing` tags every write with `source` (default `'heart_icon'`) and fires a new `saved_listing_toggle` analytics event (§7).

### Should Have (P1)
- `SavedPage` sign-up push (`SavedPageSignupPush`) with early-access framing, gated on `!isAuthenticated`, built as a `copyVariant` prop (`'earlyAccess' | 'control'`) so it's swappable without a code change once PMM decides how to test it.
- Item-count copy on `SavedPage` ("3 items ready to shop") for items with `brand` + `productUrl`.
- Cap-reached UX polish: Add-to-Cart button renders `disabled` with a tooltip at the existing 200-item saved cap, instead of silently no-op'ing on click.

### Nice to Have (P2)
- Real traffic-split mechanism for the sign-up copy variant (URL param, GA4-side experiment, etc.) — deferred, see §8.

---

## 6. UX Requirements

- **PDP Add to Cart button**: visually identical to the button it replaces (same `PrimaryButton` styling) — implemented as a new `cta` variant on the existing `SavedListingButton` component so it inherits `isSaved`/`inProgress`/cap-reached state for free, rather than a new hand-rolled button.
- **Trust/feedback modal (`RedirectTrustSheet`)**: unmodified content and behavior, relocated to fire from `SavedPage` instead of the PDP for the in-stock path. Disclosure copy about redirecting to the brand's own checkout must not be watered down — this is what keeps "Add to Cart" honest given Mela never processes payment itself.
- **`SavedPage` per-item CTA**: needs `e.preventDefault()`/`stopPropagation()` since it sits inside `ListingCard`'s `NamedLink` wrapper (same pattern already used by `SavedListingButton`'s heart icon). Mobile: 44px+ tap target in the existing 2-column grid; handle brand-name truncation.
- **Sign-up push**: static inline block on `SavedPage` (not a floating auto-dismissing toast like `SavedItemsBanner` — different component, see §9), visible whenever `!isAuthenticated && anonSavedItems.length > 0`.

### Edge Cases
| Scenario | Behavior |
|---|---|
| Anonymous user clicks Add to Cart | Existing anon/localStorage save path handles the write; the global toast is suppressed for this source; the inline SavedPage push still shows |
| Items saved before this ships | No migration needed — `savedListingIds`/`anonSavedItems` carry no per-item source field; `source` only affects the analytics event at toggle time |
| 200-item saved cap reached | Add-to-Cart button renders disabled + tooltip (not silent no-op) |
| Listing has no `brand`/`productUrl` | PDP fully untouched (legacy Buy Now path); `SavedPage` card simply doesn't render a Shop CTA for it |
| Multiple different brands saved in one session | Trust sheet dedupe stays session-global — shows once total, not once per brand |

---

## 7. Analytics Requirements

See `mela-docs/technical/analytics/crossshop-tracking.md` for the full event schema (updated alongside this PRD).

- **New event**: `saved_listing_toggle` — `{ event: 'saved_listing_toggle', source: 'add_to_cart_button' | 'heart_icon', listing_id, is_saved }`, fired from `toggleSaveListing` in `savedListings.duck.js`, covering both the anonymous (localStorage) and authenticated (Sharetribe `privateData`) write paths identically.
- **Existing event, new trigger surface**: `brand_clickout` (schema unchanged, see crossshop-tracking.md §3) now also fires from `SavedPage`'s per-item Shop CTA, in addition to its existing surfaces (PDP out-of-stock path, brand-page "Brand website" link). The in-stock PDP surfaces (`ProductOrderForm.js`, `OrderPanel.js`, `InquiryWithoutPaymentForm.js`) stop firing `brand_clickout` directly for in-stock listings — they now fire `saved_listing_toggle` instead, and `brand_clickout` fires later, from `/saved`, if and when the shopper clicks through.
- `pushSaveToggle()` helper: new file `src/util/analytics/savedListings.js`, following the existing minimal `window.dataLayer.push(...)` pattern (no shared event bus) already used by `brandClickout.js` / `vettingStrip.js`.

---

## 8. Sign-Up Push — Copy Variant (Open Follow-Up for PMM)

`SavedPageSignupPush` ships with a `copyVariant` prop defaulting to `'earlyAccess'` (e.g. "Save your list — be first in when we open direct checkout" / "Get early access"), with a `'control'` variant (plain "create an account" framing) available via the same prop. **No A/B/experimentation framework exists in this repo** (confirmed via grep — no LaunchDarkly/Split/Optimizely). This PRD ships the mechanism as a simple exported constant, not a new system.

**Open question for PMM**: how should the actual traffic split be executed — a manual per-deploy toggle, a URL param, or a GA4-side experiment? Do not over-build this until answered.

---

## 9. Acceptance Criteria

> Checked items are implemented in code and covered by unit tests (`OrderPanel.test.js`, full suite green). Browser/manual QA is still in progress — see build note below.

- [x] In-stock brand+productUrl PDP listings show "Add to Cart," not "Shop from {brand}"
- [x] Clicking Add to Cart does not open `RedirectTrustSheet` and does not open a new tab
- [x] Clicking Add to Cart fires `saved_listing_toggle` with `source: 'add_to_cart_button'`
- [x] Out-of-stock brand+productUrl PDP listings are unchanged (still "View on {brand}," direct redirect + trust sheet)
- [x] All three PDP CTA surfaces (`ProductOrderForm`, `OrderPanel` mobile bar, `InquiryWithoutPaymentForm`) reflect the change consistently
- [x] `/saved` shows a "Shop on {brand} →" CTA on each saved item with `brand` + `productUrl` (stock-aware copy)
- [x] Clicking that CTA opens `RedirectTrustSheet` on the first click of the session (any item, any brand) and redirects directly on subsequent clicks
- [x] `RedirectTrustSheet`'s trust/disclosure copy is unmodified from its current PDP version
- [x] `brand_clickout` fires (unchanged schema) when the shopper actually continues from `/saved`
- [x] Heart-icon saves still fire `saved_listing_toggle` with `source: 'heart_icon'` and still trigger the anonymous `SavedItemsBanner` toast
- [x] Add-to-Cart saves (anon) do NOT trigger the `SavedItemsBanner` toast
- [x] `/saved` route, component, and translation identity remain "Saved" — no "Cart" naming introduced in code, URL, or page heading
- [x] `SavedPageSignupPush` renders only for `!isAuthenticated` users with ≥1 anon-saved item, using the `earlyAccess` copy by default
- [x] 200-item saved cap: Add-to-Cart button renders disabled + tooltip, not a silent no-op

> **Build note (2026-08-12):** Implementation shipped across three commits in `web-client` (`339d022b3`, `f9d502237`, `332def44f`). Founder has follow-up feedback on the implementation to work through in a follow-up session — treat this AC list as "code-complete," not "final."

---

## 10. Dependencies & Risks

**Dependencies**
- Reuses `savedListings.duck.js`, `SavedListingButton`, `ListingCard`, `RedirectTrustSheet`, `openBrandStorefront`/`pushBrandClickout` — no new Redux subsystem.
- `fetchSavedListings`'s SDK query needs `currentStock` added to its `include` array so `SavedPage`'s CTA can be stock-aware (currently only fetches `images`, `author`).

**Risks**
| Risk | Likelihood | Mitigation |
|---|---|---|
| Missing one of the three duplicated PDP CTA call sites → inconsistent mobile/desktop behavior | Medium | Ship all three in the same change; existing `OrderPanel.test.js` "Affiliate brand button functionality" suite covers this and needs updating, not just passing |
| `SavedPage.test.js` currently mocks `ListingCard` entirely, so it won't exercise the new CTA/trust-sheet wiring by default | Medium | New test cases either un-mock `ListingCard` for this path or assert `SavedPage`'s own `handleShopNow` state directly |
| Early-access copy ships as a de facto permanent choice with no real experiment ever run | Medium | Flagged explicitly in §8 as an open PMM follow-up, not resolved here |
| Anon toast-suppression logic (tracking "last toggle source") adds a small new reducer field | Low | Keep to a single `lastToggleSource` field, a display gate only — not a new subsystem |

---

## 11. Out of Scope / Future Considerations

- A real Sharetribe cart/multi-item checkout (would require the full custom build Sharetribe's own dev-blog series describes — new transaction process, `CartPage.duck.js`, partial-refund handling — not undertaken here).
- Renaming `/saved` to "Cart" (see §3) — revisit only alongside a real, committed "full marketplace" roadmap and its own comms plan, not as a byproduct of this change.
- A real experimentation framework for the sign-up copy variant (§8).
- `brand_id` as a confirmed schema field (pre-existing open item, see `crossshop-tracking.md` §3 "brand_id caveat" — unaffected by this PRD).
- Sort / filter controls, explicit Remove+Undo, a sold-out "Saved for later" section, and price-drop / back-in-stock alerts on `/saved` — all acknowledged competitor patterns, deferred out of §14 (see §14.4).

---

## 12. Follow-Up: Post-Ship UX Fixes (Founder Review, 2026-08-13)

Founder's first in-browser pass on the shipped flow (§9's build note flagged this was still pending) surfaced two issues, both confirmed against the actual code — not hypothesized:

1. **No way back to the cart from the PDP.** The header's only entry point to `/saved` (`savedLinkMaybe` in `TopbarDesktop.js` / `TopbarMobileMenu.js`) is gated behind `authenticatedOnClientSide`. Combined with `SavedItemsBanner`'s toast being deliberately suppressed for `add_to_cart_button`-sourced saves (§6 edge cases, correct as designed), **anonymous shoppers get zero feedback and zero navigation path after clicking Add to Cart** — the banner-suppression comment's claim that "this flow already routes the shopper through /saved" is not true for anon users. Even authenticated shoppers get only a static text link with no count, unlike the adjacent `InboxLink`, which already has a badge precedent (`.notificationDot`).
2. **CTA content renders left-aligned, not centered.** `SavedListingButton.module.css`'s `.buttonContent` is `display: flex` with no `justify-content`, silently overriding the `text-align: center` inherited from the composed `.buttonPrimary` global class. Affects both the `cta` and `button` variants.

A `/ux-design panel` + `/uxr` review (transcript: this session) ran against the fix set below. Their additions are folded into the acceptance criteria and analytics requirements here so a fresh implementation session doesn't have to re-derive them.

### 12.1 Root Causes (confirmed in code, not inferred)

| Issue | File | Root cause |
|---|---|---|
| No path back to cart | `TopbarDesktop.js:182`, `TopbarMobileMenu.js:265` | `SavedPage` header link conditioned on `authenticatedOnClientSide` |
| No confirmation feedback | `SavedItemsBanner.js:22-24` | Toast suppressed for `add_to_cart_button` source with no replacement feedback mechanism, so anon users get nothing |
| Left-aligned CTA text | `SavedListingButton.module.css` `.buttonContent` | `display: flex` with no `justify-content: center`, overrides inherited `text-align: center` from `.buttonPrimary` |

### 12.2 Fixes to Implement

| # | Fix | Files touched |
|---|---|---|
| 1 | Add `justify-content: center;` to `.buttonContent` | `SavedListingButton.module.css` |
| 2 | Un-gate the header "Saved" link — visible whenever `savedCount + anonSavedItems.length > 0`, not just when authenticated | `TopbarDesktop.js`, `TopbarMobileMenu.js` |
| 3 | Add a numeric count badge to the header Saved link, sourced from the same `selectSavedListingIds` / `selectAnonSavedItems` selectors `SavedListingButton` already uses | `TopbarDesktop.js` + its CSS module |
| 4 | On Add to Cart click, show an inline "✓ Added · View Saved (n) →" confirmation under the CTA, auto-dismissing after ~4s (reuse `SavedItemsBanner`'s existing `AUTO_DISMISS_MS` convention) — **must render for anonymous users**, since that's the segment with zero feedback today | `ProductOrderForm.js`, `OrderPanel.js`, `InquiryWithoutPaymentForm.js` |

### 12.3 Panel Additions (from `/ux-design panel` + `/uxr`, folded into scope)

- **P0, non-negotiable**: fix #4's confirmation must be `aria-live="polite"` — the existing "Added to Cart ✓" button-text swap is currently silent to screen readers, which is worse than what sighted anon users get today (Chidinma Okafor, accessibility panel).
- **Build note, not a new AC**: back the header badge count, the fix #4 confirmation text, and `SavedPage.itemsReadyToShop` with one shared count-format function, not three hand-rolled pluralizations that will drift (David Kessler, design-systems panel).
- **New analytics requirement**: no event today connects "clicked Add to Cart" to "returned to /saved" to "clicked Shop" — without a funnel-linking event, this fix round can't be measured post-launch (Priya Ramanathan, growth-PM panel). Add a lightweight `source` tag (e.g. `saved_page_view` with `entry: 'add_to_cart_confirmation' | 'header_badge' | 'direct'`) alongside the existing `saved_listing_toggle` / `brand_clickout` events — same minimal `dataLayer.push` pattern, no new event bus.
- **Accepted as known trade-off, not actioned this round**: this fix set makes the flow legible but doesn't shorten it — a shopper who already knows and trusts the brand (Neha's fulfillment-mode behavior, `buyer-personas.md`) still takes the same number of clicks to reach the brand's checkout. No fast-path is being built here.
- **Escalate later, not now**: whether `/saved` should support a no-navigation "quick check" (e.g., a hover/tap preview off the header badge) instead of always requiring a full page visit is a legitimate information-architecture question (Kavya Subramaniam) but out of scope for this fix round — added to §11 Out of Scope.

### 12.4 Updated Acceptance Criteria (additive to §9)

- [x] CTA button content (`cta` and `button` variants) renders horizontally centered
- [x] Header "Saved" link is visible for any user (authenticated or anonymous) with ≥1 saved item, not just authenticated users
- [x] Header "Saved" link shows a numeric count reflecting `savedListingIds.length` (authenticated) or `anonSavedItems.length` (anonymous)
- [x] Clicking Add to Cart shows an inline confirmation with a direct link to `/saved`, for both authenticated and anonymous users
- [x] That confirmation is announced via `aria-live="polite"` for screen-reader users
- [x] Confirmation auto-dismisses after ~4s, consistent with `SavedItemsBanner`'s existing timing
- [x] A new analytics event (or tagged `source` on an existing one) connects Add-to-Cart-confirmation clicks to `/saved` page views

### 12.5 Out of Scope (additive to §11)

- A fast-path checkout flow for shoppers who already recognize and trust the brand (Neha's fulfillment-mode case) — friction is reduced via legibility, not step-count, in this round.
- A no-navigation "quick check" preview off the header badge (hover/tap mini-list) instead of a full `/saved` page visit — real IA question, deferred to a future PRD cycle.

---

## 13. Follow-Up: SavedPage Full-Page UX Review (2026-08-13)

§12 scoped the add-to-cart confirmation slice only. A second `/ux-design panel` + `/uxr` pass reviewed the rest of `/saved` as a page — header/subheading, `SavedPageSignupPush`, empty state, item-count line, the `ListingCard` grid, and `RedirectTrustSheet` — and surfaced additional, distinct issues, all grounded in the current code (`SavedPage.js`, `ListingCard.js`, `RedirectTrustSheet.js`).

### 13.1 Fixes to Implement

| # | Fix | Priority | Files touched |
|---|---|---|---|
| 5 | Render the item-count line (and ideally the grid) above `SavedPageSignupPush`, not below it — an anon shopper arriving to confirm a save should see their item before a sign-up pitch | P0 | `SavedPage.js` |
| 6 | Add a total-saved count alongside the existing "ready to shop" count (e.g. "5 saved · 3 ready to shop") — today `itemsReadyToShop` silently counts only `brand && productUrl` listings with no explanation for the rest | P0 | `SavedPage.js`, `en.json` (new/updated translation key) |
| 7 | Return focus to the triggering "Shop on {brand}" button when `RedirectTrustSheet` closes (`onClose` / `handleContinue`) — currently drops keyboard/screen-reader focus with no defined landing spot (WCAG 2.4.3) | P0 | `RedirectTrustSheet.js`, `SavedPage.js` (needs a ref back to the clicked card's button) |
| 8 | Announce the Continue button's 1.5s activation delay via `aria-live`, not just a visual `disabled` state — a screen-reader user currently gets no indication the button will become interactive shortly | P0 | `RedirectTrustSheet.js` |
| 9 | Give cards that lack a qualifying `brand`+`productUrl` (so they render no Shop CTA) a small affordance instead of just looking incomplete next to cards that do have one | P2 | `ListingCard.js` |

### 13.2 Explicitly Not Actioned (documented trade-offs, not gaps)

- `RedirectTrustSheet` doing double duty as trust disclosure *and* sentiment-collection survey at the highest-intent moment in the flow — valuable as a research instrument; flagged so a future session doesn't "simplify" it without knowing why it's shaped this way.
- No sort/filter/grouping on the saved-items grid — real information-architecture question once usage grows toward the 200-item cap, but no current usage data justifies building it now. Added to §11/§12.5 Out of Scope.

### 13.3 Updated Acceptance Criteria (additive to §9 and §12.4)

- [x] `SavedPage`'s item-count line (and grid) renders above `SavedPageSignupPush` in visual order
- [x] `SavedPage` shows both a total-saved count and the existing "ready to shop" count
- [x] Closing `RedirectTrustSheet` (via Continue or dismiss) returns keyboard focus to the button that opened it
- [x] `RedirectTrustSheet`'s 1.5s Continue-button activation delay is announced via `aria-live="polite"`
- [x] Cards without a qualifying Shop CTA render a defined fallback state rather than an unexplained gap (P2 — nice to have, not blocking)

### 13.4 Out of Scope (additive to §12.5)

- Sort, filter, or grouping controls on the saved-items grid.
- Any redesign of `RedirectTrustSheet`'s sentiment-survey content or flow — its dual-purpose shape is intentional, not a defect.

### 13.5 Build Note (2026-08-13) — Two Additional Bugs Found in Browser QA

§12/§13's nine fixes shipped 2026-08-13, full test suite green (unit tests updated in
`OrderPanel.test.js`, `SavedPage.test.js`, `RedirectTrustSheet.test.js`,
`TopbarMobileMenu.test.js`). Manual browser verification of the anonymous path — done
specifically because §9's original round shipped on unit tests alone and missed the bugs
that led to this follow-up — surfaced two further blocking bugs, neither hypothesized,
both confirmed live and fixed:

1. **`/saved` route was auth-gated** (`routeConfiguration.js`, `auth: true` /
   `authPage: 'LoginPage'` on the `SavedPage` route). Every fix in §12 that gives an
   anonymous shopper a link to `/saved` (header badge, Add-to-Cart confirmation) was
   silently routing them to `/login` instead — the route guard predates this PRD and was
   never revisited when `SavedPage.js` grew its own anonymous-shopper rendering path.
   Fixed by removing the guard; `SavedPage.js` already branches correctly on
   `isAuthenticated`.
2. **`SavedPage` never fetched or rendered listings for anonymous shoppers.**
   `mapStateToProps` derived the grid exclusively from `selectSavedListingIds` (the
   authenticated-only list from `privateData`), never from `anonSavedItems`. An anonymous
   shopper who added an item saw "Nothing saved yet" on `/saved` even with a real saved
   item and a correct header badge count. Fixed by adding
   `selectEffectiveSavedListingIds` to `savedListings.duck.js` (auth → `savedListingIds`,
   anon → `anonSavedItems.map(id)`) and using it for both the fetch trigger and the grid
   in `SavedPage.js`; `selectSavedItemsCount` now derives from the same selector instead
   of duplicating the branch.

Both fixes are covered by new tests (`SavedPage.test.js`: anonymous-grid regression test;
`routing` suite unaffected). Verified live: anonymous Add-to-Cart → header badge → `/saved`
→ item renders → Shop CTA → `RedirectTrustSheet` → aria-live delay/ready announcement →
dismiss → focus returned to the triggering button. Authenticated path verified via the
existing/updated unit tests (component logic is shared, only the data source selector
branches on `isAuthenticated`) — not re-verified live in-browser in this session.

---

## 14. Follow-Up: Multi-Brand Cart Grouping + Inspiration-First Recommendations (✅ Shipped, 2026-08-13)

§12/§13 fixed the *legibility* of `/saved` (nav paths, counts, focus, anon parity). A
marketplace-UX competitor review (Etsy, Amazon "Saved for later", ASOS Saved Items, Depop,
Wayfair, Pinterest boards) then looked at the *shopping model* itself and surfaced two
distinct improvements, both grounded in current code — not the sort/filter question §13.4
deferred, which stays deferred.

### 14.0 Why

1. **`/saved` is structurally a *multi-brand* cart, not a single basket.** Every exit is a
   per-brand Shopify redirect (Mela never runs a unified checkout — §2, §11). The correct
   competitor analog is therefore **Etsy's cart** (grouped by shop, per-shop checkout),
   *not* Amazon's single basket. The current flat `ListingCard` grid (`SavedPage.js:172-185`)
   hides this: "3 items ready to shop" should read "2 on Nicobar · 1 on Nesavu." Grouping
   by brand makes the page's structure match how buying actually works here.
2. **A saved page is a discovery surface, not a dead end.** Amazon/Wayfair seed empty and
   thin carts with recommendations — which *is* Mela's stated identity (inspiration-first,
   not fulfillment). Today the empty state is a bare "Nothing saved yet" + one Browse link
   (`SavedPage.js:145-157`), and a populated page ends abruptly after the grid.

### 14.1 Fixes to Implement

| # | Fix | Priority | Files touched |
|---|---|---|---|
| 10 | Group `savedListings` by `publicData.brand` into per-brand groups, each rendered via a new presentational `SavedBrandGroup` component (header: brand name · item count · soft subtotal · optional group CTA, then the existing responsive grid of that brand's cards). Preserve recency order (`getListingsById` at `SavedPage.js:214` already returns entities in `savedListingIds` insertion order). | P0 | `SavedPage.js`, new `components/SavedBrandGroup/*`, `SavedPage.module.css`, `components/index.js`, `en.json` |
| 11 | Listings with no `brand` collect into a trailing **"More saved"** group so nothing is dropped — these are the same cards that already render the §13.1 #9 fallback link. | P0 | `SavedPage.js` |
| 12 | Group **"Shop {brand} →"** CTA routes through the **existing** `handleShopNow` → `RedirectTrustSheet` → `openBrandStorefront` pipeline (`SavedPage.js:87-99`) using the **first in-stock item's `productUrl`**. ⚠️ There is **no brand-storefront root URL** in `publicData` — only per-product `productUrl` (`ListingCard.js:341`) — so the CTA lands on the brand's store via a representative product and is framed "Shop {brand} →", *not* "Shop all N" (which would over-promise a brand landing page we don't have). Omit the group CTA when a group has no shoppable item; per-card CTAs still cover those. Pass `triggerElement` so §13.1 #7 focus-return keeps working. | P0 | `SavedBrandGroup`, `SavedPage.js` |
| 13 | Soft per-brand subtotal via `formatMoney` (`util/currency.js`) — rendered only when every item in the group has a price in the **same** currency; otherwise show count only. Never invent a total across mixed/missing currencies. | P1 | `SavedBrandGroup`, `en.json` |
| 14 | Inspiration-first recommendations: new `SavedPageRecommendations` reusing the `NewFromIndia.js` pattern (`util/homepageSdk` query → `updatedEntities`/`denormalisedEntities` → `ProductCarousel`, capped per brand with `capPerBrand`). **Exclude already-saved ids** and self-hide when empty. Render in the empty state (as a "Popular on Mela" entry point) and once at page bottom for populated pages. | P0 | new `components/SavedPageRecommendations/*` (or co-located), `SavedPage.js`, `en.json` |

### 14.2 Panel Additions (from `/ux-design panel` + `/uxr`, folded into scope)

- **P0, a11y (Chidinma Okafor):** each brand group's header must be a real heading
  (`<h2>` inside a `<section aria-label="{brand}">`), not styled text, so screen-reader
  users get the same "cart is grouped by brand" structure sighted users get; the recs
  `ProductCarousel` must stay keyboard-reachable and not trap focus.
- **Build note, design-systems (David Kessler):** reuse the shared count-format helper
  introduced for the §12.3 header badge / `itemsSummary` for the per-group counts — don't
  hand-roll a fourth pluralization that will drift.
- **New analytics requirement (Priya Ramanathan):** the group CTA and the recs rail need
  their own surface tags so the funnel can distinguish "shopped the whole brand" from
  "shopped one item," and can measure whether recs drive discovery — see
  `insights/crossshop-tracking-prd.md` §14.
- **Accepted trade-off, not actioned:** grouping adds vertical length on large carts;
  acceptable for legibility. This round still adds **no fast-path checkout** (§12.5 stands).

### 14.3 Acceptance Criteria (additive to §9, §12.4, §13.3 — ✅ Shipped, code-complete + browser-verified)

- [x] Saved items render in per-brand groups, each with brand name, an accurate item count, and (when derivable) a soft subtotal
- [x] Listings without a `brand` render in a trailing "More saved" group; nothing is dropped
- [x] Subtotal is suppressed when a group's items span multiple currencies or any item lacks a price
- [x] Group "Shop {brand} →" CTA routes through `RedirectTrustSheet` (first session click), returns focus to the group CTA on close, and is omitted when the group has no shoppable item
- [x] Recommendations render in the empty state and once at the bottom of a populated page, never echo already-saved items, and self-hide when the query returns nothing
- [x] Group headers are real `<h2>`s within labelled sections; the recs carousel is keyboard-navigable
- [x] New analytics surfaces are emitted per `insights/crossshop-tracking-prd.md` §14

### 14.5 Build Note (2026-08-13)

Implemented as specified: `SavedPage.js` groups `savedListings` by `publicData.brand`
(first-seen order preserved), trailing brand-less items into a `{ brandName: null }`
"More saved" group; new `SavedBrandGroup` (header `<h2>` in a labelled `<section>`, item
count, `formatMoney`-based subtotal via `Decimal` summation gated on same-currency +
every-item-priced, group CTA using the first in-stock shoppable listing) and new
`SavedPageRecommendations` (recency query via `util/homepageSdk`, `capPerBrand` at 2/8,
excludes saved ids, self-hides when empty, reports back via `onLoaded` so the page's
`saved_page_view` push can carry real `recs_shown`/`brand_group_count`).

One implementation issue found and fixed during this pass, not in the original spec: a
naive `!fetchInProgress` gate on the bottom recs rail and the delayed `saved_page_view`
push caused a one-render flash (recs mounting then immediately unmounting) whenever
listing entities were already in the Redux store before the fetch thunk's
`fetchInProgress` flag had settled, and could leave `saved_page_view` permanently unfired
if a fetch never resolved. Fixed with a `dataSettled = hasListings || !fetchInProgress`
condition used consistently for both. Covered by a dedicated unit test
(`SavedPage.test.js`, "fires the delayed saved_page_view...").

**Live-verified 2026-08-13, anonymous path** (localhost dev, real dev Sharetribe
backend — House of Chikankari + Tarinika listings): saved 1 + 2 items across two brands →
`/saved` rendered two real `<h2>` brand groups ("House Of Chikankari" · 1 item · $48,
"Tarinika" · 2 items · $265, subtotal summed correctly); clicked group "Shop Tarinika →" →
`RedirectTrustSheet` opened (first click) → dismissed → focus returned to the group CTA
button (confirmed via `document.activeElement`); clicked it again → `brand_clickout` fired
with `saved_surface: 'saved_brand_group'`, correct `destination` (first in-stock item's
`productUrl`), real outbound redirect to tarinika.com in a new tab; a per-card CTA on the
same page fired `brand_clickout` with `saved_surface: 'saved_item_card'` and its own
product's URL. `saved_page_view` observed via `window.dataLayer` with
`recs_shown: true, brand_group_count: 2` on the populated page and
`recs_shown: true, brand_group_count: 0` on an emptied cart. Emptied the cart and
confirmed the "Popular on Mela" empty-state recs entry point rendered with its own copy.
No console errors attributable to this change (only a pre-existing, unrelated Mapbox
token warning). Not verified live in this pass: the authenticated path (logic is shared
with the anon path per `selectEffectiveSavedListingIds`, and is covered by
`isAuthenticated: true` unit tests) and the "no shoppable item" / "every item out of
stock" group-CTA-omission edge cases (covered by `SavedBrandGroup.test.js` only).

### 14.4 Out of Scope (additive to §11, §12.5, §13.4)

- Sort / filter controls on the saved grid (still deferred per §13.4).
- Explicit Remove + Undo affordance (today removal is the heart toggle only).
- Stock-state separation — a distinct sold-out "Saved for later" section — and price-drop
  / back-in-stock alerts (the latter needs backend not built here).

---

## Superseded Approach (for reference)

Prior to this PRD, `pre-redirect-sentiment-prd.md` shipped the trust/feedback modal (`RedirectTrustSheet`) triggered directly from the PDP's "Shop from {brand}" CTA, with no intermediate cart-like step — i.e. "Add" and "go to brand" were the same click. That approach is not wrong on its own terms (it shipped, and the trust-sheet mechanics are fully preserved here); it's being changed specifically because F-004 identified the missing intermediate step as making the PDP feel incomplete for purchase-flow testing, and because splitting "add" from "go to brand" creates a natural, non-generic-sounding surface (`/saved`) to host a sign-up ask. The trust-sheet component, its copy, and its session-dedupe logic are carried forward unchanged — only the trigger point moves.

---

*Created: 2026-08-12*
*Updated: 2026-08-13 — added §12 (add-to-cart confirmation follow-up: founder browser-testing feedback + `/ux-design panel` + `/uxr` review) and §13 (full-page SavedPage review: second `/ux-design panel` + `/uxr` pass); §12+§13 fixes shipped and browser-verified same day, see §13.5 build note*
*Updated: 2026-08-13 — added §14 (Planned: multi-brand cart grouping + inspiration-first recommendations, from a marketplace-UX competitor review; instrumentation in `insights/crossshop-tracking-prd.md` §14; execution handoff in `scratchpad/saved-multibrand-recs-handoff-prompt.md`). Not yet built.*
*Related PRDs: `pre-redirect-sentiment-prd.md` (trust-sheet origin, superseded trigger point — see build note added there), `saved-items-pasand-prd.md` (SavedPage origin, extended with Shop CTA — see build note added there), `mela-docs/technical/analytics/crossshop-tracking.md` (event schema, updated alongside this PRD)*
