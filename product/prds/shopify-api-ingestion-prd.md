# Shopify API-Based Product Ingestion PRD

## Executive Summary
**Feature**: Replace per-brand HTML scrapers for Shopify stores with a single generic Shopify JSON API ingester
**Target**: `Mela-scrapper-integrations/scrapper and classifiers/product scrappers/`
**Business Objective**: Reduce scraper maintenance cost, eliminate Firecrawl dependency for Shopify brands, and make adding new Shopify brand partners a 5-minute config change instead of a multi-day scraper project
**Primary Success Metrics**:
- Zero Firecrawl API calls for Shopify brands
- 100% field parity with existing CSV schema
- New Shopify brand onboarded in < 10 minutes (config only, no new code)
- Scrapers no longer break on HTML/CSS changes

---

## 1. Problem Statement

### Current State
Each of the 12 brands in `initial_scrapers/` has its own Python file (~200-350 lines) that:
1. Parses category navigation HTML to find category URLs
2. Paginates through category listing pages
3. Visits every individual product page to extract name, price, description, SKU, stock status
4. Calls Firecrawl (paid external API) to extract product images and recommendations from dynamic JS-rendered content

Many of these brands (Greendigo, Masilo, SuperBottoms, ChooseKind, etc.) are built on Shopify. Shopify exposes a free, structured JSON API that returns everything we need — no HTML parsing, no Firecrawl, no per-page requests.

### Pain Points
- **Fragile**: Any CSS/HTML change on a brand's site breaks the scraper silently
- **Expensive**: Firecrawl is a paid API called per-product for images and recommendations
- **Slow**: Each product requires an individual HTTP request + Firecrawl call; full scrapes take hours
- **Hard to scale**: Onboarding a new Shopify brand requires writing a new ~300-line scraper
- **Incomplete data**: Current scrapers miss variants (size/color), tags, and Shopify product IDs — all of which are valuable for Mela's classification pipeline
- **Inconsistent**: Each scraper has slightly different logic for price normalization, image extraction, category assignment

### Business Impact of Inaction
Every new Indian brand partner on Shopify (the majority) requires a dev sprint to onboard. Firecrawl costs scale linearly with catalog size. Broken scrapers cause stale data on Mela listings without alerting anyone.

---

## 2. Goals & Non-Goals

### Goals
- Build a single, config-driven Shopify ingester that works for any Shopify store
- Replace all existing scrapers for confirmed Shopify brands
- Match the existing CSV output schema exactly so downstream classification pipeline is unaffected
- Eliminate Firecrawl calls for all Shopify brands (images and recommendations come from the API)
- Enable adding a new Shopify brand with a one-line config entry
- Support incremental sync (fetch only new/changed products)

### Non-Goals
- Replacing scrapers for **non-Shopify brands** (MeeMee, Skillmatics, etc. — these stay as-is)
- Building a real-time sync or webhook system (batch pull is sufficient for now)
- Migrating to a database — CSV output is kept for pipeline compatibility
- Scraping Shopify checkout, cart, or authenticated data
- Handling Shopify Plus custom storefronts with API authentication requirements

---

## 3. Shopify API Overview

### Products Endpoint
```
GET https://{store_domain}/collections/all/products.json?limit=250&page={n}
```
Returns up to 250 products per page. Paginate by incrementing `page` until response returns fewer than 250 products.

**Response shape** (per product):
```json
{
  "id": 9930136355092,
  "title": "Organic Cotton Kurta Set",
  "handle": "organic-cotton-kurta-set",
  "body_html": "<p>Description here...</p>",
  "vendor": "ChooseKind",
  "product_type": "Clothing",
  "tags": ["organic", "0-3m", "kurta"],
  "status": "active",
  "variants": [
    {
      "id": 123,
      "sku": "CK-KURTA-001-0-3M",
      "price": "1299.00",
      "compare_at_price": "1599.00",
      "available": true,
      "title": "0-3 Months"
    }
  ],
  "images": [
    { "src": "https://cdn.shopify.com/s/files/..." },
    { "src": "https://cdn.shopify.com/s/files/..." }
  ]
}
```

### Recommendations Endpoint
```
GET https://{store_domain}/recommendations/products.json?product_id={shopify_id}&limit=10
```
Requires the **numeric Shopify product ID** (available in the products.json response). Returns up to 10 recommended products with their handles (which map to our SKU field).

### Key Mapping: Shopify → CSV Fields
| CSV Field | Shopify Source | Notes |
|-----------|---------------|-------|
| Product Name | `product.title` | Direct |
| SKU/Product ID | `product.handle` | URL-safe slug, used as SKU in existing CSVs |
| Was Price | `variants[0].compare_at_price` | Original price before discount |
| Price | `variants[0].price` | Current price |
| Product Image URL | `product.images[*].src` | All images, comma-separated |
| Product URL | `{base_url}/products/{handle}` | Constructed |
| Category | `product.product_type` or tag heuristic | See §4 requirements |
| Description | `product.body_html` (stripped) | Strip HTML tags |
| Brand Name | Config value or `product.vendor` | |
| Stock Status | `variants[0].available` → "In Stock" / "Out of Stock" | |
| Recommended Products | Recommendations endpoint → handles | Comma-separated handles |

---

## 4. Feature Requirements

### Must Have (P0)
- **Generic Shopify fetcher**: A single `shopify_scraper.py` (or `shopify_ingester.py`) that accepts a brand config dict and produces a CSV
- **Brand registry**: A config file (`shopify_brands.py` or `shopify_brands.json`) listing all Shopify brands with `base_url`, `brand_name`, `output_file`, and optional `collection` (default: `all`)
- **Full product data**: Extract all fields matching the existing CSV schema — name, handle (SKU), price, compare_at_price, all image URLs, product URL, product_type (category), HTML-stripped description, vendor, stock status
- **Recommendations**: Fetch from recommendations endpoint using the product's numeric Shopify ID; store as comma-separated handles
- **Incremental mode**: `--new-only` flag that skips products already in the CSV (match by handle)
- **Output format**: Same CSV schema as current scrapers — drop-in replacement, no downstream changes needed
- **Pagination**: Handle stores with >250 products (paginate `products.json`)

### Should Have (P1)
- **Category fallback**: If `product_type` is empty, derive category from tags (e.g., tag "clothing" → "Clothing") or use a configurable default per brand
- **Variant expansion**: Store all variants' sizes/colors as a `Variants` column (new optional column, not breaking)
- **Tags column**: Store raw Shopify tags as a `Tags` column for the AI classification pipeline
- **Shopify product ID column**: Store numeric `product.id` for future use (webhook support, faster re-sync)
- **Run all brands**: A `run_all.sh` or CLI flag that loops through all brands in the registry

### Nice to Have (P2)
- **Auto-detect Shopify**: Script that checks whether a given domain responds to `/products.json` — useful for quickly auditing new brand partners
- **Rate limit handling**: Respect `Retry-After` header if Shopify returns 429
- **Delta detection**: Re-fetch recommendations only when price or availability changes (same logic as current `needs_firecrawl` check)

---

## 5. Brand Identification

The following brands need to be confirmed as Shopify before migration. A Shopify store will respond with valid JSON at `{domain}/products.json`.

| Brand | Scraper File | Likely Platform | Action |
|-------|-------------|-----------------|--------|
| Greendigo | greendigo_scraper.py | **Shopify** (CDN URLs confirm) | Replace |
| Masilo | masilo_scraper.py | Likely Shopify | Confirm + Replace |
| SuperBottoms | superbottoms_scraper.py | Likely Shopify | Confirm + Replace |
| ChooseKind | *(no scraper yet)* | **Shopify** (user confirmed) | New via config |
| Shumee | *(no scraper yet)* | Likely Shopify | Confirm + New |
| Pluchi | pluchi_scraper.py | Likely Shopify | Confirm + Replace |
| Aagghhoo | aagghhoo_scraper.py | Unknown | Confirm |
| Baby Forest | babyforest_scraper.py | Unknown | Confirm |
| Earthy Tweens | earthytweens_scraper.py | Unknown | Confirm |
| Kicks & Crawl | kicksandcrawl_scraper.py | Unknown | Confirm |
| Little West Street | littleweststreet_scraper.py | Unknown | Confirm |
| MiDulce Anya | midulceanya_scraper.py | Unknown | Confirm |
| MeeMee | meemee_scraper.py | Likely custom/Magento | Keep HTML scraper |
| Skillmatics | skillmatics_scraper.py | Unknown | Confirm |

**Confirmation method**: `curl https://{domain}/products.json?limit=1` — if it returns JSON with a `products` key, it's Shopify.

---

## 6. Technical Architecture

### New File Structure
```
initial_scrapers/
  shopify_ingester.py          # New: Generic Shopify ingester
  shopify_brands.py            # New: Brand registry / config
  greendigo_scraper.py         # Keep until Shopify confirmed + tested
  [other HTML scrapers]        # Keep for non-Shopify brands

shared/
  shopify_utils.py             # New: Shopify API helpers (fetch, paginate, map)
  recommendation_utils.py      # Existing: Still used by HTML scrapers
  scraper_utils.py             # Existing: CSV helpers reused by Shopify ingester
```

### `shopify_brands.py` schema
```python
SHOPIFY_BRANDS = [
    {
        "brand_name": "Greendigo",
        "base_url": "https://greendigo.com",
        "collection": "all",        # Optional, default "all"
        "output_file": "greendigo_products.csv",
    },
    {
        "brand_name": "ChooseKind",
        "base_url": "https://www.choosekind.in",
        "collection": "all",
        "output_file": "choosekind.csv",
    },
    # ... one entry per Shopify brand
]
```

### CLI
```bash
# Single brand
python shopify_ingester.py --brand greendigo

# All brands
python shopify_ingester.py --all

# Incremental (skip existing)
python shopify_ingester.py --brand greendigo --new-only

# Check if a domain is Shopify
python shopify_ingester.py --detect https://masilo.in
```

---

## 7. Acceptance Criteria

- [ ] `shopify_ingester.py --brand greendigo` produces a CSV with the same columns as `greendigo_products.csv`
- [ ] All 11 existing CSV fields are populated for every product where data is available in the API
- [ ] Image URLs are comma-separated (multiple images per product)
- [ ] Recommended Products field contains comma-separated product handles (not numeric IDs)
- [ ] `--new-only` flag skips products whose handle already exists in the output CSV
- [ ] Brands with >250 products are fully fetched via pagination
- [ ] Adding a new Shopify brand requires only a new entry in `shopify_brands.py` — zero code changes
- [ ] No Firecrawl API calls are made for any Shopify brand
- [ ] HTML tags are stripped from `body_html` before writing to Description field
- [ ] `Was Price` is empty string (not null/NaN) when `compare_at_price` is null
- [ ] `Stock Status` is "In Stock" or "Out of Stock" (not boolean)
- [ ] Existing HTML scrapers for non-Shopify brands are **not modified**

---

## 8. Success Metrics

| Metric | Before | Target After |
|--------|--------|-------------|
| Time to add a new Shopify brand | 1-2 days (new scraper) | < 10 minutes (config entry) |
| Firecrawl calls per full Greendigo sync | ~150 (one per product) | 0 |
| Full Greendigo sync time | ~45 min | < 5 min |
| Scraper breakage on site redesign | Likely breaks | No impact (API-based) |
| Lines of code per brand | ~300 | ~5 (config entry) |

---

## 9. Dependencies & Risks

**Dependencies**
- Shopify's undocumented public API (`/products.json`) has no official SLA. It has been stable for 10+ years and is widely used by price trackers, but Shopify could theoretically restrict it.
- Recommendations endpoint (`/recommendations/products.json`) requires a numeric product ID. This is only available after fetching products — must store `product.id` in the pipeline.
- `scraper_utils.py` CSV helpers (load, merge, save) are reused. Interface must stay compatible.

**Risks**
| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Some "Shopify" brands return empty `products.json` (private catalog) | Low | Detect during brand audit; keep HTML scraper as fallback |
| Recommendations endpoint removed or rate-limited | Low | Cache responses; degrade gracefully to empty string |
| `product_type` field is blank for many products | Medium | Fallback to tag-based category, then configurable default |
| Variant explosion: products with 20+ size/color combos | Low | Use only first variant for price fields; store all as optional Variants column |

---

## 10. Out of Scope / Future Considerations

- **Webhook-based real-time sync**: When Mela scales to 50+ brands, replacing batch pulls with Shopify webhook subscriptions will eliminate the need to run scrapers entirely
- **Storefront API (authenticated)**: Unlocks metafields, collections, and richer product data — relevant once Mela negotiates formal API partnerships with brands
- **Non-Shopify brand unification**: MeeMee, Skillmatics, and any WooCommerce/Magento brands will need separate treatment; this PRD does not address them
- **Price history tracking**: Storing `Was Price` over time to surface sale events — useful future feature for buyer alerts
