# Mela Pre-Publish Scorecard

> **⚠️ During warmup, run the single pass in `pre-publish-gate.md`, not this doc directly.** The gate merges this (caption) with `visual-scorecard.md` (visual) into one lane-routed checklist so you open one doc per post. This file is now the **detailed caption diagnostic bank** the gate points to — full content retained. Warmup rules the gate applies: the **Step 1 hard-fail gate here is BLOCKING**; the **Step 2 diagnostic 1–10 scoring is DEFERRED** (capture the raw metric per `metrics-log.md`, defer scoring until a baseline exists); hook/voice checks are **coaching notes that never halt a ship**. The full SHIP/REVISE/BLOCK banding below **re-arms when warmup ends** (`pre-publish-gate.md` → "When warmup ends").

**Last updated:** August 22, 2026
**Canonical home for:** the pre-publish quality gate — the harsh SHIP / REVISE / BLOCK band a post must clear *before* it publishes.
**Adapted from:** Blotato's `post-grader` skeleton (hook-weighted scoring, first-3-words test, top-3-fixes format), re-tuned for Mela's voice and guardrails. Their numeric composite is **replaced with a three-band verdict** (SHIP / REVISE / BLOCK) — the old "≥8.0" weighted-sum math produced false-precision and magnitude bugs (a −0.5-per-fail penalty stacking arbitrarily against a 40%-weighted hook). The 7 diagnostic dimensions and their 1–10 scores are **kept**, but as a logged, non-gating record for future score→performance correlation — they no longer decide the verdict. Their generic "polarity/virality" dimension stays **removed** — it pushes toward the manufactured controversy `hook-engineering.md` §2 forbids — and stays replaced with **situational relevance** (our moat) plus the **hard-fail gate** built from our real defects.

> **What this is vs. isn't.** This is the *pre-publish, editorial* gate — grade a draft, catch the weak hook before it ships. It is **not** the post-hoc, data-driven teardown (`metrics-log.md` scores published posts against baseline). Two different loops: this one predicts, that one measures. This one uses no live data — it's judgment against the rules. Never conflate the two.

---

## When to run

Inside `/social-review`, **Phase 5b** — after the caption + visual are drafted (Phase 3) and before Approve & Publish (Phase 6). Applies to **every** post, product and education alike. `/social-launch` runs it per-post on the batch before the founder review.

Standalone: paste a draft caption + say "grade this" → run the scorecard, return the card, offer to apply the top-3 fixes.

**Be harsh but fair on the diagnostic scores.** A 7 is good. An 8 is strong. A 9 means almost nothing needs fixing. A 10 doesn't exist. Most first-draft hooks score 4–6. But the diagnostic score is not the verdict — see Step 4 for how the band is actually decided, and the harshness standard that applies to it.

---

## Step 1 — Hard-fail gate (pass/fail, runs FIRST)

These are not point deductions. **Any single fail = BLOCK, regardless of the diagnostic scores.** They're the `/social-review` cross-cutting defects + `hook-engineering.md` §2 "Never" column, collected as a gate. Fix and re-run — a post that would otherwise score well does not ship with a hard-fail standing.

| # | Hard fail if the post… | Source rule |
|---|---|---|
| 1 | **Disparages the shopper's own local / family-run desi store** (belonging ≠ gatekeeping) | `hook-engineering.md` §2, §5 |
| 2 | **Exoticizes / others Indian culture** ("exotic," "500-year-old relic," museum-piece framing) | `visual-style-guide.md` → What NOT to Do |
| 3 | Says a brand is **"unavailable in the US"** (say "hard to find") | memory `[[feedback_mela_copy_positioning]]` |
| 4 | Says **"Mela ships" / "available from Mela"** (Mela discovers, brands ship) | `/social-review` 3c affiliate precision |
| 5 | **@tags a brand** on any platform (paused — warmup, no affiliate agreement) | memory `[[no-brand-tagging-yet]]` |
| 6 | Uses an **AI-generated product** image, or a product image with **name/price/text overlay** baked in | `visual-style-guide.md` Blotato Templates |
| 7 | A **reel with no payoff beat** (pure wordmark-converge / no reveal) | `hook-engineering.md` §4 |
| 8 | States a **craft or certification claim not verified on the live listing** | `/social-review` Ph2/3d verify-first |
| 9 | **Missing UTM, alt text, or watermark** (any one) | `/social-review` cross-cutting |
| 10 | **Bare or guessed URL path** (not a confirmed `shopatmela.com` path) | `/social-review` Ph2 |
| 11 | **Names the viewer's ethnicity / anchors identity** instead of *situation* ("for Indian-American families") | `visual-style-guide.md` → Diaspora Anchoring |

If any fail → **BLOCK. Report the failed rows; do not proceed to diagnostic scoring until fixed.** The gate is the point; the diagnostic pass is secondary.

---

## Step 2 — Diagnostic dimensions (1–10 each) — DIAGNOSTIC ONLY, NON-GATING

Score each 1–10 and be specific about the problem whenever you score under 8. **These scores are logged, not summed into a pass/fail** — they exist so we can correlate score against real performance (`metrics-log.md`) over time. The band verdict in Step 4 is what actually gates publish. Weights below are diagnostic/logging weights, carried over from the original hook-weighted design — they are **not** band-deciding.

| Dimension | Weight (diagnostic) | What to check |
|---|---|---|
| **Hook strength** | 40% | Does the first line / first frame / first ~125 chars stop the scroll? Run the **first-3-words test**: reading only the first 3 words, is there curiosity, surprise, or emotional pull? Is it a `hook-engineering.md` §2 Mela-safe trigger, or throat-clearing ("Discover our…," "In today's world," "Let me tell you about")? Would it stand alone as a line? Score brutally — most are 4–6. |
| **Situational relevance** | 15% | Does the post anchor a *specific, felt* shopper moment — not a generic category? See the dedicated section below. Replaces Blotato's "polarity." |
| **Specificity & curiosity** | 10% | Real origin ("handwoven in Varanasi"), a real craft term, a named cert, a real number — or vague ("beautiful," "eco-friendly," "great quality")? Does it open a loop and then close it? |
| **Payoff delivered** | 10% | Does the post/reel actually deliver the thing the hook promised — the reveal, the finished scene, the "oh, that's why"? A hook that writes a check the body doesn't cash scores low. Applies to **every format**, not just reels. |
| **Voice match** | 10% | Grade against `brand-brief.md` (the single voice spec): calm, specific, respectful, living-culture, discovery-not-access — or generic AI copy that could sell anything? Named POV, not filler. Folds in the Step 3 density-backstop flag if it fires. |
| **Discovery framing & affiliate precision** | 10% | "Hard to find," never "unavailable." "Ships from India / discovered on Mela," never "available from Mela." Price skipped where markup is high. Discovery-framed soft CTA, not a hard sell. |
| **Platform fit** | 5% | IG: hook inside first 125 chars, max 5 mixed hashtags in caption-end/first-comment (Blotato API hard cap, confirmed 2026-08-27), not on image. Pinterest: keyword title ≤60 chars, keywords not hashtags. Format matches the platform's rewarded metric (IG = saves, Pinterest = clicks). |

### Situational relevance — what "anchored" means

Anchor a **specific, felt** shopper moment:

- ✅ "Reading a confusing care tag before you buy."
- ✅ "Your cousin in India tags this on every wedding post."
- ❌ "You're shopping for shoes." (generic category, not a moment)

**Belonging/diaspora is the highest-yield version of this and is the moat** — reach for it first (`hook-engineering.md` §2, `brand-brief.md`). But a well-anchored **non-diaspora** situation (a cert lane, a materials question, a gifting deadline) is fully SHIP-worthy on its own. "Coach toward a diaspora angle" is a **suggestion note only** — it must **never** lower the band or be scored as a penalty against situational relevance. This protects the Sarah/cert lane and the other non-belonging lanes the brand deliberately rebalanced toward after over-serving Arun's heritage angle (memory `[[project_social_persona_coverage_gaps]]`).

---

## Step 3 — Voice micro-rules (judge function, not lexeme)

No penalty math here — the old "−0.5 each, capped −2" scheme is removed; it produced magnitude bugs against the hook's weight. Instead: one item below is a genuine band-deciding trigger (fatal, feeds Step 4d), everything else is a note.

| Rule | Treatment |
|---|---|
| **Filler-openers in the hook** | **Fatal — REVISE trigger** (Step 4d). Throat-clearing that fails the first-3-words test: "Discover our…," "In today's world," "Let me tell you," "Picture this," "Are you ready to." This is a hook-level failure, not a body-level polish note. |
| **Mid-sentence intensifiers** (just, really, very, actually, basically, simply, literally) | **Note, judgment call — never auto-REVISE.** Judge whether the word is load-bearing. E.g. "'vegan leather' is usually **just** plastic" — "just" means "merely" and is legitimate, deflating rhetoric, not filler. |
| **Intensifier density backstop** | **3 or more intensifiers in the BODY** → a voice-match diagnostic flag (logged against the Voice match score in Step 2) — at that density it reads as generic AI copy, regardless of whether any single instance was load-bearing. |
| **Digits** | Targets **hook** numbers only — "3 tells," not "three tells," for scroll-stopping punch. Rhetorical enumeration in the **body** ("One… Two… Three…") reads naturally and is not penalized. Always a note, never a gate. |
| Dashes | No em dashes or " – " dashes anywhere (`visual-style-guide.md` → Caption Style). Note. |
| Short sentences | No sentence runs long / comma-spliced; caption reads in short beats. Note. |
| Hashtag/keyword count | IG max 5 in caption-end/comment (Blotato hard cap); Pinterest keywords, 0 hashtags. Note. |

All rows except the filler-opener row are **body-level polish notes** — they never block the band on their own (see Step 4's SHIP definition).

---

## Step 4 — Band verdict: SHIP / REVISE / BLOCK

No numeric composite. Three bands, decided by explicit logic:

**BLOCK** = any Step 1 hard-fail row fires. Full stop, regardless of anything else.

**REVISE** = gate clear (no hard-fail), but **any** of the following:
- (a) **Hook does not land** — fails the first-3-words test, or the hook is vague.
- (b) **No situational anchor** — the post names no specific, felt shopper moment (see Step 2's Situational relevance section).
- (c) **Payoff missing** — the post/reel does not deliver what the hook promised. Applies to **all formats now**, not just reels.
- (d) **A filler-opener in the hook** (Step 3) — throat-clearing that fails the first-3-words test.

**SHIP** = gate clear **and** hook lands **and** a specific situational anchor is present **and** payoff is present **and** no filler-opener in the hook. Everything else — dashes, sentence length, hashtag count, intensifier density, diagnostic-dimension scores under 8 that aren't one of (a)–(d) — is a **polish note**, not a blocker.

**Harshness standard.** "Hook lands" means the current harsh bar, not a courtesy pass: most first drafts are 4–6 on the diagnostic hook score, and a hook at that level does **not** land. A false SHIP is worse than an honest REVISE — it wastes more downstream time (a weak post live, or a bad hook logged as validated) than one more revision pass costs now. Do not let banding collapse into "three easy checkboxes = ship." The bar for (a)–(d) is the same bar the old 40%-weighted hook score was protecting; it just isn't diluted by an average anymore.

---

## Step 5 — Output the card

```
## Pre-Publish Verdict: [SHIP / REVISE / BLOCK]

### Hard-fail gate
[✅ all clear]  — or —  [🚫 BLOCKED: rule #N — <the line that fails> → <fix>]

### Band reasoning (if REVISE)
[which of (a) hook / (b) situational anchor / (c) payoff / (d) filler-opener fired, with the exact line]

### Diagnostic scores (logged, non-gating)
| Dimension | Weight | Score | Note (if under 8) |
|---|---|---|---|
| Hook strength | 40% | X/10 | ... |
| Situational relevance | 15% | X/10 | ... |
| Specificity & curiosity | 10% | X/10 | ... |
| Payoff delivered | 10% | X/10 | ... |
| Voice match | 10% | X/10 | ... |
| Discovery & affiliate | 10% | X/10 | ... |
| Platform fit | 5% | X/10 | ... |

### Voice notes
[filler-opener flag if fatal; intensifier density flag if 3+ in body; digits note if relevant; dashes/short-sentence/hashtag notes; "none" if clean]

### Top 3 fixes (ranked by impact)
1. **[issue]** — Current: "<exact quote>" · Why it hurts: <cost> · Fix: "<exact rewrite>"
2. ...
3. ...
```

Every fix names the **exact line**, the **cost**, and an **exact rewrite** — never "make the hook better." That's where the operator actually learns.

---

## What NOT to do

- **Don't grade leniently on the band.** A false SHIP wastes more time than an honest REVISE.
- **Don't skip the hard-fail gate** because the rest looks clean. BLOCK always wins, regardless of the diagnostic scores.
- **Don't let "coach toward a diaspora angle" lower the band.** Situational relevance suggestion notes are never penalties — a well-anchored non-diaspora situation ships (protects the Sarah/cert lane and the other rebalanced lanes).
- **Don't auto-REVISE on a mid-sentence intensifier.** Judge whether it's load-bearing. Only a filler-**opener** in the hook is fatal; body intensifiers are a note, and only become a flag at 3+ density.
- **Don't rewrite the whole post** in the scorecard — verdict + specific fixes only; `/social-review` Phase 3 applies them, then re-run.
- **Don't treat this verdict as performance data.** It predicts; it doesn't measure. Only the `metrics-log.md` teardown, on real posts, promotes a hook from hypothesis to proven — the diagnostic scores here exist to make that future correlation possible.
- **Don't flag a style *preference* as a fail.** Grade against the rules here and in the canonical docs (`hook-engineering.md`, `visual-style-guide.md`, `brand-brief.md`). If it passes, it passes, even if you'd have written it differently.
