from __future__ import annotations

from .config import Context
from .model import Post, Violation
from . import rules

POST_RULES = [
    rules.rule1_brand_coverage, rules.rule2_cadence, rules.rule3_people_quota, rules.rule4_rights,
    rules.rule5_format_mix, rules.rule6_copy, rules.rule7_story_link,
]


def run_all(ctx: Context, batch: list[Post], operations: list[dict] | None = None) -> list[Violation]:
    found: list[Violation] = []
    for rule in POST_RULES:
        found += rule(ctx, batch)
    found += rules.rule8_freeze(ctx, operations or [])
    return sorted(found, key=lambda v: (v.rule, v.post))
