#!/usr/bin/env python3
"""Validate workflow artifacts, project Skills, and cross-worktree task state."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

from workflow_archive import (ARCHIVE_ROOT, ArchiveError, archive_reference,
                              open_artifacts, route_matches, route_path, safe_path,
                              scoped_artifacts, validate_terminal_evidence)


CORE_FILES = (
    Path("AGENTS.md"),
    Path("CLAUDE.md"),
    Path("zettelkasten/AI.md"),
    Path("zettelkasten/workflow.md"),
    Path("zettelkasten/skill-lifecycle.md"),
    Path("zettelkasten/git-collaboration.md"),
    Path("zettelkasten/templates/initiative.md"),
    Path("zettelkasten/templates/work-item.md"),
    Path("zettelkasten/templates/workflow-observations.md"),
    Path("zettelkasten/work/README.md"),
    Path("zettelkasten/knowledge-lifecycle.md"),
    Path("project-skills/INDEX.md"),
)

CORE_DIRECTORIES = (Path("zettelkasten/work"), Path("project-skills"))

WORK_STATES = {"backlog", "active", "blocked", "review", "done", "cancelled"}
INITIATIVE_STATES = WORK_STATES

ACTIVE_WORK_STATES = {"active", "blocked", "review"}
ACTIVE_INITIATIVE_STATES = {"active", "blocked", "review"}
TERMINAL_STATES = {"done", "cancelled"}
WORK_ID_RE = re.compile(r"^WORK-[0-9]{14}-[a-z0-9][a-z0-9-]*$")
INITIATIVE_ID_RE = re.compile(
    r"^INITIATIVE-[0-9]{14}-[a-z0-9][a-z0-9-]*$"
)
WORK_REQUIRED_SECTIONS = (
    "## Parent Coordination",
    "## Goal And Acceptance",
    "## Route Decision",
    "## Context Pack",
    "## Scope And Ownership",
    "## Validation",
    "## Experience Candidates",
    "## Context Checkpoint",
)
INITIATIVE_REQUIRED_SECTIONS = (
    "## Goal And Boundaries",
    "## Overall Acceptance",
    "## Shared Decisions And Gates",
    "## Decomposition Contract",
    "## Integration And Closure",
    "## Coordination Checkpoint",
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
EXPERIENCE_DECISIONS = {"pending", "promoted", "updated", "no-op", "not-promoted"}

PLACEHOLDER_RE = re.compile(r"\{\{[A-Z_]+\}\}")
WIKI_LINK_RE = re.compile(r"(?<!!)\[\[([^\]|#]+)")
FENCED_CODE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})[^\n]*\n.*?(?:^[ \t]*\1[^\n]*$|\Z)", re.DOTALL | re.MULTILINE)
INLINE_CODE_RE = re.compile(r"(`+)(?:.|\n)*?\1")
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
    initiative_id: str
    external_parent: str
    depends_on: tuple[str, ...]
    owned_paths: tuple[str, ...]
    dirty: bool
    last_commit: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--strict", action="store_true", help="fail on warnings")
    parser.add_argument("--status", action="store_true", help="show active work without validation")
    parser.add_argument("--full", action="store_true", help="explicitly audit all stable records and archived evidence")
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


def strip_code(text: str) -> str:
    """Blank out fenced blocks and inline code spans.

    Wiki links are not links inside code. Without this, a documented shell
    conditional such as [[ "$rc" == "0" ]] is reported as a broken wiki link.
    Spans are replaced with blank lines rather than removed so that any
    line-based reporting keeps its original line numbers.
    """
    def blank(match: re.Match[str]) -> str:
        return "\n" * match.group(0).count("\n")

    return INLINE_CODE_RE.sub(blank, FENCED_CODE_RE.sub(blank, text))


def relative(root: Path, path: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def add(findings: list[Finding], severity: str, message: str, path: Path | None = None) -> None:
    findings.append(Finding(severity, message, path))


FrontmatterValue = str | tuple[str, ...]


def decode_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
        return decoded if isinstance(decoded, str) else str(decoded)
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def parse_frontmatter(text: str) -> dict[str, FrontmatterValue] | None:
    """Parse top-level scalar and sequence fields without a YAML dependency."""
    match = FRONTMATTER_RE.search(text)
    if not match:
        return None
    lines = match.group(1).splitlines()
    values: dict[str, FrontmatterValue] = {}
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
        if not block_style:
            sequence_index = index + 1
            items: list[str] = []
            while sequence_index < len(lines):
                candidate = lines[sequence_index]
                if candidate and not candidate[0].isspace():
                    break
                stripped = candidate.strip()
                if stripped:
                    if not stripped.startswith("- "):
                        break
                    items.append(decode_scalar(stripped[2:]))
                sequence_index += 1
            if items:
                values[key] = tuple(items)
                index = sequence_index
                continue
        values[key] = decode_scalar(raw_value)
        index += 1
    return values


def field_value(text: str, field: str) -> str | None:
    values = parse_frontmatter(text)
    if values is None:
        return None
    raw_value = values.get(field, "")
    if not isinstance(raw_value, str):
        return None
    value = raw_value.strip()
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


def field_list(text: str, field: str) -> tuple[str, ...]:
    values = parse_frontmatter(text)
    if values is None:
        return ()
    value = values.get(field, "")
    if isinstance(value, tuple):
        return value
    return parse_inline_list(value)


def workflow_artifacts(root: Path, full: bool = False) -> list[Path]:
    if not full:
        return scoped_artifacts(root)
    directory = root / "zettelkasten/work"
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


def markdown_files(root: Path, full: bool = False) -> list[Path]:
    files: list[Path] = []
    for relative_path in (Path("AGENTS.md"), Path("CLAUDE.md")):
        path = root / relative_path
        if path.is_file():
            files.append(path)
    for directory in (root / "zettelkasten", root / "project-skills"):
        if directory.is_dir():
            for current, directories, names in os.walk(directory, followlinks=False):
                directories[:] = sorted(name for name in directories
                    if not (Path(current) / name).is_symlink()
                    and (full or Path(current) / name not in {
                        root / ARCHIVE_ROOT, root / "zettelkasten/work", root / "zettelkasten/templates"}))
                files.extend(safe_path(root, (Path(current) / name).relative_to(root))
                             for name in sorted(names) if name.endswith(".md"))
    if not full:
        files.extend(workflow_artifacts(root))
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
    for marker in (".repo-continuity-template", ".ai-collaboration-workflow-template"):
        if (root / marker).is_file():
            add(
                findings,
                "WARN",
                "payload marker is present; initialization is not finished",
                Path(marker),
            )


def check_placeholders(root: Path, findings: list[Finding], full: bool = False) -> None:
    for path in markdown_files(root, full):
        if path.is_relative_to(root / ARCHIVE_ROOT):
            continue
        text = read_text(path)
        matches = sorted(set(PLACEHOLDER_RE.findall(text)))
        if matches:
            add(findings, "ERROR", "unresolved placeholders: " + ", ".join(matches), relative(root, path))


def check_wiki_links(root: Path, findings: list[Finding], full: bool = False) -> None:
    vault = root / "zettelkasten"
    if not vault.is_dir():
        return
    by_stem: dict[str, list[Path]] = {}
    paths = [path for path in markdown_files(root, full) if path.is_relative_to(vault)]
    for path in paths:
        by_stem.setdefault(path.stem, []).append(path)
    for path in paths:
        for raw_target in WIKI_LINK_RE.findall(strip_code(read_text(path))):
            target = raw_target.strip().removesuffix(".md")
            if any(marker in target for marker in ("YYYY", "<", "{{")):
                continue
            if "/" in target:
                candidate = safe_path(root, Path("zettelkasten") / (target + ".md"))
                if not candidate.is_file():
                    add(findings, "ERROR", f"broken wiki link: [[{target}]]", relative(root, path))
                continue
            candidates = by_stem.get(target, [])
            if not candidates:
                add(findings, "ERROR", f"broken wiki link: [[{target}]]", relative(root, path))
            elif len(candidates) > 1:
                choices = ", ".join(item.relative_to(vault).as_posix() for item in candidates)
                add(findings, "ERROR", f"ambiguous wiki link [[{target}]]; use an explicit path: {choices}", relative(root, path))


def heading_re(heading: str) -> re.Pattern[str]:
    """Match one level-2 heading on a line of its own, ignoring case.

    Anchoring matters in both directions. Substring matching let an inline
    mention of a heading inside prose satisfy a required-section check, and it
    let the same mention hijack where section_body() started reading.
    """
    title = heading.strip().removeprefix("##").strip()
    return re.compile(
        rf"^##[ \t]+(?P<title>{re.escape(title)}).*$", re.MULTILINE | re.IGNORECASE
    )


def find_heading(text: str, heading: str) -> re.Match[str] | None:
    return heading_re(heading).search(text)


def section_body(text: str, heading: str) -> str:
    match = find_heading(text, heading)
    if match is None:
        return ""
    rest = text[match.end() :]
    following = re.search(r"^## ", rest, re.MULTILINE)
    return rest[: following.start()] if following else rest


def report_heading(
    findings: list,
    text: str,
    section: str,
    subject: str,
    rel_path: Path,
) -> None:
    """Report an absent required heading, and case drift separately.

    A heading whose case differs from the template is present, so calling it
    missing is factually wrong and trains readers to ignore the finding.
    """
    match = find_heading(text, section)
    if match is None:
        add(findings, "ERROR", f"{subject} is missing {section}", rel_path)
        return
    expected = section.strip().removeprefix("##").strip()
    if match.group("title") != expected:
        add(
            findings,
            "WARN",
            f"{subject} heading {match.group('title')!r} differs in case from {expected!r}",
            rel_path,
        )


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


def experience_candidate_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section_body(text, "Experience Candidates").splitlines():
        cells = split_markdown_table_row(line)
        if len(cells) >= 5 and cells[0] not in {"Candidate", "---"}:
            rows.append(cells)
    return rows


def has_pending_experience_decision(text: str) -> bool:
    return any(
        cells[2].strip().lower() == "pending"
        for cells in experience_candidate_rows(text)
    )


def has_pending_governed_gate(text: str) -> bool:
    for line in section_body(text, "Governed Gates").splitlines():
        cells = split_markdown_table_row(line)
        if len(cells) >= 4 and cells[0] not in {"Gate or decision", "---"}:
            if cells[3].strip().lower() == "pending":
                return True
    return False


def has_pending_initiative_gate(text: str) -> bool:
    for line in section_body(text, "Shared Decisions And Gates").splitlines():
        cells = split_markdown_table_row(line)
        if len(cells) >= 5 and cells[0] not in {"Decision or gate", "---"}:
            if cells[0].strip() and cells[4].strip().lower() == "pending":
                return True
    return False


def check_artifacts(root: Path, findings: list[Finding], full: bool = False) -> None:
    artifacts = workflow_artifacts(root, full)
    initiative_paths: dict[str, Path] = {}
    work_paths: dict[str, Path] = {}
    work_texts: dict[str, str] = {}
    work_statuses: dict[str, str] = {}
    dependencies: dict[str, tuple[str, ...]] = {}
    active_branches: dict[str, Path] = {}
    for path in artifacts:
        rel_path = relative(root, path)
        if path.suffix != ".md":
            add(findings, "ERROR", "unexpected work artifact name", rel_path)
            continue
        if path.name.startswith("INITIATIVE-"):
            text = read_text(path)
            status = field_value(text, "status")
            initiative_id = field_value(text, "initiative_id")
            if not INITIATIVE_ID_RE.fullmatch(path.stem):
                add(findings, "ERROR", "invalid Initiative filename", rel_path)
            if initiative_id != path.stem:
                add(findings, "ERROR", "initiative_id must match the stable filename", rel_path)
            elif initiative_id in initiative_paths:
                add(findings, "ERROR", "duplicate Initiative ID", rel_path)
            else:
                initiative_paths[initiative_id] = path
            if status not in INITIATIVE_STATES:
                add(findings, "ERROR", f"invalid Initiative status {status!r}", rel_path)
            if not field_value(text, "archive_ref"):
                for section in INITIATIVE_REQUIRED_SECTIONS:
                    report_heading(findings, text, section, "Initiative", rel_path)
            if status in ACTIVE_INITIATIVE_STATES:
                next_action = field_value(text, "next_action")
                if not next_action:
                    add(findings, "ERROR", "active Initiative is missing next_action", rel_path)
                add(findings, "INFO", f"active Initiative: status={status}", rel_path)
            continue
        if not path.name.startswith("WORK-"):
            add(findings, "ERROR", "unexpected work artifact name", rel_path)
            continue
        text = read_text(path)
        status = field_value(text, "status")
        if status not in WORK_STATES:
            add(findings, "ERROR", f"invalid WORK status {status!r}", rel_path)

        work_id = field_value(text, "work_id")
        if not WORK_ID_RE.fullmatch(path.stem):
            add(findings, "ERROR", "invalid WORK filename", rel_path)
        if work_id != path.stem:
            add(findings, "ERROR", "work_id must match the stable filename", rel_path)
        elif work_id in work_paths:
            add(findings, "ERROR", "duplicate WORK ID", rel_path)
        else:
            work_paths[work_id] = path
            work_texts[work_id] = text
            work_statuses[work_id] = status or "unknown"
            dependencies[work_id] = field_list(text, "depends_on") if full or status not in TERMINAL_STATES else ()
        initiative_id = field_value(text, "initiative_id")
        external_parent = field_value(text, "external_parent")
        if initiative_id and external_parent:
            add(
                findings,
                "ERROR",
                "WORK must use either initiative_id or external_parent, not both",
                rel_path,
            )
        if initiative_id and not INITIATIVE_ID_RE.fullmatch(initiative_id):
            add(findings, "ERROR", f"invalid initiative_id {initiative_id!r}", rel_path)
        route = field_value(text, "route")
        if route not in {"tracked", "governed"}:
            add(findings, "ERROR", f"invalid WORK route {route!r}", rel_path)
        if not field_value(text, "archive_ref"):
            for section in WORK_REQUIRED_SECTIONS:
                report_heading(findings, text, section, "work item", rel_path)
        for cells in experience_candidate_rows(text):
            decision = cells[2].strip().lower()
            if decision not in EXPERIENCE_DECISIONS:
                add(findings, "ERROR", f"invalid experience decision {decision!r}", rel_path)
            if decision != "pending" and not cells[0].strip():
                add(findings, "ERROR", "decided experience candidate is missing its lesson", rel_path)
            if decision in {"promoted", "updated", "no-op"} and not cells[3].strip():
                add(findings, "ERROR", "promoted experience is missing its destination", rel_path)
            if decision != "pending" and not cells[4].strip():
                add(findings, "ERROR", "decided experience is missing evidence or outcome", rel_path)
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
            if not field_list(text, "owned_paths"):
                add(
                    findings,
                    "WARN",
                    "active work has no owned_paths; parallel overlap cannot be checked",
                    rel_path,
                )
            add(findings, "INFO", f"active work: status={status}, branch={branch or 'unknown'}", rel_path)
        if status == "done" and not field_value(text, "archive_ref"):
            if not PROMOTION_COMPLETE_RE.search(text):
                add(findings, "ERROR", "closed work has incomplete Experience Promotion", rel_path)
            if has_pending_experience_decision(text):
                add(findings, "ERROR", "closed work has a pending experience candidate", rel_path)
            if route == "governed" and has_pending_governed_gate(text):
                add(findings, "ERROR", "closed governed work has a pending gate", rel_path)

    for work_id, path in work_paths.items():
        if not full and work_statuses[work_id] in TERMINAL_STATES:
            continue
        rel_path = relative(root, path)
        initiative_id = field_value(work_texts[work_id], "initiative_id")
        if initiative_id and initiative_id not in initiative_paths:
            add(findings, "ERROR", f"local Initiative does not exist: {initiative_id}", rel_path)
        for dependency in dependencies[work_id]:
            if not WORK_ID_RE.fullmatch(dependency):
                add(findings, "ERROR", f"invalid WORK dependency {dependency!r}", rel_path)
            elif dependency == work_id:
                add(findings, "ERROR", "WORK cannot depend on itself", rel_path)
            elif dependency not in work_paths:
                add(findings, "ERROR", f"WORK dependency does not exist: {dependency}", rel_path)
            elif (
                work_statuses[work_id] in {"active", "review", "done"}
                and work_statuses[dependency] != "done"
            ):
                add(
                    findings,
                    "ERROR",
                    f"{work_statuses[work_id]} WORK has incomplete dependency: {dependency}",
                    rel_path,
                )

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(work_id: str, trail: tuple[str, ...]) -> None:
        if work_id in visited:
            return
        if work_id in visiting:
            cycle = trail[trail.index(work_id) :] + (work_id,)
            add(
                findings,
                "ERROR",
                "WORK dependency cycle: " + " -> ".join(cycle),
                relative(root, work_paths[work_id]),
            )
            return
        visiting.add(work_id)
        for dependency in dependencies.get(work_id, ()):
            if dependency in work_paths:
                visit(dependency, trail + (work_id,))
        visiting.remove(work_id)
        visited.add(work_id)

    for work_id in work_paths:
        visit(work_id, ())

    for initiative_id, path in initiative_paths.items():
        text = read_text(path)
        status = field_value(text, "status")
        children = sorted(
            work_id
            for work_id, work_text in work_texts.items()
            if field_value(work_text, "initiative_id") == initiative_id
        )
        if status == "done" and full:
            nonterminal = [
                work_id for work_id in children if work_statuses[work_id] not in TERMINAL_STATES
            ]
            if not children:
                add(findings, "ERROR", "done Initiative has no child WORK", relative(root, path))
            if nonterminal:
                add(
                    findings,
                    "ERROR",
                    "done Initiative has nonterminal children: " + ", ".join(nonterminal),
                    relative(root, path),
                )
            if not field_value(text, "archive_ref") and has_pending_initiative_gate(text):
                add(
                    findings,
                    "ERROR",
                    "done Initiative has a pending shared gate",
                    relative(root, path),
                )


def check_lifecycle(root: Path, findings: list[Finding], full: bool = False) -> None:
    routes = set(open_artifacts(root))
    for path in workflow_artifacts(root, full):
        text = read_text(path)
        is_open = field_value(text, "status") in {"backlog", "active", "blocked", "review"}
        if is_open != (path in routes):
            add(findings, "ERROR", "open-work route disagrees with source; review reindex --dry-run", relative(root, path))
        if path in routes and not route_matches(path, text, read_text(route_path(root, path))):
            add(findings, "ERROR", "stale work routing hint; update the route with its source", relative(root, path))
    for path in markdown_files(root, full):
        if path.is_relative_to(root / ARCHIVE_ROOT):
            continue
        text = read_text(path)
        if not field_value(text, "archive_ref"):
            continue
        rel_path = relative(root, path)
        for field in ("archive_summary", "archive_reason", "archive_sha256", "archived_at"):
            if not field_value(text, field):
                add(findings, "ERROR", f"archived record is missing {field}", rel_path)
        if field_value(text, "status") not in TERMINAL_STATES | {"superseded", "deprecated", "retired"}:
            add(findings, "ERROR", "restore archived content before reopening or reactivating it", rel_path)
        try:
            snapshot = archive_reference(root, text)
            if not re.fullmatch(r"[0-9a-f]{64}", field_value(text, "archive_sha256") or ""):
                raise ArchiveError("invalid archive checksum")
            if parse_iso_date(field_value(text, "archived_at") or "") is None:
                raise ArchiveError("invalid archive date")
            if full:
                original = snapshot.read_bytes()
                if hashlib.sha256(original).hexdigest() != field_value(text, "archive_sha256"):
                    raise ArchiveError("archive checksum mismatch")
                evidence = original.decode("utf-8")
                for field in ("work_id", "initiative_id", "depends_on", "status", "route"):
                    if field_value(text, field) != field_value(evidence, field):
                        raise ArchiveError(f"archived {field} differs from original; restore before changing task state")
                if path.parent == root / "zettelkasten/work":
                    validate_terminal_evidence(path, evidence)
        except (ArchiveError, UnicodeError) as exc:
            add(findings, "ERROR", str(exc), rel_path)


def parse_iso_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def check_note_freshness(root: Path, findings: list[Finding], full: bool = False) -> None:
    today = date.today()
    for path in markdown_files(root, full):
        if path.is_relative_to(root / ARCHIVE_ROOT):
            continue
        metadata = parse_frontmatter(read_text(path))
        if not metadata or "archive_ref" in metadata or "review_after_days" not in metadata:
            continue
        rel_path = relative(root, path)
        try:
            interval = int(str(metadata["review_after_days"]))
        except (TypeError, ValueError):
            add(findings, "ERROR", "review_after_days must be an integer", rel_path)
            continue
        if interval <= 0:
            add(findings, "ERROR", "review_after_days must be positive", rel_path)
            continue
        verified = parse_iso_date(str(metadata.get("last_verified_at", "")))
        if verified is None:
            add(findings, "WARN", "reviewed knowledge is missing a concrete last_verified_at date", rel_path)
        elif (today - verified).days > interval:
            add(findings, "WARN", f"knowledge is stale by {(today - verified).days - interval} day(s)", rel_path)


def skill_index_rows(index_text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in index_text.splitlines():
        if not line.startswith("|"):
            continue
        cells = split_markdown_table_row(line)
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
        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if name != directory.name:
            add(findings, "ERROR", "project Skill name must match its directory", rel_path)
        if not isinstance(description, str) or len(description) < 24:
            add(findings, "ERROR", "project Skill description must include concrete triggers", rel_path)
        for section in SKILL_REQUIRED_SECTIONS:
            report_heading(findings, text, section, "project Skill", rel_path)
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
    if not actual_branch:
        return []
    dirty = worktree_is_dirty(root)
    commit = last_commit(root)
    records: list[WorkRecord] = []
    for path in open_artifacts(root):
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
                initiative_id=field_value(text, "initiative_id") or "",
                external_parent=field_value(text, "external_parent") or "",
                depends_on=field_list(text, "depends_on"),
                owned_paths=field_list(text, "owned_paths"),
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


def status_payload(root: Path, all_worktrees: bool, full: bool = False) -> dict[str, object]:
    roots = registered_worktrees(root) if all_worktrees else [root]
    records: list[WorkRecord] = []
    detached_worktrees: list[str] = []
    for candidate in roots:
        if candidate.is_dir():
            if not current_branch(candidate):
                detached_worktrees.append(str(candidate))
                continue
            records.extend(collect_work_records(candidate))
    initiative_rollups: list[dict[str, object]] = []
    current_artifacts = workflow_artifacts(root, full)
    current_works = {
        field_value(read_text(path), "work_id") or path.stem: read_text(path)
        for path in current_artifacts
        if path.name.startswith("WORK-")
    }
    for path in current_artifacts:
        if not path.name.startswith("INITIATIVE-"):
            continue
        text = read_text(path)
        initiative_id = field_value(text, "initiative_id") or path.stem
        children = [
            {
                "work_id": work_id,
                "status": field_value(work_text, "status") or "unknown",
                "depends_on": list(field_list(work_text, "depends_on")),
            }
            for work_id, work_text in sorted(current_works.items())
            if field_value(work_text, "initiative_id") == initiative_id
        ]
        initiative_rollups.append(
            {
                "initiative_id": initiative_id,
                "status": field_value(text, "status") or "unknown",
                "next_action": field_value(text, "next_action") or "",
                "file": str(path),
                "children": children,
            }
        )
    return {
        "repository": str(root),
        "scope": "full" if full else "open work and exact dependencies; Initiative rollups omit unreferenced historical children",
        "all_worktrees": all_worktrees,
        "initiatives": initiative_rollups,
        "active_work": [asdict(record) for record in records],
        "scope_overlaps": find_scope_overlaps(records),
        "unscoped_work": [record.work_id for record in records if not record.owned_paths],
        "detached_worktrees": detached_worktrees,
    }


def print_status(root: Path, all_worktrees: bool, as_json: bool, full: bool = False) -> None:
    payload = status_payload(root, all_worktrees, full)
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    print(f"Scope: {payload['scope']}")
    print(f"Workflow Status: {root}")
    for initiative in payload["initiatives"]:
        child_counts: dict[str, int] = {}
        for child in initiative["children"]:
            child_counts[child["status"]] = child_counts.get(child["status"], 0) + 1
        rollup = ", ".join(
            f"{status}={count}" for status, count in sorted(child_counts.items())
        ) or "no children"
        print(
            f"- {initiative['initiative_id']}: {initiative['status']}; {rollup}; "
            f"next={initiative['next_action'] or 'unspecified'}"
        )
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
    for worktree in payload["detached_worktrees"]:
        print(f"WARN: detached worktree has no branch-matched active work: {worktree}")


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


def run_checks(args: argparse.Namespace) -> int:
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: root is not a directory: {root}", file=sys.stderr)
        return 2
    if args.status:
        print_status(root, args.all_worktrees, args.json, args.full)
        return 0

    findings: list[Finding] = []
    check_core(root, findings)
    try:
        check_placeholders(root, findings, args.full)
        check_wiki_links(root, findings, args.full)
        check_artifacts(root, findings, args.full)
        check_note_freshness(root, findings, args.full)
        check_lifecycle(root, findings, args.full)
    except (ArchiveError, OSError) as exc:
        add(findings, "ERROR", str(exc))
    check_project_skills(root, findings)
    print_findings(root, findings)
    has_errors = any(item.severity == "ERROR" for item in findings)
    has_warnings = any(item.severity == "WARN" for item in findings)
    return 1 if has_errors or (args.strict and has_warnings) else 0


def main() -> int:
    try:
        return run_checks(parse_args())
    except (ArchiveError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
