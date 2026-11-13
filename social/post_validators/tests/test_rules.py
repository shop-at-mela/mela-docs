import datetime as dt
import unittest
from zoneinfo import ZoneInfo

from post_validators import rules
from post_validators.config import load_context
from post_validators.model import Post

TZ = ZoneInfo("America/New_York")
NOW = dt.datetime(2026, 11, 13, 16, 0, tzinfo=dt.timezone.utc)

BASE = {
    "id": "p1", "status": "scheduled", "format": "reel", "scheduled_at": "2026-11-24T14:00:00-05:00",
    "brands": ["saphed"], "caption": "I picked this up this week. It is soft.", "voice": "sana",
    "person_speaks": True, "people_present": True, "first_second_face_or_hands": True,
    "media": [{"kind": "mela_shot", "file": "a.mp4"}],
    "approval": {"approved_by": "Sana", "approved_at": "2026-11-23T10:00:00-05:00"},
    "story_drafts": [{"brand": "saphed", "scheduled_at": "2026-11-24T16:00:00-05:00",
                      "link": "https://shopatmela.com/brands/saphed?utm_source=instagram&utm_content=p1"}],
}


def post(**kw):
    d = dict(BASE)
    d.update(kw)
    return Post.from_dict(d, TZ)


def ledger_post(pid, brand=None, when="2026-11-01T12:00:00-05:00", people=False, fmt="carousel"):
    return Post.from_dict({"id": pid, "status": "live", "format": fmt, "posted_at": when,
                           "brands": [brand] if brand else [], "people_present": people}, TZ)


def ctx_(ledger=None):
    c = load_context(now=NOW)
    c.ledger = ledger or []
    return c


def all_brands_ledger(ctx):
    return [ledger_post(f"old-{b}", b, when=f"2026-10-{i + 1:02d}T12:00:00-04:00") for i, b in enumerate(sorted(ctx.roster.listed))]


class Rule1(unittest.TestCase):
    def test_first_post_for_gap_brand_after_dm_date_passes(self):
        self.assertEqual(rules.rule1_brand_coverage(ctx_(), [post()]), [])

    def test_first_post_before_dm_date_fails(self):
        v = rules.rule1_brand_coverage(ctx_(), [post(scheduled_at="2026-11-18T12:00:00-05:00")])
        self.assertEqual(len(v), 1)
        self.assertIn("outreach DM date", v[0].message)

    def test_second_post_blocked_while_gaps_exist(self):
        c = ctx_([ledger_post("x", "vilvah")])
        v = rules.rule1_brand_coverage(c, [post(brands=["vilvah"])])
        self.assertEqual(len(v), 1)
        self.assertIn("saphed", v[0].message)

    def test_second_post_allowed_when_every_brand_has_one(self):
        c = ctx_()
        c.ledger = all_brands_ledger(c)
        self.assertEqual(rules.rule1_brand_coverage(c, [post(brands=["vilvah"])]), [])

    def test_unlisted_brand_blocked(self):
        v = rules.rule1_brand_coverage(ctx_(), [post(brands=["the-nesavu"])])
        self.assertIn("not currently listed", v[0].message)

    def test_two_posts_same_brand_in_batch_second_blocked(self):
        c = ctx_()
        b = [post(id="a"), post(id="b", scheduled_at="2026-11-26T14:00:00-05:00")]
        v = rules.rule1_brand_coverage(c, b)
        self.assertEqual([x.post for x in v], ["b"])

    def test_missing_dm_date_fails(self):
        c = ctx_()
        c.roster_cfg["first_outreach_dm_dates"].pop("saphed")
        self.assertIn("no outreach DM date", rules.rule1_brand_coverage(c, [post()])[0].message)


class Rule2(unittest.TestCase):
    def test_compliant_post_passes(self):
        self.assertEqual(rules.rule2_cadence(ctx_(), [post()]), [])

    def test_two_posts_same_day_fail(self):
        b = [post(id="a"), post(id="b", scheduled_at="2026-11-24T21:00:00-05:00")]
        self.assertTrue(any("feed posts on" in v.message for v in rules.rule2_cadence(ctx_(), b)))

    def test_new_york_day_boundary(self):
        # 23:30 ET and 00:30 ET next day are different days but 1h apart: caught by the 6 hour rule.
        b = [post(id="a", scheduled_at="2026-11-24T23:30:00-05:00"), post(id="b", scheduled_at="2026-11-25T00:30:00-05:00")]
        v = rules.rule2_cadence(ctx_(), b)
        self.assertFalse(any("feed posts on" in x.message for x in v))
        self.assertTrue(any("min from post" in x.message for x in v))

    def test_five_posts_in_four_minutes_rejected(self):
        b = [post(id=f"p{i}", scheduled_at=f"2026-11-11T14:4{i}:00Z") for i in range(5)]
        v = rules.rule2_cadence(ctx_(), b)
        self.assertTrue(any("min from post" in x.message for x in v))

    def test_fifth_post_in_rolling_week_fails(self):
        b = [post(id=f"p{i}", scheduled_at=f"2026-11-{24 + i}T14:00:00-05:00") for i in range(5)]
        v = rules.rule2_cadence(ctx_(), b)
        self.assertTrue(any("Max 4" in x.message for x in v))

    def test_four_posts_in_week_pass(self):
        b = [post(id=f"p{i}", scheduled_at=f"2026-11-{24 + i}T14:00:00-05:00") for i in range(4)]
        self.assertEqual(rules.rule2_cadence(ctx_(), b), [])

    def test_existing_ledger_posts_count(self):
        c = ctx_([ledger_post("old", "vilvah", when="2026-11-24T09:00:00-05:00")])
        self.assertTrue(rules.rule2_cadence(c, [post()]))

    def test_missing_approval_fails(self):
        v = rules.rule2_cadence(ctx_(), [post(approval=None)])
        self.assertIn("No recorded human approval", v[0].message)

    def test_automation_cannot_approve(self):
        p = post(approval={"approved_by": "automation", "approved_at": "2026-11-23T10:00:00-05:00"})
        self.assertTrue(rules.rule2_cadence(ctx_(), [p]))

    def test_approval_after_publish_time_fails(self):
        p = post(approval={"approved_by": "Sana", "approved_at": "2026-11-25T10:00:00-05:00"})
        self.assertIn("after the publish time", rules.rule2_cadence(ctx_(), [p])[0].message)

    def test_auto_publish_fails(self):
        self.assertTrue(any("on its own" in v.message for v in rules.rule2_cadence(ctx_(), [post(auto_publish=True)])))

    def test_story_does_not_count_as_feed_post(self):
        b = [post(id="a"), post(id="s", format="story", scheduled_at="2026-11-24T18:00:00-05:00")]
        self.assertEqual(rules.rule2_cadence(ctx_(), b), [])


class Rule3(unittest.TestCase):
    def window(self, people_count):
        led = [ledger_post(f"l{i}", when=f"2026-11-{i + 1:02d}T12:00:00-05:00", people=i < people_count) for i in range(8)]
        return ctx_(led)

    def test_three_of_nine_passes(self):
        self.assertEqual(rules.rule3_people_quota(self.window(2), [post(people_present=True)]), [])

    def test_two_of_nine_fails(self):
        v = rules.rule3_people_quota(self.window(1), [post(people_present=True)])
        self.assertIn("Only 2 of the last 9", v[0].message)

    def test_untagged_candidate_fails(self):
        v = rules.rule3_people_quota(self.window(3), [post(people_present=None)])
        self.assertIn("no people_present tag", v[0].message)

    def test_untagged_history_fails(self):
        c = self.window(3)
        c.ledger[0].people_present = None
        v = rules.rule3_people_quota(c, [post()])
        self.assertIn("no people_present tag", v[0].message)

    def test_text_cover_cannot_count_as_person(self):
        v = rules.rule3_people_quota(self.window(3), [post(cover_kind="text_only")])
        self.assertTrue(any("do not count" in x.message for x in v))

    def test_sequential_batch_counts_earlier_batch_posts(self):
        c = self.window(2)
        b = [post(id="a", people_present=False, scheduled_at="2026-11-24T14:00:00-05:00"),
             post(id="b", people_present=False, scheduled_at="2026-11-26T14:00:00-05:00")]
        self.assertTrue(rules.rule3_people_quota(c, b))


class Rule4(unittest.TestCase):
    brand_media = [{"kind": "brand_asset", "brand": "saphed", "file": "saphed.jpg"}]

    def test_default_none_blocks_brand_image_and_names_permission(self):
        v = rules.rule4_rights(ctx_(), [post(media=self.brand_media)])
        self.assertIn("permission_granted or collab_agreed", v[0].message)
        self.assertIn("Sana", v[0].fix)

    def test_permission_with_date_and_source_passes(self):
        c = ctx_()
        c.permissions["brands"] = {"saphed": {"state": "permission_granted", "date": "2026-11-25", "source": "DM"}}
        self.assertEqual(rules.rule4_rights(c, [post(media=self.brand_media)]), [])

    def test_permission_without_source_fails(self):
        c = ctx_()
        c.permissions["brands"] = {"saphed": {"state": "collab_agreed", "date": "2026-11-25"}}
        self.assertTrue(rules.rule4_rights(c, [post(media=self.brand_media)]))

    def test_mela_shot_passes(self):
        self.assertEqual(rules.rule4_rights(ctx_(), [post()]), [])

    def test_owned_asset_needs_record(self):
        p = post(media=[{"kind": "owned_asset", "file": "x"}])
        self.assertTrue(rules.rule4_rights(ctx_(), [p]))

    def test_scheduled_post_without_media_fails_but_copy_draft_passes(self):
        self.assertTrue(rules.rule4_rights(ctx_(), [post(media=[])]))
        self.assertEqual(rules.rule4_rights(ctx_(), [post(media=[], status="draft")]), [])

    def test_unknown_kind_fails(self):
        self.assertTrue(rules.rule4_rights(ctx_(), [post(media=[{"kind": "stock", "file": "x"}])]))


class Rule5(unittest.TestCase):
    def test_carousel_only_plan_fails(self):
        b = [post(id=f"c{i}", format="carousel") for i in range(3)]
        self.assertTrue(any("video" in v.message for v in rules.rule5_format_mix(ctx_(), b)))

    def test_six_of_ten_passes(self):
        b = [post(id=f"v{i}", format="reel") for i in range(6)] + [post(id=f"c{i}", format="carousel") for i in range(4)]
        self.assertEqual(rules.rule5_format_mix(ctx_(), b), [])

    def test_five_of_ten_fails(self):
        b = [post(id=f"v{i}", format="reel") for i in range(5)] + [post(id=f"c{i}", format="carousel") for i in range(5)]
        self.assertTrue(rules.rule5_format_mix(ctx_(), b))

    def test_reel_checklist_false_fails(self):
        v = rules.rule5_format_mix(ctx_(), [post(first_second_face_or_hands=False)])
        self.assertIn("first second", v[0].message)

    def test_reel_checklist_missing_fails(self):
        self.assertTrue(rules.rule5_format_mix(ctx_(), [post(first_second_face_or_hands=None)]))


class Rule6(unittest.TestCase):
    def v(self, caption, **kw):
        return rules.rule6_copy(ctx_(), [post(caption=caption, **kw)])

    def test_clean_caption_passes(self):
        self.assertEqual(self.v("I found this linen shirt. It is light."), [])

    def test_em_dash_fails(self):
        self.assertIn("em dash", self.v("I love it — truly.")[0].message)

    def test_en_dash_and_hyphen_are_not_blocked(self):
        self.assertEqual(self.v("I wear it 9-5 and 10–12 hours."), [])

    def test_long_sentence_fails(self):
        self.assertTrue(any("words" in x.message for x in self.v(" ".join(["word"] * 25) + ".")))

    def test_wrong_voice_fails(self):
        self.assertTrue(any("Sana's voice" in x.message for x in self.v("I like it.", voice="brand")))

    def test_spoken_post_needs_first_person(self):
        self.assertTrue(any("first person" in x.message for x in self.v("This is lovely.", person_speaks=True)))

    def test_singular_buyer_fails_group_passes(self):
        self.assertTrue(any("Singular buyer" in x.message for x in self.v("A shopper who wants linen would buy this.")))
        self.assertTrue(any("Singular buyer" in x.message for x in self.v("Neha would buy this.")))
        self.assertEqual(self.v("Few shoppers told me they want linen."), [])

    def test_unverified_shipping_claim_fails(self):
        v = self.v("Ships to the US from India.")
        self.assertTrue(any("Unverified" in x.message for x in v))

    def test_duties_and_returns_claims_fail(self):
        self.assertTrue(self.v("Duties are included."))
        self.assertTrue(self.v("Easy returns."))

    def test_verified_claim_passes(self):
        c = ctx_()
        c.claims = {"saphed": [{"line": "Free US shipping over $69.", "checked_on": "2026-11-13",
                                "source_url": "https://shopatmela.com/brands/saphed"}]}
        self.assertEqual(rules.rule6_copy(c, [post(caption="Free US shipping over $69.", person_speaks=False)]), [])

    def test_claim_without_check_date_is_not_verified(self):
        c = ctx_()
        c.claims = {"saphed": [{"line": "Free US shipping.", "source_url": "https://shopatmela.com/brands/saphed"}]}
        self.assertTrue(rules.rule6_copy(c, [post(caption="Free US shipping.")]))

    def test_claim_verified_for_other_brand_does_not_count(self):
        c = ctx_()
        c.claims = {"vilvah": [{"line": "Free US shipping.", "checked_on": "2026-11-13",
                                "source_url": "https://shopatmela.com/brands/vilvah"}]}
        self.assertTrue(rules.rule6_copy(c, [post(caption="Free US shipping.")]))

    def test_hashtags_are_not_scanned_as_sentences(self):
        self.assertEqual(self.v("I like it.\n#shippingfast #returns"), [])


class Rule7(unittest.TestCase):
    def v(self, **kw):
        return rules.rule7_story_link(ctx_(), [post(**kw)])

    def test_paired_story_passes(self):
        self.assertEqual(self.v(), [])

    def test_missing_story_fails(self):
        self.assertIn("No same day Story", self.v(story_drafts=[])[0].message)

    def test_homepage_link_fails(self):
        s = [{"brand": "saphed", "scheduled_at": "2026-11-24T16:00:00-05:00", "link": "https://shopatmela.com/?utm_content=p1"}]
        self.assertTrue(any("own page" in x.message for x in self.v(story_drafts=s)))

    def test_other_brand_page_fails(self):
        s = [{"brand": "saphed", "scheduled_at": "2026-11-24T16:00:00-05:00", "link": "https://shopatmela.com/brands/vilvah?utm_content=p1"}]
        self.assertTrue(any("own page" in x.message for x in self.v(story_drafts=s)))

    def test_missing_utm_post_id_fails(self):
        s = [{"brand": "saphed", "scheduled_at": "2026-11-24T16:00:00-05:00", "link": "https://shopatmela.com/brands/saphed?utm_source=instagram"}]
        self.assertTrue(any("post id" in x.message for x in self.v(story_drafts=s)))

    def test_other_day_fails(self):
        s = [{"brand": "saphed", "scheduled_at": "2026-11-25T16:00:00-05:00", "link": "https://shopatmela.com/brands/saphed?utm_content=p1"}]
        self.assertTrue(any("same day" in x.message for x in self.v(story_drafts=s)))

    def test_wrong_host_fails(self):
        s = [{"brand": "saphed", "scheduled_at": "2026-11-24T16:00:00-05:00", "link": "https://evil.example/brands/saphed?utm_content=p1"}]
        self.assertTrue(self.v(story_drafts=s))

    def test_brandless_post_needs_no_story(self):
        self.assertEqual(self.v(brands=[], story_drafts=[]), [])


class Rule8(unittest.TestCase):
    def ctx_with_post(self, brand, pinned=False):
        c = ctx_([Post.from_dict({"id": "old", "status": "live", "posted_at": "2026-11-01", "brands": [brand], "pinned": pinned}, TZ)])
        return c

    def test_edit_frozen_brand_post_fails(self):
        v = rules.rule8_freeze(self.ctx_with_post("vilvah"), [{"type": "edit", "post_id": "old"}])
        self.assertIn("outreach freeze", v[0].message)

    def test_archive_and_delete_fail(self):
        c = self.ctx_with_post("kaunteya")
        self.assertEqual(len(rules.rule8_freeze(c, [{"type": "archive", "post_id": "old"}, {"type": "delete", "post_id": "old"}])), 2)

    def test_after_freeze_ends_passes(self):
        c = self.ctx_with_post("vilvah")
        c.now = dt.datetime(2026, 12, 4, tzinfo=TZ)
        self.assertEqual(rules.rule8_freeze(c, [{"type": "edit", "post_id": "old"}]), [])

    def test_non_cohort_brand_passes(self):
        self.assertEqual(rules.rule8_freeze(self.ctx_with_post("suta"), [{"type": "edit", "post_id": "old"}]), [])

    def test_pinned_post_never_touched_even_after_freeze(self):
        c = self.ctx_with_post("suta", pinned=True)
        c.now = dt.datetime(2027, 1, 1, tzinfo=TZ)
        self.assertTrue(rules.rule8_freeze(c, [{"type": "edit", "post_id": "old"}]))

    def test_pin_operation_always_fails(self):
        self.assertTrue(rules.rule8_freeze(ctx_(), [{"type": "pin", "post_id": "x"}]))

    def test_unknown_post_cannot_be_cleared(self):
        self.assertTrue(rules.rule8_freeze(ctx_(), [{"type": "edit", "post_id": "ghost"}]))


if __name__ == "__main__":
    unittest.main()
