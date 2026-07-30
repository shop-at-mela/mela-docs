# Mela Social Accounts

## Active Accounts

### Pinterest
- **URL**: https://www.pinterest.com/shopatmela/
- **Handle**: @shopatmela
- **Status**: Active (warmup phase as of June 2026)
- **Posting cadence**: BLOCKED via Blotato API until warmup completes — Blotato hard-rejects Pinterest posts with a "warm up for 2 weeks, 1 pin/day manually, reconnect at 100+ views/month" error (confirmed 2026-07-24 via a real API call, not assumed). Until then, pins must be posted manually, directly in the Pinterest app, 1/day — **canonical in [`category-routing.yaml`](category-routing.yaml) → `cadence`** (scales to 5–10/day auto once the Catalog Feed ships)
- **Primary content**: Product pins (catalog API), brand boards, occasion collections
- **Conversion focus**: High ROI for Mela's product mix

### Instagram
- **URL**: https://www.instagram.com/shopatmela/
- **Handle**: @shopatmela
- **Status**: Active (warmup phase as of June 2026)
- **Posting cadence**: 3–4 standalone posts/week, at least 2 product-forward — **canonical in [`category-routing.yaml`](category-routing.yaml) → `cadence`**
- **Feed layout**: Theme-row grid is **deferred** (`category-routing.yaml` → `grid.enabled: false`) — reach (standalone posts optimized individually) is the higher-ROI use of production time until there's real profile-visit volume to navigate. See `grid.activation_gate` for the re-enable trigger.
- **Primary content**: Product-forward posts/Reels (real photos reused as motion where possible, brand-supplied footage), educational content, new arrivals Stories, seasonal posts
- **Trust focus**: Brand education and cultural authenticity layer

### Reddit
- **Status**: Participation-only (no account; human-posted in communities)
- **Communities**: r/IndiaMoms, r/AsianParenting, r/SustainableFashion, etc.
- **Cadence**: 3–5 quality interactions/week
- **Automation**: None — founder/team only
- **Full playbook**: see [`reddit-strategy.md`](reddit-strategy.md) for ground rules, participation modes, candidate subreddits, and how this ties into the AEO co-mention goal in `aeo-next-steps.md`

### TikTok
- **Status**: Deferred to Phase 2 (not yet launched)

---

## Account Management

**Credentials & API access**: Managed via Blotato MCP server
- Blotato handles account auth and token management
- `/social-review` skill calls `blotato_list_accounts` at publish time (Phase 6)
- For account updates or access issues, check Blotato MCP setup

---

## Brand Identity

- **Display name**: Mela | Brands from India
- **Logo**: See `/mela-docs/Mela logos/` for brand assets
- **Colors**: Navy #2D2D7B + marigold #F0A030
- **Tone**: Discovery-focused, authentic, never prescriptive

---

## Seasonal Calendar

Posts are queued 4 weeks before major events — **except Pinterest boards**, which need to be live earlier for search indexing lead time (Pinterest surfaces seasonal content weeks before the event itself, not on it):
- **Diwali**: October 1 — Pinterest board live by **mid-August** (~6-7 weeks out, not 4); Instagram content queue from Sept 1
- **Holi**: February 1 — Pinterest board live by **mid-December**; Instagram content queue from Jan 1
- **Mother's Day**: April 1 — Pinterest board live by **mid-February**; Instagram content queue from Mar 1
- **New Year**: December 1 — Pinterest board live by **mid-October**; Instagram content queue from Nov 1

---

## Blotato Integration

Mela uses Blotato for visual creation and publishing automation:
- Free plan (monthly budget)
- Image templates: Image Slideshow (`5903b592-1255-43b4-b9ac-f8ed7cbf6a5f/v1`), Product Scene Placement (`f524614b-ba01-448c-967a-ce518c52a700`)
- Canva for text/logo-only content (not Blotato)
- See `/social-review` Phase 3b for template details
