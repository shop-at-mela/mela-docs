# Mela Pre-Publish Gate (single pass)

**Last updated:** August 22, 2026
**Canonical home for:** the **one** pre-publish pass a post runs before it ships during warmup. It merges the caption gate (`pre-publish-scorecard.md`) and the visual gate (`visual-scorecard.md`) into a single lane-routed checklist so you open **one doc, not two**, per post.

> **This doc does not replace the two scorecards — it orchestrates them.** The full diagnostic banks, band logic, First-Frame Test, and per-dimension detail still live in `pre-publish-scorecard.md` (caption) and `visual-scorecard.md` (visual). Nothing there was deleted. This gate inlines the **blocking** checklist so the common case needs no doc-hopping, and points to those banks when you want the deep detail. If this and a scorecard disagree on a hard-fail rule, the scorecard wins and this file is stale.

---

## Warmup posture (why this gate is lean)

We are a **zero-audience warmup account, no validated performance data, two operators.** First principles:

- **The real risk is under-shipping, not a weak post.** A post nobody sees costs ~nothing; a post that never ships costs the one thing that matters — time-to-baseline-data and the shipping habit.
- **But un-optimized ≠ off-brand.** The bar is **consistently on-brand and legible**, not "optimized." Early posts still train the algorithm's read of the account, so sloppy/illegible/off-brand is not free. Optimized-for-reach is what we can't judge yet.
- **Two kinds of gate, treated differently:**
  - **Harm-prevention + real-defect gates → BLOCKING** (cultural harm, false claims, affiliate misrepresentation, dead links, garbled/morphed renders). Irreversible at *any* audience size, cheap to check.
  - **Performance-optimization gates → COACHING** (hook-strength banding, first-frame thumbnail test, save-reason, motion pacing). They predict reach we have no data to validate. Logged as notes; they **never block a ship** during warmup.
- **Defer the *scoring*, not the *measurement*.** The 13-dimension 1–10 diagnostic scoring is **deferred** until ~20–30 posts of baseline exist to correlate against (see `metrics-log.md`). But we **capture the raw north-star metric + a one-line hypothesis from post #1** so that baseline actually accumulates.

When performance data exists (per the `metrics-log.md` promote/kill thresholds), the coaching layer earns the right to gate again. Until then it coaches.

---

## Step 0 — Route the lane

| | **FAST LANE** | **FULL LANE** |
|---|---|---|
| **When** | Vetted brand · real product photo · listing verified OPEN | Education (`cultural_education` / `trust_service`) · any craft/cert/material **claim** · a brand's **first-ever** post · new/unvetted source |
| **Why** | Inherently low-risk; most hard-fails auto-pass or are a one-glance check | Carries the real irreversible risk (false claims, cultural framing, misleading teaching) |
| **Per-post effort** | Blocking checklist (most rows N/A) + one founder glance | Full blocking checklist **+ verify-claims-on-live-listing + education visual system** + founder review |
| **Coaching layer** | Logged, light | Logged, with extra attention to framing |
| **UX destination audit** | **Batched** (weekly / on first-post or page change), not per-post | Per-post if the post makes a page-specific promise |

**The blocking rules are identical in both lanes — the lane only changes how much scrutiny and per-post overhead each row gets.** You never drop a harm gate to go fast.

---

## Step 1 — Blocking hard-fail gate (both lanes; any one fail = BLOCK)

Deduped from the two scorecards (rules that appeared in both are stated once here). Tagged by **when** they fire — you cannot check a render before it exists, so the gate runs at three moments, not one instant.

### Copy (pre-publish) — from `pre-publish-scorecard.md`
1. **Exoticizes / others** Indian culture ("exotic," "500-year-old relic," museum-piece).
2. **Disparages the shopper's own** local / family-run desi store.
3. **Names the viewer's ethnicity / anchors identity** ("for Indian families in the US") instead of *situation*.
4. Says a brand is **"unavailable in the US"** (say "hard to find").
5. Says **"Mela ships / available from Mela"** (Mela discovers, brands ship).
6. **@tags a brand** (paused during warmup).
7. **Craft / cert / material claim not verified** on the live listing (Full lane: verify-first is mandatory).
8. **Missing UTM or alt text.**
9. **Bare / guessed URL path** (not a confirmed `shopatmela.com` path).

### Visual source (pre-render) — from `visual-scorecard.md` Stage 1
10. Source **not from an IN-STOCK, OPEN, live-listing row, SKU-keyed** (drift-bug guard — `[[project_listing_id_drift_bug]]`).
11. **AI-generated product** image, not a real product photo.
12. **Below resolution** (IG < 1080px long edge; Pinterest < 1000×1500).
13. **Baked-in price/title/text on the source** image.
14. **Education routed through Product Scene Placement**, or a **product on education slide 1** (Full lane).
15. Grid off and the brand/product **grid face is a lone text card** (must be product-forward).

### Visual render (post-render) — from `visual-scorecard.md` Stage 2 (diff render vs source)
16. **Garbled product text/label** (OCR gibberish).
17. **Product morphed / hallucinated parts / wrong count** vs source.
18. **Color drift that misrepresents the product** vs source.
19. **Wrong aspect ratio** or key content **outside the safe zone** (IG 3:4; Pinterest 2:3).
20. **Watermark missing**, illegible-contrast at its actual placement, or **overshadowing** the product.
21. **Baked-in text introduced by the render.**
22. **Reel with no visible payoff beat.**
23. **Exoticizing / cliché staging** (mystical-India trope) — the visual twin of row 1.

### Publish-step (reel only, at manual IG assembly) — from `visual-scorecard.md` Stage 4
24. **Published silent** / audio not set.
25. **Cover frame not deliberately set**, or cover fails the 3:4 grid-crop safe zone.
26. **Over 30 seconds.**

**Any fail → BLOCK. Report the failed row(s), fix, re-run.** No coaching note or lane overrides a hard-fail.

---

## Step 2 — Coaching notes (logged, NON-blocking during warmup)

Record these; do **not** let them stop a ship. Full definitions + the First-Frame Test live in the two scorecards.

- **Diaspora anchoring / situational relevance** — **the loud one.** It's the moat and the shareability lever, not just an anti-exoticizing blocker. Always note whether the post anchors a *specific, felt shopper situation* (`visual-style-guide.md` → Diaspora Anchoring). Weak here = fix if cheap, but still ships.
- Hook strength / first-3-words test (`pre-publish-scorecard.md`).
- First-frame scroll-stop / thumbnail test (`visual-scorecard.md`).
- Save / watch-through reason; motion quality & pacing (reels).
- Specificity & curiosity, voice-match, platform-fit.
- **The 13-dimension 1–10 scoring is DEFERRED** — do not score per post yet. It resumes once `metrics-log.md` has a baseline to correlate against.

---

## Step 3 — Learning instruments (cheap; run from post #1)

These are what make the deferral safe — you keep learning without the scoring overhead:

1. **One-line hypothesis** — what is this post testing? (which angle / hook / persona). Log it in the campaign YAML `hypothesis` field.
2. **North-star metric capture** — after publish, capture the one platform metric that matters (**IG = saves; Pinterest = outbound clicks**) into `metrics-log.md` + the campaign YAML `northstar_metric` field. This is just reading a number Blotato/IG already gives you; it builds the baseline the deferred scoring will one day use.

---

## Step 4 — Tool-outage fallback lane

**A vendor outage must never zero a week.** If Blotato (or any render vendor) is down or a render is stuck:

- Ship the **real product photo** (already baseline-staged) with the **HTML-composited watermark** (`templates/photo-watermark.html`, rendered via `templates/render.sh`) and a **manual schedule/publish**.
- The blocking gate still applies (it's a real photo → morph/garble/AI-product rows auto-pass; check watermark contrast + aspect on the composite).
- Log the post as fallback-produced so the batch isn't blocked waiting on the vendor.

*(This lane is not hypothetical — it's the standing answer to the Aug 2026 Blotato pipeline outage.)*

---

## Output the card (single, replaces the two separate cards during warmup)

```
## Pre-Publish Gate: [SHIP / BLOCK]   ·   Lane: [FAST / FULL]

### Blocking hard-fail gate
Copy (pre-publish):     [✅ clear]  — or —  [🚫 row #N — <what fails> → <fix>]
Visual source (pre):    [✅ clear]  — or —  [🚫 row #N — <what fails> → <fix>]
Visual render (post):   [✅ clear]  — or —  [🚫 row #N — <what fails> → <fix>]
Publish-step (reel):    [✅ clear / N/A]  — or —  [🚫 row #N — <what fails> → <fix>]

### Coaching notes (logged, non-blocking)
Diaspora anchor: <note>  ·  Hook: <note>  ·  First-frame: <note>  ·  Other: <note>
Diagnostic 1–10 scoring: DEFERRED (no baseline yet)

### Learning
Hypothesis: <one line — angle/hook/persona under test>
North-star metric to capture post-publish: IG saves / Pinterest clicks
```

Note there is no `REVISE` band during warmup: a post either clears the blocking gate (**SHIP**) or it doesn't (**BLOCK**). Coaching notes never produce a REVISE that halts shipping. The three-band SHIP/REVISE/BLOCK logic in the two scorecards resumes when the coaching layer is re-armed (post-baseline).

---

## When warmup ends (re-arming the gates)

Once `metrics-log.md` has a baseline and the promote/kill thresholds start firing:
- Resume the 13-dimension diagnostic scoring.
- Re-arm the performance-optimization checks (hook banding, First-Frame Test, save-reason, motion) from **coaching** back to the **REVISE band** in the two scorecards.
- The Fast/Full lane split and this single-pass structure stay — they're a permanent simplification, not a warmup-only crutch.
