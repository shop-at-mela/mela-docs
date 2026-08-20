# Mela Visual Scorecard

**Last updated:** August 20, 2026
**Canonical home for:** the pre-publish **visual** quality gate — the harsh SHIP / REVISE / BLOCK band a post's image or reel must clear *before* it publishes. Sibling to `pre-publish-scorecard.md` (the caption gate) — same banded structure, same hard-fail-first discipline, same voice. The visual is **~90% of the impression** (`hook-engineering.md` §3), so this gate is at least as important as the caption gate, not a lesser add-on.

**Points at, does not restate:** the aesthetic rules, Blotato templates, watermark spec, education visual system, and the tool-decision procedure all live in `visual-style-guide.md`. This doc grades *against* those rules; it does not re-describe them. If this and `visual-style-guide.md` disagree, `visual-style-guide.md` wins and this file is stale.

> **What this is vs. isn't.** This is the *pre-publish, editorial* gate — grade a source/render, catch a weak first frame before it ships. It is **not** the post-hoc, data-driven teardown (`metrics-log.md` scores published posts against baseline). Two different loops: this one predicts, that one measures. This one uses no live data — it's judgment against the rules. Never conflate the two.

---

## Core stance

- **Hard-fail gate runs FIRST** (pass/fail). **Any single fail, at any stage, = BLOCK**, regardless of the diagnostic scores.
- **Diagnostic 1–10 dimension scores are LOGGED but NON-GATING.** No composite, no weighted sum — that bug was already killed once in the caption gate (`pre-publish-scorecard.md` §5) and does not get reintroduced here.
- **Three-band verdict** — SHIP / REVISE / BLOCK — decided by explicit logic (Band Logic below), not a score threshold.
- **Harshness standard:** a false SHIP costs more than an honest REVISE. A weak first frame live for a week wastes more than one more re-render or reframe costs now.

### Governing anti-rework principle

> **Pre-render PREVENTS. Post-render DETECTS ONLY render-introduced defects.**
>
> Stage 1 (pre-render) catches everything knowable from the source image and the brief — bad listing, low resolution, no staging plan, baked-in text, wrong routing. Stage 2 (post-render) catches only what you *cannot* see until the render exists — morphing, color drift, garbled text, a broken aspect ratio. **If Stage 2 ever BLOCKs on something knowable at Stage 1, the Stage 1 gate was too loose — tighten it, don't just fail the render.** A defect belongs at the earliest stage that could have caught it.

---

## The stages

### Stage 0 — Does this even need Blotato?

Runs before any grading and before any credit is spent. This is the gate's front door.

- **Prefer the untouched real product photo**, or a real photo + HTML-composited watermark, when the source already meets baseline staging (`visual-style-guide.md` → Backgrounds & Settings). It costs **zero credits** and carries **zero morph risk**.
- **Route to a Blotato scene only when the source lacks staging** (white/seamless background, no context).
- **For reels where morph risk is high** (garment drape, jewelry detail, multi-object scenes): render **one still/slide first and diff it** against the source (a cheap probe) before spending credits on full motion.
- Full tool logic (which template, which gate, when it's HTML vs. Blotato vs. SVG vs. Canva) is `visual-style-guide.md` → **Tool decision procedure**. Run that procedure here; this stage does not re-derive it.

### Stage 1 — Pre-render (source + brief)

Wired into `/social-review` Phase 3b (product visuals) and Phase 3d (education/anchor visuals). Runs **before** any render request goes out.

1. **Grade the source** — resolution, staging, no baked text, real product (not a stock/placeholder image).
2. **Verify listing provenance** — the source image traces to an IN-STOCK, OPEN, live-listing row, SKU-keyed (see Hard-fail row 1 — this is the drift-bug guard).
3. **Write the scene brief** — outcome-language prompt, category styling, watermark spec, per `visual-style-guide.md`.
4. **Predict frame 0** — before rendering, state what the first frame/cover *should* look like and whether it will pass the First-Frame Test below. If the brief can't produce a frame-0 that would pass, fix the brief now, not after the render.
5. **Confirm the US-context cue** — per `visual-style-guide.md` → Diaspora Anchoring, for a product photo the *scene* is the anchor. Name it in the brief (a modern US kitchen, a Diwali table in an American home) before rendering.

### Stage 2 — Post-render QA

Wired into `/social-review` Phase 6, before the publish confirmation.

**Frame this as DIFF RENDER AGAINST SOURCE, not "view and grade in isolation."** This is what makes an AI QA pass reliable: put the source image and the render side by side and check what *changed*, rather than judging the render cold.

- **Morphing / hallucination** — extra or missing parts, warped proportions, wrong product count vs. source.
- **Color drift** — does the render misrepresent the product's actual color vs. the source (beyond stylistic warmth/lighting)?
- **Garbled text** — any product label/text in-frame, OCR it; diffusion garbles text reliably.
- **Watermark** — present, legible contrast at its actual placement on the *rendered pixels* (not assumed from the prompt), not overshadowing the product.
- **Aspect / safe zone** — actual output ratio and whether key content sits inside the platform's crop-safe zone.
- **Payoff visibility** — for reels/carousels, is the promised reveal actually visible in the render.

### Stage 3 — Human aesthetic sign-off (founder/wife)

Not "do you like it." A checklist of exactly what AI cannot verify — everything AI-verifiable (hard-fail gate + Stage 1/2) is already done and attached, so human attention goes straight to taste:

1. **Color true to the REAL product?** (AI can catch drift vs. the source image; only a human who has seen the actual product, or trusts the brand's own photography, can confirm the source itself was accurate.)
2. **Staging feels Mela** — calm, not exoticizing, not stock? (Gestalt read; a human catches "technically correct but feels off" that no rule captures.)
3. **On the contact sheet** (frame0 · mid · payoff, all at real thumbnail size) **does the story read small?**
4. **Batch consistency** — does this sit with the week's other assets as one hand, or does it look like a different brand made it?

Attach the AI's completed hard-fail result + Stage 1/2 findings + the contact sheet to this review — never ask a human to re-check what the gate already cleared. **Output a band** (SHIP / REVISE / BLOCK), not a vibe — the human sign-off still resolves to the same three-band verdict, it just runs on a different checklist.

### Stage 4 — Publish-step mini-gate (reels only)

Runs at the actual IG publish step, **on the published artifact** — after the manual audio + cover assembly that happens inside IG. **The published artifact is NOT the silent rendered artifact** — this is the biggest hole a render-only gate would miss, so it gets its own stage.

| Check | What to verify |
|---|---|
| Audio set + synced | Audio is present and synced to the cuts; respect the Business-account Meta Sound Collection constraint (`reel-audio-strategy.md`) |
| Cover frame | Deliberately set (not left to IG's auto-pick), and passes the 3:4 grid-crop safe zone |
| Length | Under 30 seconds |
| Loop | Clean — the last frame cuts back to frame 0 without a jarring jump |

Any fail here = BLOCK, same as any other stage — see Hard-fail rows 16–18.

---

## Hard-fail gate (pass/fail, any one fail at any stage → BLOCK)

Not point deductions. Fix and re-run — a visual that would otherwise score well does not ship with a hard-fail standing.

### Pre-render / source (Stage 1)

| # | Hard fail if the source/brief… | Source rule |
|---|---|---|
| 1 | Is **not** from an IN-STOCK, OPEN, live-listing row, SKU-keyed and verified | Listing-ID drift lesson — `[[project_listing_id_drift_bug]]`; `[[feedback_verify_listing_and_blotato_label_garble]]` |
| 2 | Is an **AI-generated product** image, not a real product photo | `visual-style-guide.md` → Blotato Templates; `brand-brief.md` → Never |
| 3 | Is **below resolution** (IG < 1080px long edge; Pinterest < 1000×1500) | `visual-style-guide.md` → Instagram Feed / Pinterest Pins |
| 4 | Is a **white/seamless source with no staging planned** | `visual-style-guide.md` → Backgrounds & Settings |
| 5 | Has **baked-in price/title/text on the source** | `visual-style-guide.md` → Text Treatment |
| 6 | Routes **education** (`trust_service` / `cultural_education`) through **Product Scene Placement**, OR puts a **product on education slide 1** | `visual-style-guide.md` → Education Visual System |
| 7 | Grid is off and the brand/product asset's **grid face** (frame0/cover/slide1) is a **lone text card** (must be product-forward) | `visual-style-guide.md` → Grid face: product-forward |

### Post-render (Stage 2, judged by source-vs-render diff)

| # | Hard fail if the render… | Source rule |
|---|---|---|
| 8 | Has **garbled product text/label** (OCR gibberish) | `visual-style-guide.md` → Tool decision procedure guardrails |
| 9 | Shows the **product morphed / hallucinated parts / wrong count** vs. source | Anti-rework principle above |
| 10 | Shows **color drift that MISREPRESENTS the product** vs. source (beyond stylistic warmth) | Anti-rework principle above |
| 11 | Is the **wrong aspect ratio** or has key content **outside the safe zone** (IG 3:4; Pinterest 2:3) | `visual-style-guide.md` → Instagram Grid Row Anchors; Pinterest Pins |
| 12 | Has a **watermark missing**, OR **contrast below legibility** at its placement, OR **overshadowing the product** | `visual-style-guide.md` → Affiliate & Watermark |
| 13 | Has **baked-in price/title/text introduced by the render** | `visual-style-guide.md` → Text Treatment |
| 14 | Is a **reel with no visible payoff beat** | Mirrors caption-gate row 7; `hook-engineering.md` §4 |
| 15 | Is **exoticizing/cliché staging** (mystical-India trope) | Visual twin of the caption exoticize hard-fail — `brand-brief.md` → Never |

### Publish-step, reel only (Stage 4)

| # | Hard fail if the published reel… | Source rule |
|---|---|---|
| 16 | Is **published silent** / audio not set | `reel-audio-strategy.md` |
| 17 | Has a **cover frame not deliberately set**, OR the cover **fails the 3:4 grid-crop safe zone** | `visual-style-guide.md` → Instagram Grid Row Anchors |
| 18 | Runs **over 30 seconds** | `hook-engineering.md` §4 |

If any fail → **BLOCK. Report the failed rows, grouped by stage; do not proceed to diagnostic scoring until fixed.** The gate is the point; the diagnostic pass is secondary.

---

## Diagnostic dimensions (1–10 each) — DIAGNOSTIC ONLY, NON-GATING

Score each 1–10 and be specific about the problem whenever you score under 8. **These scores are logged, not summed into a pass/fail** — they exist to correlate score against real performance (`metrics-log.md`) over time. The band verdict below is what actually gates publish. Weights are diagnostic/logging only — **not** band-deciding, no composite.

| Dimension | What to check |
|---|---|
| **First-frame scroll-stop** | The visual analog of the caption hook — see the First-Frame Test below. Does frame 0 / the cover / the pin stop a scroll at real thumbnail size? |
| **Product desirability & legibility** | Is the product clearly the subject, well lit, in focus, and identifiable at a glance? |
| **Save/watch-through reason** | Is there a reason to save (Pinterest) or watch through (reel) beyond the first frame — a detail, a reveal, a texture worth a second look? |
| **Brand-fit** | Earthy/calm Mela baseline held, plus the US-context cue present (`visual-style-guide.md` → Diaspora Anchoring). |
| **Motion quality & pacing** (reels only) | Cuts land on beat, pacing intentional rather than template-default, loop clean — not generic template drift. |
| **Technical polish** | Lighting, color, composition, negative space. |

---

## Band verdict: SHIP / REVISE / BLOCK

No numeric composite. Three bands, decided by explicit logic:

**BLOCK** = any hard-fail row fires, at any stage. Full stop, regardless of anything else.

**REVISE** = gate clear (no hard-fail), but **any** of the following:
- (a) **First frame fails the thumbnail test** (First-Frame Test below).
- (b) **No save/watch reason** — the payoff is missing or too weak to earn a save or a watch-through.
- (c) **Scene carries no situation/US-context anchor** — the visual twin of the caption gate's "situational relevance." For product photos, the *scene itself* is the anchor (there's no text layer); if the scene could run unchanged on the brand's own India feed, it fails this.
- (d) **Motion cheap / pacing off** (reels only) — template-default drift, cuts that don't land, a loop that jumps.

**SHIP** = gate clear **and** frame-0 stops at thumbnail size **and** payoff/save-reason is present **and** the scene anchors the situation **and** (reels) motion is clean. Everything else — technical-polish notes under 8, minor composition preferences — is a **polish note**, not a blocker.

**Harshness standard.** A false SHIP is worse than an honest REVISE — it wastes more downstream time (a weak visual live for a week, or a cheap-looking reel logged as validated) than one more re-render or reframe costs now. Don't let banding collapse into "three easy checkboxes = ship." A frame-0 that "looks fine" in isolation but disappears at 160px is not a SHIP.

---

## The First-Frame Test

The exact protocol — run all five steps, don't eyeball it:

1. **Export the object.** "First frame" is not one thing — it splits into **four distinct objects**, and cover-frame selection is its own decision, separate from the render itself:
   - reel frame-0
   - IG grid cover (may differ from frame-0 if a cover frame was deliberately selected)
   - the selectable cover itself (the decision of *which* frame becomes the cover)
   - the Pinterest pin (the whole image, not a crop)
2. **Downscale to the real surface width**: ~160px for the IG feed, ~120px for a 3-up grid tile, ~236px for Pinterest masonry.
3. **0.5-second glance + squint pass** (blur or grayscale the downscaled image): Is the subject identifiable? Is there one clear focal point / subject-ground separation? Is any on-frame word (reel/education only) actually legible at this size?
4. **Evaluate IN-CONTEXT** — drop it into a mock 3-up grid row or a masonry layout beside neighboring tiles, never judged in isolation. A frame that reads fine alone can disappear next to competing tiles.
5. **On fail: reframe, recrop, or RESELECT a different cover frame first.** This is usually cheap and does **not** require a re-render — check cover-frame reselection before reaching for a new render.

Pair "stops the scroll" with "gives a reason to stay" — a strong frame-0 with no save-reason (Stage 2 payoff check) still lands in REVISE via band-logic row (b).

---

## Instagram vs. Pinterest

| | **Instagram** | **Pinterest** |
|---|---|---|
| **Shared** | Source staging, listing provenance, watermark, no baked price, resolution floor — identical bar on both | *(same row)* |
| **First-frame object** | Reel frame-0 **and** the 3:4 grid cover (two objects, may differ) | The whole 2:3 pin (no separate cover concept) |
| **Motion-payoff lever** | Reels — yes, mandatory payoff beat | N/A — drop this dimension entirely for pins |
| **Text on image** | **NOT allowed** on product images (`visual-style-guide.md` → Text Treatment) | **ALLOWED and encouraged** — keyword-led pin title (`visual-style-guide.md` → Pinterest Pins) |
| **Evaluated at** | ~160px feed width | ~236px masonry, next to search competitors |
| **Rewarded-metric framing** | Saves, watch-through, shares | Outbound **click** — "does it look like the answer to a search" |
| **Safe zone** | 3:4 grid crop | 2:3 full pin |

**The IG "no text on image" rule must NEVER be applied to Pinterest.** A correctly keyword-titled pin is not a hard-fail row 5/13 violation — it is the Pinterest-native requirement. Grading a pin against the IG text rule is a gate misapplication, not a real defect.

---

## Output the card

```
## Visual Verdict: [SHIP / REVISE / BLOCK]

### Hard-fail gate (grouped by stage)
Pre-render/source:  [✅ all clear]  — or —  [🚫 BLOCKED: rule #N — <what fails> → <fix>]
Post-render:        [✅ all clear]  — or —  [🚫 BLOCKED: rule #N — <what fails> → <fix>]
Publish-step (reel): [✅ all clear] — or — [🚫 BLOCKED: rule #N — <what fails> → <fix>] — or — [N/A, not a reel]

### Band reasoning (if REVISE)
[which of (a) first-frame / (b) save-watch reason / (c) situation anchor / (d) motion fired, with specifics]

### Diagnostic scores (logged, non-gating)
| Dimension | Score | Note (if under 8) |
|---|---|---|
| First-frame scroll-stop | X/10 | ... |
| Product desirability & legibility | X/10 | ... |
| Save/watch-through reason | X/10 | ... |
| Brand-fit | X/10 | ... |
| Motion quality & pacing (reels only) | X/10 | ... |
| Technical polish | X/10 | ... |

### Top 3 fixes (ranked by impact)
1. **[issue]** — Why it hurts: <cost> · Fix: <exact fix — reframe / recrop / reselect cover / re-render / re-prompt>
2. ...
3. ...
```

Every fix names the **exact issue**, the **cost**, and an **exact fix** — never "make it pop more." That's where the operator actually learns.

---

## What NOT to do

- **Don't hard-fail on taste.** Gestalt/aesthetic judgment ("does this feel Mela") routes to Stage 3 human sign-off, not the AI hard-fail gate.
- **Don't grade color fidelity to the real product as a hard-fail on your own.** AI catches drift *vs. the source*; whether the *source itself* is color-accurate to the physical product is a Stage 3 human call.
- **Don't apply the IG "no text on image" rule to Pinterest.** A correct keyword-titled pin is compliant, not a violation.
- **Don't BLOCK post-render on anything knowable pre-render.** If Stage 2 catches something Stage 1 should have caught, that's a Stage 1 gap — tighten Stage 1, don't just fail the render and move on.
- **Don't build a composite score.** No weighted sum, no "8+ ships" threshold — the caption gate killed that bug once already; it doesn't come back here.
- **Don't skip Stage 4 for reels.** The rendered artifact is not the published artifact — silent audio, an undeliberate cover, or a jarring loop only show up after manual IG assembly, and none of the earlier stages can catch them.
