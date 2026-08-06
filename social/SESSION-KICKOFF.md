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
- **Templates (built, rendering):** `templates/` — `hook-card.html`, `teaching-card.html`,
  `payoff-card.html` (cultural_education); `shipping-timeline.html`, `myth-vs-fact.html`
  (trust_service); `spotlight-card.html` (brand story); `photo-watermark.html` (watermark a
  real product/lifestyle photo); shared `mela-kit.css`, `render.sh`, `README.md`.
- **Topics:** `education-topics.yaml` — every cultural topic has a `contemporary_angle`;
  customs duties nuance + parked brand-DDP idea captured. Used so far: craft-blockprint
  (cultural_education, wk2), ship-01 (trust_service, wk3). NEXT should be cultural_education.
- **First education post — SHIPPED 2026-08-05:** `log/ankid/week-2-education-campaign.yaml`
  (Ankid block-print, live at instagram.com/p/DbrxR-VET7Y). The rebuild recipe under
  `notes.resolution_2026_08_05` is the worked example for future cultural_education posts.

## Data-quality watch (learned 2026-08-06)

- **Verify every product listing live before a product post.** The classified CSV "In Stock"
  flag does NOT mean the Mela listing is open. In the wk3 batch, Baby Forest's + Nicobar's
  onboarding hero listing IDs were **closed**, and **Nicobar's Dev_Listing_IDs are drifted**
  (a "dress" ID resolved to a live "bracelet"). Ankid + Baby Forest are reconciled/verified;
  **Nicobar is NOT** — it needs a SKU-keyed reconcile before any specific-product post.
- **Blotato Product Scene Placement garbles product labels** (diffusion text failure). For
  label-forward products (skincare, baby), use the brand's own real photo + `photo-watermark.html`,
  not a Blotato scene. Scenes are fine for motif-only products (e.g. Nicobar ceramics).
- **The IG grid is DEFERRED** (`category-routing.yaml` grid.enabled: false) — batches are
  standalone posts (product + brand-story + education), NOT 9-tile rows, until profile-visit
  volume justifies wayfinding.

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
