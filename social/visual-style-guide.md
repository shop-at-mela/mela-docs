# Mela Social Visual Style Guide

**Last updated:** June 28, 2026  
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
- Then: brief occasion/use → craft detail → CTA "Discover [Brand] on Mela →"
- **Include product list** — "Featured in this carousel: [product 1, product 2, ...]" (aids discoverability on destination page)
- NO price in caption; NO text overlays on images

### Instagram Grid Row Anchors (Theme Cards & Teaser Reels)

The Instagram **feed** is laid out as **theme-rows of 3**. A weekly `/social-launch` batch = **3 rows (9 tiles): 2 brand-themed rows + 1 education row.** Each row shares one brand or one education theme, with a navigation **anchor** in the **center** tile. Across weeks the center column forms a vertical "spine" of anchors that lets profile visitors (esp. Arun, Priya) navigate. Row planning lives in `/social-launch`; routing config in `category-routing.yaml` → `grid`.

- **Brand-themed row composition:** a brand row is `[craft-story / founder / artisan tile] · [center ANCHOR] · [product tile]` — story + product, **not** a product catalog (inspiration-first). Only the product tile cross-posts to Pinterest.
- **3:4 grid crop (critical):** The IG profile grid crops feed posts to **3:4 portrait**. Design the anchor at the post's native ratio but keep the **theme title / wordmark / logo inside the centered 3:4 safe zone** — anything near the top/bottom edge clips on the grid. This is the one spec that most often breaks an anchor.
- **Anchor forms (reels-first):**
  - **Teaser reel** (DEFAULT — reels carry the reach): motion photo-collage — cut-out craft elements (jewelry, textiles, dried flowers, brass vessels, motifs tied to the theme) drift and layer over a textured ground, then **converge into the brand/theme wordmark**. Trending Sufi/folk audio; one-line curiosity caption that builds intrigue, doesn't explain. **Show no product directly.** Semi-automated: Blotato can build the collage, but **audio + final publish are a manual step natively in Instagram** (Blotato templates are silent). ~2 anchor reels/week.
  - **Theme card** (FALLBACK — when a reel can't be produced that week): static Canva graphic — Mela brand kit (navy #2D2D7B + marigold #F0A030), the brand/category/theme name as the legible focal element, earthy baseline. Cheap to produce.
- **Converge-line gating:** the wordmark reveal may read **"coming soon"** ONLY for a brand genuinely not-yet-live on Mela. For a live brand it must read **"Now on Mela" / "Discover on Mela"** — never imply unavailability.
- **Side tiles:** the flanking posts (craft/founder story on one side, product on the other) follow the normal category styling below, tuned to sit tonally with the anchor.
- **Watermark:** anchors still carry the "Discovered on [Mela Logo]" watermark, but subordinate to the theme wordmark.

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
- **Board naming:** craft/occasion-descriptive, never a bare brand slug as the sole board (e.g. `artisan-footwear`, `Heritage Gifting` — not `fizzy-goblet`). A brand-specific board can exist *in addition*, never instead of a discoverable one — nobody searches Pinterest for a brand slug they've never heard of
- **Strategy:** manual warmup can run 3–5 pins/day, not capped at 1/day — Pinterest volume isn't gated by the same "warmup" concept as Instagram's algorithm; cadence is canonical in `category-routing.yaml` → `cadence`
- **Link strategy:** Use specific product URLs, not brand page — `https://www.shopatmela.com/l/{Dev_Listing_ID}` (extract from classified CSV) — with UTM params per `category-routing.yaml` → `tracking`

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
