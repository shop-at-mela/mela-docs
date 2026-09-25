# Homepage FAQ + GEO Signals PRD

**Document Owner:** Product / SEO Team  
**Last Updated:** 2026-09-25  
**Status:** In progress — engineering underway in parallel with category-page GEO work  
**Priority:** Medium — small, well-scoped AI-answer-engine visibility fix  
**Related PRDs:** `seo-aeo-category-brand-pages-prd.md` (sibling; sets the shared date/authorship convention), `homepage-hero-prd.md`, `homepage-redesign-prd.md`

---

## Executive Summary

**Feature:** Show the homepage's existing FAQ as visible content, and add the same last-reviewed date and Organization byline used on category pages.  
**Target URL / Entry Point:** `/`, rendered by `MelaHomePage` (`src/containers/MelaHomePage/MelaHomePage.js`)  
**Target Users:** First-time US visitors with practical doubts (shipping, payment, duties, returns), plus AI answer engines (Perplexity, ChatGPT Search, Gemini, Google AI Overviews) that quote visible passages.  
**Business Objective:** Make the homepage a quotable source for "can I buy Indian brands from the US?" questions, and answer the most common pre-purchase doubts on the page itself.

**Primary Success Metrics:**
- The homepage passes the GEO audit on all four checks: a 40+ word passage in the first third, a question-form heading, a published/updated date, and an authorship signal
- AI-engine referrals to `/` (`perplexity.ai`, `chatgpt.com`, `gemini.google.com`): establish a baseline, then track the trend
- `homepage_faq_expand` interactions: establish a baseline (if the accordion pattern is used)

---

## 1. Problem Statement

### Current State

`MelaHomePage.js` already emits a 5-question `FAQPage` JSON-LD block through the `Page` `schema` prop. It covers US shipping, US credit cards, customs duties, returns, and shipping time. **None of it appears on the page.** The questions and answers exist only inside `<script type="application/ld+json">`.

A GEO audit of `/` found:

| Gap | Current homepage state |
|-----|------------------------|
| No self-contained 40+ word passage in the first third of the page | Hero and VettingStrip are short marketing lines, not quotable answers |
| No question-form heading | No `<h2>`/`<h3>` phrased as a question anywhere on the page |
| No published/last-updated date | `Page` supports `published`/`updated` props, but the homepage never passes them |
| No author byline or Person/Organization attribution | The global Organization entity exists in `@graph`, but nothing on the page references it as author/publisher |

### Why It Matters

- **Invisible FAQ = wasted asset.** AI engines weight visible text. Google's structured-data guidelines also say FAQ markup should match content users can see. Markup with no visible counterpart gives little benefit and is a policy risk.
- **The answers are good content.** "Can I use my US credit card?" and "Do brands ship to the US?" are the practical doubts that first-time visitors (Sarah, Arun) and AI engines both have. Showing them costs no new copy.
- **Consistency with category pages.** The category pages are getting dated, bylined, question-led content in the same effort. An undated, unattributed homepage would be the weakest page on the site.

---

## 2. Goals & Non-Goals

### Goals

1. **Visible FAQ section** that renders the 5 existing Q&As as real `<h2>`/`<h3>` + `<p>` content.
2. **One source of truth.** The visible FAQ and the `FAQPage` JSON-LD are generated from the same data array, so they can't drift apart.
3. **Last-reviewed date**, passed through `Page`'s existing `published`/`updated` props (→ `article:published_time` / `article:modified_time`).
4. **Organization byline + attribution** that matches the category-page pattern.

### Non-Goals

- New FAQ questions or rewritten answers, except for the factual accuracy check in §5.
- Any change to hero, carousel, module order, or visual redesign beyond inserting this one section.

---

## 3. Shared Convention (defined in sibling PRD)

The date and authorship rules are **defined in `seo-aeo-category-brand-pages-prd.md`** (Build Status Summary, §7 AEO Implementation Checklist, §9 Acceptance Criteria). This PRD adopts them unchanged:

- **Date:** a hand-maintained "content last reviewed" date, bumped only when this page's copy changes. It is never derived from listing data, deploy time, or `Date.now()`, because that pattern is freshness spam.
- **Authorship:** a visible "Curated by the Mela team" byline, plus schema.org `author`/`publisher` references to the Organization entity that `Page.js` already injects (`@id: ${marketplaceRootURL}#organization`). No named author persona and no new entity.

If the convention changes, change it in the sibling PRD first, then update both pages.

---

## 4. Requirements

### 4A — `FAQSection` component (P0)

- New component: `src/containers/MelaHomePage/sections/FAQSection/FAQSection.js` + `FAQSection.module.css`, following the existing `sections/*` pattern (`VettingStrip`, `BrandSpotlight`, etc.).
- **Data:** move the 5 Q&As out of the inline `schema` literal into one exported array (e.g. `homepageFaqs` as `{ question, answer }` objects) in the `FAQSection` folder. `MelaHomePage.js` builds the `FAQPage` JSON-LD `mainEntity` by mapping over this same array. **No Q&A text may be duplicated between the component and the schema.**
- **Markup:**
  - Section heading: `<h2>` (e.g. "Common questions about shopping Indian brands from the US").
  - Each question: `<h3>` phrased as a question, followed by its answer in a `<p>`.
  - The answer text must be in the server-rendered HTML. If an accordion is used, collapsed answers must stay in the DOM (CSS-hidden, not conditionally rendered), matching the sibling PRD's "server-rendered, not client-only" rule for FAQs.
- **Byline:** "Curated by the Mela team · Last reviewed {Month YYYY}" renders at the foot of the section, using the same date value passed to `Page`.

### 4B — Placement (P0)

- Insert `<FAQSection />` in `MelaHomePage.js` **directly after `<VettingStrip vettingSectionId="how-we-vet" />`**. It lands before `BrandSpotlight`, which puts the first 40+ word answer inside the first third of the page.
- `SavedItemsModule` (shown only to signed-in users with saves) currently sits between VettingStrip and BrandSpotlight. `FAQSection` goes **above** it, so logged-out visitors and crawlers see the same order.

### 4C — Schema & meta (P0)

- `FAQPage` JSON-LD: same 5 questions, generated from the shared array (§4A).
- `Page` receives `published` and `updated` props from a hand-maintained constant (e.g. `HOMEPAGE_CONTENT_REVIEWED = '2026-09-25'`) kept next to the FAQ data.
- The `WebPage` JSON-LD node gets `author` and `publisher` set to `{ "@id": "${marketplaceRootURL}#organization" }`, following the sibling PRD's convention.

### 4D — Analytics (P2)

- If an accordion is used: `faq_expand` with `{ page_type: 'homepage', question_index }`, the same event the sibling PRD defines.

---

## 5. Risks

| Risk | Mitigation |
|------|------------|
| **Stale facts become visible.** The duties answer cites a US de minimis threshold of $800. US de minimis rules for imports changed in 2025, so this is likely out of date. Once the answer is visible, Mela is making the claim in front of users. | **Pre-ship copy check (blocking):** PM verifies each of the 5 answers against current US CBP rules and brand policies before the section goes live, then sets the last-reviewed date. |
| Visible FAQ and schema drift apart after later edits | Single data array (§4A). Unit test asserts that JSON-LD `mainEntity` equals the rendered questions. |
| Freshness spam (date auto-bumped) | Date is a hand-edited constant; code review rejects any computed date. |
| Section adds scroll depth above product modules | Compact styling; accordion option. UX to confirm at 375px. |

---

## 6. Acceptance Criteria

- [ ] `FAQSection` exists at `src/containers/MelaHomePage/sections/FAQSection/FAQSection.js` and renders on `/`.
- [ ] `FAQSection` renders directly after `VettingStrip` and before `SavedItemsModule`/`BrandSpotlight`.
- [ ] The section has one `<h2>` heading and one question-form `<h3>` per Q&A, with the answer as visible text.
- [ ] All 5 answers are present in the server-rendered HTML (view-source), including any collapsed accordion items.
- [ ] Visible Q&A text and `FAQPage` JSON-LD `mainEntity` come from the same data array; a unit test fails if they differ.
- [ ] `<head>` contains `article:published_time` and `article:modified_time` from a hand-maintained constant (not computed).
- [ ] A visible "Curated by the Mela team" byline with the last-reviewed date renders in the section.
- [ ] Homepage JSON-LD includes `author` and `publisher` references to `{marketplaceRootURL}#organization`, and no new Person/Organization entity is added.
- [ ] All 5 answers have been fact-checked against current US import/duty rules before launch (§5).
- [ ] Google Rich Results Test shows valid `FAQPage` with no errors on `/`.
- [ ] Mobile: section is readable and doesn't break layout at 375px.

---

## 7. Out of Scope

- **Category and brand pages:** covered by `seo-aeo-category-brand-pages-prd.md`.
- **Hero, carousel, and module layout/redesign:** covered by `homepage-hero-prd.md` and `homepage-redesign-prd.md`.
- New FAQ content or a CMS-driven FAQ; the current 5 Q&As stay config-in-code.
- Named author personas or Person schema (rejected in the sibling PRD's convention).
