from __future__ import annotations

import datetime as dt
import re
import urllib.request
from dataclasses import dataclass
from typing import Optional


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


class RosterError(Exception):
    """Roster unavailable or stale. Validation fails closed."""


@dataclass
class Roster:
    entries: list[dict]          # canonical entries from config (slug, name, aliases)
    listed: set[str]             # slugs currently listed
    source: str                  # live | snapshot
    fetched_at: Optional[dt.datetime] = None

    def names(self, slug: str) -> set[str]:
        for e in self.entries:
            if e["slug"] == slug:
                return {norm(slug), norm(e["name"]), *(norm(a) for a in e.get("aliases", []))}
        return {norm(slug)}

    def resolve(self, text: str) -> Optional[str]:
        t = norm(text)
        for e in self.entries:
            if t in self.names(e["slug"]):
                return e["slug"]
        return None


def from_snapshot(cfg: dict, now: dt.datetime, allow_stale: bool = False) -> Roster:
    snap = cfg["snapshot"]
    fetched = dt.datetime.fromisoformat(str(snap["fetched_at"]).replace("Z", "+00:00"))
    age_h = (now - fetched).total_seconds() / 3600
    if age_h > float(snap.get("max_age_hours", 48)) and not allow_stale:
        raise RosterError(
            f"Roster snapshot is {age_h:.0f}h old (max {snap.get('max_age_hours', 48)}h). "
            "Fix: run `python3 -m post_validators roster-update` where shopatmela.com is reachable, "
            "or pass --live-roster."
        )
    brands = snap["brands"]
    return Roster(entries=brands, listed={b["slug"] for b in brands}, source="snapshot", fetched_at=fetched)


def parse_live_html(html: str) -> set[str]:
    """Brand path segments from links like /brands/<slug>."""
    return {m.group(1).lower() for m in re.finditer(r'href=["\'](?:https?://[^/"\']+)?/brands/([a-z0-9][a-z0-9-]*)', html, re.I)}


def fetch_live_html(url: str = "https://shopatmela.com/brands", timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "mela-post-validators/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310 - fixed https URL
        return r.read().decode("utf-8", "replace")


def from_live(cfg: dict, now: dt.datetime, html: Optional[str] = None) -> Roster:
    try:
        html = html if html is not None else fetch_live_html()
    except Exception as exc:  # network errors fail closed
        raise RosterError(f"Could not read live roster from shopatmela.com/brands: {exc}. Fix: retry, or use a fresh snapshot.") from exc
    segs = {norm(s) for s in parse_live_html(html)}
    if not segs:
        raise RosterError("Live roster page had no /brands/<slug> links. Fix: check the page, then retry.")
    entries = cfg["snapshot"]["brands"]
    probe = Roster(entries=entries, listed=set(), source="live", fetched_at=now)
    listed = {e["slug"] for e in entries if probe.names(e["slug"]) & segs}
    return Roster(entries=entries, listed=listed, source="live", fetched_at=now)
