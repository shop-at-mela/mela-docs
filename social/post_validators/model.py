from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from typing import Any, Optional
from zoneinfo import ZoneInfo

APPROVED_STATUSES = {"ready", "scheduled", "published", "live", "posted"}


def parse_when(value: Any, tz: ZoneInfo) -> tuple[Optional[dt.datetime], str]:
    """Return (datetime, precision). precision is exact, date (noon local) or none."""
    if value is None or value == "":
        return None, "none"
    if isinstance(value, dt.datetime):
        return (value if value.tzinfo else value.replace(tzinfo=tz)), "exact"
    if isinstance(value, dt.date):
        return dt.datetime(value.year, value.month, value.day, 12, tzinfo=tz), "date"
    text = str(value).strip()
    try:
        if len(text) == 10:
            d = dt.date.fromisoformat(text)
            return dt.datetime(d.year, d.month, d.day, 12, tzinfo=tz), "date"
        parsed = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
        return (parsed if parsed.tzinfo else parsed.replace(tzinfo=tz)), "exact"
    except ValueError:
        return None, "none"


@dataclass
class Violation:
    rule: int
    name: str
    post: str
    message: str
    fix: str

    def format(self) -> str:
        return f"FAIL rule {self.rule} ({self.name}) post={self.post}: {self.message}\n     fix: {self.fix}"

    def as_dict(self) -> dict:
        return {"rule": self.rule, "name": self.name, "post": self.post, "message": self.message, "fix": self.fix}


@dataclass
class Post:
    id: str
    status: str = "draft"
    format: str = "carousel"
    when: Optional[dt.datetime] = None
    precision: str = "none"
    brands: list[str] = field(default_factory=list)
    caption: str = ""
    media: list[dict] = field(default_factory=list)
    people_present: Optional[bool] = None
    cover_kind: Optional[str] = None
    voice: Optional[str] = None
    person_speaks: bool = False
    approval: Optional[dict] = None
    story_drafts: list[dict] = field(default_factory=list)
    first_second_face_or_hands: Optional[bool] = None
    pinned: bool = False
    auto_publish: bool = False
    source: str = ""
    confirmed: bool = True

    @classmethod
    def from_dict(cls, d: dict, tz: ZoneInfo) -> "Post":
        when, precision = parse_when(d.get("scheduled_at") or d.get("posted_at"), tz)
        return cls(
            id=str(d["id"]),
            status=str(d.get("status", "draft")),
            format=str(d.get("format", "carousel")),
            when=when,
            precision=d.get("time_precision") or precision,
            brands=list(d.get("brands") or []),
            caption=str(d.get("caption") or ""),
            media=list(d.get("media") or []),
            people_present=d.get("people_present"),
            cover_kind=d.get("cover_kind"),
            voice=d.get("voice"),
            person_speaks=bool(d.get("person_speaks", False)),
            approval=d.get("approval"),
            story_drafts=list(d.get("story_drafts") or []),
            first_second_face_or_hands=d.get("first_second_face_or_hands"),
            pinned=bool(d.get("pinned", False)),
            auto_publish=bool(d.get("auto_publish", False)),
            source=str(d.get("source", "")),
            confirmed=bool(d.get("confirmed", True)),
        )

    def sort_key(self):
        return (self.when is None, self.when or dt.datetime.max.replace(tzinfo=dt.timezone.utc), self.id)
