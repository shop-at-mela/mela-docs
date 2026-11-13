import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from post_validators import cli
from post_validators.config import DEFAULT_CONFIG_DIR

DRAFT = Path(__file__).resolve().parent.parent / "examples" / "compliant_draft.yaml"
NOW = "2026-11-13T16:00:00Z"


class EndToEnd(unittest.TestCase):
    def copy_config(self):
        d = Path(tempfile.mkdtemp())
        for f in DEFAULT_CONFIG_DIR.glob("*.yaml"):
            shutil.copy(f, d / f.name)
        return d

    def test_draft_on_real_config_blocks_only_on_untagged_history(self):
        # Real state today: no old post has a people_present tag, so rule 3 is the one thing blocking.
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cli.main(["--now", NOW, "check", str(DRAFT), "--json"])
        import json
        rules = {v["rule"] for v in json.loads(buf.getvalue())}
        self.assertEqual(code, 1)
        self.assertEqual(rules, {3})

    def test_draft_passes_when_history_is_tagged(self):
        cfg = self.copy_config()
        ledger = yaml.safe_load((cfg / "ledger.yaml").read_text())["posts"]
        timed = sorted((p for p in ledger if p.get("posted_at")), key=lambda p: str(p["posted_at"]))
        tags = {p["id"]: {"people_present": i < 3} for i, p in enumerate(timed[-8:])}  # demo tags, not committed
        (cfg / "post_tags.yaml").write_text(yaml.safe_dump({"tags": tags}))
        self.assertEqual(cli.main(["--config-dir", str(cfg), "--now", NOW, "check", str(DRAFT)]), 0)

    def test_same_draft_fails_when_scheduled_without_approval(self):
        cfg = self.copy_config()
        data = yaml.safe_load(DRAFT.read_text())
        data["posts"][0]["status"] = "scheduled"
        batch = cfg / "b.yaml"
        batch.write_text(yaml.safe_dump(data))
        self.assertEqual(cli.main(["--config-dir", str(cfg), "--now", NOW, "check", str(batch)]), 1)

    def test_draft_before_dm_date_is_blocked(self):
        cfg = self.copy_config()
        data = yaml.safe_load(DRAFT.read_text())
        data["posts"][0]["scheduled_at"] = "2026-11-17T11:00:00-05:00"
        data["posts"][0]["story_drafts"][0]["scheduled_at"] = "2026-11-17T17:00:00-05:00"
        batch = cfg / "b.yaml"
        batch.write_text(yaml.safe_dump(data))
        self.assertEqual(cli.main(["--config-dir", str(cfg), "--now", NOW, "check", str(batch)]), 1)


if __name__ == "__main__":
    unittest.main()
