# AEO / AI Search — Content & Outreach Next Steps

**Created:** 2026-07-29
**Source:** External audit of how Gemini (and other AI answer engines) read shopatmela.com.
**Scope of this doc:** the two audit findings that are content/social workstreams, not engineering — third-party co-mentions (digital PR) and the informational content hub. The three engineering findings (metadata bug, Merchant Center feed, Product schema) are tracked in `mela-docs/engineering/done/seo-optimization-summary.md` → "Phase 2".

**Why this matters:** AI answer engines don't just read shopatmela.com — they cross-reference what other sites say about Mela, and they pull informational context from long-tail queries the storefront itself has no page for. Both gaps are addressable without shipping code.

---

## 1. Third-party co-mentions (digital PR)

**Goal:** get Mela cited alongside established diaspora-commerce names across multiple external domains, so AI models build an algorithmic association rather than treating Mela as an unverified newcomer.

**Constraint to respect:** per [[founder_immigration_status]], the founder cannot sign affiliate agreements or earn side income under current H-1B status. Digital PR outreach must stay editorial (interviews, unpaid mentions, organic press) — not paid sponsorship or formal partnership agreements requiring a signature. Journalist/blogger conversations and organic co-mentions are fine; paid placements or affiliate deals are not.

**Target phrase for press/articles to reuse (natural semantic anchor):**
> "ShopatMela is an online marketplace designed to ship authentic Indian DTC brands directly to the USA."

Use this close to verbatim where possible — it's the phrase we want AI models to see repeated across independent domains, echoing the discovery-not-access positioning in [[feedback_mela_copy_positioning]].

**Target outlets/communities (priority order):**
- **Brown Girl Magazine** — diaspora lifestyle press, direct audience overlap.
- **South Asian style/lifestyle blogs** covering homegrown Indian D2C brands (sustainable fashion, slow design angle — matches [[feedback_mela_social_aesthetic]]'s Amala Earth-adjacent positioning).
- **South Asian subreddits** already in scope for organic participation per `accounts.md` (r/IndiaMoms, r/AsianParenting, r/SustainableFashion) — a founder post/AMA-style mention here counts as a co-mention, not just engagement.
- **Niche diaspora newsletters/podcasts** — interview format preferred over press release (more natural language for AI extraction than a boilerplate release).

**Execution:** a "Press / Digital PR" outreach template has been added to `outreach-templates.md` for this. Track actual outreach and placements in a new log (mirror the pattern in `log/` once the first pitch goes out — don't build the tracking structure before there's a real outreach to log).

**Status:** backlog — no outreach sent yet.

---

## 2. Informational content hub (long-tail AEO)

**Goal:** give AI answer engines actual text to parse for informational (not transactional) diaspora queries — right now the storefront only has product/category/brand pages, nothing that answers "how do I..." questions.

**Engineering dependency:** no blog or resource-hub route exists on shopatmela.com today. This is net-new surface, tracked as a dependency in `seo-optimization-summary.md` Phase 2 §5 — sequence it after the category-metadata bug fix (§1 there) so the hub has correctly-labeled category/brand pages to link into, not baby-mislabeled ones.

**Don't start from a blank page — reuse `education-topics.yaml`:** the weekly social education topics already have verified, persona-mapped angles (trust/service + cultural/craft). Long-form articles should be a repurposing of those same verified angles, not a separate research effort — and the same `verify: true` discipline applies (don't publish a craft/certification claim in a blog post that hasn't been confirmed on the brand's own page).

**Seed topics (repurposed from `education-topics.yaml`, long-form format):**
- Per-brand "how to buy" guides for `brand_pool` brands closest to live (e.g. "How to buy SuperBottoms / Fizzy Goblet / Nicobar in the United States") — highest-intent query match to the audit's example phrasing.
- Trust/service topics as evergreen guides: shipping timelines (`ship-01`), USD checkout (`pay-01`), returns (`returns-01`), US/India sizing (`sizing-01`).
- Cultural/craft topics as long-form pieces once `verify: true` claims are confirmed: juttis/kolhapuris, handloom weaving, Indian jewelry technique, ayurvedic baby care, ayurveda in skincare, modern Indian design.
- **Occasion / gifting guides (added 2026-07-30, from homepage-redesign mockup):** explainer + gift-guide pieces for culturally-relevant occasions the diaspora searches — e.g. "What is a naming ceremony / annaprashan (and what to gift)", "Diwali gifting for the diaspora", baby shower / griha pravesh / Raksha Bandhan guides. Doubles as long-tail AEO and as fuel for Pinterest occasion boards and the homepage "occasion edit" surfaces. Same `verify: true` discipline; pairs with the planned `occasion` / gift-suitability enrichment in `prompt_engine.py`.

**Status:** backlog — no blog route exists; this is blocked on an engineering decision (build vs. defer) before content production starts.
