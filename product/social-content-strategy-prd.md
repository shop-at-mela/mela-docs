# Social Content Strategy, Plan & Automation
**Status:** Active — reflects live tooling (Blotato) and operational skills
**Last Updated:** July 2026
**Owner:** Mela Product

---

## Problem

Mela's web experience is currently optimized for users who arrive with intent (search, category browse). The majority of the target audience — Sarah, Arun, and Priya — arrives without intent, needing inspiration before they can have purchase motivation. Social platforms (Pinterest, Instagram, Reddit) are where inspiration happens, but Mela has no systematic strategy for driving that inspiration traffic to the web app, and no automation to keep social content in sync with what's live on Mela.

The result: social presence requires constant manual effort to maintain, product/brand data on Mela isn't being leveraged as a content source, and new brand and product launches have no automatic social amplification.

---

## Background: Why Inspiration-First, Not Brand-First

Research and persona analysis (see [buyer-personas.md](../UXR/buyer-personas.md)) shows the audience splits by intent:

- **Neha** (first-gen immigrant) — brand-aware, arrives knowing what she wants
- **Sarah** (conscious American parent) — brand-unaware, arrives by attribute ("organic baby clothes")
- **Priya** (mixed heritage parent) — occasion-aware, arrives by moment ("Diwali gift for baby")
- **Arun** (second-gen) — brand-unaware and occasion-learning, needs aesthetic inspiration as entry point

Amazon/eBay are retrieval tools — you go knowing what you want. Mela's differentiation is that people come for inspiration. That means social should handle the top-of-funnel inspiration work and the web app should be the place that catches that inspired intent and converts it — not a parallel search engine.

**Competitive models that solved this:**
- **Wolf & Badger** (independent designer curation): editorial lives on-site, Instagram links to Journal posts
- **Not On The High Street**: occasion-first navigation, editorial gift guides
- **LTK**: social does inspiration, web app does conversion — job separation is the model
- **Etsy + Pinterest**: Pinterest is Etsy's highest-volume referral channel; catalog auto-sync does the work

---

## Goals

1. Generate social content primarily from Mela's existing product and brand data (product CSVs, brand pages) — not manually written from scratch.
2. Give each platform a defined job (top-of-funnel vs. trust vs. community) and content type.
3. Run a repeatable, skill-driven production loop (`/social-launch`, `/social-review`) that a single operator can sustain in ≤3 hours/week.
4. Establish Pinterest as the highest-ROI channel given the home/lifestyle/gifting category fit.
5. Keep a machine-readable record of every campaign (YAML logs) so the system avoids repeats, rotates categories/personas, and learns from UX observations.

---

## Non-Goals

- Building a native social feed inside the Mela web app.
- Automating Reddit (requires authentic human participation — automation is harmful there).
- TikTok in Phase 1 (requires video production infrastructure not yet in place).
- Social commerce checkout integration (Pinterest "Buy" button, Instagram Shopping catalog checkout) — complex, deferred.
- Music/audio on visuals — Blotato's image-slideshow and product-scene templates are silent by design; add trending audio natively in-app if/when Reels launch (see [visual-style-guide.md](../social/visual-style-guide.md)).

---

## Current Status (July 2026)

- **Accounts:** Instagram [@shopatmela](https://www.instagram.com/shopatmela/) + Pinterest [@shopatmela](https://www.pinterest.com/shopatmela/), both in **warmup phase** since June 2026.
- **Publishing engine:** Blotato (free plan) via MCP, driven by the `/social-review` and `/social-launch` skills.
- **Pinterest:** manual posting (~1 pin/day) during warmup — Catalog API auto-sync not yet built (see Technical Plan, Phase A).
- **Campaigns logged:** Fizzy Goblet (Weeks 1–2), The Alternate (Week 1) — all fashion/footwear. See `../social/log/*.yaml`.
- **Known gap:** every campaign to date is fashion; Pinterest's documented sweet-spot categories (home, baby, jewelry, gifting) are untested. Category-rotation guardrails exist in both skills but haven't yet pulled production into a Pinterest-native category.
- **Priority vs. effort (deliberate):** Pinterest is the *target* primary channel (highest ROI), but it's **gated on the Catalog Feed** (Technical Plan, Phase A) — until that ships, Pinterest is manual ~1 pin/day and **Instagram carries the warmup production load** (hence the theme-row grid investment). This is sequencing, not a change of priority: when the Catalog Feed lands, Pinterest volume scales automatically and Instagram stays the trust layer.

---

## Platform Strategy

### Pinterest — Target Primary Channel (manual during warmup, gated on Catalog Feed)

**Why:** Pinterest users are in discovery/inspiration mode, not purchase mode. Products in home, lifestyle, baby, gifting categories perform best here. Etsy drives significant revenue through Pinterest. Users clicking Pinterest pins have higher purchase intent than Instagram users. This is the lowest manual effort, highest conversion channel for Mela's product mix.

**Content types:**
- **Product Pins** — individual pins linking to a specific Mela listing (`https://www.shopatmela.com/l/{Dev_Listing_ID}`). Today posted via Blotato/manual; at scale, auto-synced via Pinterest Catalog Feed (Technical Plan, Phase A).
- **Occasion Boards** — curated boards for Diwali, New Baby, Modern Indian Nursery, Organic Baby Essentials, Heritage Gifting. Updated seasonally.
- **Styled collection images** — 5-product flat-lay or lifestyle imagery organized around a visual theme (not isolated product shots).

**Cadence:** Warmup: ~1 pin/day (manual). Target (post-Catalog Feed): 5–10 pins/day automated + monthly manual board curation.

**Link destinations:** Mela listing pages (Product Pins) and Mela collection/category pages (boards). Use specific product URLs, not brand pages, for conversion.

**Automation level:** Warmup ~0% (manual). Target ~90% via Pinterest Catalog API.

---

### Instagram — Carries Warmup Execution Today (Secondary Channel long-term: Brand & Cultural Education)

**Why:** Priya already discovers Indian items on Instagram. Arun follows Indian-American parenting accounts. Instagram is the trust-building layer — it tells the brand story behind the product that converts a browser to a buyer. Instagram engagement ≠ direct purchase; it builds the brand recognition that makes Mela web app visits convert.

**Content types:**
- **Brand Spotlight Carousels** (6–8 slides): brand origin story, 3+ product highlights, link to Mela brand page. Semi-automated — Blotato visuals + skill-drafted caption.
- **Collection Carousels** (4–7 slides): 3+ products from one brand or occasion, lifestyle-staged. Current default format.
- **Cultural Education Reels**: e.g. "Block printing: 500 years old, still made this way." Weekly topic drawn from [`education-topics.yaml`](../social/education-topics.yaml) (one education row/week).
- **Anchor Teaser Reels**: the reels-first center-tile anchor of each brand-themed row — a motion photo-collage that converges into the brand/theme wordmark (no product shown). ~2/week. Semi-automated: Blotato builds the collage, but trending audio + final publish are a manual in-Instagram step (Blotato templates are silent); fall back to a static theme card when a reel can't be produced. See [`visual-style-guide.md`](../social/visual-style-guide.md) → Instagram Grid Row Anchors.
- **Trust/Service posts** (feed + Stories): international shipping (realistic 5–7+ day timelines from India), product quality/materials, customer service, returns, USD payment, sizing. Addresses the purchase objections that block conversion — **Neha** (shipping reliability, fair price), **Sarah** (quality, safety). Weekly topic drawn from [`education-topics.yaml`](../social/education-topics.yaml). **Instagram + Reddit only — never Pinterest** (Pinterest is discovery mode; nobody browses pins to evaluate shipping).
- **New Arrivals Stories**: template card — product image + "Now on Mela."
- **Occasion/seasonal posts**: Diwali countdown, Holi, New Year. Scheduled 4–6 weeks in advance.

**Feed layout:** The IG feed is planned as **theme-rows of 3** — a weekly batch = **3 rows (9 tiles): 2 brand-themed rows + 1 education row**, each with a reels-first anchor in the center tile. Brand rows are `[craft/founder story] · [anchor] · [product]` (story + product, not a catalog). The executable spec lives in [`category-routing.yaml`](../social/category-routing.yaml) → `grid` (not restated here, to avoid drift).

**Cadence:** 9 feed posts/week (three theme-rows); Stories = overflow (grid-neutral). Canonical cadence lives in [`category-routing.yaml`](../social/category-routing.yaml) → `cadence` by `active_phase`.

**Link destinations:** Link in bio rotates to the most relevant collection page for the current season; posts deep-link to Mela brand pages.

**Automation level:** ~50%. Visuals + caption drafts are skill-generated; creative review is human before posting.

---

### Reddit — Trust Channel, Human-Only

**Why:** Neha and Priya are active in diaspora parenting communities. Reddit trust is earned through authentic expertise. A single genuinely helpful answer about Indian baby certifications is worth more than 100 Instagram posts for this persona. Reddit penalizes promotional behavior severely — this channel requires patience and genuine contribution.

**Content types:** helpful answers (never promotional); quarterly AMA-style posts; resource links only when directly relevant. **Trust/service** is the natural Reddit contribution — genuine answers about international shipping, product quality/safety, sizing, and returns for Indian brands (shared source with Instagram trust/service posts via [`education-topics.yaml`](../social/education-topics.yaml)).

**Cadence:** 3–5 quality community interactions per week. **Automation:** None — founder/team time.

**Key subreddits:** r/IndiaMoms, r/AsianParenting, r/SustainableFashion, r/BabyBumps, r/EcoParenting, r/ZeroWaste, r/IndianFashion.

---

### TikTok — Phase 2 (Deferred)

Highest upside but requires consistent video production. Best angle: founder as face of brand, brand-discovery storytelling. Consider after Pinterest and Instagram are running at cadence.

---

## Operational Engine: The Two Skills

Content production runs through two Claude Code skills. They are the day-to-day interface to this strategy; the sections below (caption, visual, logging) are the rules those skills enforce.

### `/social-launch` — Batch Cold-Start (Month 1)

Bootstraps a week of content at once and coaches the operator through cold-start execution.

| Phase | Action |
|---|---|
| 0 | Read all `../social/log/*-campaign-*.yaml` — flag prior brands/products for exclusion; scan last 5 posts for category concentration |
| 1 | Select **2 brands (different categories)** + a hero product & story angle each, plus **1 education topic**; exclude prior-campaign brands |
| 2 | Plan the week's **3 theme-rows** (2 brand-themed + 1 education) per `category-routing.yaml` → `grid`; apply category/persona rotation |
| 3 | Batch-create visuals + captions (uses `/social-review` internally) |
| 4 | **Review gate (mandatory)** — display Review Sheet; approver signs off or flags redos |
| 5 | Refine flagged posts, re-review |
| 6 | Batch-schedule in Blotato |
| 7 | Log campaign to YAML |

### `/social-review` — Single Post / Small Batch (7 phases)

| Phase | Action |
|---|---|
| 1 | Read campaign history + aggregate `ux_review.observations` across all logs |
| 2 | Strategy: format table → platform → persona → board → destination URL → Indian anchoring; run **freshness checks** (brand recency <7d, persona fatigue 3+/5, category concentration 3+) |
| 3 | Blotato visual (real product images only) + platform/persona-specific caption; Canva fallback for text-only |
| 4 | UX review of the destination page |
| 5 | Record findings into the campaign YAML `ux_review` block |
| 6 | Approve & publish via Blotato (`create_post`); never auto-publish |
| 7 | Campaign logging (YAML) |

---

## Caption Strategy & Persona Guardrails

**Base structure (all platforms):** Origin story → craft/cert detail → occasion/use → CTA ("Discover [brand] on Mela →").

**Platform structure:**
- **Pinterest:** Title ≤60 chars + 2–3 sentence keyword-rich description. End: "[Brand] on Mela."
- **Instagram Feed:** persona-led order (below) + "Featured in this carousel: [product list]" for destination-page findability.
- **Instagram Stories:** "[Product] · New on Mela →".

**Persona-specific lead:**
| Persona | Lead with | Guardrail |
|---|---|---|
| **Sarah** | Certification → materials → use | Never claim "sustainable/eco-friendly/natural" without a **specific cert**; omit if unsure |
| **Priya** | Occasion → craft origin → use | Avoid "traditional/ethnic/Bollywood/costume"; use occasion or regional-craft framing |
| **Arun** | Craft origin + cultural context → use | Include ≥1 sentence glossing craft terms (e.g. "kolhapuris — handcrafted leather sandals from Maharashtra") |
| **Neha** | Regional specificity → use | Not a primary angle; skip price callout (she knows INR pricing) |

**Standing guardrails (all personas):**
- **Indian Anchoring (non-negotiable):** describe the product's craft origin, never the buyer's identity. ✓ "Hand-woven in a 4th-generation Varanasi workshop" ✗ "Perfect for Indian-American families."
- **Discovery, not access:** "hard to find," never "unavailable in the US."
- **Affiliate copy precision:** Mela does not hold inventory or ship. Never "we ship / available from Mela / Mela delivers." Use "ships from India," "brand ships to the US," "discovered on Mela."
- **Shipping trust-signal:** captions reaching diaspora/gifting audiences must name the shipping actor ("Ships to the US from [Brand]") — never an ownerless "Shipped to the US."

**Enforcement (why this section exists twice):** these rules were already documented when the first 4 campaigns shipped with an ownerless "Shipped to the US" line and banned "ethnic wear"/"traditional" phrasing anyway — the gap was never the rule, it was that nothing checked copy against it before publish. `/social-review` Phase 4–5 must diff every caption and pin description against this table before logging `ux_review` or `notes` — and a banned phrase must never be logged as compliant (Week 2's log did exactly this: `notes.shipping_clarity` praised the ownerless line as a positive). If a violation ships anyway, the log must say so, not paper over it.

**Banned-phrase quick reference:** "ethnic wear," "traditional" (as a product descriptor), "Bollywood," "costume," "sustainable/eco-friendly/natural/ethically made" (without a named cert), ownerless "Shipped to the US," "we ship / available from Mela / Mela delivers."

---

## Visual System

Governed by [visual-style-guide.md](../social/visual-style-guide.md). Baseline (non-negotiable across all categories): natural backgrounds (marble/wood/linen/stone), soft golden-hour light, calm artisanal mood (Amala Earth-inspired), earthy palette, "Discovered on [Mela Logo]" watermark bottom-right, no product titles/prices/text overlays on images.

**Blotato templates:**
| Use case | Template | Notes |
|---|---|---|
| Single product + real photo | Image Slideshow (`5903b592…`) | Silent; pass real product image URL |
| Product in lifestyle scene | Product Scene Placement (`f524614b…`) | Still image; scene described in prompt |
| Text/logo-only card | — (use Canva) | Mela brand kit; navy #2D2D7B + marigold #F0A030 |

**Category-specific accents** (within baseline) are defined per category in the style guide. **Platform routing** — which platform leads each category, plus persona, board, format, and cadence — is the executable source of truth in [`category-routing.yaml`](../social/category-routing.yaml), consumed by `/social-launch` and `/social-review` at Phase 2 (not restated here, to avoid drift). In summary: **Pinterest leads** home, baby, jewelry, food, and beauty (discovery / gifting categories); **Instagram leads** fashion and art & craft (story-dependent categories).

> **Note:** "Always use real product images from the product CSV. Never AI-generate the product itself." The scene/background may be AI-styled; the product may not.

---

## Campaign Logging & Feedback Loop

Every published campaign is recorded as `../social/log/[brand-slug]-week-[N]-campaign.yaml` per `CAMPAIGN_TEMPLATE.yaml`. This is the system's memory and the input to freshness/rotation checks.

**Each log captures:** metadata (brand, week, date, platforms, format, persona, category); full Instagram section (caption, products with image URLs, Blotato visual IDs, prices, listing IDs); full Pinterest section (pins with titles, descriptions, links); a `ux_review` block (per-check results + observations); and notes.

**The `ux_review` block replaces the retired `ux-observations.jsonl`.** UX findings from `/social-review` Phase 4–5 are written inline per campaign with `theme`, `severity`, `status`, `description`, `mitigation`. If a theme reaches 3+ open observations across all logs, the skill surfaces the pattern as a systemic product-page issue to route to the dev backlog.

**Guardrails enforced from the logs:**
- **Brand recency:** same brand posted <7 days → suggest alternative.
- **Persona fatigue:** same persona 3+ of last 5 posts → rotate.
- **Category concentration:** 3+ consecutive posts same category → require a different Mela category.

**Attribution (UTM):** every destination URL in a log — listing links, brand-page links — must carry the UTM schema defined in [`category-routing.yaml`](../social/category-routing.yaml) → `tracking` before publish. None of the first 4 campaigns did this, which means the "Pinterest referral > 5% of GA4 sessions" success metric (below) has no data to be measured against yet. This is the single highest-leverage fix available — it's a template change, not an engineering project, and it unblocks every downstream measurement decision (including whether Phase A is worth building).

---

## Automation Architecture

**Core principle:** Mela's product and brand data is the content source. Social content is generated from that data, not created independently.

**Tooling reality:** Blotato (via MCP + the two skills) now performs visual creation, scheduling, and multi-platform publishing — collapsing what the earlier plan split across Canva + Buffer + Claude API. Two capabilities remain **outside** Blotato:

1. **Trigger layer** — Blotato has no visibility into Mela's Sharetribe backend. "New listing → auto-draft" requires a watcher (cron script or Zapier/Make) polling Sharetribe and calling Blotato. **Until built, automation is skill-triggered** (operator runs `/social-launch` / `/social-review`), i.e. assisted batch, not event-driven.
2. **Pinterest Catalog Feed** — Blotato posts individual pins, not a live product catalog. Catalog-scale Pinterest (nightly price/stock auto-sync) still needs the `/feeds/pinterest` endpoint + Pinterest Catalog Manager.

### Triggers (target state, once the watcher exists)

| Trigger | Auto-action | Manual step |
|---|---|---|
| New product listed | Pinterest pin (Catalog nightly) + IG Story drafted in Blotato | 5-sec IG approve |
| New brand goes live | Blotato IG carousel drafted + Pinterest brand board | Caption review + approve |
| Seasonal event (4 wks out) | Blotato queue populated (~12 posts) | 30-min queue review |
| Price / stock change | Pinterest catalog pin updated/removed (nightly) | None |

---

## Content Calendar (Recurring)

Every week is the same **structure** — 3 IG theme-rows (2 brand-themed + 1 education) + daily Pinterest pins + Reddit presence. What rotates week to week is the **brands, education topic, and any seasonal overlay**:

| Week | Pinterest | Instagram (3 rows/wk) | Reddit (human) |
|------|-----------|-----------------------|----------------|
| W1 | Product pins / catalog | 2 brand rows (rotate categories) + 1 education row | 1–2 community answers |
| W2 | Product pins / catalog | 2 brand rows (new brands/categories) + 1 education row | 1–2 community answers |
| W3 | Product pins / catalog | 2 brand rows + 1 education row | AMA prep or Q&A |
| W4 | Product pins / catalog | 2 brand rows + 1 education row (seasonal overlay if event ≤6 wks out) | 1–2 community answers |

**Weekly manual effort target:** creation ≤3 hrs (one `/social-launch` batch) + ~30 min/day engagement + Reddit 30–45 min. *Reels-first anchors push creation time up; default to static theme cards to stay within budget.* Canonical cadence: `category-routing.yaml`.

---

## Technical Implementation Plan

Blotato + the skills cover creation/scheduling/publishing today. The remaining engineering is what makes automation *event-driven and catalog-scale*.

### Phase A — Pinterest Catalog Feed (2–3 days eng)
Server-side `/feeds/pinterest` route in the Mela web-client that queries active Sharetribe listings (pattern used in CategoryShowcase) and returns a Pinterest-compatible XML catalog (`id`, `title`, `description`, `link`, `image_link`, `price`, `availability`, `condition`, `brand`, `product_type`). Register in Pinterest Catalog Manager; pins auto-create nightly. **Unblocks:** Pinterest target cadence (5–10/day) + price/stock auto-sync.

### Phase B — Trigger Watcher (3–5 days, light eng)
Cron or Zapier/Make job polling Sharetribe for newly published listings / new featured brands → fetch data → call Blotato (MCP or API) to draft the visual + caption → land in Blotato's scheduled/draft queue → Slack notification. **Unblocks:** event-driven drafting (vs. operator running skills).

### Phase C — Seasonal Calendar Automation (2–3 days, light eng)
Monthly cron checking the hardcoded seasonal calendar; if an event is 4 weeks out, query Sharetribe by occasion tag, generate drafts, push a Blotato queue spread over the window, send a digest.

**Seasonal calendar:**
| Season | Trigger date | Products sourced by |
|--------|-------------|-------------------|
| Diwali | Oct 1 | `pub_occasion=diwali-festivals` |
| New Year gifting | Dec 1 | `pub_occasion=gifting` |
| Mother's Day | Apr 1 | gifting + jewelry + home |
| New Baby (evergreen) | Monthly | newborn + 0–6 months |

**Note:** this table's generic "4 weeks out" trigger is for content generation broadly. Pinterest boards specifically need to go live earlier than that for search indexing — see `accounts.md` → Seasonal Calendar for per-event Pinterest lead times (Diwali: mid-August, not Sept 1).
| Holi | Feb 1 | fashion + art-craft |

---

## Tool Stack & Cost

| Tool | Role | Monthly cost |
|------|------|-------------|
| **Blotato** | Visual creation, scheduling, multi-platform publish (replaces Canva + Buffer for most flows) | Free plan today; paid tier at scale |
| Claude Code skills | Strategy, caption generation, UX review, logging | Incl. in Claude usage |
| Pinterest Business | Catalog feed + pin management | Free |
| Canva (optional) | Text/logo-only cards, brand-kit graphics | $0–13 |
| Trigger layer (future) | Sharetribe→Blotato watcher (Zapier/Make or cron) | $0–29 |
| Anthropic API (future, headless) | Caption gen outside interactive skills | ~$5–10 pay-per-use |

**Superseded:** the earlier Buffer (Essentials) + Zapier (Starter) + Canva Pro stack (~$44–70/mo) is replaced by Blotato + skills for interactive production. Zapier/Make returns only if/when the Phase B watcher is built.

---

## Success Metrics

**Warmup (Month 1, current):**
- Both accounts posting on a consistent cadence ✓
- Aesthetic consistency (reviewer signs off) ✓
- ≥1 non-fashion, Pinterest-native category tested
- Baseline data: which categories/brands drive saves + clicks

**Months 3–6 (early traction):**
- Pinterest Catalog Feed live and syncing daily
- Pinterest monthly impressions > 50K
- Pinterest referral traffic to Mela > 5% of total sessions (GA4)

**Months 6–12 (validation):**
- Social referral sessions have higher avg. time-on-site than direct/organic
- At least one non-Neha persona (Sarah or Arun) converting through social referral
- Manual content production time confirmed ≤3 hours/week

---

*Informed by: Mela buyer personas (April 2026); competitive analysis of Wolf & Badger, Not On The High Street, LTK, Etsy/Pinterest; live tooling (Blotato) and the `/social-review` + `/social-launch` skills; visual-style-guide.md, accounts.md, and campaign logs as of July 2026.*
