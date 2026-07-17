# Homepage Feedback — Session Handoff

> **Status:** Roundtable analysis complete (PM + UXR + UX-Design). Awaiting mockup review, then PRD.
> **Date:** 2026-07-07
> **Next action:** User is restarting terminal to clear macOS quarantine on `proposal/mela-homepage-mockup.html` so it can be read. After that: review mockup → align Tier 0 hero spec → PM drafts Homepage Hero PRD (Tier 0 + Tier 1).

---

## How to resume (new session, read this first)

1. **Read the mockup** `proposal/mela-homepage-mockup.html` — the product owner's reference/inspiration. Was blocked by `com.apple.quarantine` xattr; user cleared it via `xattr -d com.apple.quarantine <file>` + terminal restart. It likely already encodes owner intent for the hero.
2. **Read** `mela-docs/UXR/feedback-log.md` — the 3 logged feedback entries (F-001..F-003) this analysis is built on.
3. **Then** align the Tier 0 hero design against the mockup, and offer to draft the **Homepage Hero PRD** (scoped to Tier 0 + Tier 1 below).

Related plan file: `~/.claude/plans/web-client-homepage-feedback-i-playful-pizza.md` (the earlier A/B/C plan — now superseded by the tiering below).

---

## The feedback (3 sources, all first-impression / first-fold only)

- **F-001** (1st-gen diaspora, shops Indian brands): "too many product listings; no inspiration; doesn't know what to shop or how Mela differs from Amazon."
- **F-002** (US-market friend, no Indian-brand knowledge): "landing page doesn't signal India — no brand/hero/design cue; some products look like US-store items."
- **F-003** (1st-gen, UX designer): "font and design language don't feel Indian."

**Product owner's decisive framing:** *"The first 5-10 seconds are critical — a visitor needs to quickly understand what problem Mela is solving and how it will help them."*

---

## Resolved diagnosis (PM ruling)

The real problem is **not** "the homepage is a catalog." It's that **the hero fails the value-prop test in the first 5-10 seconds — specifically the guaranteed cold-load hero (what renders BEFORE the async brand carousel arrives).** Everything below the fold is a distant second.

Acceptance framework = **UX-Design's three sequential questions:**

| Q | Current hero answer | Verdict |
|---|---|---|
| **1. What is this?** | h1 "Independent Indian Brands, Curated for Your Family" | Partial — copy names it, but the *visual* (teal gradient) says "clean baby SaaS" |
| **2. Why does it exist?** | *nothing* | **Missing entirely — THE core failure.** F-001's "no inspiration/how is this different from Amazon" = this gap. Mela never says why these brands are invisible in the US without it. |
| **3. What do I do here?** | CTA "Explore Brands" + 6 category pills | Contradictory — pills teach Amazon-style "search by department," undercutting the "curated" claim |

Three problems, shared P0 dependency:
- **F-001 → editorial voice / the "why" → P0** (the value prop; non-negotiable)
- **F-002 → visual orientation → P1 WITH A TRAP:** real symptom, wrong persona. Take the symptom (no instant orientation), REJECT the implied solution (big US-DTC lifestyle hero). Building for F-002 literally = generic exotic-India theme that alienates the diaspora core.
- **F-003 → visual coherence → P1 for the MINIMUM shift, P2 beyond.** "Feels Indian" is an outcome to test, NOT a spec. Explicitly refuse saffron/Devanagari/mandala clichés.

---

## Committed priority order (re-sorted by value-prop impact per unit risk, NOT by eng effort)

### TIER 0 — Fix the cold-load hero (the whole ballgame; ship as one coherent revision)
1. **Hero answers Q2 in one line** — promote the "why Mela exists / why these brands are invisible without us" message INTO the hero (not a separate scroll-down section). Absorbs old A2 + the *essence* of B1 (WhyIndia).
2. **Resolve the Q3 contradiction** — category pills vs. "curated." Either reframe pills with a curation label, or demote them below the primary discovery CTA.
3. **Hero must stand alone WITHOUT the carousel** — hard acceptance criterion. The most India-signaling element (brand carousel) loads async and is often still loading in the 5-10s window. Cold-load state must pass all 3 questions on a plain background, zero async content. Today it fails.

### TIER 1 — Minimum visual coherence + trust model (after Tier 0 locked)
4. **Trust-model callout** (old A3): "You browse here — then shop on each brand's own store." Cheap, resolves affiliate confusion.
5. **Minimum viable visual shift** — replace teal/aqua gradient with warmer register (CSS-only). NOT typography, NOT motifs yet.
6. **Remove ComingSoonSection** (old B4) — "coming soon" badge is a trust liability.

### TIER 2 — Below-fold architecture (mobile-driven; after Tier 0)
7. **Reorder brand stories above product grid** (old A1) — reframed as a MOBILE fix (rich content currently sits 2000-2500px down, invisible to mobile majority).
8. **Reduce product density** 8→4 (old A4) — supporting move, not headline.
9. **Full WhyIndia section** (old B1) — below-fold reinforcement of the hero's Q2 promise.

### TIER 3 — Needs validation/assets first; DO NOT build blind
10. **"Products look like US-store items"** (F-002) → INVESTIGATION task (see probes).
11. **Artisan story** (old B2) — blocked on real brand asset + permission; name owner + specific brand first.
12. **Indian-accent typography** (old C2) — only if testing still shows a coherence gap; high cliché risk; use **Hind** (Indian Type Foundry), NOT Tiro Devanagari (that's a Devanagari-script face, wrong for English display).
13. **Hero photography** (old C1) — deliberately deferred; the most dangerous F-002-driven bet. Validate direction before commissioning.

### SIDECAR — ship independently, no dependencies
- **A5 canonical URL fix** — `.env.development` has `REACT_APP_MARKETPLACE_ROOT_URL=https://mela-marketplace.onrender.com`; set to real prod domain (confirm domain w/ user). Do now.
- **C3 Sharetribe footer audit** — check Console for residual "© 2024 Your marketplace" / "Post a new listing" / Sharetribe social links. 2-min fix; live trust bug if present. Footer is loaded from Sharetribe Asset Delivery API, NOT in repo.

---

## Validate BEFORE building Tier 2-3 (cheap probes that resize the project)

1. **THE key question (resizes everything):** Does the page improve after the first scroll? Ask F-001: "Did you scroll past the hero? What did you see?" If yes-and-better → hero-only (Tier 0). If no → Tier 2 architecture justified. Cost: one text.
2. **Probe F-002's "US-store items" before any photography/curation spend.** Pull actual homepage carousel products, classify: (a) genuinely generic → curation fix; (b) Indian products shot Western-studio-style → photography fix; (c) cards stripped of origin context → card-design fix. Three different workstreams; can't action until we know which.
3. **Get an Arun (2nd-gen) reaction before any "make it feel Indian" visual work.** All 3 reviewers were 1st-gen/US-market; Arun is the primary conversion persona and most likely to DISTRUST heavy Indian visual coding. Run `/uxr personas`.
4. **Review the mockup before locking Tier 0 design** (blocked pending quarantine clear).

---

## Where the roles disagreed → PM rulings

1. **One problem or three?** → Three for *solutioning* (UXR wins), but sequenced so the P0 "why" does double duty; F-002/F-003 are partly downstream of it.
2. **WhyIndia = hero element or below-fold section?** → UX-Design wins. Split it: the *message* → hero (Tier 0); the *section* → below-fold (Tier 2).
3. **How hard to chase "feel Indian"?** → UXR wins on restraint. Minimum CSS-only shift now (Tier 1); typography/photography gated behind Arun validation (Tier 3). Cultural legibility without exoticization.
4. **Effort-sort vs impact-sort?** → Re-sorted by impact/risk; the cheap-but-critical hero "why" was mis-filed as "medium lift" in the old plan.

---

## Ground-truth code refs (verified this session)

- Hero: `web-client/src/containers/MelaHomePage/sections/HeroSection/HeroSection.js`
  - h1 default: "Independent Indian Brands, Curated for Your Family" (line ~140)
  - `TRUST_BADGES`: "Ships to All 50 States" / "US Cards Accepted" (line ~16)
  - `TOP_CATEGORY_PILLS`: 6 categories (line ~20)
  - CTA "Explore Brands" → BrandsPage (msg id `SectionMelaHero.shopNow`)
  - Cold-load / no-brands / fetch-error branches all render hero WITHOUT carousel — this is the fragile path
- Page container: `web-client/src/containers/MelaHomePage/MelaHomePage.js` (section order lives here)
- Category grid: `web-client/src/containers/MelaHomePage/sections/CategoryShowcase/CategoryShowcase.js` (8-per-carousel count constant to change for A4/Tier 2)
- Affiliate-precision rule (memory): never say brands are "not available in US" — say "hard to find" / "not carried in US stores."
