# Search Page Optimization PRD

**Document Owner:** Product Team
**Last Updated:** November 21, 2025
**Status:** Draft
**Priority:** High

---

## Executive Summary

This PRD outlines comprehensive improvements to Mela's search and filtering experience based on analysis of best-in-class marketplaces (Amazon, Etsy, Zappos) and established UX research from Baymard Institute and Algolia. Currently, only 16% of major ecommerce sites provide a good filtering experience, presenting a significant opportunity for Mela to differentiate through superior search UX.

**Key Goals:**
- Increase conversion rate by 5-10% through improved product discoverability
- Reduce search abandonment by making filters more intuitive and contextual
- Improve mobile search experience with optimized touch interactions
- Enable users to find products faster with smart filtering and sorting

---

## Problem Statement

### Current Pain Points

Based on analysis of Mela's current implementation:

1. **Limited Filter Visibility**: Filters are present but may not be prominent enough for quick product refinement
2. **Generic Sorting Options**: Only basic sorting (price, date) without category-specific sort types
3. **No Faceted Sorting**: Users can't combine scope and sorting in one action (e.g., "Baby Clothing by: Lowest Price")
4. **Missing Result Count Indicators**: Filters don't show how many products match each option
5. **Mobile Experience Gap**: Desktop-first filter design may not optimize for mobile browsing patterns
6. **Limited Filter Context**: No visual confirmation of active filters or easy removal
7. **Zero-Result Scenarios**: Potential for filter combinations that return no results

### User Impact

- **Discovery Challenge**: Users struggle to browse and discover products efficiently
- **Search Friction**: Multiple steps required to narrow down to desired products
- **Abandonment Risk**: Poor filter UX leads to frustration and site abandonment
- **Mobile Frustration**: Suboptimal mobile experience drives users away

---

## Goals & Success Metrics

### Primary Goals

1. **Improve Product Discoverability**: Enable users to find products through both search (findability) and browsing (discoverability)
2. **Reduce Time to Purchase**: Decrease clicks and time from search to product selection
3. **Increase Mobile Conversions**: Optimize for mobile-first shopping experience
4. **Enhance User Satisfaction**: Create intuitive, frustration-free filtering experience

### Success Metrics

| Metric | Current Baseline | Target | Timeline |
|--------|-----------------|--------|----------|
| Conversion Rate (Search → Purchase) | TBD | +5-10% | 3 months |
| Search Abandonment Rate | TBD | -15% | 3 months |
| Filter Engagement Rate | TBD | +30% | 2 months |
| Average Time to Product Selection | TBD | -20% | 2 months |
| Mobile Conversion Rate | TBD | +10% | 3 months |
| Zero-Result Filter Combinations | TBD | <5% | 1 month |

### Secondary Metrics

- Filters applied per session
- Search refinement rate
- Add-to-cart rate from search results
- Return visit rate from search users
- Mobile filter usage rate

---

## Target Users

### Primary Personas

1. **Indian Diaspora Parents (Primary)**
   - Age: 28-40
   - Tech-savvy, mobile-first
   - Looking for authentic Indian baby products
   - Values: Quality, cultural connection, convenience
   - Behavior: Comparison shoppers, review-conscious

2. **Gift Buyers**
   - Age: 25-45
   - Occasional buyers for friends/family
   - Need quick, confident purchasing
   - Values: Reliability, uniqueness, fast shipping

3. **Traditional Clothing Seekers (Future)**
   - Age: 25-50
   - Searching for ethnic wear, home decor
   - Values: Authenticity, quality, cultural significance

---

## Research Findings

### Industry Best Practices

Based on analysis of top marketplaces and UX research:

#### 1. **Filter Design Principles** (Source: Algolia, The Good)

- **Choose Relevant Filters**: Age group, material, certification are perfect for baby products
- **Show Result Counts**: Display number of products for each filter option (dynamically updates)
- **Allow Simultaneous Filtering & Sorting**: Users need both capabilities at once
- **Easy Filter Removal**: Clear visual indicators and simple removal mechanism
- **Mobile Optimization**: Separate list-browsing and filter-edit modes

#### 2. **Faceted Sorting** (Source: Baymard Institute)

- **Problem**: Sorting site-wide searches by price shows irrelevant accessories instead of desired products
- **Solution**: Suggest category scope before allowing sort, or combine scope + sort in one action
- **Example**: "Baby Clothing by: Lowest Price" applies both category filter and sorting
- **Benefit**: 42% fewer confused users, faster path to relevant products

#### 3. **Filter Organization** (Source: The Good - 25 Best Practices)

- **Order by Importance**: Not alphabetically (Amazon pattern)
- **Category-Specific Filters**: Different products need different filters
- **Thematic Filters**: Group by use cases (occasion, season, age range)
- **Visual Confirmation**: Active filters clearly distinguished with color/icons
- **Prevent Over-Filtering**: Show product count to prevent zero results
- **Allow Multiple Values**: Select multiple sizes, colors, materials simultaneously

#### 4. **Mobile-Specific Patterns**

- **Top-Right Placement**: Users expect filter access in top-right corner
- **Full vs. Partial Screen**: Full screen for specific searches (Airbnb), partial for exploration (Amazon)
- **Horizontal Filter Bars**: For simpler filter sets on mobile
- **Collapsible Groups**: Reduce cognitive load, show only relevant filters

---

## Proposed Solution

### 1. Enhanced Filter System

#### 1.1 Result Count Indicators

**Feature**: Display product count for each filter option

```
Material:
☐ Organic Cotton (47)
☐ Bamboo (23)
☐ Cotton Jersey (31)
☐ Muslin (12)
```

**Implementation**:
- Query Sharetribe API for facet counts
- Update counts dynamically as filters are applied
- Gray out or hide options with zero results

**Priority**: P0 (High Impact)

#### 1.2 Active Filter Display

**Feature**: Show all active filters with easy removal

```
Active Filters: [Age: 0-6 months ✕] [Material: Organic Cotton ✕] [Clear All]
```

**Implementation**:
- Display active filters as removable chips/badges
- Place at top of search results
- Include "Clear All" option
- Visual distinction (color, border) from inactive filters

**Priority**: P0 (High Impact)

#### 1.3 Category-Specific Filters

**Feature**: Show different filters based on product category

**Baby Clothing**:
- Age Group, Material, Color, Size, Certification, Key Features

**Baby Gear** (Future):
- Age Group, Safety Certification, Material, Weight Capacity

**Traditional Clothing** (Future):
- Occasion, Season, Style, Fabric, Region

**Implementation**:
- Extend configListing.js with category-specific filter configurations
- Conditionally render filters based on active category
- Use existing `isFieldForCategory` utility function

**Priority**: P1 (Medium Priority)

#### 1.4 Multi-Select Within Same Filter

**Feature**: Allow selecting multiple values in same filter type

**Example**:
```
Size:
☑ 0-6 months
☑ 6-12 months
☐ 12-18 months
```

**Current Status**: Already supported via multi-enum schema type
**Action Needed**: Verify UX makes this capability clear to users

**Priority**: P2 (Validation)

---

### 2. Faceted Sorting Implementation

#### 2.1 Smart Sort Suggestions

**Feature**: Suggest category-specific sorting when scope is clear

**Example - Search: "Baby Onesies"**

```
Sort by:
┌─────────────────────────────────┐
│ Baby Clothing by: Lowest Price  │ <- Faceted Sort
│ Baby Clothing by: Newest        │ <- Faceted Sort
│ Baby Clothing by: Best Rated    │ <- Faceted Sort
├─────────────────────────────────┤
│ All Results by: Price           │ <- Generic Sort
│ All Results by: Date            │ <- Generic Sort
└─────────────────────────────────┘
```

**Implementation**:
1. Detect high-relevance category from search query
2. Display category-specific sort options at top
3. Include generic sort options below separator
4. Apply both scope filter and sort when selected

**Technical Approach**:
- Extend sortConfig in configSearch.js with faceted sort logic
- Add relevance threshold for suggesting faceted sorts
- Create new sort option type: `{ key: 'baby_clothing_price', scope: 'baby_clothing', sort: 'price' }`

**Priority**: P0 (High Differentiation)

#### 2.2 Category-Specific Sort Types

**Feature**: Offer sorting options unique to product categories

**Baby Products**:
- Sort by: Age Group (youngest first)
- Sort by: Safety Rating
- Sort by: Softness (material quality)

**Traditional Clothing** (Future):
- Sort by: Formality (casual to formal)
- Sort by: Season (current season first)

**Implementation**:
- Define category-specific sort types in configListing.js
- Map to backend API meta-fields or computed scores
- Display only when category filter is active

**Priority**: P1 (Enhancement)

---

### 3. Mobile Optimization

#### 3.1 Dual-Mode Interface

**Feature**: Separate list-browsing and filter-edit modes

**List-Browsing Mode**:
- Primary focus on product grid
- Sticky filter button (top-right)
- Active filters shown as removable chips
- Quick sort dropdown

**Filter-Edit Mode**:
- Full-screen filter panel (slide in from right)
- All filter groups visible
- "Apply Filters" button at bottom
- Product count preview updates live

**Implementation**:
- Create mobile-specific SearchFiltersMobile component (exists)
- Enhance with full-screen overlay mode
- Add bottom sheet animation
- Include live result count

**Priority**: P0 (Mobile-First)

#### 3.2 Filter Placement & Design

**Mobile**:
- Filter button: Top-right corner (user expectation)
- Icon: Three horizontal lines or funnel icon
- Badge showing number of active filters

**Desktop**:
- Left sidebar (current approach is good)
- Collapsible filter groups
- Sticky positioning during scroll

**Priority**: P1 (UX Enhancement)

---

### 4. Zero-Result Prevention

#### 4.1 Smart Filter Hiding

**Feature**: Hide or disable filters that would return zero results

**Implementation**:
- Query available facet combinations before rendering
- Gray out options that would return empty results
- Show tooltip: "No products match this combination"
- Alternative: Remove options entirely

**Trade-offs**:
- Pro: Prevents user frustration
- Con: May hide options user expects to see
- Decision: Gray out with tooltip (transparent approach)

**Priority**: P1 (Quality of Life)

#### 4.2 Related Products Suggestion

**Feature**: When filters return zero results, suggest related products

**Example**:
```
No products found for: Age 0-6 months + Organic Cotton + Blue

Try:
- View all Organic Cotton products (47 items)
- View all Blue baby products (23 items)
- Remove a filter to see more options
```

**Priority**: P2 (Nice to Have)

---

### 5. Filter Performance & Speed

#### 5.1 Instant Filter Response

**Feature**: Sub-300ms filter application

**Implementation**:
- Client-side filter state management
- Debounced API calls (300ms)
- Optimistic UI updates
- Loading skeleton for results

**Technical Notes**:
- Current Redux architecture supports this
- May need query optimization on backend
- Consider adding filter result cache

**Priority**: P0 (Performance)

#### 5.2 Filter Preloading

**Feature**: Preload filter facet counts on page load

**Implementation**:
- Fetch facet counts alongside search results
- Cache in Redux store
- Update incrementally as filters applied

**Priority**: P1 (Performance)

---

### 6. Advanced Features (Future)

#### 6.1 Saved Searches & Filters

**Feature**: Allow users to save frequent search + filter combinations

**Use Case**: Parent shopping for 6-12 month organic cotton clothes regularly

**Priority**: P3 (Future)

#### 6.2 Smart Filter Suggestions

**Feature**: ML-based suggestions based on user behavior

**Example**: "Most parents also filter by: Organic Cotton, GOTS Certified"

**Priority**: P3 (Future)

#### 6.3 Filter History

**Feature**: Recently used filters appear at top

**Priority**: P3 (Future)

---

## Technical Implementation

### Phase 1: Foundation (Weeks 1-2)

**Goal**: Implement core filter improvements

1. **Result Count Indicators**
   - Modify SearchPage.duck.js to fetch facet counts
   - Update FilterComponent to display counts
   - Add dynamic count updates on filter change

2. **Active Filter Display**
   - Create ActiveFiltersBar component
   - Implement filter removal logic
   - Style as removable chips

3. **Mobile Filter Optimization**
   - Enhance SearchFiltersMobile component
   - Implement full-screen mode
   - Add bottom apply button with live count

**Files to Modify**:
- `/web-client/src/containers/SearchPage/SearchPage.duck.js`
- `/web-client/src/containers/SearchPage/FilterComponent.js`
- `/web-client/src/containers/SearchPage/SearchFiltersMobile/SearchFiltersMobile.js`
- `/web-client/src/containers/SearchPage/SearchPage.module.css`

### Phase 2: Faceted Sorting (Weeks 3-4)

**Goal**: Implement smart sorting with category suggestions

1. **Faceted Sort Logic**
   - Extend configSearch.js sortConfig structure
   - Add relevance detection for category scoping
   - Create FacetedSortBy component

2. **Category-Specific Sort Types**
   - Define category-specific sort options in configListing.js
   - Map to backend sort parameters
   - Conditionally display based on active category

**Files to Create/Modify**:
- `/web-client/src/containers/SearchPage/SortBy/FacetedSortBy.js` (new)
- `/web-client/src/config/configSearch.js`
- `/web-client/src/config/configListing.js`
- `/web-client/src/containers/SearchPage/SearchPage.shared.js`

### Phase 3: Quality & Performance (Weeks 5-6)

**Goal**: Polish and optimize

1. **Zero-Result Prevention**
   - Add facet availability checking
   - Implement gray-out styling for unavailable filters
   - Add helpful tooltips

2. **Performance Optimization**
   - Implement filter result caching
   - Add optimistic UI updates
   - Optimize bundle size

3. **Testing & Refinement**
   - A/B test key changes (faceted sort, result counts)
   - Mobile usability testing
   - Performance benchmarking

---

## Backend Requirements

### Sharetribe API Enhancements Needed

1. **Facet Count Query**
   - Current: Sharetribe API supports facet counts via meta parameter
   - Action: Ensure all custom fields return facet counts
   - Endpoint: `/listings/query` with meta parameter

2. **Category-Specific Sorting**
   - Current: Generic sort parameters (price, createdAt)
   - Needed: Support for custom meta field sorting (age_group, material_quality)
   - Action: May need Integration API to add custom sort indices

3. **Filter Combination Validation**
   - Needed: Endpoint to check if filter combination returns results
   - Workaround: Client-side checks using facet counts

---

## Design Specifications

### Visual Design Updates

#### Filter Components

**Result Count Badge**:
```
Font: Inter 12px
Color: #6B7280 (gray-500)
Position: Right-aligned after filter label
Format: (23) - parentheses, no comma separator
```

**Active Filter Chips**:
```
Background: #DBEAFE (blue-100)
Border: 1px solid #3B82F6 (blue-500)
Text: #1E40AF (blue-800)
Close icon: #3B82F6 (blue-500)
Padding: 6px 12px
Border radius: 16px (pill shape)
```

**Clear All Button**:
```
Text: "Clear All"
Color: #EF4444 (red-500)
Font weight: 500
Underline on hover
```

#### Mobile Filter Modal

```
Overlay: rgba(0, 0, 0, 0.5)
Panel: Slide in from right, 90% width
Animation: 300ms ease-out
Close button: Top-left
Apply button: Fixed bottom, full width, primary color
```

### Interaction Patterns

**Filter Selection**:
- Checkbox visual feedback: 100ms
- Result count update: <300ms
- Product grid refresh: <500ms

**Mobile Filter Modal**:
- Open: Tap filter button, slide in animation
- Close: Tap outside, swipe right, or tap X
- Apply: Tap "Apply Filters" button

---

## A/B Testing Plan

### Test 1: Result Count Indicators

**Hypothesis**: Showing result counts will increase filter engagement by 25%

**Variants**:
- Control: Current filter UI without counts
- Variant A: Result counts shown
- Variant B: Result counts + hide zero-result options

**Metrics**:
- Filter engagement rate
- Filters applied per session
- Conversion rate

**Duration**: 2 weeks

### Test 2: Faceted Sorting

**Hypothesis**: Faceted sorting will reduce search abandonment by 15%

**Variants**:
- Control: Generic sorting only
- Variant A: Faceted sort suggestions (top of dropdown)
- Variant B: Faceted sort suggestions + category-specific types

**Metrics**:
- Search abandonment rate
- Sort usage rate
- Time to product selection
- Conversion rate

**Duration**: 2 weeks

### Test 3: Mobile Filter UI

**Hypothesis**: Full-screen filter mode will increase mobile conversions by 10%

**Variants**:
- Control: Current partial overlay
- Variant A: Full-screen filter modal
- Variant B: Bottom sheet drawer

**Metrics**:
- Mobile filter engagement
- Mobile conversion rate
- Mobile bounce rate

**Duration**: 2 weeks

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Sharetribe API limitations for faceted sorting | High | Medium | Use client-side filtering + server-side sorting as workaround |
| Performance degradation with complex filters | Medium | Medium | Implement aggressive caching, optimize queries |
| User confusion with new sorting options | Medium | Low | Clear labeling, tooltips, gradual rollout |
| Mobile filter modal breaks existing flows | High | Low | Extensive mobile testing, feature flag |
| Zero-result scenarios frustrate users | Medium | Medium | Smart filter hiding + helpful suggestions |
| Backend query load increases | Medium | Medium | Implement query caching, rate limiting |

---

## Open Questions

1. **Faceted Sorting API Support**: Does Sharetribe API support applying category filter + sort in single query efficiently?
   - Action: Test API behavior, document limitations
   - Owner: Engineering

2. **Filter Order Optimization**: Should filter order be dynamic based on user behavior or category?
   - Action: Analyze user data, consult with analytics
   - Owner: Product + Data

3. **Mobile Filter Button Placement**: Top-right or bottom floating action button?
   - Action: Mobile usability testing
   - Owner: Design

4. **Category Detection Threshold**: What relevance score qualifies for faceted sort suggestions?
   - Action: Test with various thresholds (70%, 80%, 90%)
   - Owner: Engineering + Product

---

## Success Criteria

### Launch Readiness Checklist

**Functionality**:
- [ ] Result counts display correctly on all filters
- [ ] Active filters show as removable chips
- [ ] Mobile filter modal works on all devices
- [ ] Faceted sorting suggestions appear for relevant searches
- [ ] Zero-result filters are hidden/grayed out
- [ ] Filter performance <300ms response time

**Quality**:
- [ ] Cross-browser testing complete (Chrome, Safari, Firefox, Edge)
- [ ] Mobile testing on iOS and Android
- [ ] Accessibility audit passed (keyboard navigation, screen readers)
- [ ] Performance benchmarks met (Lighthouse score >90)

**Business**:
- [ ] A/B tests show positive results (or neutral)
- [ ] Analytics tracking in place for all new features
- [ ] Documentation updated for team

---

## Timeline & Milestones

### Month 1
- **Week 1-2**: Phase 1 (Foundation)
  - Result count indicators
  - Active filter display
  - Mobile optimization

- **Week 3-4**: Phase 2 (Faceted Sorting)
  - Faceted sort implementation
  - Category-specific sort types

### Month 2
- **Week 5-6**: Phase 3 (Quality & Performance)
  - Zero-result prevention
  - Performance optimization
  - Testing

- **Week 7-8**: A/B Testing & Iteration
  - Run A/B tests
  - Analyze results
  - Iterate based on findings

### Month 3
- **Week 9-10**: Final Polish
  - Address feedback
  - Additional optimizations
  - Documentation

- **Week 11-12**: Full Rollout
  - Gradual rollout to 100%
  - Monitor metrics
  - Support & bug fixes

---

## Dependencies

**Internal**:
- Design team: UI mockups and design system updates
- Engineering: Frontend and backend implementation
- QA: Testing across devices and browsers
- Analytics: Tracking setup and dashboard creation
- Marketing: Communication of improved search experience

**External**:
- Sharetribe API: Facet count support, custom sorting capabilities
- Third-party services: None identified

---

## Post-Launch Plan

### Monitoring (First 30 Days)

**Key Metrics Dashboard**:
- Search conversion rate (daily)
- Filter engagement rate (daily)
- Mobile vs. desktop performance (weekly)
- Zero-result occurrences (daily)
- Page load times (daily)
- Error rates (real-time alerts)

### Iteration Plan

**Week 1-2 Post-Launch**:
- Monitor for critical issues
- Hot-fix any blocking bugs
- Collect user feedback

**Week 3-4 Post-Launch**:
- Analyze A/B test results
- Plan iteration cycle 1
- Address top user pain points

**Month 2-3 Post-Launch**:
- Implement learnings from data
- Plan advanced features (saved searches, smart suggestions)
- Optimize based on usage patterns

---

## Appendix

### Research Sources

1. **Algolia - Search Filter UX Best Practices**
   - 5 core principles for filter design
   - Mobile optimization patterns
   - Performance considerations

2. **The Good - 25 Ecommerce Product Filters Best Practices**
   - Comprehensive filter design strategies
   - Case study: Fully furniture (5.97% conversion lift)
   - 25 specific tactical recommendations

3. **Baymard Institute - Faceted Sorting**
   - Research on sorting site-wide searches
   - Faceted sorting concept and implementation
   - 3 solution approaches with trade-offs

### Competitive Analysis

**Amazon**:
- Disables site-wide sorting, suggests category first
- Excellent faceted navigation
- Result counts on all filters

**Etsy**:
- Category-specific attributes as filters
- Multi-select within filters
- Strong mobile experience

**Zappos**:
- Clear active filter display
- Easy filter removal
- Multiple value selection within same filter type

### Technical References

- Sharetribe Flex CLI documentation for search schemas
- Current Mela implementation: configSearch.js, configListing.js
- SearchPage architecture: SearchPage.shared.js, SearchPage.duck.js

---

## Approval & Sign-off

| Role | Name | Date | Status |
|------|------|------|--------|
| Product Manager | TBD | - | Pending |
| Engineering Lead | TBD | - | Pending |
| Design Lead | TBD | - | Pending |
| Stakeholder | TBD | - | Pending |

---

**Document Version History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-21 | Product Team | Initial draft based on research and analysis |

