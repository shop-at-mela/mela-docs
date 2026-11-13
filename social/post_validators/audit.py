"""Replay existing posts through the validators and print a report."""
from __future__ import annotations

from collections import Counter

from .config import Context
from .engine import run_all
from .model import Post, Violation

RULE_NAMES = {1: "brand coverage", 2: "cadence", 3: "people quota", 4: "rights", 5: "format mix",
              6: "copy", 7: "link rule", 8: "freeze list"}


def coverage_table(ctx: Context) -> tuple[list[tuple[str, int]], list[str], list[tuple[str, int]]]:
    counts: Counter = Counter()
    for p in ctx.ledger:
        for b in set(p.brands):
            counts[b] += 1
    listed = sorted(ctx.roster.listed)
    rows = sorted(((b, counts[b]) for b in listed), key=lambda r: (-r[1], r[0]))
    zero = [b for b in listed if counts[b] == 0]
    unlisted = sorted(((b, n) for b, n in counts.items() if b not in ctx.roster.listed), key=lambda r: -r[1])
    return rows, zero, unlisted


def replay(ctx: Context) -> list[Violation]:
    """Treat every ledger post as a new post in one batch, against an empty history."""
    posts = [Post(**{**p.__dict__}) for p in ctx.ledger]
    saved = ctx.ledger
    ctx.ledger = []
    try:
        return run_all(ctx, posts, [])
    finally:
        ctx.ledger = saved


def report(ctx: Context, violations: list[Violation], window_label: str, focus_date: str = "") -> str:
    out: list[str] = []
    a = out.append
    posts = ctx.ledger
    a(f"# Dry run report ({window_label})")
    a("")
    a(f"Posts replayed: {len(posts)}  (confirmed live: {sum(1 for p in posts if p.confirmed)}, "
      f"logged as scheduled: {sum(1 for p in posts if not p.confirmed)})")
    a(f"Roster: {ctx.roster.source}, {len(ctx.roster.listed)} brands listed, fetched {ctx.roster.fetched_at:%Y-%m-%d %H:%M} UTC")
    a("")
    a("## Violations by rule")
    a("")
    a("| Rule | Name | Violations | Posts affected |")
    a("|---|---|---|---|")
    for r in range(1, 9):
        vs = [v for v in violations if v.rule == r]
        a(f"| {r} | {RULE_NAMES[r]} | {len(vs)} | {len({v.post for v in vs})} |")
    a("")
    a("## 1. Five posts in four minutes (rule 2)")
    a("")
    gap = ctx.settings["cadence"]["min_hours_between_posts"]
    timed = sorted((p for p in posts if p.format in ctx.settings["cadence"]["feed_formats"] and p.when and p.precision == "exact"),
                   key=Post.sort_key)
    clusters, cur = [], []
    for p in timed:
        if cur and (p.when - cur[-1].when).total_seconds() < gap * 3600:
            cur.append(p)
        else:
            if len(cur) > 1:
                clusters.append(cur)
            cur = [p]
    if len(cur) > 1:
        clusters.append(cur)
    for c in clusters:
        span = int((c[-1].when - c[0].when).total_seconds() // 60)
        a(f"- {c[0].when.astimezone(ctx.tz):%Y-%m-%d %H:%M} America/New_York: **{len(c)} posts in {span} min** "
          f"(rule: {gap}h apart, 1 per day). Posts: " + ", ".join(f"`{p.id}`" for p in c))
    if not clusters:
        a("- none flagged")
    a("")
    a("## 2. People quota (rule 3)")
    a("")
    tagged = [p for p in posts if p.people_present is not None]
    a(f"- {len(tagged)} of {len(posts)} posts carry a people_present tag. The rest are untagged, so the quota cannot pass.")
    for v in [v for v in violations if v.rule == 3][:3]:
        a(f"- `{v.post}`: {v.message}")
    a("")
    a("## 3. Brand coverage (rule 1)")
    a("")
    rows, zero, unlisted = coverage_table(ctx)
    a("| Brand | Named posts in ledger |")
    a("|---|---|")
    for b, n in rows:
        a(f"| {b} | {n} |")
    a("")
    a(f"- Listed brands with zero named posts: {', '.join(zero) or 'none'}")
    top = rows[0] if rows else None
    if top and zero:
        a(f"- Most posted brand: **{top[0]} ({top[1]})** while {len(zero)} listed brands have none.")
    a("")
    a("## 4. Posts about brands not on the site (rule 1)")
    a("")
    for b, n in unlisted:
        a(f"- **{b}**: {n} ledger post(s), brand is not on shopatmela.com/brands")
    if not unlisted:
        a("- none")
    a("")
    if focus_date:
        ids = {p.id for p in posts if p.when and p.when.astimezone(ctx.tz).date().isoformat() == focus_date}
        a(f"## The {focus_date} batch as it would be checked today")
        a("")
        a(f"{len(ids)} posts: " + ", ".join(f"`{i}`" for i in sorted(ids)))
        a("")
        for r in range(1, 8):
            vs = [v for v in violations if v.rule == r and v.post in ids]
            if vs:
                a(f"- Rule {r} ({RULE_NAMES[r]}): {len(vs)} violations on {len({v.post for v in vs})} of {len(ids)} posts. e.g. {vs[0].message}")
        a("")
    a("## Other rules on old posts")
    a("")
    for r in (4, 5, 6, 7):
        vs = [v for v in violations if v.rule == r]
        a(f"- Rule {r} ({RULE_NAMES[r]}): {len(vs)} violations. Example: " + (f"`{vs[0].post}`: {vs[0].message}" if vs else "none"))
    a("- Rule 2 approval: no old post has a recorded approval, so each fails on that.")
    a("- Rule 8 does not apply to a replay (it checks archive, edit, delete and pin operations).")
    a("")
    a("## Caveats")
    a("")
    a("- The ledger is built from social/log, not from Instagram. It does not reproduce the account's 54 posts "
      "or Vilvah's 6 named posts. Add missing posts in config/ledger_overrides.yaml, then rerun.")
    a("- Times for the 5 Nov 11 posts are estimated from the report 'five posts in four minutes' (see ledger_overrides.yaml). "
      "Most older posts have a date only, so the 6 hour check skips them.")
    a("- Old posts inferred as brand assets: logs show scenes built from each brand's own product photos.")
    return "\n".join(out)
