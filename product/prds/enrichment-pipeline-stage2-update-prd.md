# Enrichment Pipeline Stage 2 Update PRD

## Executive Summary
**Feature**: Extend the Stage 2 enrichment prompt in `prompt_engine.py` to output two additional fields — `meta_description` and `search_synonyms` — alongside the existing `item_aspects` and `seo_title`
**Target System**: Data pipeline (`prompt_engine.py`) → Classified CSV → `product-listing-integration` → Sharetribe `publicData` → `web-client` listing pages
**Target Users**: US diaspora parents discovering Mela products via Google, ChatGPT, Perplexity
**Business Objective**: Replace template-generated meta descriptions with product-specific, consumer-language copy; supply AI answer engines with the consumer phrasings they need to surface Mela listings
**Primary Success Metrics**:
- Google Search Console CTR from product pages: +15%
- AI assistant discoverability: Mela products surface in ChatGPT/Perplexity responses to consumer queries (manual spot-check)

> **Relates to**: `ai-ready-product-discovery-prd.md` — that PRD defines the web-client Schema.org container; this PRD supplies the richer data it needs.
> **Explicitly out of scope**: Stage 3B image alt text (vision model, deferred due to cost), Stage 3C FAQ generation (later phase).

## Build Status Summary *(updated 2026-05-25)*

| Layer | Item | Status |
|-------|------|--------|
| **web-client** | `<meta name="description">` uses `publicData.metaDescription` with fallback to template | ✅ Shipped — `ListingPageCarousel.js:338`, `ListingPageCoverPhoto.js:339` |
| **web-client** | JSON-LD `keywords` array from `publicData.searchSynonyms` | ✅ Shipped — `ListingPageCarousel.js:385`, `ListingPageCoverPhoto.js:440` |
| **web-client** | Graceful fallback when fields are absent (no null crash) | ✅ Shipped — conditional spread pattern |
| **pipeline** | `create_enrichment_system_prompt()` outputs `meta_description` and `search_synonyms` rules | ❓ Verify in `prompt_engine.py` |
| **pipeline** | `create_enrichment_prompt()` JSON schema includes both new fields | ❓ Verify |
| **CSV** | Classified CSV has `Meta_Description` and `Search_Synonyms` columns | ❓ Verify |
| **ingestion** | `publicData.metaDescription` and `publicData.searchSynonyms` set on new listings | ❓ Verify in Sharetribe Console on a recently-ingested listing |

**Overall:** The web-client consumption layer is fully built. Pipeline and ingestion changes need verification — the web-client falls back gracefully if fields are absent, so there's no user-facing breakage regardless.

---

## 1. Problem Statement

### Current State
Stage 2 (`create_enrichment_prompt`) outputs two fields per product:
- `item_aspects` — pipe-delimited attribute string
- `seo_title` — 60-80 char optimized title

**Meta description** is generated at render-time in `ListingPageCoverPhoto.js` using a template:
```
"Shop authentic {brand} {title} for Indian diaspora families at {price}. {first 100 chars of description}. Trusted Indian baby products delivered to USA."
```
This template is generic, doesn't reflect the product's key differentiators, and will be identical in structure for every product — exactly what search engines and AI assistants penalize.

**Search synonyms** don't exist anywhere in the pipeline. No consumer-language phrasings are stored or surfaced. When a parent asks ChatGPT "what's a good organic cotton onesie from an Indian brand?", there is no structured field that maps that query to a Mela listing.

### User Pain Points
- **Google SERP**: Generic meta descriptions lower click-through rates — the snippet looks templated
- **AI shopping assistants**: Mela products are invisible because we don't provide consumer-language phrasings that match how parents ask questions
- **GEO (Google AI Overviews)**: Attribute-complete, naturally-phrased product data is the key signal for inclusion in AI Overview shopping panels

### Business Impact of Inaction
- Every product listing competes with a generic template meta description against brand sites that write custom descriptions
- AI answer engines (Perplexity, ChatGPT, Gemini) cannot confidently surface Mela products for long-tail parent queries
- The `ai-ready-product-discovery-prd.md` Schema.org implementation is incomplete without well-formed `keywords` data

---

## 2. Goals & Non-Goals

### Goals
- Add `meta_description` and `search_synonyms` to the Stage 2 enrichment prompt output
- Add corresponding columns to the classified CSV schema
- Map new CSV columns to `publicData` in `product-listing-integration`
- Have web-client prefer `publicData.metaDescription` over the template fallback
- Surface `publicData.searchSynonyms` as `keywords` in the product JSON-LD

### Non-Goals
- Image alt text generation (Stage 3B — deferred, requires vision model)
- FAQ / Q&A generation (Stage 3C — later phase)
- Google Merchant Center feed (Stage 4 — separate initiative)
- Re-running Stage 1 (category classification) — not needed; new fields derive from existing Stage 2 inputs
- Changes to `configListing.js` — new fields are free-text/array, not filterable enums

---

## 3. User Stories

| As a... | I want to... | So that... | Priority |
|---------|-------------|------------|----------|
| Parent searching on Google | See a compelling, specific snippet about a product | I click through to Mela instead of a competitor | P0 |
| Parent asking ChatGPT "what's a good organic onesie from India?" | Get Mela products cited in the AI response | I discover Mela without going to Google first | P0 |
| Parent on Perplexity searching by occasion | See "Diwali baby outfit from Indian brand" surface Mela listings | I find what I'm looking for without knowing Mela exists | P0 |

---

## 4. Feature Requirements

### Must Have (P0)

**Pipeline (prompt_engine.py):**
- Stage 2 system prompt updated to describe meta description and search synonyms as outputs
- Stage 2 user prompt updated with output rules, format spec, and examples for both new fields
- Stage 2 JSON output schema updated: `meta_description` (string) and `search_synonyms` (array of strings) added alongside `item_aspects` and `seo_title`

**CSV schema:**
- `Meta_Description` column added to classified CSV output (string, 150-160 chars)
- `Search_Synonyms` column added to classified CSV output (pipe-delimited, 3-5 phrases)

**product-listing-integration:**
- `Meta_Description` CSV column → `publicData.metaDescription` (string)
- `Search_Synonyms` CSV column → `publicData.searchSynonyms` (array, split by `|`)

**web-client:**
- `ListingPageCoverPhoto.js`: use `publicData.metaDescription` if present; fall back to `generateSEODescription()` if absent (backward compat with existing listings)
- `ListingPageCoverPhoto.js` JSON-LD: add `keywords: publicData.searchSynonyms` to Product schema if present
- Same two changes in `ListingPageCarousel.js`

### Should Have (P1)
- Run Stage 2 in "new fields only" mode against already-classified baby_and_kids CSVs (5,376 rows) to backfill `Meta_Description` and `Search_Synonyms` without re-running Stage 1

### Nice to Have (P2)
- Extend to fashion, beauty, home categories once baby backfill is validated

---

## 5. Field Specifications

### `Meta_Description` / `publicData.metaDescription`

| Spec | Rule |
|------|------|
| Length | 150-160 characters exactly |
| Lead | Brand name + product type (from `seo_title`) |
| Body | 1-2 key attributes — whichever is most search-relevant (material > certification > occasion) |
| Close | Diaspora trust hook: "shipped to the US" or "for Indian families in the US" |
| Language | Consumer language — no merchant jargon (no "GOTS jersey", no "envelope neckline", no "kala cotton dungaree") |
| Tone | Warm, specific, parent-voice |

**Good examples:**
- `"Shop Aagghhoo's handwoven kala cotton onesie for your newborn — organic, chemical-free, made in India. Shipped to the US."` (156 chars)
- `"Discover Masilo's GOTS certified organic cotton bodysuit for babies 0-6M — soft, safe, and crafted in India for families in the US."` (133 chars — needs padding to 150)

**Bad examples (do not generate):**
- `"Shop authentic Aagghhoo Organic Onesie for Indian diaspora families at $24.99. Handwoven organic cotton onesie. Trusted Indian baby products delivered to USA."` ← template, no specificity

---

### `Search_Synonyms` / `publicData.searchSynonyms`

| Spec | Rule |
|------|------|
| Count | 3-5 phrases |
| Format in CSV | Pipe-delimited: `phrase one\|phrase two\|phrase three` |
| Format in publicData | Array of strings: `["phrase one", "phrase two", "phrase three"]` |
| Phrase length | 4-8 words each |
| Case | Lowercase, no punctuation |
| Diversity | Each phrase targets a different search angle: material, certification, brand, age group, occasion |
| NOT | Paraphrases of each other; keyword stuffing; merchant jargon |

**Good example (baby onesie, kala cotton, GOTS, 0-6M, Aagghhoo):**
```
organic cotton onesie from india|gots certified baby bodysuit|handwoven baby clothes usa|sustainable newborn outfit indian brand|kala cotton baby clothing
```

**Bad example:**
```
organic baby onesie|organic baby bodysuit|organic baby clothes|organic infant onesie|organic cotton baby onesie
```
← All the same angle (organic), no variety.

---

## 6. Technical Specification

### Stage 2 System Prompt Addition

Append to `create_enrichment_system_prompt()`:
```
8. meta_description: 150-160 characters. Consumer language (not merchant jargon). Lead with brand + product type, include 1-2 key attributes, end with "shipped to the US" or "for Indian families in the US".
9. search_synonyms: Array of 3-5 phrases. Each 4-8 words, lowercase, no punctuation. Each phrase targets a different angle (material, certification, occasion, brand, age). NOT paraphrases of each other.
```

### Stage 2 Output Schema Addition

```python
# create_enrichment_prompt() — updated OUTPUT section
OUTPUT (JSON):
{
  "product_1": {
    "item_aspects": "...",
    "seo_title": "Wooden Building Blocks Fine Motor Skills 2-3 Years Maya",
    "meta_description": "Shop Maya's natural wood building blocks for toddlers 2-3Y — non-toxic, CE certified, handcrafted in India. Shipped to the US.",
    "search_synonyms": ["wooden building blocks india", "non toxic toddler toys indian brand", "natural wood blocks 2 year old", "ce certified baby toys india", "montessori blocks from india"],
    "notes": ""
  }
}
```

### listing-model.js Addition

In `transformCSVRowToListing()`, add to the `publicData` object after existing fields:

```javascript
...(getCsvField(row, 'Meta_Description') && {
  metaDescription: getCsvField(row, 'Meta_Description'),
}),
...(getCsvField(row, 'Search_Synonyms') && {
  searchSynonyms: getCsvField(row, 'Search_Synonyms')
    .split('|')
    .map(s => s.trim())
    .filter(Boolean),
}),
```

### web-client ListingPageCoverPhoto.js + ListingPageCarousel.js

**Meta description fallback:**
```javascript
const seoDescription = publicData.metaDescription
  || generateSEODescription(title, brandName, description, formattedPrice);
```

**JSON-LD keywords addition** (inside Product schema object):
```javascript
...(publicData.searchSynonyms?.length > 0 && {
  keywords: publicData.searchSynonyms,
}),
```

---

## 7. Acceptance Criteria

### Pipeline
- [ ] `create_enrichment_system_prompt()` describes `meta_description` and `search_synonyms` rules
- [ ] `create_enrichment_prompt()` output JSON schema includes `meta_description` (string) and `search_synonyms` (array)
- [ ] Running Stage 2 on 10 sample products produces valid JSON with both new fields
- [ ] `meta_description` is 150-160 characters on all 10 samples
- [ ] `search_synonyms` contains 3-5 phrases, each targeting a different angle, on all 10 samples
- [ ] Existing `item_aspects` and `seo_title` outputs are unchanged

### CSV
- [ ] Classified CSV contains `Meta_Description` and `Search_Synonyms` columns in output
- [ ] `Search_Synonyms` uses `|` as delimiter between phrases

### product-listing-integration
- [ ] `publicData.metaDescription` is set on newly-ingested listings (verify in Sharetribe Console)
- [ ] `publicData.searchSynonyms` is set as an array (not a string) on newly-ingested listings
- [ ] Existing listings without these columns are unaffected (no null/undefined crashes)

### web-client
- [ ] `<meta name="description">` on listing pages uses `publicData.metaDescription` when present
- [ ] `<meta name="description">` falls back to `generateSEODescription()` when `publicData.metaDescription` is absent (backward compat)
- [ ] JSON-LD `<script type="application/ld+json">` contains `"keywords": [...]` array when `publicData.searchSynonyms` is present
- [ ] JSON-LD `keywords` field is absent (not null/empty) when `publicData.searchSynonyms` is absent
- [ ] Changes apply identically to `ListingPageCarousel.js`
- [ ] Google Rich Results Test passes on updated listing pages

---

## 8. Success Metrics & Measurement

| Metric | Baseline | Target | Method |
|--------|----------|--------|--------|
| Google Search Console CTR from product pages | TBD | +15% | GSC → Pages report, filter to `/l/` URLs |
| AI assistant discoverability | 0 | Mela products appear for 3+ test queries | Manual: query ChatGPT/Perplexity with synonyms from `search_synonyms` |
| Meta description coverage | 0% (all template) | 100% of newly-ingested listings | Sharetribe Console → spot-check publicData |
| JSON-LD `keywords` coverage | 0% | 100% of newly-ingested listings | View source on listing pages |

---

## 9. Dependencies & Risks

**Dependencies:**
- `ai-ready-product-discovery-prd.md` must be implemented (web-client JSON-LD container) — `keywords` field is an addition to that schema
- `product-listing-integration` must be run after CSV enrichment before web-client changes take effect

**Risks:**
| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| LLM generates meta_description outside 150-160 char range | Medium | Add character count validation in classifier; log and flag out-of-range values for manual review |
| search_synonyms phrases are too similar (low diversity) | Low | System prompt explicitly rules this out; spot-check 20 products post-run |
| Existing listings (pre-update) have no metaDescription in publicData | Certain | Web-client fallback to `generateSEODescription()` handles this — backward compatible by design |

---

## 10. Out of Scope / Future Considerations

- **Stage 3B**: Image alt text generation via Claude Vision — deferred (API cost per image)
- **Stage 3C**: FAQ Q&A generation → FAQPage schema (later phase)
- **Stage 4**: Google Merchant Center feed generation — separate initiative
- **Clickstream feedback**: Using GA4 engagement data to re-enrich low-performing listings — post-launch
- **Multilingual synonyms**: Hindi/regional language synonyms for India-side SEO — post-launch
