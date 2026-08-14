# Mela Social Metrics Log

The Sunday tracking sheet referenced by `cold-start-checklist.md` — didn't exist until 2026-07-13. Fill this in every Sunday review; by Week 3 the pattern (which categories/brands/formats win) should drive brand selection.

**Two data sources, don't conflate them:**
- **Blotato dashboard** (saves, clicks, comments, reach) — engagement-side. Shows whether content resonates on-platform.
- **GA4, filtered by `utm_campaign`** (per `category-routing.yaml` → `tracking`) — shows whether a click became an actual Mela session. This only works from the first campaign that ships with UTM-tagged URLs onward; nothing before 2026-07-13 is measurable this way.

## Log

| Date | Post | Platform | Category | Saves | Clicks | Comments | GA4 sessions (UTM) | Notes |
|------|------|----------|----------|-------|--------|----------|---------------------|-------|

## Monthly top-performer teardown

The monthly hook/format teardown (`hook-engineering.md` §6). `/social-launch` Phase 0b flags this if the latest entry is >30 days old. Each row: the date run, the 5 refreshed content angles (or "unchanged"), and the winning hooks added to the swipe file.

| Date | Niche surfaces scanned | Refreshed 5 angles? | Promote / kill decisions (hooks + angles) |
|------|------------------------|---------------------|-------------------------------------------|
| _(none yet — first teardown pending)_ | | | |

### Hook & angle scoring (promote / kill thresholds)

The teardown scores **our own** posts against the account's rolling baseline (not gut feel) — this is the single definition referenced by `hook-engineering.md` §6 and `/social-launch` Phase 0b. Thresholds are **relative to baseline** because absolute counts are meaningless on a warmup account. Signals: **reach/impressions** + **3-second view rate** (reels) + **save/share rate** from Blotato/IG Insights; **profile taps / link CTR** from GA4 `utm_campaign` sessions.

| Signal | Promote hypothesis → *proven* | Kill / retire |
|---|---|---|
| Reach vs. trailing-30-day median | ≥ 1.5× across ≥ 2 posts | ≤ 0.6× across ≥ 3 posts |
| 3-sec view rate (reels) | Top third of the month's reels | Bottom third, 2 months running |
| Save + share rate | Above account median | Consistently below |
| Profile taps / link CTR (GA4) | Any angle that drives sessions | Zero sessions after ≥ 3 fair tries |

**No baseline yet = promote nothing.** Until the account has a few weeks of posts, §7 stays entirely hypotheses and the teardown is directional only. A swipe-file line is a *hypothesis* until it clears a promote row on real posts; an *angle* is retired or reframed if it hits a kill row across a fair sample.
