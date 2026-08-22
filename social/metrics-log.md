# Mela Social Metrics Log

The Sunday tracking sheet referenced by `cold-start-checklist.md` — didn't exist until 2026-07-13. Fill this in every Sunday review; by Week 3 the pattern (which categories/brands/formats win) should drive brand selection.

**Two data sources, don't conflate them:**
- **Blotato dashboard** (saves, clicks, comments, reach) — engagement-side. Shows whether content resonates on-platform.
- **GA4, filtered by `utm_campaign`** (per `category-routing.yaml` → `tracking`) — shows whether a click became an actual Mela session. This only works from the first campaign that ships with UTM-tagged URLs onward; nothing before 2026-07-13 is measurable this way.

## Log

**Warmup capture discipline (`pre-publish-gate.md` Step 3):** the 13-dimension pre-publish *scoring* is deferred until a baseline exists — but the raw **north-star metric is captured from post #1** so the baseline actually accumulates. IG = **saves**, Pinterest = **outbound clicks**. Log each post's **hypothesis** (the one line it was testing) here too, so the eventual score→performance correlation has something to read. You cannot retroactively score posts whose metrics were never captured — that's why capture starts now even though scoring doesn't.

| Date | Post | Platform | Category | Hypothesis (angle/hook/persona) | Saves | Clicks | Comments | GA4 sessions (UTM) | Notes |
|------|------|----------|----------|----------------------------------|-------|--------|----------|---------------------|-------|

## Monthly top-performer teardown

The monthly hook/format teardown (`hook-engineering.md` §6). `/social-launch` Phase 0b flags this if the latest entry is >30 days old. Each row: the date run, the 5 refreshed content angles (or "unchanged"), and the winning hooks added to the swipe file.

| Date | Niche surfaces scanned | Refreshed 5 angles? | Promote / kill decisions (hooks + angles) |
|------|------------------------|---------------------|-------------------------------------------|
| 2026-08-16 | Directional niche scan (no own-account baseline yet): IG Reels + web + Reddit — Indian craft/D2C hooks, r/ABCDesis diaspora/suitcase threads, conscious-parenting + sustainable-fashion "how to tell" reels, "first Diwali" hosting demand. | Angles unchanged (§5's 5 hold); belonging #1 + certs #4 + occasion #5 all confirmed live in-niche. | **Promote/kill: none** (no baseline — directional only per §6). **Seeded 5 new §2-safe hook hypotheses** into §7 (suitcase-economy, GOTS/OEKO-TEX cert decode, inside-out seam teardown, discovery wedge, first-Diwali hosting). Format signal: "here's why" open loop + specific number in first ~1.5s + seam-teardown reel skeleton. |

### Hook & angle scoring (promote / kill thresholds)

The teardown scores **our own** posts against the account's rolling baseline (not gut feel) — this is the single definition referenced by `hook-engineering.md` §6 and `/social-launch` Phase 0b. Thresholds are **relative to baseline** because absolute counts are meaningless on a warmup account. Signals: **reach/impressions** + **3-second view rate** (reels) + **save/share rate** from Blotato/IG Insights; **profile taps / link CTR** from GA4 `utm_campaign` sessions.

| Signal | Promote hypothesis → *proven* | Kill / retire |
|---|---|---|
| Reach vs. trailing-30-day median | ≥ 1.5× across ≥ 2 posts | ≤ 0.6× across ≥ 3 posts |
| 3-sec view rate (reels) | Top third of the month's reels | Bottom third, 2 months running |
| Save + share rate | Above account median | Consistently below |
| Profile taps / link CTR (GA4) | Any angle that drives sessions | Zero sessions after ≥ 3 fair tries |

**No baseline yet = promote nothing.** Until the account has a few weeks of posts, §7 stays entirely hypotheses and the teardown is directional only. A swipe-file line is a *hypothesis* until it clears a promote row on real posts; an *angle* is retired or reframed if it hits a kill row across a fair sample.
