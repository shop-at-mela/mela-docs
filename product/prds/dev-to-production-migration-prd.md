# Dev-to-Production Sharetribe Migration PRD

## Document Information
- **Created**: 2026-07-30
- **Status**: 📋 Draft — first version of this checklist; no production Sharetribe environment confirmed provisioned yet (see Open Questions)
- **Owner**: Founder / Dev
- **Related docs**:
  - `mela-docs/technical/deployment/render-deployment-guide.md` (generic Render deploy walkthrough — this PRD is the migration-specific checklist that doc doesn't cover)
  - `web-client/src/config/configBrands.js` (contains the empty `production` brand-ID stub this PRD's largest checklist item resolves)
  - `mela-docs/product/prds/insights/crossshop-tracking-prd.md` (GTM/GA4/Clarity tracking — question of whether it needs a prod-specific setup lives here)

---

## Executive Summary

**Feature**: A checklist (not a feature build) for cutting `shopatmela.com` over from its current Sharetribe **dev/test** environment to a real Sharetribe **production** environment.

**Current State**: `shopatmela.com` points at a Sharetribe **dev/test** app today — this has been treated as a pseudo-production environment (live traffic runs through it), but it is not what Sharetribe considers a production marketplace. This PRD exists because that gap needs to be closed deliberately, not discovered mid-incident.

**Target Users**: Internal (Founder/Dev) — this is operational readiness work, not a user-facing feature.

**Business Objective**: Make the cutover to a real production Sharetribe environment a planned, checklist-driven event instead of an ad hoc scramble — and specifically avoid the two failure modes this research surfaced: (1) shipping with **zero brands configured** because `configBrands.js`'s production brand-ID map is currently empty, and (2) breaking the WhatsApp/social link-preview image because it's a hardcoded URL tied to the current dev environment's asset host.

**Primary Success Metrics**: This is a launch-readiness gate, not a metric-driven feature — success is "every item below is checked off and verified live on the new environment before DNS/traffic cuts over."

---

## 1. Problem Statement

### Current State
`shopatmela.com` runs against a Sharetribe environment whose Client ID (`4e0525dc-24dc-4338-950b-02715a012fee`) is configured in `web-client/.env` as the live value — the same value that `.env.development` also uses locally. There is no separate production Sharetribe app/marketplace referenced anywhere in the repo today. `configBrands.js` — the file that maps every brand shown on Mela to its Sharetribe user UUID — already anticipates a dev/production split (`brandConfigurationsByEnv.development` vs. `.production`), but the `.production` map is a **literal empty stub** (`configBrands.js:221-229` and `:257-259`): `// Add production brand UUIDs here`.

### User Pain Points
N/A directly — but the failure mode if this is done carelessly is a broken or empty-looking site for real shoppers (no brands rendering, broken share previews, checkout misconfigured).

### Business Impact of Inaction
Every day this stays undocumented is a day the actual cutover risk is invisible. If `REACT_APP_ENV` is ever set to `production` against this codebase without first populating `configBrands.js`'s production map, the homepage brand sections, `/brands` directory, and featured-product carousels go to **zero brands** — a silent, total-looking outage that has nothing to do with the new Sharetribe environment itself being broken.

---

## 2. Goals & Non-Goals

### Goals
- Provide a concrete, ordered checklist for the actual cutover, organized by what changes (Sharetribe Console setup, code/config changes, data recreation, hosting/DNS, verification).
- Flag every genuinely unknown/undocumented fact found during research as an explicit open question — not guessed at (see §8).
- Specifically resolve the two issues that prompted this PRD: the `configBrands.js` production stub, and the hardcoded social-share image URL.

### Non-Goals
- Building an automated migration/data-sync tool between dev and production Sharetribe environments — nothing in the codebase or `mela-docs` describes such a pipeline existing, and building one is out of scope for this PRD (see §8, item 5).
- Deciding *when* to cut over — this PRD is the checklist to execute once that decision is made, not the business case for making it.
- Any new feature work. If a gap below reveals a feature is missing (e.g., Sentry not configured at all), the PRD notes it as a decision point, not a build spec.

---

## 3. Migration Checklist

### 3a. Sharetribe Console setup (new production marketplace)
- [ ] Confirm whether a production Sharetribe marketplace/app has already been created in Console, or needs to be created from scratch (see Open Question 1).
- [ ] Note the new marketplace's **Client ID** and **Client Secret** — these become `REACT_APP_SHARETRIBE_SDK_CLIENT_ID` / `SHARETRIBE_SDK_CLIENT_SECRET`.
- [ ] Recreate every **hosted Console asset** the dev environment currently has configured — these are fetched at runtime per-environment and are NOT in this git repo at all (`web-client/AGENTS.md`'s own note on `appCdnAssets`): translations, branding (logo, colors, social-sharing image asset if using the Console-driven path), footer/topbar content, listing types/fields, categories, access-control rules, the analytics integration asset, minimum transaction size. Treat this as "redo the entire Console configuration pass," not a small tweak.
- [ ] Register the `sku` public-data search field on the **new** marketplace ID: `flex-cli search set --key sku --type enum --scope public -m <new-marketplace-id>` — per `render-deployment-guide.md:230-252`, skipping this silently empties the Recommended Products carousel. Easy to forget because it produces no error, just quietly-wrong behavior.
- [ ] Set up Stripe **live** keys against the new marketplace in Console (Sharetribe's Stripe integration is configured server-side in Console, not just via the `REACT_APP_STRIPE_PUBLISHABLE_KEY` env var) — confirm current live/test status first (Open Question 3).

### 3b. Environment variables (`web-client/.env` on the production host)
- [ ] `REACT_APP_SHARETRIBE_SDK_CLIENT_ID` / `SHARETRIBE_SDK_CLIENT_SECRET` → new production app credentials (currently the dev/test app's values).
- [ ] `REACT_APP_MARKETPLACE_ROOT_URL` → `https://shopatmela.com` (currently a placeholder Render URL in `.env.development`, and `localhost:3000` in the base `.env` — neither is the real production domain today).
- [ ] `REACT_APP_ENV` → confirm this is genuinely `production` on the production host (it already reads `production` in the base `.env`, but that's the same file dev currently treats as "live" — make sure the *new* host's env is distinct from whatever serves the current dev/test traffic, so both can run in parallel during cutover if needed).
- [ ] `REACT_APP_CSP` → change from `report` to `block`. `src/index.js:178` already warns production should use `block` mode; it's `report`-only everywhere today.
- [ ] `REACT_APP_STRIPE_PUBLISHABLE_KEY`, `REACT_APP_MAPBOX_ACCESS_TOKEN` / `REACT_APP_GOOGLE_MAPS_API_KEY`, `REACT_APP_SENTRY_DSN` — all blank/unset in the repo's `.env` files, meaning whatever powers maps/payments/error-tracking on the live site today is set directly in Render's dashboard and isn't visible here. **Pull the actual live values from Render before assuming what needs to change** (Open Question 3) — don't guess these from the repo.
- [ ] `REACT_APP_GTM_ID` / `REACT_APP_GA4_ID` / `REACT_APP_CLARITY_ID` — decide whether production reuses the same GTM container/GA4 property/Clarity project as today (likely fine, since these are domain-bound, not Sharetribe-environment-bound) or needs a fresh property to avoid mixing pre-launch test traffic with real production data (Open Question 4).
- [ ] `REACT_APP_SENTIMENT_WEBHOOK_URL` — same Google Sheet currently used by both `.env` and `.env.development`; decide whether production should log to a separate sheet to avoid mixing test and real sentiment data.

### 3c. Hardcoded, environment-specific values in code
- [ ] **`configBrands.js`'s `brandConfigurationsByEnv.production` map (lines 221-229) is completely empty.** Every one of the 20 brands currently in `.development` (Masilo, Baby Forest, aagghhoo, ChooseKind, SuperBottoms, Pluchi, and 14 others) needs its production Sharetribe user UUID (and featured-listing UUIDs) added here once those brands/listings exist in the new environment. **This is the single largest item in this checklist** — until it's done, setting `REACT_APP_ENV=production` makes the homepage, `/brands` directory, and featured carousels render zero brands.
- [ ] Same for `allBrandIdsByEnv.production` (lines 257-259) — also empty, also needs all 20 (or however many go live) production brand UUIDs.
- [ ] **`src/containers/MelaHomePage/MelaHomePage.js:33`** — the hardcoded `socialImage` URL (`sharetribe-assets.imgix.net/68ab648b-...`) that WhatsApp/Facebook/etc. use for the homepage link-preview. This asset lives on whatever Sharetribe account/environment it was originally uploaded through — **re-upload it (or an updated version, see the earlier conversation about sourcing a multi-product collage) to the production environment and update this literal URL.**
- [ ] **`src/containers/MelaHomePage/MelaHomePage.test.js:143`** — same URL is duplicated in a test assertion; update in lockstep or the test will assert against a now-stale URL.

### 3d. Data / content recreation
- [ ] Recreate all brand user accounts, their listings, and product images in the new production Sharetribe environment. **No automated migration path exists today** — confirm whether this happens by re-running the Shopify ingestion pipeline (`shopify-api-ingestion-prd.md`) against the new marketplace ID, or fully manual re-entry (Open Question 5 — genuinely undocumented, don't assume either way).
- [ ] Once brands/listings exist in production, populate §3c's `configBrands.js` maps with the resulting UUIDs.
- [ ] Confirm the `sku` field (§3a) is populated correctly on migrated/recreated listings, or the Recommended Products carousel silently breaks again.

### 3e. Hosting / DNS
- [ ] Confirm in the Render dashboard directly whether a second production service already exists, or whether the plan is to repoint the *existing* Render service's env vars at the new Sharetribe production app (Open Question 2 — nothing in the repo confirms either way, and the exact live hostname couldn't be independently verified from repo evidence).
- [ ] No server-side code changes are needed for the domain/CORS/CSP cutover itself — `server/apiServer.js`'s CORS and `server/csp.js`'s connect-src are both driven entirely by `REACT_APP_MARKETPLACE_ROOT_URL` / `REACT_APP_SHARETRIBE_SDK_BASE_URL` env vars, not hardcoded domains. This is purely an env-var and hosting-configuration change.
- [ ] There's no deploy step in CircleCI (`.circleci/config.yml` only runs format/test/build/audit) — deployment is Render's own auto-deploy-on-push. Confirm this same mechanism is wired up for whichever service ends up serving production.
- [ ] Confirm SSL/DNS for `shopatmela.com` actually points at whichever Render service is designated production, before or as part of cutover.

### 3f. SEO / sitemap / search console (flagged, not fully scoped here)
- [ ] If the production environment is a genuinely new deployment (new domain behavior, fresh CSP `block` mode, etc.), re-verify Google Search Console ownership and resubmit the sitemap — cross-reference with `seo-aeo-category-brand-pages-prd.md`'s existing SEO work rather than duplicating it here.

### 3g. Verification (do this before/during cutover, not after)
- [ ] Load the production build against the new Sharetribe environment in a staging-like pass (e.g., point a preview Render service or local build at the new Client ID) and confirm: homepage renders brands, `/brands` directory populates, a listing page loads and its "Shop from Brand" CTA fires `brand_clickout` correctly (per `crossshop-tracking-prd.md`), Recommended Products carousel shows results (proves the `sku` field registration worked).
- [ ] Share the production `shopatmela.com` URL on WhatsApp/iMessage/Slack and confirm the link-preview image loads (proves §3c's image re-upload worked).
- [ ] Confirm `REACT_APP_CSP=block` doesn't silently break anything that only showed up as a report-only violation before (GTM, GA4, Clarity, Stripe, Mapbox, `api.frankfurter.dev` all need to be in the CSP allowlist already — per `server/csp.js`, GTM/GA4/Clarity domains are confirmed present from the crossshop-tracking work, and `api.frankfurter.dev` (live INR→USD display rate, `src/util/liveInrRate.js`) confirmed present 2026-08-06; re-verify Stripe/Mapbox aren't newly blocked once mode flips to `block`).
- [ ] Confirm GTM Preview / GA4 DebugView / Clarity still work against the production domain (same verification pattern as `crossshop-tracking-prd.md` §6, run once against the real domain).

---

## 4. Acceptance Criteria

- [ ] Production Sharetribe marketplace exists, with all hosted Console assets (translations, branding, listing config, categories, access control, analytics asset, min transaction size) recreated.
- [ ] `sku` search field registered on the production marketplace ID.
- [ ] All production env vars set per §3b, with `REACT_APP_CSP=block`.
- [ ] `configBrands.js`'s `brandConfigurationsByEnv.production` and `allBrandIdsByEnv.production` populated with real UUIDs for every launching brand — verified non-empty and rendering on the live homepage/brands directory.
- [ ] `MelaHomePage.js:33`'s social-share image (and its test-file duplicate) point at a production-environment-hosted asset, verified by an actual WhatsApp share showing the correct preview.
- [ ] DNS/hosting confirmed pointing at the correct Render service for production traffic.
- [ ] Full verification pass (§3g) completed and documented (screenshot or log), not just assumed from the checklist being checked.

---

## 5. Success Metrics & Measurement

Not applicable in the usual sense — this PRD's "metric" is a clean cutover with no silent breakage. If useful, treat the crossshop-tracking dashboards (once pointed at production data) as the first real signal that the migration succeeded, since they'll show real session/brand_clickout volume once live traffic starts flowing through the new environment.

---

## 6. Dependencies & Risks

- **Dependency**: A production Sharetribe marketplace must exist before most of this checklist can be executed (Open Question 1).
- **Risk**: Silent brand-list emptying if `REACT_APP_ENV=production` ships before `configBrands.js`'s production maps are populated (§3c) — the highest-severity, easiest-to-miss risk this research found.
- **Risk**: Live third-party keys (Stripe, Maps, Sentry) aren't visible in this repo — assuming their current tier/values without checking Render's dashboard directly could mean shipping with the wrong keys silently (§3b).
- **Risk**: No documented data-migration process for brand/listing recreation (§3d) — likely the most time-consuming, least automatable part of this whole migration, and probably the actual long pole, not the code/config changes.

---

## 7. Out of Scope / Future Considerations

- Building an automated dev→production data-sync/migration tool.
- Deciding the business timing of the cutover.
- Any new feature work surfaced incidentally by this research (e.g., Sentry not being configured at all today is a gap, but fixing it is a separate decision, not bundled into this migration).

---

## 8. Open Questions (explicitly unverified — do not assume answers)

1. **Has a production Sharetribe marketplace/app already been created in Console?** Nothing in the repo confirms this either way.
2. **Does `shopatmela.com`'s DNS currently point at a specific named Render service, and will that same service be repointed, or will a new one be stood up?** The only Render hostname found in-repo (`mela-marketplace.onrender.com` in `.env.development`) is a placeholder/example, not confirmed as the real live hostname.
3. **What are the actual live values of `REACT_APP_STRIPE_PUBLISHABLE_KEY`, the Maps API key, and `REACT_APP_SENTRY_DSN` on the currently-live site?** All blank in this repo's `.env` files — they must be set directly in Render's dashboard, and their current test/live tier can't be verified from the codebase.
4. **Should production use the same GTM container / GA4 property / Clarity project as today, or fresh ones?** Reusing avoids setup work but mixes pre-launch test traffic with real data in the same property.
5. **What is the actual process for recreating brand accounts/listings/images in the new production Sharetribe environment?** No PRD or doc (including the Shopify ingestion PRD) describes a dev→production content migration path — confirm with whoever runs brand onboarding before assuming it's a re-run of the ingestion pipeline versus fully manual re-entry.
6. **Does the social-share image need to be re-uploaded as-is, or replaced with the multi-product collage discussed separately** (see chat history on Blotato vs. Canva for this asset) — a decision point that affects whether §3c is a straight re-upload or a small design task first.
