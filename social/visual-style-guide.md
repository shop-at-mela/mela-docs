# Mela Social Visual Style Guide

**Last updated:** August 11, 2026  
**Inspired by:** Amala Earth aesthetic (@amala.earth, Pinterest: @amalaearth)

---

## Brand Visual Identity

Mela is a **discovery platform for Indian artisan brands**. Our social visuals should reflect:
- **Authenticity** — Handcrafted heritage, not mass production
- **Sustainability** — Natural materials, artisan values, eco-conscious framing
- **Calm sophistication** — Minimal, intentional, editorial approach
- **Cultural pride** — Celebrate Indian craftsmanship without exoticizing

---

## Core Aesthetic Principles

### Color Palette
- **Primary:** Earthy tones (warm greens, browns, ochre, rust, warm grays)
- **Neutrals:** Muted creams, warm whites, soft taupes
- **Accent:** Occasional pops of jewel tones (emerald, sapphire) for emphasis
- **Avoid:** Bright neons, corporate blues, harsh contrasts

**Mela Brand Colors (use sparingly in overlays):**
- Navy: #2D2D7B (logo, minimal text)
- Marigold: #F0A030 (accent only, not dominant)

### Photography Style
- **Lighting:** Soft, natural light (golden hour, diffused indoor)
- **Mood:** Calm, grounded, organic
- **Depth:** Focus on textures, details, handcrafted qualities
- **Composition:** Intentional negative space, editorial framing (not catalog style)

### Backgrounds & Settings
Products should be **styled in natural scenes**, not isolated on white:
- **Marble, stone, or wood surfaces** — emphasizes craft and permanence
- **Draped natural fabrics** — linen, cotton, silk in neutral tones
- **Botanical elements** — dried flowers, greenery (subtle, not overwhelming)
- **Warm accessories** — candles, ceramics, woven items to build context
- **Textured surfaces** — terracotta, brass, natural materials

**Example scenes:**
- Footwear on warm marble with soft shadow and gold fabric drape
- Jewelry on linen with dried flowers and botanical elements
- Textiles folded on wooden surface with warm lighting from side
- Home goods styled with complementary natural materials

### Text Treatment
- **NO product titles in post visuals** — let imagery speak
- **NO prices in carousel/feed posts** — prices on destination page only
- **Typography:** Clean, minimal, serif or elegant sans-serif (not bold/heavy)

### Affiliate & Watermark
**All post visuals must include a watermark:**
- **Watermark text:** "Discovered on [Mela Logo]"
- **Placement:** Bottom-right corner only
- **Size:** 10–15% of image width (small, unobtrusive)
- **Style:** Semi-transparent, does NOT overshadow product
- **Color:** Navy #2D2D7B (Mela brand) or white (for contrast if needed)
- **Purpose:** Signals discovery platform (Mela is the curator, not the manufacturer) without cluttering the aesthetic

**Caption framing:**
- Frame product as "by [Brand], discovered on Mela" — NOT "from Mela"
- Never imply Mela manufactured or exclusively sells the product
- Use discovery language: "hard to find" not "unavailable"

---

## Visual Content Types

### Product Closeups (Detail Focus)
- Macro photography of embroidery, weaving, or craftsmanship
- Highlight handmade qualities (stitching, patina, irregularities = authenticity)
- Soft, directional lighting to show texture
- Neutral background (dark fabric, stone) to isolate details

### Lifestyle/Styled Scenes
- Product in use or in a curated, editorial scene
- Show context: how it fits into daily life or celebration
- Natural props (other artisan items, plants, ceramics)
- Warm, inviting mood that feels achievable (not overly styled/aspirational)

### Flat Lay with Intention
- Arrange products + complementary items on natural surface
- Include cultural/craft context (tools, materials, inspiration)
- Plenty of breathing room (negative space)
- Overhead angle with soft side lighting

### Video/Slideshow (Product Scene Placement)
- Use Blotato's "Product Scene Placement" template
- Each product in a unique, lifestyle-appropriate scene
- Transitions should be smooth, minimal (fade preferred)
- No auto-text overlays; let visuals tell the story
- 4-7 slides max to maintain engagement

### Blotato Templates & Specs
| Use case | Template | Aspect Ratio | Notes |
|---|---|---|---|
| Single product + real photo | Image Slideshow (5903b592-1255-43b4-b9ac-f8ed7cbf6a5f/v1) | Instagram 1:1, Pinterest 2:3 (1000x1500) | Pass actual product image URL; request Pinterest output at 1000x1500 explicitly — don't reuse the Instagram 1:1/4:5 render, it ships smaller/less prominent in-feed than Pinterest's own recommended ratio |
| Product in lifestyle scene | Product Scene Placement (f524614b-ba01-448c-967a-ce518c52a700) | Platform-dependent | 4–7 slides; smooth transitions |
| Multi-product carousel | Image Slideshow | 1:1 (Instagram) | Multiple images, consistent styling |

**When creating prompts:** Use outcome language ("do not overshadow the product"). Include [Mela watermark spec](#affiliate--watermark) in every prompt.

**Product Scene Placement is for PRODUCT posts only.** Do NOT route `trust_service` or `cultural_education` posts through it — that is what makes education posts look identical to product ads. Education posts use the Education Visual System below.

---

## Education Visual System

Education posts (`trust_service` and `cultural_education`, from `education-topics.yaml`) are a **separate visual language from product posts**. Product posts chase *desire* (soft, warm, product-forward, branding hidden). Education posts chase *saves and shares* (they teach, reassure, or explain). If an education post looks like a product still on linen, it reads as an ad and gets scrolled past — and it wastes the format that actually earns reach for a cold account.

### The one rule that governs every education post

> **Slide 1 is a hook, never a product.** The product, if it appears at all, is the *payoff* — the last slide, framed as "made this way, by [brand], on Mela." For logistics/trust posts there is usually no product at all.

A product macro on slide 1 signals "sponsored, scroll." A question or a process image signals "wait, what?" and earns the swipe/save.

### Two sub-systems

| | **Cultural education** (living culture) | **Trust / service** (modern logistics) |
|---|---|---|
| Feeling | Documentary, editorial | Utility, reassurance |
| Topics | craft, technique, origin, design | shipping, customs, sizing, returns, payment, vetting |
| Slide 1 | Process/material/place image **or** a big-type question | Branded title card: e.g. "Shipping from India, explained" |
| Middle slides | Teaching cards (how it's made) + illustrative process imagery | Timeline / chart / myth-vs-fact / conversion table |
| Payoff slide | *One* product shot: "made this way, by [brand] on Mela" (optional) | No product — CTA card only |
| Branding | Subtle (documentary restraint), watermark only | **Navy #2D2D7B + marigold #F0A030 worn openly** — this is a Mela utility, not a product |
| Product photo | Last slide only, optional | Never |

### Slide-1 options that are NOT a product

1. **Typographic hook card** — Mela design system, one bold line: *"No two are ever identical. Here's why."* Cheapest to produce, highest save-rate. Built via the [HTML card system](#producing-education-visuals-canva-free), not Blotato.
2. **Process / material still** — the *tool or raw material*, not the finished good: a carved wooden block, an indigo vat, a loom, dye-stained hands. Blotato-generated as an **illustrative editorial image** (see license below).
3. **Place / map** — an illustrated map ("Where India's crafts come from"). Distinctive, ownable, reusable across many posts.

### Illustrative-imagery license (resolves the "don't fabricate" paralysis)

The "do not AI-generate props / do not fabricate the product" rule in the runbooks applies to **product posts** — never invent a product's features. **Cultural-education posts run under editorial/illustration license:** a representative image of a carved printing block, an indigo dye vat, or a loom is legitimate teaching imagery, the same way a magazine uses a stock diagram.

Hard boundary: illustrative imagery **must never be captioned or implied to be a specific brand's own workshop, a specific artisan, or a specific product's making.** It illustrates the *technique*, generically. When in doubt, the caption says "block printing works like this," never "here is Ankid's printing table."

### Living culture, not heritage (framing rule)

Frame craft as **alive and being made now**, not as a museum relic. Mela sells contemporary brands *reinterpreting* craft (Nicobar, Kaunteya, Isharya), so the story is *why this is still made by hand in 2026 and who makes a living from it* — not "an ancient 500-year-old tradition." This matches the catalog, earns AEO value, and avoids the exoticizing/othering trap flagged in [What NOT to Do](#what-not-to-do). Every `cultural_education` topic carries a `contemporary_angle` in `education-topics.yaml`; lead with it. (Same reframe governs website brand/category copy — see `shopify_brands.py` brand-voice house rule.)

### Producing education visuals (Canva-free)

Cost order (the Tool decision procedure below applies it per-asset): **HTML/CSS → PNG** primary (free; hook/teaching cards, timelines, myth-vs-fact, sizing tables, maps — from the Mela templates, rendered at the target ratio via `claude-in-chrome`/headless Chrome) → **Blotato** for photographic stills HTML can't make → **SVG → PNG** for pure-vector infographics → **Canva** last (uncodeable one-offs only).

> Templates: `mela-docs/social/templates/` (built + rendering; see its README). `hook-card.html`, `shipping-timeline.html`, `myth-vs-fact.html`, shared tokens in `mela-kit.css`. Render: `./render.sh <file.html> <out.png> [square|story|pin]`. Copy a template, edit inside `<!-- EDIT -->` markers, render, post.

### Tool decision procedure (run this, don't re-reason it)

Three gates in order. Rendered imagery forces Blotato; anything graphic goes to code; Canva is only the uncodeable one-off.

- **Gate 0 — motion?** Reel/video (e.g. a row-anchor teaser) → **Blotato motion collage**; audio + publish are a manual in-IG step (`category-routing.yaml` → `grid.reel_production_note`). Else it's static frames.
- **Gate 1 — needs rendered imagery** (photographic or illustrative) that type+shapes can't make? Actual product → **real product photo** (never AI-generate a product). Craft material/process/place → **Blotato** (illustrative license: generic technique, never a specific brand's workshop). No such layer → Gate 2.
- **Gate 2 — graphic/text layer.** Pure vector (map, diagram) → **SVG**. Text flow / tables / mixed → **HTML**. Needs freeform composition or stock art → **Canva**. (Judgment call: describable as boxes/lines/text/chart/table/photo = codeable; "an illustration of…" = Canva.)

**Non-negotiable guardrails:**
- **Exact/factual text NEVER goes inside a Blotato layer** (diffusion garbles it). Blotato makes the picture; HTML/SVG composites the words on top — "photo + headline" is always a hybrid.
- **Watermark via the HTML/SVG layer**, not a Blotato prompt (Blotato watermark text is an unsolved gap).
- **Multi-aspect-ratio → prefer HTML/SVG** (one responsive file re-renders IG 1:1 + Story 9:16 + Pinterest 2:3 for free).
- **Real charts → load the `dataviz` skill first** (a simple timeline/table is fine in plain HTML).

**Cheat sheet:**

| Asset | Gate | Tool |
|---|---|---|
| Hook card (type on color) | 2 | HTML |
| Shipping timeline / customs explainer | 2 | HTML |
| Myth-vs-fact card | 2 | HTML |
| India↔US sizing table | 2 | HTML |
| "Where crafts come from" map / process diagram | 2 (pure vector) | SVG |
| Carved block / indigo dye / loom still | 1 (imagery) | Blotato |
| Dyer's hands at work | 1 (imagery) | Blotato |
| Product payoff slide | 1 (actual product) | real product photo |
| Photo with a headline / factual text over it | 1 + 2 | Blotato photo + HTML text composited |
| Row-anchor teaser | 0 (motion) | Blotato collage + manual audio/publish |
| Freeform collage needing stock art | 2 = no | Canva |

---

## Diaspora Anchoring (Audience Principle)

> Added Aug 2026, after a persona-panel review found the batch was correctly *Indian-anchored* but not *diaspora-anchored*. Sibling to the **"Indian" Anchoring Principle** in `@mela-docs/UXR/buyer-personas.md` — read both together.

Our posts already get **Indian Anchoring** right: cultural origin lives at the *product* layer ("hand embroidered in Lucknow," "made in Tamil Nadu"), never labeling the *user* by ethnicity. Keep doing that. The gap this section closes is different: a caption can be flawlessly Indian-anchored and still read as **generic** — it could run verbatim on the brand's own India Instagram, with a "Ships to the US" line bolted on as the only US signal. That post is not written *for the US shopper*; it is written *about the product* with US shipping as a footnote.

### The rule

> **Anchor the US shopper's *situation*, never their *identity*.**

There are three layers, and the same discipline as the Indian-Anchoring table applies — the third one is the trap:

| Layer | Example | Effect |
|---|---|---|
| **Product origin** (Indian Anchoring) | "Hand embroidered in Lucknow" | ✅ Always. Trust + provenance. |
| **Shopper situation** (Diaspora Anchoring) | "The good Diwali china never survives the suitcase from India." | ✅ This is the missing layer. Makes the US shopper feel *seen* without naming their ethnicity. |
| **Shopper identity** | "For Indian families in the US" / "your Indian finds" | ❌ Never. Reduces the user to their ethnicity — harms all four personas (see buyer-personas.md). |

The situation layer draws on the *lived reality* of buying Indian goods in the US — none of which requires labeling anyone:
- **The suitcase economy** — relying on family visits to bring things over, planning two months ahead.
- **Discovery difficulty** — the local Indian store is 40 minutes away, understocked, or sells machine-made lookalikes. (This is Mela's whole "hard to find" wedge — foreground it.)
- **Occasion-in-America** — hosting Diwali / a first birthday / Navratri far from where the goods are made.
- **Restocking friction** — the thing you love isn't on the US shelf and doesn't ship easily on its own.

### Before / after (situation, not identity)

| Generic (current) | Diaspora-anchored |
|---|---|
| "Set your festive table with a story this Diwali." | "The good Diwali china never survives the suitcase from India. Kaunteya's is hand painted in Jaipur and ships straight to your door." |
| "Two ingredients. One press. Baby Forest makes cold pressed baby oils." | "You used to wait for your mom's next visit to restock the good baby oil. Baby Forest ships it from India in about two weeks." |
| "Real chikankari or a printed lookalike?" | "Your local Indian store's chikankari is usually machine printed. Here is how to spot the real hand embroidered piece before you buy." |

Note what did **not** change: origin stays at the product layer, and no caption names the reader's ethnicity. Only the *opening hook* moved from product-fact to shopper-situation.

### Where the anchor must live (most people never read the caption body)

Reality check: on Instagram the caption truncates at ~125 chars and most people never tap "more"; on Reels the audio + on-screen text carry the message; on Pinterest humans scan the image + title while the description is mostly SEO the algorithm reads. **A situation hook buried in caption paragraph two reaches almost no one.** So Diaspora Anchoring is a *visual-first* principle — carry it in the layers people actually consume, in priority order:

1. **The visual / scene (primary — ~90% of the impression).** Stage the **US context**: a Diwali table in an American home, the product in a modern US kitchen or nursery. The Mela baseline (earthy, warm) is correct but reads as "could be Jaipur"; one subtle US-context cue anchors the audience before a word is read. Product-photo posts can't carry text overlays, so for those **the scene *is* the anchor.**
2. **The hook frame / on-image text** (reels + education/hook cards — these are allowed text; product photos are not). Reels: first 3 seconds + on-screen line + audio choice. Hook cards: slide 1. Put the situation line here.
3. **The first caption line (~125 chars, pre-truncation).** The one caption element everyone sees. Lead with the situation hook, never bury it in paragraph two. The before/after rewrites above are *this line*.
4. **Caption body + Pinterest description + alt text (reinforcement + SEO).** Read by the high-intent minority who expand and save (also the likeliest to click through) and by the search algorithm. Still anchor here — just not the primary carrier.

Steps 1–2 are what reach the ~80% who never read the caption; step 3 is the sliver of caption everyone sees. Don't let the anchor live only in step 4.

### Per-persona quick reference (situation hooks that land)

| Persona | Situation that resonates | Do NOT |
|---|---|---|
| **Neha** (first-gen) | Suitcase economy, restocking, fair price vs. what she'd pay in India | Debut only brands she's never heard of; skip all price/value framing |
| **Priya** (mixed heritage) | Hosting the occasion in the US, will it fit a US-sized kid, dignified not costume-y | Assume she knows the brand; omit US sizing |
| **Arun** (second-gen) | "Never had this growing up," craft explained as a safe entry point | Gatekeep or assume cultural knowledge |
| **Sarah** (conscious American parent) | Genuine sustainability she can't find on Etsy, **certifications** | Lead with Indian heritage — it's her anti-signal; she isn't shopping her identity |

**Coverage watch-out (from the Aug 2026 panel):** the batch over-indexed on craft-heritage hooks (Arun's lane) and under-served Sarah (certifications-first) and Neha (familiar brands + price). Vary the situation hook across a batch so all four personas get served, not just the heritage reclaimer.

---

## Platform-Specific Guidelines

### Caption Style (All Platforms)

Applies to every caption, pin description, and Story text:
- **No dashes.** Never use a hyphen, en dash, or em dash (-, –, —) to join clauses in caption text. Write two short sentences instead.
- **Short sentences.** One idea per sentence. Split anything that strings clauses together with commas into separate sentences.
- Hyphenated compound words should read as two words where the meaning still holds (e.g. "handwoven," "GOTS certified," "artisan made"). Keep a hyphen only where it's a fact that can't change, like a brand's own spelling.

### Instagram Feed (Carousel Posts)
- **Aspect ratio:** 1:1 (square) for the post itself; **note the profile grid crops to 3:4 portrait** — keep key content centered (see Instagram Grid Row Anchors)
- **Format:** 4–7 slides per carousel
- **Text:** Minimal on images, save context for caption
- **Style:** Vary between product detail + styled scene shots
- **Cadence:** 9 feed posts/week (= three theme-rows: 2 brand-themed + 1 education); overflow → Stories. Feed posts stay a multiple of 3 to keep row alignment.

**Caption approach:**
- **Lead is persona-led** — the selected persona sets the opening (Sarah → certification, Priya → occasion, Arun → craft origin, Neha → regional specificity). Persona is chosen per post in `/social-review` Phase 2; see the caption table in `social-content-strategy-prd.md` for the leads + guardrails (not restated here).
- **Anchor the shopper's situation, not just the product** — before finalizing the hook, check it against [Diaspora Anchoring](#diaspora-anchoring-audience-principle). A caption that could run verbatim on the brand's own India feed (product-fact hook + "Ships to the US" footnote) is under-anchored; open on the US shopper's situation instead.
- Then: brief occasion/use → craft detail → CTA "Discover [Brand] on Mela →"
- **Include product list** — "Featured in this carousel: [product 1, product 2, ...]" (aids discoverability on destination page)
- NO price in caption; NO text overlays on images

### Instagram Grid Row Anchors (Theme Cards & Teaser Reels)

Row mechanics (row = 3 tiles, weekly batch = 3 rows, composition, planning, ordering) are canonical in `category-routing.yaml` → `grid`; this section covers the anchor's **visual** design. The anchor is the center tile of a brand row.

- **3:4 grid crop (critical):** the IG profile grid crops feed posts to **3:4 portrait**. Design at native ratio but keep the theme title/wordmark/logo inside the centered 3:4 safe zone — text near the top/bottom edge clips. This is what most often breaks an anchor.
- **Teaser reel (default):** motion photo-collage — cut-out craft elements (jewelry, textiles, brass, motifs) drift over a textured ground, then converge into the brand/theme wordmark. Trending Sufi/folk audio; one-line curiosity caption; show no product directly. Semi-automated (audio + publish are manual in IG).
- **Theme card (fallback):** static graphic in the Mela brand kit (navy #2D2D7B + marigold #F0A030), theme name as the legible focal element.
- **Converge-line gating:** "coming soon" ONLY for a not-yet-live brand; live brands read "Now on Mela / Discover on Mela."
- **Watermark:** anchors carry the "Discovered on [Mela Logo]" watermark, subordinate to the wordmark.

### Instagram Stories
- Quick product feature: "[Product] · Handcrafted in [region]"
- Behind-the-scenes: artisan at work, detail shots
- Curation moments: "This week's discoveries"
- Minimal text (sticker-based, not overlaid)
- **Grid-neutral:** Stories never appear in the profile grid — they absorb any feed overflow beyond the 3-per-row cadence without scrambling row alignment.

### Pinterest Pins (Individual & Series)
- **Aspect ratio:** 2:3 (1000x1500px) — Pinterest's own recommended ratio; don't fall back to 1:1 or reuse an Instagram 4:5 render (verified against Pinterest's current pin-spec guidance — pins under 2:3 render smaller in-feed, though they won't get cropped the way over-tall pins do)
- **Style:** Lifestyle scene with product prominent
- **Text on pin (title):** Keyword-led, not a bare SKU name. ✓ "Gold Wedding Wedges | Handcrafted in India" ✗ "24K Magic Criss Cross Wedge" — the product's own name can appear, but lead with what someone would actually search
- **Description:** Keyword-rich, 2–3 sentences, no price
- **Board naming:** craft/occasion-descriptive, never a bare brand slug as the sole board (e.g. `artisan-footwear`, `Heritage Gifting` — not `fizzy-goblet`). A brand-specific board can exist *in addition*, never instead of a discoverable one. Full policy: `category-routing.yaml` → `pinterest_boards`
- **Cadence + cap:** canonical in `category-routing.yaml` → `cadence` (posts via Blotato, cap 10/24h per account)
- **Link strategy:** specific product URL, not brand page — `https://www.shopatmela.com/l/{Dev_Listing_ID}` (from classified CSV) + UTM per `category-routing.yaml` → `tracking`

**Pin description template:**
> [Brand Name] Handcrafted [Product Type] | [Craft Technique] [Regional Origin] | Sustainable artisan goods from India, shipped to the US.

**Pin link format:**
`https://www.shopatmela.com/l/{Dev_Listing_ID}` — direct link to product listing for maximum conversion

---

## What NOT to Do

❌ White/sterile product backgrounds  
❌ Product title + price overlays on images  
❌ Harsh, flat, fluorescent lighting  
❌ Generic catalog-style photography  
❌ Heavy branding/logos overshadowing product  
❌ Exoticizing or "othering" Indian culture  
❌ Corporate stock photo aesthetic  
❌ Overly stylized/unattainable lifestyle scenes  
❌ Bright neons or harsh color contrasts  

**For education posts specifically:**  
❌ A product hero shot on slide 1 (it reads as an ad — see [Education Visual System](#education-visual-system))  
❌ Routing `trust_service` / `cultural_education` through Product Scene Placement  
❌ "Ancient / 500-year-old heritage" framing that treats living craft as a museum relic  
❌ Captioning generic illustrative process imagery as a specific brand's own workshop/artisan  

---

## Blotato Prompt Template

When creating visuals with Blotato:

1. **Reference this guide's baseline**: Earthy tones, soft lighting, calm artisanal mood (inspired by @amala.earth)
2. **Apply category-specific styling** from [Category-Specific Styling](#category-specific-styling-within-mela-baseline) section
3. **Include Mela watermark** per [Affiliate & Watermark](#affiliate--watermark) rules
4. **Use outcome language**: "do not overshadow the product", "emphasize handcrafted qualities"
5. **NO product names, NO prices, NO text overlays** — let visuals tell the story

Example structure:
```
Create lifestyle scenes for [BRAND] [PRODUCT TYPE]:
Scene 1: [Product Name] on [surface] with [complementary items], [lighting]
Scene 2: [Product Name] styled with [natural materials], [mood]

MELA BASELINE: Earthy, soft lighting, artisanal mood (see visual-style-guide.md)
CATEGORY ACCENT: [Fashion: embroidery detail] [Jewelry: metalwork macro] [Home: glaze texture] (see visual-style-guide.md)
WATERMARK: "Discovered on [Mela Logo]" bottom-right, semi-transparent, navy #2D2D7B
```

---

## Checklist for Every Post

Before publishing, verify:
- [ ] **Lighting:** Soft, natural, or warm golden hour
- [ ] **Background:** Styled scene (not white/empty)
- [ ] **Product visibility:** Clear, prominent, celebrated
- [ ] **Text:** Minimal (caption only; no titles/prices on image)
- [ ] **Authenticity:** Handcrafted qualities visible (stitching, texture, patina)
- [ ] **Emotional tone:** Calm, grounded, aspirational (not exclusive)
- [ ] **Platform fit:** Aspect ratio correct, caption tailored
- [ ] **Destination page:** Aligns with post promise (brand story, craft context visible)

---

## Category-Specific Styling (Within Mela Baseline)

**Mela Visual Baseline (non-negotiable for all categories):**
- Natural backgrounds (marble, wood, linen, stone)
- Soft, golden hour lighting
- Artisanal, calm mood (Amala Earth-inspired)
- "Discovered on Mela" watermark (bottom-right)
- Clean, minimal text overlays
- Earthy color palette as primary

**Category-specific flexibility** (accents within baseline):

### Fashion (Clothing, Footwear, Accessories)
- **Styling:** Product on/near body or styled with complementary items (belts, jewelry, scarves)
- **Color focus:** Celebrate fabric colors; jewel tones + earthy tones OK
- **Detail:** Show weave, embroidery, stitching up close
- **Drape/movement:** Capture fabric flow, texture, handmade quality
- **Example:** Fizzy Goblet footwear on marble + draped gold silk, emphasizing embroidery detail

### Home & Kitchen
- **Styling:** Product in functional or lifestyle context (on table, shelf, in use)
- **Color focus:** Warm neutrals + accent colors of the piece
- **Detail:** Show craftsmanship (wood grain, ceramic glaze, weaving)
- **Negative space:** Plenty of breathing room around product
- **Example:** Ceramic bowl on wooden table with dried flowers, showing glaze detail

### Jewelry & Accessories
- **Styling:** Macro closeups + lifestyle flat lay
- **Color focus:** Metallic tones + gemstones; juxtapose with neutral surfaces
- **Detail:** Highlight metalwork, stone setting, hand-finishing
- **Scale:** Show product actual size; use objects for scale reference
- **Example:** Gold necklace on linen with botanical elements, macro shot of pendant detail

### Beauty & Wellness
- **Styling:** Product with natural ingredients/complementary items (flowers, herbs, water)
- **Color focus:** Warm taupes, cream, green; highlight product color
- **Detail:** Show texture (cream, oil, powder), ingredient natural state
- **Wellness mood:** Calm, spa-like, restorative atmosphere
- **Example:** Skincare jar surrounded by fresh herbs and soft, diffused light

### Art & Craft
- **Styling:** Product displayed as art; in creative context or on neutral surface
- **Color focus:** Celebrate artwork colors + earthy frame
- **Detail:** Texture, brushstrokes, handmade imperfections visible
- **Lighting:** Directional light to enhance dimension/depth
- **Example:** Painted textile on wood, showing brushwork detail with warm side light

### Baby & Kids
- **Styling:** Product in playful, safe context; with relevant props (blocks, plants, fabric)
- **Color focus:** Soft pastels + warm neutrals; primary colors OK if brand uses them
- **Detail:** Safety, comfort, craft quality visible
- **Mood:** Joyful, nurturing, developmental
- **Example:** Wooden toy on soft linen with nature elements, bright natural light

### Food & Gourmet
- **Styling:** Product in serving context; with complementary foods/ingredients/utensils
- **Color focus:** Food colors + warm neutrals; show natural appeal
- **Detail:** Texture (jam gloss, spice granules), freshness, ingredient quality
- **Lighting:** Warm, appetizing light; food photography best practices
- **Example:** Jar of spice or sauce on wooden surface with relevant ingredients, backlit

---

## Resources

- **Brand inspiration:** @amala.earth (Instagram), @amalaearth (Pinterest)
- **Mela brand colors:** Navy #2D2D7B, Marigold #F0A030
- **Blotato templates:** Product Scene Placement, Image Slideshow
- **UXR personas:** See `@mela-docs/UXR/buyer-personas.md`
- **Product CSVs:** `@mela-docs/scrapper_csvs/[category]/classified_products_prod/`
- **Categories:** fashion, home_and_kitchen, jewelry_and_accessories, beauty_and_wellness, art_and_craft, baby_and_kids, food_and_gourmet
