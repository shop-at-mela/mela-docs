# CSV Field Definitions - listing-fields-options.csv

## Overview
The `listing-fields-options.csv` file serves as the **single source of truth** for all Sharetribe listing field definitions, options, and mapping rules. This unified approach replaces the previous JSON+CSV split.

## Field Definitions

### **field_id**
- **Type:** String (snake_case)
- **Purpose:** Unique identifier for the listing field in Sharetribe Console
- **Rules:** Lowercase, underscores only, no spaces (e.g., `age_group`, `key_features`)
- **Usage:**
  - Sharetribe Console field creation
  - API field references
  - Database storage key

### **field_name**
- **Type:** String (Title Case)
- **Purpose:** Human-readable display name shown to users in filters/forms
- **Rules:** Proper capitalization, spaces allowed (e.g., "Age Group", "Key Features")
- **Usage:**
  - Sharetribe Console display name
  - Frontend filter labels
  - User-facing forms

### **option_name**
- **Type:** String
- **Purpose:** Human-readable option displayed to users in dropdowns/checkboxes
- **Rules:** Parent-friendly language, avoid technical terms (e.g., "Light Gray" not "Heather")
- **Usage:**
  - Sharetribe Console option display name
  - Frontend dropdown options
  - Search filter labels

### **option_value**
- **Type:** String (snake_case)
- **Purpose:** Internal identifier stored in listing data
- **Rules:** Lowercase, underscores, no spaces, permanent once created (e.g., `light_gray`, `0_3_months`)
- **Usage:**
  - Sharetribe listing data storage
  - API queries and filters
  - URL parameters for filtered searches

### **categories**
- **Type:** String (comma-separated)
- **Purpose:** Defines which product categories this field applies to
- **Values:**
  - `all` - applies to all categories
  - `clothing,accessories` - specific categories only
- **Usage:**
  - Conditional field display in Sharetribe Console
  - Category-specific filtering logic

### **priority**
- **Type:** Integer (1-10)
- **Purpose:** Display order and importance ranking for fields
- **Rules:** Lower numbers = higher priority (1 = most important)
- **Usage:**
  - Field ordering in Sharetribe Console
  - Search filter priority
  - Homepage feature importance

### **auto_generated**
- **Type:** Boolean (true/false)
- **Purpose:** Tracks whether option was auto-discovered by item_aspects_formatter.py
- **Values:**
  - `false` - manually defined core option
  - `true` - automatically discovered, needs human review
- **Usage:**
  - Quality control and review workflow
  - Identifying options that need validation
  - Cleanup and standardization

### **field_type**
- **Type:** String (enum)
- **Purpose:** Defines how users can select options in Sharetribe Console
- **Values:**
  - `select_one` - radio buttons, single choice (e.g., Age Group)
  - `select_multiple` - checkboxes, multiple choices (e.g., Colors, Features)
- **Usage:**
  - Sharetribe Console field configuration
  - Frontend form widget type
  - Validation rules

### **is_default**
- **Type:** Boolean (true/false)
- **Purpose:** Identifies core vs discovered options for organizational purposes
- **Values:**
  - `true` - core option defined in initial specification
  - `false` - option discovered later or less common
- **Usage:**
  - Prioritizing options in UI
  - Core vs extended feature sets
  - Data quality assessment

### **mapping_aliases**
- **Type:** String (comma-separated, quoted)
- **Purpose:** Alternative names/terms that should map to this option
- **Format:** `"alias1,alias2,alias3"` (quoted to handle commas in values)
- **Examples:**
  - `"Heather,Grey Heather,Heather Colored"` → maps to "Light Gray"
  - `"0-6 months,Newborn"` → maps to "0-3 months"
- **Usage:**
  - item_aspects_formatter.py automatic mapping
  - Brand-specific term standardization
  - Backward compatibility with legacy data

## Usage Examples

### **Creating New Field in Sharetribe Console:**
```csv
field_id: material
field_name: Material
field_type: select_multiple
option_name: Organic Cotton
option_value: organic_cotton
```

### **Auto-Mapping Brand Terms:**
```csv
option_name: Light Gray
option_value: light_gray
mapping_aliases: "Heather,Grey Heather,Heather Colored"
```
When item_aspects_formatter.py sees "Heather" → converts to "Light Gray|light_gray"

### **Review Auto-Generated Options:**
```csv
auto_generated: true
is_default: false
```
Indicates this option was discovered automatically and needs human review.

## Maintenance Workflow

### **1. Adding New Core Options:**
- Set `auto_generated: false`, `is_default: true`
- Define proper `field_type` and `priority`
- Add known aliases to `mapping_aliases`

### **2. Reviewing Auto-Generated Options:**
- Filter by `auto_generated: true`
- Validate `option_name` is parent-friendly
- Check if `option_value` follows naming conventions
- Add aliases if needed, set `is_default` appropriately

### **3. Field Configuration:**
- Use `field_id`, `field_name`, `field_type` for Sharetribe Console setup
- Copy `option_name|option_value` pairs directly into Console
- Set field applicability using `categories`

## Integration Points

### **item_aspects_formatter.py**
- Reads entire CSV on startup
- Builds mapping cache from `mapping_aliases`
- Auto-generates new rows with `auto_generated: true`
- Uses `field_type` for new field creation

### **Sharetribe Console**
- Manual field creation using `field_id`, `field_name`, `field_type`
- Option setup using `option_name`, `option_value` pairs
- Category restrictions using `categories`

### **create-listings.js (Future)**
- Parse Item_Aspects format: "Material: Organic Cotton|organic_cotton"
- Validate `option_value` exists in CSV
- Apply field-specific logic based on `field_type`

## Business Value & SEO Strategy

### **Field Priority for Customer Discovery:**
1. **Age Group** (Priority 1) - Primary search qualifier for parents
2. **Material** (Priority 2) - Trust signal, premium positioning
3. **Certification** (Priority 3) - Safety/quality assurance
4. **Color** (Priority 5) - Visual preference, gift selection
5. **Key Features** (Priority 6) - Functional benefits

### **Homepage Integration Opportunities:**
- **"Shop by Age"** - Most important for parents (age_group filter)
- **"Organic Collection"** - Premium positioning (material=organic_cotton)
- **"Safe & Certified"** - Trust-focused (certification=gots_certified)
- **"Easy-Dress Collection"** - Functional benefit (key_features=easy_dress)

### **SEO Keywords by Field:**
- **Age Group:** "0-3 months baby clothes", "newborn essentials"
- **Material:** "organic cotton baby wear", "bamboo baby clothes"
- **Certification:** "GOTS certified baby products", "non-toxic baby items"
- **Features:** "snap closure baby clothes", "breathable baby wear"

### **Content Marketing Themes:**
- **Seasonal:** "Summer breathable collection" (features=breathable)
- **Milestone:** "First 100 days essentials" (age_group=0_3_months)
- **Gifting:** "Premium organic gift sets" (material=organic_cotton)
- **Regional:** "Traditional Indian baby wear" (design elements)

This unified CSV approach ensures all stakeholders work from the same data source while maintaining clear separation between human-readable names and system identifiers.