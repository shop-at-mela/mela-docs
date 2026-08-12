# Add to Cart Restoration + SavedPage Shop CTA PRD

**Status:** ✅ Shipped (2026-08-12) — all P0 acceptance criteria in §9 implemented as specified. `SavedPageSignupPush`'s traffic-split mechanism (§8) remains an open PMM follow-up, unchanged from the PRD.

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

- [ ] In-stock brand+productUrl PDP listings show "Add to Cart," not "Shop from {brand}"
- [ ] Clicking Add to Cart does not open `RedirectTrustSheet` and does not open a new tab
- [ ] Clicking Add to Cart fires `saved_listing_toggle` with `source: 'add_to_cart_button'`
- [ ] Out-of-stock brand+productUrl PDP listings are unchanged (still "View on {brand}," direct redirect + trust sheet)
- [ ] All three PDP CTA surfaces (`ProductOrderForm`, `OrderPanel` mobile bar, `InquiryWithoutPaymentForm`) reflect the change consistently
- [ ] `/saved` shows a "Shop on {brand} →" CTA on each saved item with `brand` + `productUrl` (stock-aware copy)
- [ ] Clicking that CTA opens `RedirectTrustSheet` on the first click of the session (any item, any brand) and redirects directly on subsequent clicks
- [ ] `RedirectTrustSheet`'s trust/disclosure copy is unmodified from its current PDP version
- [ ] `brand_clickout` fires (unchanged schema) when the shopper actually continues from `/saved`
- [ ] Heart-icon saves still fire `saved_listing_toggle` with `source: 'heart_icon'` and still trigger the anonymous `SavedItemsBanner` toast
- [ ] Add-to-Cart saves (anon) do NOT trigger the `SavedItemsBanner` toast
- [ ] `/saved` route, component, and translation identity remain "Saved" — no "Cart" naming introduced in code, URL, or page heading
- [ ] `SavedPageSignupPush` renders only for `!isAuthenticated` users with ≥1 anon-saved item, using the `earlyAccess` copy by default
- [ ] 200-item saved cap: Add-to-Cart button renders disabled + tooltip, not a silent no-op

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

---

## Superseded Approach (for reference)

Prior to this PRD, `pre-redirect-sentiment-prd.md` shipped the trust/feedback modal (`RedirectTrustSheet`) triggered directly from the PDP's "Shop from {brand}" CTA, with no intermediate cart-like step — i.e. "Add" and "go to brand" were the same click. That approach is not wrong on its own terms (it shipped, and the trust-sheet mechanics are fully preserved here); it's being changed specifically because F-004 identified the missing intermediate step as making the PDP feel incomplete for purchase-flow testing, and because splitting "add" from "go to brand" creates a natural, non-generic-sounding surface (`/saved`) to host a sign-up ask. The trust-sheet component, its copy, and its session-dedupe logic are carried forward unchanged — only the trigger point moves.

---

*Created: 2026-08-12*
*Related PRDs: `pre-redirect-sentiment-prd.md` (trust-sheet origin, superseded trigger point — see build note added there), `saved-items-pasand-prd.md` (SavedPage origin, extended with Shop CTA — see build note added there), `mela-docs/technical/analytics/crossshop-tracking.md` (event schema, updated alongside this PRD)*
