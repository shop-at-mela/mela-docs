# Pre-Redirect Sentiment Collection PRD

**Feature:** "Was Mela Helpful?" Feedback Modal + Broader Sentiment Strategy
**Status:** ✅ Shipped — implementation diverged from spec; see build notes below
**Priority:** High — Pre-Production (launch blocker for baseline data)
**Owner:** Developer + PM

> **Build note (2026-05-25):** The pre-redirect modal was shipped as `RedirectTrustSheet` + `SentimentSheet` (in `src/components/`) rather than the `ShopifyRedirectModal` name specified here. The implementation was absorbed into `trust-conversion-signals-prd.md`, which is the authoritative tracking document for this feature. ACs below are updated to reflect actual shipping status.

---

## Problem Statement

Mela acts as a discovery layer — shoppers find Indian sustainable brands here, then purchase on Shopify. The current redirect is silent: when a user clicks "Shop from {brand}", `window.open(productUrl)` fires immediately with no signal captured. Mela has no data on whether it influenced the purchase decision or was simply a pass-through.

This must be fixed before launch to establish a feedback baseline from day one.

---

## Feature 1: Pre-Redirect Modal (Ship First)

### User Flow

1. Shopper views a listing at `/l/:slug/:id`
2. Clicks "Shop from {brand}" CTA
3. **New:** A lightweight modal appears before navigating away
4. Shopper taps Yes, No, or skips
5. Shopify URL opens immediately — shopper is never blocked

### Modal Design

```
┌─────────────────────────────────────────┐
│  Did Mela help you discover this brand? │
│                                         │
│  [ 👍 Yes, it did ]  [ 👎 Not really ]  │
│                                         │
│        Skip and continue to {brand} →   │
└─────────────────────────────────────────┘
```

- **Headline:** "Did Mela help you find this?"
- **Buttons:** "Yes" / "Not really"
- **Skip link:** "Skip and go to {brand}" — always proceeds regardless
- **Redirect timing:** Open Shopify URL immediately on any interaction (0ms delay). Capture event async in background — never block navigation.
- **Session deduplication:** Once a user responds or skips for a given listing, do not show modal again in the same session (localStorage flag per listingId).

### Data Captured Per Event

```json
{
  "event": "pre_shopify_redirect",
  "response": "yes | no | skip",
  "listingId": "uuid",
  "brand": "brand name",
  "productUrl": "shopify url",
  "timestamp": "ISO 8601",
  "sessionId": "anonymous"
}
```

### Technical Implementation

**Files to change:**
- `src/components/OrderPanel/ProductOrderForm.js` line 285 — wrap `window.open` in modal trigger
- `src/components/OrderPanel/OrderPanel.js` line 544 — same
- `src/components/OrderPanel/InquiryWithoutPaymentForm.js` line 21 — same
- New component: `src/components/ShopifyRedirectModal/ShopifyRedirectModal.js`
- `src/translations/en.json` — add modal copy keys

**Data destination:** POST event to Airtable via Make (Zapier alternative) webhook. Free tier sufficient for early launch volumes.

---

## Broader Buyer Journey — Sentiment Touchpoints

| Stage | Page | Trigger | Question | Priority |
|-------|------|---------|----------|----------|
| Pre-redirect | Listing page `/l/:slug/:id` | Click "Shop from brand" | "Did Mela help you find this?" | **P0 — ship now** |
| Dead-end search | Search `/s` with 0 results | Immediately on empty state render | "Tell us what you were looking for" (free text field) | P1 |
| Browse abandonment | Search `/s` | After 30s on page with no listing click | "Finding what you're looking for?" | P2 |
| Brand exploration | Brand profile `/u/:id` | After scrolling 75% of page | "Is this brand what you expected?" | P2 |
| Returning user NPS | Any page | 3rd+ session (localStorage session counter) | "How likely are you to recommend Mela?" (0–10) | P3 — post-launch |
| Post-save | `/saved` | After saving 3+ items | "What are you shopping for today?" (multi-select) | P3 |

**Recommended ship order:** Pre-redirect modal → Zero-results prompt → Returning user NPS.

---

## Tool Recommendation

Sharetribe has no native feedback or plugin system. All tools integrate via JS.

| Tool | Use Case | Cost | Notes |
|------|----------|------|-------|
| **Custom React modal** ← use for pre-redirect | In-flow interstitial, brand-matched styling | Free | Native React, async POST to Airtable. No third-party JS on the critical redirect path. |
| **Hotjar** ← use for passive insights | Session replay, heatmaps, NPS surveys | Free up to 35 sessions/day | Single `<script>` tag in `public/index.html`. Can run returning-user NPS without code. |
| Typeform popup | Standalone survey links | Free (10 responses/mo) | Good for email follow-ups, not in-flow |
| Google Forms hidden POST | Zero-cost capture | Free | Works but brittle; no dashboard |

**Final recommendation:**
- Pre-redirect modal: **custom React component → Airtable via Make webhook**
- Broader session insights + NPS: **Hotjar free tier** (add script tag, configure surveys in Hotjar dashboard, no further dev needed)

### Airtable Schema (Feedback Base)

| Field | Type |
|-------|------|
| Timestamp | Date/Time |
| Response | Single Select (yes / no / skip) |
| Brand | Text |
| Listing ID | Text |
| Product URL | URL |
| Stage | Single Select (pre_redirect / search_empty / nps / browse) |
| NPS Score | Number (0–10, optional) |
| Free Text | Long text (optional) |
| Session ID | Text (anonymous) |

---

## Acceptance Criteria

- [x] Clicking "Shop from {brand}" shows the modal before navigating away — shipped as `RedirectTrustSheet` triggered on first CTA click per session
- [x] Selecting Yes, No, or Skip navigates to Shopify within 200ms of click — "Continue to [Brand] →" always pinned and accessible
- [x] Response is captured async (non-blocking) — posts to webhook as `event: 'pre_shopify_redirect'`
- [x] Modal is skippable — shopper is never blocked from reaching Shopify
- [x] Modal does not re-appear for the same listing in the same browser session — gated by `mela_redirect_trust_shown` session key; subsequent CTA clicks skip the sheet and redirect directly
- [x] Mobile-responsive at 375px
- [ ] Hotjar script added to `public/index.html` (or via env-based inject) — ❌ not found in `public/index.html`
- [ ] Zero-results search state shows a text input prompt (P1) — ❌ not built
