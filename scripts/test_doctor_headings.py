#!/usr/bin/env python3
"""Regression coverage for required-heading detection in workflow_doctor.

Headings are matched on their own line. Substring matching was wrong in both
directions: an inline mention of a heading inside prose satisfied a
required-section check, and the same mention hijacked where section_body()
started reading.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCTOR = ROOT / "skills" / "repo-continuity" / "scripts" / "workflow_doctor.py"


class CheckFailure(RuntimeError):
    pass


def load_doctor():
    spec = importlib.util.spec_from_file_location("workflow_doctor", DOCTOR)
    if spec is None or spec.loader is None:
        raise CheckFailure(f"cannot import {DOCTOR}")
    module = importlib.util.module_from_spec(spec)
    # Register before executing: @dataclass resolves cls.__module__ via sys.modules.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def present(module, text: str, heading: str) -> bool:
    finder = getattr(module, "find_heading", None)
    if finder is None:  # pre-fix build: fall back to the old substring test
        return heading in text
    return finder(text, heading) is not None


def check_inline_mention_is_not_a_heading(module) -> None:
    # A record that only *talks about* the heading must still count as missing.
    text = "# Title\n\nSee `## Goal And Acceptance` in the template for the shape.\n"
    if present(module, text, "## Goal And Acceptance"):
        raise CheckFailure("an inline mention must not satisfy a required heading")


def check_real_heading_is_found(module) -> None:
    text = "# Title\n\n## Goal And Acceptance\n\n- Goal: ship it\n"
    if not present(module, text, "## Goal And Acceptance"):
        raise CheckFailure("a real heading on its own line must be found")


def check_case_variant_is_found(module) -> None:
    # Present but differently cased. Reporting it missing is factually wrong.
    text = "# Title\n\n## Goal and acceptance\n\n- Goal: ship it\n"
    if not present(module, text, "## Goal And Acceptance"):
        raise CheckFailure("a case-variant heading is present and must be found")


def check_trailing_suffix_is_tolerated(module) -> None:
    # Pre-existing substring matching accepted a suffix, including one attached
    # without a separating space. Real records rely on it.
    for suffix in (" Evidence", "（执行 agent 接手入口）", " — 2026-07-16"):
        text = f"# Title\n\n## Context Pack{suffix}\n\n- fact\n"
        if not present(module, text, "## Context Pack"):
            raise CheckFailure(f"a heading suffix must stay tolerated, failed on {suffix!r}")


def check_level_three_is_not_a_level_two_heading(module) -> None:
    # Deliberate tightening: '### X' contains '## X' as a substring, so the old
    # match accepted a subsection in place of the required section.
    text = "# Title\n\n## Other\n\n### Context Pack\n\n- fact\n"
    if present(module, text, "## Context Pack"):
        raise CheckFailure("a level-3 heading must not satisfy a level-2 requirement")


def check_section_body_ignores_inline_mention(module) -> None:
    text = (
        "# Title\n"
        "\n"
        "Out of scope: rows under `## Experience Candidates` are unchanged.\n"
        "| bogus | row | that | must | not | be read |\n"
        "\n"
        "## Experience Candidates\n"
        "\n"
        "| real | row |\n"
    )
    body = module.section_body(text, "Experience Candidates")
    if "bogus" in body:
        raise CheckFailure("section_body must start at the heading line, not a mention")
    if "real" not in body:
        raise CheckFailure("section_body must return the real section content")


def check_section_body_stops_at_next_heading(module) -> None:
    text = "## A\n\nkeep\n\n### Sub\n\nalso keep\n\n## B\n\ndrop\n"
    body = module.section_body(text, "A")
    if "keep" not in body or "also keep" not in body:
        raise CheckFailure("section_body must include level-3 subsections")
    if "drop" in body:
        raise CheckFailure("section_body must stop at the next level-2 heading")


def check_absent_heading_returns_empty(module) -> None:
    if module.section_body("# Title\n\nnothing here\n", "Validation") != "":
        raise CheckFailure("an absent heading must yield an empty body")


def main() -> int:
    try:
        module = load_doctor()
        check_inline_mention_is_not_a_heading(module)
        check_real_heading_is_found(module)
        check_case_variant_is_found(module)
        check_trailing_suffix_is_tolerated(module)
        check_level_three_is_not_a_level_two_heading(module)
        check_section_body_ignores_inline_mention(module)
        check_section_body_stops_at_next_heading(module)
        check_absent_heading_returns_empty(module)
    except CheckFailure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("PASS: required headings are matched per line, not by substring")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
