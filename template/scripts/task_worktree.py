#!/usr/bin/env python3
"""Create isolated task branches and worktrees with conservative defaults."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


SAFE_COMPONENT_RE = re.compile(r"[^a-z0-9-]+")


class WorktreeError(RuntimeError):
    """Raised when an isolated worktree cannot be created safely."""


def run_git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
    )
    if check and result.returncode != 0:
        raise WorktreeError(result.stderr.strip() or result.stdout.strip())
    return result


def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise WorktreeError("run this command inside a Git repository")
    return Path(result.stdout.strip()).resolve()


def slugify(value: str) -> str:
    normalized = SAFE_COMPONENT_RE.sub("-", value.lower()).strip("-")
    if not normalized:
        raise WorktreeError(f"value does not contain a safe branch component: {value!r}")
    return normalized


def default_base(root: Path) -> str:
    remote_head = run_git(
        root, "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD", check=False
    )
    if remote_head.returncode == 0 and remote_head.stdout.strip():
        remote_ref = remote_head.stdout.strip()
        local_name = remote_ref.removeprefix("origin/")
        if run_git(root, "show-ref", "--verify", f"refs/heads/{local_name}", check=False).returncode == 0:
            return local_name
        return remote_ref
    for candidate in ("main", "master"):
        if run_git(root, "show-ref", "--verify", f"refs/heads/{candidate}", check=False).returncode == 0:
            return candidate
    current = run_git(root, "branch", "--show-current").stdout.strip()
    if not current:
        raise WorktreeError("cannot determine a base branch")
    return current


def branch_exists(root: Path, branch: str) -> bool:
    return run_git(root, "show-ref", "--verify", f"refs/heads/{branch}", check=False).returncode == 0


def dirty_checkout(root: Path) -> bool:
    return bool(run_git(root, "status", "--porcelain").stdout.strip())


def create(args: argparse.Namespace) -> int:
    root = repo_root()
    work_component = slugify(args.work_id)
    suffix = work_component
    if args.slug:
        extra_slug = slugify(args.slug)
        if work_component != extra_slug and not work_component.endswith(f"-{extra_slug}"):
            suffix = f"{work_component}-{extra_slug}"
    branch = args.branch or f"task/{suffix}"
    destination = (
        args.path.expanduser().resolve()
        if args.path
        else (root.parent / f"{root.name}-worktrees" / suffix).resolve()
    )

    if destination.exists():
        raise WorktreeError(f"worktree destination already exists: {destination}")

    command = ["git", "-C", str(root), "worktree", "add"]
    existing_branch = branch_exists(root, branch)
    if existing_branch and not args.reuse_existing:
        raise WorktreeError(
            f"task branch already exists: {branch}; pass --reuse-existing only when resuming it intentionally"
        )
    if existing_branch and args.reuse_existing and args.base:
        raise WorktreeError("--base cannot be applied when --reuse-existing resumes an existing branch")
    if existing_branch:
        command.extend([str(destination), branch])
    else:
        base = args.base or default_base(root)
        if run_git(root, "rev-parse", "--verify", base, check=False).returncode != 0:
            raise WorktreeError(f"base branch or revision does not exist: {base}")
        command.extend(["-b", branch, str(destination), base])

    print(f"Branch: {branch}")
    if existing_branch:
        print("Resume: existing branch tip")
    else:
        print(f"Base: {base}")
    print(f"Worktree: {destination}")
    if dirty_checkout(root):
        print(
            "Warning: current checkout is dirty; the new worktree starts from committed Git state "
            "and does not include those uncommitted changes."
        )
    if args.dry_run:
        print("Dry run: " + " ".join(command))
        return 0

    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        raise WorktreeError(result.stderr.strip() or result.stdout.strip())
    print("Created isolated task worktree")
    return 0


def list_worktrees(_: argparse.Namespace) -> int:
    root = repo_root()
    result = run_git(root, "worktree", "list", "--porcelain")
    print(result.stdout.rstrip())
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="create one task branch and worktree")
    create_parser.add_argument("work_id", help="stable WORK identifier")
    create_parser.add_argument("--slug", help="short human-readable suffix")
    create_parser.add_argument("--base", help="base branch or revision")
    create_parser.add_argument("--branch", help="explicit task branch name")
    create_parser.add_argument(
        "--reuse-existing",
        action="store_true",
        help="resume an existing task branch instead of creating it from --base",
    )
    create_parser.add_argument("--path", type=Path, help="explicit worktree destination")
    create_parser.add_argument("--dry-run", action="store_true")
    create_parser.set_defaults(handler=create)

    list_parser = subparsers.add_parser("list", help="show registered worktrees")
    list_parser.set_defaults(handler=list_worktrees)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        return args.handler(args)
    except WorktreeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
