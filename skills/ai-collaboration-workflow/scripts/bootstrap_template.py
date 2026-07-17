#!/usr/bin/env python3
"""Safely bootstrap Repo Continuity into a repository."""

from __future__ import annotations

import argparse
import filecmp
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


DEFAULT_REPO_URL = "https://github.com/vector233/repo-continuity.git"
DEFAULT_REF = "main"
PAYLOAD_MARKER = Path(".ai-collaboration-workflow-template")

PAYLOAD_REQUIRED_FILES = (
    Path("AGENTS.md"),
    Path("CLAUDE.md"),
    Path("INIT.md"),
    Path("zettelkasten/AI.md"),
    Path("zettelkasten/workflow.md"),
    Path("zettelkasten/skill-lifecycle.md"),
    Path("zettelkasten/git-collaboration.md"),
    Path("zettelkasten/templates/work-item.md"),
    Path("zettelkasten/templates/workflow-observations.md"),
    Path("zettelkasten/work/README.md"),
    Path("project-skills/INDEX.md"),
)

OPTIONAL_ADAPTER_FILES = (
    Path(".codex/config.toml"),
    Path(".codex/agents/explorer.toml"),
    Path(".codex/agents/implementer.toml"),
    Path(".codex/agents/reviewer.toml"),
    Path(".codex/agents/architect.toml"),
)

INSTALLED_REQUIRED_FILES = tuple(
    path for path in PAYLOAD_REQUIRED_FILES if path != Path("INIT.md")
)

REQUIRED_DIRECTORIES = (
    Path("zettelkasten/work"),
    Path("project-skills"),
)


@dataclass(frozen=True)
class InstallPlan:
    missing: tuple[Path, ...]
    identical: tuple[Path, ...]
    conflicts: tuple[Path, ...]


class BootstrapError(RuntimeError):
    """Raised when the template source or target cannot be used safely."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Copy Repo Continuity into a repository without "
            "overwriting differing existing files."
        )
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.cwd(),
        help="Target repository root (default: current directory).",
    )
    parser.add_argument(
        "--source",
        type=Path,
        help=(
            "Local repository checkout or direct template payload directory. "
            "When omitted, clone the canonical repository."
        ),
    )
    parser.add_argument(
        "--repo-url",
        default=DEFAULT_REPO_URL,
        help=f"Template Git repository (default: {DEFAULT_REPO_URL}).",
    )
    parser.add_argument(
        "--ref",
        default=DEFAULT_REF,
        help=f"Git branch or tag to clone (default: {DEFAULT_REF}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be copied without changing the target.",
    )
    parser.add_argument(
        "--inspect",
        action="store_true",
        help="Only check whether the target has the required initialized core files.",
    )
    return parser.parse_args()


def normalize_directory(path: Path, label: str, *, must_exist: bool) -> Path:
    resolved = path.expanduser().resolve()
    if must_exist and not resolved.is_dir():
        raise BootstrapError(f"{label} is not a directory: {resolved}")
    if not must_exist and resolved.exists() and not resolved.is_dir():
        raise BootstrapError(f"{label} is not a directory: {resolved}")
    return resolved


def missing_required_paths(root: Path, required: tuple[Path, ...]) -> list[Path]:
    return [relative for relative in required if not (root / relative).is_file()]


def missing_required_directories(root: Path) -> list[Path]:
    return [
        relative
        for relative in REQUIRED_DIRECTORIES
        if not (root / relative).is_dir()
    ]


def inspect_target(target: Path) -> int:
    missing_files = missing_required_paths(target, INSTALLED_REQUIRED_FILES)
    missing_directories = missing_required_directories(target)
    if missing_files or missing_directories:
        print(f"Template status: incomplete ({target})")
        for relative in missing_files:
            print(f"  missing file: {relative}")
        for relative in missing_directories:
            print(f"  missing directory: {relative}")
        if (target / "INIT.md").is_file():
            print("Initialization status: INIT.md is present; continue initialization.")
        return 2

    print(f"Template status: core files present ({target})")
    if (target / "INIT.md").is_file():
        print("Initialization status: INIT.md is present; initialization is not finished.")
    else:
        print("Initialization status: INIT.md is absent; verify placeholder checks are clean.")
    return 0


def clone_source(repo_url: str, ref: str, destination: Path) -> Path:
    command = [
        "git",
        "clone",
        "--depth",
        "1",
        "--branch",
        ref,
        "--single-branch",
        repo_url,
        str(destination),
    ]
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError as exc:
        raise BootstrapError(
            "git is required for remote bootstrap; use --source with a local checkout"
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise BootstrapError(
            f"failed to clone {repo_url!r} at branch or tag {ref!r}"
        ) from exc
    return destination


def validate_payload(payload: Path) -> None:
    if not (payload / PAYLOAD_MARKER).is_file():
        raise BootstrapError(f"template payload marker is missing: {payload / PAYLOAD_MARKER}")
    missing_files = missing_required_paths(
        payload, PAYLOAD_REQUIRED_FILES + OPTIONAL_ADAPTER_FILES
    )
    missing_directories = missing_required_directories(payload)
    problems = [
        *(f"file {path}" for path in missing_files),
        *(f"directory {path}" for path in missing_directories),
    ]
    if problems:
        raise BootstrapError(
            "template payload is missing required paths: " + ", ".join(problems)
        )


def resolve_payload_root(source: Path) -> Path:
    candidates = (source / "template", source)
    for candidate in candidates:
        if (candidate / PAYLOAD_MARKER).is_file():
            validate_payload(candidate)
            return candidate
    raise BootstrapError(
        f"no marked template payload found under {source}; expected "
        f"{source / 'template' / PAYLOAD_MARKER} or {source / PAYLOAD_MARKER}"
    )


def template_files(source: Path) -> tuple[Path, ...]:
    files = [
        PAYLOAD_MARKER,
        Path("AGENTS.md"),
        Path("CLAUDE.md"),
        Path("INIT.md"),
    ]
    for directory in ("zettelkasten", "project-skills", ".codex"):
        source_directory = source / directory
        if not source_directory.is_dir():
            continue
        for candidate in sorted(source_directory.rglob("*")):
            if candidate.is_symlink():
                raise BootstrapError(f"template source contains a symlink: {candidate}")
            if candidate.is_file():
                files.append(candidate.relative_to(source))
    return tuple(files)


def has_symlink_component(target: Path, relative: Path) -> bool:
    candidate = target
    for part in relative.parts:
        candidate = candidate / part
        if candidate.is_symlink():
            return True
    return False


def build_plan(source: Path, target: Path) -> InstallPlan:
    missing: list[Path] = []
    identical: list[Path] = []
    conflicts: list[Path] = []

    for relative in template_files(source):
        source_file = source / relative
        target_file = target / relative
        if has_symlink_component(target, relative):
            conflicts.append(relative)
        elif not target_file.exists():
            missing.append(relative)
        elif target_file.is_file() and filecmp.cmp(
            source_file, target_file, shallow=False
        ):
            identical.append(relative)
        else:
            conflicts.append(relative)

    return InstallPlan(
        missing=tuple(missing),
        identical=tuple(identical),
        conflicts=tuple(conflicts),
    )


def apply_plan(
    source: Path, target: Path, plan: InstallPlan, *, dry_run: bool
) -> None:
    if dry_run:
        return
    target.mkdir(parents=True, exist_ok=True)
    for relative in plan.missing:
        source_file = source / relative
        target_file = target / relative
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target_file)


def print_plan(target: Path, plan: InstallPlan, *, dry_run: bool) -> None:
    verb = "Would copy" if dry_run else "Copied"
    print(f"Target: {target}")
    print(f"{verb}: {len(plan.missing)}")
    print(f"Identical: {len(plan.identical)}")
    print(f"Conflicts left untouched: {len(plan.conflicts)}")
    for relative in plan.conflicts:
        print(f"  conflict: {relative}")

    if plan.conflicts:
        print(
            "Next: inspect each conflict, preserve repository-specific content, "
            "and merge the template guidance manually."
        )
    elif dry_run:
        print("Next: rerun without --dry-run to copy the missing template files.")
    else:
        print("Next: follow INIT.md in the target repository.")


def install(args: argparse.Namespace, target: Path) -> int:
    if args.source:
        source = normalize_directory(args.source, "source", must_exist=True)
        payload = resolve_payload_root(source)
        plan = build_plan(payload, target)
        apply_plan(payload, target, plan, dry_run=args.dry_run)
        print_plan(target, plan, dry_run=args.dry_run)
        return 2 if plan.conflicts else 0

    with tempfile.TemporaryDirectory(prefix="ai-workflow-template-") as temp_dir:
        source = clone_source(
            args.repo_url, args.ref, Path(temp_dir) / "template"
        )
        payload = resolve_payload_root(source)
        plan = build_plan(payload, target)
        apply_plan(payload, target, plan, dry_run=args.dry_run)
        print_plan(target, plan, dry_run=args.dry_run)
        return 2 if plan.conflicts else 0


def main() -> int:
    args = parse_args()
    try:
        target = normalize_directory(args.target, "target", must_exist=False)
        if args.inspect:
            return inspect_target(target)
        return install(args, target)
    except BootstrapError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
