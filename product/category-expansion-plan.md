# Category Expansion Todo List

## Overview

This document outlines the steps needed to expand the Laem marketplace from baby/children products to additional product categories. The current system is optimized for Indian baby products but needs modifications to support broader categories while maintaining data quality and consistency.

---

## Phase 1: Infrastructure Preparation

### 1.1 LLM Classifier Updates

#### Current State
- [x] Baby/children-focused attribute structure implemented
- [x] Hardcoded baby-specific examples and age groups
- [x] Single category approach in `category_classifier.py`
- [x] Age group attributes standardized to 6-month ranges (Premie, Newborn, 0-6m, 6-12m, 12-18m, 18-24m)

#### Todo Items
- [ ] **Implement Category Detection Logic**
  - Create `_detect_category_type()` method in `LLMClassifier` class
  - Add category keyword mapping (baby, clothing, electronics, home, etc.)
  - Analyze product batch to determine primary category type

- [ ] **Create Universal Attribute Structure**
  - Design `_get_universal_attributes()` with cross-category attributes:
    - Material, Type, Size, Color, Features, Brand
    - Certification, Care, Warranty (as applicable)
  - Remove baby-specific attributes from universal set

- [ ] **Build Category-Specific Extensions**
  - `_get_baby_attributes()`: Age Group (Premie, Newborn, 0-6m, 6-12m, 12-18m, 18-24m), Function, Safety features
  - `_get_clothing_attributes()`: Fit, Occasion, Season, Gender
  - `_get_electronics_attributes()`: Power, Connectivity, Compatibility
  - `_get_home_attributes()`: Room, Style, Capacity, Usage
  - `_get_food_attributes()`: Ingredients, Nutrition, Shelf Life, Dietary
  - `_get_beauty_attributes()`: Skin Type, Application, Ingredients

- [ ] **Update `_create_batch_prompt()` Method**
  - Make attribute structure dynamic based on category type
  - Replace hardcoded baby examples with category-appropriate examples
  - Implement fallback to universal attributes for unknown categories

- [ ] **Update System Message Guidelines**
  - Remove baby-specific language from core guidelines
  - Add category-agnostic classification principles
  - Update examples to be more universal

### 1.2 Category Hierarchy Updates

#### Current State
- [x] Baby clothing category mapping CSV exists
- [x] 2-level and 3-level category structures defined

#### Todo Items
- [ ] **Create Category Mapping Files for New Verticals**
  - `clothing_categories.csv` - Adult clothing hierarchy
  - `electronics_categories.csv` - Electronics and gadgets
  - `home_kitchen_categories.csv` - Home and kitchen products
  - `beauty_personal_care_categories.csv` - Beauty and personal care
  - `food_grocery_categories.csv` - Food and grocery items

- [ ] **Update Category Loading Logic**
  - Modify `_load_marketplace_categories()` to handle multiple category files
  - Implement category file selection based on product type
  - Create master category index for cross-category products

- [ ] **Standardize Category Naming Convention**
  - Define consistent naming patterns across all categories
  - Implement category validation rules
  - Create category mapping documentation

---

## Phase 2: Scraper Infrastructure

### 2.1 Multi-Category Scraper Framework

#### Current State
- [x] Individual brand scrapers for baby products exist
- [x] Uniform CSV output format established

#### Todo Items
- [ ] **Create Category-Specific Scraper Templates**
  - `clothing_scraper_template.py` - Adult clothing sites
  - `electronics_scraper_template.py` - Electronics sites  
  - `home_scraper_template.py` - Home goods sites
  - `beauty_scraper_template.py` - Beauty/personal care sites

- [ ] **Update Base Scraper Class**
  - Add category detection from website structure
  - Implement category-specific field extraction
  - Add validation for category-appropriate data fields

- [ ] **Enhance Data Validation**
  - Category-specific required fields validation
  - Price format validation for different product types
  - Image URL validation and quality checks

### 2.2 New Brand Integration Pipeline

#### Todo Items
- [ ] **Research Target Categories for Indian Diaspora**
  - **Clothing & Fashion**: Traditional Indian wear, ethnic fashion brands
  - **Home & Kitchen**: Indian cookware, home decor, furniture brands  
  - **Beauty & Personal Care**: Ayurvedic beauty, traditional skincare brands
  - **Food & Grocery**: Indian spices, ready-to-eat meals, traditional foods
  - **Electronics**: Indian electronics brands popular in diaspora

- [ ] **Identify High-Priority Brands per Category**
  - Analyze diaspora shopping patterns and preferences
  - Research brand availability and affiliate program opportunities
  - Create priority matrix based on demand and feasibility

- [ ] **Create Brand Research Documentation**
  - `brand-research-clothing.md` - Traditional wear, ethnic fashion
  - `brand-research-home.md` - Cookware, decor, furniture
  - `brand-research-beauty.md` - Ayurvedic, natural beauty brands
  - `brand-research-food.md` - Spices, ready meals, traditional foods

---

## Phase 3: Frontend & Configuration Updates

### 3.1 Sharetribe Configuration

#### Current State
- [x] Baby product categories configured
- [x] Brand field implemented for baby products
- [x] Basic search and filtering working
- [x] Extended data fields configured in `configListing.js` (age_group, material, certification, color, key_features)
- [x] Search schema application script created (`apply-search-schemas.sh`)

#### Todo Items
- [ ] **Apply Search Schemas to Sharetribe Backend**
  - Install Sharetribe CLI: `npm install -g @sharetribe/flex-cli`
  - Login and select marketplace: `flex-cli login && flex-cli marketplace select`
  - Apply search schemas using the script: `cd web-client/src/config && ./apply-search-schemas.sh`
  - Or apply manually with individual commands:
    - `flex-cli search set --key age_group --type enum --scope public`
    - `flex-cli search set --key material --type multi-enum --scope public`
    - `flex-cli search set --key certification --type multi-enum --scope public`
    - `flex-cli search set --key color --type multi-enum --scope public`
    - `flex-cli search set --key key_features --type multi-enum --scope public`
  - Verify schemas applied: `flex-cli search show`
  - Test that filters work on marketplace search page
  - **Note:** Enum values are defined in `configListing.js`, NOT passed to CLI commands

- [ ] **Extend Category Structure in Sharetribe Console**
  - Add new category hierarchies for each vertical
  - Configure category-specific listing fields
  - Set up category-specific transaction processes

- [ ] **Create Category-Specific Listing Fields**
  - Electronics: Power specs, connectivity, warranty
  - Clothing: Size charts, fit guides, material care
  - Home: Dimensions, room suitability, installation
  - Beauty: Skin type, ingredients, usage instructions

- [ ] **Update Category Configuration Files**
  - Extend `configListing.js` with new category fields
  - Add category-specific validation rules
  - Implement conditional field display based on category

### 3.2 Frontend Component Updates

#### Current State
- [x] Brand display implemented in search cards and listing pages
- [x] Category-specific routing working for baby products

#### Todo Items
- [ ] **Create Category-Specific Components**
  - `ClothingSpecifications.js` - Size charts, fit guides
  - `ElectronicsSpecs.js` - Technical specifications display
  - `HomeProductSpecs.js` - Dimensions, room compatibility
  - `BeautyIngredients.js` - Ingredient lists, skin type compatibility

- [ ] **Update Search and Filtering**
  - Add category-specific filters for each vertical
  - Implement cross-category search functionality
  - Create category landing pages with unique content

- [ ] **Enhance Product Display Logic**
  - Category-aware attribute display
  - Conditional rendering based on product type
  - Category-specific product image handling

---

## Phase 4: Data Integration & Migration

### 4.1 Integration Script Updates

#### Current State
- [x] `create-listings.js` works for baby products
- [x] Brand field mapping implemented
- [x] Category mapping and price conversion working

#### Todo Items
- [ ] **Enhance Integration Script for Multi-Category**
  - Add category detection in CSV processing
  - Implement category-specific field mapping
  - Add validation for category-appropriate data

- [ ] **Update Price Handling**
  - Category-specific currency handling (electronics vs textiles)
  - Dynamic pricing rules based on product category
  - Multi-currency support for different verticals

- [ ] **Implement Bulk Category Migration**
  - Create migration script for existing data
  - Add category reassignment functionality
  - Implement data validation and rollback capabilities

### 4.2 Data Quality & Consistency

#### Todo Items
- [ ] **Create Category-Specific Quality Checks**
  - Validate required fields per category
  - Check data consistency within categories
  - Implement automated quality scoring

- [ ] **Establish Data Standardization Rules**
  - Category-specific attribute naming conventions
  - Value format standardization (sizes, colors, materials)
  - Create data validation schemas

---

## Phase 5: Content & SEO Strategy

### 5.1 Category-Specific Content Strategy

#### Todo Items
- [ ] **Update Customer Acquisition PRD**
  - Extend target keywords for new categories
  - Add category-specific content pillars
  - Update SEO strategy for multi-category approach

- [ ] **Create Category Landing Pages**
  - Traditional Indian clothing for diaspora
  - Authentic Indian home decor and cookware  
  - Ayurvedic and natural beauty products
  - Traditional Indian foods and spices

- [ ] **Develop Category-Specific Brand Stories**
  - Heritage and cultural significance
  - Diaspora connection and authenticity
  - Quality and craftsmanship narratives

### 5.2 Multi-Category Navigation

#### Todo Items
- [ ] **Design Category Navigation Structure**
  - Main category menu with subcategories
  - Cross-category product recommendations
  - Category-specific promotional banners

- [ ] **Implement Category-Aware Search**
  - Category-specific search suggestions
  - Cross-category search results
  - Category filtering and sorting options

---

## Phase 6: Testing & Validation

### 6.1 Category Expansion Testing

#### Todo Items
- [ ] **Create Test Data Sets**
  - Sample products for each new category
  - Edge cases for category classification
  - Cross-category product examples

- [ ] **Implement Integration Testing**
  - End-to-end testing for each category
  - Cross-category search and filtering
  - Category-specific product display

- [ ] **User Acceptance Testing**
  - Category-specific user journeys
  - Search and discovery across categories
  - Purchase flow for different product types

### 6.2 Performance & Scalability

#### Todo Items
- [ ] **Load Testing with Multi-Category Data**
  - Large dataset processing performance
  - Search performance across categories
  - Database query optimization

- [ ] **Monitoring & Analytics Setup**
  - Category-specific conversion tracking
  - Cross-category user behavior analysis
  - Performance monitoring per category

---

## Phase 7: Launch Strategy

### 7.1 Phased Category Rollout

#### Todo Items
- [ ] **Plan Category Launch Sequence**
  - Priority order based on diaspora demand
  - Resource allocation per category launch
  - Success metrics for each phase

- [ ] **Create Launch Checklists**
  - Technical readiness checklist
  - Content and SEO preparedness
  - Marketing campaign readiness

### 7.2 Category-Specific Marketing

#### Todo Items
- [ ] **Develop Category Launch Campaigns**
  - Social media campaigns for each vertical
  - Influencer partnerships by category
  - Email marketing segmentation

- [ ] **Create Category Performance Dashboards**
  - Track success metrics per category
  - Monitor cross-category user behavior
  - Measure ROI by vertical

---

## Implementation Timeline

### **Phase 1-2: Foundation (Months 1-2)**
- LLM classifier updates and category infrastructure
- Scraper framework and initial brand research

### **Phase 3-4: Integration (Months 3-4)**  
- Frontend updates and data integration
- Testing and validation systems

### **Phase 5-6: Content & Testing (Months 5-6)**
- Content strategy implementation
- Comprehensive testing and optimization

### **Phase 7: Launch (Month 7+)**
- Phased category rollout
- Marketing campaigns and performance monitoring

---

## Success Metrics

### **Technical Metrics**
- Classification accuracy per category (>85%)
- Data quality scores by vertical (>90%)
- Search performance across categories (<2s)

### **Business Metrics**
- User engagement per category
- Cross-category purchase behavior
- Revenue diversification across verticals

### **User Experience Metrics**
- Category-specific conversion rates
- Search success rates by vertical
- Customer satisfaction per category

---

## Risk Mitigation

### **Technical Risks**
- **Data Quality**: Implement robust validation per category
- **Performance**: Optimize for larger, diverse datasets
- **Complexity**: Maintain clear separation of concerns

### **Business Risks**
- **Market Demand**: Validate diaspora interest before full investment
- **Brand Relationships**: Secure affiliate partnerships across categories
- **Resource Allocation**: Phase rollout to manage development costs

### **Operational Risks**
- **Content Management**: Ensure scalable content creation process
- **Quality Control**: Maintain standards across all categories
- **Customer Support**: Train team on multi-category product knowledge

---

## Notes

- This expansion should align with the overall Laem → Mela rebranding strategy
- Consider competitive landscape for each new category
- Maintain focus on authentic Indian brands and cultural relevance
- Ensure affiliate revenue model scales across all categories
- Plan for eventual international expansion beyond US market