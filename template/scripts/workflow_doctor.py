#!/usr/bin/env python3
"""Validate workflow artifacts, project Skills, and cross-worktree task state."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path


CORE_FILES = (
    Path("AGENTS.md"),
    Path("CLAUDE.md"),
    Path("scripts/workflow_doctor.py"),
    Path("scripts/workflow_task.py"),
    Path("scripts/task_worktree.py"),
    Path("zettelkasten/AI.md"),
    Path("zettelkasten/00-governance/ai-workflow.md"),
    Path("zettelkasten/00-governance/skill-lifecycle.md"),
    Path("zettelkasten/00-governance/git-collaboration.md"),
    Path("zettelkasten/00-governance/templates/work-item.md"),
    Path("zettelkasten/06-work/README.md"),
    Path("project-skills/INDEX.md"),
)

CORE_DIRECTORIES = (Path("zettelkasten/06-work"), Path("project-skills"))

ARTIFACT_STATES = {
    "WORK-": {"backlog", "active", "blocked", "review", "done", "cancelled"},
    "TECH-": {"pending", "approved", "implemented", "superseded"},
    "PLAN-": {"draft", "ready", "executing", "completed", "superseded"},
    "REVIEW-": {"pending", "in-review", "done", "waived"},
}

ACTIVE_WORK_STATES = {"active", "blocked", "review"}
WORK_REQUIRED_SECTIONS = (
    "## Goal And Acceptance",
    "## Route Decision",
    "## Context Pack",
    "## Scope And Ownership",
    "## Validation",
    "## Experience Candidates",
    "## Context Checkpoint",
)
SKILL_REQUIRED_SECTIONS = (
    "## Use",
    "## Do Not Use",
    "## Procedure",
    "## Validation",
    "## Recovery",
    "## Provenance",
)
SKILL_STATES = {"active", "needs-verification", "deprecated"}

PLACEHOLDER_RE = re.compile(r"\{\{[A-Z_]+\}\}")
WIKI_LINK_RE = re.compile(r"(?<!!)\[\[([^\]|#]+)")
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
TOP_LEVEL_FIELD_RE = re.compile(r"^([A-Za-z0-9_-]+):[ \t]*(.*)$")
PROMOTION_COMPLETE_RE = re.compile(
    r"^-\s*Experience Promotion complete:\s*yes\s*$",
    re.IGNORECASE | re.MULTILINE,
)


@dataclass(frozen=True)
class Finding:
    severity: str
    message: str
    path: Path | None = None


@dataclass(frozen=True)
class WorkRecord:
    work_id: str
    status: str
    route: str
    declared_branch: str
    actual_branch: str
    worktree: str
    file: str
    next_action: str
    owned_paths: tuple[str, ...]
    dirty: bool
    last_commit: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--strict", action="store_true", help="fail on warnings")
    parser.add_argument("--status", action="store_true", help="show active work without validation")
    parser.add_argument(
        "--all-worktrees",
        action="store_true",
        help="with --status, aggregate every registered Git worktree",
    )
    parser.add_argument("--json", action="store_true", help="with --status, emit machine-readable JSON")
    args = parser.parse_args()
    if (args.all_worktrees or args.json) and not args.status:
        parser.error("--all-worktrees and --json require --status")
    return args


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def relative(root: Path, path: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def add(findings: list[Finding], severity: str, message: str, path: Path | None = None) -> None:
    findings.append(Finding(severity, message, path))


def strip_scalar_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Parse top-level scalar fields needed by the workflow without a YAML dependency."""
    match = FRONTMATTER_RE.search(text)
    if not match:
        return None
    lines = match.group(1).splitlines()
    values: dict[str, str] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        field = TOP_LEVEL_FIELD_RE.match(line)
        if not field:
            index += 1
            continue
        key, raw_value = field.groups()
        block_style = raw_value.strip()
        if block_style in {"|", "|-", "|+", ">", ">-", ">+"}:
            index += 1
            block_lines: list[str] = []
            while index < len(lines):
                candidate = lines[index]
                if candidate and not candidate[0].isspace():
                    break
                block_lines.append(candidate.strip())
                index += 1
            if block_style.startswith(">"):
                values[key] = " ".join(part for part in block_lines if part).strip()
            else:
                values[key] = "\n".join(block_lines).strip()
            continue
        values[key] = strip_scalar_quotes(raw_value)
        index += 1
    return values


def field_value(text: str, field: str) -> str | None:
    values = parse_frontmatter(text)
    if values is None:
        return None
    value = values.get(field, "").strip()
    return value or None


def parse_inline_list(value: str | None) -> tuple[str, ...]:
    if not value or value.strip() in {"", "[]"}:
        return ()
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            parsed = [part.strip() for part in value[1:-1].split(",")]
    else:
        parsed = [part.strip() for part in value.split(",")]
    if not isinstance(parsed, list):
        return ()
    return tuple(str(part).strip().strip('"').strip("'") for part in parsed if str(part).strip())


def workflow_artifacts(root: Path) -> list[Path]:
    directory = root / "zettelkasten/06-work"
    if not directory.is_dir():
        return []
    return [
        path
        for path in sorted(directory.iterdir())
        if path.is_file() and path.name not in {"README.md", ".gitkeep"}
    ]


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
    )


def current_branch(root: Path) -> str:
    result = run_git(root, "branch", "--show-current")
    return result.stdout.strip() if result.returncode == 0 else ""


def worktree_is_dirty(root: Path) -> bool:
    result = run_git(root, "status", "--porcelain")
    return result.returncode == 0 and bool(result.stdout.strip())


def last_commit(root: Path) -> str:
    result = run_git(root, "log", "-1", "--format=%H")
    return result.stdout.strip() if result.returncode == 0 else ""


def registered_worktrees(root: Path) -> list[Path]:
    result = run_git(root, "worktree", "list", "--porcelain")
    if result.returncode != 0:
        return [root]
    paths = [Path(line.removeprefix("worktree ")).resolve() for line in result.stdout.splitlines() if line.startswith("worktree ")]
    return paths or [root]


def markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for relative_path in (Path("AGENTS.md"), Path("CLAUDE.md")):
        path = root / relative_path
        if path.is_file():
            files.append(path)
    for directory in (root / "zettelkasten", root / "project-skills"):
        if directory.is_dir():
            files.extend(sorted(directory.rglob("*.md")))
    return files


def check_core(root: Path, findings: list[Finding]) -> None:
    for path in CORE_FILES:
        if not (root / path).is_file():
            add(findings, "ERROR", "missing required file", path)
    for path in CORE_DIRECTORIES:
        if not (root / path).is_dir():
            add(findings, "ERROR", "missing required directory", path)
    if (root / "INIT.md").is_file():
        add(findings, "WARN", "INIT.md is present; initialization is not finished", Path("INIT.md"))
    if (root / ".ai-collaboration-workflow-template").is_file():
        add(findings, "WARN", "payload marker is present; initialization is not finished", Path(".ai-collaboration-workflow-template"))


def check_placeholders(root: Path, findings: list[Finding]) -> None:
    for path in markdown_files(root):
        text = read_text(path)
        matches = sorted(set(PLACEHOLDER_RE.findall(text)))
        if matches:
            add(findings, "ERROR", "unresolved placeholders: " + ", ".join(matches), relative(root, path))
        if "UMBRELLA-ONLY" in text:
            add(findings, "ERROR", "umbrella-mode marker remains", relative(root, path))


def check_wiki_links(root: Path, findings: list[Finding]) -> None:
    vault = root / "zettelkasten"
    if not vault.is_dir():
        return
    exact: dict[str, Path] = {}
    by_stem: dict[str, list[Path]] = {}
    for path in sorted(vault.rglob("*.md")):
        exact[path.relative_to(vault).with_suffix("").as_posix()] = path
        by_stem.setdefault(path.stem, []).append(path)
    for path in sorted(vault.rglob("*.md")):
        for raw_target in WIKI_LINK_RE.findall(read_text(path)):
            target = raw_target.strip().removesuffix(".md")
            if any(marker in target for marker in ("YYYY", "<", "{{")):
                continue
            if "/" in target:
                if target not in exact:
                    add(findings, "ERROR", f"broken wiki link: [[{target}]]", relative(root, path))
                continue
            candidates = by_stem.get(target, [])
            if not candidates:
                add(findings, "ERROR", f"broken wiki link: [[{target}]]", relative(root, path))
            elif len(candidates) > 1:
                choices = ", ".join(item.relative_to(vault).as_posix() for item in candidates)
                add(findings, "ERROR", f"ambiguous wiki link [[{target}]]; use an explicit path: {choices}", relative(root, path))


def artifact_prefix(path: Path) -> str | None:
    return next((prefix for prefix in ARTIFACT_STATES if path.name.startswith(prefix)), None)


def experience_section(text: str) -> str:
    if "## Experience Candidates" not in text:
        return ""
    return text.split("## Experience Candidates", 1)[1].split("\n## ", 1)[0]


def check_artifacts(root: Path, findings: list[Finding]) -> None:
    active_branches: dict[str, Path] = {}
    for path in workflow_artifacts(root):
        rel_path = relative(root, path)
        prefix = artifact_prefix(path)
        if prefix is None or path.suffix != ".md":
            add(findings, "ERROR", "unexpected work artifact name", rel_path)
            continue
        text = read_text(path)
        status = field_value(text, "status")
        if status not in ARTIFACT_STATES[prefix]:
            add(findings, "ERROR", f"invalid {prefix[:-1]} status {status!r}", rel_path)
        if prefix != "WORK-":
            if not field_value(text, "related_work"):
                add(findings, "ERROR", "independent artifact is missing related_work", rel_path)
            continue

        work_id = field_value(text, "work_id")
        if work_id != path.stem:
            add(findings, "ERROR", "work_id must match the stable filename", rel_path)
        route = field_value(text, "route")
        if route not in {"tracked", "governed"}:
            add(findings, "ERROR", f"invalid WORK route {route!r}", rel_path)
        for section in WORK_REQUIRED_SECTIONS:
            if section not in text:
                add(findings, "ERROR", f"work item is missing {section}", rel_path)
        if status in ACTIVE_WORK_STATES:
            branch = field_value(text, "branch")
            next_action = field_value(text, "next_action")
            if not branch:
                add(findings, "ERROR", "active work is missing branch", rel_path)
            elif branch in {"main", "master"}:
                add(findings, "ERROR", "tracked work must not use the default branch", rel_path)
            elif branch in active_branches:
                add(findings, "ERROR", f"active branch is shared with {active_branches[branch]}", rel_path)
            else:
                active_branches[branch] = rel_path
            if not next_action:
                add(findings, "ERROR", "active work is missing next_action", rel_path)
            if not parse_inline_list(field_value(text, "owned_paths")):
                add(
                    findings,
                    "WARN",
                    "active work has no owned_paths; parallel overlap cannot be checked",
                    rel_path,
                )
            add(findings, "INFO", f"active work: status={status}, branch={branch or 'unknown'}", rel_path)
        if status == "done":
            if not PROMOTION_COMPLETE_RE.search(text):
                add(findings, "ERROR", "closed work has incomplete Experience Promotion", rel_path)
            if re.search(r"\|[^\n|]+\|[^\n|]+\|\s*pending\s*\|", experience_section(text), re.IGNORECASE):
                add(findings, "ERROR", "closed work has a pending experience candidate", rel_path)


def parse_iso_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def check_note_freshness(root: Path, findings: list[Finding]) -> None:
    today = date.today()
    for path in markdown_files(root):
        metadata = parse_frontmatter(read_text(path))
        if not metadata or not metadata.get("review_after_days"):
            continue
        rel_path = relative(root, path)
        try:
            interval = int(metadata["review_after_days"])
        except ValueError:
            add(findings, "ERROR", "review_after_days must be an integer", rel_path)
            continue
        verified = parse_iso_date(metadata.get("last_verified_at", ""))
        if verified is None:
            add(findings, "WARN", "reviewed knowledge is missing a concrete last_verified_at date", rel_path)
        elif (today - verified).days > interval:
            add(findings, "WARN", f"knowledge is stale by {(today - verified).days - interval} day(s)", rel_path)


def skill_index_rows(index_text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in index_text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 6 or cells[0] in {"Skill", "---", "None"} or set(cells[0]) == {"-"}:
            continue
        rows.append(
            {
                "name": cells[0],
                "trigger": cells[1],
                "exclude": cells[2],
                "status": cells[3],
                "last_verified": cells[4],
                "review_after_days": cells[5],
            }
        )
    return rows


def check_project_skills(root: Path, findings: list[Finding]) -> None:
    skills_root = root / "project-skills"
    index_path = skills_root / "INDEX.md"
    index_text = read_text(index_path) if index_path.is_file() else ""
    rows = skill_index_rows(index_text)
    rows_by_name = {row["name"]: row for row in rows}
    skill_dirs = [path for path in sorted(skills_root.iterdir()) if path.is_dir() and not path.name.startswith(".")] if skills_root.is_dir() else []
    if skill_dirs and "| None |" in index_text:
        add(findings, "WARN", "project Skill index still contains the empty None row", relative(root, index_path))
    triggers: dict[str, str] = {}
    today = date.today()
    for directory in skill_dirs:
        skill_file = directory / "SKILL.md"
        rel_path = relative(root, skill_file)
        if not skill_file.is_file():
            add(findings, "ERROR", "project Skill directory is missing SKILL.md", relative(root, directory))
            continue
        text = read_text(skill_file)
        metadata = parse_frontmatter(text)
        if metadata is None:
            add(findings, "ERROR", "project Skill is missing YAML frontmatter", rel_path)
            continue
        if set(metadata) != {"name", "description"}:
            add(findings, "ERROR", "project Skill frontmatter must contain only name and description", rel_path)
        if metadata.get("name") != directory.name:
            add(findings, "ERROR", "project Skill name must match its directory", rel_path)
        if len(metadata.get("description", "")) < 24:
            add(findings, "ERROR", "project Skill description must include concrete triggers", rel_path)
        for section in SKILL_REQUIRED_SECTIONS:
            if section not in text:
                add(findings, "ERROR", f"project Skill is missing {section}", rel_path)
        row = rows_by_name.get(directory.name)
        if row is None:
            add(findings, "ERROR", "project Skill is not routed from INDEX.md", rel_path)
        else:
            status = row["status"]
            if status not in SKILL_STATES:
                add(findings, "ERROR", f"invalid project Skill status {status!r}", relative(root, index_path))
            trigger_key = re.sub(r"\s+", " ", row["trigger"].lower()).strip()
            if trigger_key in triggers:
                add(findings, "WARN", f"duplicate project Skill trigger also used by {triggers[trigger_key]}", relative(root, index_path))
            elif trigger_key:
                triggers[trigger_key] = directory.name
            if status == "needs-verification":
                add(findings, "WARN", "project Skill requires verification before use", rel_path)
            if status == "active":
                verified = parse_iso_date(row["last_verified"])
                try:
                    interval = int(row["review_after_days"])
                except ValueError:
                    interval = 0
                if verified is None or interval <= 0:
                    add(findings, "ERROR", "active project Skill needs a verification date and positive review interval", relative(root, index_path))
                elif (today - verified).days > interval:
                    add(findings, "WARN", "project Skill verification is stale", rel_path)
        if (directory / "README.md").exists():
            add(findings, "WARN", "project Skill should not include an auxiliary README.md", relative(root, directory / "README.md"))


def collect_work_records(root: Path) -> list[WorkRecord]:
    actual_branch = current_branch(root)
    dirty = worktree_is_dirty(root)
    commit = last_commit(root)
    records: list[WorkRecord] = []
    for path in workflow_artifacts(root):
        if not path.name.startswith("WORK-"):
            continue
        text = read_text(path)
        status = field_value(text, "status") or "unknown"
        if status not in ACTIVE_WORK_STATES:
            continue
        declared_branch = field_value(text, "branch") or ""
        if actual_branch and declared_branch and actual_branch != declared_branch:
            continue
        records.append(
            WorkRecord(
                work_id=field_value(text, "work_id") or path.stem,
                status=status,
                route=field_value(text, "route") or "unknown",
                declared_branch=declared_branch,
                actual_branch=actual_branch,
                worktree=str(root),
                file=str(path),
                next_action=field_value(text, "next_action") or "",
                owned_paths=parse_inline_list(field_value(text, "owned_paths")),
                dirty=dirty,
                last_commit=commit,
            )
        )
    return records


def normalized_scope(value: str) -> str:
    scope = value.replace("\\", "/").strip().removeprefix("./")
    wildcard = min((scope.find(char) for char in "*?[" if char in scope), default=-1)
    if wildcard >= 0:
        scope = scope[:wildcard]
    return scope.rstrip("/") or "."


def scopes_overlap(left: str, right: str) -> bool:
    left_scope = normalized_scope(left)
    right_scope = normalized_scope(right)
    if "." in {left_scope, right_scope}:
        return True
    return (
        left_scope == right_scope
        or left_scope.startswith(right_scope + "/")
        or right_scope.startswith(left_scope + "/")
    )


def find_scope_overlaps(records: list[WorkRecord]) -> list[dict[str, object]]:
    overlaps: list[dict[str, object]] = []
    for index, left in enumerate(records):
        for right in records[index + 1 :]:
            if left.work_id == right.work_id:
                continue
            shared = sorted(
                {f"{left_path} <-> {right_path}" for left_path in left.owned_paths for right_path in right.owned_paths if scopes_overlap(left_path, right_path)}
            )
            if shared:
                overlaps.append({"left": left.work_id, "right": right.work_id, "paths": shared})
    return overlaps


def status_payload(root: Path, all_worktrees: bool) -> dict[str, object]:
    roots = registered_worktrees(root) if all_worktrees else [root]
    records: list[WorkRecord] = []
    for candidate in roots:
        if candidate.is_dir():
            records.extend(collect_work_records(candidate))
    return {
        "repository": str(root),
        "all_worktrees": all_worktrees,
        "active_work": [asdict(record) for record in records],
        "scope_overlaps": find_scope_overlaps(records),
        "unscoped_work": [record.work_id for record in records if not record.owned_paths],
    }


def print_status(root: Path, all_worktrees: bool, as_json: bool) -> None:
    payload = status_payload(root, all_worktrees)
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=True))
        return
    print(f"Workflow Status: {root}")
    records = payload["active_work"]
    if not records:
        print("Active work: none")
    for record in records:
        marker = "dirty" if record["dirty"] else "clean"
        print(
            f"- {record['work_id']}: {record['status']}; branch={record['declared_branch'] or 'unknown'}; "
            f"worktree={record['worktree']}; {marker}; next={record['next_action'] or 'unspecified'}"
        )
    for overlap in payload["scope_overlaps"]:
        print(f"WARN: scope overlap {overlap['left']} / {overlap['right']}: {', '.join(overlap['paths'])}")
    if payload["unscoped_work"]:
        print("WARN: active work without owned paths: " + ", ".join(payload["unscoped_work"]))


def print_findings(root: Path, findings: list[Finding]) -> None:
    print(f"Workflow Doctor: {root}")
    if not findings:
        print("PASS: workflow state looks consistent")
        return
    for finding in findings:
        location = f"{finding.path}: " if finding.path else ""
        print(f"{finding.severity}: {location}{finding.message}")
    errors = sum(item.severity == "ERROR" for item in findings)
    warnings = sum(item.severity == "WARN" for item in findings)
    infos = sum(item.severity == "INFO" for item in findings)
    print(f"Summary: {errors} error(s), {warnings} warning(s), {infos} info item(s)")


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: root is not a directory: {root}", file=sys.stderr)
        return 2
    if args.status:
        print_status(root, args.all_worktrees, args.json)
        return 0

    findings: list[Finding] = []
    check_core(root, findings)
    check_placeholders(root, findings)
    check_wiki_links(root, findings)
    check_artifacts(root, findings)
    check_note_freshness(root, findings)
    check_project_skills(root, findings)
    print_findings(root, findings)
    has_errors = any(item.severity == "ERROR" for item in findings)
    has_warnings = any(item.severity == "WARN" for item in findings)
    return 1 if has_errors or (args.strict and has_warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
