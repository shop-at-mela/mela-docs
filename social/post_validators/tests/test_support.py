import datetime as dt
import tempfile
import unittest
from pathlib import Path

import yaml

from post_validators import cli, ledger
from post_validators.config import load_context
from post_validators.roster import RosterError, from_live, from_snapshot, parse_live_html
from post_validators.engine import run_all
from post_validators.model import Post

from .test_rules import BASE, NOW, TZ, ctx_

HTML = '<a href="/brands/saphed">Saphed</a><a href="https://shopatmela.com/brands/Vilvah">V</a><a href="/brands/banjaaran">B</a>'


class RosterTests(unittest.TestCase):
    def test_parse_live_html(self):
        self.assertEqual(parse_live_html(HTML), {"saphed", "vilvah", "banjaaran"})

    def test_live_roster_matches_aliases(self):
        c = ctx_()
        r = from_live(c.roster_cfg, NOW, HTML)
        self.assertEqual(r.listed, {"saphed", "vilvah", "banjaaran-studio"})

    def test_live_roster_failing_fetch_fails_closed(self):
        with self.assertRaises(RosterError):
            from_live(ctx_().roster_cfg, NOW, "<html>no links</html>")

    def test_stale_snapshot_fails_closed(self):
        c = ctx_()
        with self.assertRaises(RosterError):
            from_snapshot(c.roster_cfg, NOW + dt.timedelta(days=10))
        self.assertTrue(from_snapshot(c.roster_cfg, NOW + dt.timedelta(days=10), allow_stale=True).listed)

    def test_resolve_display_names(self):
        r = ctx_().roster
        self.assertEqual(r.resolve("Hemant & Nandita"), "hemant-and-nandita")
        self.assertEqual(r.resolve("The Alternate India"), "the-alternate")
        self.assertIsNone(r.resolve("Unknown Brand"))


class LedgerTests(unittest.TestCase):
    def test_import_filters_staged_and_flags_confirmation(self):
        with tempfile.TemporaryDirectory() as d:
            logs = Path(d)
            (logs / "acme").mkdir()
            (logs / "acme" / "week-1.yaml").write_text(yaml.safe_dump({
                "brand_slug": "acme", "status": "posted", "date_posted": "2026-11-01", "format": "collection_carousel",
                "instagram": {"caption": "hi", "products": [{"name": "A", "source_photo": "http://x/a.jpg"}]}}))
            (logs / "acme" / "week-2.yaml").write_text(yaml.safe_dump({"brand_slug": "acme", "status": "staged", "instagram": {}}))
            (logs / "acme" / "week-3.yaml").write_text(yaml.safe_dump({"brand_slug": "acme", "status": "scheduled", "date_posted": "2026-11-05", "instagram": {}}))
            posts = ledger.build(logs, {}, {})
            self.assertEqual([p["id"] for p in posts], ["acme/week-1", "acme/week-3"])
            self.assertTrue(posts[0]["confirmed"])
            self.assertFalse(posts[1]["confirmed"])
            self.assertEqual(posts[0]["media"][0]["kind"], "brand_asset")
            self.assertIsNone(posts[0]["people_present"])

    def test_overrides_apply_and_add(self):
        with tempfile.TemporaryDirectory() as d:
            logs = Path(d)
            (logs / "acme").mkdir()
            (logs / "acme" / "w.yaml").write_text(yaml.safe_dump({"brand_slug": "acme", "status": "posted", "date_posted": "2026-11-01", "instagram": {}}))
            posts = ledger.build(logs, {"acme/w": {"posted_at": "2026-11-01T10:00:00Z"}, "extra": {"add": True, "status": "live", "brands": ["vilvah"]}}, {})
            self.assertEqual(posts[0]["posted_at"], "2026-11-01T10:00:00Z")
            self.assertEqual(posts[1]["id"], "extra")

    def test_tags_file_merges_into_ledger(self):
        with tempfile.TemporaryDirectory() as d:
            cfg = Path(d)
            for f in Path(load_context(now=NOW).config_dir).glob("*.yaml"):
                (cfg / f.name).write_text(f.read_text())
            (cfg / "ledger.yaml").write_text(yaml.safe_dump({"posts": [{"id": "a", "status": "live", "posted_at": "2026-11-01", "brands": ["vilvah"]}]}))
            (cfg / "post_tags.yaml").write_text(yaml.safe_dump({"tags": {"a": {"people_present": True}}}))
            self.assertIs(load_context(cfg, now=NOW).ledger[0].people_present, True)


class CliTests(unittest.TestCase):
    def run_batch(self, posts, ops=None):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "batch.yaml"
            f.write_text(yaml.safe_dump({"posts": posts, "operations": ops or []}))
            return cli.main(["--now", "2026-11-13T16:00:00Z", "check", str(f)])

    def good_ledger_ctx(self):
        return ctx_()

    def test_compliant_batch_exit_zero_with_stubbed_clean_ledger(self):
        c = ctx_()
        posts = [Post.from_dict(dict(BASE), TZ)]
        self.assertEqual(run_all(c, posts), [])

    def test_violations_exit_nonzero(self):
        bad = dict(BASE, caption="Nope — bad.", approval=None)
        self.assertEqual(self.run_batch([bad]), 1)

    def test_stale_roster_exits_two(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "b.yaml"
            f.write_text(yaml.safe_dump({"posts": [dict(BASE)]}))
            self.assertEqual(cli.main(["--now", "2027-01-01T00:00:00Z", "check", str(f)]), 2)


if __name__ == "__main__":
    unittest.main()
