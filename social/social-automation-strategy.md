# Social Automation Strategy — Lightweight Weekly Loop

**Created:** 2026-09-29 · **Owner:** founder · **Status:** approved direction, not yet built
**Decision mode:** park-for-approval · native Claude Code routine + phone notification · weekly batch, 2-week Blotato queue depth (founder-confirmed 2026-09-29)

This doc is self-contained and executable cold in a fresh session. It supersedes ad-hoc "just run
`/social-launch` when I remember" as the operating model. It does **not** change the content rules —
those still live in their canonical homes (`category-routing.yaml`, `visual-style-guide.md`,
`hook-engineering.md`, `pre-publish-gate.md`, the two skills). This is the *trigger + queue* layer
wrapped around them.

---

## 1. The problem, stated precisely

The pipeline is not slow — it is **un-triggered**.

- `/social-launch` already batches a full week at once; Blotato already schedules posts days ahead.
- So the ~3-week silence (last batch shipped 2026-09-06/07, nothing since) was **one missed batch
  session**, not 21 missed posts.
- Root cause: the whole workflow (7 phases, ~6 human gates, plus manual IG reel steps) sits behind
  *the founder personally sitting down and driving a long interactive session*. When busy, that
  session never starts, and there is no queue depth to coast on.

**The fix is not "post automatically." It is: move the labor off the founder, keep the approval,
and hold a buffer so a missed week degrades gracefully.**

---

## 2. Design principles (first-principles)

1. **Separate labor from approval.** ~90% of `/social-review` is un-gated grunt work a machine
   should do unattended: read logs, run freshness/cooldown checks, resolve routing, render Blotato
   visuals, write captions + alt text + UTMs, run the pre-publish gate. Only **approve+publish** and
   **wife grid-review** genuinely need a human.
2. **Machine proposes, founder disposes.** The automated run stops at a finished Review Sheet and
   pushes a notification. Nothing reaches an account until the founder approves. (`Never auto-publish`
   from both skills is preserved exactly.)
3. **Queue depth is the shock absorber.** Always keep ~2 weeks staged in Blotato so one missed
   approval week never = silence. This is the single change that would have prevented the 3-week gap.
4. **Carousels-only during warmup kills the manual steps.** Blotato publishes IG carousels fully via
   API. Reels are the *only* format that forces the founder back into manual IG work (audio, cover,
   publish). The founder already made carousels the default (2026-09-05, memory
   `[[feedback_ig_multiproduct_carousel_default]]`), so lean all the way in while automating: **no
   reels in the automated lane.** Reels remain a deliberate, manual, occasional exception outside this loop.
5. **Reuse what exists.** The skills, Blotato MCP, logs, and auto-memory are already wired into Claude
   Code. The automation layer is a scheduled cron around them — no new pipeline, no new infra for Phase 1.

---

## 3. What gets automated vs. what stays human

| Step (maps to skill phases) | Who | Notes |
|---|---|---|
| Read all logs, build history/observation/recency indexes | **Auto** | `/social-launch` Phase 0 |
| Teardown-freshness check | **Auto** (flags only) | Phase 0b — flags if stale, still runs the batch |
| Brand + product + education-topic selection | **Auto (proposes)** | Phase 1 — picks candidates, founder confirms in the one approval |
| Listing-live verification (`shopatmela.com/l/{id}` open?) | **Auto** | Hard gate; drops unverified products before they reach the sheet |
| Cooldown / rotation / category-concentration checks | **Auto** | Phase 2 — result shown on the sheet, never silent |
| Blotato visuals (Product Scene / real-photo + watermark) | **Auto** | Phase 3b — carousels only; morph-QC notes surfaced on sheet |
| Captions + alt text + UTMs + persona lead | **Auto** | Phase 3a/3c |
| Pre-publish gate (blocking hard-fails + coaching notes) | **Auto** | Phase 5b — a hard-fail tile is dropped/flagged, never shipped |
| **Build Review Sheet + grid preview, push notification** | **Auto** | The parking point — run ends here |
| **Founder approve / "redo tile N" / edit** | **HUMAN** | ~2 min on phone in a short Claude session |
| **Wife grid-shape sign-off** | **HUMAN** | `/social-launch` Phase 4 — mandatory, unchanged |
| Schedule approved batch into Blotato (prev+24h) | **Auto (post-approval)** | Phase 6 |
| Log campaign YAML + hypothesis + northstar metric | **Auto** | Phase 7 |
| Attach clean scenes to listings (P1 scent-match) | **Auto** | Phase 7b |

The founder's job shrinks from "run the production line" to "approve a finished sheet." Everything
above the two HUMAN rows happens unattended.

---

## 4. Architecture

```
  WEEKLY CRON  (native Claude Code routine, runs in the cloud, unattended)
      │  runs /social-launch Phases 0–3 + pre-publish gate for the whole batch
      │  carousels only · listing-live verified · cooldown checked · gate-passed
      ▼
  STAGED REVIEW SHEET written to mela-docs/social/staging/  +  PUSH NOTIFICATION
      │  (visuals + captions + alt + UTMs + grid ASCII preview, all hard-fails already dropped)
      ▼
  FOUNDER  — short session:  "approve"  ·  "redo tile 3"  ·  quick caption edit
  WIFE     — grid-shape sign-off (feed reads as intended)
      │
      ▼
  SCHEDULE INTO BLOTATO 1–2 weeks out (prev+24h)  ──►  Blotato auto-publishes carousels via API
      │
      ▼
  LOG (campaign YAML, hypothesis, northstar) + attach clean scenes to listings
```

**Why the run "parks" instead of finishing the publish:** a cron cloud agent runs to completion and
ends — it cannot truly block mid-run waiting for a human. So the run's *deliverable* is the staged
sheet + notification, not published posts. Scheduling-into-Blotato is a separate, tiny, human-approved
step. This is what makes "park for approval" real rather than a promise the runtime can't keep.

---

## 5. Queue-depth mechanic (the anti-silence guarantee)

- Blotato holds the live queue. The routine's job each week is to **top the queue back up to ~14 days
  of scheduled posts.**
- Each run first reads what's already scheduled in Blotato (`blotato_list_schedules` /
  `blotato_get_schedule`), computes the gap to the 14-day horizon, and only builds enough tiles to
  refill it. No double-booking, no over-production.
- Effect: if the founder misses one week's approval, there is still ~1 week of runway already live.
  Two misses before it goes quiet. The 3-week-silence failure mode becomes structurally impossible
  unless the founder ignores 2+ consecutive notifications.

---

## 6. Tool comparison (the "how to trigger it" question)

**Native Claude Code Routines / scheduled cloud agents — CHOSEN for Phase 1.**
Runs the *actual existing skills* with full repo context, the Blotato MCP, the logs, and auto-memory
already wired. Zero new infrastructure. Cron'd weekly; pushes a notification when the sheet is staged.
Lowest-effort path by a wide margin because the pipeline already lives in Claude Code. Set up via the
`schedule` skill (routine) + `PushNotification` for the ping.

**Block's Buzz — Phase 2 upgrade path, not now.**
A shared human+agent workspace that ships event triggers on day one (message / reaction / schedule /
webhook) and can host **Claude Code itself** as the agent. Its real advantage is *where the approval
lives*: a chat room the founder already checks, where "approve" / "redo tile 3" is a message instead
of opening a terminal — a genuinely better mobile approval surface. Cost: new surface to set up and
maintain. Adopt only after the native loop is proven and the friction that remains is specifically the
approval-surface friction. (Refs: block.xyz/inside/introducing-buzz, github.com/block/buzz)

**Zavi / Praxis fleet — feeder, not pipeline.**
The fleet is draft/approval-gated *strategy* agents (`growth-lead`, `cgo`, `content-design`,
`performance-marketer`, `browser-operator`). There is **no social-publish agent**, and driving Blotato
by hand through `browser-operator` would be brittle overkill vs. the Blotato MCP already in Claude Code.
Best role: `growth-lead` / `cgo` as an **upstream idea/signal source** — what's converting, what to post
about — feeding topic/brand selection. Not the trigger, not the publisher.

---

## 7. Rollout

**Phase 0 — Immediate unblock (this week, manual).**
Run `/social-launch` once now to refill the queue to 14 days and end the silence. Don't wait for the
automation to be built.

**Phase 1 — The native automated loop (target: within 1–2 weeks).**
1. Add a `carousels_only_automated_lane: true` note to `category-routing.yaml` (or a small
   `automation:` block) so the skill knows the automated run skips reels. Document that reels are a
   manual out-of-loop exception.
2. Add a queue-depth check to `/social-launch` Phase 0/2: read Blotato's current schedule, target the
   14-day horizon, build only the gap.
3. Add a staging output: `/social-launch` writes the Review Sheet + grid preview to
   `mela-docs/social/staging/week-of-<date>.md` and stops before scheduling when run in "staged" mode.
4. Create the weekly routine via the `schedule` skill: run `/social-launch` in staged mode, then
   `PushNotification` the founder with a one-line summary + the staging file path.
5. Create a tiny `/social-approve` flow (or just a documented kickoff prompt) for the 2-minute human
   session: read the staging sheet → apply any "redo tile N" → get wife sign-off → schedule into
   Blotato → log → attach scenes.

**Phase 2 — Approval-surface upgrade (only if the native approval still feels heavy).**
Move the parking + approval into a Buzz room so approve/redo is a chat message. Keep the same
staged-sheet contract so it's a surface swap, not a rebuild.

---

## 8. Guardrails preserved (nothing below is relaxed by automation)

- **Never auto-publish.** The routine parks; the human schedules. (Both skills, Phase 6.)
- **Wife grid-review stays mandatory** before anything schedules (`/social-launch` Phase 4).
- **Listing-live verification is a hard gate** — CSV "In Stock" ≠ live; the automated run drops
  unverified products (memory `[[project_listing_id_drift_bug]]`,
  `[[feedback_verify_listing_and_blotato_label_garble]]`).
- **Cooldown / rotation checks run and are shown every batch**, never silently passed (the 2026-08-30
  gap). Result printed on the Review Sheet.
- **Pre-publish blocking gate all-clear = ships; hard-fail tile is dropped/flagged.** Coaching notes
  (incl. the loud diaspora-anchoring one) logged, non-blocking during warmup.
- **No brand @tagging yet** (memory `[[feedback_no_brand_tagging_yet]]`).
- **UTM on every URL, alt text on every image, watermark on every visual** — a miss is a defect.
- **Pinterest 10 pins/24h cap** respected; overflow scheduled past the cap.

---

## 9. Success criteria

- Queue never drops below ~7 days of scheduled posts without the founder having ignored ≥2
  notifications.
- Founder's weekly time-on-social drops from a multi-hour production session to a <10-min approval.
- Zero manual IG steps in the automated lane (carousels only).
- No regression on the guardrails in §8 (spot-check: every automated batch's log has cooldown line,
  UTMs, alt text, hypothesis).

---

## 10. Kickoff prompt (paste into a fresh session to build Phase 1)

> Build the social automation loop from `mela-docs/social/social-automation-strategy.md` Phase 1.
> Add the carousels-only automated lane + queue-depth check to `/social-launch`, add staged-mode
> output to `mela-docs/social/staging/`, create the weekly Claude Code routine that runs it staged
> and push-notifies me, and write the `/social-approve` short-session flow. Preserve every guardrail
> in §8.

---

## 11. Build spec — the full-cloud weekly routine (settled 2026-09-29)

All decisions below are final; a fresh session should build the routine from this spec without
re-litigating. Blotato was connected to claude.ai via **OAuth** (not the api-key header — that path is
rejected by claude.ai's approved-header list) on 2026-09-29; `blotato_list_accounts` confirmed working
(IG @shopatmela id `53100`, Pinterest shopatmela id `7472`, YouTube id `41091`).

**Routine config**
- **Name:** `Mela Social — Weekly Staging`
- **Schedule:** `0 13 * * 3` (Wednesday 9am ET during EDT; note it drifts to 8am ET after DST ends
  2026-11-02 — acceptable for a weekly stage-for-approval job)
- **Model:** `claude-sonnet-5`
- **Environment:** Default (`env_015SQnFGk3JfQp61fLfLcWcL`)
- **Repos (sources):** `shop-at-mela/mela-docs`, `shop-at-mela/mela-skills`,
  `ppjogani/Mela-scrapper-integrations`
- **Connectors (`mcp_connections`):** **Blotato** (`https://mcp.blotato.com/mcp`) + **Claude-Docs**.
  Blotato must appear in the routine connector list first — if it doesn't, the Claude Code session
  needs a restart so the newly-added custom connector propagates; do not fabricate its `connector_uuid`.
- **allowed_tools:** `Bash, Read, Write, Edit, Glob, Grep` (Blotato MCP tools arrive via the connection).
- **Connector tool permissions (set in claude.ai):** auto-allow all read-only + Create Visual /
  Create Upload URL / Extract Source Content; keep Create Post / Update+Delete Scheduled Post on
  Needs-approval (enforces never-auto-publish); block the DM-automation + Post Comment + Send Message
  tools (out of scope).

**Prerequisites to verify at build time**
- The Default environment's GitHub auth can **push to `shop-at-mela/mela-docs`** (the routine commits the
  Review Sheet) and **read `ppjogani/Mela-scrapper-integrations`** (CSVs). Read is enough for the scrapper repo.

**The routine's internal prompt (self-contained — the cloud agent starts cold):**

> You are the Mela weekly social staging agent, running unattended in the cloud. You do NOT publish
> anything — you stage a batch for the founder's approval and stop.
>
> Context is in the cloned repos. Read these first: `mela-docs/social/social-automation-strategy.md`
> (the operating model), `mela-skills/social-launch/SKILL.md` and `mela-skills/social-review/SKILL.md`
> (the workflow you follow). Rules: `mela-docs/social/` → `category-routing.yaml`,
> `visual-style-guide.md`, `hook-engineering.md`, `pre-publish-gate.md`, `education-topics.yaml`,
> `pinterest-playbook.md`, `buyer-personas.md`, and `log/` (history + `CAMPAIGN_TEMPLATE.yaml`).
> Product data: `Mela-scrapper-integrations/scrapper_csvs/[category]/classified_products_prod/`.
>
> 1. Follow `/social-launch` Phases 0–3 plus the pre-publish gate.
> 2. Queue-depth check: via Blotato (`blotato_list_schedules` / `blotato_get_schedule`) for IG id
>    `53100` and Pinterest id `7472`, compute how many days of posts are already scheduled. Target a
>    **14-day** horizon; build only enough to refill the gap. If ≥14 days are already scheduled, stage
>    nothing and report "queue full."
> 3. **Carousels only — no reels** (carousels publish fully via API; reels need manual IG steps).
>    Select per Phase 1 (2 brands in different categories + 1 education topic), honoring the 240-day
>    product cooldown, category concentration, and **listing-live verification** — open
>    `shopatmela.com/l/{dev_listing_id}` and confirm the live text before any claim; drop any product
>    whose listing isn't open.
> 4. Render visuals with `blotato_create_visual` (real product images only, watermark, no text/price
>    overlays) per `visual-style-guide.md`; poll `blotato_get_visual_status`. Write captions + UTMs +
>    alt text per `/social-review` Phase 3.
> 5. Run the `pre-publish-gate.md` single pass on every tile; drop/flag any blocking hard-fail; log
>    coaching notes (especially diaspora anchoring) + a one-line hypothesis per tile.
> 6. **Do NOT create, schedule, or publish any post. Never call `blotato_create_post`.**
> 7. Write a Review Sheet to `mela-docs/social/staging/week-of-YYYY-MM-DD.md`: per tile — platform,
>    format, brand, product(s)+`dev_listing_id`, destination URL (with UTM), board, rendered visual
>    URL(s), caption, alt text, cooldown result, gate verdict, coaching notes, hypothesis; plus an
>    ASCII grid preview. Write per-tile campaign YAML stubs under `mela-docs/social/log/[brand-slug]/`
>    with `status: staged`.
> 8. Commit + push to a branch `social-staging/week-of-YYYY-MM-DD` and open a PR against `mela-docs`.
> 9. End with a one-paragraph summary: tiles staged, days added to queue, flags, and the Review Sheet path.
>
> Guardrails: never auto-publish; never guess a URL or brand handle; no brand @tagging; UTM on every
> URL, alt text on every image, watermark on every visual; respect Pinterest 10 pins/24h. Skip Phase
> 7b (attach-scene) — it needs Sharetribe creds unavailable in the cloud; note it for the founder's
> local approval session.

**After creation:** output the routine link `https://claude.ai/code/routines/{id}` and offer a
`RemoteTrigger action:"run"` dry-run so the first Review Sheet lands before waiting for Wednesday.

---

## Superseded approaches (kept per house rule)

- **"Just run `/social-launch` when I remember."** Set aside 2026-09-29: it is exactly the model that
  produced the 3-week silence — the trigger and all the labor sit on the founder, so a busy stretch =
  zero output. Replaced by the scheduled park-for-approval loop.
- **Fully autonomous auto-publish (no gate).** Considered and rejected 2026-09-29: fastest, but drops
  wife-review + founder approval, which is unacceptable brand risk during warmup. Revisit only after a
  long track record of the park-for-approval batches needing no edits.
- **Zavi/Praxis as the publisher.** Rejected 2026-09-29: no social-publish agent in the fleet; driving
  Blotato via `browser-operator` is brittle vs. the native Blotato MCP. Retained only as an upstream
  idea/signal feeder (§6).
- **Buzz as the Phase-1 surface.** Deferred, not rejected: better approval UX but new infra; adopt in
  Phase 2 if native approval friction justifies it (§7).
