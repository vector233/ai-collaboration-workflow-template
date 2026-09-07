#!/usr/bin/env python3
"""Create and update bounded Initiative and stable WORK artifacts."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

from workflow_archive import ArchiveError, safe_path, write_artifact


SAFE_SLUG_RE = re.compile(r"[^a-z0-9-]+")
WORK_ID_RE = re.compile(r"^WORK-[0-9]{14}-[a-z0-9][a-z0-9-]*$")
INITIATIVE_ID_RE = re.compile(
    r"^INITIATIVE-[0-9]{14}-[a-z0-9][a-z0-9-]*$"
)
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
EXPERIENCE_SHAPES = (
    "rule",
    "gotcha",
    "fact",
    "runbook",
    "project-skill",
    "workflow-feedback",
)
EXPERIENCE_DECISIONS = ("promoted", "updated", "no-op", "not-promoted")


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


def generate_initiative_id(slug: str) -> str:
    return f"INITIATIVE-{datetime.now().strftime('%Y%m%d%H%M%S')}-{slugify(slug)}"


def validate_work_id(work_id: str) -> str:
    if not WORK_ID_RE.fullmatch(work_id):
        raise WorkflowTaskError(
            "work ID must match WORK-YYYYMMDDHHMMSS-lowercase-slug"
        )
    return work_id


def validate_initiative_id(initiative_id: str) -> str:
    if not INITIATIVE_ID_RE.fullmatch(initiative_id):
        raise WorkflowTaskError(
            "initiative ID must match INITIATIVE-YYYYMMDDHHMMSS-lowercase-slug"
        )
    return initiative_id


def work_path(root: Path, work_id: str) -> Path:
    path = safe_path(root, Path("zettelkasten/work") / f"{validate_work_id(work_id)}.md")
    if not path.parent.is_dir():
        raise WorkflowTaskError("zettelkasten/work is missing; initialize the template first")
    return path


def initiative_path(root: Path, initiative_id: str) -> Path:
    path = safe_path(root, Path("zettelkasten/work") / f"{validate_initiative_id(initiative_id)}.md")
    if not path.parent.is_dir():
        raise WorkflowTaskError("zettelkasten/work is missing; initialize the template first")
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


def frontmatter_field(text: str, field: str) -> str | None:
    match = FRONTMATTER_RE.search(text)
    if not match:
        return None
    pattern = re.compile(rf"^{re.escape(field)}:[ \t]*(.*)$", re.MULTILINE)
    field_match = pattern.search(match.group(1))
    if not field_match:
        return None
    value = field_match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
        return decoded if isinstance(decoded, str) else str(decoded)
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value or None


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


def section_body(text: str, heading: str) -> str:
    marker = f"## {heading}"
    if marker not in text:
        return ""
    return text.split(marker, 1)[1].split("\n## ", 1)[0]


def markdown_cell(value: str) -> str:
    return single_line(value).replace("|", r"\|")


def experience_rows(text: str) -> list[tuple[int, list[str]]]:
    lines = text.splitlines()
    try:
        section_start = lines.index("## Experience Candidates")
    except ValueError as exc:
        raise WorkflowTaskError("WORK file is missing ## Experience Candidates") from exc
    section_end = next(
        (index for index in range(section_start + 1, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )
    rows: list[tuple[int, list[str]]] = []
    for index in range(section_start + 1, section_end):
        cells = split_markdown_table_row(lines[index])
        if len(cells) < 5 or cells[0] == "Candidate":
            continue
        if all(not cell or set(cell) <= {"-", ":"} for cell in cells):
            continue
        rows.append((index, cells))
    return rows


def experience_row(
    candidate: str,
    shape: str,
    decision: str,
    destination: str,
    result: str,
) -> str:
    return "| " + " | ".join(
        markdown_cell(value)
        for value in (candidate, shape, decision, destination, result)
    ) + " |"


def replace_or_append_experience_row(text: str, row: str) -> str:
    lines = text.splitlines()
    rows = experience_rows(text)
    placeholder = next(
        (index for index, cells in rows if not cells[0] and cells[2].lower() == "pending"),
        None,
    )
    if placeholder is not None:
        lines[placeholder] = row
    elif rows:
        lines.insert(rows[-1][0] + 1, row)
    else:
        raise WorkflowTaskError("Experience Candidates table is missing its writable row")
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def destination_paths(value: str) -> list[str]:
    raw_paths = [item.strip() for item in value.split(";") if item.strip()]
    if not raw_paths:
        raise WorkflowTaskError("a promoted, updated, or no-op candidate needs a destination")
    return validate_owned_paths(raw_paths)


def has_pending_experience_decision(text: str) -> bool:
    for line in section_body(text, "Experience Candidates").splitlines():
        cells = split_markdown_table_row(line)
        if len(cells) >= 5 and cells[0] not in {"Candidate", "---"}:
            if cells[2].strip().lower() == "pending":
                return True
    return False


def has_pending_governed_gate(text: str) -> bool:
    for line in section_body(text, "Governed Gates").splitlines():
        cells = split_markdown_table_row(line)
        if len(cells) >= 4 and cells[0] not in {"Gate or decision", "---"}:
            if cells[3].strip().lower() == "pending":
                return True
    return False


def command_id(args: argparse.Namespace) -> int:
    print(generate_work_id(args.slug))
    return 0


def command_initiative_id(args: argparse.Namespace) -> int:
    print(generate_initiative_id(args.slug))
    return 0


def command_initiative_new(args: argparse.Namespace) -> int:
    root = repository_root(args.root)
    branch = current_branch(root)
    if branch in {"main", "master"}:
        raise WorkflowTaskError(
            "create or switch to a coordination task branch before creating an Initiative"
        )
    initiative_id = validate_initiative_id(
        args.initiative_id or generate_initiative_id(args.slug)
    )
    destination = initiative_path(root, initiative_id)
    if destination.exists():
        raise WorkflowTaskError(f"Initiative already exists: {destination}")
    template = root / "zettelkasten/templates/initiative.md"
    if not template.is_file():
        raise WorkflowTaskError(f"Initiative template is missing: {template}")
    title = single_line(args.title or args.slug.replace("-", " ").strip().title())
    text = template.read_text(encoding="utf-8")
    replacements = {
        "title: Initiative Title": f"title: {json.dumps(title, ensure_ascii=True)}",
        "# Initiative Title": f"# {title}",
        "INITIATIVE-YYYYMMDDHHMMSS-short-name": initiative_id,
        "status: backlog": "status: active",
        "next_action: define independently deliverable child work": (
            f"next_action: {json.dumps(single_line(args.next_action), ensure_ascii=False)}"
        ),
        "last_verified_at: YYYY-MM-DD": f"last_verified_at: {date.today().isoformat()}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    write_artifact(root, destination, text)
    write_result(
        {
            "initiative_id": initiative_id,
            "path": str(destination.relative_to(root)),
            "status": "active",
        },
        args.json,
    )
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
    template = root / "zettelkasten/templates/work-item.md"
    if not template.is_file():
        raise WorkflowTaskError(f"WORK template is missing: {template}")
    title = single_line(args.title or args.slug.replace("-", " ").strip().title())
    owned_paths = validate_owned_paths(args.owned_path)
    initiative_id = ""
    if args.initiative_id:
        initiative_id = validate_initiative_id(args.initiative_id)
        if not initiative_path(root, initiative_id).is_file():
            raise WorkflowTaskError(f"local Initiative does not exist: {initiative_id}")
    external_parent = single_line(args.external_parent or "")
    dependencies: list[str] = []
    for dependency in args.depends_on:
        dependency_id = validate_work_id(dependency)
        if dependency_id == work_id:
            raise WorkflowTaskError("WORK cannot depend on itself")
        if not work_path(root, dependency_id).is_file():
            raise WorkflowTaskError(f"WORK dependency does not exist: {dependency_id}")
        if dependency_id not in dependencies:
            dependencies.append(dependency_id)
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
    text = set_frontmatter_field(text, "initiative_id", initiative_id)
    text = set_frontmatter_field(text, "external_parent", external_parent)
    text = set_frontmatter_field(text, "depends_on", dependencies)
    text = set_section_bullet(text, "Route Decision", "Selected route", args.route)
    write_artifact(root, destination, text)
    write_result(
        {
            "work_id": work_id,
            "path": str(destination.relative_to(root)),
            "branch": branch,
            "route": args.route,
            "initiative_id": initiative_id,
            "external_parent": external_parent,
            "depends_on": dependencies,
        },
        args.json,
    )
    return 0


def require_work(root: Path, work_id: str) -> Path:
    path = work_path(root, work_id)
    if not path.is_file():
        raise WorkflowTaskError(f"WORK does not exist: {path}")
    if frontmatter_field(path.read_text(), "archive_ref"):
        raise WorkflowTaskError("restore the archived WORK before updating it")
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
    write_artifact(root, path, text)
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


def command_learn_add(args: argparse.Namespace) -> int:
    root = repository_root(args.root)
    path = require_work(root, args.work_id)
    text = path.read_text(encoding="utf-8")
    candidate = single_line(args.candidate)
    if not candidate:
        raise WorkflowTaskError("candidate must not be empty")
    evidence = single_line(args.evidence)
    if not evidence:
        raise WorkflowTaskError("evidence must not be empty")
    for _, cells in experience_rows(text):
        if cells[0] == candidate:
            raise WorkflowTaskError(f"experience candidate already exists: {candidate}")
    destination = ""
    if args.destination:
        destination = "; ".join(destination_paths(args.destination))
    row = experience_row(
        candidate,
        args.shape,
        "pending",
        destination,
        f"Evidence: {evidence}",
    )
    write_artifact(root, path, replace_or_append_experience_row(text, row))
    write_result(
        {
            "work_id": args.work_id,
            "candidate": candidate,
            "decision": "pending",
            "path": str(path.relative_to(root)),
        },
        args.json,
    )
    return 0


def command_learn_none(args: argparse.Namespace) -> int:
    root = repository_root(args.root)
    path = require_work(root, args.work_id)
    text = path.read_text(encoding="utf-8")
    substantive = [cells for _, cells in experience_rows(text) if cells[0]]
    if substantive:
        raise WorkflowTaskError("cannot record no reusable lesson after candidates exist")
    reason = single_line(args.reason)
    if not reason:
        raise WorkflowTaskError("reason must not be empty")
    row = experience_row(
        "No reusable lesson",
        "fact",
        "not-promoted",
        "work item",
        f"Learning Check: {reason}",
    )
    write_artifact(root, path, replace_or_append_experience_row(text, row))
    write_result(
        {
            "work_id": args.work_id,
            "candidate": "No reusable lesson",
            "decision": "not-promoted",
            "path": str(path.relative_to(root)),
        },
        args.json,
    )
    return 0


def command_learn_decide(args: argparse.Namespace) -> int:
    root = repository_root(args.root)
    path = require_work(root, args.work_id)
    text = path.read_text(encoding="utf-8")
    candidate = single_line(args.candidate)
    if not candidate:
        raise WorkflowTaskError("candidate must not be empty")
    reason = single_line(args.reason)
    if not reason:
        raise WorkflowTaskError("reason must not be empty")
    matches = [
        (index, cells)
        for index, cells in experience_rows(text)
        if cells[0] == candidate
    ]
    if not matches:
        raise WorkflowTaskError(f"experience candidate does not exist: {candidate}")
    if len(matches) > 1:
        raise WorkflowTaskError(f"experience candidate is duplicated: {candidate}")
    index, cells = matches[0]
    if cells[2].lower() != "pending":
        raise WorkflowTaskError(
            f"experience candidate already has decision {cells[2]!r}: {candidate}"
        )
    if args.decision == "not-promoted":
        destination = single_line(args.destination or "work item")
        if destination != "work item":
            raise WorkflowTaskError("a not-promoted candidate must remain in the work item")
    else:
        destination = "; ".join(destination_paths(args.destination or ""))
        missing = [
            value
            for value in destination_paths(destination)
            if not (root / value).exists()
        ]
        if missing:
            raise WorkflowTaskError(
                "durable destination does not exist after writeback: " + ", ".join(missing)
            )
    previous = cells[4]
    outcome = f"{previous}; Outcome: {reason}" if previous else reason
    lines = text.splitlines()
    lines[index] = experience_row(candidate, cells[1], args.decision, destination, outcome)
    updated = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    write_artifact(root, path, updated)
    write_result(
        {
            "work_id": args.work_id,
            "candidate": candidate,
            "decision": args.decision,
            "destination": destination,
            "path": str(path.relative_to(root)),
        },
        args.json,
    )
    return 0


def command_learn_status(args: argparse.Namespace) -> int:
    root = repository_root(args.root)
    path = require_work(root, args.work_id)
    rows = experience_rows(path.read_text(encoding="utf-8"))
    candidates = [
        {
            "candidate": cells[0] or "<learning-check-required>",
            "shape": cells[1],
            "decision": cells[2],
            "destination": cells[3],
            "evidence_and_outcome": cells[4],
        }
        for _, cells in rows
    ]
    pending = [item for item in candidates if item["decision"].lower() == "pending"]
    payload = {
        "work_id": args.work_id,
        "path": str(path.relative_to(root)),
        "complete": not pending,
        "pending": len(pending),
        "candidates": candidates,
    }
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"work_id: {args.work_id}")
        print(f"complete: {'yes' if not pending else 'no'}")
        print(f"pending: {len(pending)}")
        for item in candidates:
            print(
                f"candidate: {item['candidate']} | shape={item['shape']} | "
                f"decision={item['decision']} | destination={item['destination'] or '-'}"
            )
    return 1 if args.require_complete and pending else 0


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
    if frontmatter_field(text, "route") == "governed" and has_pending_governed_gate(text):
        raise WorkflowTaskError("governed gates still contain a pending gate")
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
    write_artifact(root, path, text)
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

    initiative_id_parser = subparsers.add_parser(
        "initiative-id", help="generate a stable Initiative identifier"
    )
    initiative_id_parser.add_argument("slug")
    initiative_id_parser.set_defaults(handler=command_initiative_id)

    initiative_new_parser = subparsers.add_parser(
        "initiative-new", help="create a thin local coordination Initiative"
    )
    initiative_new_parser.add_argument("slug")
    initiative_new_parser.add_argument("--id", dest="initiative_id")
    initiative_new_parser.add_argument("--title")
    initiative_new_parser.add_argument(
        "--next-action", default="define independently deliverable child work"
    )
    initiative_new_parser.add_argument("--root", type=Path, default=Path.cwd())
    initiative_new_parser.add_argument("--json", action="store_true")
    initiative_new_parser.set_defaults(handler=command_initiative_new)

    new_parser = subparsers.add_parser("new", help="create a WORK on the current task branch")
    new_parser.add_argument("slug")
    new_parser.add_argument("--id", dest="work_id")
    new_parser.add_argument("--title")
    new_parser.add_argument("--route", choices=("tracked", "governed"), default="tracked")
    new_parser.add_argument("--risk", default="normal")
    new_parser.add_argument("--worktree", choices=("current", "dedicated"), default="current")
    new_parser.add_argument("--next-action", default="clarify acceptance criteria")
    new_parser.add_argument("--owned-path", action="append", default=[])
    parent_group = new_parser.add_mutually_exclusive_group()
    parent_group.add_argument("--initiative", dest="initiative_id")
    parent_group.add_argument("--external-parent")
    new_parser.add_argument(
        "--depends-on",
        action="append",
        default=[],
        help="existing WORK ID that must complete first; repeat for multiple dependencies",
    )
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

    learn_add_parser = subparsers.add_parser(
        "learn-add", help="record an evidence-backed experience candidate"
    )
    learn_add_parser.add_argument("work_id")
    learn_add_parser.add_argument("--candidate", required=True)
    learn_add_parser.add_argument("--shape", choices=EXPERIENCE_SHAPES, required=True)
    learn_add_parser.add_argument("--evidence", required=True)
    learn_add_parser.add_argument(
        "--destination",
        help="optional repository-relative destination hint; separate multiple paths with ';'",
    )
    learn_add_parser.add_argument("--root", type=Path, default=Path.cwd())
    learn_add_parser.add_argument("--json", action="store_true")
    learn_add_parser.set_defaults(handler=command_learn_add)

    learn_none_parser = subparsers.add_parser(
        "learn-none", help="record that the Learning Check found no reusable lesson"
    )
    learn_none_parser.add_argument("work_id")
    learn_none_parser.add_argument("--reason", required=True)
    learn_none_parser.add_argument("--root", type=Path, default=Path.cwd())
    learn_none_parser.add_argument("--json", action="store_true")
    learn_none_parser.set_defaults(handler=command_learn_none)

    learn_decide_parser = subparsers.add_parser(
        "learn-decide", help="record the final promotion decision for a candidate"
    )
    learn_decide_parser.add_argument("work_id")
    learn_decide_parser.add_argument("--candidate", required=True)
    learn_decide_parser.add_argument("--decision", choices=EXPERIENCE_DECISIONS, required=True)
    learn_decide_parser.add_argument(
        "--destination",
        help="repository-relative destination; separate multiple paths with ';'",
    )
    learn_decide_parser.add_argument("--reason", required=True)
    learn_decide_parser.add_argument("--root", type=Path, default=Path.cwd())
    learn_decide_parser.add_argument("--json", action="store_true")
    learn_decide_parser.set_defaults(handler=command_learn_decide)

    learn_status_parser = subparsers.add_parser(
        "learn-status", help="show whether every Learning Check candidate has a final decision"
    )
    learn_status_parser.add_argument("work_id")
    learn_status_parser.add_argument("--require-complete", action="store_true")
    learn_status_parser.add_argument("--root", type=Path, default=Path.cwd())
    learn_status_parser.add_argument("--json", action="store_true")
    learn_status_parser.set_defaults(handler=command_learn_status)

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
    except (WorkflowTaskError, ArchiveError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
