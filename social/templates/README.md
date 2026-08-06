# Mela Social — HTML Card Templates

The **primary, zero-cost** way to produce education/utility post images (see
`../visual-style-guide.md` → Education Visual System → *Tool decision procedure*).
Canva MCP is the last resort; these cover ~90% of what it was used for.

**Why HTML:** a post image is just a fixed-size rectangle of pixels. HTML/CSS lays
out text/shapes/charts, and headless Chrome screenshots it into a PNG at the exact
post dimensions. The Mela brand kit is encoded once in `mela-kit.css` — every card
inherits it, so swap the text and re-render.

## The cards

| File | Use | Content type |
|---|---|---|
| `hook-card.html` | Slide 1 curiosity hook (never a product) | `cultural_education` |
| `shipping-timeline.html` | Shipping/customs explainer | `trust_service` |
| `myth-vs-fact.html` | Bust a purchase objection | `trust_service` |

`mela-kit.css` = shared brand tokens (navy `#2D2D7B`, marigold `#F0A030`, cream,
serif display, watermark). Edit palette/type there once.

## Workflow

1. Copy a template to a working file (keep templates pristine):
   `cp hook-card.html /tmp/ankid-hook.html`
2. Edit the text inside the `<!-- EDIT -->` markers. For a navy/marigold pop, wrap
   one word/phrase in `<span class="accent">…</span>`.
3. Render:
   ```
   ./render.sh /tmp/ankid-hook.html /tmp/ankid-hook.png square
   ```
   Ratios: `square` (1080×1080, IG feed, default) · `story` (1080×1920) · `pin` (1000×1500).
   The **same file renders at all three** — that's the multi-aspect-ratio win.
   Retina-crisp: prefix `MELA_SCALE=2`.
4. Post the PNG: hand it to Blotato (`blotato_create_post`, in `mediaUrls`) exactly
   like a product image, or drop it straight into Instagram.

> Keep rendered PNGs OUT of this folder — templates are source. Output per-post
> (e.g. into the campaign's `log/<brand>/` dir or a temp path).

## Guardrails (from the visual-style-guide decision procedure)

- **Slide 1 is a hook, never a product.** These cards are non-product by design.
- **Exact/factual text lives here, never in a Blotato-generated image** (diffusion
  garbles text). For "photo + headline," Blotato makes the photo, an HTML card lays
  the words on top.
- **Watermark is baked in** (the `.watermark` element), not a Blotato prompt.
- **Verify shipping/customs numbers** before publishing — they're `verify:true`
  claims in `education-topics.yaml`. `shipping-timeline.html` ships with placeholder
  day ranges; confirm real figures first.
- **Real charts** (beyond a simple timeline/table) → load the `dataviz` skill.

## Fonts

Renders use fonts installed on this Mac (`Baskerville` for display). For pixel-identical
output on any machine, embed a webfont: add an `@font-face` with a base64 `data:` URI
in `mela-kit.css` and point `--serif` at it. Not required for local rendering today.
