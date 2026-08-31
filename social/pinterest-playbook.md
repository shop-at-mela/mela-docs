# Pinterest Playbook

Mela's single reference for Pinterest cold-start growth (no ads). Pinterest is a **search +
planning engine**, not a feed — pins surface via search and related-pins, almost never by anyone
browsing your boards. Everything here follows from that.

**Contents:** 1 · Foundation · 2 · Board architecture · 3 · Tags · 4 · Keyword bank · 5 · Board copy · 6 · Pipeline-generated pin copy

Board decisions are also encoded in `category-routing.yaml → pinterest_boards` (executable source
of truth that the `/social-review` + `/social-launch` skills read). This doc holds the rationale.

---

## 1 · Foundation

Three foundations gate distribution. Do them before optimizing content.

| Pillar | Status | Notes |
|---|---|---|
| **Domain claim** | ✅ done 2026-08-03 | `<meta name="p:domain_verify">` in `web-client/public/index.html` (SSR head), deployed; `shopatmela.com` claimed in Pinterest. Unlocks pin attribution + "More from this site". |
| **Rich Pins** | ✅ live | Listing pages already emit server-rendered schema.org `Product` JSON-LD (price, currency, availability, brand) via `ListingPageCarousel.js`. Validated + applied → price/stock render on every pin. |
| **Keyword SEO** | 🔄 ongoing | This doc (§4–5). Keywords, not hashtags, are Pinterest's real ranking surface. |

Why it matters: at cold start, 15–30 impressions with 0 clicks is *expected math* (0.2–2% CTR on
30 views ≈ 0 clicks). The bottleneck is **distribution (impressions)**, not CTR — which is what
the foundation + keywords fix. Give pins 30–90 days; Pinterest content has a long search tail.

## 2 · Board architecture

**Panel decision (2026-08-06).** A board earns its place only if (a) its name/description rank in
search and (b) it gives pins topical context. Judged that way, of the four candidate board types:

| Type | Verdict | Why |
|---|---|---|
| **Category** | ✅ Keep — the spine | Highest evergreen search volume; maps to catalog |
| **Occasion** | ✅ Keep — highest Pinterest ROI | Pinterest is a planning engine; diaspora searches occasions early |
| **Gift** | 🔀 Merge into occasion | Diaspora gifting is occasion-anchored; keep ONE evergreen gift board, not a family of them |
| **Brand name** | ⏸️ Skip at cold start | Weakest discovery — nobody browses a marketplace's brand boards. Revisit post-traction. **Pinterest-only** — brands stay first-class on Instagram |

**Cold-start target set (~6 boards):** Home and Kitchen · Handmade Indian Juttis & Artisan Footwear ·
one **merged** Baby & Kids (the two thin nursery/organic boards collapse until volume justifies a
split) · Ayurvedic Skincare & Natural Beauty · Diwali Gifting (seasonal) · Indian Gift Ideas &
Festive Occasions (the evergreen gift/occasion board). Add jewelry/food category + more occasion
boards as pin volume arrives. Fewer, fuller boards beat more, thinner ones at ~10 total pins.

**Brand boards:** *Fizzy Goblet* and *The Alternate* were consolidated into theme boards and
**archived** (reversible) 2026-08-06 — do not route pins to them. Supersedes the earlier "keep as
optional secondary destination" stance.

### New theme/attribute board? Run this checklist first

**Proposed generalization (2026-08-30), inferred from the sustainability/vegan case below — not
yet panel-ratified as formal policy, treat as the working default until it is.** The board-type
table above only covers category/occasion/gift/brand. When a *new* cross-cutting attribute shows up
(sustainability, plus-size, a regional-craft micro-niche, a price tier — anything that isn't a
catalog category, an occasion, or a brand) the instinct is to ask "doesn't this deserve its own
board?" Answer it with this checklist before creating one:

1. **One category, or several?** Does the attribute map to a single catalog category, or does it
   cut across two or more (e.g. footwear + apparel)? Cross-category attributes fight the "one
   keyword cluster ≈ one board" rule (§4) — a board can't cleanly hold a cluster that spans boards.
2. **One brand, or several?** Check live-pin count against `brand_board_threshold` (8). An attribute
   carried by a single brand is a brand board wearing a theme costume — exactly the thin-board
   pattern the 2026-08-06 archival (Fizzy Goblet, The Alternate) rejected.
3. **Already-ruled-on board type, or a new one?** If this attribute doesn't fit category / occasion
   / gift / brand, it's a **policy gap**, not a routing-yaml edit. Flag it explicitly rather than
   deciding unilaterally — it needs the same panel-level review the original four types got.
4. **Default:** keyword layer within the existing relevant board(s), not a new board. Revisit only
   once (1) resolves to a single category or a deliberate multi-board keyword set, **and** (2) shows
   multiple brands at real volume, not one.

Worked example: `sustainability_and_vegan` in §4 below applied this and landed on keyword layer, not
a board (single brand, 3 pins, spans footwear + apparel, and "attribute board" isn't a ruled-on
type).

### 2b · Format experiment: education carousels (test, not a committed lane)

**Decision (2026-08-06).** Pinterest's native composer offers multi-image collages/carousels. **Never for product pins** — a single-image pin linking to one listing is what carries Rich Pins (§1) and the Phase 7b scent-match; a collage has no single source listing and forfeits both.

The one opening: **education content** (IG-only today, no Rich Pin metadata or scent-match to lose). How-to/explainer carousels ("How to style a Diwali table," "What is Pattachitra") are what users search and save. Run as a **manual, in-composer test** (not Blotato):
- **Scope:** 1–2/month, posted by hand to the relevant category/occasion board.
- **Source:** an existing `education-topics.yaml` topic + its Education Visual System slides (slide 1 = hook). No product tagging.
- **Kill/keep at 30–60 days:** keep only if carousels beat single-image education pins on saves/impressions (long-tail, not week-1).

## 3 · Tags on Pinterest

**Keywords, not hashtags.** "Tags" means four things:
1. **Hashtags → dead, skip.** ~Zero ranking weight. Keywords (title, description, board name/description, alt text) are Pinterest's real tagging mechanism. 1–2 hashtags max if you must.
2. **Interest/topic tags at pin creation → use** the genuinely relevant ones (don't stuff).
3. **Tagged products (shoppable) → later**, once catalog/Rich Pins mature (ties to the Catalog Feed target in `cadence`).
4. **"Pinterest Tag" → a conversion pixel** for shopatmela.com, not discovery. Install once outbound clicks exist (pairs with GA4/UTM).

---

## 4 · Keyword bank (starter)

Seed keywords per Mela category — for board names/descriptions, pin titles, pin descriptions, and
alt text. These terms are distribution, not decoration.

**Audience lens:** Mela's schema declares "Indian Diaspora Shoppers in USA." Diaspora search
intent blends three axes — **craft/heritage** (block print, Pattachitra), **occasion**
(Diwali, Raksha Bandhan, baby shower), and **US-gifting** ("Indian [x] USA", "gift for").
Good pins combine one term from at least two axes.

> ⚠️ **These are research-informed seeds, not verified volumes.** I can't query live Pinterest
> autocomplete/Trends from here. Before a term goes into rotation, validate it: type the seed
> into Pinterest search, record the autocomplete tail, and sanity-check seasonality in Pinterest
> Trends (trends.pinterest.com). Keep/expand the winners; drop terms that autocomplete doesn't echo.

---

## How to use the bank (placement priority)

| Slot | Weight | Rule |
|---|---|---|
| **Board name** | highest | Lead with the primary keyword of the cluster (not a cute name). |
| **Board description** | high | 1–2 sentences, 2–3 cluster keywords, natural language. |
| **Pin title** | high | Front-load the primary keyword; keep readable. |
| **Pin description** | medium | 2–4 sentences; first ~50 chars carry the intent; 2–3 related terms. |
| **Alt text** | medium | Literal, keyword-rich description of the image. |
| **Hashtags** | low | 2–3 max; low ranking weight on Pinterest now. |

**One keyword cluster ≈ one board.** After ~2–4 weeks, Pinterest Analytics shows which terms
earned impressions — prune dead terms, double down on winners, and make new pins for
high-volume terms that have no pin yet (content-gap filling).

---

## Per-category clusters → live boards

Board ids from `category-routing.yaml → pinterest_boards.boards`.

### home_and_kitchen → *Home and Kitchen* (`…3626`) · *Gifting and Occasions* (`…3628`)
- **Primary:** hand painted ceramics · Indian dinnerware · bone china mug · artisan tableware
- **Occasion:** Diwali table setting · festive tablescape · housewarming gift · Diwali home decor
- **Craft/AEO:** Pattachitra art · Phad painting · hand-painted pottery
- **US-gifting:** Indian home decor USA · ethnic home decor · Indian housewarming gift

### baby_and_kids → *Modern Indian Nursery* (`…3629`) · *Organic Baby Essentials* (`…3630`) · festive → *Gifting and Occasions* (`…3628`)
- **Primary:** Indian baby clothes · ethnic baby outfit · organic cotton baby clothes
- **Craft:** hand block print kids clothing · hand embroidered baby outfit
- **Occasion:** festive kids wear · Diwali outfit for toddler · baby boy bandhgala · first birthday Indian outfit
- **US-gifting:** baby shower gift Indian · newborn gift Indian · toddler ethnic wear USA
- *Note:* nursery/organic boards ≠ festive wear — route festive kidswear to *Gifting and Occasions* (per The Nesavu/Ankid board-fit decisions).

### jewelry_and_accessories → *Gifting and Occasions* (`…3628`)
- **Primary:** Indian jewelry · temple jewelry · kundan jewelry · oxidized silver earrings
- **Craft:** handmade earrings · meenakari · jadau
- **Occasion:** bridal jewelry Indian · wedding guest jewelry · Diwali jewelry · Raksha Bandhan gift
- **US-gifting:** Indian jewelry USA · gift for her Indian

### food_and_gourmet → *Gifting and Occasions* (`…3628`)
- **Primary:** Indian sweets · mithai · artisanal Indian snacks · masala chai
- **Occasion:** Diwali sweets gift box · festive hamper · Indian gift basket
- **US-gifting:** gourmet Indian food gift · healthy Indian snacks USA

### beauty_and_wellness → *Beauty Ritual* (`…3631`)
- **Primary:** Ayurvedic skincare · natural skincare · herbal hair oil · clean beauty
- **Craft/ingredient:** ubtan · turmeric skincare · cold pressed oil
- **Intent:** self-care ritual · Ayurvedic beauty routine · Indian skincare brands

### fashion → *Artisan Footwear* (`…1541`, footwear) · *Indian Ethnic Wear & Hand-Embroidered Fashion* (`…9116`, apparel)
- **Primary:** Indian ethnic wear · handloom saree · block print dress · embroidered juttis
- **Footwear (Artisan Footwear board):** handmade juttis · embroidered flats · Indian wedding shoes
- **Craft:** Chikankari · Bandhani · Ikat · handloom
- **Occasion:** festive outfit · Diwali outfit ideas · wedding guest outfit Indian
- **US-gifting:** sustainable ethnic wear · Indian fashion USA

### sustainability_and_vegan → keyword LAYER within *Handmade Indian Juttis & Artisan Footwear* (`brand`) and *Indian Ethnic Wear & Hand-Embroidered Fashion* (`apparel`) — NOT a standalone board

**Decision (2026-08-30):** sustainability/vegan-ness is applied as a pin-level keyword layer on the
existing footwear/apparel boards, not a new board. Rationale: only one brand (The Alternate) is
currently positioned this way and it has 3 live pins, well under even the single-brand
`brand_board_threshold` (8); the attribute cuts across footwear + apparel rather than mapping to
one category the way every other live board does; and "attribute board" is a board type the
2026-08-06 panel never evaluated (only category/occasion/gift/brand were judged — see Board
architecture §2). A cross-brand "Sustainable Indian Fashion" board becomes a real candidate once a
brand crosses `brand_board_threshold` **and** a second sustainability-positioned brand has
comparable volume — that is a new board-type addition to the §2 policy table and needs the same
panel-level review the original four types got, not a routing-yaml edit.

⚠️ Unverified volume, same caveat as the rest of §4 — validate against Pinterest autocomplete/Trends
before rotation. Cross-checked against live comparable-brand pin/product copy (Ethical Rani, Ethik
Footwear, Mulmul — India vegan-footwear brands), not guessed from scratch.

- **Primary:** vegan leather shoes · vegan jutti · cruelty free footwear · plant based leather ·
  faux leather shoes India
- **Material fact (verify per listing before use — same discipline as the GOTS caveat in §6):**
  deadstock fabric · natural dye · faux suede · vegan velvet · pineapple leather · cactus leather ·
  cork leather · apple leather — only the ones the specific listing/brand page actually states
- **Craft/heritage crossover (axis 1):** hand embroidered vegan jutti · artisan vegan leather ·
  handcrafted vegan footwear India
- **Occasion (axis 2):** sustainable wedding guest outfit · eco conscious festive wear · vegan
  shoes for Diwali
- **US-gifting/diaspora (axis 3):** vegan Indian shoes USA · sustainable Indian fashion USA ·
  ethical Indian brand USA · cruelty free Indian footwear
- **Certification terms (use ONLY if verified on the listing — do not assume from category):** PETA
  approved vegan · GOTS certified — neither currently verified for The Alternate; "100% vegan
  friendly" is the verified claim in rotation today (confirmed against live listing copy
  2026-08-30)

### art_and_craft → *Artisan Footwear* / brand theme board
- **Primary:** Indian handicrafts · handmade home art · handcrafted decor
- **Craft/AEO:** block printing craft · Madhubani painting · Pattachitra · Warli art
- **Intent:** Indian wall art · handmade gift · artisan-made decor

---

## Seasonal overlay (evergreen boards, seeded ahead)
Per `pinterest_boards.seasonal_boards`. Pin 30–45 days before the moment.

| Board | Live by | Keyword anchors |
|---|---|---|
| Diwali Gifting | mid-August | Diwali gift ideas · Diwali decor · festive gifting |
| New Year, New Home | mid-October | new home decor · housewarming · Indian home refresh |
| Holi Colors | mid-December | Holi outfit · Holi party ideas · colorful decor |
| Mother's Day Edit | mid-February | gift for mom · Indian gift for her · thoughtful gift |

Also worth seasonal boards: **Raksha Bandhan** (gift for brother/sister, ~June), **Wedding Guest** (year-round, peaks fall).

---

## Board copy (paste-ready)

Rename + description for each **live** board. Renaming changes the board's URL slug — do it
now while boards are new and low-traffic. In Pinterest: **Edit board → Name / Description**.
Pinterest board descriptions cap at 500 chars; these run ~250–350.

| Board id | Current name | → Rename to | Description (paste) |
|---|---|---|---|
| …3626 | Home and Kitchen | **Indian Home Decor & Artisan Kitchen** | Hand-painted Indian ceramics, bone china mugs, and artisan tableware for a festive table. Discover handmade home decor and kitchen pieces — Pattachitra and Phad-inspired dinnerware, housewarming gifts, and Diwali tablescapes from independent Indian brands on Mela. |
| …3628 | Gifting and Occasions | **Indian Gift Ideas & Festive Occasions** | Indian gift ideas for every occasion — Diwali gifting, housewarming, baby showers, Raksha Bandhan, and wedding season. Handmade jewelry, festive kidswear, gourmet hampers, and artisan home pieces from independent Indian brands, shipped to the US. |
| …3629 | Modern Indian Nursery | *(keep — already keyworded)* | Modern Indian nursery decor and baby essentials — organic cotton clothing, hand block print outfits, and thoughtfully made pieces for newborns and toddlers. Nursery inspiration and baby gifts from independent Indian brands on Mela. |
| …3630 | Organic Baby Essentials | **Organic Indian Baby Clothes & Essentials** | Organic cotton Indian baby clothes and essentials — soft, breathable, hand block printed and hand embroidered outfits for newborns and toddlers. Ethical baby gifts and everyday wear from independent Indian brands. |
| …3631 | Beauty Ritual | **Ayurvedic Skincare & Natural Beauty** | Ayurvedic skincare and natural beauty from independent Indian brands — herbal hair oils, ubtan, turmeric and cold-pressed formulations. Clean beauty rituals rooted in Indian tradition, discovered on Mela. |
| …1541 | Artisan Footwear | **Handmade Indian Juttis & Artisan Footwear** | Handmade Indian juttis and artisan footwear — embroidered flats, wedding shoes, and festive footwear crafted by Indian artisans. Ethnic wear footwear and gifting from independent Indian brands on Mela. |

**Brand boards** *Fizzy Goblet* and *The Alternate* were **archived 2026-08-06** (consolidated into theme boards) — do not route pins to them. Brand boards are deferred until post-traction (see §2).

**Fallback board** *Brands from India* — `Independent Indian brands — handmade fashion, jewelry, home decor, and gifts from across India, curated and shipped to the US. Discover on Mela.`

**Still to create manually** (seasonal, per `pinterest_boards.seasonal_boards`): Diwali Gifting (live by mid-Aug — **overdue soon**), New Year New Home (mid-Oct), Holi Colors (mid-Dec), Mother's Day Edit (mid-Feb).

---

## 6 · Pipeline-generated pin copy (search-metadata reuse)

**The ingestion pipeline now writes pin-ready copy for every listing — stop authoring pins from scratch.** The classifier's enrichment pass (`Mela-scrapper-integrations/.../prompt_engine.py`) already generates, per product, exactly the fields Pinterest ranks on (this is the same work powering on-site search — see `search-ranking-relevance-prd.md` §4B/§4D). Because Pinterest *is* a search engine, its copy and the site's keyword index draw from one source of truth:

| Pipeline field | → Pin slot | Note |
|---|---|---|
| `seo_title` | **Pin title** | Front-loaded keyword title, already written for search. Trim to readable length. |
| `meta_description` | **Pin description** | 2–4 sentence keyword-rich description; first ~50 chars carry intent. Append "Discover on Mela." |
| `searchKeywords` / `search_synonyms` | **Keyword bank + alt text** | The **diaspora vocabulary map** — real US↔Indian/regional terms (kurta↔tunic, jhula↔swing). Per-listing keyword fuel that *complements* the §4 seed bank. |
| `isBestseller` / `melaScore` tier | **Which products to pin first** | Seed each board from top-`melaScore` + bestseller listings — curation ranking picks the pins, not recency. |

**Two things this changes:**
1. **The §4 "can't verify volumes" caveat is partially closed** — you now have *real per-listing language* pulled from actual products, not guessed seeds. Still validate high-stakes board/title terms against Pinterest Trends (§4), but the per-pin description/alt can come straight from the pipeline.
2. **Zero-result query logs (search-ranking PRD §7) are a Pinterest content-gap finder** — searches that returned nothing on-site are terms shoppers want; make pins for them. This is the same demand loop Reddit feeds (`reddit-strategy.md`).

**Guardrail:** the synonym field is generated by an LLM — keep the `verify: true` craft/cert discipline (`education-topics.yaml`). Don't paste a synonym like "GOTS certified" into a pin unless the listing actually carries it.

---

## Example: a fully keyworded pin (Kaunteya Airavata mug)
- **Board:** Home and Kitchen → *(keyworded description: "Hand-painted Indian ceramics, bone china mugs, and artisan tableware for a festive table.")*
- **Title:** `Hand-Painted Pattachitra Coffee Mug | Indian Bone China`
- **Description:** `Fine bone china mug hand-painted with Pattachitra motifs by Indian artisans. A meaningful piece for a Diwali chai spread or a housewarming gift. Discover on Mela.`
- **Alt:** `Hand-painted white bone china coffee mug with Pattachitra Garuda motif on a warm neutral surface`
