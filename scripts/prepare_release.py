#!/usr/bin/env python3
"""Check or update every canonical Repo Continuity release-version surface."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION_TEXT = (
    r"v(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
)
VERSION_PATTERN = re.compile(rf"^{VERSION_TEXT}$")


@dataclass(frozen=True)
class VersionAnchor:
    path: Path
    pattern: re.Pattern[str]
    expected_matches: int
    label: str


ANCHORS = (
    VersionAnchor(
        Path("README.md"),
        re.compile(rf"pinned to the current release, `({VERSION_TEXT})`"),
        1,
        "English Quick Start release",
    ),
    VersionAnchor(
        Path("README.md"),
        re.compile(rf"repo-continuity/tree/({VERSION_TEXT})/skills/repo-continuity"),
        2,
        "English Skill install URLs",
    ),
    VersionAnchor(
        Path("README.md"),
        re.compile(rf"git clone --branch ({VERSION_TEXT}) --depth 1"),
        1,
        "English manual clone",
    ),
    VersionAnchor(
        Path("docs/zh-CN/README.md"),
        re.compile(rf"当前版本 `({VERSION_TEXT})`"),
        1,
        "Chinese Quick Start release",
    ),
    VersionAnchor(
        Path("docs/zh-CN/README.md"),
        re.compile(rf"repo-continuity/tree/({VERSION_TEXT})/skills/repo-continuity"),
        2,
        "Chinese Skill install URLs",
    ),
    VersionAnchor(
        Path("docs/zh-CN/README.md"),
        re.compile(rf"git clone --branch ({VERSION_TEXT}) --depth 1"),
        1,
        "Chinese manual clone",
    ),
    VersionAnchor(
        Path("scripts/validate_distribution.py"),
        re.compile(rf'^RELEASE_VERSION = "({VERSION_TEXT})"$', re.MULTILINE),
        1,
        "distribution validator release",
    ),
    VersionAnchor(
        Path("skills/repo-continuity/scripts/bootstrap_template.py"),
        re.compile(rf'^DEFAULT_REF = "({VERSION_TEXT})"$', re.MULTILINE),
        1,
        "Companion Skill default ref",
    ),
    VersionAnchor(
        Path("template/zettelkasten/AI.md"),
        re.compile(rf"Template baseline: `({VERSION_TEXT})`"),
        1,
        "payload baseline",
    ),
    VersionAnchor(
        Path("template/INIT.md"),
        re.compile(rf"Template baseline: `({VERSION_TEXT})`"),
        1,
        "initialization baseline example",
    ),
)


class ReleaseError(RuntimeError):
    pass


def load_contents() -> dict[Path, str]:
    contents: dict[Path, str] = {}
    for path in sorted({anchor.path for anchor in ANCHORS}):
        absolute = ROOT / path
        try:
            contents[path] = absolute.read_text(encoding="utf-8")
        except OSError as exc:
            raise ReleaseError(f"cannot read release surface {path}: {exc}") from exc
    return contents


def versions_for(
    contents: dict[Path, str],
) -> list[tuple[VersionAnchor, list[str]]]:
    found: list[tuple[VersionAnchor, list[str]]] = []
    for anchor in ANCHORS:
        versions = anchor.pattern.findall(contents[anchor.path])
        if len(versions) != anchor.expected_matches:
            raise ReleaseError(
                f"{anchor.label} expected {anchor.expected_matches} match(es), "
                f"found {len(versions)} in {anchor.path}"
            )
        found.append((anchor, versions))
    return found


def aligned_version(contents: dict[Path, str]) -> str:
    found = versions_for(contents)
    versions = {version for _, matches in found for version in matches}
    if len(versions) != 1:
        details = ", ".join(f"{anchor.label}={matches}" for anchor, matches in found)
        raise ReleaseError(f"release versions are not aligned: {details}")
    return versions.pop()


def replace_version(
    contents: dict[Path, str],
    old_version: str,
    new_version: str,
) -> dict[Path, str]:
    updated = dict(contents)
    for anchor in ANCHORS:
        text = updated[anchor.path]

        def replacement(match: re.Match[str]) -> str:
            if match.group(1) != old_version:
                raise ReleaseError(f"{anchor.label} changed during release preparation")
            return match.group(0).replace(old_version, new_version, 1)

        updated[anchor.path], count = anchor.pattern.subn(replacement, text)
        if count != anchor.expected_matches:
            raise ReleaseError(f"{anchor.label} replacement count changed: {count}")
    if aligned_version(updated) != new_version:
        raise ReleaseError(
            "updated release surfaces did not converge on the new version"
        )
    return updated


def write_contents(
    original: dict[Path, str],
    updated: dict[Path, str],
) -> list[Path]:
    changed = [path for path in original if original[path] != updated[path]]
    written: list[Path] = []
    try:
        for path in changed:
            (ROOT / path).write_text(updated[path], encoding="utf-8")
            written.append(path)
    except OSError as exc:
        for path in written:
            (ROOT / path).write_text(original[path], encoding="utf-8")
        raise ReleaseError(f"failed to update release surfaces: {exc}") from exc
    return changed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", nargs="?", help="New version, for example v4.3.0")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check that every release-version surface is aligned without editing.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show which files would change without editing them.",
    )
    args = parser.parse_args()
    if args.check and args.version:
        parser.error("--check does not accept a new version")
    if args.check and args.dry_run:
        parser.error("--check is already read-only; omit --dry-run")
    if not args.check and not args.version:
        parser.error("pass --check or a new version")
    if args.dry_run and not args.version:
        parser.error("--dry-run requires a new version")
    return args


def main() -> int:
    args = parse_args()
    try:
        original = load_contents()
        current = aligned_version(original)
        if args.check:
            print(f"OK: all release-version surfaces are aligned at {current}")
            return 0
        if not VERSION_PATTERN.fullmatch(args.version):
            raise ReleaseError(
                "version must use vMAJOR.MINOR.PATCH with an optional SemVer prerelease"
            )
        updated = replace_version(original, current, args.version)
        changed = [path for path in original if original[path] != updated[path]]
        if args.dry_run:
            print(
                f"Would update {current} -> {args.version} in {len(changed)} file(s):"
            )
            for path in changed:
                print(f"  {path}")
            return 0
        written = write_contents(original, updated)
        print(f"Updated {current} -> {args.version} in {len(written)} file(s):")
        for path in written:
            print(f"  {path}")
        return 0
    except ReleaseError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
