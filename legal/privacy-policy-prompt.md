# Privacy Policy — Generation Prompt

Use this prompt with Termly.io, Iubenda, or a similar tool to generate Mela's Privacy Policy.
Termly.io is recommended — free tier, CCPA-compliant output, ~10 minutes.

---

## Prompt

Create a Privacy Policy for **Mela**, a personal, non-commercial project operated by an individual (not a registered business entity). Mela is a curated discovery directory for Indian brands — not a retailer, marketplace, or e-commerce store.

### Operator
- **Name**: [Your Full Name], an individual
- **Contact Email**: [your email] (or privacy@[domain] if configured)
- **Location**: [Your state], United States
- **Effective Date**: [date]
- No business entity; no LLC; no EIN

### What Data Mela Collects

| Data | How Collected | Why |
|------|---------------|-----|
| Email address | Account signup | To create and maintain user account |
| First and last name | Account signup | To personalise account experience |
| Saved products / brands | User action (save button) | To power the wishlist / saved items feature |
| Browsing behaviour (pages visited, clicks) | Analytics tools | To understand how users discover brands |
| Feedback responses | Optional in-app prompts | To improve curation and product quality |
| Session cookies | Automatically | Required for Sharetribe platform to function |

### What Mela Does NOT Collect
- Payment information (no transactions on Mela)
- Shipping addresses
- Phone numbers
- Device location
- Advertising profile data

### Third-Party Services in Use
- **Sharetribe** — backend platform; stores account data and session state
- **Google Analytics** (or Hotjar, if active) — anonymous browsing analytics; no personal data shared
- **Airtable** — optional feedback form responses
- Clicking "Shop on [Brand]" redirects to that brand's **Shopify store** — from that point, Shopify's and the brand's own privacy policy govern; Mela has no visibility into what happens on their store

### How Data Is Used
- To provide the saved items / wishlist feature
- To improve product curation and discovery
- To send transactional emails (account verification, password reset) — no marketing emails at launch
- Data is never sold to third parties
- Data is never used for advertising targeting

### Cookies
- **Essential cookies**: Required for the Sharetribe platform to function (session management, login state)
- **Analytics cookies**: Google Analytics / Hotjar — anonymous, aggregated usage data
- **No advertising cookies** at launch

### California Residents (CCPA)
Include a full CCPA section covering:
- Right to know what personal data is held
- Right to delete personal data (contact [email] to request)
- Right to opt out of sale of personal information (Mela does not sell data — state this explicitly)
- Non-discrimination: exercising rights does not affect access to the platform

### Data Retention
- Account data: retained until deletion is requested
- Saved items: deleted when account is deleted
- Anonymous analytics: retained indefinitely (no personal identifiers)
- Feedback responses: retained for product improvement; anonymised or deleted on request

### Children
- Mela is not directed at children under 13
- No knowing collection of data from children under 13

### Changes to This Policy
- Users will be notified of material changes via the platform or email
- Continued use after changes constitutes acceptance

### Contact
- For data requests, account deletion, or privacy questions: [your email]

### Tone
- Plain English
- Honest and minimal — do not over-promise ("we will never...") or under-disclose
- No language implying Mela is a company, LLC, or registered business
- No GDPR section (US-only audience at launch; add before EU expansion)

---

## After Generating

1. Paste the output into the Sharetribe CMS page at `/privacy-policy`
2. Manually add a `#cookies` anchor heading to the cookies section (footer links to `/privacy-policy#cookies`)
3. Verify the CCPA section is present and accurate
4. Remove any auto-generated GDPR, ePrivacy, or international sections
5. Set up privacy@[domain] email forwarding before publishing
