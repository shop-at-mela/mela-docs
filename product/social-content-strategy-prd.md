# Social Content Strategy, Plan & Automation
**Status:** Draft — Ready for Review  
**Last Updated:** June 2026  
**Owner:** Mela Product

---

## Problem

Mela's web experience is currently optimized for users who arrive with intent (search, category browse). The majority of the target audience — Sarah, Arun, and Priya — arrives without intent, needing inspiration before they can have purchase motivation. Social platforms (Pinterest, Instagram, Reddit) are where inspiration happens, but Mela has no systematic strategy for driving that inspiration traffic to the web app, and no automation to keep social content in sync with what's live on Mela.

The result: social presence requires constant manual effort to maintain, product/brand data on Mela isn't being leveraged as a content source, and new brand and product launches have no automatic social amplification.

---

## Background: Why Inspiration-First, Not Brand-First

Research and persona analysis (see [buyer-personas.md](../UXR/buyer-personas.md)) shows the audience splits by intent:

- **Neha** (first-gen immigrant) — brand-aware, arrives knowing what she wants
- **Sarah** (conscious American parent) — brand-unaware, arrives by attribute ("organic baby clothes")
- **Priya** (mixed heritage parent) — occasion-aware, arrives by moment ("Diwali gift for baby")
- **Arun** (second-gen) — brand-unaware and occasion-learning, needs aesthetic inspiration as entry point

Amazon/eBay are retrieval tools — you go knowing what you want. Mela's differentiation is that people come for inspiration. That means social should handle the top-of-funnel inspiration work and the web app should be the place that catches that inspired intent and converts it — not a parallel search engine.

**Competitive models that solved this:**
- **Wolf & Badger** (independent designer curation): editorial lives on-site, Instagram links to Journal posts
- **Not On The High Street**: occasion-first navigation, editorial gift guides
- **LTK**: social does inspiration, web app does conversion — job separation is the model
- **Etsy + Pinterest**: Pinterest is Etsy's highest-volume referral channel; catalog auto-sync does the work

---

## Goals

1. Make social content primarily auto-generated from Mela's existing product and brand data — not manually written from scratch.
2. Create a channel strategy where each platform has a defined job (top-of-funnel vs. trust vs. community) and content type.
3. Build a seasonal content calendar that runs without manual intervention for routine posts.
4. Establish Pinterest as the highest-ROI channel given the home/lifestyle/gifting category fit.
5. Ensure any change in Mela product data (new listing, new brand, price update) propagates to social automatically.

---

## Non-Goals

- Building a native social feed inside the Mela web app.
- Automating Reddit (requires authentic human participation — automation is harmful there).
- TikTok in Phase 1 (requires video production infrastructure not yet in place).
- Social commerce checkout integration (Pinterest "Buy" button, Instagram Shopping catalog checkout) — complex, deferred.

---

## Platform Strategy

### Pinterest — Primary Channel, Highest Automation

**Why:** Pinterest users are in discovery/inspiration mode, not purchase mode. Products in home, lifestyle, baby, gifting categories perform best here. Etsy drives significant revenue through Pinterest. Users clicking Pinterest pins have higher purchase intent than Instagram users. This is the lowest manual effort, highest conversion channel for Mela's product mix.

**Content types:**
- **Product Pins** (auto-synced from Mela catalog — see Automation section): product image + price + description + link to Mela listing.
- **Occasion Boards**: Curated boards for Diwali, New Baby, Modern Indian Nursery, Organic Baby Essentials, Heritage Gifting. Updated seasonally.
- **Styled collection images**: 5-product flat-lay or lifestyle imagery organized around a visual theme (not isolated product shots).

**Cadence:** 5–10 pins/day (automated from catalog sync). Manual board curation once per month.

**Link destinations:** Mela listing pages (for Product Pins) and Mela collection/category pages (for boards).

**Automation level:** 90% automated via Pinterest Catalog API.

---

### Instagram — Secondary Channel, Brand & Cultural Education

**Why:** Priya already discovers Indian items on Instagram. Arun follows Indian-American parenting accounts. Instagram is the trust-building layer — it tells the brand story behind the product that converts a browser to a buyer. Instagram engagement ≠ direct purchase; it builds the brand recognition that makes Mela web app visits convert.

**Content types:**
- **Brand Spotlight Carousels** (6–8 slides): Brand origin story, founder photo, 3 product highlights, link to Mela brand page. Semi-automated — template-filled from brand data.
- **Cultural Education Reels**: "What is a naming ceremony? Here's what families are gifting" / "Block printing: 500 years old, still made this way." Short, educational, shareable. Manual production, 2–3×/month.
- **New Arrivals Stories**: Auto-generated from new product listings. Template card: product image + price + "Now on Mela."
- **Occasion/seasonal posts**: Diwali countdown, Holi, New Year. Scheduled 4–6 weeks in advance.

**Cadence:** 4–5 posts/week (auto-generated Stories + weekly grid posts).

**Link destinations:** Link in bio rotates to the most relevant collection page for the current season. Individual posts deep-link to Mela brand pages via Stories.

**Automation level:** ~50%. Stories and new arrivals are auto-drafted. Reels and Brand Spotlight captions require human creative review before posting.

---

### Reddit — Trust Channel, Human-Only

**Why:** Neha and Priya are active in diaspora parenting communities (r/IndiaMoms, r/AsianParenting). Reddit trust is earned through authentic expertise. A single genuinely helpful answer about Indian baby certifications from "the Mela team" is worth more than 100 Instagram posts for this persona. Reddit penalizes promotional behavior severely — this channel requires patience and genuine contribution.

**Content types:**
- Helpful answers to questions about Indian baby brands, certifications, sizing, import, cultural context. Never promotional.
- AMA-style posts (once per quarter): "We curate Indian brands for US families — happy to answer questions."
- Resource links: only when directly relevant to an existing conversation.

**Cadence:** 3–5 quality community interactions per week.

**Automation:** None. This is founder/team time.

**Key subreddits:** r/IndiaMoms, r/AsianParenting, r/SustainableFashion, r/BabyBumps, r/EcoParenting, r/ZeroWaste, r/IndianFashion.

---

### TikTok — Phase 2 (Deferred)

Highest upside but requires consistent video production. Best angle: founder as face of brand, brand discovery storytelling ("This Indian brand has been making organic baby clothes for 40 years and nobody in the US knows about it"). Consider after Pinterest and Instagram are running at cadence.

---

## Automation Architecture

**Core principle: Mela's product and brand data is the content source. Social content is generated from that data, not created independently.**

### Trigger 1: New Product Listed → Pinterest Pin + Instagram Story

**When:** A listing goes live on Mela (state = published).

**Auto-action:**
1. **Pinterest:** Product pin created automatically via nightly Pinterest Catalog feed sync.
2. **Instagram:** Draft Story card generated (product image + price + "New on Mela" + swipe-up link). Placed in Buffer/Later "Pending Approval" queue.

**Data used:** title, primary image, price (USD), category, listing URL.  
**Manual step:** 5-second Instagram Story approval tap.

---

### Trigger 2: New Brand Goes Live → Brand Spotlight Package

**When:** A new brand account is marked active/featured on Mela.

**Auto-action:**
1. **Instagram:** Draft carousel generated from brand data (name, tagline, origin story, certifications, first 3 product images). Caption drafted via Claude API (see Phase 3). Pushed to Buffer pending queue.
2. **Pinterest:** Brand board created ("{Brand Name} | Mela") with first 10 products auto-pinned.
3. **Reddit:** Draft post text generated for reference — always human-posted.

**Data used:** `publicData.brandTagline`, `publicData.brandStory`, `publicData.brandMission`, `publicData.certifications`, `publicData.brandCity`, listing images.  
**Manual step:** Caption review + approve/edit in Buffer. Reddit post is always human-written.

---

### Trigger 3: Seasonal Calendar → Content Queue Population

**When:** 4 weeks before each seasonal event (hard-coded calendar).

| Season | Trigger date | Products sourced by |
|--------|-------------|-------------------|
| Diwali | Oct 1 | `pub_occasion=diwali-festivals` |
| New Year gifting | Dec 1 | `pub_occasion=gifting` |
| Mother's Day | Apr 1 | gifting + jewelry + home |
| New Baby (evergreen) | Monthly | newborn + 0-6 months |
| Holi | Feb 1 | fashion + art-craft |

**Auto-action:** Buffer queue populated with 12–16 drafted posts for the season. Team receives Slack/email notification: "Your Diwali content queue is ready — review and approve."

**Manual step:** 30-minute seasonal queue review + approve in Buffer.

---

### Trigger 4: Price or Availability Change → Pinterest Pin Update

**When:** A listing price changes or stock drops to 0.

**Auto-action:** Pinterest catalog feed updated on next nightly sync. Pins automatically reflect new price. Out-of-stock listings removed from catalog automatically.

**Manual step:** None.

---

## Sync Summary Table

| Change on Mela | Auto-action on Social | Manual step |
|---------------|----------------------|-------------|
| New product listed | Pinterest pin created (nightly) + Instagram Story drafted | 5-sec Instagram approve |
| Product price changes | Pinterest pin updated (nightly) | None |
| Product out of stock | Pinterest pin removed (nightly) | None |
| New brand goes live | Pinterest brand board + IG carousel drafted | Caption review + approve |
| Seasonal event (4 wks out) | Content queue populated (~12 posts) | 30-min queue review |
| Daily (no trigger) | Catalog pins kept current | None |

---

## Content Calendar (Recurring)

| Week | Pinterest (auto) | Instagram (semi-auto) | Reddit (human) |
|------|-----------------|----------------------|----------------|
| W1 | Catalog sync daily | Brand Spotlight carousel | 1–2 community answers |
| W2 | Catalog sync daily | New Arrivals Story batch | 1–2 community answers |
| W3 | Catalog sync daily | Cultural Education Reel | AMA prep or Q&A |
| W4 | Catalog sync daily | Occasion/seasonal post | 1–2 community answers |

**Monthly manual effort target:** ≤ 3 hours.
- Instagram content review + approve: 45 min
- Brand Spotlight caption editing: 30 min
- Reddit community participation: 30–45 min/week
- Seasonal queue review: 30 min/month

---

## Technical Implementation Plan

### Phase 1 — Pinterest Catalog Feed (Weeks 1–2)
**Engineering work required.**

Add a server-side route at `/feeds/pinterest` in the Mela web-client that:
1. Queries all active Sharetribe listings via the SDK (integration pattern already used in CategoryShowcase).
2. Returns a Pinterest-compatible XML catalog with fields: `id`, `title`, `description`, `link`, `image_link`, `price`, `availability`, `condition`, `brand`, `product_type`.
3. Runs as a publicly accessible, cache-friendly endpoint (no auth required).

Register the feed URL in Pinterest Catalog Manager. Pinterest syncs nightly. Product Pins auto-create.

**Effort:** 2–3 days engineering.

---

### Phase 2 — Scheduling Tool Setup (Week 2–3)
**No engineering required.**

1. Create Buffer (Essentials plan) or Later account.
2. Connect Instagram Business account + Pinterest Business account.
3. Set up draft → approval workflow: all auto-generated posts land in "Pending" queue, not auto-published.
4. Connect Buffer to Zapier/Make (Phase 3).

**Effort:** 1 day setup.

---

### Phase 3 — Automation Triggers via Zapier/Make (Weeks 3–4)
**Light engineering required.**

- **New listing trigger:** Sharetribe API polling (every 15 min) for newly published listings → fetch listing data → populate Instagram Story template via Canva API or image template → push draft to Buffer queue → Slack notification.
- **New brand trigger:** Poll for new featured user accounts → fetch brand profile data → call Claude API with brand story/tagline/certifications to generate Instagram carousel caption → push to Buffer + create Pinterest board via Pinterest API.

**Claude API caption prompt pattern:**
```
You are writing an Instagram carousel caption for Mela, a curated marketplace for Indian brands.
Brand: {brandName} from {brandCity}
Story: {brandStory}
Mission: {brandMission}
Certifications: {certifications}
Top products: {productTitles}

Write a 3–4 sentence Instagram caption that:
- Leads with the brand story/origin (not "introducing")
- Mentions 1 certification if present
- Ends with "Discover {brandName} on Mela →"
- Follows the Indian Anchoring Principle: describe the product's cultural origin, never the user's identity
```

**Effort:** 3–5 days (Zapier/Make setup + API connections + Claude integration).

---

### Phase 4 — Seasonal Calendar Automation (Weeks 4–5)
**Light engineering required.**

A scheduled script (cron, runs monthly) that:
1. Checks the hardcoded seasonal event calendar.
2. If an event is 4 weeks out, queries Sharetribe for relevant listings by occasion tag.
3. Generates draft content (caption + image selection) for each post in the season.
4. Pushes the full queue to Buffer with pre-scheduled post times spread over the 4-week window.
5. Sends a Slack/email digest: "Diwali queue ready: 12 posts, Oct 1–31. Review at [Buffer link]."

**Effort:** 2–3 days engineering.

---

## Tool Stack & Cost

| Tool | Role | Monthly cost |
|------|------|-------------|
| Pinterest Business | Product catalog, pin management | Free |
| Buffer (Essentials) | Scheduling, approval queue, analytics | $6–18 |
| Zapier (Starter) or Make (Core) | Automation triggers | $20–29 |
| Anthropic API (Claude) | Caption generation from brand data | ~$5–10 (pay-per-use) |
| Canva (Pro) | Instagram carousel templates, brand spotlight images | $13 |

**Total monthly cost:** ~$44–70  
**Total setup engineering effort:** ~8–12 days  
**Ongoing manual effort:** ~2–3 hours/week

---

## Success Metrics

**Months 1–3 (setup complete):**
- Pinterest catalog feed live and syncing daily ✓
- Buffer approval workflow active ✓
- First 5 brand spotlights published to Instagram ✓

**Months 3–6 (early traction):**
- Pinterest monthly impressions > 50K
- Pinterest referral traffic to Mela > 5% of total sessions (GA4)
- Instagram Reels average profile visits > 1K/month

**Months 6–12 (validation):**
- Social referral sessions have higher avg. time-on-site than direct/organic (confirms inspiration intent is landing)
- At least one non-Neha persona (Sarah or Arun) is converting through social referral path
- Manual content production time confirmed ≤ 3 hours/week

---

*Informed by: Mela buyer personas (April 2026), competitive analysis of Wolf & Badger, Not On The High Street, Net-a-Porter, Glossier, LTK, Etsy/Pinterest integration patterns.*
