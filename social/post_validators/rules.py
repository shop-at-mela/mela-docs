"""One function per rule. Each returns a list of Violation. All are hard fails."""
from __future__ import annotations

import datetime as dt
import math
import re
from collections import Counter
from urllib.parse import parse_qs, urlparse

from .config import Context
from .model import APPROVED_STATUSES, Post, Violation, parse_when
from .roster import norm

SANA_FIX = "Default to a founder led post: Sana on camera, or Sana wearing or using a product she owns."


def _feed(ctx: Context, p: Post) -> bool:
    return p.format in ctx.settings["cadence"]["feed_formats"]


def _day(ctx: Context, when: dt.datetime) -> dt.date:
    return when.astimezone(ctx.tz).date()


# ---------------------------------------------------------------- rule 1
def rule1_brand_coverage(ctx: Context, batch: list[Post]) -> list[Violation]:
    out: list[Violation] = []
    name = "brand coverage"
    counts: Counter = Counter()
    for p in ctx.ledger:
        for b in set(p.brands):
            counts[b] += 1
    listed = ctx.roster.listed
    priority = [b for b in ctx.roster_cfg.get("priority_gaps", []) if b in listed]
    dm_dates = ctx.roster_cfg.get("first_outreach_dm_dates", {})
    for p in sorted(batch, key=Post.sort_key):
        named = list(dict.fromkeys(p.brands))
        for b in named:
            if b not in listed:
                out.append(Violation(1, name, p.id, f"Brand '{b}' is not currently listed on shopatmela.com/brands.",
                                     "Remove the brand from this post. Add it to config/roster.yaml only after it is listed."))
                continue
            if counts[b] >= 1:
                gaps = [g for g in priority if counts[g] == 0] + \
                       [g for g in sorted(listed) if counts[g] == 0 and g not in priority]
                if gaps:
                    out.append(Violation(1, name, p.id,
                        f"'{b}' already has {counts[b]} named post(s) and these listed brands have none: {', '.join(gaps)}.",
                        f"Post about {gaps[0]} first, after its outreach DM date. No second post for any brand until every listed brand has a first."))
            else:
                dm = dm_dates.get(b)
                if not dm:
                    out.append(Violation(1, name, p.id, f"First post for '{b}' has no outreach DM date in config.",
                                         "Add the brand's first outreach DM date to first_outreach_dm_dates in config/roster.yaml."))
                    continue
                dm_day = dt.date.fromisoformat(str(dm))
                earliest = dt.datetime.combine(dm_day + dt.timedelta(days=1), dt.time(0), tzinfo=ctx.tz)
                if p.when is None or p.when < earliest:
                    out.append(Violation(1, name, p.id,
                        f"First post for '{b}' is scheduled {p.when.isoformat() if p.when else 'with no time'}, "
                        f"but its outreach DM date is {dm}.",
                        f"Schedule it on or after {earliest.date().isoformat()} 00:00 America/New_York."))
        for b in named:
            if b in listed:
                counts[b] += 1
    return out


# ---------------------------------------------------------------- rule 2
def rule2_cadence(ctx: Context, batch: list[Post]) -> list[Violation]:
    out: list[Violation] = []
    name = "cadence"
    c = ctx.settings["cadence"]
    existing = [p for p in ctx.ledger if _feed(ctx, p) and p.when]
    for p in sorted(batch, key=Post.sort_key):
        if p.status in APPROVED_STATUSES or p.status == "scheduled":
            ap = p.approval or {}
            by = str(ap.get("approved_by", "")).strip()
            at, _ = parse_when(ap.get("approved_at"), ctx.tz)
            if not by or by.lower() in {n.lower() for n in c["automation_approver_names"]}:
                out.append(Violation(2, name, p.id, "No recorded human approval.",
                                     "Record approval.approved_by (a person) and approval.approved_at before scheduling."))
            elif at is None:
                out.append(Violation(2, name, p.id, "Approval has no valid approved_at time.", "Record when the person approved."))
            elif p.when and at > p.when:
                out.append(Violation(2, name, p.id, "Approval was recorded after the publish time.", "Approve before the post is due."))
        if p.auto_publish:
            out.append(Violation(2, name, p.id, "Post is set to publish on its own.",
                                 "Set auto_publish to false. Automation drafts and schedules only."))
        if not (_feed(ctx, p) and p.when):
            continue
        others = existing + [q for q in batch if q is not p and _feed(ctx, q) and q.when]
        same_day = [q for q in others if _day(ctx, q.when) == _day(ctx, p.when)]
        if len(same_day) >= c["max_feed_posts_per_day"]:
            out.append(Violation(2, name, p.id,
                f"{len(same_day) + 1} feed posts on {_day(ctx, p.when)} (America/New_York). Max {c['max_feed_posts_per_day']}.",
                "Move this post to a day with no other feed post."))
        min_gap = dt.timedelta(hours=c["min_hours_between_posts"])
        for q in others:
            if p.precision == "exact" and q.precision == "exact" and abs(q.when - p.when) < min_gap:
                mins = int(abs((q.when - p.when).total_seconds()) // 60)
                out.append(Violation(2, name, p.id,
                    f"Scheduled {mins} min from post {q.id}. Batch rejected: posts must be {c['min_hours_between_posts']}h apart.",
                    f"Space the posts at least {c['min_hours_between_posts']} hours apart."))
        allp = others + [p]
        for a in allp:
            if a.when <= p.when < a.when + dt.timedelta(days=7):
                n = sum(1 for z in allp if a.when <= z.when < a.when + dt.timedelta(days=7))
                if n > c["max_feed_posts_per_rolling_7_days"]:
                    out.append(Violation(2, name, p.id,
                        f"{n} feed posts in the 7 days from {a.when.astimezone(ctx.tz):%Y-%m-%d %H:%M}. Max {c['max_feed_posts_per_rolling_7_days']}.",
                        "Drop or delay a post so no 7 day window has more than 4."))
                    break
    return out


# ---------------------------------------------------------------- rule 3
def rule3_people_quota(ctx: Context, batch: list[Post]) -> list[Violation]:
    out: list[Violation] = []
    name = "people quota"
    q = ctx.settings["people_quota"]
    window, need_full = q["window_posts"], q["min_people_posts"]
    history = sorted([p for p in ctx.ledger if _feed(ctx, p) and p.when], key=Post.sort_key)
    for p in sorted([b for b in batch if _feed(ctx, b)], key=Post.sort_key):
        win = history[-(window - 1):] + [p]
        need = need_full if len(win) >= window else math.ceil(len(win) * need_full / window)
        people = sum(1 for z in win if z.people_present is True)
        untagged = [z.id for z in win if z.people_present is None]
        if p.people_present is None:
            out.append(Violation(3, name, p.id, "Candidate has no people_present tag.",
                                 "Set people_present to true or false. The validator reads tags, it does not look at images."))
        elif untagged:
            out.append(Violation(3, name, p.id,
                f"{len(untagged)} of the last {len(win)} covers have no people_present tag ({', '.join(untagged[:4])}{'...' if len(untagged) > 4 else ''}).",
                "Tag those posts in config/post_tags.yaml so the quota can be checked."))
        elif people < need:
            out.append(Violation(3, name, p.id,
                f"Only {people} of the last {len(win)} covers show a person. Need {need}.",
                "Make this cover show a face, hands, or a worn product. " + SANA_FIX))
        if p.people_present is True and p.cover_kind in ("text_only", "product_staging"):
            out.append(Violation(3, name, p.id, f"people_present is true but cover_kind is {p.cover_kind}. Those do not count.",
                                 "Set people_present to false, or change the cover to show a person."))
        history.append(p)
    return out


# ---------------------------------------------------------------- rule 4
def rule4_rights(ctx: Context, batch: list[Post]) -> list[Violation]:
    out: list[Violation] = []
    name = "rights"
    default = ctx.permissions.get("default_state", "none")
    perms = ctx.permissions.get("brands") or {}
    for p in batch:
        scheduled = p.status in APPROVED_STATUSES or p.status == "scheduled"
        if not p.media:
            if scheduled:
                out.append(Violation(4, name, p.id, "Post is scheduled but lists no media, so image rights cannot be checked.",
                                     "List every image or video with its kind. Copy only drafts must stay in draft status."))
            continue
        for m in p.media:
            kind, brand, file = m.get("kind"), m.get("brand"), m.get("file", "?")
            if kind == "mela_shot":
                continue
            if kind == "owned_asset":
                if not (m.get("date") and m.get("source")):
                    out.append(Violation(4, name, p.id, f"owned_asset '{file}' has no date and source.",
                                         "Record when and where Mela made or bought this asset."))
                continue
            if kind != "brand_asset":
                out.append(Violation(4, name, p.id, f"Media '{file}' has unknown kind '{kind}'.",
                                     "Use mela_shot, owned_asset or brand_asset."))
                continue
            rec = perms.get(brand) or {}
            state = rec.get("state", default)
            if state == "none":
                out.append(Violation(4, name, p.id,
                    f"Image '{file}' is {brand}'s asset. Missing permission: permission_granted or collab_agreed from {brand}.",
                    f"Draft copy only. Use Mela shot media instead. {SANA_FIX}"))
            elif state in ("permission_granted", "collab_agreed", "owned_asset"):
                if not (rec.get("date") and rec.get("source")):
                    out.append(Violation(4, name, p.id, f"{brand} is marked {state} with no date and source.",
                                         f"Add date and source for {brand} in config/permissions.yaml."))
            else:
                out.append(Violation(4, name, p.id, f"{brand} has unknown permission state '{state}'.",
                                     "Use owned_asset, permission_granted, collab_agreed or none."))
    return out


# ---------------------------------------------------------------- rule 5
def rule5_format_mix(ctx: Context, batch: list[Post]) -> list[Violation]:
    out: list[Violation] = []
    name = "format mix"
    cfg = ctx.settings["format_mix"]
    video = set(cfg["video_formats"])
    feed = [p for p in batch if _feed(ctx, p)]
    if feed:
        n_video = sum(1 for p in feed if p.format in video)
        need = math.ceil(cfg["min_video_share"] * len(feed))
        if n_video < need:
            out.append(Violation(5, name, "(batch)",
                f"{n_video} of {len(feed)} new posts are video. Need at least {need} (6 per 10).",
                "Plan more Reels. Carousel only plans fail."))
    for p in feed:
        if p.format in video and p.first_second_face_or_hands is not True:
            out.append(Violation(5, name, p.id, "Reel checklist: face or hands visible in the first second is not true.",
                                 "Re-cut so a face or hands show in the first second, then set the checklist field to true."))
    return out


# ---------------------------------------------------------------- rule 6
def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [s.strip() for s in parts if s.strip() and not s.strip().startswith("#")]


def _verified(ctx: Context, p: Post, sentence: str) -> bool:
    want = " ".join(sentence.split())
    for b in p.brands:
        for e in ctx.claims.get(b) or []:
            src = str(e.get("source_url", ""))
            if (" ".join(str(e.get("line", "")).split()) == want and e.get("checked_on")
                    and src.startswith("https://shopatmela.com/")):
                return True
    return False


def rule6_copy(ctx: Context, batch: list[Post]) -> list[Violation]:
    out: list[Violation] = []
    name = "copy"
    c = ctx.settings["copy"]
    for p in batch:
        text = p.caption
        if not text:
            continue
        for ch in c["banned_characters"]:
            if ch in text:
                i = text.index(ch)
                out.append(Violation(6, name, p.id, f"Caption contains an em dash near '{text[max(0, i - 15):i + 15].strip()}'.",
                                     "Replace it with a period or comma and split into two short sentences."))
        for s in _sentences(text):
            words = len(s.split())
            if words > c["max_sentence_words"]:
                out.append(Violation(6, name, p.id, f"Sentence has {words} words (max {c['max_sentence_words']}): '{s[:60]}...'",
                                     "Split it into short sentences."))
                break
        if (p.voice or "").lower() != c["voice_required"]:
            out.append(Violation(6, name, p.id, f"Voice is '{p.voice}'. Captions must be in Sana's voice.",
                                 "Rewrite as Sana, founder of Mela, and set voice: sana."))
        if p.person_speaks and not re.search(c["first_person_pattern"], text):
            out.append(Violation(6, name, p.id, "A person speaks in this post but the caption has no first person.",
                                 "Write it in first person (I, my)."))
        for pat in c["singular_buyer_patterns"]:
            m = re.search(pat, text, re.I if "Sarah" not in pat else 0)
            if m:
                out.append(Violation(6, name, p.id, f"Singular buyer reference: '{m.group(0)}'.",
                                     "Cite buyer research only as a group, for example 'few shoppers'."))
                break
        claim_res = [re.compile(x, re.I) for x in c["claim_patterns"]]
        for s in _sentences(text):
            if any(r.search(s) for r in claim_res) and not _verified(ctx, p, s):
                out.append(Violation(6, name, p.id,
                    f"Unverified shipping, duties or returns claim: '{s}'.",
                    "Omit the line. Or add that exact line, a check date and the brand page URL to config/verified_claims.yaml after checking shopatmela.com."))
    return out


# ---------------------------------------------------------------- rule 7
def rule7_story_link(ctx: Context, batch: list[Post]) -> list[Violation]:
    out: list[Violation] = []
    name = "link rule"
    prefix = ctx.settings["link"]["brand_path_prefix"]
    hosts = set(ctx.settings["link"]["allowed_hosts"])
    for p in batch:
        if p.format == "story" or not p.brands:
            continue
        for b in dict.fromkeys(p.brands):
            story = next((s for s in p.story_drafts if s.get("brand") == b), None)
            if not story:
                out.append(Violation(7, name, p.id, f"No same day Story draft for brand '{b}'.",
                                     f"Add a story_drafts entry for {b} linking to shopatmela.com{prefix}{b} with the post id in a utm tag."))
                continue
            s_when, _ = parse_when(story.get("scheduled_at"), ctx.tz)
            if not (p.when and s_when and _day(ctx, s_when) == _day(ctx, p.when)):
                out.append(Violation(7, name, p.id, f"Story draft for '{b}' is not on the same day as the post.",
                                     "Schedule the Story on the post's calendar day (America/New_York)."))
            u = urlparse(str(story.get("link", "")))
            segs = [x for x in u.path.split("/") if x]
            ok_path = len(segs) >= 2 and "/" + segs[0] + "/" == prefix and norm(segs[1]) in ctx.roster.names(b)
            if u.scheme != "https" or u.netloc.lower() not in hosts or not ok_path:
                out.append(Violation(7, name, p.id, f"Story link '{story.get('link')}' is not {b}'s own page on shopatmela.com.",
                                     f"Link to https://shopatmela.com{prefix}<{b} page>. A homepage link fails."))
            utm_ok = any(k.startswith("utm_") and any(p.id in v for v in vals) for k, vals in parse_qs(u.query).items())
            if not utm_ok:
                out.append(Violation(7, name, p.id, "Story link has no UTM tag carrying the post id.",
                                     f"Add utm_content={p.id} to the Story link."))
    return out


# ---------------------------------------------------------------- rule 8
def rule8_freeze(ctx: Context, operations: list[dict]) -> list[Violation]:
    out: list[Violation] = []
    name = "freeze list"
    until = dt.datetime.combine(dt.date.fromisoformat(str(ctx.freeze["until"])), dt.time(0), tzinfo=ctx.tz)
    frozen = set(ctx.freeze.get("brands", []))
    by_id = {p.id: p for p in ctx.ledger}
    for op in operations or []:
        pid, kind = str(op.get("post_id")), str(op.get("type", "")).lower()
        target = by_id.get(pid)
        if kind in ("pin", "unpin") or (target and target.pinned):
            out.append(Violation(8, name, pid, f"Operation '{kind}' touches a pinned post or pins a post.",
                                 "Never in code. Pinning and pinned posts are managed manually in the app."))
            continue
        if kind in ("archive", "edit", "delete") and ctx.now < until:
            hit = sorted(frozen & set(target.brands)) if target else []
            if target is None:
                out.append(Violation(8, name, pid, f"Cannot confirm post '{pid}' is outside the freeze: it is not in the ledger.",
                                     "Add the post to the ledger with its brands, or drop the operation."))
            elif hit:
                out.append(Violation(8, name, pid, f"Cannot {kind} a post about {', '.join(hit)} before {ctx.freeze['until']} (outreach freeze).",
                                     f"Wait until {ctx.freeze['until']}, or drop the operation."))
    return out
