# Blotato runbook: Kaunteya W1 + Ankid W2 (x2)

Prepared 2026-08-01. Everything below is ready to run. Three posts are queued at
`status: ready_to_schedule`, all captions final, all destinations UTM tagged, all
source photos resolved and visually verified.

## 0. Start the session correctly

Blotato is scoped to the Mela project in `.claude.json`. A session started from `~`
loads only firecrawl and **no `blotato_*` tools will exist**. That is what blocked
the 2026-08-01 run.

```
cd ~/Documents/Mela && claude
```

Confirm with `blotato_list_accounts` before anything else. If the tool is not found,
you are in the wrong directory.

Housekeeping: `.claude.json` has two identical entries, `blotato` and `Blotato`,
same URL and same key. Delete one.

---

## 1. Kaunteya W1 — no visual work needed

`log/kaunteya/week-1-campaign.yaml`

Visuals already exist from an earlier session and all four were re-verified live on
2026-08-01 (HTTP 200). The destination page crash that held this post is confirmed
fixed. Submit straight to Instagram.

```
blotato_list_accounts
blotato_create_post
  platform:   instagram
  mediaUrls:  the 4 instagram.products[].image_url values, in file order
  text:       instagram.caption verbatim
  scheduledAt: <user's chosen time>
blotato_get_post_status   (poll once)
```

Carousel order: Airavata Garuda, Airavata Owl, Byah Jug, Byah Coffee Mug.

---

## 2 and 3. Ankid W2 product + education — build visuals first

`log/ankid/week-2-campaign.yaml` and `log/ankid/week-2-education-campaign.yaml`

Each product now carries a `source_image_url`: a real product photo, chosen by eye
rather than by hero position, with a `source_image_note` saying why. **Use those
exact URLs.** Do not re-derive them from the listing and do not AI generate the
products themselves.

The imgix URLs are signed. The `s=` signature is bound to the `w`/`h` params, so
editing the dimensions returns 403. Copy each URL whole.

### Why the hero images are wrong

Do not swap in a listing hero to "improve" a slide. Verified 2026-08-01:

| Listing | Hero actually shows |
|---|---|
| Bandana | a gingham **dress** on a child; bandana is only a headband |
| Bandhgala | cropped legs and sandals; gallery also holds a size chart and a face portrait |

For the bandhgala, only **one** of four gallery images shows the product. It is the
hanger shot, and it is also what substantiates the caption's hand embroidered floral
claim. It is already recorded as that product's `source_image_url`.

### Build the visual

Template: Product Scene Placement `f524614b-ba01-448c-967a-ce518c52a700`
Aspect: Instagram 1:1. Keep key content centred, the profile grid crops to 3:4.

Prompt for the **product carousel** (post 2):

```
Create lifestyle scenes for Ankid children's festival wear.
Place each supplied product photo into its own scene, one product per slide,
4 slides total, in this order:

Slide 1: rust gingham bandana on a warm stone surface with soft folded cotton
         and a few dried botanicals
Slide 2: peach top and gingham pant set laid on pale linen, morning light
         across the fabric
Slide 3: black bandhgala set on a wooden surface with brass and marigold,
         festive but calm
Slide 4: mustard appliqued linen top on warm neutral cloth with small wooden
         play objects

MELA BASELINE: earthy tones, soft natural light, calm artisanal mood
CATEGORY ACCENT (baby and kids): joyful and nurturing, soft pastels with warm
neutrals, craft quality and stitching visible, gentle natural props
OUTCOME: props must not overshadow the garment; keep the block print, applique
and embroidery legible; plenty of negative space
WATERMARK: "Discovered on [Mela Logo]" bottom right, semi transparent,
navy #2D2D7B, 10 to 15% of image width
NO product names, NO prices, NO text overlays
```

Prompt for the **education carousel** (post 3), craft process focus:

```
Create scenes illustrating hand block printing for Ankid, 4 slides:

Slide 1: macro of the rust gingham block print, raking light so the slight
         registration variation between repeats is visible
Slide 2: carved wooden printing blocks resting beside folded printed cotton
Slide 3: the printed top and pant set laid flat on warm linen
Slide 4: detail of the print meeting a seam, showing the fabric weave

MELA BASELINE: earthy tones, soft natural light, calm artisanal mood
OUTCOME: the print texture and its hand made irregularity is the subject;
do not smooth or regularise the pattern
WATERMARK: "Discovered on [Mela Logo]" bottom right, semi transparent,
navy #2D2D7B, 10 to 15% of image width
NO product names, NO prices, NO text overlays
```

Then:

```
blotato_get_visual_status   (poll until complete)
blotato_create_post
  platform:    instagram
  mediaUrls:   the rendered visual URLs, in slide order
  text:        instagram.caption verbatim
  scheduledAt: <user's chosen time>
blotato_get_post_status     (poll once)
```

Known gap: Blotato's Product Scene Placement has not been applying the watermark
(see `feedback_blotato_scene_watermark_gap`). Include the spec anyway, then check the
render. If it is missing again, that is expected, not a reason to block the post.

---

## 4. Pinterest stays manual, all three posts

The account is still inside Blotato's warmup block. Blotato's API hard rejects every
Pinterest post until roughly two weeks of 1 pin per day manual posting and 100+
monthly views. **Do not call `blotato_create_post` for Pinterest.** It will fail, and
the failure is not informative.

Post each pin by hand in the Pinterest app once that campaign's Instagram post is
live. Drafts are complete in each YAML: title, description, link with UTMs, board.

- Kaunteya, 4 pins, board Home and Kitchen `1103593152379723626`. Images ready.
- Ankid product, 4 pins, board Gifting and Occasions `1103593152379723628`.
  Each pin has a `source_image_url`; its `image_url` needs the Blotato render first.
- Ankid education is Instagram only. No pins.

Pinterest wants 2:3 (1000x1500). Do not reuse the Instagram 1:1 render, request the
Pinterest size explicitly.

---

## 5. Phase 7 logging, write back after each post

Per campaign file:

- `status`: `ready_to_schedule` becomes `scheduled` (or `posted`)
- `date_posted`: actual date
- `instagram.submission_id` and `instagram.schedule_id`: from the Blotato response
- `instagram.products[].image_url`: the **rendered** Blotato URL.
  Leave `source_image_url` alone, it records the input, not the output
- education file: `instagram.image_url` is a list, fill in slide order
- Pinterest pins stay `manual_pending` until posted by hand, then `posted`

Re-validate after editing:

```
cd mela-docs/social/log && python3 -c "
import yaml,glob
[yaml.safe_load(open(f)) for f in glob.glob('*/*.yaml')]
print('all parse')"
```

---

## Changes made 2026-08-01, before any publish

1. **UTMs added** to all three `instagram.destination` values, which were bare.
   Schema per `category-routing.yaml` → `tracking`. The seven already published
   campaigns are also bare but were left alone; editing them would misrepresent
   what actually shipped. Worth a separate backfill decision.
2. **pink became rust** in the Ankid caption and bandana pin description. The photo
   is visibly rust/terracotta. The carousel bullet was shortened to "Hand Block
   Printed Bandana" so it still matches the listing name without asserting a colour
   the image contradicts. No other caption text touched.
3. **`week-2-education-campaign.yaml` did not parse as YAML.** A stray `image_url`
   sat at the same indent as the `anchor_products` list items. Any Phase 1 run that
   loads every log file would have errored or skipped this campaign. Fixed.
4. **`fizzy-goblet/week-1-campaign.yaml` did not parse either**, an unquoted
   `"Featured in this carousel: [list]"` inside a plain scalar. Fixed, syntax only.
5. All 11 campaign logs now parse. A lint step over `social/log/*/*.yaml` would catch
   this class of break at write time.

## Still open

- `destination_not_linked`: IG captions are not clickable and the bio link is the
  generic homepage. Affects all three posts. Copy says "link in bio" for accuracy.
- `listing_image_quality` (new, logged in the Ankid product campaign): listing heroes
  are often not the product, size charts and portraits sit inline in galleries, and
  the bandana's title says Pink for a rust product. Needs a fix at the listings layer.
- Kaunteya `mobile_responsive` is still `tbd`, only ever checked at 1515px.
