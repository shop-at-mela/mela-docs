# Mela Brands Page PRD

## Executive Summary

**Product**: Brands Directory & Profile Pages for Mela Marketplace
**Target Market**: New visitors discovering authentic Indian organic baby brands
**Business Model**: Multi-purpose page serving SEO/traffic acquisition, brand partnerships, and product discovery
**Primary Success Metrics**:
- Organic traffic growth from brand-related search queries
- User engagement rate (directory → brand profile → product conversions)
- Brand partnership applications and featured brand placements
- Repeat customer visits to favorite brand profiles

---

## 1. Market Opportunity

### Target Audience

**Primary Users**: New visitors in discovery phase
- Parents seeking authentic Indian organic baby products
- Quality-conscious shoppers researching brand certifications
- Indian diaspora looking for culturally relevant brands
- Gift buyers seeking trusted premium baby brands

**User Behaviors**:
- 80% of new parents research brands online before purchasing
- 70%+ use smartphones at every stage of discovery
- Trust third-party certifications over self-claimed quality
- Value authenticity and real-life brand stories over polished marketing

### Pain Points Addressed

1. **Fragmented Discovery**: No centralized directory of Indian organic baby brands
2. **Trust Barriers**: Difficulty verifying certifications and brand authenticity
3. **Information Overload**: Too many options without clear quality signals
4. **Cultural Gap**: Lack of brands connecting Indian heritage with modern parenting needs

### Market Opportunity

- **2M+ Indian diaspora families** in USA seeking authentic Indian products
- **$60B+ US baby care market** growing 8% annually, with sustainability segment growing faster
- **Underserved niche**: Limited platforms curating verified Indian organic baby brands
- **SEO Potential**: Low competition for "Indian organic baby brands," "GOTS certified baby brands India"
- **Partnership Opportunity**: 50+ Indian brands seeking global distribution channels

---

## 2. Customer Insights

### New Parent Brand Discovery Behavior

**Research Findings**:
- **70%+ of millennial parents** use smartphones throughout the entire purchase journey
- **Influencer marketing dominates** brand discovery in parenting communities
- **Word-of-mouth remains powerful** through parenting groups and social circles
- **Nearly universal research step**: Product reviews and ratings before purchase

**Discovery Priorities**:
1. Certifications and safety standards (GOTS, BIS, organic verification)
2. Brand story and authenticity (founder story, values, transparency)
3. Product quality indicators (reviews, materials, craftsmanship)
4. Cultural relevance (Indian heritage, traditional practices)
5. Convenience factors (return policy, shipping, customer service)

### Trust Factors for Baby Product Purchases

**Priority Hierarchy**:
1. **Transparency**: Clear sourcing, material disclosure, manufacturing process
2. **Quality Assurance**: Third-party certifications (GOTS > self-claimed organic)
3. **Authenticity**: Real-life depictions, relatable brand stories
4. **Values Alignment**: Sustainability, ethical practices, cultural sensitivity
5. **Social Proof**: Reviews from other parents, media features, testimonials

**Conversion Impact**:
- Trust badges increase e-commerce sales by **up to 32%**
- Reduce cart abandonment by **20%**
- Forms/CTAs with trust badges see **42% more conversions**

### Indian Diaspora Shopping Preferences

**Cultural Characteristics**:
- **Collectivism**: Family and friend recommendations carry high weight
- **Value-consciousness**: Balance between price sensitivity and quality expectations
- **Cultural identity**: Growing preference for brands reflecting Indian roots
- **Regional pride**: Products showcasing Indian craftsmanship and heritage

**Contemporary Trends**:
- Eco-conscious choices with sustainable edge, plastic-free packaging
- Transparency in sourcing, ingredients, origin, labor ethics
- Support for women-owned businesses and artisan communities
- Bilingual content preferences (English primary, Hindi/regional secondary)

---

## 3. Product Goals & Success Metrics

### Business Goals

**1. SEO & Traffic Acquisition**
- Rank for brand-related keywords: "Indian organic baby brands," "[brand name] products," "GOTS certified baby clothing India"
- Generate backlinks through brand partnerships and content marketing
- Increase organic search visibility via schema.org rich results

**2. Brand Partnership Tool**
- Showcase partner brands to attract new sellers
- Strengthen existing brand relationships through featured placements
- Provide brands with analytics and customer insights
- Create clear value proposition for brand partnership program

**3. Product Discovery & Customer Engagement**
- Help customers discover brands through certifications, categories, and stories
- Build brand loyalty through transparent storytelling
- Enable comparison shopping across brands
- Drive repeat visits through personalized brand recommendations

### Key Performance Indicators

#### Primary Metrics

**Traffic Metrics**:
- Monthly organic traffic to `/brands` directory: Target 5,000+ visits by Month 3
- Brand-related keyword rankings: 20+ keywords in top 10 within 6 months
- Direct traffic to brand profile pages: Target 15% of total brand page visits
- Referral traffic from brand partners: Track partnership effectiveness

**Engagement Metrics**:
- Discovery rate: % of homepage visitors who visit brands directory (Target: 15%)
- Engagement rate: % of directory visitors who click brand cards (Target: 40%)
- Brand profile depth: Average pages viewed per brand visit (Target: 3+)
- Session duration on brand pages: Target 2+ minutes

**Conversion Metrics**:
- Directory → Brand Profile conversion: Target 40%
- Brand Profile → Product Page conversion: Target 60%
- Brand Profile → Purchase conversion: Target 10%
- Repeat visits to same brand within 30 days: Target 25%

#### Secondary Metrics

**Partnership Metrics**:
- Brand partnership applications per month: Target 5+ qualified applications
- Featured brand placement requests: Track demand and pricing potential
- Brand satisfaction score: Quarterly survey (Target: 8+/10)

**SEO Metrics**:
- Schema.org validation score: 100% across all brand pages
- Rich results appearance in Google: Track featured snippets and knowledge panels
- Page speed scores: Target 90+ on mobile, 95+ on desktop
- Backlinks to brand directory: Target 50+ quality backlinks in 6 months

---

## 4. Technical Architecture

### 4.1 Curated Brand Directory Approach

**Implementation Strategy**: Static Brand Registry + Marketplace API

**Architecture Decision**:
After evaluating Integration API vs. Marketplace API constraints, we chose a **curated brand directory** approach that leverages existing Marketplace API capabilities:

**Why Curated Registry?**
- Works with Marketplace API (no Integration API complexity required)
- Better performance through lazy loading and parallel requests
- Quality control - only vetted/approved brands appear
- Simpler server architecture - no custom API endpoints needed
- Easier to maintain and update brand list
- Scales efficiently with growing brand count

**Architecture Flow**:
```
Brand Registry (configBrands.js)
    ↓
BrandsPage Component
    ↓
Marketplace API (users.show for each brand)
    ↓
Brand Cards with lazy-loaded data
```

**Benefits**:
- Each brand is a Provider user in Sharetribe's standard Customer/Provider model
- User profiles contain all brand data (publicData, metadata, profileImage)
- Leverages existing `/u/{userId}` profile page infrastructure
- No server-side endpoints or Integration API authentication needed
- Fast parallel fetching of brand details via Marketplace API

### 4.2 Brand Registry Configuration

**File**: `/src/config/configBrands.js`

This file contains the curated list of brand user IDs, separated into featured and all brands:

```javascript
/**
 * Featured brands - displayed in top section (max 6 recommended)
 */
export const featuredBrandIds = [
  '7e1e3c5a-9b4d-4e6f-8a2c-1d5f6e8b9c0a',
  '3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c',
  // ... more featured brand UUIDs
];

/**
 * All brands - complete directory
 */
export const allBrandIds = [
  '7e1e3c5a-9b4d-4e6f-8a2c-1d5f6e8b9c0a',  // Featured brands included
  '3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c',
  '8a3b2c1d-4e5f-6a7b-8c9d-0e1f2a3b4c5d',  // Regular brands
  // ... more brand UUIDs
];

/**
 * Get paginated brand IDs for lazy loading
 */
export const getPaginatedBrandIds = (page = 1, perPage = 24) => {
  const startIndex = (page - 1) * perPage;
  const endIndex = startIndex + perPage;
  return {
    brandIds: allBrandIds.slice(startIndex, endIndex),
    totalPages: Math.ceil(allBrandIds.length / perPage),
    totalItems: allBrandIds.length,
    page, perPage
  };
};
```

**Managing the Brand List**:
1. Get brand user UUID from their profile URL: `/u/{uuid}`
2. Add to `featuredBrandIds` (if featured) or `allBrandIds`
3. Ensure brand user has `userType: 'provider'` in Sharetribe
4. Brand data fetched automatically from user profile

### 4.3 User Extended Data Schema

**Provider User Profile Structure**:

```javascript
{
  userId: UUID,
  userType: 'provider',  // Standard Sharetribe user type
  attributes: {
    profile: {
      displayName: "Masilo",
      bio: "Premium organic baby clothing from India",
      publicData: {
        certifications: [
          'gots_certified',
          'organic_cotton',
          'bis_approved'
        ],
        brandLogoUrl: "https://...",
        foundedYear: 2015,
        origin: 'Mumbai, India',
        specialty: 'Organic baby clothing',
        websiteUrl: "https://masilo.com"
      },
      metadata: {
        listingCount: 45,        // Auto-calculated by Sharetribe
        averageRating: 4.8,
        reviewCount: 234
      }
    },
    profileImage: {
      id: UUID,
      type: 'image',
      attributes: {
        variants: {
          'square-small': { url: '...', width: 240, height: 240 },
          'square-small2x': { url: '...', width: 480, height: 480 }
        }
      }
    }
  }
}
```

**Extended Data Field Definitions** (in `configUser.js`):

```javascript
{
  key: 'certifications',
  scope: 'public',
  schemaType: 'multi-enum',
  enumOptions: [
    { option: 'gots_certified', label: 'GOTS Certified' },
    { option: 'organic_cotton', label: '100% Organic Cotton' },
    { option: 'bis_approved', label: 'BIS Approved' },
    // ... more certifications
  ],
  userTypeConfig: {
    limitToUserTypeIds: true,
    userTypeIds: ['provider']
  }
}
```

### 4.4 Client-Side Implementation

**BrandsPage Duck**: `/src/containers/BrandsPage/BrandsPage.duck.js`

This file handles fetching brand data using Marketplace API:

```javascript
import { storableError } from '../../util/errors';
import { addMarketplaceEntities } from '../../ducks/marketplaceData.duck';
import { getFeaturedBrandIds, getPaginatedBrandIds } from '../../config/configBrands';

/**
 * Fetch brand details from Marketplace API
 * Fetches multiple brands in parallel using users.show
 */
export const fetchBrands = (params = {}) => (dispatch, getState, sdk) => {
  const { page = 1, perPage = 24 } = params;

  // Get brand IDs from config
  const { brandIds, totalPages, totalItems } = getPaginatedBrandIds(page, perPage);

  // Fetch all brands in parallel using Marketplace API
  const brandPromises = brandIds.map(brandId =>
    sdk.users.show({
      id: brandId,
      include: ['profileImage'],
      'fields.image': ['variants.square-small', 'variants.square-small2x']
    })
  );

  return Promise.all(brandPromises)
    .then(responses => {
      // Combine responses
      const users = responses.map(r => r.data.data);
      const included = responses.flatMap(r => r.data.included || []);

      // Add to marketplace entities
      dispatch(addMarketplaceEntities({ data: users, included }));

      return {
        brandIds: users.map(u => u.id.uuid),
        pagination: { page, perPage, totalPages, totalItems }
      };
    });
};

/**
 * Fetch featured brands
 */
export const fetchFeaturedBrands = () => (dispatch, getState, sdk) => {
  const featuredIds = getFeaturedBrandIds();

  const brandPromises = featuredIds.map(brandId =>
    sdk.users.show({
      id: brandId,
      include: ['profileImage'],
      'fields.image': ['variants.square-small', 'variants.square-small2x']
    })
  );

  return Promise.all(brandPromises).then(responses => {
    const users = responses.map(r => r.data.data);
    const included = responses.flatMap(r => r.data.included || []);
    dispatch(addMarketplaceEntities({ data: users, included }));
  });
};
```

**Key Features**:
- Uses Marketplace API `users.show()` for each brand
- Fetches brands in parallel for better performance
- Lazy loading via pagination
- No server-side endpoints needed
- Works without user authentication

### 4.5 Data Flow Summary

```
1. Page Load
   ↓
2. configBrands.js (get brand IDs for current page)
   ↓
3. Parallel API calls (sdk.users.show for each brand)
   ↓
4. Marketplace Data Store (normalized user entities)
   ↓
5. BrandsPage Component (denormalized brand data)
   ↓
6. BrandCard Components (render brand details)
```

**Performance Characteristics**:
- **Initial Load**: Fetches 24 brands in parallel (~500ms)
- **Load More**: Fetches next 24 brands (~500ms)
- **Featured Brands**: Fetches 6 brands in parallel (~300ms)
- **Caching**: User entities cached in Redux store
- **Network**: N+1 pattern acceptable for curated directory (limited scale)

---

## 5. UX Design & Information Architecture

### 5.1 Page Structure

#### Brands Directory Page (`/brands`)

**Layout Components**:

```
┌─────────────────────────────────────────────────────────────┐
│ Hero Section                                                 │
│ ┌─────────────────────────────────────────────────────────┐│
│ │ H1: "Discover India's Most Trusted Organic Baby Brands"││
│ │ Subheadline: "Curated collection of 50+ GOTS certified"││
│ │ CTA: [Explore All Brands] [Apply to Partner]           ││
│ └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│ Featured Brands Carousel (if featured brands exist)         │
│ ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐                     │
│ │ Logo │  │ Logo │  │ Logo │  │ Logo │  →                  │
│ └──────┘  └──────┘  └──────┘  └──────┘                     │
├─────────────────────────────────────────────────────────────┤
│ Filter/Sort Bar                                              │
│ [Search brands...] | Sort: [Alphabetical ▼] | [24 per page]│
├─────────────────────────────────────────────────────────────┤
│ Brand Grid                                                   │
│ ┌─────────┐  ┌─────────┐  ┌─────────┐                      │
│ │  LOGO   │  │  LOGO   │  │  LOGO   │                      │
│ │  Name   │  │  Name   │  │  Name   │                      │
│ │ 🏆 Badge│  │ 🏆 Badge│  │ 🏆 Badge│                      │
│ │Tagline  │  │Tagline  │  │Tagline  │                      │
│ │45 Items │  │32 Items │  │67 Items │                      │
│ │[Shop]   │  │[Shop]   │  │[Shop]   │                      │
│ └─────────┘  └─────────┘  └─────────┘                      │
│                                                              │
│ [Load More] or [1] [2] [3] [4] [5]                          │
└─────────────────────────────────────────────────────────────┘
```

**Mobile Responsive Breakdown**:
- **Desktop (1024px+)**: 3-column grid, sidebar filters
- **Tablet (768-1023px)**: 2-column grid, collapsible filters
- **Mobile (<768px)**: 1-column grid, sticky filter button at bottom

#### Brand Profile Page (`/brands/:brandSlug`)

**Layout Components**:

```
┌─────────────────────────────────────────────────────────────┐
│ Brand Header                                                 │
│ ┌─────────────────────────────────────────────────────────┐│
│ │ [Logo]  Brand Name                    🏆 GOTS Certified ││
│ │         One-line tagline              ⭐ Featured Brand ││
│ │         ──────────────────────────────────────────────  ││
│ │         45 Products | ⭐ 4.8 (234 reviews) | Est. 2015 ││
│ │         [Shop All Products] [Visit Website] [Share]    ││
│ └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│ Navigation Tabs                                              │
│ [Products] [Our Story] [Certifications] [Reviews]           │
├─────────────────────────────────────────────────────────────┤
│ Tab Content Area                                             │
│                                                              │
│ PRODUCTS TAB:                                                │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│ │ Product  │ │ Product  │ │ Product  │ │ Product  │       │
│ │  Card    │ │  Card    │ │  Card    │ │  Card    │       │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│                                                              │
│ OUR STORY TAB:                                               │
│ Brand bio (2-3 paragraphs)                                   │
│ Founder's journey, mission, values                           │
│                                                              │
│ CERTIFICATIONS TAB:                                          │
│ ┌────────────────────────────────────────────┐              │
│ │ 🏆 GOTS Certified                          │              │
│ │ Control Union | Cert #12345 | Valid 2025  │              │
│ │ 100% organic fibers, non-toxic dyes...    │              │
│ └────────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Component Specifications

#### BrandCard Component

**Props**:
```javascript
{
  brand: {
    id: UUID,
    displayName: string,
    bio: string,
    publicData: {
      brandLogoUrl: string,
      certifications: string[],
      isFeaturedBrand: boolean
    },
    metadata: {
      listingCount: number,
      averageRating: number
    }
  }
}
```

**Visual Hierarchy**:
1. **Brand Logo**: Square, 200x200px display, centered
2. **Brand Name**: H3, 18-20px, semibold, centered below logo
3. **Certification Badge**: Absolute positioned top-left corner of logo
4. **Featured Badge**: Absolute positioned top-right if applicable
5. **Tagline**: 1-line excerpt from bio, 14px, gray, centered
6. **Product Count**: "45 Products" in small gray text
7. **CTA Button**: Primary button "Shop Brand"

**States**:
- Default: White card, subtle shadow
- Hover: Elevated shadow, slight scale (1.02x)
- Active/Clicked: Brief scale animation

**Trust Badge Placement**:
```css
.brandCard {
  position: relative;
  padding: 24px;
  border-radius: 12px;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.certificationBadge {
  position: absolute;
  top: 12px;
  left: 12px;
  background: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  box-shadow: 0 2px 4px rgba(0,0,0,0.15);
}

.featuredBadge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: var(--marketplaceColor);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
}
```

#### FilterBar Component

**Functionality**:
- **Search Input**: Brand name autocomplete
- **Sort Dropdown**: Alphabetical (A-Z, Z-A), Featured First, Most Products, Newest
- **Per Page**: 12, 24, 48 options
- **Clear Filters**: Reset all to defaults

**Mobile Behavior**:
- Collapse into sticky footer button: "Filters & Sort"
- Slide-up modal when clicked
- Apply/Cancel actions

### 5.3 Navigation Patterns

**Primary Entry Points**:
1. **Top Navigation**: "Brands" link in main menu
2. **Homepage**: "Explore All Brands" CTA in FeaturedBrands section
3. **Product Pages**: "View Brand Profile" link on listings
4. **Search Results**: Brand filter → "View All from [Brand]"

**Conversion Paths**:
```
Path 1: Homepage → Brands Directory → Brand Profile → Product → Purchase
Path 2: Homepage → Featured Brand → Brand Profile → Product → Purchase
Path 3: Search → Product → Brand Profile → More Products → Purchase
Path 4: Google → Brand Profile (SEO direct) → Product → Purchase
```

**Breadcrumb Navigation**:
```
Home > Brands > Masilo
Home > Brands > Search: "organic"
```

### 5.4 Accessibility Requirements

**WCAG 2.1 AA Compliance**:
- Color contrast ratio: Minimum 4.5:1 for text, 3:1 for UI components
- Keyboard navigation: Tab order, focus indicators, skip links
- Screen reader support: ARIA labels, semantic HTML, alt text
- Focus management: Trap focus in modals, announce filter changes

**Implementation**:
```jsx
<div
  className={css.brandCard}
  role="article"
  aria-labelledby={`brand-${brand.id.uuid}`}
>
  <img
    src={logoUrl}
    alt={`${brand.displayName} logo`}
    aria-describedby={`brand-desc-${brand.id.uuid}`}
  />
  <h3 id={`brand-${brand.id.uuid}`}>{brand.displayName}</h3>
  <p id={`brand-desc-${brand.id.uuid}`} className={css.srOnly}>
    {brand.bio}. {certificationCount} certifications.
    {listingCount} products available.
  </p>
  <Link
    to={`/brands/${brandSlug}`}
    aria-label={`Shop ${brand.displayName} products`}
  >
    Shop Brand
  </Link>
</div>
```

**Screen Reader Announcements**:
- Filter applied: "Showing 12 brands with GOTS certification"
- Page loaded: "Brands directory, page 2 of 5, 24 brands displayed"
- Sort changed: "Brands sorted by most products, descending"

---

## 6. Content Strategy

### 6.1 Brand Storytelling Framework

**Research-Backed Principles**:
- Authenticity over perfection: Real-life depictions resonate more
- Purpose-driven narrative: Connect brand mission to customer values
- Founder's journey: Why they started, personal connection to baby products
- Transparency: Honest about process, materials, pricing

**Content Sections for Brand Profiles**:

#### Brand Bio (100-150 words)
**Structure**:
1. Opening hook: Unique value proposition (1 sentence)
2. Origin story: When/why founded (2-3 sentences)
3. Mission statement: What drives the brand (1-2 sentences)
4. Key differentiator: What makes them special (1-2 sentences)

**Example Template**:
```
[Brand Name] creates [product category] for [target customer] who value [key benefit].

Founded in [year] by [founder name(s)], a [background] in [city, India],
the brand was born from [specific problem/experience that led to founding].
[Founder] noticed [gap in market] and set out to [mission].

Today, [Brand Name] [current scale/achievement] while [maintaining values].
Every product is [unique process/quality commitment], ensuring [benefit for customer].

What sets [Brand Name] apart: [key differentiator that competitors can't easily copy].
```

**Real Example**:
```
Masilo creates premium organic baby bedding for parents who refuse to compromise
on safety and sustainability.

Founded in 2015 by two new mothers in Mumbai frustrated by the lack of GOTS-certified
options in India, Masilo partnered with local artisans to revive traditional textile
craftsmanship using modern organic standards. They noticed Indian families were forced
to choose between authentic Indian designs and international safety certifications.

Today, Masilo serves over 10,000 families across 15 countries while supporting 50+
artisan families in Maharashtra. Every piece is hand-inspected and washed with
natural plant-based soaps, ensuring baby's first dreams are free from chemicals.

What sets Masilo apart: They're the only GOTS-certified brand in India offering
custom-designed nursery sets inspired by regional Indian art forms.
```

#### Certification Details

**Format for Each Certification**:
```
┌──────────────────────────────────────────────┐
│ 🏆 [Certification Name]                      │
│                                              │
│ Issued by: [Certifying Body]                │
│ Certificate #: [Number]                     │
│ Valid through: [Date]                       │
│                                              │
│ What this means for you:                    │
│ • [Benefit 1]                               │
│ • [Benefit 2]                               │
│ • [Benefit 3]                               │
│                                              │
│ [View Certificate] [Learn More]             │
└──────────────────────────────────────────────┘
```

**Certification Copy Examples**:

**GOTS (Global Organic Textile Standard)**:
```
What this means for you:
• 100% certified organic fibers from non-GMO seeds
• No toxic dyes, formaldehyde, or heavy metals
• Fair wages and safe working conditions verified
• Wastewater treatment and energy-efficient production
```

**BIS (Bureau of Indian Standards)**:
```
What this means for you:
• Meets Indian government safety standards for baby products
• Tested for flammability, chemical content, and durability
• Regular factory audits for quality compliance
• Consumer protection under Indian law
```

**Handcrafted / Artisan Badge**:
```
What this means for you:
• Each piece individually crafted by skilled artisans
• Supports traditional Indian textile techniques
• Unique variations celebrate authentic handwork
• Direct economic impact on artisan communities
```

### 6.2 Directory Page Messaging

**Hero Section Copy**:
```
H1: Discover India's Most Trusted Organic Baby Brands

Subheadline: Curated collection of 50+ GOTS certified brands creating
safe, sustainable products for your little one. Every brand is verified,
every product is authentic, every purchase supports Indian artisans.

CTA Primary: Explore All Brands
CTA Secondary: Become a Partner Brand
```

**Empty State (if filters return no results)**:
```
No brands match your current filters

We're adding new brands every week! Try adjusting your filters or
sign up below to get notified when brands matching your criteria join Mela.

[Adjust Filters] [Notify Me]
```

**Loading State**:
```
Discovering amazing brands for you...
(with animated logo or brand card skeletons)
```

### 6.3 Trust Signal Microcopy

**Badge Hover Tooltips** (appears on hover over badge):

```javascript
const badgeTooltips = {
  gots_certified: "Verified organic cotton grown without pesticides or GMOs, processed with non-toxic dyes",
  verified_seller: "Identity verified by Mela team, background checked, committed to quality standards",
  featured_brand: "Hand-selected by Mela for exceptional quality, customer reviews, and sustainable practices",
  made_in_india: "Proudly crafted in India, supporting local artisans and traditional craftsmanship",
  women_owned: "Owned and operated by women entrepreneurs",
  fair_trade: "Fair wages, safe working conditions, and community development verified",
  bis_approved: "Meets Bureau of Indian Standards safety requirements for baby products",
  non_toxic_dyes: "Natural or non-toxic synthetic dyes, free from harmful chemicals"
};
```

**Product Count Display**:
- 1-10 products: "{count} Products"
- 11-50 products: "{count} Products Available"
- 51+ products: "{count}+ Products Available"

### 6.4 SEO-Optimized Copy Templates

**Meta Title Templates**:
```
Directory Page:
"Indian Organic Baby Brands | {count}+ GOTS Certified Brands | Mela"

Brand Profile Page:
"{Brand Name} - {Tagline} | Authentic Indian Baby Products | Mela"

Example:
"Masilo - Organic Comfort for Little Ones | Authentic Indian Baby Products | Mela"
```

**Meta Description Templates**:
```
Directory Page (150-160 chars):
"Discover {count}+ verified Indian organic baby brands. Shop GOTS certified
clothing, natural care products, and handcrafted toys. Trusted by {customer_count}+ parents."

Brand Profile Page (150-160 chars):
"{Brand Name} - {One sentence about brand}. {Primary certification}.
{Product category}. Shop {product_count}+ authentic products on Mela."

Example:
"Masilo creates premium organic baby bedding handcrafted in India.
GOTS certified organic cotton. Shop 45+ nursery essentials on Mela."
```

**H1/H2 Hierarchy**:
```
Directory Page:
H1: "Trusted Indian Organic Baby Brands"
H2: "Featured Brands" (if section exists)
H2: "All Brands" (main grid section)
H2: "Why Shop Brands on Mela" (optional trust section)

Brand Profile Page:
H1: "{Brand Name} - {One-Line Tagline}"
H2: "Our Story"
H2: "Certifications & Standards"
H2: "Shop {Brand Name} Products"
H2: "Customer Reviews"
```

---

## 7. SEO Optimization

### 7.1 Schema.org Structured Data

**Directory Page Schema** (`/brands`):

```javascript
// BrandsPage.js - Schema implementation
const directorySchema = {
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "Indian Organic Baby Brands Directory",
  "description": "Curated collection of verified Indian organic baby brands offering GOTS certified clothing, natural care products, and handcrafted toys",
  "url": `${siteURL}/brands`,
  "mainEntity": {
    "@type": "ItemList",
    "itemListElement": brands.map((brand, index) => ({
      "@type": "ListItem",
      "position": index + 1,
      "item": {
        "@type": "Organization",
        "@id": `${siteURL}/brands/${brand.slug}`,
        "name": brand.displayName,
        "url": `${siteURL}/brands/${brand.slug}`,
        "logo": brand.publicData.brandLogoUrl,
        "description": brand.bio
      }
    }))
  },
  "breadcrumb": {
    "@type": "BreadcrumbList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": siteURL
      },
      {
        "@type": "ListItem",
        "position": 2,
        "name": "Brands"
      }
    ]
  }
};
```

**Brand Profile Page Schema** (`/brands/:brandSlug`):

```javascript
// BrandProfilePage.js - Schema implementation
const brandProfileSchema = {
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": `${siteURL}/brands/${brandSlug}`,
  "name": brand.displayName,
  "url": `${siteURL}/brands/${brandSlug}`,
  "logo": {
    "@type": "ImageObject",
    "url": brand.publicData.brandLogoUrl,
    "width": 400,
    "height": 400
  },
  "image": brand.publicData.brandLogoUrl,
  "description": brand.bio,
  "foundingDate": brand.publicData.foundedYear?.toString(),
  "address": {
    "@type": "PostalAddress",
    "addressCountry": "IN"
  },
  ...(brand.publicData.websiteUrl && {
    "sameAs": [
      brand.publicData.websiteUrl,
      brand.publicData.socialMedia?.instagram &&
        `https://instagram.com/${brand.publicData.socialMedia.instagram.replace('@', '')}`,
      brand.publicData.socialMedia?.facebook &&
        `https://facebook.com/${brand.publicData.socialMedia.facebook}`
    ].filter(Boolean)
  }),
  "brand": {
    "@type": "Brand",
    "name": brand.displayName,
    "logo": brand.publicData.brandLogoUrl,
    "slogan": brand.bio.split('.')[0] // First sentence as slogan
  },
  ...(brand.metadata?.averageRating && {
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": brand.metadata.averageRating,
      "reviewCount": brand.metadata.reviewCount,
      "bestRating": 5,
      "worstRating": 1
    }
  })
};
```

**Breadcrumb Schema** (on all brand pages):

```javascript
const breadcrumbSchema = {
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": siteURL
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Brands",
      "item": `${siteURL}/brands`
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": brand.displayName
    }
  ]
};
```

### 7.2 URL Structure & Routing

**Routes** (add to `routeConfiguration.js`):

```javascript
{
  path: '/brands',
  name: 'BrandsPage',
  component: BrandsPage,
  loadData: BrandsPage.loadData
},
{
  path: '/brands/:brandSlug',
  name: 'BrandProfilePage',
  component: BrandProfilePage,
  loadData: BrandProfilePage.loadData
}
```

**Slug Generation** (consistent with existing pattern):
```javascript
// src/util/urlHelpers.js
export const createBrandSlug = (brandName) => {
  return brandName
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')  // Replace non-alphanumeric with hyphens
    .replace(/^-+|-+$/g, '');      // Remove leading/trailing hyphens
};

// Examples:
// "Masilo" → "masilo"
// "The Little Tailor" → "the-little-tailor"
// "Nino Bambino" → "nino-bambino"
```

**Canonical URLs**:
```javascript
<link rel="canonical" href={`${siteURL}/brands/${brandSlug}`} />
```

**Pagination URLs** (if using pagination over infinite scroll):
```
/brands?page=1
/brands?page=2
/brands?page=3
```

### 7.3 Meta Tags Implementation

**BrandsPage (Directory)**:

```javascript
// BrandsPage.js
export const BrandsPageMeta = ({ intl, brandCount }) => {
  const title = intl.formatMessage(
    { id: 'BrandsPage.title' },
    { brandCount }
  );
  const description = intl.formatMessage(
    { id: 'BrandsPage.description' },
    { brandCount }
  );

  return {
    title,
    description,
    schema: directorySchema
  };
};
```

**Translation Strings** (`en.json`):
```json
{
  "BrandsPage.title": "Indian Organic Baby Brands | {brandCount}+ GOTS Certified Brands | Mela",
  "BrandsPage.description": "Discover {brandCount}+ verified Indian organic baby brands. Shop GOTS certified clothing, natural care products, and handcrafted toys. Trusted by 10,000+ parents.",
  "BrandProfilePage.title": "{brandName} - {tagline} | Authentic Indian Baby Products | Mela",
  "BrandProfilePage.description": "{brandName} - {bio}. {certification}. Shop {productCount}+ authentic products on Mela."
}
```

### 7.4 Performance Optimization

**Image Optimization**:
```javascript
// Brand logo variants (configure in Sharetribe Console)
const logoVariants = {
  'square-small': { width: 240, height: 240 },    // Card display
  'square-small2x': { width: 480, height: 480 },  // Retina displays
  'square-large': { width: 800, height: 800 }     // Profile page hero
};

// Usage in BrandCard
<ResponsiveImage
  rootClassName={css.brandLogo}
  alt={`${brand.displayName} logo`}
  image={brand.profileImage}
  variants={['square-small', 'square-small2x']}
  sizes="(max-width: 768px) 50vw, (max-width: 1024px) 33vw, 25vw"
/>
```

**Page Speed Targets**:
- Largest Contentful Paint (LCP): < 2.5s
- First Input Delay (FID): < 100ms
- Cumulative Layout Shift (CLS): < 0.1
- Mobile PageSpeed Score: 90+
- Desktop PageSpeed Score: 95+

**Optimization Techniques**:
1. **Lazy load brand cards**: Intersection Observer for below-fold cards
2. **Image lazy loading**: Native `loading="lazy"` attribute
3. **Code splitting**: Separate bundles for BrandsPage vs BrandProfilePage
4. **Prefetch on hover**: Preload brand profile pages when user hovers card
5. **CDN caching**: Cache-Control headers for static assets (logos, etc.)

**Implementation**:
```javascript
// Lazy load brand cards
const BrandCard = lazy(() => import('./BrandCard'));

// Prefetch on hover
const handleCardHover = (brandSlug) => {
  const link = document.createElement('link');
  link.rel = 'prefetch';
  link.href = `/brands/${brandSlug}`;
  document.head.appendChild(link);
};
```

### 7.5 Rich Results & Featured Snippets

**Target Rich Results**:
1. **Knowledge Panel**: Brand name, logo, description, social links
2. **Product Carousel**: Featured products from brand
3. **Rating Stars**: Aggregate reviews in search results
4. **Breadcrumb Trail**: In search result snippets

**FAQ Schema** (optional, for brand profile pages):
```javascript
const faqSchema = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What certifications does {Brand Name} have?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{Brand Name} is GOTS certified by {Certifying Body}, ensuring 100% organic cotton, non-toxic dyes, and fair labor practices."
      }
    },
    {
      "@type": "Question",
      "name": "Where is {Brand Name} manufactured?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{Brand Name} products are handcrafted in {City, State}, India, supporting local artisan communities."
      }
    }
  ]
};
```

---

## 8. Implementation Phases

### Phase 1: Configuration & Setup (Weeks 1-2)

**Milestone**: Brand registry and Redux infrastructure ready

**Tasks**:
1. **Configure Extended Data Schema**
   - Define brand-specific fields in configUser.js for Provider users
   - Fields: certifications, brandLogoUrl, foundedYear, origin, specialty, websiteUrl
   - Add validation rules and display configurations
   - Test schema validation with mock data

2. **Create Brand Registry Configuration**
   - Implement `/src/config/configBrands.js`
   - Populate `featuredBrandIds` array with 6-10 featured brand UUIDs
   - Populate `allBrandIds` array with 20+ brand UUIDs for launch
   - Implement `getPaginatedBrandIds()` and `getFeaturedBrandIds()` helper functions
   - Document process for adding/removing brands

3. **Build BrandsPage Redux Duck Module**
   - Create `/src/containers/BrandsPage/BrandsPage.duck.js`
   - Implement actions, reducers, thunks for fetching brands via Marketplace API
   - Use `sdk.users.show()` for parallel brand fetching
   - Add selectors: getBrands, getFeaturedBrands, getBrandsPagination
   - Register reducer in reducers.js

4. **Brand Data Collection**
   - Identify existing provider users to include in directory
   - Collect brand UUIDs from their profile URLs (`/u/{uuid}`)
   - Request high-quality logos (400x400px minimum)
   - Gather brand bios and certification information
   - Verify all providers have complete profiles

**Acceptance Criteria**:
- [ ] configBrands.js contains 20+ verified brand UUIDs
- [ ] BrandsPage duck fetches brands successfully using Marketplace API
- [ ] Parallel API requests complete in <1 second for 24 brands
- [ ] Redux state updates properly with brand entities
- [ ] All selected brands have userType: 'provider' configured

### Phase 2: UI Development (Weeks 3-4)

**Milestone**: Functional brands directory page

**Tasks**:
1. **Create BrandsPage Container**
   - File: `/src/containers/BrandsPage/BrandsPage.js`
   - Implement loadData for SSR
   - Connect to brands duck
   - Pagination or infinite scroll
   - Loading, error, empty states

2. **Build BrandCard Component**
   - File: `/src/components/BrandCard/BrandCard.js`
   - Logo, name, tagline, badges, product count
   - Hover effects and transitions
   - Responsive grid layout
   - Accessibility features (ARIA, keyboard nav)

3. **Implement FilterBar Component**
   - File: `/src/components/BrandFilterBar/BrandFilterBar.js`
   - Search input with autocomplete
   - Sort dropdown
   - Per-page selector
   - Mobile-friendly collapsible design

4. **Featured Brands Section**
   - Update FeaturedBrands component to use API
   - Replace static data with dynamic fetch
   - Fallback to hardcoded if API fails

5. **Routing & Navigation**
   - Add BrandsPage route to routeConfiguration.js
   - Update TopbarDesktop/TopbarMobileMenu with "Brands" link
   - Add breadcrumb navigation
   - Test deep linking and back button behavior

6. **Styling & Responsiveness**
   - CSS modules for all components
   - Mobile-first responsive design
   - Test on iOS Safari, Android Chrome, desktop browsers
   - Cross-browser compatibility

**Acceptance Criteria**:
- [ ] Directory page loads in <3 seconds
- [ ] Brand cards display correctly on all screen sizes
- [ ] Filters update results without page reload
- [ ] Search autocomplete works with keyboard and mouse
- [ ] Pagination maintains filter state
- [ ] All interactive elements are keyboard accessible
- [ ] Screen reader announces brand cards correctly

### Phase 3: Polish & Enhancements (Weeks 5-6)

**Milestone**: Production-ready brands directory with optimal UX

**Note**: Brand profile pages already exist at `/u/{user-id}` - no new pages needed. BrandCard components link directly to existing profile pages.

**Tasks**:
1. **Enhance Brand Cards**
   - Add hover effects and animations
   - Implement certification badge tooltips
   - Add "Featured" badge styling for featured brands
   - Ensure responsive behavior across devices
   - Accessibility improvements (ARIA labels, keyboard navigation)

2. **Optimize Loading States**
   - Add skeleton loading for brand cards
   - Implement progressive loading for images
   - Show meaningful loading messages
   - Handle empty states gracefully

3. **Add Search and Filtering** (Optional)
   - Client-side search by brand name
   - Filter by certifications
   - Sort options (alphabetical, featured first, etc.)
   - URL state management for filters

4. **Performance Optimization**
   - Lazy load brand card images
   - Implement intersection observer for below-fold cards
   - Optimize bundle size with code splitting
   - Add performance monitoring

5. **Error Handling**
   - Graceful degradation when brand data fails to load
   - Retry mechanism for failed API calls
   - User-friendly error messages
   - Fallback UI for missing brand data

6. **Analytics Integration**
   - Track brand card clicks
   - Monitor load more button usage
   - Measure conversion from directory to brand profiles
   - Set up conversion funnels

**Acceptance Criteria**:
- [ ] Directory page loads in <3 seconds on 3G
- [ ] All brand cards display correctly on mobile and desktop
- [ ] Featured brands section shows when data available
- [ ] Load more pagination works smoothly
- [ ] Error states handled gracefully
- [ ] Analytics tracking fires correctly
- [ ] Accessibility score 90+ in Lighthouse

### Phase 4: Brand Onboarding & Testing (Week 7)

**Milestone**: Production-ready with curated brand directory

**Tasks**:
1. **Brand Profile Preparation**
   - Identify 20+ provider users to include in launch directory
   - Ensure all brands have userType: 'provider' configured
   - Request high-res profile images/logos (400x400px minimum)
   - Collect brand bios and descriptions
   - Verify certification information and documentation
   - Add brand UUIDs to configBrands.js

2. **Content Quality Assurance**
   - Review all brand profiles for completeness
   - Ensure consistent formatting of bios and descriptions
   - Verify all images meet quality standards
   - Check that certifications are properly tagged
   - Confirm all links (website, social media) are valid
   - Add featured brand status for 6-10 top partners

3. **A/B Testing Setup**
   - Test featured brands placement (carousel vs grid)
   - Test load more vs traditional pagination
   - Test brand card layouts
   - Track engagement metrics for each variant

4. **Performance Testing**
   - Load testing with realistic brand counts (50-100 brands)
   - Page speed optimization (target 90+ mobile score)
   - API response time monitoring for parallel brand fetches
   - Image optimization and lazy loading verification
   - Test with slow 3G network conditions

5. **Analytics Implementation**
   - Google Analytics 4 events for brand interactions
   - Track: brand card clicks, load more usage, featured brand clicks
   - Set up conversion funnels: Directory → Profile → Product → Purchase
   - Monitor API error rates and failed brand fetches
   - Create custom dashboard for brand metrics

6. **QA & Bug Fixes**
   - Cross-browser testing (Chrome, Safari, Firefox, Edge)
   - Mobile device testing (iOS, Android, various screen sizes)
   - Test with empty brand arrays (edge case)
   - Test with failed API requests
   - Accessibility audit with axe DevTools
   - Fix any bugs found during testing

**Acceptance Criteria**:
- [ ] configBrands.js contains 20+ verified brand UUIDs
- [ ] All brands have complete, high-quality profiles
- [ ] No broken links or missing images
- [ ] Page speed scores meet targets (90+ mobile, 95+ desktop)
- [ ] Parallel API fetching completes in <1 second for 24 brands
- [ ] Analytics tracking works for all key events
- [ ] Zero critical or high-severity bugs
- [ ] Accessibility score 90+ in Lighthouse

### Phase 5: Launch & Optimization (Week 8+)

**Milestone**: Public launch with ongoing improvements

**Tasks**:
1. **Soft Launch**
   - Enable brands pages for 10% of traffic (feature flag)
   - Monitor error rates, page speed, conversion rates
   - Gather user feedback via in-app surveys
   - Fix any critical issues before full launch

2. **Full Launch**
   - Announce to all users via email/social
   - Publish blog post: "Introducing Mela Brands Directory"
   - Reach out to partner brands for co-promotion
   - Submit updated sitemap to Google Search Console

3. **SEO Monitoring**
   - Track keyword rankings for brand-related terms
   - Monitor click-through rates in Search Console
   - Analyze which brands drive most organic traffic
   - Identify opportunities for featured snippets

4. **Conversion Optimization**
   - Analyze funnel drop-off points
   - A/B test improvements based on data
   - Iterate on badge placement, copy, CTAs
   - Optimize mobile experience based on user behavior

5. **Content Expansion**
   - Add more brands (target: 10+ per month)
   - Encourage brands to complete profiles
   - Create blog content about featured brands
   - Develop brand spotlight video series

6. **Feature Enhancements** (Future Roadmap)
   - Automated brand onboarding flow for new providers
   - Brand dashboards with sales analytics
   - Direct messaging between customers and brands
   - Brand subscription/follow feature
   - Personalized brand recommendations based on user preferences
   - Brand comparison tool
   - Dynamic brand registry management (admin interface for adding/removing brands)

**Success Metrics** (3-month targets):
- [ ] 5,000+ monthly visits to brands directory
- [ ] 40% engagement rate (directory → profile clicks)
- [ ] 15% conversion rate (profile → product views)
- [ ] 20+ keywords in top 10 Google results
- [ ] 10+ new brand partnerships signed
- [ ] 4.5+ user satisfaction rating for brand discovery

---

## 9. Success Metrics & Monitoring

### 9.1 Key Performance Indicators

#### Traffic Metrics

**Organic Search Performance**:
- **Keyword Rankings**: Track 50+ brand-related keywords
  - "Indian organic baby brands" (primary)
  - "[Brand name] products" (brand-specific)
  - "GOTS certified baby clothes India"
  - "Authentic Indian baby products"
- **Target**: 20+ keywords in top 10 positions by Month 6
- **Measurement**: Google Search Console, Ahrefs/SEMrush weekly

**Page Views**:
- Brands directory: Target 5,000+ monthly by Month 3
- Brand profiles: Target 10,000+ monthly by Month 3
- Year-over-year growth: 25% monthly increase
- **Measurement**: Google Analytics 4

**Traffic Sources**:
- Organic search: Target 60% of brand page traffic
- Direct: Target 15% (bookmark, repeat visits)
- Referral: Target 15% (from brand partners)
- Social: Target 10%
- **Measurement**: GA4 Acquisition reports

#### Engagement Metrics

**Directory Page Engagement**:
- Discovery rate: % of homepage visitors who visit `/brands` (Target: 15%)
- Brand card click rate: % who click at least one card (Target: 40%)
- Average cards viewed per session: Target 8+
- Filter usage rate: % who apply at least one filter (Target: 30%)
- Search usage rate: % who use search bar (Target: 20%)

**Brand Profile Engagement**:
- Average session duration: Target 2+ minutes
- Pages per session: Target 3+ (profile + products)
- Bounce rate: Target <40%
- Tab interaction rate: % who click tabs (Story, Certifications) (Target: 25%)
- Product click-through rate: % who click products from profile (Target: 60%)

**Measurement**:
```javascript
// Google Analytics 4 Events
gtag('event', 'brand_directory_visit', {
  'source': referrer,
  'user_type': isAuthenticated ? 'logged_in' : 'guest'
});

gtag('event', 'brand_card_click', {
  'brand_name': brandName,
  'brand_position': cardPosition,
  'is_featured': isFeaturedBrand
});

gtag('event', 'brand_filter_applied', {
  'filter_type': 'certification',
  'filter_value': 'gots_certified'
});

gtag('event', 'brand_profile_view', {
  'brand_name': brandName,
  'source': 'directory' | 'search' | 'direct'
});

gtag('event', 'brand_product_click', {
  'brand_name': brandName,
  'product_id': productId,
  'from_tab': 'products' | 'featured'
});
```

#### Conversion Metrics

**Funnel Analysis**:
```
Step 1: Homepage → Brands Directory (Target: 15% conversion)
Step 2: Directory → Brand Profile (Target: 40% conversion)
Step 3: Brand Profile → Product Page (Target: 60% conversion)
Step 4: Product Page → Initiate Checkout (Target: 15% conversion)
Step 5: Checkout → Purchase (Target: 70% conversion)

Overall: Homepage → Purchase via Brands (Target: 1.8%)
```

**Brand Attribution**:
- % of purchases with "brand page" in conversion path (Target: 25%)
- Average order value from brand-attributed conversions vs. overall
- Repeat purchase rate within 30 days for brand-attributed customers (Target: 30%)

**Measurement**: GA4 Conversion Paths, Enhanced E-commerce tracking

#### Partnership Metrics

**Brand Acquisition**:
- Brand partnership applications per month: Target 5+ qualified
- Application → approval rate: Target 60%+
- Time from application to first listing: Target <14 days
- Brand retention rate: % still active after 6 months (Target: 80%)

**Brand Engagement**:
- % of brands with complete profiles (Target: 70%)
- Average products per brand: Target 25+
- Featured brand upgrade requests: Track demand and pricing
- Brand satisfaction score: Quarterly survey (Target: 8/10)

**Measurement**: Custom admin dashboard, Sharetribe Console analytics

### 9.2 Analytics Implementation

**Google Analytics 4 Setup**:

```javascript
// src/util/analytics.js
export const trackBrandEvent = (eventName, eventParams) => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', eventName, {
      event_category: 'Brands',
      ...eventParams
    });
  }
};

// Usage in components
import { trackBrandEvent } from '../../util/analytics';

// In BrandCard onClick
onClick={() => {
  trackBrandEvent('brand_card_click', {
    brand_name: brand.displayName,
    brand_id: brand.id.uuid,
    brand_position: index + 1,
    is_featured: brand.publicData.isFeaturedBrand,
    certifications: brand.publicData.certifications?.join(','),
    product_count: brand.metadata.listingCount
  });
  history.push(`/brands/${brandSlug}`);
}}

// In FilterBar onChange
onFilterChange={(filterType, filterValue) => {
  trackBrandEvent('brand_filter_applied', {
    filter_type: filterType,
    filter_value: filterValue,
    brands_displayed: filteredBrands.length
  });
}}
```

**Custom Dashboard** (Google Analytics):
- Create "Brand Performance" custom report
- Widgets: Traffic sources, top brands, conversion funnels, engagement metrics
- Segments: New vs. returning visitors to brand pages
- Alerts: Traffic drops >20%, conversion rate drops >10%

### 9.3 A/B Testing Framework

**Test Hypotheses**:

**Test 1: Badge Placement**
- Variant A: Certification badge top-left of logo
- Variant B: Certification badge below brand name
- Variant C: No badges on cards, only on profile
- **Hypothesis**: Top-left placement increases trust perception and CTR by 15%
- **Measurement**: Click-through rate to brand profile

**Test 2: CTA Copy**
- Variant A: "Shop Brand"
- Variant B: "View Products"
- Variant C: "Explore {Brand Name}"
- **Hypothesis**: Personalized copy ("Explore Masilo") increases conversions by 10%
- **Measurement**: Product page visits from brand profile

**Test 3: Sort Default**
- Variant A: Alphabetical (A-Z)
- Variant B: Featured brands first, then alphabetical
- Variant C: Most products, descending
- **Hypothesis**: Featured first increases engagement with high-quality brands by 20%
- **Measurement**: Average session duration, products viewed per session

**Test 4: Featured Section**
- Variant A: Carousel at top (current)
- Variant B: Grid with "Featured" badge
- Variant C: No separate featured section
- **Hypothesis**: Grid layout increases featured brand clicks by 25%
- **Measurement**: Featured brand profile visits

**Implementation**:
```javascript
// Using Google Optimize or custom A/B testing
import { useABTest } from '../../util/abTesting';

const BrandsPage = () => {
  const { variant } = useABTest('brand_badge_placement');

  const badgePosition = {
    A: 'top-left',
    B: 'below-name',
    C: 'none'
  }[variant] || 'top-left';

  return (
    <BrandCard badgePosition={badgePosition} ... />
  );
};
```

### 9.4 Monitoring & Alerts

**Real-Time Monitoring**:
- Page load time alerts: >5 seconds for 3+ consecutive requests
- Error rate alerts: >5% 5xx errors in 5-minute window
- Traffic spike alerts: >200% increase in 1 hour (positive or negative)

**Weekly Reports** (automated email):
- Top 10 brands by traffic
- Top 10 brands by conversions
- New brand partnerships
- SEO ranking changes for target keywords
- User feedback summary

**Monthly Business Review**:
- Traffic trends and forecast
- Conversion funnel analysis
- Brand partnership pipeline
- SEO performance vs. competitors
- Feature requests and roadmap updates

---

## 10. Risk Mitigation

### 10.1 Technical Risks

**Risk: Marketplace API Rate Limiting**
- **Impact**: Directory page fails to load if parallel brand fetches exceed rate limits
- **Likelihood**: Low-Medium
- **Mitigation**:
  - Limit parallel requests (max 24 brands fetched at once via pagination)
  - Implement exponential backoff for failed requests
  - Client-side caching of brand data in Redux store
  - Monitor API error rates in production
  - Consider implementing request queue for large brand counts
- **Contingency**: Display cached brands with "Updating..." indicator, implement retry mechanism

**Risk: Invalid Brand UUIDs in Configuration**
- **Impact**: Brand fetches fail, causing errors in directory or missing brands
- **Likelihood**: Low
- **Mitigation**:
  - Validate all brand UUIDs before adding to configBrands.js
  - Implement defensive filtering in fetch logic (filter out invalid responses)
  - Add error logging for failed brand fetches
  - Manual QA process when adding new brands
  - Consider adding automated validation script
- **Contingency**: Failed brand fetches are silently filtered out; remaining brands display normally

**Risk: Stale Brand Registry**
- **Impact**: Directory shows brands that are no longer active or misses new brands
- **Likelihood**: Medium-High
- **Mitigation**:
  - Establish regular review process (monthly) for brand registry
  - Monitor provider activity (listing counts, last login)
  - Create admin tools/scripts to identify inactive brands
  - Document clear process for adding/removing brands
  - Set up automated alerts for providers with zero listings
  - Future: Build admin UI for managing brand registry
- **Contingency**: Manual quarterly audit of all brands in registry

**Risk: Poor Page Performance**
- **Impact**: High bounce rates, low SEO rankings
- **Likelihood**: Medium
- **Mitigation**:
  - Limit parallel API requests (24 at a time via pagination)
  - Image optimization (WebP, lazy loading, responsive images)
  - Code splitting and lazy component loading
  - Client-side caching in Redux store
  - Regular performance audits (Lighthouse)
- **Contingency**: Implement progressive enhancement, reduce initial load, decrease perPage limit

### 10.2 Business Risks

**Risk: Low Brand Adoption**
- **Impact**: Directory looks empty, low trust from customers
- **Likelihood**: Medium
- **Mitigation**:
  - Launch with minimum 20 brands already onboarded
  - Proactive outreach to existing sellers
  - Incentives for early adopters (free featured placement)
  - Simplified onboarding process with step-by-step guide
- **Contingency**: Delay public launch, focus on brand recruitment

**Risk: Brand Profile Quality Issues**
- **Impact**: Incomplete profiles, low-quality content, broken links
- **Likelihood**: High
- **Mitigation**:
  - Profile completeness indicators (40%, 70%, 100%)
  - Required fields: logo, bio, at least 5 products
  - Manual review for featured brand applications
  - Automated checks for broken links, missing images
- **Contingency**: Admin tools to complete profiles, reach out to brands

**Risk: Competitive Response**
- **Impact**: Larger platforms (Amazon, Flipkart) launch similar features
- **Likelihood**: Medium
- **Mitigation**:
  - Focus on niche: authentic Indian organic baby brands
  - Stronger brand relationships through partnership program
  - Superior content quality and storytelling
  - Faster iteration and feature development
- **Contingency**: Double down on cultural authenticity and curation

### 10.3 User Experience Risks

**Risk: Information Overload**
- **Impact**: Users overwhelmed by too many brands, high bounce rate
- **Likelihood**: Medium (as brand count grows)
- **Mitigation**:
  - Smart defaults (featured brands first)
  - Effective filtering and search
  - "Recommended for you" personalization (future)
  - Category-based brand organization (future)
- **Contingency**: Reduce brands per page, add guided discovery flow

**Risk: Trust Signals Not Understood**
- **Impact**: Certification badges don't increase conversions
- **Likelihood**: Medium
- **Mitigation**:
  - Clear tooltips explaining each badge
  - Dedicated "Certifications" tab with details
  - Educational content about GOTS, BIS, etc.
  - A/B test badge designs and placement
- **Contingency**: Create video explainers, link to certification authority sites

**Risk: Mobile Experience Suffers**
- **Impact**: High mobile bounce rate (60%+ of traffic is mobile)
- **Likelihood**: Low (with proper testing)
- **Mitigation**:
  - Mobile-first design approach
  - Touch-friendly targets (48x48px minimum)
  - Sticky filters accessible without scrolling
  - Fast mobile page speeds (<3s)
- **Contingency**: Create separate mobile-optimized layout

### 10.4 SEO Risks

**Risk: Duplicate Content Issues**
- **Impact**: Google penalizes pages, low rankings
- **Likelihood**: Low
- **Mitigation**:
  - Unique content for each brand profile
  - Canonical URLs properly set
  - Robots.txt and meta robots tags correctly configured
  - Regular SEO audits with Screaming Frog
- **Contingency**: 301 redirects, consolidate duplicate pages

**Risk: Schema Validation Errors**
- **Impact**: No rich results in Google, lower CTR
- **Likelihood**: Low
- **Mitigation**:
  - Automated schema validation in CI/CD pipeline
  - Google's Structured Data Testing Tool in QA
  - Monitor Search Console for schema errors
  - Template-based schema generation (less error-prone)
- **Contingency**: Fix schema errors within 24 hours of detection

---

## 11. Appendix

### 11.1 Code Examples

#### Extended Data Configuration (`configUser.js`)

```javascript
export const userFields = [
  // User Type
  {
    key: 'userType',
    scope: 'public',
    schemaType: 'enum',
    enumOptions: [
      { option: 'brand-seller', label: 'Brand/Seller' },
      { option: 'individual-seller', label: 'Individual Seller' },
      { option: 'buyer', label: 'Buyer' }
    ],
    showConfig: {
      label: 'Account Type',
      displayInProfile: false
    },
    saveConfig: {
      label: 'I am a',
      displayInSignUp: true,
      isRequired: true,
      requiredMessage: 'Please select your account type'
    }
  },

  // Featured Brand Flag
  {
    key: 'isFeaturedBrand',
    scope: 'public',
    schemaType: 'boolean',
    showConfig: {
      label: 'Featured Brand',
      displayInProfile: false
    },
    saveConfig: {
      label: 'Apply for Featured Brand status',
      displayInSignUp: false,
      isRequired: false
    },
    userTypeConfig: {
      limitToUserTypeIds: true,
      userTypeIds: ['brand-seller']
    }
  },

  // Certifications
  {
    key: 'certifications',
    scope: 'public',
    schemaType: 'multi-enum',
    enumOptions: [
      { option: 'gots_certified', label: 'GOTS Certified' },
      { option: 'organic_cotton', label: '100% Organic Cotton' },
      { option: 'bis_approved', label: 'BIS Approved' },
      { option: 'non_toxic_dyes', label: 'Non-toxic Dyes' },
      { option: 'handcrafted', label: 'Handcrafted' },
      { option: 'fair_trade', label: 'Fair Trade' },
      { option: 'women_owned', label: 'Women-Owned Business' }
    ],
    showConfig: {
      label: 'Certifications',
      displayInProfile: true,
      placeholderMessage: 'Select all that apply'
    },
    saveConfig: {
      label: 'Brand Certifications',
      displayInSignUp: false,
      isRequired: false
    },
    userTypeConfig: {
      limitToUserTypeIds: true,
      userTypeIds: ['brand-seller']
    }
  },

  // Brand Logo URL (temporary until file upload)
  {
    key: 'brandLogoUrl',
    scope: 'public',
    schemaType: 'text',
    showConfig: {
      label: 'Brand Logo URL',
      displayInProfile: false,
      placeholderMessage: 'https://example.com/logo.png'
    },
    saveConfig: {
      label: 'Brand Logo URL',
      displayInSignUp: false,
      isRequired: false
    },
    userTypeConfig: {
      limitToUserTypeIds: true,
      userTypeIds: ['brand-seller']
    }
  },

  // Founded Year
  {
    key: 'foundedYear',
    scope: 'public',
    schemaType: 'long',
    showConfig: {
      label: 'Founded Year',
      displayInProfile: true,
      placeholderMessage: '2015'
    },
    saveConfig: {
      label: 'Year Founded',
      displayInSignUp: false,
      isRequired: false
    },
    userTypeConfig: {
      limitToUserTypeIds: true,
      userTypeIds: ['brand-seller']
    }
  },

  // Origin
  {
    key: 'origin',
    scope: 'public',
    schemaType: 'text',
    showConfig: {
      label: 'Origin',
      displayInProfile: true,
      placeholderMessage: 'Mumbai, India'
    },
    saveConfig: {
      label: 'Brand Origin (City, State)',
      displayInSignUp: false,
      isRequired: false
    },
    userTypeConfig: {
      limitToUserTypeIds: true,
      userTypeIds: ['brand-seller']
    }
  },

  // Specialty
  {
    key: 'specialty',
    scope: 'public',
    schemaType: 'text',
    showConfig: {
      label: 'Specialty',
      displayInProfile: true,
      placeholderMessage: 'Organic baby clothing'
    },
    saveConfig: {
      label: 'Brand Specialty',
      displayInSignUp: false,
      isRequired: false
    },
    userTypeConfig: {
      limitToUserTypeIds: true,
      userTypeIds: ['brand-seller']
    }
  },

  // Website URL
  {
    key: 'websiteUrl',
    scope: 'public',
    schemaType: 'text',
    showConfig: {
      label: 'Website',
      displayInProfile: true,
      placeholderMessage: 'https://example.com'
    },
    saveConfig: {
      label: 'Brand Website',
      displayInSignUp: false,
      isRequired: false
    },
    userTypeConfig: {
      limitToUserTypeIds: true,
      userTypeIds: ['brand-seller']
    }
  }
];
```

#### Translation Strings (`en.json`)

```json
{
  "BrandsPage.title": "Indian Organic Baby Brands | {brandCount}+ GOTS Certified Brands | Mela",
  "BrandsPage.description": "Discover {brandCount}+ verified Indian organic baby brands. Shop GOTS certified clothing, natural care products, and handcrafted toys. Trusted by 10,000+ parents.",
  "BrandsPage.heroTitle": "Discover India's Most Trusted Organic Baby Brands",
  "BrandsPage.heroSubtitle": "Curated collection of {brandCount}+ GOTS certified brands creating safe, sustainable products for your little one. Every brand is verified, every product is authentic, every purchase supports Indian artisans.",
  "BrandsPage.ctaExploreAll": "Explore All Brands",
  "BrandsPage.ctaBecomePartner": "Become a Partner Brand",
  "BrandsPage.featuredBrandsTitle": "Featured Brands",
  "BrandsPage.allBrandsTitle": "All Brands",
  "BrandsPage.sortLabel": "Sort by:",
  "BrandsPage.sortAlphabetical": "Alphabetical (A-Z)",
  "BrandsPage.sortFeatured": "Featured First",
  "BrandsPage.sortMostProducts": "Most Products",
  "BrandsPage.sortNewest": "Newest First",
  "BrandsPage.perPageLabel": "Show:",
  "BrandsPage.perPage12": "12 per page",
  "BrandsPage.perPage24": "24 per page",
  "BrandsPage.perPage48": "48 per page",
  "BrandsPage.searchPlaceholder": "Search brands...",
  "BrandsPage.emptyStateTitle": "No brands match your current filters",
  "BrandsPage.emptyStateDescription": "We're adding new brands every week! Try adjusting your filters or sign up below to get notified when brands matching your criteria join Mela.",
  "BrandsPage.emptyStateCtaAdjust": "Adjust Filters",
  "BrandsPage.emptyStateCtaNotify": "Notify Me",
  "BrandsPage.loadingState": "Discovering amazing brands for you...",

  "BrandCard.productCount": "{count, plural, one {# Product} other {# Products}}",
  "BrandCard.productCountAvailable": "{count, plural, one {# Product Available} other {# Products Available}}",
  "BrandCard.ctaShop": "Shop Brand",
  "BrandCard.ctaViewProfile": "View Profile",
  "BrandCard.featuredBadge": "Featured",
  "BrandCard.ariaLabel": "View {brandName} profile. {certificationCount} certifications. {productCount} products available.",

  "BrandProfilePage.title": "{brandName} - {tagline} | Authentic Indian Baby Products | Mela",
  "BrandProfilePage.description": "{brandName} - {bio}. {certification}. Shop {productCount}+ authentic products on Mela.",
  "BrandProfilePage.tabProducts": "Products",
  "BrandProfilePage.tabStory": "Our Story",
  "BrandProfilePage.tabCertifications": "Certifications",
  "BrandProfilePage.tabReviews": "Reviews",
  "BrandProfilePage.ctaShopAll": "Shop All Products",
  "BrandProfilePage.ctaVisitWebsite": "Visit Website",
  "BrandProfilePage.ctaShare": "Share",
  "BrandProfilePage.statsProducts": "{count, plural, one {# Product} other {# Products}}",
  "BrandProfilePage.statsRating": "⭐ {rating} ({reviewCount} reviews)",
  "BrandProfilePage.statsEstablished": "Est. {year}",
  "BrandProfilePage.certificationIssuedBy": "Issued by: {issuer}",
  "BrandProfilePage.certificationNumber": "Certificate #: {number}",
  "BrandProfilePage.certificationValidThrough": "Valid through: {date}",
  "BrandProfilePage.certificationLearnMore": "Learn More",
  "BrandProfilePage.certificationViewCertificate": "View Certificate",

  "BrandBadge.gots_certified": "GOTS Certified",
  "BrandBadge.organic_cotton": "Organic Cotton",
  "BrandBadge.bis_approved": "BIS Approved",
  "BrandBadge.non_toxic_dyes": "Non-toxic Dyes",
  "BrandBadge.handcrafted": "Handcrafted",
  "BrandBadge.fair_trade": "Fair Trade",
  "BrandBadge.women_owned": "Women-Owned",
  "BrandBadge.made_in_india": "Made in India",
  "BrandBadge.verified_seller": "Verified Seller",

  "BrandBadgeTooltip.gots_certified": "Verified organic cotton grown without pesticides or GMOs, processed with non-toxic dyes",
  "BrandBadgeTooltip.verified_seller": "Identity verified by Mela team, background checked, committed to quality standards",
  "BrandBadgeTooltip.featured_brand": "Hand-selected by Mela for exceptional quality, customer reviews, and sustainable practices",
  "BrandBadgeTooltip.made_in_india": "Proudly crafted in India, supporting local artisans and traditional craftsmanship",
  "BrandBadgeTooltip.women_owned": "Owned and operated by women entrepreneurs",
  "BrandBadgeTooltip.fair_trade": "Fair wages, safe working conditions, and community development verified",
  "BrandBadgeTooltip.bis_approved": "Meets Bureau of Indian Standards safety requirements for baby products",
  "BrandBadgeTooltip.non_toxic_dyes": "Natural or non-toxic synthetic dyes, free from harmful chemicals"
}
```

### 11.2 Technical Requirements Summary

**Backend**:
- Sharetribe Flex/Go marketplace with Marketplace API access
- Node.js server (existing) - no custom API endpoints required
- Brand registry configuration file (configBrands.js)
- Provider user type configured in Sharetribe Console

**Frontend**:
- React 16.8+ (existing)
- Redux for state management (existing)
- sharetribe-flex-sdk for Marketplace API calls (existing)
- Transit-js for API response parsing (existing)

**Third-Party Services**:
- Google Analytics 4 for tracking
- Google Search Console for SEO monitoring
- Google Optimize or custom A/B testing (optional)
- CDN for image delivery (Cloudflare, Cloudinary, or Sharetribe's built-in)

**Browser Support**:
- Chrome/Edge (last 2 versions)
- Safari (last 2 versions)
- Firefox (last 2 versions)
- iOS Safari 12+
- Android Chrome 80+

### 11.3 Glossary

**Terms**:
- **Brand Profile**: User account representing a brand/seller with extended data
- **Featured Brand**: Brand with `publicData.isFeaturedBrand = true`, gets prominent placement
- **Extended Data**: Custom fields on User profiles (publicData, privateData, metadata)
- **Integration API**: Sharetribe's server-side API for advanced queries (vs. Marketplace API)
- **Search Schema**: Configuration defining which extended data fields are queryable
- **Trust Badge**: Visual indicator of certification or verification status
- **Schema.org**: Structured data vocabulary for SEO rich results

**Acronyms**:
- **GOTS**: Global Organic Textile Standard
- **BIS**: Bureau of Indian Standards
- **SEO**: Search Engine Optimization
- **CTR**: Click-Through Rate
- **CTA**: Call To Action
- **GA4**: Google Analytics 4
- **LCP**: Largest Contentful Paint
- **FID**: First Input Delay
- **CLS**: Cumulative Layout Shift

---

## Conclusion

This PRD outlines a comprehensive approach to building a Brands page for Mela marketplace that serves multiple business goals: SEO-driven traffic acquisition, brand partnership development, and enhanced product discovery for customers.

**Key Success Factors**:

1. **Technical Simplicity**: Curated brand registry with Marketplace API for simple, performant brand directory - no complex server-side infrastructure required

2. **Quality Control**: Manual curation ensures only verified, high-quality brands appear in directory, building trust with customers

3. **User-Centric Design**: Alphabetical directory with featured brands, mobile-first responsive design, and clear trust signals to build confidence with new visitors

4. **Content Quality**: Authentic brand storytelling with verified certifications, transparent sourcing, and cultural connection to Indian heritage

5. **SEO Optimization**: Schema.org structured data, rich meta tags, and performance optimization to capture organic search traffic for brand-related queries

6. **Data-Driven Iteration**: Comprehensive analytics, A/B testing framework, and continuous optimization based on user behavior

**Strategic Advantages for Mela**:

- **Differentiation**: No other marketplace focuses exclusively on curated Indian organic baby brands with this level of verification and storytelling
- **Partnership Value**: Brands get dedicated profiles and marketing exposure, strengthening relationships
- **Customer Trust**: Transparent certification details and brand stories reduce purchase anxiety for new parents
- **Organic Growth**: SEO-optimized brand pages become evergreen traffic drivers and backlink generators

**Next Steps**:
1. Approve this PRD with stakeholders
2. Prioritize Phase 1 (Backend Setup) for immediate start
3. Recruit initial 20+ brands for launch inventory
4. Set up analytics and monitoring infrastructure
5. Begin development with 8-week timeline to launch

With proper execution, the Brands page will become a cornerstone of Mela's value proposition, driving sustained organic growth while creating a win-win ecosystem for brands and customers alike.
