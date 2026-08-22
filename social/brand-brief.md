# Mela Brand Brief

**Last updated:** August 19, 2026
**Purpose:** The single, skimmable voice spec the `pre-publish-scorecard.md` grades "voice match" against, and the wedge `hook-engineering.md` pulls from. This is a **pointer document** — it names the rule and links its canonical home; it does not restate the detail. If this and a canonical doc disagree, the canonical doc wins and this file is stale.

---

## One-line positioning

Mela helps the Indian diaspora in the US **discover** brands from India that are hard to find here — inspiration-first, not an Amazon-style fulfillment catalog. **Mela discovers; brands ship.**
→ `[[insight_inspiration_vs_fulfillment]]`, `[[project_mela_multi_category_scope]]` (fashion, home & kitchen, jewelry, baby/kids — not baby-only).

## The wedge (fuels the highest-yield hooks)

**Belonging — the diaspora *situation*, never the identity.** The suitcase economy, the restock-from-home moment, the first Diwali in the US. This is the one thing competitors outside the diaspora can't copy; reach for it first.
→ `hook-engineering.md` §2 (belonging trigger) + `visual-style-guide.md` → Diaspora Anchoring.

## Voice

Calm, specific, respectful. Living culture, **not** heritage-relic. Short sentences, no dashes, real specifics over adjectives. Sounds like a knowledgeable friend, never generic AI copy or a hard sell.
→ `visual-style-guide.md` → Caption Style · `[[project_living_culture_reframe]]` · brand voice house rule in `shopify_brands.py` docstring (`[[project_brand_voice_house_rule]]`).

## Visual identity

Navy `#2D2D7B` + marigold `#F0A030`. Natural/earthy, lifestyle-staged, no white backgrounds, no price/title text on product images. "Discovered on [Mela logo]" watermark, subtle, never overshadowing the product.
→ `[[project_mela_brand_identity]]` · `[[feedback_mela_social_aesthetic]]` · `[[feedback_mela_watermark_spec]]` · `visual-style-guide.md`.

## Who we talk to (pick one lead per post)

| Persona | Leads with | Guardrail |
|---|---|---|
| **Sarah** | Certifications + materials | Never vague "eco-friendly" without a named cert |
| **Priya** | Occasion | Avoid "traditional / ethnic / Bollywood / costume" |
| **Arun** | Craft origin + visual story | ≥1 sentence of cultural context per craft term |
| **Neha** | Familiar brands, price, belonging | Occasional lead only — she's in inspiration mode |

→ `buyer-personas.md` (incl. known gaps `[[project_persona_known_gaps]]`).

## The 5 content angles

1 Belonging / suitcase economy · 2 Discovery ("brands you can't find") · 3 How it's actually made · 4 What the claim really means (certs) · 5 Occasion-in-America.
→ `hook-engineering.md` §5.

## Never (the hard-fail list)

The voice defined by what it refuses. These are the `pre-publish-scorecard.md` Step-1 hard fails:

- **Exoticize / other** Indian culture ("exotic," "500-year-old relic," museum framing).
- **Disparage the shopper's own local / family-run desi store** (belonging ≠ gatekeeping).
- Say a brand is **"unavailable in the US"** — say "hard to find." → `[[feedback_mela_copy_positioning]]`.
- Say **"Mela ships" / "available from Mela"** — brands ship, Mela discovers.
- **@tag a brand** — paused during warmup, no affiliate agreement yet. → `[[no-brand-tagging-yet]]`.
- **Anchor the viewer's identity** ("for Indian-American families") instead of their situation.
- **AI-generate a product**, or overlay name/price/text on a product image.

---

*Machine-readable summary for the scorecard's voice-match check:* calm · specific · non-exoticizing · living-culture · discovery-not-access · belonging-is-the-moat · Mela-discovers-brands-ship · no-dashes · short-sentences.
