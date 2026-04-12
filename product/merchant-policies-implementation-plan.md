---
planStatus:
  planId: plan-merchant-policies-schema
  title: Add Merchant Return Policy and Shipping Details to Schema.org
  status: draft
  planType: feature
  priority: high
  owner: developer
  stakeholders: [SEO, Brand Partners, Product]
  tags: [seo, schema.org, google-rich-results, merchant-policies, shipping]
  created: "2026-01-28"
  updated: "2026-01-28T00:00:00.000Z"
  progress: 0
---

# Add Merchant Return Policy and Shipping Details to Schema.org

## Problem Statement

Google's Rich Result Test identified missing optional fields in our Product schema:
- `hasMerchantReturnPolicy` (on Offer object)
- `shippingDetails` (on Offer object) - **PARTIALLY IMPLEMENTED**

While these are optional fields, adding them improves:
- Search visibility and rich snippet quality
- Customer trust and transparency
- Compliance with e-commerce best practices
- Potential for better ranking in Google Shopping

**Current Status**: `shippingDetails` is partially implemented (US destination only, no rates). `hasMerchantReturnPolicy` is missing entirely.

## Goals

1. Document merchant policy data structure in mela-docs
2. Store return and shipping policies in provider's `publicData`
3. Update Offer schema to include complete `hasMerchantReturnPolicy` and `shippingDetails`
4. Display policies on listing pages following marketplace best practices
5. Support per-brand policy customization

## Data Model Design

### 1. Provider Public Data Schema

Store in `user.publicData.merchantPolicies`:

```javascript
{
  // Return Policy
  returnPolicy: {
    enabled: true,
    returnWindow: 30, // days
    returnFees: "free", // "free" | "customer-pays" | "restocking-fee"
    restockingFeePercent: 0, // if returnFees = "restocking-fee"
    returnMethod: "mail", // "mail" | "in-store" | "both"
    conditions: [
      "Unused and in original packaging",
      "Tags must be attached",
      "Proof of purchase required"
    ],
    refundMethod: "original-payment", // "original-payment" | "store-credit" | "both"
    categoryExceptions: {
      // Optional: override for specific categories
      "Baby-Clothes-Accessories": {
        returnWindow: 60,
        additionalConditions: ["Unopened hygiene items only"]
      }
    }
  },

  // Shipping Policy
  shippingPolicy: {
    handlingTime: {
      min: 1,
      max: 3,
      unit: "business-days"
    },
    shippingRates: [
      {
        region: "US",
        method: "standard",
        cost: 0, // cents, 0 = free
        minOrderForFree: 0, // cents, 0 = always free
        estimatedDelivery: {
          min: 5,
          max: 7,
          unit: "business-days"
        }
      },
      {
        region: "US",
        method: "expedited",
        cost: 1500, // $15.00
        estimatedDelivery: {
          min: 2,
          max: 3,
          unit: "business-days"
        }
      }
    ],
    freeShippingThreshold: 5000, // cents ($50), 0 = no threshold
    restrictions: {
      shipsTo: ["US"],
      poBox: true,
      apo: true
    }
  },

  // Contact for policy questions
  policyContact: {
    email: "support@brand.com",
    phone: "+1-555-123-4567", // optional
    responseTime: "24-48 hours"
  }
}
```

### 2. Default Policies

For brands without custom policies, use Mela marketplace defaults:

```javascript
// Store in web-client/src/config/defaultMerchantPolicies.js
export const DEFAULT_MERCHANT_POLICIES = {
  returnPolicy: {
    enabled: true,
    returnWindow: 30,
    returnFees: "free",
    returnMethod: "mail",
    conditions: [
      "Items must be unused and in original packaging",
      "Return within 30 days of delivery",
      "Proof of purchase required"
    ],
    refundMethod: "original-payment"
  },
  shippingPolicy: {
    handlingTime: { min: 1, max: 3, unit: "business-days" },
    shippingRates: [
      {
        region: "US",
        method: "standard",
        cost: 0,
        minOrderForFree: 0,
        estimatedDelivery: { min: 5, max: 7, unit: "business-days" }
      }
    ],
    freeShippingThreshold: 0,
    restrictions: { shipsTo: ["US"], poBox: true, apo: true }
  },
  policyContact: {
    email: "support@mela-marketplace.com",
    responseTime: "24-48 hours"
  }
};
```

## Schema.org Implementation

### Updated Offer Object Structure

```javascript
offers: {
  '@type': 'Offer',
  url: productURL,
  ...priceForSchemaMaybe(price),
  availability: schemaAvailability,

  // Seller information
  seller: {
    '@type': 'Organization',
    name: brandName || marketplaceName,
    description: `Authentic Indian baby products brand${brandName ? ' available on Mela marketplace' : ''}`
  },

  // ENHANCED: Complete shipping details
  shippingDetails: {
    '@type': 'OfferShippingDetails',
    shippingRate: {
      '@type': 'MonetaryAmount',
      value: shippingCost, // from merchantPolicies.shippingPolicy.shippingRates[0].cost / 100
      currency: 'USD'
    },
    shippingDestination: {
      '@type': 'DefinedRegion',
      addressCountry: 'US'
    },
    deliveryTime: {
      '@type': 'ShippingDeliveryTime',
      handlingTime: {
        '@type': 'QuantitativeValue',
        minValue: handlingTimeMin,
        maxValue: handlingTimeMax,
        unitCode: 'DAY'
      },
      transitTime: {
        '@type': 'QuantitativeValue',
        minValue: deliveryTimeMin,
        maxValue: deliveryTimeMax,
        unitCode: 'DAY'
      }
    }
  },

  // NEW: Merchant return policy
  hasMerchantReturnPolicy: {
    '@type': 'MerchantReturnPolicy',
    applicableCountry: 'US',
    returnPolicyCategory: 'https://schema.org/MerchantReturnFiniteReturnWindow',
    merchantReturnDays: returnWindow,
    returnMethod: 'https://schema.org/ReturnByMail',
    returnFees: returnFeesSchema, // https://schema.org/FreeReturn or ReturnFeesCustomerResponsibility
    refundType: 'https://schema.org/FullRefund'
  }
}
```

### Schema.org Enums Reference

```javascript
// Return Policy Categories
- 'https://schema.org/MerchantReturnFiniteReturnWindow' // 30-day return
- 'https://schema.org/MerchantReturnNotPermitted' // No returns
- 'https://schema.org/MerchantReturnUnlimitedWindow' // Unlimited returns

// Return Methods
- 'https://schema.org/ReturnByMail'
- 'https://schema.org/ReturnInStore'

// Return Fees
- 'https://schema.org/FreeReturn'
- 'https://schema.org/ReturnFeesCustomerResponsibility'
- 'https://schema.org/RestockingFees'

// Refund Types
- 'https://schema.org/FullRefund'
- 'https://schema.org/StoreCreditRefund'
```

## UI/UX Implementation

### Display Location Strategy

Following marketplace best practices (Amazon, Etsy, eBay):

**Option A: Policy Accordion in Order Panel** (RECOMMENDED)
- Location: Above or below "Contact Seller" in OrderPanel
- Format: Expandable accordion sections
- Sections: "Shipping & Returns", "Return Policy", "Contact"
- Benefit: Policies visible during purchase decision

**Option B: Author/Seller Section Enhancement**
- Location: In `<section id="author">`
- Format: Tabs or collapsible sections under seller info
- Benefit: Groups all seller-related information together

**Recommendation**: Implement **Option A** for visibility during purchase flow, with link to full policies in footer.

### Component Structure

```jsx
// New component: PolicyInformation.js
<PolicyInformation
  returnPolicy={merchantPolicies.returnPolicy}
  shippingPolicy={merchantPolicies.shippingPolicy}
  policyContact={merchantPolicies.policyContact}
  listingPrice={price}
  displayMode="accordion" // or "tabs"
  className={css.policySection}
/>
```

### Visual Design Elements

1. **Shipping Section**
   - Free shipping badge (if applicable)
   - Estimated delivery range
   - Handling time notice
   - Expedited shipping options (if available)

2. **Return Policy Section**
   - Return window highlighted (e.g., "30-day returns")
   - Return conditions as bulleted list
   - Restocking fee notice (if applicable)
   - Return shipping cost indicator

3. **Icons & Visual Cues**
   - ✓ Free shipping icon
   - ↩ Return policy icon
   - 📦 Shipping/delivery icon
   - Trust indicators (e.g., "Hassle-free returns")

### Mobile Considerations
- Collapsible by default on mobile
- Sticky CTA button doesn't obscure policy info
- Touch-friendly accordion controls

## Implementation Steps

### Phase 1: Documentation & Data Model (Week 1)
1. ✅ Create plan document (this file)
2. Create `mela-docs/technical/merchant-policies-data-model.md`
   - Document complete data schema
   - Include JSON examples for each brand type
   - Add migration guide for existing brands
3. Create `mela-docs/product/merchant-policies-ui-spec.md`
   - UI mockups for policy display
   - User flow for policy editing (brand partner dashboard)
   - Customer-facing policy page designs

### Phase 2: Backend Implementation (Week 2)
4. Add default policies config: `web-client/src/config/defaultMerchantPolicies.js`
5. Create policy helper utilities: `web-client/src/util/merchantPolicyHelpers.js`
   - `getMerchantPolicies(author)` - fetch from author publicData with defaults fallback
   - `formatShippingForSchema(shippingPolicy)` - convert to schema.org format
   - `formatReturnPolicyForSchema(returnPolicy)` - convert to schema.org format
   - `calculateShippingCost(shippingPolicy, listingPrice)` - handle free shipping thresholds
6. Update ListingPage.shared.js to include policy schema helpers

### Phase 3: Schema.org Updates (Week 2)
7. Update `ListingPageCoverPhoto.js` offers object
   - Add complete `shippingDetails` with rates and timing
   - Add `hasMerchantReturnPolicy` object
   - Test with Google Rich Results Test
8. Update `ListingPageCarousel.js` offers object (same changes)
9. Add policy schema to other product listings (CategoryShowcase, RecommendedProducts if applicable)

### Phase 4: UI Component Development (Week 3)
10. Create `PolicyInformation` component
    - Shipping details display
    - Return policy display
    - Contact information
    - Responsive design
11. Create `PolicyAccordion` component (if using accordion pattern)
12. Add styles: `PolicyInformation.module.css`
13. Update OrderPanel to include PolicyInformation component
14. Optional: Add policy summary to SectionAuthorMaybe

### Phase 5: Brand Migration & Testing (Week 4)
15. Create migration script: `product-listing-integration/scripts/migrate-brand-policies.js`
    - Parse existing brand data for policy hints
    - Generate `merchantPolicies` object for each brand
    - Update user publicData via Sharetribe API
16. Document policy editing process for brand partners
17. Test Rich Results on staging
18. User acceptance testing with brand partners

### Phase 6: Launch & Monitor
19. Deploy to production
20. Monitor Google Search Console for Rich Results improvements
21. Collect brand partner feedback
22. Monitor customer questions about policies (should decrease)

## File Structure

```
mela-docs/
└── technical/
    └── merchant-policies-data-model.md (NEW)
└── product/
    └── merchant-policies-ui-spec.md (NEW)

web-client/src/
├── config/
│   └── defaultMerchantPolicies.js (NEW)
├── util/
│   └── merchantPolicyHelpers.js (NEW)
├── components/
│   ├── PolicyInformation/
│   │   ├── PolicyInformation.js (NEW)
│   │   ├── PolicyInformation.module.css (NEW)
│   │   └── PolicyAccordion.js (NEW)
├── containers/
│   └── ListingPage/
│       ├── ListingPageCoverPhoto.js (MODIFY - offers schema)
│       └── ListingPageCarousel.js (MODIFY - offers schema)

product-listing-integration/scripts/
└── migrate-brand-policies.js (NEW)
```

## Success Metrics

1. **Technical**
   - Google Rich Results Test passes with no warnings for merchant policies
   - Schema validation passes on schema.org validator
   - No console errors on listing pages

2. **SEO**
   - Improved rich snippet display in Google Search
   - Increased click-through rate from search results
   - Better ranking for product queries (track over 30 days)

3. **User Experience**
   - Reduced customer inquiries about shipping/returns (target: 20% decrease)
   - Increased conversion rate on listing pages (target: 5-10% increase)
   - Positive brand partner feedback on policy management

4. **Business**
   - All brand partners have policies configured (100% coverage)
   - Policies display correctly on 100% of listings
   - Mobile and desktop UX scores maintained or improved

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Brand partners have non-standard policies | Medium | Use flexible schema with category exceptions |
| Schema changes break existing SEO | High | Test thoroughly in staging, gradual rollout |
| UI adds clutter to listing page | Medium | Use collapsible/accordion pattern, A/B test |
| Migration script errors | High | Dry-run mode, manual review before production |
| Increased page load time | Medium | Lazy load policy component, optimize schema size |

## Dependencies

- Sharetribe API access for user publicData updates
- Brand partner coordination for policy collection
- Design approval for UI components
- Google Search Console access for monitoring

## Open Questions

1. Should we allow category-specific policies (e.g., different return windows for clothing vs. toys)?
   - **Recommendation**: Yes, add `categoryExceptions` object

2. Do we need international shipping policies now, or US-only?
   - **Recommendation**: Start with US-only, add international later

3. Should policies be required for all brands, or optional with defaults?
   - **Recommendation**: Optional with marketplace defaults fallback

4. Where should brand partners edit their policies?
   - **Recommendation**: Add to brand partner dashboard settings (future enhancement)

## Related Resources

- [Google Merchant Return Policy Schema](https://schema.org/MerchantReturnPolicy)
- [Google Shipping Details Schema](https://schema.org/OfferShippingDetails)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [E-commerce Best Practices - Return Policies](https://www.shopify.com/blog/return-policy)
- Amazon, Etsy, eBay policy display patterns (reference for UX)

## Notes

- Current implementation already has partial `shippingDetails` (US destination only)
- Focus on completing shipping details + adding return policy
- Consider A/B testing policy placement (OrderPanel vs Author section)
- Document policy schema in mela-docs for future brand onboarding
