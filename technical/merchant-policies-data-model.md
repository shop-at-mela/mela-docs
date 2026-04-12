# Merchant Policies Data Model

**Version:** 1.0
**Last Updated:** 2026-01-28
**Status:** Draft

## Overview

This document defines the data model for storing merchant return and shipping policies in Mela's platform. These policies are used for:
- Schema.org structured data (Google Rich Results)
- Customer-facing policy displays on listing pages
- Brand partner policy management

## Storage Location

Merchant policies are stored in the **provider's (brand partner's) user object** under `publicData.merchantPolicies`:

```javascript
// Sharetribe user.publicData structure
{
  merchantPolicies: {
    returnPolicy: { ... },
    shippingPolicy: { ... },
    policyContact: { ... }
  }
}
```

### Why publicData?

- **Public visibility**: Policies need to be displayed to customers
- **Per-brand customization**: Each brand can have unique policies
- **Fallback support**: Missing policies fall back to marketplace defaults
- **API accessible**: Available through Sharetribe SDK without auth

## Complete Data Schema

### Root Structure

```typescript
interface MerchantPolicies {
  returnPolicy: ReturnPolicy;
  shippingPolicy: ShippingPolicy;
  policyContact: PolicyContact;
  version?: string; // Schema version for future migrations
  lastUpdated?: string; // ISO 8601 timestamp
}
```

### Return Policy Schema

```typescript
interface ReturnPolicy {
  enabled: boolean; // Can customers return items?
  returnWindow: number; // Days from delivery
  returnFees: 'free' | 'customer-pays' | 'restocking-fee';
  restockingFeePercent?: number; // Required if returnFees = 'restocking-fee'
  returnMethod: 'mail' | 'in-store' | 'both';
  conditions: string[]; // Array of return conditions
  refundMethod: 'original-payment' | 'store-credit' | 'both';
  categoryExceptions?: CategoryReturnPolicyOverride; // Optional overrides
  excludedCategories?: string[]; // Categories not eligible for returns
  nonReturnableItems?: string[]; // Specific item types (e.g., "opened hygiene products")
}

interface CategoryReturnPolicyOverride {
  [categoryId: string]: {
    returnWindow?: number;
    returnFees?: 'free' | 'customer-pays' | 'restocking-fee';
    additionalConditions?: string[];
  };
}
```

**Example:**

```json
{
  "enabled": true,
  "returnWindow": 30,
  "returnFees": "free",
  "returnMethod": "mail",
  "conditions": [
    "Items must be unused and in original packaging",
    "Tags must be attached",
    "Proof of purchase required",
    "Return within 30 days of delivery"
  ],
  "refundMethod": "original-payment",
  "nonReturnableItems": [
    "Opened bottles or feeding products",
    "Personalized items"
  ],
  "categoryExceptions": {
    "Baby-Clothes-Accessories": {
      "returnWindow": 60,
      "additionalConditions": ["Unopened hygiene items only"]
    }
  }
}
```

### Shipping Policy Schema

```typescript
interface ShippingPolicy {
  handlingTime: TimeRange; // Time to process order
  shippingRates: ShippingRate[]; // Available shipping options
  freeShippingThreshold: number; // Cents, 0 = no threshold
  restrictions: ShippingRestrictions;
}

interface TimeRange {
  min: number;
  max: number;
  unit: 'business-days' | 'calendar-days' | 'hours';
}

interface ShippingRate {
  region: string; // 'US', 'US-CA', 'US-NY', etc.
  method: string; // 'standard', 'expedited', 'overnight', etc.
  cost: number; // Cents (0 = free)
  minOrderForFree?: number; // Cents, if applicable
  estimatedDelivery: TimeRange;
  carrier?: string; // 'USPS', 'FedEx', 'UPS', etc.
  trackingAvailable?: boolean;
}

interface ShippingRestrictions {
  shipsTo: string[]; // Country codes ['US', 'CA']
  poBox: boolean; // Ships to PO boxes?
  apo: boolean; // Ships to APO/FPO addresses?
  excludedRegions?: string[]; // State/region codes not served
}
```

**Example:**

```json
{
  "handlingTime": {
    "min": 1,
    "max": 3,
    "unit": "business-days"
  },
  "shippingRates": [
    {
      "region": "US",
      "method": "standard",
      "cost": 0,
      "minOrderForFree": 0,
      "estimatedDelivery": {
        "min": 5,
        "max": 7,
        "unit": "business-days"
      },
      "carrier": "USPS",
      "trackingAvailable": true
    },
    {
      "region": "US",
      "method": "expedited",
      "cost": 1500,
      "estimatedDelivery": {
        "min": 2,
        "max": 3,
        "unit": "business-days"
      },
      "carrier": "FedEx",
      "trackingAvailable": true
    }
  ],
  "freeShippingThreshold": 5000,
  "restrictions": {
    "shipsTo": ["US"],
    "poBox": true,
    "apo": true
  }
}
```

### Policy Contact Schema

```typescript
interface PolicyContact {
  email: string; // Required
  phone?: string; // Optional, format: "+1-555-123-4567"
  responseTime: string; // Human-readable (e.g., "24-48 hours", "Same business day")
  contactUrl?: string; // Link to contact form or support page
}
```

**Example:**

```json
{
  "email": "support@brand.com",
  "phone": "+1-555-123-4567",
  "responseTime": "24-48 hours",
  "contactUrl": "https://brand.com/contact"
}
```

## Default Policies

For brands without custom policies, use **Mela marketplace defaults**:

**File:** `web-client/src/config/defaultMerchantPolicies.js`

```javascript
export const DEFAULT_MERCHANT_POLICIES = {
  returnPolicy: {
    enabled: true,
    returnWindow: 30,
    returnFees: "free",
    returnMethod: "mail",
    conditions: [
      "Items must be unused and in original packaging",
      "Return within 30 days of delivery",
      "Proof of purchase required",
      "Original tags must be attached"
    ],
    refundMethod: "original-payment",
    nonReturnableItems: [
      "Opened bottles or feeding products",
      "Personalized or custom items"
    ]
  },
  shippingPolicy: {
    handlingTime: { min: 1, max: 3, unit: "business-days" },
    shippingRates: [
      {
        region: "US",
        method: "standard",
        cost: 0,
        minOrderForFree: 0,
        estimatedDelivery: { min: 5, max: 7, unit: "business-days" },
        carrier: "USPS",
        trackingAvailable: true
      }
    ],
    freeShippingThreshold: 0,
    restrictions: {
      shipsTo: ["US"],
      poBox: true,
      apo: true
    }
  },
  policyContact: {
    email: "support@mela-marketplace.com",
    responseTime: "24-48 hours"
  }
};
```

## Schema.org Mapping

### Mapping to MerchantReturnPolicy

```javascript
// From returnPolicy object to schema.org
{
  '@type': 'MerchantReturnPolicy',
  applicableCountry: 'US',
  returnPolicyCategory: mapReturnPolicyCategory(returnPolicy),
  merchantReturnDays: returnPolicy.returnWindow,
  returnMethod: mapReturnMethod(returnPolicy.returnMethod),
  returnFees: mapReturnFees(returnPolicy.returnFees),
  refundType: mapRefundType(returnPolicy.refundMethod)
}

// Mapping functions
function mapReturnPolicyCategory(policy) {
  if (!policy.enabled) return 'https://schema.org/MerchantReturnNotPermitted';
  if (policy.returnWindow === -1) return 'https://schema.org/MerchantReturnUnlimitedWindow';
  return 'https://schema.org/MerchantReturnFiniteReturnWindow';
}

function mapReturnMethod(method) {
  const mapping = {
    'mail': 'https://schema.org/ReturnByMail',
    'in-store': 'https://schema.org/ReturnInStore',
    'both': 'https://schema.org/ReturnByMail' // Default to mail for schema
  };
  return mapping[method] || 'https://schema.org/ReturnByMail';
}

function mapReturnFees(fees) {
  const mapping = {
    'free': 'https://schema.org/FreeReturn',
    'customer-pays': 'https://schema.org/ReturnFeesCustomerResponsibility',
    'restocking-fee': 'https://schema.org/RestockingFees'
  };
  return mapping[fees] || 'https://schema.org/FreeReturn';
}

function mapRefundType(refundMethod) {
  const mapping = {
    'original-payment': 'https://schema.org/FullRefund',
    'store-credit': 'https://schema.org/StoreCreditRefund',
    'both': 'https://schema.org/FullRefund' // Default to full refund
  };
  return mapping[refundMethod] || 'https://schema.org/FullRefund';
}
```

### Mapping to OfferShippingDetails

```javascript
{
  '@type': 'OfferShippingDetails',
  shippingRate: {
    '@type': 'MonetaryAmount',
    value: calculateShippingCost(shippingPolicy, listingPrice),
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
      minValue: shippingPolicy.handlingTime.min,
      maxValue: shippingPolicy.handlingTime.max,
      unitCode: 'DAY'
    },
    transitTime: {
      '@type': 'QuantitativeValue',
      minValue: shippingPolicy.shippingRates[0].estimatedDelivery.min,
      maxValue: shippingPolicy.shippingRates[0].estimatedDelivery.max,
      unitCode: 'DAY'
    }
  }
}
```

## Helper Utilities

**File:** `web-client/src/util/merchantPolicyHelpers.js`

```javascript
import { DEFAULT_MERCHANT_POLICIES } from '../config/defaultMerchantPolicies';

/**
 * Get merchant policies for a brand, with fallback to defaults
 */
export function getMerchantPolicies(author) {
  const customPolicies = author?.attributes?.publicData?.merchantPolicies;

  if (!customPolicies) {
    return DEFAULT_MERCHANT_POLICIES;
  }

  // Merge with defaults for any missing sections
  return {
    returnPolicy: customPolicies.returnPolicy || DEFAULT_MERCHANT_POLICIES.returnPolicy,
    shippingPolicy: customPolicies.shippingPolicy || DEFAULT_MERCHANT_POLICIES.shippingPolicy,
    policyContact: customPolicies.policyContact || DEFAULT_MERCHANT_POLICIES.policyContact
  };
}

/**
 * Calculate shipping cost based on policy and listing price
 */
export function calculateShippingCost(shippingPolicy, listingPrice) {
  const standardRate = shippingPolicy.shippingRates.find(r => r.method === 'standard');
  if (!standardRate) return 0;

  // Check if order qualifies for free shipping
  const priceInCents = listingPrice?.amount || 0;
  const threshold = shippingPolicy.freeShippingThreshold || 0;

  if (threshold > 0 && priceInCents >= threshold) {
    return 0; // Free shipping
  }

  // Check if this specific rate has free shipping threshold
  if (standardRate.minOrderForFree && priceInCents >= standardRate.minOrderForFree) {
    return 0;
  }

  return standardRate.cost / 100; // Convert cents to dollars
}

/**
 * Format return policy for schema.org
 */
export function formatReturnPolicyForSchema(returnPolicy) {
  if (!returnPolicy.enabled) {
    return {
      '@type': 'MerchantReturnPolicy',
      applicableCountry: 'US',
      returnPolicyCategory: 'https://schema.org/MerchantReturnNotPermitted'
    };
  }

  return {
    '@type': 'MerchantReturnPolicy',
    applicableCountry: 'US',
    returnPolicyCategory:
      returnPolicy.returnWindow === -1
        ? 'https://schema.org/MerchantReturnUnlimitedWindow'
        : 'https://schema.org/MerchantReturnFiniteReturnWindow',
    merchantReturnDays: returnPolicy.returnWindow,
    returnMethod: mapReturnMethod(returnPolicy.returnMethod),
    returnFees: mapReturnFees(returnPolicy.returnFees),
    refundType: mapRefundType(returnPolicy.refundMethod)
  };
}

/**
 * Format shipping policy for schema.org
 */
export function formatShippingForSchema(shippingPolicy, listingPrice) {
  const standardRate = shippingPolicy.shippingRates.find(r => r.method === 'standard')
    || shippingPolicy.shippingRates[0];

  if (!standardRate) return null;

  return {
    '@type': 'OfferShippingDetails',
    shippingRate: {
      '@type': 'MonetaryAmount',
      value: calculateShippingCost(shippingPolicy, listingPrice),
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
        minValue: shippingPolicy.handlingTime.min,
        maxValue: shippingPolicy.handlingTime.max,
        unitCode: 'DAY'
      },
      transitTime: {
        '@type': 'QuantitativeValue',
        minValue: standardRate.estimatedDelivery.min,
        maxValue: standardRate.estimatedDelivery.max,
        unitCode: 'DAY'
      }
    }
  };
}
```

## Brand-Specific Examples

### Example 1: Premium Brand with Generous Return Policy

```json
{
  "returnPolicy": {
    "enabled": true,
    "returnWindow": 60,
    "returnFees": "free",
    "returnMethod": "both",
    "conditions": [
      "Items must be in original condition",
      "Return shipping is free",
      "No questions asked"
    ],
    "refundMethod": "both"
  },
  "shippingPolicy": {
    "handlingTime": { "min": 1, "max": 2, "unit": "business-days" },
    "shippingRates": [
      {
        "region": "US",
        "method": "standard",
        "cost": 0,
        "estimatedDelivery": { "min": 3, "max": 5, "unit": "business-days" }
      }
    ],
    "freeShippingThreshold": 0
  }
}
```

### Example 2: Budget Brand with Limited Returns

```json
{
  "returnPolicy": {
    "enabled": true,
    "returnWindow": 14,
    "returnFees": "customer-pays",
    "returnMethod": "mail",
    "conditions": [
      "Unopened items only",
      "Customer pays return shipping",
      "Original packaging required"
    ],
    "refundMethod": "store-credit"
  },
  "shippingPolicy": {
    "handlingTime": { "min": 2, "max": 5, "unit": "business-days" },
    "shippingRates": [
      {
        "region": "US",
        "method": "standard",
        "cost": 695,
        "minOrderForFree": 3500,
        "estimatedDelivery": { "min": 7, "max": 10, "unit": "business-days" }
      }
    ],
    "freeShippingThreshold": 3500
  }
}
```

### Example 3: Hygiene Products (No Returns)

```json
{
  "returnPolicy": {
    "enabled": false,
    "returnWindow": 0,
    "conditions": [
      "Due to hygiene regulations, this item cannot be returned",
      "Please contact us for defective or damaged items"
    ]
  },
  "shippingPolicy": {
    "handlingTime": { "min": 1, "max": 3, "unit": "business-days" },
    "shippingRates": [
      {
        "region": "US",
        "method": "standard",
        "cost": 495,
        "estimatedDelivery": { "min": 5, "max": 7, "unit": "business-days" }
      }
    ],
    "freeShippingThreshold": 5000
  }
}
```

## Migration Guide

### Adding Policies to Existing Brands

**Script:** `product-listing-integration/scripts/migrate-brand-policies.js`

```javascript
// Pseudocode for migration script
for each brand in database:
  1. Check if merchantPolicies already exists
  2. If not, analyze brand data:
     - Check for policy hints in brand description
     - Use brand category to infer appropriate defaults
     - Generate merchantPolicies object
  3. Update user.publicData.merchantPolicies via Sharetribe API
  4. Log results for manual review
```

### Manual Policy Entry (Brand Partner Dashboard)

Future enhancement: Add policy editor to brand partner dashboard
- Form-based policy entry
- Preview how policies appear to customers
- Validation and save to publicData

## Validation Rules

```javascript
function validateMerchantPolicies(policies) {
  const errors = [];

  // Return policy validation
  if (policies.returnPolicy.enabled) {
    if (!policies.returnPolicy.returnWindow || policies.returnPolicy.returnWindow < 0) {
      errors.push('Return window must be positive');
    }
    if (policies.returnPolicy.returnFees === 'restocking-fee' &&
        !policies.returnPolicy.restockingFeePercent) {
      errors.push('Restocking fee percentage required');
    }
  }

  // Shipping policy validation
  if (!policies.shippingPolicy.shippingRates.length) {
    errors.push('At least one shipping rate required');
  }

  // Contact validation
  if (!policies.policyContact.email || !isValidEmail(policies.policyContact.email)) {
    errors.push('Valid contact email required');
  }

  return { valid: errors.length === 0, errors };
}
```

## Future Enhancements

1. **International Shipping**: Add support for international shipping rates and policies
2. **Dynamic Shipping Rates**: Integrate with shipping carriers for real-time rates
3. **Return Label Generation**: Automate return label creation
4. **Policy Versioning**: Track policy changes over time for compliance
5. **A/B Testing**: Test different policy displays for conversion optimization
6. **Localization**: Support multiple languages for policy display

## References

- [Schema.org MerchantReturnPolicy](https://schema.org/MerchantReturnPolicy)
- [Schema.org OfferShippingDetails](https://schema.org/OfferShippingDetails)
- [Google Structured Data Guidelines](https://developers.google.com/search/docs/appearance/structured-data/product)
- [FTC Guidelines on Return Policies](https://www.ftc.gov/business-guidance/resources/business-guide-ftcs-mail-internet-or-telephone-order-merchandise-rule)
