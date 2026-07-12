#!/usr/bin/env python3
"""Validate stable workflow artifacts and project-Skill routing."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


CORE_FILES = (
    Path("AGENTS.md"),
    Path("CLAUDE.md"),
    Path("scripts/workflow_doctor.py"),
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

LEGACY_PATHS = (
    Path("zettelkasten/CURRENT.md"),
    Path("zettelkasten/06-requirements"),
    Path("zettelkasten/07-review"),
    Path("zettelkasten/08-technical-designs"),
    Path("zettelkasten/09-implementation-plans"),
)

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

PLACEHOLDER_RE = re.compile(r"\{\{[A-Z_]+\}\}")
WIKI_LINK_RE = re.compile(r"(?<!!)\[\[([^\]|#]+)")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
FIELD_RE_TEMPLATE = r"^{}:\s*(.*?)\s*$"


@dataclass(frozen=True)
class Finding:
    severity: str
    message: str
    path: Path | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--strict", action="store_true", help="fail on warnings")
    parser.add_argument("--status", action="store_true", help="show active work without validation")
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def relative(root: Path, path: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def add(findings: list[Finding], severity: str, message: str, path: Path | None = None) -> None:
    findings.append(Finding(severity, message, path))


def field_value(text: str, field: str) -> str | None:
    frontmatter = FRONTMATTER_RE.search(text)
    if not frontmatter:
        return None
    match = re.search(FIELD_RE_TEMPLATE.format(re.escape(field)), frontmatter.group(1), re.MULTILINE)
    if not match:
        return None
    value = match.group(1).strip().strip('"').strip("'")
    return value or None


def workflow_artifacts(root: Path) -> list[Path]:
    directory = root / "zettelkasten/06-work"
    if not directory.is_dir():
        return []
    return [
        path
        for path in sorted(directory.iterdir())
        if path.is_file() and path.name not in {"README.md", ".gitkeep"}
    ]


def current_branch(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "branch", "--show-current"],
        text=True,
        capture_output=True,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


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
    for path in LEGACY_PATHS:
        if (root / path).exists():
            add(findings, "WARN", "legacy moving-state layout remains; migrate to zettelkasten/06-work", path)
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
    index: dict[str, Path] = {}
    for path in vault.rglob("*.md"):
        index[path.relative_to(vault).with_suffix("").as_posix()] = path
        index.setdefault(path.stem, path)
    for path in sorted(vault.rglob("*.md")):
        for raw_target in WIKI_LINK_RE.findall(read_text(path)):
            target = raw_target.strip().removesuffix(".md")
            if any(marker in target for marker in ("YYYY", "<", "{{")):
                continue
            if target not in index:
                add(findings, "ERROR", f"broken wiki link: [[{target}]]", relative(root, path))


def artifact_prefix(path: Path) -> str | None:
    return next((prefix for prefix in ARTIFACT_STATES if path.name.startswith(prefix)), None)


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
            add(findings, "INFO", f"active work: status={status}, branch={branch or 'unknown'}", rel_path)
        if status == "done":
            if "- Experience Promotion complete: yes" not in text:
                add(findings, "ERROR", "closed work has incomplete Experience Promotion", rel_path)
            experience_section = text.split("## Experience Candidates", 1)[-1].split("\n## ", 1)[0]
            if re.search(r"\|[^\n|]+\|[^\n|]+\|\s*pending\s*\|", experience_section):
                add(findings, "ERROR", "closed work has a pending experience candidate", rel_path)


def skill_frontmatter(text: str) -> dict[str, str] | None:
    match = FRONTMATTER_RE.search(text)
    if not match:
        return None
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def check_project_skills(root: Path, findings: list[Finding]) -> None:
    skills_root = root / "project-skills"
    index_path = skills_root / "INDEX.md"
    index_text = read_text(index_path) if index_path.is_file() else ""
    skill_dirs = [path for path in sorted(skills_root.iterdir()) if path.is_dir() and not path.name.startswith(".")] if skills_root.is_dir() else []
    if skill_dirs and "| None |" in index_text:
        add(findings, "WARN", "project Skill index still contains the empty None row", relative(root, index_path))
    for directory in skill_dirs:
        skill_file = directory / "SKILL.md"
        rel_path = relative(root, skill_file)
        if not skill_file.is_file():
            add(findings, "ERROR", "project Skill directory is missing SKILL.md", relative(root, directory))
            continue
        text = read_text(skill_file)
        metadata = skill_frontmatter(text)
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
        if directory.name not in index_text:
            add(findings, "ERROR", "project Skill is not routed from INDEX.md", rel_path)
        if (directory / "README.md").exists():
            add(findings, "WARN", "project Skill should not include an auxiliary README.md", relative(root, directory / "README.md"))


def print_status(root: Path) -> None:
    branch = current_branch(root) or "unknown"
    print(f"Workflow Status: {root}")
    print(f"Branch: {branch}")
    active = []
    for path in workflow_artifacts(root):
        if not path.name.startswith("WORK-"):
            continue
        text = read_text(path)
        status = field_value(text, "status")
        if status in ACTIVE_WORK_STATES:
            active.append((path, status, field_value(text, "branch"), field_value(text, "next_action")))
    if not active:
        print("Active work: none")
        return
    for path, status, task_branch, next_action in active:
        marker = "*" if task_branch == branch else "-"
        print(f"{marker} {path.name}: {status}; branch={task_branch or 'unknown'}; next={next_action or 'unspecified'}")


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
        print_status(root)
        return 0

    findings: list[Finding] = []
    check_core(root, findings)
    check_placeholders(root, findings)
    check_wiki_links(root, findings)
    check_artifacts(root, findings)
    check_project_skills(root, findings)
    print_findings(root, findings)
    has_errors = any(item.severity == "ERROR" for item in findings)
    has_warnings = any(item.severity == "WARN" for item in findings)
    return 1 if has_errors or (args.strict and has_warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
