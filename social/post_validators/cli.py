from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

import yaml

from . import audit as audit_mod
from . import ledger as ledger_mod
from .config import DEFAULT_CONFIG_DIR, Context, load_context
from .engine import run_all
from .model import Post
from .roster import RosterError, fetch_live_html, norm, parse_live_html


def _ctx(args) -> Context:
    now = dt.datetime.fromisoformat(args.now.replace("Z", "+00:00")) if args.now else None
    return load_context(Path(args.config_dir), now=now, live_roster=args.live_roster,
                        allow_stale_roster=getattr(args, "allow_stale_roster", False))


def cmd_check(args) -> int:
    ctx = _ctx(args)
    data = yaml.safe_load(Path(args.batch).read_text(encoding="utf-8")) or {}
    batch = [Post.from_dict(p, ctx.tz) for p in data.get("posts", [])]
    violations = run_all(ctx, batch, data.get("operations", []))
    if args.json:
        print(json.dumps([v.as_dict() for v in violations], indent=2))
    else:
        for v in violations:
            print(v.format())
        print(f"\n{len(batch)} post(s) checked, {len(violations)} violation(s). " +
              ("BLOCKED: do not schedule." if violations else "PASS: safe to hand to a human for approval."))
    return 1 if violations else 0


def cmd_audit(args) -> int:
    args.allow_stale_roster = True
    ctx = _ctx(args)
    violations = audit_mod.replay(ctx)
    text = audit_mod.report(ctx, violations, f"replay of config/ledger.yaml, run {ctx.now:%Y-%m-%d}", args.focus_date or "")
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)
    if args.violations_out:
        Path(args.violations_out).write_text("\n".join(v.format() for v in violations) + "\n", encoding="utf-8")
    return 0


def cmd_import_ledger(args) -> int:
    cfg = Path(args.config_dir)
    ov_path = cfg / "ledger_overrides.yaml"
    overrides = (yaml.safe_load(ov_path.read_text(encoding="utf-8")) or {}).get("posts", {}) if ov_path.exists() else {}
    posts = ledger_mod.build(Path(args.logs), overrides, {})
    ledger_mod.write(cfg / "ledger.yaml", posts)
    print(f"wrote {cfg / 'ledger.yaml'} with {len(posts)} posts")
    return 0


def cmd_roster_update(args) -> int:
    cfg_path = Path(args.config_dir) / "roster.yaml"
    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
    try:
        segs = {norm(s) for s in parse_live_html(fetch_live_html())}
    except Exception as exc:
        print(f"Could not read shopatmela.com/brands: {exc}", file=sys.stderr)
        return 2
    entries = cfg["snapshot"]["brands"]
    known: set[str] = set()
    for e in entries:
        names = {norm(e["slug"]), norm(e["name"]), *(norm(a) for a in e.get("aliases", []))}
        known |= names
        if not names & segs:
            print(f"NOT LISTED any more: {e['slug']}  -> remove it from roster.yaml")
    for s in sorted(segs - known):
        print(f"NEW on site: /brands/{s}  -> add it to roster.yaml")
    text = cfg_path.read_text(encoding="utf-8")
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cfg_path.write_text(re.sub(r'(fetched_at:\s*)"[^"]*"', rf'\1"{stamp}"', text, count=1), encoding="utf-8")
    print(f"snapshot fetched_at set to {stamp}. Fix any lines above, then rerun.")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="post_validators", description="Hard-fail checks before scheduling Instagram posts.")
    p.add_argument("--config-dir", default=str(DEFAULT_CONFIG_DIR))
    p.add_argument("--now", help="ISO time to treat as now (tests, dry runs)")
    p.add_argument("--live-roster", action="store_true", help="read shopatmela.com/brands now instead of the snapshot")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="validate a batch file before scheduling")
    c.add_argument("batch")
    c.add_argument("--json", action="store_true")
    c.set_defaults(fn=cmd_check)
    a = sub.add_parser("audit", help="replay config/ledger.yaml through all rules")
    a.add_argument("--out")
    a.add_argument("--violations-out")
    a.add_argument("--focus-date", help="YYYY-MM-DD to break out (for example 2026-11-11)")
    a.set_defaults(fn=cmd_audit)
    i = sub.add_parser("import-ledger", help="rebuild config/ledger.yaml from social/log")
    i.add_argument("--logs", default=str(DEFAULT_CONFIG_DIR.parent / "log"))
    i.set_defaults(fn=cmd_import_ledger)
    r = sub.add_parser("roster-update", help="re-read shopatmela.com/brands and refresh the snapshot time")
    r.set_defaults(fn=cmd_roster_update)
    args = p.parse_args(argv)
    try:
        return args.fn(args)
    except RosterError as exc:
        print(f"ROSTER ERROR (failing closed): {exc}", file=sys.stderr)
        return 2
