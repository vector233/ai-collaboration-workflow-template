#!/usr/bin/env python3
"""Create and update stable WORK artifacts without hand-editing workflow fields."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path


SAFE_SLUG_RE = re.compile(r"[^a-z0-9-]+")
WORK_ID_RE = re.compile(r"^WORK-[0-9]{14}-[a-z0-9][a-z0-9-]*$")
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)


class WorkflowTaskError(RuntimeError):
    """Raised when a WORK artifact cannot be changed safely."""


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
    )


def repository_root(root: Path) -> Path:
    resolved = root.expanduser().resolve()
    result = run_git(resolved, "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        raise WorkflowTaskError(f"not a Git repository: {resolved}")
    return Path(result.stdout.strip()).resolve()


def current_branch(root: Path) -> str:
    result = run_git(root, "branch", "--show-current")
    if result.returncode != 0 or not result.stdout.strip():
        raise WorkflowTaskError("a non-detached task branch is required")
    return result.stdout.strip()


def slugify(value: str) -> str:
    slug = SAFE_SLUG_RE.sub("-", value.lower()).strip("-")
    if not slug:
        raise WorkflowTaskError(f"cannot create a safe slug from {value!r}")
    return slug


def generate_work_id(slug: str) -> str:
    return f"WORK-{datetime.now().strftime('%Y%m%d%H%M%S')}-{slugify(slug)}"


def validate_work_id(work_id: str) -> str:
    if not WORK_ID_RE.fullmatch(work_id):
        raise WorkflowTaskError(
            "work ID must match WORK-YYYYMMDDHHMMSS-lowercase-slug"
        )
    return work_id


def work_path(root: Path, work_id: str) -> Path:
    path = root / "zettelkasten/06-work" / f"{validate_work_id(work_id)}.md"
    if not path.parent.is_dir():
        raise WorkflowTaskError("zettelkasten/06-work is missing; initialize the template first")
    return path


def set_frontmatter_field(text: str, field: str, value: str | list[str]) -> str:
    match = FRONTMATTER_RE.search(text)
    if not match:
        raise WorkflowTaskError("WORK file is missing YAML frontmatter")
    lines = match.group(1).splitlines()
    normalized: str | list[str]
    if isinstance(value, str):
        normalized = single_line(value)
    else:
        normalized = value
    replacement = f"{field}: {json.dumps(normalized, ensure_ascii=False)}"
    for index, line in enumerate(lines):
        if re.match(rf"^{re.escape(field)}:[ \t]*", line):
            continuation = index + 1
            while continuation < len(lines) and (
                not lines[continuation] or lines[continuation][0].isspace()
            ):
                continuation += 1
            lines[index:continuation] = [replacement]
            break
    else:
        lines.append(replacement)
    new_frontmatter = "---\n" + "\n".join(lines) + "\n---\n"
    return new_frontmatter + text[match.end() :]


def set_section_bullet(text: str, section: str, label: str, value: str) -> str:
    marker = f"## {section}"
    if marker not in text:
        raise WorkflowTaskError(f"WORK file is missing {marker}")
    before, remainder = text.split(marker, 1)
    body, separator, after = remainder.partition("\n## ")
    pattern = re.compile(rf"^- {re.escape(label)}:.*$", re.MULTILINE)
    replacement = f"- {label}: {single_line(value)}"
    if not pattern.search(body):
        raise WorkflowTaskError(f"{marker} is missing '- {label}:'")
    body = pattern.sub(replacement, body, count=1)
    suffix = separator + after if separator else ""
    return before + marker + body + suffix


def write_result(payload: dict[str, object], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")


def single_line(value: str) -> str:
    return " ".join(value.splitlines()).strip()


def validate_owned_paths(paths: list[str]) -> list[str]:
    validated: list[str] = []
    for raw_path in paths:
        value = raw_path.replace("\\", "/").strip().removeprefix("./").rstrip("/")
        parts = value.split("/")
        if (
            not value
            or value.startswith("/")
            or re.match(r"^[A-Za-z]:", value)
            or ".." in parts
        ):
            raise WorkflowTaskError(f"owned path must be repository-relative: {raw_path!r}")
        if value not in validated:
            validated.append(value)
    return validated


def split_markdown_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return []
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for character in stripped[1:]:
        if escaped and character == "|":
            current.append(character)
            escaped = False
        elif escaped:
            current.extend(("\\", character))
            escaped = False
        elif character == "\\":
            escaped = True
        elif character == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(character)
    if escaped:
        current.append("\\")
    if current or not stripped.endswith("|"):
        cells.append("".join(current).strip())
    return cells


def has_pending_experience_decision(text: str) -> bool:
    if "## Experience Candidates" not in text:
        return False
    section = text.split("## Experience Candidates", 1)[1].split("\n## ", 1)[0]
    for line in section.splitlines():
        cells = split_markdown_table_row(line)
        if len(cells) >= 5 and cells[0] not in {"Candidate", "---"}:
            if cells[2].strip().lower() == "pending":
                return True
    return False


def command_id(args: argparse.Namespace) -> int:
    print(generate_work_id(args.slug))
    return 0


def command_new(args: argparse.Namespace) -> int:
    root = repository_root(args.root)
    branch = current_branch(root)
    if branch in {"main", "master"}:
        raise WorkflowTaskError("create or switch to a task branch before creating tracked work")
    work_id = validate_work_id(args.work_id or generate_work_id(args.slug))
    destination = work_path(root, work_id)
    if destination.exists():
        raise WorkflowTaskError(f"WORK already exists: {destination}")
    template = root / "zettelkasten/00-governance/templates/work-item.md"
    if not template.is_file():
        raise WorkflowTaskError(f"WORK template is missing: {template}")
    title = single_line(args.title or args.slug.replace("-", " ").strip().title())
    owned_paths = validate_owned_paths(args.owned_path)
    text = template.read_text(encoding="utf-8")
    replacements = {
        "title: Work Item Title": f"title: {json.dumps(title, ensure_ascii=True)}",
        "# Work Item Title": f"# {title}",
        "WORK-YYYYMMDDHHMMSS-short-name": work_id,
        "status: backlog": "status: active",
        "risk: normal": f"risk: {json.dumps(single_line(args.risk), ensure_ascii=False)}",
        "branch: task/work-id-short-name": f"branch: {json.dumps(branch)}",
        "worktree: current": f"worktree: {json.dumps(args.worktree)}",
        "owned_paths: []": f"owned_paths: {json.dumps(owned_paths)}",
        "next_action: clarify acceptance criteria": (
            f"next_action: {json.dumps(single_line(args.next_action), ensure_ascii=False)}"
        ),
        "last_verified_at: YYYY-MM-DD": f"last_verified_at: {date.today().isoformat()}",
        "- Isolation: task branch / dedicated worktree": (
            f"- Isolation: {'dedicated worktree' if args.worktree == 'dedicated' else 'task branch'}"
        ),
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = set_frontmatter_field(text, "route", args.route)
    text = set_section_bullet(text, "Route Decision", "Selected route", args.route)
    destination.write_text(text, encoding="utf-8")
    write_result(
        {
            "work_id": work_id,
            "path": str(destination.relative_to(root)),
            "branch": branch,
            "route": args.route,
        },
        args.json,
    )
    return 0


def require_work(root: Path, work_id: str) -> Path:
    path = work_path(root, work_id)
    if not path.is_file():
        raise WorkflowTaskError(f"WORK does not exist: {path}")
    return path


def worktree_summary(root: Path) -> str:
    result = run_git(root, "status", "--short")
    if result.returncode != 0:
        return "unknown"
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return "clean before checkpoint update" if not lines else "; ".join(lines[:8])


def command_checkpoint(args: argparse.Namespace) -> int:
    root = repository_root(args.root)
    path = require_work(root, args.work_id)
    text = path.read_text(encoding="utf-8")
    text = set_frontmatter_field(text, "next_action", args.next_action)
    text = set_frontmatter_field(text, "last_verified_at", date.today().isoformat())
    if args.owned_path is not None:
        text = set_frontmatter_field(text, "owned_paths", validate_owned_paths(args.owned_path))
    checkpoint_values = {
        "Last completed step": args.completed_step,
        "Commit": args.commit,
        "Validation": args.validation,
        "Worktree status": args.worktree_status or worktree_summary(root),
        "Risks or unresolved decisions": args.risks,
        "Next allowed action": args.next_action,
    }
    for label, value in checkpoint_values.items():
        text = set_section_bullet(text, "Context Checkpoint", label, value)
    path.write_text(text, encoding="utf-8")
    write_result(
        {
            "work_id": args.work_id,
            "path": str(path.relative_to(root)),
            "next_action": args.next_action,
            "commit_reference": args.commit,
        },
        args.json,
    )
    return 0


def command_close(args: argparse.Namespace) -> int:
    required_flags = {
        "--acceptance-complete": args.acceptance_complete,
        "--gates-closed": args.gates_closed,
        "--promotion-complete": args.promotion_complete,
        "--writeback-complete": args.writeback_complete,
    }
    missing = [flag for flag, enabled in required_flags.items() if not enabled]
    if missing:
        raise WorkflowTaskError("close requires explicit confirmation: " + ", ".join(missing))
    root = repository_root(args.root)
    path = require_work(root, args.work_id)
    text = path.read_text(encoding="utf-8")
    if has_pending_experience_decision(text):
        raise WorkflowTaskError("experience candidates still contain a pending decision")
    text = set_frontmatter_field(text, "status", "done")
    text = set_frontmatter_field(text, "next_action", "none")
    text = set_frontmatter_field(text, "last_verified_at", date.today().isoformat())
    closure = {
        "Acceptance complete": "yes",
        "Required gates closed": "yes",
        "Experience Promotion complete": "yes",
        "Durable writeback complete": "yes",
        "Integration result": args.integration_result,
    }
    for label, value in closure.items():
        text = set_section_bullet(text, "Closure", label, value)
    path.write_text(text, encoding="utf-8")
    write_result(
        {"work_id": args.work_id, "path": str(path.relative_to(root)), "status": "done"},
        args.json,
    )
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    id_parser = subparsers.add_parser("id", help="generate a stable WORK identifier")
    id_parser.add_argument("slug")
    id_parser.set_defaults(handler=command_id)

    new_parser = subparsers.add_parser("new", help="create a WORK on the current task branch")
    new_parser.add_argument("slug")
    new_parser.add_argument("--id", dest="work_id")
    new_parser.add_argument("--title")
    new_parser.add_argument("--route", choices=("tracked", "governed"), default="tracked")
    new_parser.add_argument("--risk", default="normal")
    new_parser.add_argument("--worktree", choices=("current", "dedicated"), default="current")
    new_parser.add_argument("--next-action", default="clarify acceptance criteria")
    new_parser.add_argument("--owned-path", action="append", default=[])
    new_parser.add_argument("--root", type=Path, default=Path.cwd())
    new_parser.add_argument("--json", action="store_true")
    new_parser.set_defaults(handler=command_new)

    checkpoint_parser = subparsers.add_parser("checkpoint", help="update durable resume state")
    checkpoint_parser.add_argument("work_id")
    checkpoint_parser.add_argument("--completed-step", required=True)
    checkpoint_parser.add_argument("--validation", required=True)
    checkpoint_parser.add_argument("--next-action", required=True)
    checkpoint_parser.add_argument("--commit", default="this checkpoint commit")
    checkpoint_parser.add_argument("--worktree-status")
    checkpoint_parser.add_argument("--risks", default="none known")
    checkpoint_parser.add_argument(
        "--owned-path",
        action="append",
        help="replace owned paths; repeat for multiple repository-relative paths",
    )
    checkpoint_parser.add_argument("--root", type=Path, default=Path.cwd())
    checkpoint_parser.add_argument("--json", action="store_true")
    checkpoint_parser.set_defaults(handler=command_checkpoint)

    close_parser = subparsers.add_parser("close", help="close a WORK after explicit gates")
    close_parser.add_argument("work_id")
    close_parser.add_argument("--acceptance-complete", action="store_true")
    close_parser.add_argument("--gates-closed", action="store_true")
    close_parser.add_argument("--promotion-complete", action="store_true")
    close_parser.add_argument("--writeback-complete", action="store_true")
    close_parser.add_argument("--integration-result", required=True)
    close_parser.add_argument("--root", type=Path, default=Path.cwd())
    close_parser.add_argument("--json", action="store_true")
    close_parser.set_defaults(handler=command_close)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        return args.handler(args)
    except WorkflowTaskError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
