from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional
from zoneinfo import ZoneInfo

import yaml

from .model import Post
from .roster import Roster, from_live, from_snapshot

DEFAULT_CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


def _load(path: Path) -> Any:
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


@dataclass
class Context:
    settings: dict
    roster_cfg: dict
    roster: Roster
    permissions: dict
    claims: dict
    freeze: dict
    ledger: list[Post]
    now: dt.datetime
    tz: ZoneInfo
    config_dir: Path = field(default=DEFAULT_CONFIG_DIR)


def load_ledger(config_dir: Path, tz: ZoneInfo) -> list[Post]:
    ledger_path = config_dir / "ledger.yaml"
    if not ledger_path.exists():
        return []
    raw = _load(ledger_path).get("posts", [])
    tags_path = config_dir / "post_tags.yaml"
    tags = (_load(tags_path).get("tags") or {}) if tags_path.exists() else {}
    posts = []
    for d in raw:
        d = dict(d)
        d.update(tags.get(d["id"], {}))
        posts.append(Post.from_dict(d, tz))
    return posts


def load_context(config_dir: Optional[Path] = None, now: Optional[dt.datetime] = None,
                 live_roster: bool = False, allow_stale_roster: bool = False,
                 live_html: Optional[str] = None) -> Context:
    config_dir = Path(config_dir or DEFAULT_CONFIG_DIR)
    settings = _load(config_dir / "settings.yaml")
    tz = ZoneInfo(settings["timezone"])
    now = now or dt.datetime.now(tz)
    roster_cfg = _load(config_dir / "roster.yaml")
    roster = from_live(roster_cfg, now, live_html) if live_roster else from_snapshot(roster_cfg, now, allow_stale_roster)
    return Context(
        settings=settings,
        roster_cfg=roster_cfg,
        roster=roster,
        permissions=_load(config_dir / "permissions.yaml"),
        claims=(_load(config_dir / "verified_claims.yaml").get("brands") or {}),
        freeze=_load(config_dir / "freeze.yaml"),
        ledger=load_ledger(config_dir, tz),
        now=now,
        tz=tz,
        config_dir=config_dir,
    )
