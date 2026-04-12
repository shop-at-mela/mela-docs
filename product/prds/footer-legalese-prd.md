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

Mela operates as a **discovery and affiliate platform**, not a retailer:
- Mela does not sell products directly
- Mela does not process payments
- Mela does not ship goods or manage fulfillment
- Transactions happen on each brand's Shopify store
- Mela earns through affiliate/referral relationships with brands

This materially limits legal exposure but does not eliminate it.

---

## Required Legal Pages

### 1. Terms of Service — `/terms-of-service`

**Must cover:**

| Section | Content |
|---------|---------|
| Platform role | "Mela is a product discovery platform, not a retailer. We do not sell, ship, or fulfill orders. Clicking 'Shop from [brand]' takes you to a third-party Shopify store." |
| User accounts | What data is stored, how to delete account, age requirement (13+) |
| Saved items | Mela saves product links on your behalf; not a purchase or reservation |
| Brand listings | Listings are submitted by brands; Mela does not verify accuracy of descriptions, pricing, or availability |
| Affiliate disclosure | Mela may earn a commission when you purchase through links (FTC requirement) |
| Prohibited use | No scraping, fake accounts, misleading reviews |
| Limitation of liability | Mela is not responsible for product quality, delivery, or disputes on Shopify stores |
| Governing law | Recommend: Delaware |
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
> © 2026 Mela. A discovery platform for sustainable Indian brands. Mela is not a retailer — products are sold by independent brands on their own Shopify stores.

---

## Acceptance Criteria

- [ ] `/terms-of-service` has real legal content (not placeholder)
- [ ] `/privacy-policy` has real legal content including cookie and CCPA section
- [ ] Affiliate disclosure is present in ToS (FTC requirement)
- [ ] Platform disclaimer ("Mela is not a retailer") is present in both ToS and footer
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
