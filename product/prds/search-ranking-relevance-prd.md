# Search Results Ranking & Relevance (Mela Relevance Score) PRD

**Document Owner:** Product Team
**Last Updated:** August 16, 2026 (rev. 2 — search-engineering panel review folded in)
**Status:** Draft — for review
**Priority:** High
**Related PRDs:** `search-page-optimization-prd.md` (this is the deferred "faceted sorting / category-specific filters" Phase 2), `seo-aeo-category-brand-pages-prd.md` (ranking = what answer-engines cite), `enrichment-pipeline-stage2-update-prd.md` (score + indexed text fields are computed in the same pipeline)

---

## Executive Summary

**Feature**: Two coordinated relevance surfaces, both native to Sharetribe's Elasticsearch layer:
1. **Browse ranking** — replace the age-based default sort with a **stored, tiered composite "Mela Relevance Score" (`melaScore`)**, gated by an editorial `boostTier`, paired with category-contextual filters and entry-point-aware behavior.
2. **Keyword relevance & diaspora vocabulary** — enrich the indexed `text` fields Sharetribe's keyword search reads, including a **US-English ↔ Hindi/regional synonym + transliteration layer**, so query-driven traffic (on-site search + AEO) actually finds the catalog.

**Why both**: Sharetribe's ES exposes two independent relevance mechanisms — numeric sort (browse) and keyword relevance (query) — and **they are mutually exclusive server-side** (passing `sort` discards keyword relevance). A ranking plan that only touches sort silently ignores every keyword session. See §4B.

**Target URL / Entry Point**: `/s` (SearchPage), plus every category/facet landing surface that renders search results (`CategoryPage`, SEO/AEO facet pages, social deep-link destinations).

**Target Users**: All four co-equal personas — Sarah (safety/certs), Neha (familiar brands + price), Arun (heritage/craft), Priya (browse/serendipity). Ranking must serve all three entry paths: social deep-link, search-engine/AEO, on-site browse.

**Business Objective**: Convert Mela's inspiration-first positioning into the *default* results order — surfacing curated, purchasable, diverse inventory first — instead of rewarding whichever listing was ingested most recently. Ranking is merchandising; today Mela has no objective function behind it.

**Primary Success Metrics**:
- **SRP → PDP click-through rate (CTR)**: +15% vs. newest-first baseline
- **Outbound/affiliate click rate from search sessions**: +10% (the money event)
- **Brand diversity in top 24 results**: no single brand > 20% of any first page (measured)
- **Zero-purchasable-result and dead-link exposure in top 24**: → ~0%
- **Keyword zero-result rate**: −50% (driven by the diaspora synonym/transliteration layer)
- **Keyword-session CTR@10 / MRR**: establish baseline, then improve sweep-over-sweep via the search-quality scorecard (§7)

> ⚠️ All targets are gated on analytics instrumentation, which is still unshipped per `search-page-optimization-prd.md` (Phase 1). Baseline capture is a hard dependency (§8).

---

## 1. Problem Statement

### Current State
- The stock Sharetribe Web Template SearchPage defaults `sortConfig.options[0]` to `createdAt` (newest). In `SearchPage.duck.js`, `sortSearchParams()` falls back to this default whenever there is **no keyword and no user-selected sort** — which is the majority of sessions.
- **Net effect: Mela's most-seen ordering is driven by upload recency** — an operations artifact, not shopper relevance. Good inventory sinks as it ages; the last brand to ingest wins the top.
- Filters are the flat stock rail. `configListing.js` already defines rich facets (`age_group`, `gender`, `material`, `certification`, `color`, `key_features`, `skill_type`, `play_type`, `sustainability_claim`, `occasion`, boolean `isBestseller`), but they render uniformly across all categories — a jewelry shopper sees `age_group`; a toy shopper sees `occasion`.
- Out-of-stock / non-purchasable listings are not systematically down-ranked. (Known issue: CSV "In Stock" ≠ live-purchasable; Sharetribe-side duplicate/closed listings exist.)

### The hard platform constraint (this reframes the whole solution)
Sharetribe runs **Elasticsearch under the hood, but exposes almost none of its ranking control surface** — no `function_score`, script sort, custom analyzers, boosting queries, or vector/kNN. What it *does* expose:
- **Numeric sort** on `createdAt`, `price`, or a `long`-schema `metadata`/`publicData` field (`sort=meta_<key>` / `pub_<key>`), **up to 3 keys**, comma-separated, tie-broken in order.
- **Keyword relevance** — ES n-gram matching over listing `title`, `description`, and any **`text`-schema extended-data field**, weighted `title > description > extended fields`, full-word > n-gram.
- **Exact filters** — `enum` / `multi-enum` / `long` / `boolean`.

Three consequences that shape everything below:
1. **No query-time composite scoring.** Ranking "smarter than newest" means: **pre-compute a number, store it, sort by the stored value.** (Sharetribe's own blessed pattern for curated marketplaces.)
2. **Sort and keyword relevance are mutually exclusive server-side.** If `keywords` is present and you also pass `sort`, sort wins and relevance is discarded; omit `sort` and you get pure relevance with zero curation. Blending requires client-side re-ranking of the fetched page (§4B.3).
3. **Only top-level extended-data attributes are indexable** — every scoring/keyword input must be a flat top-level key, and a schema already defined in Console **cannot** be re-set via CLI (409). These are hard rules for the pipeline.

### User Pain Points (persona lens)
- **Sarah** can't trust that certified, safe products surface first — recency buries them behind whatever was just added.
- **Neha** hits price-agnostic ordering and occasionally lands on dead/out-of-stock links, eroding trust.
- **Arun** — story-rich, handcrafted listings (his signal) get no ranking advantage over thin, freshly-ingested ones.
- **Priya** — browsing gives a chronological wall, sometimes one brand repeated, instead of curated serendipity.

### Business Impact of Inaction
Every entry path is undercut: social deep-links dump high-intent shoppers into a generic grid; AEO/SEO landing pages present a recency order that misrepresents catalog quality to Google and answer-engines; on-site browse fails the inspiration-first promise. We leave outbound-click revenue on the table and train shoppers that Mela results are noisy.

---

## 2. Goals & Non-Goals

### Goals
- Make **curated relevance the invisible default order** on browse surfaces, with recency demoted to a small, decayed input.
- Make **keyword search actually find the catalog** by enriching indexed `text` fields, and **bridge the diaspora vocabulary gap** (US ↔ Indian/regional terms) that ES n-grams cannot cross.
- Keep the entire solution **within native Sharetribe capabilities** (stored numeric sort + `text`-schema keyword index). Zero new search infrastructure.
- Compute `melaScore`, `boostTier`, and the enriched `text` fields in the **existing pipeline** (`product-listing-integration/scripts/create-listings.js` + classifier) at ingest/update, refreshed by a **2–3 week re-score sweep** (freshness half-life ≈ 30–45 days makes weekly unnecessary).
- Guarantee **purchasable, non-duplicate** inventory ranks above dead/closed listings.
- Deliver **category-contextual filters** using native `categoryConfig.limitToCategoryIds`.
- Provide **entry-point-aware results** (social continuity, AEO-canonical facet pages, browse serendipity).
- Stand up a **search-quality measurement flywheel** (scorecard + zero-result mining) so relevance improves each sweep.

### Non-Goals
- **No external search layer** (Algolia/Typesense/Elasticsearch). Explicitly out of scope this cycle.
- **No per-request personalization** or real-time composite scoring — impossible natively; deferred to a future "v2 with external search."
- **No behavioral/ML ranking model** — we have almost no engagement data yet; v1 is curation/attribute-proxy driven.
- Not re-solving Phase 1 UX items (scroll preservation, image lazy-load) — owned by `search-page-optimization-prd.md`.

---

## 3. User Stories

| As a... | I want to... | So that... | Priority |
|---------|-------------|------------|----------|
| Sarah (safety) | See certified, well-documented products first by default | I can trust Mela without hunting | P0 |
| Neha (price/brand) | Never land on out-of-stock or dead links from results | I don't lose faith in the catalog | P0 |
| Arun (heritage) | Have craft-rich, story-complete listings rank up | quality/curation is rewarded over recency | P0 |
| Priya (browse) | See variety across brands per screen | browsing feels like discovery, not a feed | P0 |
| Shopper from IG/Pinterest | Land pre-filtered to what I saw, with "more like this" | the thread from social isn't lost | P1 |
| Shopper from Google/AI | Reach a canonical, well-ordered category/facet page | the first results represent Mela's best | P1 |
| Any shopper | Still opt into "Recently added" or price sorts | I keep control when I want it | P1 |
| Merchandiser (internal) | Adjust score weights without a code deploy | we can tune ranking as the catalog evolves | P2 |

---

## 4. Feature Requirements

### Must Have (P0)

**4.1 The Mela Relevance Score (`melaScore`) — tiered**
- New listing **`metadata` field `melaScore`**, schema type **`long`**, **search-indexed and sortable**, **default value `0`**.
  - CLI: `sharetribe-cli search set --key melaScore --type long --scope metadata --default 0` (verify exact flag syntax against installed CLI version; if the key is later defined in Console it can no longer be CLI-managed — 409).
- **Encoded as a tiered integer** to prevent rank churn between sweeps and keep ordering explainable:

  `melaScore = tier × 1000 + intraTierKey`   (range ~0–10000; tier ∈ 0–9, intraTierKey 0–999)

  where `tier` is a coarse quality band (stable; a listing rarely changes band) and `intraTierKey` is the fine composite that breaks ties within a band. A single fine-grained score is rejected because it makes listings jump position every sweep — bad for returning users and SEO crawl stability.
- **Composite (v1, attribute/curation proxies — no behavioral data)** feeding tier + intraTierKey:

  `composite = 0.35·Quality + 0.30·ConversionProxy + 0.20·Discovery + 0.15·Freshness`

  - **Quality (0.35):** certification count (normalized/capped), `sustainability_claim` present, quality `material`, description richness, **attribute completeness** (fraction of category-relevant facets filled), image count ≥ 3.
  - **ConversionProxy (0.30):** **near-hard gate** — if not purchasable (`state='open'` AND `currentStock>0` AND not a known duplicate/closed listing), this term ≈ 0 (forces the listing into tier 0); else `isBestseller` bump + price sane + multiple images.
  - **Discovery (0.20):** computed with **global catalog knowledge at batch time** — brand-dampening (diminishing multiplier for the Nth+ listing of an over-represented brand) + small new-brand boost.
  - **Freshness (0.15):** exponential decay on `createdAt`, half-life ≈ 30–45 days. Recency survives as a minor, fading input — never the master key.
- **Weights, tier boundaries, and thresholds live in a config object** (in `create-listings.js` / a shared JSON), not hard-coded inline, so tuning doesn't require logic changes.

**4.2 Editorial boost tier (`boostTier`) — merchandiser control, decoupled from the algorithm**
- Separate **`metadata` field `boostTier`**, `long`, indexed/sortable, default `0`. Human/editorial control: pin a new brand, feature a collection, later monetize placement — **changed independently, no full re-score required.**
- Keeps "a merchandiser wants this up" orthogonal to "recompute the model" — a lever you'll want in week one.

**4.3 Default sort change (3-key)**
- Default browse order becomes **`sort=meta_boostTier,meta_melaScore,-createdAt`** — editorial band first, algorithmic tiered score second, `createdAt` as a deterministic freshness tiebreak. (Sharetribe allows up to 3 sort keys.)
- Applied wherever `SearchPage.duck.js` currently falls back to `createdAt`.
- **Keyword search cannot use this sort** (mutual exclusivity — §4B.3); keyword sessions get relevance order + client-side curation blend instead.

**4.4 Rollout backfill guardrail (blocking)**
- **Listings without `melaScore` sort LAST** (unless the schema default is set). Therefore: (1) create the schema with **default 0**, (2) **backfill 100% of live listings** with a real score, (3) verify coverage, **then** (4) flip the default sort. Do not reorder these steps. Same applies to `boostTier`.

**4.5 Purchasability integrity**
- The scorer must consume a **live purchasability check** (reuse the listing-reconcile logic) so out-of-stock, closed, and duplicate listings are gated down. No dead links in the top results.

**4.6 Category-contextual filters**
- Use native **`categoryConfig.limitToCategoryIds`** in `configListing.js` to scope fields: `age_group`/`play_type`/`skill_type` → baby/kids; `gender`/`occasion` → fashion; keep `material`/`certification`/`sustainability_claim`/`color` global.
- Filter rail reshapes per active category automatically.

---

### 4B. Keyword Relevance & Diaspora Vocabulary (P0/P1 — the underused ES lever)

Browse ranking (§4.1–4.6) never touches keyword sessions. Sharetribe's ES keyword search reads `title`, `description`, and any **`text`-schema extended-data field**; ES n-grams handle misspellings but **not synonyms** — fatal for a US-shopper ↔ Indian-brand vocabulary gap.

> **Key finding — we already generate this, but it isn't indexed.** The classifier's enrichment pass (`prompt_engine.py`) already produces `search_synonyms` and `meta_description` (diaspora-flavored, e.g. "handcrafted wood rings 6 months"), and `listing-model.js` already writes them to `publicData`. **But neither has a `text` search schema, so Elasticsearch never indexes them** — the AEO metadata sits inert. Worse, `searchSynonyms` is stored as an **array**, which under a search schema becomes **multi-enum (exact match)**, useless for free-text queries. **The gap is plumbing + schema registration, not generation.** See §4D.

**4B.1 Enriched search text field (P0)** — Ensure a top-level `text`-schema field **`searchKeywords`** (public data) — a single joined string of brand + craft + material + occasion + category terms + synonyms. Indexed into keyword relevance at `title>description>extended` weighting. Immediate recall/precision lift for query + AEO traffic at zero infra cost.

**4B.2 Diaspora synonym / transliteration layer (P0 — arguably highest-leverage native win)** — The synonym content is already generated; two changes make it work: (a) reshape from array → the joined `searchKeywords` **string** and register a `text` schema; (b) make the prompt explicitly cross-vocabulary — US-English ↔ Hindi/regional synonyms and transliteration variants (romper↔onesie, tunic↔kurta, swing↔jhula, Kanchipuram↔Kanjivaram, jhumka↔jhumki). This is the single term-matching gap ES cannot infer; it makes Mela's search *diaspora-native*. Must be flat top-level (nested is not indexable).

**4B.3 Client-side curation blend for keyword sessions (P1)** — Because `sort` and keyword relevance are mutually exclusive server-side, keyword searches return pure relevance with zero curation. Fetch by relevance, then **client-side re-rank the page** blending relevance-rank with `melaScore`/`boostTier`. Implement as one generalized client re-ranker shared with §4.8 (brand interleaving) — a single hook, two behaviors.

---

### 4D. Pipeline Integration — where each field is produced (P0)

The scoring/search fields are computed in the **existing ingestion pipeline**, split by whether the field is generative (LLM) or deterministic (JS). **The LLM never computes `melaScore`** — it can't see the whole catalog and can't be trusted for a stable number.

| Field | Owner | File / location | Status today |
|---|---|---|---|
| `item_aspects`, `seo_title`, `meta_description`, `search_synonyms` | **LLM** | `single_file_classifier.py` → `prompt_engine.py` enrichment | ✅ generated |
| `searchKeywords` (single `text` string) | derive (join) | classifier or `listing-model.js` | ⚠️ reshape array→string |
| `melaScore` (tiered), `boostTier` | **deterministic JS** | `create-listings.js` → `metadata:{}` (line ~463, currently empty) | ❌ build |
| Quality / ConversionProxy / Freshness sub-scores | JS, per-listing from `publicData` | scorer module | ❌ build |
| Discovery (brand-dampening, new-brand boost) | JS, **needs whole catalog** | `create-listings.js` pre-pass over all CSVs | ❌ build |
| Purchasability gate | JS (already gates on `'In Stock'`, line ~166) | `create-listings.js` | ✅ signal exists |
| Drift/reconciliation gate | JS | `unmapped-item-aspect-options.json` (lines 11–59) | ✅ **already exists** — extend to fail CI |

**4D.1 Turn on what's already generated (smallest change, biggest win):** reshape `searchSynonyms` array → joined `searchKeywords` string; register `text` schemas:
`sharetribe-cli search set --key searchKeywords --type text --scope public` and same for `metaDescription`.

**4D.2 Catalog-aware scorer:** `melaScore` cannot be per-row (Discovery needs every listing). Batch mode already iterates all classified CSVs — add a **pre-pass** aggregating per-brand counts, then score each listing and write `metadata.melaScore` + `metadata.boostTier=0`.

**4D.3 Re-score sweep lives here:** add a `--rescore` mode to `create-listings.js` that recomputes `melaScore` for live listings and PATCHes `metadata` only (no re-create), reusing existing auth/CSV/brand plumbing. This is the home of the 2–3 week sweep.

**4D.4 Bilingual prompt tweak:** ~3-line addition to `create_enrichment_system_prompt` to force US↔Indian/regional + transliteration pairs in `search_synonyms`.

---

### Should Have (P1)

**4.7 Sort UI cleanup** — Remove "Newest"/"Oldest" as default. Default = **Curated** (no visible dropdown label when it's the sole primary sort). Keep Price ↑/↓. Add **"Recently added"** as an *optional* sort. Keep Relevance for keyword.

**4.8 Client re-ranker: per-page brand interleaving (the only native real-time lever)** — After each page fetch (`RESULT_PAGE_SIZE`), client-side re-order in `SearchResultsPanel` to interleave brands so identical-brand cards never visually cluster, and (for keyword sessions) apply the §4B.3 curation blend. Complements the score's global dampening. Build it as a general re-ranker so lightweight session/entry signals can plug in later.

**4.9 Values filter cluster** — Group `certification` + `sustainability_claim` into one trust-forward "Values" filter, promoted to primary (serves Sarah; differentiates from generic marketplaces).

**4.10 Entry-point-aware results**
- **Social deep-link:** from a product, "explore more" opens results pre-filtered to that product's category + shared values (or same brand), leading with similar items.
- **AEO/SEO facet pages:** high-value facet combos are canonical, server-rendered, curated-sorted, indexable (coordinate with `seo-aeo-category-brand-pages-prd.md`).

### Nice to Have (P2)

**4.11 Console-tunable weights** — Expose score weights via a Console-editable asset so merchandisers tune without a deploy.
**4.12 Editorial rows** — "New Brands" / "Certified Picks" rows above the browse grid.
**4.13 Zero-result recovery** — `NoSearchResultsMaybe` relaxes the least-important active facet and surfaces curated fallbacks; feed the zero-result query log into §7's synonym loop.

---

## 5. UX Requirements
- **Default state:** curated order, no sort label shown; shopper perceives a hand-picked grid.
- **Sort menu:** Curated (default), Recently added, Price ↑, Price ↓ (+ Relevance when keyword active).
- **Category switch:** filter rail visibly reshapes to that category's relevant facets.
- **Per page:** no more than ~2 consecutive cards from the same brand (post-interleave).
- **Empty/edge states:** zero-result recovery (P2); loading and error states inherit Phase 1 handling.
- **Mobile-first:** 70%+ traffic is mobile; sort/filter controls and interleaving must hold on mobile layout.

---

## 6. Acceptance Criteria
- [ ] `melaScore` and `boostTier` metadata fields exist, type `long`, indexed, sortable, default `0`.
- [ ] `melaScore` is tier-encoded (`tier×1000 + intraTierKey`); a listing that doesn't change quality band does not change tier between sweeps.
- [ ] 100% of live listings have a non-default `melaScore` before default sort flips.
- [ ] Default browse order is `sort=meta_boostTier,meta_melaScore,-createdAt` on all surfaces where the fallback was `createdAt`.
- [ ] Non-purchasable (closed / 0-stock / known-duplicate) listings do not appear in the top 24 of any default-sorted page.
- [ ] No brand exceeds ~20% of the first page after interleaving.
- [ ] `searchKeywords` (joined string, **not array**) and `metaDescription` have registered `text` search schemas and are indexed for keyword search (spot-check: an Indian-vocabulary query e.g. "kurta"/"jhula" returns the expected English-labeled listings).
- [ ] `search_synonyms` prompt output includes explicit US↔Indian/regional + transliteration pairs.
- [ ] The `unmapped-item-aspect-options.json` drift log fails CI when non-empty.
- [ ] Keyword sessions apply the client-side curation blend (relevance + melaScore/boostTier), not raw relevance order.
- [ ] Filter rail shows only category-relevant facets when a category is active (verified for baby/kids, fashion, jewelry, home).
- [ ] Sort menu no longer defaults to recency; "Recently added" is available as an explicit option.
- [ ] Re-score sweep runs end-to-end over the full catalog and updates `melaScore` idempotently (same inputs + date → same score).
- [ ] Weights, tier boundaries, and thresholds are config-driven, not inline literals.

---

## 7. Success Metrics & Measurement
- **Browse metrics:** SRP→PDP CTR (+15%), outbound/affiliate click rate (+10%), top-24 brand diversity (≤20%/brand), dead-link exposure (~0%).
- **Keyword/search-quality scorecard** (a dedicated dashboard, not generic page analytics): **CTR@10, MRR, zero-result rate, low-result-count rate, outbound-click@k**, tracked per sweep to catch regressions.
- **Golden-set eval:** 30–50 representative queries (incl. diaspora terms) with hand-judged "should-be-top" results; run each sweep as a relevance regression gate.
- **Zero-result mining loop:** log queries returning nothing/little → feed back as new `searchSynonyms` and vocabulary fixes. Cheapest recurring relevance win, especially for Indian-term misses.
- **Required analytics events** (dependency on Phase 1 instrumentation): `search_results_view` (sort + entry-point + query), `result_card_click` (position, brand, melaScore tier), `outbound_click`, `sort_changed`, `filter_applied`, `zero_results` (query). Without position + tier + query logging we cannot validate ranking quality or graduate to behavioral weighting.
- **A/B or before/after:** compare curated default vs. recency baseline; compare keyword relevance with/without the enriched `text` fields.

---

## 8. Dependencies & Risks
- **[BLOCKER] Analytics baseline** unshipped (`search-page-optimization-prd.md` Phase 1). All targets are TBD until it lands.
- **[BLOCKER] Full backfill before sort flip** — else unscored listings sort last and vanish.
- **Array-vs-text schema trap** — `searchSynonyms` is currently stored as an array (`listing-model.js:449`); a search schema on an array is **multi-enum (exact match)**, not `text`, so it would do nothing for keyword relevance. Must be a joined string under a `text` schema. Same check: confirm `metaDescription` actually has a `text` schema or it isn't indexed either (today it isn't).
- **Config sync drift** — the classifier keeps aspects category-scoped via a shared **options CSV**, aligned to `configListing.js` **by naming convention, not a shared source of truth**. *Mitigation already partially built:* `create-listings.js` logs unmapped options to `unmapped-item-aspect-options.json` (lines 11–59) — extend it to **fail CI** on non-empty output; this protects both filtering and the completeness sub-score.
- **Purchasability signal freshness** — the score is only as honest as the reconcile data; stale stock → dead links resurface. Tie re-score sweep to reconcile cadence.
- **Frozen-score drift** — Freshness and Discovery terms drift daily/as catalog grows; the 2–3 week sweep bounds staleness but does not eliminate it between runs. Acceptable at current scale; revisit if catalog velocity rises.
- **Whole-number precision** — tier-encoded 0–10000 gives adequate resolution; avoid finer scales that imply false precision.
- **No per-query diversity from a scalar** — global order can't guarantee per-*result-set* diversity; mitigated by client-side interleaving (§4.8), which only reorders the fetched page, not cross-page.
- **Reindex write-load** — writing `melaScore`/`boostTier`/text fields to N listings triggers N reindexes; the bottleneck is Marketplace API write throughput, not ES. The sweep must batch + backoff within rate limits.
- **Console-vs-CLI schema conflict (409)** — a field's search schema can be managed by Console *or* CLI, not both. Decide per field (`melaScore`, `boostTier`, `searchText`, `searchSynonyms`) before creating it; a Console-defined key cannot later be CLI-edited.
- **Nested data not indexable** — every scoring/keyword input (`searchText`, `searchSynonyms`, all facets) must be a **flat top-level** extended-data key. Classifier output must not nest them.
- **Keyword vs. sort mutual exclusivity** — server-side you get one or the other; the curation blend for keyword sessions is client-side only (§4B.3) and thus limited to the fetched page.
- **QA = pseudo-production** — live traffic runs off the QA/dev Sharetribe env; treat QA rollout as live rollout.

---

## 9. Phased Rollout (supersedes single-track sequencing)
Revised per the search-engineering panel — front-load the cheap, diaspora-critical keyword wins:
- **Phase A — Browse ranking:** tier-encoded `melaScore` + `boostTier` + 3-key default sort + backfill guardrail + purchasability gate. *(serves browse traffic)*
- **Phase B — Keyword enrichment:** `searchText` + `searchSynonyms`/transliteration `text` fields, classifier-generated. *Do early — cheap and diaspora-critical for query + AEO traffic.*
- **Phase C — Client re-ranker:** one hook for brand interleaving + keyword curation blend (§4.8, §4B.3).
- **Phase D — Search-quality flywheel:** scorecard + golden-set eval + zero-result → synonym loop (§7).
- **Phase E — External index (only if outgrown):** mirror via Integration API; `melaScore` + text fields port directly.

## 10. Out of Scope / Future Considerations
- **External search layer** (Algolia/Typesense): unlocks real-time composite ranking, custom analyzers, true personalization, vector/semantic search — none available through Sharetribe's exposed ES DSL. Deferred to Phase E.
- **Behavioral weighting**: once outbound-click / save / dwell data accrues, add a conversion term from real signal (architecture already supports it — swap the proxy for measured CTR).
- **Monetized placement** (featured slots) — technically trivial on this pattern (`boostTier` already exists), but a positioning decision, deferred.

---

## Appendix A — Reference scorer sketch (for `create-listings.js`)
```js
// each sub-score returns 0..1; weights, tier boundaries & thresholds come from a config object
const quality    = w([certScore, sustainScore, materialScore, storyScore, completeness, imageScore]);
const conversion = purchasable ? w([bestseller, priceOk, multiImage]) : 0; // near-hard gate → forces tier 0
const discovery  = brandDampen(brandListingRank) * newBrandBoost(brandSize);  // needs global catalog stats
const freshness  = Math.exp(-ageDays / HALF_LIFE_45);
const composite  = 0.35*quality + 0.30*conversion + 0.20*discovery + 0.15*freshness; // 0..1

// tier-encode for stability + explainability: coarse band × 1000 + fine intra-band key
const tier         = purchasable ? Math.min(9, Math.floor(composite * 10)) : 0; // stable band
const intraTierKey = Math.round((composite * 10 - Math.floor(composite * 10)) * 999);
const melaScore    = tier * 1000 + intraTierKey; // 0..9999, whole number

// write listing.metadata.melaScore (idempotent: pure fn of listing state + today's date)
// boostTier is written separately by editorial tooling, NOT by this scorer.
// searchText + searchSynonyms are written by the classifier as flat top-level text fields.
```

## Appendix B — Why native-only (superseded alternative, kept per house rule)
An **external search layer** (Algolia/Typesense) was considered and set aside for v1. It would allow real-time composite/personalized ranking and richer matching, but adds infra cost, a sync pipeline, and operational surface the team chose not to take on before proving the ranking model. The native stored-score approach delivers ~80% of the ranking benefit at near-zero new infrastructure and ports cleanly into an external layer later. Revisit when: (a) behavioral data justifies per-request scoring, or (b) catalog velocity makes the 2–3 week sweep too stale.
