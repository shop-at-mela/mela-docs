# AI-Ready Product Discovery PRD

## Document Information
- **Created**: 2025-12-11
- **Status**: Draft
- **Owner**: Product Team
- **Related Docs**:
  - `product-data/item-aspects-analysis.md`
  - `legal/terms-of-service-prompt.md`
  - `product/homepage/seo-optimization-summary.md`

---

## Executive Summary

Implement Schema.org structured data and consumer-friendly product attributes across Mela's product and category pages to optimize for both AI shopping assistants (AEO - AI Engine Optimization) and traditional search engines (SEO). This enhancement will enable LLM-powered shopping tools (ChatGPT, Claude, Perplexity) to discover, understand, and recommend Mela products to parents searching for organic baby clothing.

**The Problem**: Current e-commerce sites (including competitors like ShopEthnos) use merchant language and lack structured data, making them invisible to AI shopping assistants. Parents ask "What's the safest organic cotton onesie for a newborn?" and AI can't surface Mela products because we don't provide machine-readable, consumer-friendly data.

**The Solution**: Transform Mela's product catalog from merchant-centric to AI-ready by implementing Schema.org structured data, translating technical terms to parent-friendly language, and exposing granular product attributes (fabric composition, certifications, safety standards).

---

## Goals & Success Metrics

### Primary Goals
1. **AI Discoverability**: Enable AI shopping assistants to find and recommend Mela products
2. **Consumer Language**: Replace merchant jargon with parent-friendly terminology
3. **Structured Data**: Implement Schema.org JSON-LD across all product pages
4. **Granular Attributes**: Expose ingredient-level product details (fabric %, certifications, origin)

### Success Metrics
| Metric | Baseline | Target (3 months) | Measurement |
|--------|----------|-------------------|-------------|
| Schema.org Validation | 0% pages | 100% product/category pages | Google Rich Results Test |
| AI Assistant Discovery | 0 products indexed | 80%+ catalog discoverable | Manual AI queries |
| Organic Search Traffic | TBD | +40% from product pages | Google Analytics |
| Parent Engagement | TBD | +25% time on product pages | Hotjar/Analytics |
| Conversion Rate | TBD | +15% from organic search | Sharetribe Analytics |

### Key Results
- All product pages pass Schema.org validation
- AI assistants (ChatGPT, Claude, Perplexity) can answer parent queries with Mela products
- 100% of product attributes use consumer-friendly language
- Parent feedback shows improved understanding of product benefits

---

## Background & Context

### Market Insight: Merchant vs Consumer Language

From LinkedIn analysis (reference: conversation context):

**Merchant Language** (current state):
- "GOTS certified organic cotton jersey bodysuit with envelope neckline"
- "Bamboo rayon blend with moisture-wicking properties"
- "Handloom woven kala cotton dungaree set"

**Consumer Language** (AI-ready state):
- "Soft organic cotton onesie - GOTS certified for baby's sensitive skin"
- "Breathable bamboo fabric that keeps baby dry and comfortable"
- "Traditional Indian cotton overalls - handcrafted, chemical-free"

AI shopping assistants need:
1. **Structured data** (Schema.org) to parse product information
2. **Consumer terminology** to match parent search queries
3. **Granular details** (fabric %, certifications, safety) for comparison
4. **Context** (age appropriateness, use cases, care instructions)

### Competitive Analysis

**ShopEthnos.com** (ethnic fashion marketplace):
- ❌ No Schema.org structured data
- ❌ Uses merchant jargon: "Zari lining", "Handloom weaving border"
- ❌ No granular fabric composition
- ❌ Certifications buried in descriptions
- ✅ Has customer reviews and social proof
- ✅ Multi-currency and international shipping

**Mela's Advantages** (from codebase analysis):
- ✅ TrustBadges component ready (`ListingCard.js:35-66`)
- ✅ ConversionBadges component ready (`ListingCard.js:78-99`)
- ✅ SEO-optimized alt text generation (`ListingCard.js:164-188`)
- ✅ Parent-friendly terminology framework (`item-aspects-analysis.md`)
- ✅ Flexible publicData structure (Sharetribe)
- ⏳ Schema.org implementation (this PRD)

### Strategic Positioning

Mela is positioned to be the **first baby fashion marketplace optimized for AI shopping assistants**. This creates:
- **Competitive moat**: Early mover advantage in AEO
- **Brand authority**: "The marketplace AI trusts for baby clothing"
- **Customer acquisition**: Organic discovery through AI tools
- **Partner value**: Brands benefit from AI-driven visibility

---

## In Scope

### Pages & Components

1. **Product Listing Pages** (`src/containers/ListingPage/`)
   - Schema.org Product markup
   - Enhanced publicData display
   - Consumer-friendly attribute labels
   - Structured certifications section
   - Care instructions in plain language

2. **Category/Search Pages** (`src/containers/SearchPage/`)
   - Schema.org ItemList markup
   - Category-level attributes (age groups, materials, certifications)
   - Filter labels in consumer language

3. **Brand/Provider Pages** (`src/containers/ProfilePage/`)
   - Schema.org Organization markup
   - Brand story and values
   - Certification showcase
   - Product collection context

4. **Homepage Featured Products** (`src/containers/LandingPage/`)
   - Schema.org CollectionPage markup
   - Featured collections with structured data

5. **Components to Update**
   - `ListingCard.js` - Add schema data attributes
   - `ListingImage.js` - Enhanced alt text with structured context
   - `PriceMaybe.js` - Schema.org Offer markup
   - `TrustBadges.js` - Link to certification details
   - `ConversionBadges.js` - Add urgency context

### Data & Attributes

From `item-aspects-analysis.md` implementation:

**High-Priority Attributes** (MUST implement):
1. **Material** - Consumer-friendly fabric names
   - Merchant: "100% GOTS certified organic cotton jersey"
   - Consumer: "Soft organic cotton (GOTS certified) - gentle on baby's skin"

2. **Certifications** - Trust signals
   - GOTS Certified
   - Non-toxic AZO-free dyes
   - BPA Free
   - BIS Approved (India)
   - Oeko-Tex Standard 100

3. **Age Group** - Clear targeting
   - Merchant: "0-6m", "6-12m"
   - Consumer: "Newborn (0-3 months)", "Baby (3-6 months)"

4. **Safety Features** - Parent priorities
   - "No small parts (choking hazard free)"
   - "Nickel-free snaps"
   - "Flame retardant free"

5. **Care Instructions** - Practical guidance
   - Merchant: "Machine wash cold, tumble dry low"
   - Consumer: "Easy care: Machine washable, no special treatment needed"

**Medium-Priority Attributes**:
- Product dimensions (chest, length, sleeve)
- Weight/fabric GSM
- Origin (Made in India)
- Sustainability story
- Artisan/craft details

### Technical Implementation

1. **Schema.org JSON-LD Scripts**
   ```javascript
   // Add to ListingPage.duck.js or new schema.js utility
   {
     "@context": "https://schema.org",
     "@type": "Product",
     "name": "Organic Cotton Bodysuit - Newborn",
     "description": "Soft GOTS certified organic cotton onesie...",
     "brand": {
       "@type": "Brand",
       "name": "Aagghhoo"
     },
     "material": "100% Organic Cotton (GOTS Certified)",
     "offers": {
       "@type": "Offer",
       "price": "24.99",
       "priceCurrency": "USD",
       "availability": "https://schema.org/InStock",
       "seller": {
         "@type": "Organization",
         "name": "Mela"
       }
     },
     "aggregateRating": {
       "@type": "AggregateRating",
       "ratingValue": "4.8",
       "reviewCount": "127"
     },
     "additionalProperty": [
       {
         "@type": "PropertyValue",
         "name": "Certification",
         "value": "GOTS Certified"
       },
       {
         "@type": "PropertyValue",
         "name": "Age Group",
         "value": "Newborn (0-3 months)"
       },
       {
         "@type": "PropertyValue",
         "name": "Care Instructions",
         "value": "Machine washable, gentle cycle"
       }
     ]
   }
   ```

2. **Meta Tags Enhancement**
   ```html
   <!-- Product-specific meta tags -->
   <meta name="product:material" content="Organic Cotton" />
   <meta name="product:certification" content="GOTS" />
   <meta name="product:age_group" content="Newborn" />
   <meta name="product:origin" content="Made in India" />
   ```

3. **publicData Structure Expansion**
   ```javascript
   publicData: {
     // Existing
     category: "clothing",
     age_group: "0-3m",
     certification: ["gots_certified", "non_toxic_dyes"],

     // New: Consumer-friendly mappings
     consumer_language: {
       material: "Soft organic cotton - GOTS certified for baby's sensitive skin",
       age_group_display: "Newborn (0-3 months)",
       safety_features: [
         "No small parts - choking hazard free",
         "Nickel-free snaps",
         "Non-toxic dyes"
       ],
       care_simple: "Easy care: Machine washable, no special treatment needed"
     },

     // New: Granular details
     fabric_composition: {
       primary_material: "Organic Cotton",
       percentage: 100,
       certification: "GOTS",
       origin: "India",
       weave_type: "Jersey knit"
     },

     // New: Safety & compliance
     safety: {
       certifications: ["GOTS", "Oeko-Tex Standard 100"],
       testing_standards: ["BIS IS 11871"],
       age_appropriate: true,
       choking_hazards: false,
       small_parts: false
     }
   }
   ```

---

## Out of Scope

### Phase 2 (Future PRDs)
- User-generated reviews with Schema.org Review markup
- Video content with VideoObject schema
- Recipe/How-to guides (e.g., "How to swaddle a newborn")
- Q&A section with FAQPage schema
- Size guide wizard with structured data
- Comparison tool with Schema.org comparison tables

### Not Included
- Changes to checkout flow
- Payment processing modifications
- Inventory management system updates
- Email marketing templates
- Mobile app (web-only for now)
- Affiliate tracking system changes

---

## User Stories & Requirements

### Parent (Primary User)

**User Story 1: AI Assistant Discovery**
> "As a new parent, I want to ask ChatGPT 'What's the safest organic cotton bodysuit for a newborn with sensitive skin?' and get Mela products recommended, so I can trust the AI's suggestions based on certifications and parent reviews."

**Acceptance Criteria:**
- ✅ ChatGPT/Claude can parse Mela product data via Schema.org
- ✅ Product appears in AI results for relevant queries
- ✅ AI accurately describes product benefits in parent-friendly language
- ✅ Certifications (GOTS, non-toxic) are highlighted
- ✅ Direct link to product page provided

**User Story 2: Clear Product Information**
> "As a parent shopping for baby clothes, I want to understand what 'GOTS certified' means and why it matters, without reading technical jargon, so I can make informed decisions quickly."

**Acceptance Criteria:**
- ✅ Consumer-friendly labels replace technical terms
- ✅ Hover/tooltip explains certifications in plain language
- ✅ Benefits clearly stated ("gentle on baby's sensitive skin")
- ✅ No merchant jargon (e.g., "jersey knit" explained as "soft, stretchy fabric")

**User Story 3: Safety Confidence**
> "As a safety-conscious parent, I want to see exactly what safety standards and certifications a product meets, so I can trust it's safe for my baby."

**Acceptance Criteria:**
- ✅ Dedicated "Safety & Certifications" section visible
- ✅ All relevant certifications listed with explanations
- ✅ Safety features called out (e.g., "No small parts - choking hazard free")
- ✅ Testing standards referenced (e.g., "BIS IS 11871 compliant")

### Brand Partner (Secondary User)

**User Story 4: Visibility in AI Search**
> "As a baby clothing brand, I want my products to appear when parents use AI shopping assistants, so I can reach customers discovering products through ChatGPT/Claude."

**Acceptance Criteria:**
- ✅ Brand name appears in Schema.org markup
- ✅ Brand story and values included in structured data
- ✅ AI assistants can recommend brand-specific products
- ✅ Brand certifications prominently displayed

### Search Engine Crawler (System User)

**User Story 5: Structured Data Indexing**
> "As a search engine crawler (Google, Bing), I want to find Schema.org structured data on Mela pages, so I can create rich search results with product details, ratings, and pricing."

**Acceptance Criteria:**
- ✅ Valid Schema.org JSON-LD on every product page
- ✅ Passes Google Rich Results Test
- ✅ Product, Offer, Brand, and Organization schemas present
- ✅ All required properties included (name, image, description, price)

---

## Technical Requirements

### 1. Schema.org Implementation

#### Product Page Schema (Priority: P0)

**Required Schema Types:**
- `Product` - Core product information
- `Offer` - Pricing and availability
- `Brand` - Brand/seller information
- `AggregateRating` - Reviews and ratings (when available)

**Implementation Location:**
- File: `src/containers/ListingPage/ListingPage.js`
- Method: Server-side rendering via Helmet or next/head equivalent
- Format: JSON-LD script tag in `<head>`

**Example Implementation:**
```javascript
// src/containers/ListingPage/ListingPageSchema.js
export const generateProductSchema = (listing, currentUser) => {
  const { title, description, price, publicData, images } = listing.attributes;
  const { author } = listing;

  return {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": title,
    "description": description || publicData.consumer_language?.material,
    "image": images.map(img => img.attributes.variants.default.url),
    "brand": {
      "@type": "Brand",
      "name": author.attributes.profile.displayName,
      "logo": author.profileImage?.attributes.variants['square-small']?.url
    },
    "offers": {
      "@type": "Offer",
      "url": `${config.canonicalRootURL}/l/${listing.id.uuid}/${createSlug(title)}`,
      "priceCurrency": price.currency,
      "price": price.amount / 100,
      "availability": "https://schema.org/InStock",
      "priceValidUntil": new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      "seller": {
        "@type": "Organization",
        "name": author.attributes.profile.displayName
      }
    },
    "material": publicData.consumer_language?.material || publicData.fabric_composition?.primary_material,
    "additionalProperty": [
      ...publicData.certification?.map(cert => ({
        "@type": "PropertyValue",
        "name": "Certification",
        "value": certificationLabels[cert] || cert
      })) || [],
      {
        "@type": "PropertyValue",
        "name": "Age Group",
        "value": publicData.consumer_language?.age_group_display || publicData.age_group
      },
      {
        "@type": "PropertyValue",
        "name": "Origin",
        "value": publicData.fabric_composition?.origin || "Made in India"
      }
    ]
  };
};
```

#### Category/Search Page Schema (Priority: P1)

**Required Schema Types:**
- `ItemList` - List of products
- `BreadcrumbList` - Navigation context

**Implementation Location:**
- File: `src/containers/SearchPage/SearchPage.js`
- Render: Dynamically based on search results

**Example:**
```javascript
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Organic Baby Clothing",
  "description": "Safe, certified organic clothing for babies and toddlers",
  "numberOfItems": searchResults.length,
  "itemListElement": searchResults.map((listing, index) => ({
    "@type": "ListItem",
    "position": index + 1,
    "url": `${config.canonicalRootURL}/l/${listing.id.uuid}/${createSlug(listing.attributes.title)}`,
    "name": listing.attributes.title,
    "image": listing.attributes.images[0]?.attributes.variants.default.url
  }))
}
```

#### Brand/Provider Page Schema (Priority: P1)

**Required Schema Types:**
- `Organization` - Brand information
- `CollectionPage` - Brand's product collection

**Implementation Location:**
- File: `src/containers/ProfilePage/ProfilePage.js`

### 2. Consumer Language Mapping

#### Translation Dictionary (Priority: P0)

**File**: `src/util/consumerLanguage.js`

```javascript
export const CONSUMER_LANGUAGE_MAP = {
  // Materials
  materials: {
    'organic_cotton': 'Soft organic cotton - GOTS certified for baby\'s sensitive skin',
    'bamboo': 'Breathable bamboo fabric that keeps baby dry and comfortable',
    'cotton_jersey': 'Soft, stretchy cotton that moves with your baby',
    'kala_cotton': 'Traditional Indian cotton - handcrafted, chemical-free',
    'muslin': 'Lightweight, breathable fabric perfect for warm weather'
  },

  // Age Groups
  age_groups: {
    '0-3m': 'Newborn (0-3 months)',
    '3-6m': 'Baby (3-6 months)',
    '6-12m': 'Baby (6-12 months)',
    '12-18m': 'Toddler (12-18 months)',
    'premie': 'Premature Baby'
  },

  // Certifications
  certifications: {
    'gots_certified': {
      label: 'GOTS Certified',
      explanation: 'Global Organic Textile Standard - guarantees organic fibers and safe processing',
      consumer_benefit: 'Safe for baby\'s sensitive skin, no harmful chemicals'
    },
    'non_toxic_dyes': {
      label: 'Non-Toxic Dyes',
      explanation: 'AZO-free dyes that won\'t harm your baby',
      consumer_benefit: 'Colors won\'t irritate skin or fade after washing'
    },
    'bpa_free': {
      label: 'BPA Free',
      explanation: 'No harmful plastics in buttons, snaps, or zippers',
      consumer_benefit: 'Safe if baby chews on closures'
    },
    'oeko_tex': {
      label: 'Oeko-Tex Standard 100',
      explanation: 'Tested for harmful substances',
      consumer_benefit: 'Independently verified safe for babies'
    }
  },

  // Features
  features: {
    'envelope_neckline': 'Easy-dress neckline (stretches wide for quick changes)',
    'snap_closure': 'Snap buttons for easy diaper changes',
    'two_way_zipper': 'Two-way zipper for quick diaper access',
    'built_in_footies': 'Built-in feet to keep baby warm',
    'adjustable_straps': 'Adjustable to grow with your baby',
    'raglan_sleeves': 'Flexible shoulder seams for easy movement',
    'boxy_style': 'Loose, comfortable fit'
  },

  // Care Instructions
  care: {
    'machine_wash_cold': 'Machine washable - gentle cycle',
    'tumble_dry_low': 'Tumble dry on low heat or air dry',
    'hand_wash': 'Hand wash recommended for longevity',
    'dry_clean': 'Professional dry cleaning recommended',
    'no_bleach': 'Do not bleach',
    'iron_low': 'Iron on low heat if needed'
  }
};

// Helper function
export const translateToConsumerLanguage = (field, value) => {
  const map = CONSUMER_LANGUAGE_MAP[field];
  if (!map) return value;

  if (typeof map[value] === 'string') {
    return map[value];
  }

  if (typeof map[value] === 'object') {
    return map[value];
  }

  return value;
};
```

#### Component Updates (Priority: P0)

**ListingCard.js Updates:**
```javascript
// src/components/ListingCard/ListingCard.js

import { translateToConsumerLanguage } from '../../util/consumerLanguage';

// In component render
const materialDisplay = publicData.consumer_language?.material ||
  translateToConsumerLanguage('materials', publicData.material);

const ageGroupDisplay = publicData.consumer_language?.age_group_display ||
  translateToConsumerLanguage('age_groups', publicData.age_group);

// Enhanced TrustBadges with tooltips
const TrustBadges = ({ certifications }) => {
  return (
    <div className={css.trustBadges}>
      {certifications.map(cert => {
        const certData = translateToConsumerLanguage('certifications', cert);
        return (
          <span
            key={cert}
            className={css.badge}
            title={certData.explanation}
            aria-label={`${certData.label}: ${certData.consumer_benefit}`}
          >
            {certData.label}
          </span>
        );
      })}
    </div>
  );
};
```

### 3. Meta Tags Enhancement

#### Open Graph & Twitter Cards (Priority: P1)

**File**: `src/containers/ListingPage/ListingPage.js` (Helmet section)

```javascript
<Helmet>
  {/* Existing meta tags */}
  <title>{title} - Mela</title>
  <meta name="description" content={description} />

  {/* Enhanced product-specific meta */}
  <meta name="product:material" content={publicData.fabric_composition?.primary_material} />
  <meta name="product:certification" content={publicData.certification?.join(', ')} />
  <meta name="product:age_group" content={publicData.consumer_language?.age_group_display} />
  <meta name="product:origin" content={publicData.fabric_composition?.origin} />
  <meta name="product:safety" content={publicData.safety?.certifications?.join(', ')} />

  {/* Open Graph enhancements */}
  <meta property="og:type" content="product" />
  <meta property="og:title" content={title} />
  <meta property="og:description" content={publicData.consumer_language?.material} />
  <meta property="og:image" content={firstImage?.attributes.variants.default.url} />
  <meta property="og:url" content={canonicalUrl} />
  <meta property="product:price:amount" content={price.amount / 100} />
  <meta property="product:price:currency" content={price.currency} />
  <meta property="product:availability" content="in stock" />
  <meta property="product:brand" content={author.attributes.profile.displayName} />

  {/* Twitter Card */}
  <meta name="twitter:card" content="product" />
  <meta name="twitter:title" content={title} />
  <meta name="twitter:description" content={publicData.consumer_language?.material} />
  <meta name="twitter:image" content={firstImage?.attributes.variants.default.url} />
  <meta name="twitter:label1" content="Certification" />
  <meta name="twitter:data1" content={publicData.certification?.[0]} />
  <meta name="twitter:label2" content="Age Group" />
  <meta name="twitter:data2" content={publicData.consumer_language?.age_group_display} />
</Helmet>
```

### 4. robots.txt & sitemap.xml Configuration

#### robots.txt (Priority: P1)

**File**: `public/robots.txt`

```
User-agent: *
Allow: /
Allow: /l/*
Allow: /s?*
Allow: /u/*

Disallow: /api/*
Disallow: /checkout/*
Disallow: /account/*
Disallow: /inbox/*
Disallow: /order/*

Sitemap: https://www.mela.baby/sitemap.xml
```

#### Dynamic Sitemap Generation (Priority: P2)

**File**: `server/api/sitemap.js` (new)

```javascript
// Generate dynamic sitemap for products
export const generateProductSitemap = async () => {
  const listings = await sdk.listings.query({
    pub_listingState: 'published',
    perPage: 1000
  });

  const urls = listings.data.data.map(listing => ({
    loc: `${config.canonicalRootURL}/l/${listing.id.uuid}/${createSlug(listing.attributes.title)}`,
    lastmod: listing.attributes.updatedAt,
    changefreq: 'weekly',
    priority: 0.8,
    image: listing.attributes.images.map(img => ({
      loc: img.attributes.variants.default.url,
      caption: listing.attributes.title,
      title: listing.attributes.title
    }))
  }));

  return generateXML(urls);
};
```

---

## UI/UX Requirements

### Product Page Enhancements

#### 1. Safety & Certifications Section (Priority: P0)

**Location**: Below product title, above price

**Design**:
```
┌─────────────────────────────────────────────┐
│ ✓ GOTS Certified Organic Cotton             │
│   → Safe for baby's sensitive skin          │
│                                              │
│ ✓ Non-Toxic Dyes (AZO-Free)                 │
│   → Colors won't irritate or fade           │
│                                              │
│ ✓ No Small Parts - Choking Hazard Free      │
│   → Tested to BIS IS 11871 standards        │
│                                              │
│ [Learn more about our safety standards →]   │
└─────────────────────────────────────────────┘
```

**Component**: `SafetyCertifications.js` (new)

```javascript
// src/components/SafetyCertifications/SafetyCertifications.js
export const SafetyCertifications = ({ publicData }) => {
  const { certification, safety } = publicData;

  return (
    <div className={css.safetySection}>
      <h3 className={css.sectionTitle}>
        <FormattedMessage id="ListingPage.safetyTitle" />
      </h3>

      <ul className={css.certificationList}>
        {certification?.map(cert => {
          const certData = translateToConsumerLanguage('certifications', cert);
          return (
            <li key={cert} className={css.certItem}>
              <IconCheckmark className={css.checkIcon} />
              <div className={css.certContent}>
                <strong className={css.certLabel}>{certData.label}</strong>
                <p className={css.certBenefit}>{certData.consumer_benefit}</p>
              </div>
            </li>
          );
        })}

        {safety?.safety_features?.map(feature => (
          <li key={feature} className={css.certItem}>
            <IconCheckmark className={css.checkIcon} />
            <div className={css.certContent}>
              <span>{feature}</span>
            </div>
          </li>
        ))}
      </ul>

      <NamedLink name="SafetyStandardsPage" className={css.learnMoreLink}>
        <FormattedMessage id="ListingPage.learnMoreSafety" />
      </NamedLink>
    </div>
  );
};
```

#### 2. Product Details in Consumer Language (Priority: P0)

**Location**: Product description section

**Design**:
```
About This Product
──────────────────

Material & Feel
Soft organic cotton (GOTS certified) - gentle on baby's
sensitive skin. Jersey knit provides stretch for easy
movement.

Perfect For
Newborns (0-3 months) - ideal for everyday wear and
sleep time.

Safety Features
• No small parts - choking hazard free
• Nickel-free snap buttons
• Non-toxic dyes won't irritate skin

Care Instructions
Easy care: Machine washable on gentle cycle. Tumble
dry low or air dry. Gets softer with each wash.

Made in India by artisan weavers committed to
sustainable practices.
```

#### 3. Brand Story Card (Priority: P1)

**Location**: Below product details, above reviews

**Design**:
```
┌─────────────────────────────────────────────┐
│  [Brand Logo]    About Aagghhoo              │
│                                              │
│  Handcrafted organic baby clothing made by  │
│  Indian artisans. Every piece supports fair │
│  wages and traditional weaving techniques.  │
│                                              │
│  ✓ GOTS Certified Organic                   │
│  ✓ Fair Trade Practices                     │
│  ✓ Women-Owned Business                     │
│                                              │
│  [Visit Brand Page →]                        │
└─────────────────────────────────────────────┘
```

---

## Implementation Plan

### Phase 1: Foundation (Weeks 1-2)

**Week 1: Data Layer**
- [ ] Create `consumerLanguage.js` utility with translation maps
- [ ] Expand publicData structure for new products
- [ ] Add migration script for existing product data
- [ ] Create `schemaGenerator.js` utility functions

**Week 2: Schema Implementation**
- [ ] Implement Product schema on ListingPage
- [ ] Add Offer schema with pricing
- [ ] Add Brand schema
- [ ] Test with Google Rich Results Test

### Phase 2: UI Enhancement (Weeks 3-4)

**Week 3: Component Development**
- [ ] Build SafetyCertifications component
- [ ] Enhance TrustBadges with tooltips
- [ ] Update product description layout
- [ ] Create BrandStoryCard component

**Week 4: Integration**
- [ ] Integrate new components into ListingPage
- [ ] Update ListingCard with consumer language
- [ ] Add meta tags to all pages
- [ ] QA and responsive testing

### Phase 3: Validation & Launch (Week 5)

**Week 5: Testing & Optimization**
- [ ] Validate all Schema.org markup
- [ ] Test with AI assistants (ChatGPT, Claude, Perplexity)
- [ ] Manual QA on sample products
- [ ] Performance testing
- [ ] Accessibility audit
- [ ] Launch to production

### Phase 4: Measurement (Week 6+)

**Ongoing:**
- [ ] Monitor Google Search Console for rich results
- [ ] Track AI assistant discovery via manual queries
- [ ] Measure organic traffic changes
- [ ] Collect parent feedback on clarity
- [ ] A/B test consumer language variations

---

## Dependencies

### Technical Dependencies
- **Sharetribe SDK**: Ensure publicData structure supports new fields
- **React Helmet**: For meta tag and schema injection
- **Server-side Rendering**: Schema.org must render server-side for crawlers
- **Image CDN**: Ensure all images have stable URLs for schema

### Data Dependencies
- **Product Catalog**: Need 50+ products with complete data to validate
- **Brand Information**: All providers must have brand story and certifications
- **Review System**: (Future) Need review data for AggregateRating schema
- **Inventory System**: Must track stock levels for Schema.org availability

### Design Dependencies
- **Icon Library**: Need checkmark, info icons for certifications
- **Typography**: Consumer-friendly labels must be legible
- **Color System**: Certification badges need accessible contrast
- **Spacing**: New sections must fit existing layout system

---

## Risks & Mitigations

### Risk 1: Schema.org Validation Failures

**Risk**: Invalid schema markup causes Rich Results to not appear

**Likelihood**: Medium
**Impact**: High
**Mitigation**:
- Use Google's Rich Results Test in development
- Implement automated schema validation tests
- Follow Schema.org best practices strictly
- Monitor Google Search Console for errors

### Risk 2: AI Assistant Adoption Lag

**Risk**: AI assistants don't immediately index/use our structured data

**Likelihood**: Medium
**Impact**: Medium
**Mitigation**:
- Focus equally on traditional SEO benefits
- Measure success via organic search traffic, not just AI
- Manual testing with AI tools to verify discoverability
- Long-term play - early mover advantage

### Risk 3: Parent Confusion with New Language

**Risk**: Consumer-friendly language doesn't resonate with target audience

**Likelihood**: Low
**Impact**: Medium
**Mitigation**:
- User testing with 10-15 parents before launch
- A/B test different language variations
- Provide tooltips/explanations for technical terms
- Monitor customer support inquiries for confusion

### Risk 4: Performance Impact

**Risk**: Additional schema scripts and meta tags slow page load

**Likelihood**: Low
**Impact**: Low
**Mitigation**:
- Server-side render schema (no client-side overhead)
- Minify JSON-LD scripts
- Lazy load non-critical components
- Monitor Core Web Vitals in Google PageSpeed Insights

### Risk 5: Incomplete Product Data

**Risk**: Brands don't provide necessary certification/safety data

**Likelihood**: High
**Impact**: High
**Mitigation**:
- Create brand onboarding checklist with required data
- Provide templates and examples for product listings
- Manual review process for initial products
- Incentivize complete data (featured placements, better visibility)

---

## Testing Strategy

### 1. Schema.org Validation

**Tools**:
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)
- [Structured Data Linter](http://linter.structured-data.org/)

**Test Cases**:
- [ ] Product schema passes validation
- [ ] All required properties present (name, image, description, offers)
- [ ] Nested Brand and Offer schemas valid
- [ ] additionalProperty array properly formatted
- [ ] No warnings or errors in Google test

### 2. AI Assistant Testing

**Manual Testing with AI Tools**:

**Test Query 1**: "What's the best GOTS certified organic cotton bodysuit for a newborn?"
- [ ] Mela product appears in results
- [ ] Certifications correctly mentioned
- [ ] Age appropriateness highlighted
- [ ] Direct link provided

**Test Query 2**: "Show me safe baby clothes made in India with no toxic dyes"
- [ ] Multiple Mela products returned
- [ ] Non-toxic certification emphasized
- [ ] Origin (India) correctly identified

**Test Query 3**: "I need easy-care baby clothes that are machine washable"
- [ ] Care instructions correctly parsed from schema
- [ ] Products with simple care highlighted

**AI Tools to Test**:
- ChatGPT (Browse with Bing/web search enabled)
- Claude (with web search)
- Perplexity AI
- Google Bard/Gemini

### 3. User Acceptance Testing

**Parent Testing Session** (10-15 participants):

**Tasks**:
1. "Find a safe organic cotton outfit for your 3-month-old"
2. "What certifications does this product have? Do you understand them?"
3. "How would you care for this item at home?"
4. "Does this product feel trustworthy? Why or why not?"

**Success Criteria**:
- 80%+ understand certification benefits
- 90%+ can identify age appropriateness
- 85%+ feel confident about safety
- 70%+ complete purchase intent

### 4. Performance Testing

**Metrics to Track**:
- Page load time (target: <3s on 3G)
- Lighthouse SEO score (target: 95+)
- Core Web Vitals (LCP <2.5s, FID <100ms, CLS <0.1)
- Schema.org script size (target: <10KB per page)

**Tools**:
- Google PageSpeed Insights
- WebPageTest
- Chrome DevTools Performance tab

### 5. Accessibility Testing

**WCAG 2.1 AA Compliance**:
- [ ] All certification badges have proper aria-labels
- [ ] Tooltips accessible via keyboard
- [ ] Color contrast meets 4.5:1 minimum
- [ ] Screen reader testing (NVDA, JAWS)
- [ ] Keyboard navigation works for all interactive elements

---

## Success Criteria

### Launch Criteria (Week 5)

**Must Have** (P0):
- ✅ All product pages have valid Schema.org Product markup
- ✅ Google Rich Results Test passes with no errors
- ✅ Consumer language translations implemented for top 20 products
- ✅ SafetyCertifications component visible and accessible
- ✅ No performance regression (page load <3s)

**Should Have** (P1):
- ✅ Category pages have ItemList schema
- ✅ Brand pages have Organization schema
- ✅ Meta tags enhanced on all pages
- ✅ robots.txt and sitemap.xml configured

**Nice to Have** (P2):
- ✅ Dynamic sitemap generation
- ✅ BrandStoryCard component
- ✅ A/B test setup for language variations

### 3-Month Success Metrics

**Discoverability**:
- 100% of products pass Schema.org validation
- 80%+ of products discoverable via AI assistant queries
- 50+ rich search result impressions in Google Search Console

**Traffic & Engagement**:
- +40% organic search traffic to product pages
- +25% average time on product pages
- -15% bounce rate on product pages

**Conversion**:
- +15% conversion rate from organic search
- +20% add-to-cart rate on products with complete data
- +10% average order value

**Parent Feedback**:
- 4.5+ star rating on product page clarity (user surveys)
- <5% customer support inquiries about product safety/certifications
- 80%+ parent satisfaction with product information

---

## Rollout Strategy

### Pilot Phase (Week 1-2)

**Scope**: 10 hero products from 3 brands
- Aagghhoo: 3 products (onesies, dungarees)
- Masilo: 3 products (sleepsuits, sets)
- Greendigo: 4 products (bodysuits, rompers)

**Goals**:
- Validate schema implementation
- Test AI assistant discovery
- Gather initial parent feedback
- Identify data gaps

### Staged Rollout (Week 3-4)

**Wave 1**: Top 50 products by view count
**Wave 2**: All clothing products (100+ items)
**Wave 3**: Accessories and other categories

**Rollout Criteria**:
- Each wave requires 95%+ schema validation pass rate
- No critical bugs from previous wave
- Performance metrics stable

### Full Launch (Week 5)

**Announcement**:
- Blog post: "Mela becomes first AI-ready baby marketplace"
- Email to existing users highlighting new clarity
- Social media campaign showcasing certifications
- Press release to parenting/tech media

---

## Open Questions

### Technical Questions

1. **Schema.org AggregateRating**: Do we implement placeholder ratings before we have review system?
   - **Decision needed**: Yes/No/Wait for reviews
   - **Owner**: Product Team
   - **Due**: Week 1

2. **Server-side vs Client-side Schema Rendering**: Current Sharetribe SSR limitations?
   - **Decision needed**: Verify SSR capabilities
   - **Owner**: Engineering Team
   - **Due**: Week 1

3. **Dynamic Sitemap**: Should we build custom or use Sharetribe's built-in?
   - **Decision needed**: Custom build vs extend existing
   - **Owner**: Engineering Team
   - **Due**: Week 2

### Content Questions

4. **Certification Explanations**: How detailed should tooltip content be?
   - **Decision needed**: 1-2 sentences vs full paragraph
   - **Owner**: Content/UX Team
   - **Due**: Week 2

5. **Brand Story Requirements**: What's minimum required brand information?
   - **Decision needed**: Define mandatory fields
   - **Owner**: Brand Partnerships Team
   - **Due**: Week 1

### Business Questions

6. **Incomplete Data Handling**: Do we show products without full certification data?
   - **Decision needed**: Hide vs show with disclaimer
   - **Owner**: Product Team
   - **Due**: Week 1

7. **Brand Onboarding**: Who validates certification claims from brands?
   - **Decision needed**: Manual review process vs self-attestation
   - **Owner**: Operations Team
   - **Due**: Week 2

---

## Appendix

### A. Schema.org Resources

- [Schema.org Product Documentation](https://schema.org/Product)
- [Google Rich Results Guide](https://developers.google.com/search/docs/appearance/structured-data/product)
- [Schema.org Validator](https://validator.schema.org/)
- [JSON-LD Playground](https://json-ld.org/playground/)

### B. Consumer Language Examples

**Before (Merchant Language)**:
- "GOTS certified organic cotton jersey bodysuit with envelope neckline and snap closure"
- "Handloom woven kala cotton dungaree set with adjustable straps"
- "Bamboo rayon blend sleepsuit with built-in footies and two-way zipper"

**After (Consumer Language)**:
- "Soft organic cotton onesie (GOTS certified) with easy-dress neckline and snap buttons for quick diaper changes"
- "Traditional Indian cotton overalls - handcrafted, chemical-free, grows with your baby"
- "Breathable bamboo sleeper that keeps baby dry - built-in feet for warmth, zipper opens both ways for easy changes"

### C. Certification Glossary

**GOTS (Global Organic Textile Standard)**:
- What: International certification for organic fibers
- Parent Benefit: Guarantees no harmful chemicals touch baby's skin
- Verification: Third-party tested

**Oeko-Tex Standard 100**:
- What: Independent testing for harmful substances
- Parent Benefit: Tested for 100+ toxic chemicals
- Verification: Annual lab testing

**BIS (Bureau of Indian Standards)**:
- What: India's national quality standards
- Parent Benefit: Meets safety requirements for children's clothing
- Verification: Government certified

**Non-Toxic AZO-Free Dyes**:
- What: Dyes without carcinogenic compounds
- Parent Benefit: Colors won't irritate skin or cause allergies
- Verification: Laboratory tested

### D. Related Documents

- `item-aspects-analysis.md` - Product attribute prioritization
- `mela_homepage_optimization_strategy.md` - Overall SEO approach
- `affiliate-brand-onboarding.md` - Brand data requirements

---

## Changelog

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-12-11 | 1.0 | Initial draft | Product Team |

---

## Approval

- [ ] Product Lead
- [ ] Engineering Lead
- [ ] Design Lead
- [ ] Brand Partnerships Lead
- [ ] CEO/Founder

**Target Approval Date**: 2025-12-15
**Target Launch Date**: 2026-01-15 (5 weeks)
