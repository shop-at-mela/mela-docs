# Newsletter & Login Nudge PRD

**Feature:** Newsletter Email Capture + Save Nudge Redesign
**Status:** 🟡 Ready for Development
**Priority:** High — Primary audience-building mechanism for validation phase
**Owner:** PM + Developer
**Created:** May 2026

---

## Executive Summary

**Feature**: Replace the existing single "sign up" save-nudge with a two-CTA model (newsletter first, account second), and add an email capture block to the ComingSoonSection on the homepage.
**Target Entry Points**: Homepage ComingSoonSection, SavedItemsBanner (all listing pages)
**Target Users**: Priya (second-gen, occasion-driven), Arun (cultural reclaimer), Neha (first-gen power user), Sarah (conscious parent)
**Business Objective**: Build an owned email audience to validate demand before formal brand agreements or revenue activity.
**Primary Success Metric**: Newsletter email captures per week (anonymous + authenticated combined)
**Secondary Metric**: Account signups (depth of intent)

---

## 1. Problem Statement

### Current State
- The `SavedItemsBanner` fires when an anonymous user saves a product. It shows a single CTA linking to `/signup`. Auto-dismisses in 4 seconds.
- The `ComingSoonSection` on the homepage shows 4 feature teaser cards with no engagement mechanism.
- **No email capture exists anywhere on the site.**

### User Pain Points
- Priya and Arun are in discovery mode — asking for a full account on first save is too high a commitment ask.
- Users who are interested in "what's coming" (checkout, reviews, wishlists) have no way to stay informed.
- The 4s auto-dismiss on the banner is too short to act on.

### Business Impact of Inaction
- Every browsing session that ends without email capture is a lost audience member.
- "Coming Soon" signals create curiosity with no conversion mechanism — wasted intent.
- Without an email list, there is no owned channel to validate demand, share brand launches, or get feedback.

---

## 2. Goals & Non-Goals

### Goals
- Capture email addresses from anonymous browsing users at two key moments: after saving a product and while viewing the coming-soon roadmap.
- Add a newsletter opt-in checkbox to the account signup flow for authenticated users.
- Sync all opt-ins to Beehiiv (email service) via a server-side API route.

### Non-Goals
- Building a full email preference center in-app (Beehiiv handles unsubscribe natively)
- Per-feature "Notify me" CTAs on individual ComingSoonSection cards (premature segmentation)
- Double opt-in confirmation email (revisit at 1,000+ subscribers)
- A/B testing infrastructure
- Push notifications or SMS
- Using newsletter email as login pre-fill or auto-creating Sharetribe accounts for newsletter subscribers

---

## 3. User Stories

| As a... | I want to... | So that... | Priority |
|---------|-------------|------------|----------|
| Browsing anonymous user | Stay informed about new brands without creating an account | I can return when I'm ready to buy | P0 |
| Anonymous user who saved a product | Get notified of new arrivals by email | I don't lose track of what I liked | P0 |
| Signed-up user | Opt in to Mela updates during account creation | I don't miss brand launches | P1 |
| Any user | See that "what's coming" on Mela is real | I trust the platform is actively developing | P1 |

---

## 4. Feature Requirements

### Must Have (P0)

**4.1 SavedItemsBanner — Two-CTA Model**
- Primary CTA: "Notify me" button → expands banner in-place to show inline email input + submit
- Secondary CTA: "Create account" plain-text link → navigates to `/signup`
- On email submit: POST to `/api/newsletter/subscribe`, show success state, set `sessionStorage` flag, dismiss banner after 3s
- Auto-dismiss (4s) only applies when email input is NOT expanded
- Once subscribed in session (`sessionStorage.melaNewsletterSubscribed = true`), banner never re-shows in that session
- Banner still hidden for authenticated users (existing behavior unchanged)

**4.2 ComingSoonSection — Unified Email Capture Block**
- Add one capture block below the 4 feature cards, above the `currentNote` disclaimer
- Heading: "Get early access"
- Subtext: "Be first when Unified Checkout, Community Reviews, and more go live."
- Email input + "Notify me" button
- Microcopy: "No spam. Mela updates only."
- On submit: POST to `/api/newsletter/subscribe` with `source: 'coming-soon-section'`
- Show inline success state after submission
- Stateless — local `useState` only, no Redux

**4.3 Server Route: `/api/newsletter/subscribe`**
- Accepts `POST { email: string, source: string }`
- Validates email format server-side
- Calls Beehiiv `POST /v2/publications/{PUBLICATION_ID}/subscriptions`
- Returns `{ subscribed: true }` on success
- API key stored in server env vars only — never exposed to client

### Should Have (P1)

**4.4 Signup Form — Newsletter Opt-In Checkbox**
- Add `marketingOptIn` boolean field to `configUser.js` with `scope: 'private'`
- Displayed in signup form via existing `CustomExtendedDataField` machinery
- **Default: unchecked** (CCPA requires affirmative opt-in for marketing email)
- Label: "Send me updates about new brands and products on Mela"
- Stored in `currentUser.attributes.profile.privateData.marketingOptIn`
- Not displayed on public profile (`displayInProfile: false`)

**4.5 Post-Signup Beehiiv Sync**
- After `signupThunk` resolves successfully, if `marketingOptIn === true`:
  fire-and-forget call to `subscribeToNewsletter(email, 'signup')`
- Must not block or break the signup flow on error

### Nice to Have (P2)

- Tag subscribers by source in Beehiiv for segmentation analytics
- Show "You're subscribed" state on ComingSoonSection for users who've already subscribed in the session (sessionStorage check)

---

## 5. UX Requirements

### SavedItemsBanner Flow

```
Anonymous user clicks heart on listing
          ↓
SavedItemsBanner appears (existing)
          ↓
      [Notify me]    [Create account →]
      (primary btn)  (secondary text link)
          ↓
  Banner expands in-place:
  [your@email.com input] [Subscribe]
  4s auto-dismiss CANCELLED
          ↓
  User submits email
          ↓
  "You're in — we'll notify you of new arrivals ✓"
  Banner auto-dismisses after 3s
  sessionStorage.melaNewsletterSubscribed = 'true'
```

**Edge cases:**
- User dismisses before clicking either CTA → existing dismiss behavior, timer still runs
- User clicks "Notify me" then manually dismisses without submitting → dismiss, no API call
- User already subscribed in session → banner shows "Create account" only (no email input)
- API error → show inline "Something went wrong — try again", do not auto-dismiss

### ComingSoonSection Capture Block Layout

```
┌─────────────────────────────────────┐
│  Get early access                   │
│  Be first when Unified Checkout,    │
│  Community Reviews, and more        │
│  go live.                           │
│                                     │
│  [your@email.com     ] [Notify me]  │
│  No spam. Mela updates only.        │
└─────────────────────────────────────┘
```

Success state: Replace form with "You're on the list ✓ We'll be in touch."

---

## 6. Technical Architecture

### Email Service: Beehiiv

Beehiiv selected over Mailchimp and Brevo:
- Free tier: 2,500 subscribers, unlimited sends
- Mailchimp rejected: 500-contact cap on free tier
- Brevo rejected: 300 emails/day cap (cannot send one newsletter to 500+ subscribers)
- API is idempotent by email — no custom dedup logic needed for anonymous-to-authenticated merge

### Storage Model

| User state | Storage |
|---|---|
| Anonymous newsletter subscriber | Beehiiv only |
| Authenticated user with opt-in | Sharetribe `privateData.marketingOptIn: true` + Beehiiv |

### Anonymous → Authenticated Merge Strategy

When an anonymous subscriber later creates an account with the same email and `marketingOptIn: true`, the Beehiiv subscription API upserts the contact (idempotent by email). No dedup logic required in the codebase.

### Files to Modify

| File | Change |
|---|---|
| `server/api/newsletter/subscribe.js` | **CREATE** — Beehiiv API route |
| `server/apiRouter.js` | Register `POST /newsletter/subscribe` |
| `src/util/api.js` | Add `subscribeToNewsletter(email, source)` helper (plain JSON, not transit) |
| `src/components/SavedItemsBanner/SavedItemsBanner.js` | Two-CTA model, inline email expand |
| `src/components/SavedItemsBanner/SavedItemsBanner.module.css` | Expanded state styles |
| `src/containers/MelaHomePage/sections/ComingSoonSection/ComingSoonSection.js` | Add email capture block |
| `src/containers/MelaHomePage/sections/ComingSoonSection/ComingSoonSection.module.css` | Capture block styles |
| `src/config/configUser.js` | Add `marketingOptIn` field |
| `src/ducks/auth.duck.js` | Post-signup Beehiiv sync in `signupThunk` |
| `src/translations/en.json` | SavedItemsBanner translation keys |
| `.env` | `BEEHIIV_API_KEY`, `BEEHIIV_PUBLICATION_ID` |

### New Translation Keys (`en.json`)

```json
"SavedItemsBanner.notifyMe": "Notify me",
"SavedItemsBanner.createAccount": "Create account",
"SavedItemsBanner.emailPlaceholder": "your@email.com",
"SavedItemsBanner.subscribeButton": "Subscribe",
"SavedItemsBanner.successMessage": "You're in — we'll notify you of new arrivals"
```

---

## 7. Acceptance Criteria

- [ ] Anonymous user saves a product → SavedItemsBanner shows "Notify me" as primary CTA and "Create account" as secondary text link
- [ ] Clicking "Notify me" expands banner in-place with email input; 4s auto-dismiss is cancelled
- [ ] Submitting email in banner → POST to `/api/newsletter/subscribe` succeeds → success message shown → banner dismisses after 3s
- [ ] After subscribing via banner, saving another product in same session → banner does NOT reappear
- [ ] Homepage ComingSoonSection shows email capture block below feature cards, above disclaimer
- [ ] Submitting email in ComingSoonSection → POST succeeds → inline success state shown
- [ ] `/signup` page shows `marketingOptIn` checkbox, **unchecked by default**
- [ ] Signing up with checkbox checked → `privateData.marketingOptIn: true` set on Sharetribe user AND contact created in Beehiiv
- [ ] Signing up with checkbox unchecked → no Beehiiv call made
- [ ] Anonymous subscriber + account signup with same email → one Beehiiv contact (not two)
- [ ] `BEEHIIV_API_KEY` is never present in any client-side bundle
- [ ] All email inputs validate format before submission (client + server)
- [ ] API error shows inline error state; banner/form does not disappear silently
- [ ] Both surfaces are mobile-responsive at 375px

---

## 8. Success Metrics & Measurement

**Primary KPI**: Newsletter email captures per week (tracked in Beehiiv dashboard)
- Week 1–2 (LinkedIn feedback cohort): 20+ captures
- Week 4 (wider sharing): 100+ captures
- Month 2: 250+ captures

**Track in Beehiiv:**
- Total subscribers by source (`save-nudge` vs `coming-soon-section` vs `signup`)
- Open rate on first send (>30% healthy for this audience)

**Track in GA4 / Hotjar:**
- `newsletter_subscribe_attempt` (email input focused)
- `newsletter_subscribe_success` (successful POST)
- `newsletter_subscribe_source` dimension

**Secondary KPI**: Account signups week-over-week (expect gradual uplift as newsletter audience converts)

---

## 9. Dependencies & Risks

| Item | Notes |
|---|---|
| Beehiiv account setup | Required before dev begins. ~30 min. Free at beehiiv.com. |
| `BEEHIIV_API_KEY` in production env | Must be added to Render/Heroku config vars before deploy |
| `CustomExtendedDataField` renders booleans as checkboxes | Verify before building signup checkbox — existing provider fields use boolean schema |
| CCPA compliance | Checkbox must be unchecked by default. Do not pre-check. |
| Founder H-1B constraint | No affiliate agreements signed; no revenue collected. Email capture is for validation only. See `footer-legalese-prd.md` for full legal context. |

---

## 10. Implementation Sequence

| Step | Work | Est. |
|---|---|---|
| 1 | Beehiiv account + publication + API key | 30 min |
| 2 | Server route (`newsletter/subscribe.js`) + `apiRouter.js` registration | 1 hr |
| 3 | `api.js` client helper `subscribeToNewsletter` | 15 min |
| 4 | `ComingSoonSection` capture block **(start here — no auth dependency, fastest live capture)** | 2 hr |
| 5 | `SavedItemsBanner` two-CTA model + CSS | 3 hr |
| 6 | `configUser.js` + signup checkbox | 1 hr |
| 7 | `auth.duck.js` post-signup sync | 1 hr |
| 8 | Translation keys + CSS polish | 1 hr |

**Total: ~10 hours**

---

## 11. Out of Scope / Future Considerations

- Email preference center in-app (Beehiiv handles unsubscribe natively)
- Per-card "Notify me" CTAs on ComingSoonSection feature cards
- Double opt-in email flow (revisit at 1,000+ subscribers)
- Segment / Amplitude funnel tracking (revisit at 500+ subscribers)
- Beehiiv referral / share mechanics (configure in Beehiiv dashboard when ready, no code needed)
- SMS or push notifications
- Drip email sequences for saved-items re-engagement (listed as Phase 2 in saved-items-pasand-prd.md)
