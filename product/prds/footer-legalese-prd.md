# Footer Legalese PRD

**Feature:** Terms of Service, Privacy Policy, Footer Legal Links
**Status:** ⛔ Blocked — Legal copy not yet written (as of April 2026)
**Priority:** High — Launch Blocker (legal requirement before public launch)
**Owner:** PM (copy) + Developer (footer config)

> **Action Required**: PM must generate legal copy using Termly.io (~1 day of work). See Blockers table and Recommended Tool section below. This is the only outstanding dependency — infrastructure is fully ready.

---

## Problem Statement

Mela is not yet legally covered for public launch. `/terms-of-service` and `/privacy-policy` routes exist in the codebase but contain placeholder content. The footer has no legal links. This is a launch blocker.

---

## Current State

- Routes exist: `/terms-of-service` and `/privacy-policy` are in `routeConfiguration.js` and already indexed in `sitemap-default.xml`
- Page content: **placeholder / empty** — needs real legal copy
- Footer: **CMS-driven via Sharetribe Console** (PageBuilder). No legal links currently configured.
- Both pages render correctly — the infrastructure is complete. Only content and footer links are missing.

---

## Mela's Legal Context

Mela operates as a **curated discovery directory**, not a retailer or marketplace:
- Mela does not sell products
- Mela does not process payments
- Mela does not ship goods or manage fulfillment
- Transactions happen on each brand's own Shopify store
- Mela earns no revenue and has no affiliate or referral relationships with featured brands
- Mela is operated by an individual (no LLC, no business entity) due to H-1B visa constraints

This materially limits legal exposure but does not eliminate it — a published Privacy Policy is legally required because Mela collects email addresses and uses analytics.

---

## Founder's Immigration & Incorporation Status

**Important context that governs all legal structure decisions for Mela:**

The founder is on an **H-1B visa**, which prohibits self-employment, forming an LLC as an operator, and earning income from a side business. This is not a typical startup legal risk — it is an immigration risk. A violation can affect visa status and green card proceedings.

### What this means for Mela's current phase

| Activity | Status |
|----------|--------|
| Building and sharing the product for feedback | Allowed |
| Sharing a public URL with no revenue | Allowed |
| Forming an LLC in founder's name | Not allowed |
| Signing affiliate agreements | Not allowed |
| Earning any income from Mela | Not allowed |
| Using spouse's LLC as operator | Not allowed — same immigration risk, different wrapper |

### Entity options when status changes

- **Single-member LLC** — appropriate at first revenue or formal brand partnerships
- **Add EIN + business bank account** — once LLC is formed
- **Convert to Delaware C-Corp** — only needed if raising venture capital

### Using a spouse's LLC

The founder's spouse holds an LLC for a photography business. **Using it for Mela is not recommended** for the following reasons:
- Liability contamination — a Mela dispute exposes photography business assets
- The LLC's operating agreement does not authorize marketplace/affiliate activity
- Spouse is the legal owner; founder has no formal ownership stake
- Legal pages and ToS would show the photography LLC's name
- Tax and accounting complexity from mixed business activities
- Does not resolve the H-1B compliance question

### Path forward

1. Consult an immigration attorney before taking any formal incorporation step
2. Keep Mela as a non-commercial validation project until status changes
3. Do not sign affiliate agreements or accept revenue in current status
4. Sharing a URL for feedback with no revenue and no contracts is the lowest-risk activity available now

---

## Required Legal Pages

### 1. Terms of Service — `/terms-of-service`

**Must cover:**

| Section | Content |
|---------|---------|
| Platform role | "Mela is a curated discovery directory, not a retailer. We do not sell, ship, or fulfill orders. Clicking 'Shop on [brand]' takes you to that brand's own Shopify store." |
| Operator | Individual (personal name) — no business entity due to H-1B constraints |
| User accounts | What data is stored, how to delete account, age requirement (13+) |
| Saved items | Mela saves product links on your behalf; not a purchase or reservation |
| Brand listings | Brands are editorially selected by Mela; Mela does not verify real-time accuracy of descriptions, pricing, or availability |
| No affiliate disclosure | Mela earns no commissions and has no affiliate relationships — remove any FTC affiliate disclosure language from generator output |
| Prohibited use | No scraping, fake accounts, misleading reviews |
| Limitation of liability | Mela is not responsible for product quality, delivery, or disputes on brand Shopify stores |
| Governing law | [Founder's state] — no Delaware entity, no incorporation until immigration status changes |
| Changes to terms | Right to update with notice |

### 2. Privacy Policy — `/privacy-policy`

**Must cover:**

| Section | Content |
|---------|---------|
| Data collected | Email, saved listings, browsing behavior (Hotjar), feedback responses (Airtable) |
| How it's used | To improve product discovery; not sold to third parties |
| Third-party links | Clicking to Shopify takes you off Mela; their privacy policy governs from that point |
| Cookies | Session cookies (Sharetribe), analytics (Hotjar), no advertising cookies at launch |
| CCPA rights | California residents: right to know what data is held, right to delete, no sale of personal information |
| Data retention | Account data kept until deletion request; anonymous analytics retained indefinitely |
| Contact | privacy@[domain] for data requests |

**Note:** GDPR compliance (for EU users) is not a launch requirement if Mela is targeting US users only. Add GDPR section before expanding to EU markets.

### 3. Cookie Policy

Can be a `#cookies` anchor section within Privacy Policy — no separate page needed at launch.

---

## Recommended Tool for Legal Copy

**Termly.io** — free tier generates CCPA-compliant Terms of Service and Privacy Policy in ~10 minutes. Outputs clean, embeddable HTML or plain text. Best fit for Mela's scope.

Steps:
1. Go to termly.io → Create free account
2. Add Mela's details (platform type: "marketplace/discovery", jurisdiction: US)
3. Generate ToS + Privacy Policy
4. Paste into Sharetribe CMS pages at `/terms-of-service` and `/privacy-policy`
5. Review affiliate disclosure language and platform role language manually — the generator's defaults assume a direct retailer

Alternative: **Iubenda** (similar capability, slightly more automated but less control over wording).

---

## Footer Configuration (Sharetribe Console)

Footer is configured via **Sharetribe Console → Content → Footer**. No code changes needed — this is a CMS operation.

**Footer column to add: "Legal"**

| Link Text | URL |
|-----------|-----|
| Terms of Service | `/terms-of-service` |
| Privacy Policy | `/privacy-policy` |
| Cookie Policy | `/privacy-policy#cookies` |

**Footer inline disclaimer text (add to copyright/slogan field):**
> © 2026 Mela. A curated directory of Indian brands. Mela is not a retailer — clicking through takes you to each brand's own store.

---

## Acceptance Criteria

- [ ] `/terms-of-service` has real legal content (not placeholder) — use `legal/terms-of-service-prompt.md` to generate
- [ ] `/privacy-policy` has real legal content including cookie and CCPA section — use `legal/privacy-policy-prompt.md` to generate
- [ ] ToS states Mela earns no commissions and has no affiliate relationships (no FTC affiliate disclosure)
- [ ] ToS operator is listed as individual name, not a company or LLC
- [ ] Platform disclaimer ("Mela is a curated directory, not a retailer") is present in both ToS and footer
- [ ] Footer links to both pages (configured in Sharetribe Console)
- [ ] Footer shows copyright + one-line disclaimer
- [ ] Both pages are mobile-readable at 375px
- [ ] Both pages appear in `sitemap-default.xml` (already configured — verify at `/sitemap-default.xml` after deploy)
- [ ] privacy@[domain] email address is live and monitored

---

## Blockers

| Blocker | Owner | Notes |
|---------|-------|-------|
| Legal copy must be written/generated first | PM | Use Termly.io. ~1 day of work. |
| Production domain must be confirmed | PM | Needed for privacy contact email and sitemap |
| Sharetribe Console footer configuration | PM | 30 min once copy is ready, no dev needed |
