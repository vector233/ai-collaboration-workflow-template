#!/usr/bin/env python3
"""Regression coverage for wiki-link scanning in workflow_doctor.

Wiki links are not links inside code. A runbook that documents a shell
conditional such as `[[ "$rc" == "0" ]]` must not be reported as containing a
broken wiki link, while real links outside code must still be scanned.
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
    sys.path.insert(0, str(DOCTOR.parent))
    spec = importlib.util.spec_from_file_location("workflow_doctor", DOCTOR)
    if spec is None or spec.loader is None:
        raise CheckFailure(f"cannot import {DOCTOR}")
    module = importlib.util.module_from_spec(spec)
    # Register before executing: @dataclass resolves cls.__module__ via sys.modules.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def targets(module, text: str) -> list[str]:
    # Fall back to identity so a build without strip_code fails on the actual
    # false positive rather than on a missing attribute.
    strip = getattr(module, "strip_code", lambda value: value)
    return [
        raw.strip().removesuffix(".md")
        for raw in module.WIKI_LINK_RE.findall(strip(text))
    ]


def check_fenced_shell_conditional(module) -> None:
    text = (
        "See [[architecture]] for the flow.\n"
        "\n"
        "```\n"
        '[[ "$install_rc" == "0" && "$diag_present" == "true" ]]\n'
        "```\n"
    )
    found = targets(module, text)
    if found != ["architecture"]:
        raise CheckFailure(f"fenced shell conditional must be skipped, got {found}")


def check_tilde_and_language_fences(module) -> None:
    text = "~~~bash\n[[ -f x ]]\n~~~\n\n```sh\n[[ -d y ]]\n```\n\n[[gotchas]]\n"
    found = targets(module, text)
    if found != ["gotchas"]:
        raise CheckFailure(f"tilde/language fences must be skipped, got {found}")


def check_inline_code(module) -> None:
    text = "Write `[[work/README]]` verbatim, then link [[decisions]].\n"
    found = targets(module, text)
    if found != ["decisions"]:
        raise CheckFailure(f"inline code must be skipped, got {found}")


def check_real_links_survive(module) -> None:
    text = "[[project]] and [[work/README]] and [[a|alias]] and [[b#anchor]]\n"
    found = targets(module, text)
    if found != ["project", "work/README", "a", "b"]:
        raise CheckFailure(f"links outside code must still be scanned, got {found}")


def check_line_numbers_preserved(module) -> None:
    text = "a\n```\nb\nc\n```\nd\n"
    if module.strip_code(text).count("\n") != text.count("\n"):
        raise CheckFailure("stripping code must preserve line count")


def check_unclosed_fence(module) -> None:
    text = "intro [[project]]\n\n```\n[[ -f x ]]\n"
    found = targets(module, text)
    if found != ["project"]:
        raise CheckFailure(f"unclosed fence must swallow to end of file, got {found}")


def main() -> int:
    try:
        module = load_doctor()
        check_fenced_shell_conditional(module)
        check_tilde_and_language_fences(module)
        check_inline_code(module)
        check_real_links_survive(module)
        check_line_numbers_preserved(module)
        check_unclosed_fence(module)
    except CheckFailure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("PASS: wiki-link scanning ignores code and keeps real links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
