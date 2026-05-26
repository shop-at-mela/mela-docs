# Saved Items — "Saved / meri pasand" PRD

## Executive Summary
**Feature**: Heart / save any listing — letting users build a personal collection of items they love, with a dedicated "Saved" page (culturally subtitled *meri pasand*) to review them later.
**Target URL / Entry Points**:
- Heart icon overlaid on every `ListingCard` (Homepage, SearchPage)
- Heart icon + explicit "Save" button on ListingPage (image gallery module + OrderPanel)
- `MelaHomePage` — new **"Your Saved Items"** module below the HeroSection (signed-in users only)
- `/saved` — dedicated page showing all saved listings + link from Topbar (signed-in)
**Target Users**: Priya (Mixed Heritage), Arun (Second-Gen Cultural Reclaimer) — occasion-driven browsers who compare across multiple sessions; Neha (First-Gen) for brand-curating; Sarah for research-heavy decision cycles.
**Business Objective**: Increase return-visit rate and session depth; reduce "tab-hoarding" behaviour by giving users a native save mechanism; capture intent signal for future personalisation and email re-engagement.
**Primary Success Metrics**:
- Saves per signed-in session: baseline → target 1.2 (measured at 30-day mark)
- Return-visit rate (users who saved ≥ 1 item): baseline → +20% within 60 days
- Conversion rate from "Saved" page to external brand link click: target 15%

---

## Build Status Summary *(updated 2026-05-25)*

| Item | Component / File | Status |
|------|-----------------|--------|
| Redux duck (`savedListings`) | `src/ducks/savedListings.duck.js` | ✅ Shipped (269 lines) |
| `SavedListingButton` on `ListingCard` | `src/components/ListingCard/ListingCard.js` line 378 | ✅ Shipped |
| `SavedItemsBanner` (auth nudge) | `src/components/SavedItemsBanner/`, used in `TopbarContainer` | ✅ Shipped |
| Homepage `SavedItems` module ("Your Saved Items / meri pasand") | `src/containers/MelaHomePage/sections/SavedItems/SavedItemsModule.js` | ✅ Shipped |
| `SavedPage` container (`/saved` route) | `src/containers/SavedPage/SavedPage.js`, route configured | ✅ Shipped |
| Heart icon on `ListingCard` (hollow ↔ filled) | `src/components/ListingCard/` | ⚠️ Verify — `SavedListingButton` is imported but heart visual states unclear |
| Topbar `"❤ Saved"` link (authenticated) | `src/containers/TopbarContainer/` | ⚠️ Verify — `SavedItemsBanner` is in Topbar but may be auth nudge banner, not nav link |
| Auth gate — Tier 1 modal on first anon click | New modal or bottom sheet | ❓ Unknown — no separate auth gate modal found |
| Auth gate — Tier 2 persistent banner (≥2 anon saves) | Part of `SavedItemsBanner` | ⚠️ Likely partial — `SavedItemsBanner` exists, tier logic unknown |
| localStorage migration on login | `src/ducks/auth.duck.js` | ❓ Unknown — verify `migrateLocalSavesToProfile` dispatch |
| `/saved` page `noindex` meta | `SavedPage.js` | ❓ Verify |

**Overall**: Core save/unsave loop and all primary surfaces are shipped. Auth gate tiers, topbar nav link, and localStorage migration need verification.

---

## 1. Problem Statement

### Current State
Mela has no mechanism for users to save or revisit items they like. A user who browses a Chanderi baby kurta, goes away to show their partner, and returns the next day must search again from scratch. Competing surfaces (Etsy, Amazon, Pinterest) all offer native save/wishlist functionality. Mela's research-heavy personas (Priya, Sarah) open multiple tabs — a clear proxy for wanting to save.

### User Pain Points
- **Priya**: Shops for Diwali weeks in advance, across sessions; currently loses items she found earlier
- **Arun**: Shows Anjali items on mobile, wants a shared (or shareable) list rather than forwarded URLs
- **Sarah**: Does multi-day research before buying; no save = no loyalty loop
- **Neha**: Curates brand lists to share in WhatsApp groups; forwards individual URLs because there's no collection view

### Business Impact of Inaction
- No return-visit hook → single-session browse, low email retargeting signal
- No intent data → cannot surface "people are saving this" social proof
- No loyalty primitive → every session starts cold, weakening brand recall
- Missing a table-stakes feature that every Mela competitor already has

---

## 2. Goals & Non-Goals

### Goals
- Let any user heart/save a listing from the card (grid views) or listing page
- Persist saves to the authenticated user's Sharetribe `privateData` field (`savedListings`)
- Show a "Saved" module on the homepage for returning signed-in users (replaces or augments the hero CTA)
- Provide a dedicated `/saved` page listing all saved items
- Show a visible "Saved" link in the Topbar when the user is signed in
- Prompt unauthenticated users who click the heart to sign in / sign up (soft gate)
- Support un-saving (clicking the heart again removes the item)

### Non-Goals
- Public or shareable "Saved" collections (Phase 2 — see §12)
- Collaborative lists / multi-user sharing
- Email re-engagement using saved items (Phase 2)
- Admin-side analytics on most-saved items (Phase 2)
- Native mobile app (web-first for now)

---

## 3. Naming & Cultural Character

### Naming decision: Function in English, culture as texture

"Pasand" was the initial candidate but fails UXR scrutiny across all four personas:

| Persona | Hindi literacy | "Pasand" reaction |
|---------|---------------|-------------------|
| Sarah (Portland, non-Indian) | None | Mystery word — invisible feature |
| Priya (2nd gen, Chicago) | Passive — knows some words | Recognises warmly, wouldn't have discovered it |
| Neha (1st gen, Chennai / Tamil background) | Bollywood Hindi | Understands it, not her primary language |
| Arun (2nd gen, learning Hindi as adult) | Beginner | Risk of amplifying "not Indian enough" anxiety |

**Rule**: The functional label (in navigation, buttons, page H1) must be English. "Meri pasand" is used as cultural *texture* — a subtitle, a tooltip aside, a design signature — not a primary navigation label.

**Do not use as primary labels**: "Wishlist" (too transactional), "Favourites" (British spelling confusion in US market), "Like" (Facebook connotation), "Bookmark" (too functional/cold).

### Copy system

| Surface | Primary label | Cultural texture / note |
|---------|--------------|------------------------|
| Topbar link | `❤ Saved` | Tooltip: `"Your saved Mela finds"` — brand name carries cultural identity, no "Indian" label on user layer |
| Homepage module title | `"Your Saved Items"` | Italic subtitle: `"— meri pasand"` in warm serif (opt-in cultural texture, not primary nav) |
| Dedicated page H1 | `"Saved"` | Subheading: `"Your personal Mela collection — meri pasand ❤️"` |
| Heart icon tooltip / ARIA | `"Save"` / `"Saved"` | Icon carries meaning — no Hindi or "Indian" label needed |
| Explicit ListingPage button | `"Save ❤️"` → `"Saved ❤️"` | — |
| Empty state headline | `"Nothing saved yet"` | Sub-copy: `"Start exploring and heart the things you love — your meri pasand waits ❤️"` |
| Auth modal headline | `"Save this to your collection"` | Sub-copy: `"Create your meri pasand — it's free"` |
| Auth banner (≥2 anon saves) | `"Sign in to keep your [N] saved items"` | — |

> **Copy rule applied here**: "Indian" does not appear in any user-possessive context. "Mela" carries the cultural identity at the brand layer. "Meri pasand" appears only as decorative subtitle — cultural texture the user opts into by being on Mela, not a label imposed on them.

### Where the cultural character actually lives

The heart feature is a vehicle — the cultural differentiation is in the **icon design and empty state**:

1. **Heart icon — saved state**: Use a rangoli-inspired or mehndi-pattern filled heart instead of a solid red heart. Instantly distinct from every other platform. Sarah finds it beautiful; Priya and Neha feel seen; Arun feels culturally confident. No translation required.
2. **Empty state illustration**: A hand-drawn diya or lotus motif with `"Your meri pasand starts here"`. Works across all personas as evocative design, not language barrier.
3. **Page meta**: `/saved` route (not `/pasand`) — keeps URLs clean for English speakers and SEO.

---

## 4. Technical Architecture

### Data Storage: Sharetribe `privateData` — confirmed viable

`sdk.currentUser.updateProfile` is **already used** in this codebase (`ProfileSettingsPage.duck.js`). `privateData` is already read in `ProfileSettingsPage.js` via `user?.attributes.profile.privateData`. The `fetchCurrentUser` call in `user.duck.js` (via `sdk.currentUser.show`) automatically returns `attributes.profile.privateData` for authenticated users — no additional include parameters needed.

**Access path in duck thunks**:
```js
const savedIds = getState().user.currentUser?.attributes?.profile?.privateData?.savedListings ?? [];
```

**Why `privateData` over `publicData`**:
- `privateData` is only accessible to the user themselves via the authenticated Marketplace API — other users cannot read it
- `publicData` would expose a user's saved items to any API caller — a privacy violation
- Sharetribe does a **shallow merge** on `privateData` — writing `{ savedListings: [...] }` only updates that key and leaves all other `privateData` keys untouched. No need to spread the full object before writing.

**Write call**:
```js
sdk.currentUser.updateProfile({ privateData: { savedListings: updatedIds } }, queryParams)
```

**Schema — `privateData`**:
```json
{
  "savedListings": ["uuid-1", "uuid-2", "uuid-3"]
}
```
- **Max cap: 200 listings** — binding constraint is Sharetribe's 10KB `privateData` size limit (200 × 36-char UUID ≈ 7.2KB). At >275 saves, `updateProfile` would silently fail or error. 200 is a safe ceiling. At scale, Phase 2 shareable collections should use a separate data structure outside `privateData`.
- Ordering: prepend new saves (most-recent first)
- Removal: filter out the UUID on unsave

### Unauthenticated state — localStorage schema
```js
// Key: 'melaUnsavedItems'
// Array of objects (not just IDs) so nudge UI can show thumbnails without an API call:
[
  { id: 'uuid-1', title: 'Baby Kurta Set', imageUrl: 'https://...' },
  { id: 'uuid-2', title: 'Organic Swaddle', imageUrl: 'https://...' }
]
```
On login: all IDs are migrated to `privateData.savedListings` via `migrateLocalSavesToProfile` thunk, then `localStorage.removeItem('melaUnsavedItems')`.

### Redux Duck: `src/ducks/savedListings.duck.js`
Actions:
- `SAVE_LISTING_REQUEST / SUCCESS / ERROR`
- `UNSAVE_LISTING_REQUEST / SUCCESS / ERROR`
- `FETCH_SAVED_LISTINGS_REQUEST / SUCCESS / ERROR`

State shape:
```js
{
  savedListingIds: [],       // ordered array of UUIDs from privateData
  savedListings: [],         // full listing entities (fetched separately)
  saveInProgress: {},        // { [listingId]: true } — per-listing loading state
  fetchInProgress: false,
  fetchError: null,
}
```

Thunks:
1. `saveListing(listingId)` — optimistically add to local state; call `updateProfile`; rollback on error
2. `unsaveListing(listingId)` — optimistically remove; call `updateProfile`; rollback on error
3. `fetchSavedListings()` — read `currentUser.privateData.savedListings`; batch-fetch listing entities via `sdk.listings.query({ ids: [...] })`

### API Calls
```js
// Save / unsave (both use the same call, different arrays)
sdk.currentUser.updateProfile({
  privateData: { savedListings: updatedIds }
});

// Fetch listing entities for saved IDs
sdk.listings.query({ ids: savedIds, include: ['images', 'author'] });
```

### Unauthenticated State
- Heart icon is rendered on all cards regardless of auth state
- Clicking while unauthenticated triggers a modal: `"Save this to your collection"` with Login / Sign Up CTAs
- Store intent in `melaUnsavedItems` localStorage array — on successful login, auto-migrate all saved items

---

## 5. Feature Requirements

### Must Have (P0)

#### 5.1 Heart Icon on ListingCard
- Positioned: **bottom-right corner of the image**, inside `css.imageContainer`, above the `TrustBadges`
- Size: 32×32px tap target (mobile-safe)
- States: hollow heart (not saved) → filled red/coral heart (saved) → loading spinner (in-progress)
- The `ListingCard` receives `isSaved` (bool) and `onToggleSave` (function) as props
- Heart icon does NOT navigate to the listing page — it must `stopPropagation` on click (the outer `NamedLink` wraps the entire card)
- Rendered on: `HomePage` listing grids, `SearchPage` results

#### 5.2 Heart + Explicit Button on ListingPage
- **Image gallery module** (`SectionGallery`): heart icon overlaid on the primary image, bottom-right corner — mirrors card behaviour
- **OrderPanel / action area**: explicit `"Save ❤️"` button rendered below the primary CTA ("Shop at [Brand]")
  - Filled state: `"Saved ❤️"` (already saved)
  - This is the primary save CTA for the listing page; the gallery icon is a secondary convenience affordance

#### 5.3 Save / Unsave Redux Flow
- All save/unsave operations go through the `savedListings` duck
- Optimistic updates so the UI responds instantly
- Error rollback with a toast notification: `"Couldn't save — please try again"`

#### 5.4 "Saved" Module on Homepage (signed-in users with ≥ 1 saved item)
- **Placement**: New `<section>` inserted **between HeroSection and CategoryShowcase** in `MelaHomePage.js`
- **Renders**: A horizontal scroll row of up to 6 most-recently-saved `ListingCard` components (with heart icons active)
- **Section title**: `"Your Saved Items"` + italic subtitle: `"— meri pasand"` in warm serif
- **Section subtitle**: `"Items you loved — right where you left them"`
- **Footer CTA**: `"See all [N] saved items →"` → `/saved`
- **Condition**: only rendered if `currentUser` is authenticated AND `savedListings.length > 0`
- If user has 0 saves: section does not render (no empty state teaser on homepage — keep hero clean)

#### 5.5 Dedicated `/saved` Page
- Route: `SavedPage` (new container at `src/containers/SavedPage/`)
- Layout: full-width grid of `ListingCard` components (same layout as SearchPage results grid)
- H1: `"Saved"` + subheading: `"Your personal Mela collection — meri pasand ❤️"`
- Empty state headline: `"Nothing saved yet"` + sub-copy: `"Start exploring and heart the things you love — your meri pasand waits ❤️"` + CTA to Browse / Search
- Unauthenticated: redirect to `/login?from=/saved`
- Each card has its heart filled; clicking removes item from the list

#### 5.6 Topbar Link (signed-in users)
- **Desktop Topbar**: Add `"❤ Saved"` as a `NamedLink` in `TopbarDesktop.js`, to the left of the `InboxLink`, visible only when `currentUser` is authenticated
- **Mobile Menu** (`TopbarMobileMenu.js`): Add `"Saved"` as a top-level menu item when signed in
- Show a count badge if `savedListings.length > 0` (e.g. `❤ Saved (4)`) — optional, can be P1

#### 5.7 Auth Gate — Three-tier Escalating Nudge

**Tier 1 — First heart click (1 item in `melaUnsavedItems`)**
- Immediately on click: modal / bottom sheet
- Copy: `"Save this to your collection"` + sub-copy: `"Create your meri pasand — it's free"` + CTAs: `"Sign In"` / `"Create Account"`
- Dismissable — item is saved to localStorage even if dismissed

**Tier 2 — Second save and beyond (≥ 2 items in `melaUnsavedItems`)**
- On any page load (and immediately when the 2nd item is saved): a **persistent slim banner** appears below the Topbar
- Banner copy: `"❤️  You've saved [N] items — sign in to keep them forever   [Sign In]  [Create Account]  ✕"`
- Background: `#FDF0EE` (soft coral tint) — warm, non-alarming
- Height: 44px, `position: sticky; top: topbarHeight`
- The `✕` hides the banner for 24hrs (stored as `melaUnsavedBannerDismissed: timestamp` in localStorage) — banner reappears after 24hrs
- Banner is NOT shown if user is authenticated

**Post-login migration** (both tiers):
```js
// In auth.duck.js login success — add migration step:
const pending = JSON.parse(localStorage.getItem('melaUnsavedItems') || '[]');
if (pending.length > 0) {
  const ids = pending.map(p => p.id);
  dispatch(migrateLocalSavesToProfile(ids)); // thunk in savedListings.duck.js
  localStorage.removeItem('melaUnsavedItems');
  localStorage.removeItem('melaUnsavedBannerDismissed');
}
```

---

### Should Have (P1)

#### 5.8 Count Badge in Topbar
- Show `(N)` count next to `"❤ Saved"` when N > 0
- Disappears if user empties their list

#### 5.9 Save as Sign-up / Login Value Prop
- On `AuthenticationPage` login and signup forms, add a **contextual prompt** below the form headline
- If `melaUnsavedItems` is in `localStorage` with ≥ 1 item: `"Sign in to save [item name] to your collection"` with thumbnail
- Generic fallback (no pending items): add a 3-bullet value prop:
  - `❤️ Save your favourite Mela finds`
  - `🔔 Get back to items you loved, instantly`
  - `🛍️ Build your personal collection`

> **UXR note 2026-05-25**: The generic fallback bullets above sell *bookmarking*, but users come to Mela to *discover* — they haven't found things they love yet when they hit the signup page. The value of an account should be framed around discovery continuity (Mela remembers what you care about, surfaces new relevant products) rather than retrieval. Consider replacing the generic fallback with: `"Mela remembers what you love — and surfaces new arrivals you'll want to see."` as a headline + shorter bullets. See also §8 below for the `SignupPage/ValueProposition` component, which currently uses copy that violates the user-layer "Indian" framing rule.

#### 5.10 Save Count in Listing Title Area (Social Proof)
- On ListingPage, show: `"Saved by [N] people"` (requires aggregated count — store in listing `metadata` via Integration API cron job, updated nightly)
- This is a Phase 1.5 feature — include as P1 but can ship after core save is live

---

### Nice to Have (P2)

- Shareable saved collection via a generated link (`/saved/share/[token]`) — Phase 2
- "Also loved by people who saved this" recommendation strip — Phase 2
- Email re-engagement: `"You left some saved items behind"` — Phase 2
- Export / share as WhatsApp-friendly list — culturally resonant for Neha persona

---

## 6. UX Requirements

### Heart Icon — Visual Design
- Icon: outlined heart (not saved) ↔ filled coral/red heart (saved). Use Mela's warm accent colour (`#D4534A` or brand coral) for filled state
- Hover state on desktop: scale 1.1 + subtle shadow
- The icon must have a `z-index` above the image and trust badges
- Position: `position: absolute; bottom: 12px; right: 12px;` within `css.imageContainer`
- The NamedLink wrapping the card must NOT capture the heart button click — use `e.stopPropagation()` on the button

### ListingCard Architecture Change
The card is currently a single `<NamedLink>` wrapping everything. To support the heart button (which must NOT navigate), we need a **structural change**:
```jsx
// Before: entire card is a NamedLink
<NamedLink ...>
  <div className={css.imageContainer}>...</div>
  <div className={css.info}>...</div>
</NamedLink>

// After: NamedLink wraps only the content areas; heart is a sibling button
<div className={css.root}>
  <NamedLink className={css.cardLink} name="ListingPage" params={{ id, slug }}>
    <div className={css.imageContainer}>...</div>
    <div className={css.info}>...</div>
  </NamedLink>
  <button className={css.heartButton} onClick={onToggleSave} aria-label={...}>
    <HeartIcon filled={isSaved} />
  </button>
</div>
```
> **Critical**: this changes the `css.root` from being on a `<a>` tag to a `<div>`. Verify keyboard navigation and accessibility. The `NamedLink` inner element handles the card-click navigation.

### Homepage "Saved" Module
- Section background: warm off-white (`#f7f4ef`) — visually distinct from adjacent white sections
- Horizontal scroll on mobile, 3-col grid on desktop (same as CategoryShowcase product grids)
- Each card shows the heart as filled (the user already saved these)
- Section animates in on first render (fade-up, 200ms) to signal freshness

### Listing Page
- Gallery heart: same position/style as card (bottom-right of main image)
- `"Save ❤️"` button: secondary button style (outlined), placed below the primary `"Shop at [Brand]"` CTA in the `OrderPanel`
- On save: button text changes to `"Saved ❤️"`, fills with coral background

### Edge Cases
| Scenario | Behaviour |
|----------|-----------|
| User saves 200 listings (cap) | Disable save button; show toast `"You've reached 200 saves — remove some to add more"` |
| Saved listing is deleted by brand | Show a placeholder card `"This item is no longer available"` with a remove button |
| Network error on save | Rollback optimistic update; show toast error |
| User signs out | Clear `savedListingIds` from Redux state (not localStorage — privacy) |
| User clicks heart before listings load | Disabled state with spinner |
| `privateData` is null/undefined on first load | Treat as empty array `[]` |

### Loading States
- Heart icon: show a small spinner in place of the icon while a save/unsave is in progress for that specific listing
- `SavedPage`: skeleton loader grid while fetching listings (same skeleton as SearchPage)
- Homepage module: do not render the section until saved listing data is fetched (prevents layout shift)

---

## 7. SEO Considerations

The `/saved` page itself is **auth-gated and personalised** — it will not be indexed by search engines and has no direct SEO value. However, the feature creates several **indirect SEO and discovery benefits**:

### 7.1 Social Sharing — Highest SEO Lever
When users share their saved collections (Phase 2), those shared pages:
- Are publicly accessible and indexable
- Generate natural backlinks (WhatsApp shared links, Instagram story links, mom-group posts)
- Neha's persona explicitly curates brand lists for WhatsApp groups — a shared collection page is a natural product-market-fit feature

### 7.2 Save Count as Social Proof → CTR Signal
- `"Saved by 47 people"` on the ListingPage signals popularity to organic search visitors
- Higher CTR and lower bounce rate from organic are indirect ranking signals

### 7.3 Schema.org `ItemList` (Phase 2)
When shared saved collection pages launch, add schema.org markup:
```json
{
  "@type": "ItemList",
  "name": "Priya's Mela Collection — Diwali picks",
  "itemListElement": [ ... ]
}
```
This makes shared collections eligible for rich results.

### 7.4 Internal Linking
- The `"❤ Saved"` Topbar link and homepage module both increase page depth for signed-in users → positive engagement signal
- Saved listing pages visited again via `/saved` → repeat organic sessions counted positively

### 7.5 What NOT to do for SEO
- Do **not** make `savedListings` in `publicData` (privacy violation + no SEO benefit)
- Do **not** index `/saved` — add `<meta name="robots" content="noindex">` to `SavedPage`
- Do **not** expose a user's saves in their public profile

---

## 8. Auth Page Recommendations

### Login Page Changes
1. **Contextual save prompt** (when `melaUnsavedItems` has ≥ 1 item in `localStorage`):
   - Add above the login form: `"Sign in to save [listing title] to your collection ❤️"`
   - Shows a small thumbnail of the item being saved — creates urgency and personal context
2. **Generic value prop** (no pending items):
   - Add a 3-bullet value prop below the page headline:
     - `❤️ Save your favourite Mela finds`
     - `🔔 Get back to items you loved, instantly`
     - `🛍️ Build your personal collection`

### Sign-up Page Changes
1. Same contextual prompt as login (above form)
2. **Post-signup redirect**: if `melaUnsavedItems` exists, after signup + email verification auto-migrate all saved items and redirect to `/saved`
3. **Social login copy**: `"Continue with Google to save your finds"` — replaces the generic `"Continue with Google"` when pending saves exist

> **UXR copy audit 2026-05-25 — `SignupPage/ValueProposition` component**: The current customer-facing `ValueProposition.js` on the signup page has two copy violations that should be corrected before this feature ships:
>
> 1. **Headline**: `"Never Lose Track of Your Favorites"` — frames signup value as retrieval/bookmarking rather than discovery. Users arrive at signup before they've found things they love. Recommended replacement: `"Your personal guide to what's new on Mela"` (discovery-forward) or `"Pick up right where you left off"` (return-visit framing, neutral enough to work at all stages).
>
> 2. **Subtitle**: `"Save and organize the Indian products you love"` — applies "Indian" at the **user identity layer** (possessive: "you love"), which this PRD explicitly prohibits (§3, copy rule). The word "Indian" describes a product origin; it should not describe a user's personal collection. Recommended replacement: `"Save the products you love — and find new ones you'll want."` The cultural identity lives in Mela's brand; it does not need to be re-imposed on the user's personal saves.
>
> These are copy-only changes (no component restructure needed) — update `en.json` keys under `SignupPage.ValueProposition.*`.

### What NOT to Change
- Do not add a dedicated save-related signup step — keep the flow minimal
- Do not require login/signup to *view* listings — only gate the save action

---

## 9. Acceptance Criteria

### Heart Icon — ListingCard
- [ ] Heart icon appears bottom-right of the image on every `ListingCard`
- [ ] Heart is hollow when listing is not saved; filled coral when saved
- [ ] Clicking the heart does NOT navigate to the listing page
- [ ] Clicking heart while logged out opens the auth modal
- [ ] Clicking heart while logged in (not saved) saves the listing and fills the heart (optimistic)
- [ ] Clicking filled heart removes the listing and hollows the heart (optimistic)
- [ ] Heart has `aria-label="Save"` / `"Remove from saved"` based on state
- [ ] Loading spinner appears in place of heart during save/unsave in progress
- [ ] Network error rolls back optimistic update and shows toast

### Heart + Button — ListingPage
- [ ] Heart icon appears bottom-right of the primary gallery image in `SectionGallery`
- [ ] `"Save ❤️"` button appears in the OrderPanel below the primary CTA
- [ ] Both the gallery heart and the button are in sync (saving via one updates the other)
- [ ] Button reads `"Saved ❤️"` (filled coral) when already saved

### Redux / Data Layer
- [ ] `savedListings` duck exists at `src/ducks/savedListings.duck.js`
- [ ] Save writes `savedListings: [newId, ...previousIds]` to `currentUser.privateData`
- [ ] Unsave writes `savedListings: [...previousIds].filter(id !== removedId)` to `currentUser.privateData`
- [ ] On app load with authenticated user, `savedListingIds` is hydrated from `currentUser.attributes.privateData.savedListings`
- [ ] Max 200 listings enforced — 201st save is blocked with toast

### Homepage "Saved" Module
- [ ] Module renders between HeroSection and CategoryShowcase for authenticated users with ≥ 1 save
- [ ] Module does NOT render for unauthenticated users
- [ ] Module does NOT render for authenticated users with 0 saves
- [ ] Shows up to 6 most-recently-saved listings as `ListingCard`s
- [ ] Footer CTA `"See all [N] saved items →"` links to `/saved`
- [ ] Section title is `"Your Saved Items"` with italic subtitle `"— meri pasand"` per §3 copy system

### Dedicated `/saved` Page
- [ ] Route `/saved` exists and renders `SavedPage`
- [ ] Unauthenticated access redirects to `/login?from=/saved`
- [ ] Shows all saved listings in a responsive grid
- [ ] Empty state renders with `"Nothing saved yet"` headline and `"your meri pasand waits"` sub-copy + browse CTA
- [ ] Each card's heart is filled; clicking removes item from list
- [ ] Unavailable listings (deleted) show a placeholder card with remove option
- [ ] Page has `<meta name="robots" content="noindex">`

### Topbar
- [ ] `"❤ Saved"` link appears in desktop Topbar when user is authenticated
- [ ] Link does NOT appear when user is logged out
- [ ] `"Saved"` appears in `TopbarMobileMenu` when user is authenticated
- [ ] Link routes to `/saved`

### Auth Page
- [ ] When `melaUnsavedItems` exists in `localStorage`, login and signup pages show contextual save prompt: `"Sign in to save [item] to your collection"` with thumbnail
- [ ] After login/signup: all pending items auto-migrate to `privateData.savedListings` and user is redirected to `/saved`

### i18n
- [ ] All user-facing strings use `FormattedMessage` with keys in `en.json`
- [ ] No hardcoded English strings in JSX

---

## 10. Success Metrics & Measurement

| Metric | GA4 Event | Parameters |
|--------|-----------|------------|
| Heart clicked (save) | `saved_save` | `listing_id`, `listing_title`, `source` (card/listingPage/gallery) |
| Heart clicked (unsave) | `saved_unsave` | `listing_id`, `source` |
| Auth modal shown (anon click) | `saved_auth_gate_shown` | `listing_id` |
| Auth modal → login CTA | `saved_auth_gate_login` | — |
| Auth modal → signup CTA | `saved_auth_gate_signup` | — |
| Homepage module rendered | `saved_homepage_module_view` | `count` (# of saved items shown) |
| Homepage module CTA click | `saved_homepage_see_all` | — |
| SavedPage viewed | `saved_page_view` | `saved_count` |
| SavedPage → listing click | `saved_listing_click` | `listing_id`, `position` |

**30-day review targets**:
- Save events per authenticated session > 0.8
- Auth gate → signup conversion > 5%
- SavedPage → listing click-through > 20%

---

## 11. Dependencies & Risks

**Performance strategy — zero impact on page load**

- `savedListingIds` (the UUID array) arrives **for free** inside the existing `fetchCurrentUser` response — no extra API call
- Heart icon state on every `ListingCard` derives from a `.includes()` check against `savedListingIds` in Redux — no network, no delay
- Listing *entity* fetches (for `SavedItemsModule` and `SavedPage`) fire in `useEffect` after initial paint — pages render fully without them; content populates into skeleton placeholders
- `SavedPage` has **no `loadData` / SSR** — entirely client-side rendered, zero server-side overhead
- `SavedItemsBanner` (anon banner) reads `localStorage` synchronously — no network, no Redux

**Dependencies**
- `sdk.currentUser.updateProfile` uses shallow merge on `privateData` — writing `{ savedListings: [...] }` only updates that key; no spread needed
- `sdk.listings.query({ ids: [...] })` supports batch ID lookup — max 100 IDs per call; paginate at >100 saves
- `ListingCard` structural refactor (§6) must not break existing `SearchPage`, `MelaHomePage` category grids, or `FeaturedBrandPartners` — run full regression on all card-rendering surfaces
- Topbar changes require updates to both `TopbarDesktop.js` and `TopbarMobileMenu.js`
- New `SavedPage` route registered in `src/routing/routeConfiguration.js` only — **not** in `pageDataLoadingAPI.js` (no SSR loadData)
- **Only `ListingPageCarousel.js` needs modification** — Mela's `configLayout.js` hardcodes `variantType: 'carousel'`, making `ListingPageCoverPhoto.js` unreachable dead code

**Risks**
| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| `privateData` size limit | Low | 200-item cap keeps payload at ~7.2KB, well within Sharetribe's 10KB limit |
| `ListingCard` structural change breaks existing tests/snapshots | High | Delete stale snapshot before running tests; treat snapshot update as deliberate commit |
| `signupWithIdp` (social login) misses localStorage migration | Medium | Add migration dispatch in BOTH `login` and `signupWithIdp` thunks — they follow different code paths |
| `MelaHomePage` test suite fails after `connect()` is added | High | Add Redux `Provider` wrapper to `MelaHomePage.test.js` — same fix as other connected containers |
| `sdk.listings.query` IDs parameter name wrong | Low | Verify against Sharetribe Flex API docs before coding `fetchSavedListings` thunk |

---

## 12. Out of Scope / Future Considerations

- **Shareable saved collections** (`/saved/share/[token]`) — Phase 2; high value for Neha's WhatsApp curation behaviour; shared pages are public and indexable (SEO benefit)
- **"Trending in Saves"** — Surface the most-saved listings on the homepage or SearchPage as social proof (`"Saved by 47 people"` — requires Integration API aggregation job)
- **Email re-engagement** — `"You left some saved items behind"` drip email sequence
- **Push notifications** (mobile PWA) — `"Back in stock: an item you saved"`
- **"People who saved this also saved..."** — cross-recommendation module on ListingPage
- **Pasand count as editorial signal** — `"Saved by 200+ Mela shoppers"` badge on listing cards for highly-saved items
- **Parent/child account** — allow grandparents to view (not edit) a child's Pasand list for gifting

---

*Last updated: 2026-04-05*
*Roadmap status: Customer Experience — previously listed as "Wishlist & favourites functionality" (Low Priority). Recommend elevating to Medium Priority given return-visit and auth-gate value.*
