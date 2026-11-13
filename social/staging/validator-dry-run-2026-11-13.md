# Dry run report (replay of config/ledger.yaml, run 2026-11-13)

Posts replayed: 42  (confirmed live: 38, logged as scheduled: 4)
Roster: snapshot, 21 brands listed, fetched 2026-11-13 15:00 UTC

## Violations by rule

| Rule | Name | Violations | Posts affected |
|---|---|---|---|
| 1 | brand coverage | 37 | 37 |
| 2 | cadence | 106 | 42 |
| 3 | people quota | 42 | 42 |
| 4 | rights | 85 | 23 |
| 5 | format mix | 1 | 1 |
| 6 | copy | 108 | 35 |
| 7 | link rule | 37 | 37 |
| 8 | freeze list | 0 | 0 |

## 1. Five posts in four minutes (rule 2)

- 2026-08-09 11:00 America/New_York: **2 posts in 0 min** (rule: 6h apart, 1 per day). Posts: `_education/chikankari-01-w1-campaign`, `nicobar/week-1-campaign`
- 2026-11-11 09:40 America/New_York: **5 posts in 4 min** (rule: 6h apart, 1 per day). Posts: `banjaaran-studio/week-2-campaign`, `_education/craft-farm-to-bottle-beauty-w1-campaign`, `suta/week-1-campaign`, `kaunteya/week-4-campaign`, `_education/sizing-01-w1-campaign`

## 2. People quota (rule 3)

- 0 of 42 posts carry a people_present tag. The rest are untagged, so the quota cannot pass.
- `_education/certdecode-01-w1-campaign`: Candidate has no people_present tag.
- `_education/chikankari-01-w1-campaign`: Candidate has no people_present tag.
- `_education/craft-farm-to-bottle-beauty-w1-campaign`: Candidate has no people_present tag.

## 3. Brand coverage (rule 1)

| Brand | Named posts in ledger |
|---|---|
| kaunteya | 4 |
| vilvah | 4 |
| ankid | 3 |
| house-of-chikankari | 3 |
| isharya | 3 |
| banjaaran-studio | 2 |
| fizzy-goblet | 2 |
| gullylabs | 2 |
| superbottoms | 2 |
| tarinika | 2 |
| the-alternate | 2 |
| aagghhoo | 1 |
| babyforest | 1 |
| choosekind | 1 |
| nicobar | 1 |
| polite-society | 1 |
| suta | 1 |
| hemant-and-nandita | 0 |
| masilo | 0 |
| needledust | 0 |
| saphed | 0 |

- Listed brands with zero named posts: hemant-and-nandita, masilo, needledust, saphed
- Most posted brand: **kaunteya (4)** while 4 listed brands have none.

## 4. Posts about brands not on the site (rule 1)

- **pluchi**: 1 ledger post(s), brand is not on shopatmela.com/brands
- **the-nesavu**: 1 ledger post(s), brand is not on shopatmela.com/brands

## The 2026-11-11 batch as it would be checked today

5 posts: `_education/craft-farm-to-bottle-beauty-w1-campaign`, `_education/sizing-01-w1-campaign`, `banjaaran-studio/week-2-campaign`, `kaunteya/week-4-campaign`, `suta/week-1-campaign`

- Rule 1 (brand coverage): 4 violations on 4 of 5 posts. e.g. 'vilvah' already has 3 named post(s) and these listed brands have none: saphed, needledust, hemant-and-nandita, masilo, suta.
- Rule 2 (cadence): 35 violations on 5 of 5 posts. e.g. No recorded human approval.
- Rule 3 (people quota): 5 violations on 5 of 5 posts. e.g. Candidate has no people_present tag.
- Rule 4 (rights): 9 violations on 3 of 5 posts. e.g. Image 'https://database.blotato.io/storage/v1/object/public/public_media/40ff5931-a86e-4c86-8caf-693002fc13d9/videogen2-render-0c11f3a5-1704-4684-8cd0-099de7bb7b04.jpg' is banjaaran-studio's asset. Missing permission: permission_granted or collab_agreed from banjaaran-studio.
- Rule 6 (copy): 14 violations on 5 of 5 posts. e.g. Sentence has 21 words (max 18): 'Goat milk, cold pressed oils, and botanical extracts go in c...'
- Rule 7 (link rule): 4 violations on 4 of 5 posts. e.g. No same day Story draft for brand 'vilvah'.

## Other rules on old posts

- Rule 4 (rights): 85 violations. Example: `aagghhoo/week-1-campaign`: Image 'Leaf Green Cotton Flannel Baby/Toddler Blanket' is aagghhoo's asset. Missing permission: permission_granted or collab_agreed from aagghhoo.
- Rule 5 (format mix): 1 violations. Example: `(batch)`: 0 of 42 new posts are video. Need at least 26 (6 per 10).
- Rule 6 (copy): 108 violations. Example: `_education/certdecode-01-w1-campaign`: Sentence has 27 words (max 18): 'One, a named material and its percentage, not a vibe like 'e...'
- Rule 7 (link rule): 37 violations. Example: `_education/chikankari-01-w1-campaign`: No same day Story draft for brand 'house-of-chikankari'.
- Rule 2 approval: no old post has a recorded approval, so each fails on that.
- Rule 8 does not apply to a replay (it checks archive, edit, delete and pin operations).

## Caveats

- The ledger is built from social/log, not from Instagram. It does not reproduce the account's 54 posts or Vilvah's 6 named posts. Add missing posts in config/ledger_overrides.yaml, then rerun.
- Times for the 5 Nov 11 posts are estimated from the report 'five posts in four minutes' (see ledger_overrides.yaml). Most older posts have a date only, so the 6 hour check skips them.
- Old posts inferred as brand assets: logs show scenes built from each brand's own product photos.

## Compliant draft end to end

Draft: `post_validators/examples/compliant_draft.yaml` (Saphed first post, Reel, Sana on camera, `mela_shot` media,
paired Story, no claims). Checked with `--now 2026-11-13T16:00:00Z` against the real config.

```
FAIL rule 3 (people quota) post=example-saphed-first-look: 8 of the last 9 covers have no people_present tag ...
     fix: Tag those posts in config/post_tags.yaml so the quota can be checked.
1 post(s) checked, 1 violation(s). BLOCKED: do not schedule.
```

That is the true state today: rules 1, 2, 4, 5, 6 and 7 pass, and the draft is blocked only because none of the
last 8 posts has a `people_present` tag. With those 8 tagged (3 true, as a demo copy of the config, not committed),
the same draft passes with exit 0 (`tests/test_end_to_end.py`). Moving the same draft to `scheduled` with no recorded
approval fails rule 2, and dating it Nov 17 fails rule 1 (before Saphed's DM date).

## What a human still has to do

1. Tag the last 8 live posts in `config/post_tags.yaml` (people_present true or false). Nothing posts until then.
2. Add the posts the logs miss (for example 2 more Vilvah posts) in `config/ledger_overrides.yaml`.
3. Add the two missing names to the freeze list (22 brands in the outreach cohort, 20 listed).
4. Check the roster: the page title says 23+ brands, 21 names were read.
