# Paste this into a new session

Start it from the Mela directory or Blotato will not exist:

```
cd ~/Documents/Mela && claude
```

---

Three social posts are queued at `status: ready_to_schedule` and prepped. Follow
`mela-docs/social/log/ankid/BLOTATO-RUNBOOK.md` top to bottom. Read it and the three
campaign files before doing anything:

- `mela-docs/social/log/kaunteya/week-1-campaign.yaml`
- `mela-docs/social/log/ankid/week-2-campaign.yaml`
- `mela-docs/social/log/ankid/week-2-education-campaign.yaml`

**First, prove Blotato is reachable.** Call `blotato_list_accounts`. If no `blotato_*`
tool exists, stop and tell me. The session is in the wrong directory and nothing
below will work.

**Captions, handles and destinations are final.** Do not rewrite them, do not
re-derive @handles from `shopify_brands.py`, do not re-add UTMs. All three
destinations are already tagged.

## Instagram

Kaunteya W1: visuals already exist and were verified live on 2026-08-01. No visual
work. Submit the four `instagram.products[].image_url` values in file order.

Both Ankid posts: build visuals with Blotato Product Scene Placement
(`f524614b-ba01-448c-967a-ce518c52a700`) using the exact `source_image_url` recorded
on each product. Scene prompts are written out in the runbook, use them as is. Then
`blotato_get_visual_status` until complete.

Hard rules for the Ankid visuals:

- Use `source_image_url` only. Do not grab a listing hero. The heroes are wrong and
  each product's `source_image_note` says why.
- Do not AI generate the products themselves. Scene placement only.
- The imgix URLs are signed and the `s=` value is bound to the `w`/`h` params. Copy
  each URL whole. Editing dimensions returns 403.
- If the render comes back with no Mela watermark, that is a known Blotato gap. Note
  it and carry on, do not block the post.

Then `blotato_create_post` per post, and poll `blotato_get_post_status` once.

## Pinterest

Manual for all three. The account is still inside Blotato's warmup block and the API
hard rejects every Pinterest post.

**Do not call `blotato_create_post` for Pinterest.** Not even once to re-check.

Instead, present each pin as ready to paste: title, description, image, link, board.
I will post them by hand in the Pinterest app after that campaign's Instagram post is
live. Pins stay `manual_pending` until I confirm.

- Kaunteya: 4 pins, board Home and Kitchen, images ready now.
- Ankid product: 4 pins, board Gifting and Occasions. Each has a `source_image_url`
  but needs the Blotato render before its `image_url` is fillable.
- Ankid education: Instagram only, no pins.

Pinterest wants 2:3 at 1000x1500. Request that size explicitly, do not reuse the
Instagram 1:1 render.

## Approval

Show the `/social-review` Phase 6 summary for all three posts before publishing
anything: platform, format, visual URL, caption, destination, board, one line UX
note. **Never auto publish.** Ask me timing per post: now, next slot, a specific
time, or skip.

## After scheduling

Phase 7 logging in each YAML: `status`, `date_posted`, `submission_id`,
`schedule_id`, and `image_url` with the rendered Blotato URL. Leave
`source_image_url` alone, it records the input, not the output. In the education
file `instagram.image_url` is a list, fill it in slide order.

Then re-validate, two of these files were unparseable before 2026-08-01:

```
cd mela-docs/social/log && python3 -c "
import yaml,glob
[yaml.safe_load(open(f)) for f in glob.glob('*/*.yaml')]
print('all parse')"
```
