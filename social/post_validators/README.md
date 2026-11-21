# Post validators

Hard-fail checks that run before any Instagram post is scheduled. They draft and block. They never
publish, schedule, archive or call Instagram. Eight rules, nothing else.

## Run

From `mela-docs/social`:

```
python3 -m post_validators check path/to/batch.yaml     # exit 0 pass, 1 blocked, 2 roster error
python3 -m post_validators check batch.yaml --live-roster   # read shopatmela.com/brands now
python3 -m post_validators audit --out staging/report.md --focus-date 2026-11-11   # replay old posts
python3 -m post_validators import-ledger                 # rebuild config/ledger.yaml from social/log
python3 -m post_validators roster-update                 # refresh roster snapshot time, list changes
python3 -m unittest discover -s post_validators/tests -t .   # 80 tests
```

Needs Python 3.11+ and PyYAML. No other dependencies.

## Batch file

See `post_validators/examples/compliant_draft.yaml`. A batch has `posts:` and optional `operations:`
(`type: archive|edit|delete|pin`, `post_id`). A post carries: `id, status, format (reel|video|carousel|image|story),
scheduled_at, brands, caption, voice, person_speaks, people_present, cover_kind, first_second_face_or_hands,
media [{kind: mela_shot|owned_asset|brand_asset, brand, file}], story_drafts [{brand, scheduled_at, link}],
approval {approved_by, approved_at}`. Workflow: draft, `check` passes, a person records approval, set status
to `scheduled`, `check` again.

## Rules and where they live

| # | Rule | Code (`rules.py`) | Config a human edits (`config/`) |
|---|---|---|---|
| 1 | Brand coverage, DM timing, listed brands only | `rule1_brand_coverage` | `roster.yaml` (snapshot, `priority_gaps`, `first_outreach_dm_dates`) |
| 2 | 1 per NY day, 4 per 7 days, 6h apart, human approval | `rule2_cadence` | `settings.yaml` `cadence` |
| 3 | 3 of any 9 covers show a person | `rule3_people_quota` | `post_tags.yaml`, `settings.yaml` `people_quota` |
| 4 | Image rights per brand, default none | `rule4_rights` | `permissions.yaml` |
| 5 | 6 of 10 new posts video, Reel first second check | `rule5_format_mix` | `settings.yaml` `format_mix` |
| 6 | Copy: no em dash, short sentences, Sana voice, group-only buyer research, verified claims only | `rule6_copy` | `verified_claims.yaml`, `settings.yaml` `copy` |
| 7 | Same day Story draft to the brand's own page with post id UTM | `rule7_story_link` | `settings.yaml` `link` |
| 8 | Freeze list until 2026-12-03, never touch pinned | `rule8_freeze` | `freeze.yaml` |

Other config: `ledger.yaml` (generated post history), `ledger_overrides.yaml` (corrections, extra posts).

## Behavior worth knowing

- **Roster fails closed.** The snapshot in `roster.yaml` is accepted for `max_age_hours` (48). After that the check exits 2
  until `--live-roster` works or the snapshot is refreshed. A brand missing from the snapshot is treated as not listed.
- **Tags are never guessed.** An untagged post cannot count toward the people quota, and an untagged candidate or untagged
  history blocks. Tag posts in `config/post_tags.yaml`.
- **"After Nov 17" means from Nov 18 00:00 America/New_York.**
- **Video share** is `ceil(0.6 x new feed posts in the batch)`, so a single new carousel fails until the mix is planned.
- **Claims:** any sentence mentioning shipping, duties, customs, returns, refunds or delivery must match, word for word, a line in
  `verified_claims.yaml` for a brand named in the post, with a check date and a shopatmela.com URL. Otherwise omit it.
- **Em dash only** is blocked (U+2014). Hyphens and en dashes are allowed.
- Date-only history (most old posts) counts for the daily and 7 day limits at noon local time. The 6 hour rule needs exact times.

## Known conflicts with existing guidance (not edited here)

These docs still describe the old behavior. The validators win. Update them when ready:
`category-routing.yaml` (daily cadence, carousel default), `social-automation-strategy.md` and
`mela-skills/social-launch|social-review/SKILL.md` (9 tiles a week, carousel only, brand-voiced captions,
third person "Discover X on Mela", shipping lines from `shopify_brands.py`, `utm_campaign={brand}_w{week}` links).
The routine must run `check` before it schedules anything.
