# Social — New Session Kickoff

Start here to resume social production in a fresh Claude Code session with full context.
**Nothing is lost between sessions** — the context lives in these files + auto-loaded memory,
not in any one chat. A new session loads `MEMORY.md` automatically and the skills re-read the
docs below on each run.

## What's persisted (the context a new session inherits)

- **Memory:** `project_living_culture_reframe` (loaded via MEMORY.md) — the Education Visual
  System, living-culture reframe, tool decision procedure, and the built templates.
- **Visual system + tool decision procedure:** `visual-style-guide.md` → Education Visual System.
- **Skills:** `/social-review` (single post) and `/social-launch` (weekly batch) — both already
  route education away from the product pipeline (Phase 3d).
- **Templates (built, rendering):** `templates/` — `hook-card.html`, `shipping-timeline.html`,
  `myth-vs-fact.html`, shared `mela-kit.css`, `render.sh`, `README.md`.
- **Topics:** `education-topics.yaml` — every cultural topic has a `contemporary_angle`;
  customs duties nuance + parked brand-DDP idea captured.
- **First education post, scoped + held:** `log/ankid/week-2-education-campaign.yaml` — has a
  full rebuild recipe under `notes.resolution_2026_08_05`.

## Current task (one-time — prune when done, see Housekeeping)

> **Decided order (2026-08-05): do A first, then B.** Ship the held Ankid education post end to
> end, then run the next batch. First education post = held Ankid block-print.

**Housekeeping (do this when A + B are complete):** mark the Ankid campaign `status: posted` in
its log, then delete THIS "Current task" section only. Do **not** delete the file — the rest is
the durable resume guide, and `MEMORY.md` + the skills point to it.

## Kickoff prompts (paste one into the new session)

**A) Build the FIRST education post (held Ankid block-print):**
> Build the held Ankid Week 2 education post. Follow the rebuild recipe in
> `mela-docs/social/log/ankid/week-2-education-campaign.yaml` → `notes.resolution_2026_08_05`
> and the Education Visual System in `visual-style-guide.md`. Use the `templates/` HTML kit for
> the hook + teaching cards (render via `render.sh`), Blotato for the illustrative block/dye
> still, and the existing Ankid product photo as the final payoff slide. Retune the caption to
> lead with the topic's `contemporary_angle`. Then run the `/social-review` UX + publish phases.

**B) Kick off the NEXT batch:**
> Run `/social-launch` for the next weekly batch. Score `education-topics.yaml` for the next
> education topic (alternate type from the last used), pick 2 brands in different categories,
> and produce all tiles. Education tiles use the Education Visual System + `templates/` kit,
> not the product pipeline.

(Do A first if you want the single post shipped before batching; or go straight to B — social-launch
will include an education tile either way.)

## Live rules to honor (already in the docs, flagged here so they're not missed)

- **Slide 1 of any education post is a hook, never a product.**
- **Mela is currently AFFILIATE** — buyers discover on Mela, then check out on the brand's own
  site. Never imply Mela is the store/shipper. (Timeline template already fixed to "order from
  the brand.")
- **Duties vary by brand** — some prepay (DDP), many don't. Never claim "duties handled up front"
  as a blanket fact. (Myth/fact template default avoids it.)
- **Verify `verify:true` claims** (shipping days, customs, craft specifics) on the source before
  publishing.
- **Tool choice:** run the decision procedure in `visual-style-guide.md` (Gate 0 motion → Gate 1
  imagery → Gate 2 codeable). Canva last.
