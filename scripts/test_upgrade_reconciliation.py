#!/usr/bin/env python3
"""Regression coverage for three-way upgrade reconciliation.

The distribution smoke test only exercises initialization (`--target`), so the
`--upgrade-apply` reconciliation path shipped without coverage. These checks
pin the contract of `merge_upgrade_content`: a clean merge returns content,
any conflicting merge returns None so the caller preserves the local file, and
only a real `git merge-file` failure raises.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "skills" / "repo-continuity" / "scripts" / "bootstrap_template.py"


class CheckFailure(RuntimeError):
    pass


def load_bootstrap():
    spec = importlib.util.spec_from_file_location("bootstrap_template", BOOTSTRAP)
    if spec is None or spec.loader is None:
        raise CheckFailure(f"cannot import {BOOTSTRAP}")
    module = importlib.util.module_from_spec(spec)
    # Register before executing: @dataclass resolves cls.__module__ via sys.modules.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def build_sources(conflicts: int) -> tuple[bytes, bytes, bytes]:
    """Build baseline/local/upstream text with N separated conflict regions.

    Regions are padded so git cannot coalesce them into a single conflict;
    the number of conflict regions is what git reports as its exit code.
    """
    baseline: list[str] = []
    local: list[str] = []
    upstream: list[str] = []
    for region in range(conflicts):
        for line in range(10):
            padding = f"context-{region}-{line}"
            baseline.append(padding)
            local.append(padding)
            upstream.append(padding)
        baseline.append(f"baseline-{region}")
        local.append(f"local-{region}")
        upstream.append(f"upstream-{region}")
    encode = lambda rows: ("\n".join(rows) + "\n").encode("utf-8")
    return encode(local), encode(baseline), encode(upstream)


def check_clean_merge(merge) -> None:
    baseline = b"shared\nbaseline-only\ntrailing\n"
    local = b"local-edit\nbaseline-only\ntrailing\n"
    upstream = b"shared\nbaseline-only\nupstream-edit\n"
    merged = merge(local, baseline, upstream)
    if merged is None:
        raise CheckFailure("non-overlapping edits must merge cleanly, got a conflict")
    if b"<<<<<<<" in merged:
        raise CheckFailure("clean merge must not contain conflict markers")
    if b"local-edit" not in merged or b"upstream-edit" not in merged:
        raise CheckFailure("clean merge must retain both sides")


def check_conflicts_preserve_local(merge) -> None:
    # One conflict already worked. Two or more is the regression: git reports
    # the conflict count as its exit code, so `== 1` misread 2+ as a failure
    # and aborted the whole upgrade instead of preserving the local file.
    for conflicts in (1, 2, 3, 7):
        local, baseline, upstream = build_sources(conflicts)
        result = merge(local, baseline, upstream)
        if result is not None:
            raise CheckFailure(
                f"{conflicts} conflicting region(s) must return None, got merged content"
            )


def check_binary_is_skipped(merge) -> None:
    if merge(b"local\0", b"baseline\0", b"upstream\0") is not None:
        raise CheckFailure("binary content must be skipped")


def main() -> int:
    try:
        module = load_bootstrap()
        merge = module.merge_upgrade_content
        check_clean_merge(merge)
        check_conflicts_preserve_local(merge)
        check_binary_is_skipped(merge)
    except CheckFailure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("PASS: three-way upgrade reconciliation preserves local files on conflict")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
