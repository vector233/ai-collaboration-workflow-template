#!/usr/bin/env python3
"""Check AI Collaboration Workflow repository state for common drift."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


CORE_FILES = (
    Path("AGENTS.md"),
    Path("CLAUDE.md"),
    Path("scripts/workflow_doctor.py"),
    Path("zettelkasten/AI.md"),
    Path("zettelkasten/CURRENT.md"),
    Path("zettelkasten/00-governance/ai-workflow.md"),
    Path("zettelkasten/00-governance/templates/review.md"),
    Path("zettelkasten/06-requirements/README.md"),
    Path("zettelkasten/07-review/README.md"),
    Path("zettelkasten/08-technical-designs/README.md"),
    Path("zettelkasten/09-implementation-plans/README.md"),
)

CORE_DIRECTORIES = (
    Path("zettelkasten/06-requirements/backlog"),
    Path("zettelkasten/06-requirements/in-progress"),
    Path("zettelkasten/06-requirements/done"),
    Path("zettelkasten/07-review/pending"),
    Path("zettelkasten/07-review/in-review"),
    Path("zettelkasten/07-review/done"),
    Path("zettelkasten/08-technical-designs/pending"),
    Path("zettelkasten/08-technical-designs/approved"),
    Path("zettelkasten/08-technical-designs/implemented"),
    Path("zettelkasten/09-implementation-plans"),
)

STATE_DIRECTORIES = {
    Path("zettelkasten/06-requirements/backlog"): ("REQ-", "backlog"),
    Path("zettelkasten/06-requirements/in-progress"): ("REQ-", "in-progress"),
    Path("zettelkasten/06-requirements/done"): ("REQ-", "done"),
    Path("zettelkasten/07-review/pending"): ("REVIEW-", "pending"),
    Path("zettelkasten/07-review/in-review"): ("REVIEW-", "in-review"),
    Path("zettelkasten/07-review/done"): ("REVIEW-", "done"),
    Path("zettelkasten/08-technical-designs/pending"): ("TECH-", "pending"),
    Path("zettelkasten/08-technical-designs/approved"): ("TECH-", "approved"),
    Path("zettelkasten/08-technical-designs/implemented"): ("TECH-", "implemented"),
}

PLAN_ALLOWED_STATES = {"draft", "ready", "executing", "completed", "superseded"}
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z_]+\}\}")
STATUS_RE = re.compile(r"^status:\s*([^\n#]+)", re.MULTILINE)
WIKI_LINK_RE = re.compile(r"(?<!!)\[\[([^\]|#]+)")
PROMOTION_DECISION_RE = re.compile(
    r"^-\s*Promote to durable rule:\s*(.*?)\s*$",
    re.MULTILINE,
)


@dataclass(frozen=True)
class Finding:
    severity: str
    message: str
    path: Path | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate AI Collaboration Workflow state in a target repository."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root to check (default: current directory).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero on warnings as well as errors.",
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for relative in (Path("AGENTS.md"), Path("CLAUDE.md")):
        path = root / relative
        if path.is_file():
            files.append(path)
    vault = root / "zettelkasten"
    if vault.is_dir():
        files.extend(sorted(vault.rglob("*.md")))
    return files


def relative_to_root(root: Path, path: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def artifact_files(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return [
        path
        for path in sorted(directory.iterdir())
        if path.is_file() and path.name != ".gitkeep"
    ]


def status_value(text: str) -> str | None:
    match = STATUS_RE.search(text)
    if not match:
        return None
    return match.group(1).strip().strip('"').strip("'")


def wiki_index(vault: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for path in vault.rglob("*.md"):
        relative = path.relative_to(vault).with_suffix("").as_posix()
        index[relative] = path
        index.setdefault(path.stem, path)
    return index


def normalize_wiki_target(target: str) -> str:
    normalized = target.strip()
    if normalized.endswith(".md"):
        normalized = normalized[:-3]
    return normalized


def add(
    finding_list: list[Finding],
    severity: str,
    message: str,
    path: Path | None = None,
) -> None:
    finding_list.append(Finding(severity=severity, message=message, path=path))


def promotion_decision(text: str) -> str | None:
    match = PROMOTION_DECISION_RE.search(text)
    if not match:
        return None
    return match.group(1).strip().lower()


def check_core(root: Path, findings: list[Finding]) -> None:
    for relative in CORE_FILES:
        if not (root / relative).is_file():
            add(findings, "ERROR", "missing required file", relative)
    for relative in CORE_DIRECTORIES:
        if not (root / relative).is_dir():
            add(findings, "ERROR", "missing required directory", relative)

    if (root / "INIT.md").is_file():
        add(
            findings,
            "WARN",
            "INIT.md is present; initialization is not finished",
            Path("INIT.md"),
        )
    if (root / ".ai-collaboration-workflow-template").is_file():
        add(
            findings,
            "WARN",
            "payload marker is present; remove it after initialization",
            Path(".ai-collaboration-workflow-template"),
        )


def check_placeholders(root: Path, findings: list[Finding]) -> None:
    for path in markdown_files(root):
        text = read_text(path)
        matches = sorted(set(PLACEHOLDER_RE.findall(text)))
        if matches:
            add(
                findings,
                "ERROR",
                "unresolved template placeholders: " + ", ".join(matches),
                relative_to_root(root, path),
            )
        if "UMBRELLA-ONLY" in text:
            add(
                findings,
                "ERROR",
                "umbrella-mode marker remains after initialization",
                relative_to_root(root, path),
            )


def check_wiki_links(root: Path, findings: list[Finding]) -> None:
    vault = root / "zettelkasten"
    if not vault.is_dir():
        return
    index = wiki_index(vault)
    for path in sorted(vault.rglob("*.md")):
        text = read_text(path)
        for raw_target in WIKI_LINK_RE.findall(text):
            target = normalize_wiki_target(raw_target)
            if any(marker in target for marker in ("YYYY", "<", "{{")):
                continue
            if target not in index:
                add(
                    findings,
                    "ERROR",
                    f"broken wiki link: [[{target}]]",
                    relative_to_root(root, path),
                )


def check_state_directories(root: Path, findings: list[Finding]) -> None:
    for relative, (prefix, expected_status) in STATE_DIRECTORIES.items():
        for path in artifact_files(root / relative):
            rel_path = relative_to_root(root, path)
            if not path.name.startswith(prefix) or path.suffix != ".md":
                add(findings, "ERROR", f"unexpected file in state directory; expected {prefix}*.md", rel_path)
                continue

            text = read_text(path)
            actual_status = status_value(text)
            if actual_status is None:
                add(findings, "ERROR", "missing status frontmatter", rel_path)
            elif actual_status != expected_status:
                add(
                    findings,
                    "ERROR",
                    f"status {actual_status!r} does not match directory state {expected_status!r}",
                    rel_path,
                )

            if prefix == "REVIEW-" and "## Rule Promotion Check" not in text:
                add(findings, "ERROR", "review handoff is missing Rule Promotion Check", rel_path)
            elif prefix == "REVIEW-" and expected_status == "done":
                decision = promotion_decision(text)
                if decision in (None, "", "yes / no"):
                    add(
                        findings,
                        "ERROR",
                        "closed review has incomplete Rule Promotion Check decision",
                        rel_path,
                    )


def check_plans(root: Path, findings: list[Finding]) -> None:
    plans = root / "zettelkasten/09-implementation-plans"
    for path in artifact_files(plans):
        rel_path = relative_to_root(root, path)
        if path.name in {"README.md", ".gitkeep"}:
            continue
        if not path.name.startswith("PLAN-") or path.suffix != ".md":
            add(findings, "ERROR", "unexpected implementation-plan file; expected PLAN-*.md", rel_path)
            continue
        actual_status = status_value(read_text(path))
        if actual_status is None:
            add(findings, "ERROR", "missing status frontmatter", rel_path)
        elif actual_status not in PLAN_ALLOWED_STATES:
            add(findings, "ERROR", f"unknown PLAN status {actual_status!r}", rel_path)


def check_activity(root: Path, findings: list[Finding]) -> None:
    active_requirements = artifact_files(root / "zettelkasten/06-requirements/in-progress")
    open_reviews = [
        *artifact_files(root / "zettelkasten/07-review/pending"),
        *artifact_files(root / "zettelkasten/07-review/in-review"),
    ]
    current_state = root / "zettelkasten/CURRENT.md"
    current_text = read_text(current_state) if current_state.is_file() else ""
    for path in active_requirements:
        rel_path = relative_to_root(root, path)
        add(
            findings,
            "INFO",
            "active requirement; verify its delivery path before editing business code",
            rel_path,
        )
        if path.stem not in current_text:
            add(findings, "WARN", "active requirement is not referenced in CURRENT.md", rel_path)
    for path in open_reviews:
        rel_path = relative_to_root(root, path)
        add(
            findings,
            "INFO",
            "open review blocks the next implementation slice unless explicitly waived",
            rel_path,
        )
        if path.stem not in current_text:
            add(findings, "WARN", "open review is not referenced in CURRENT.md", rel_path)


def print_findings(root: Path, findings: list[Finding]) -> None:
    print(f"Workflow Doctor: {root}")
    if not findings:
        print("PASS: workflow state looks consistent")
        return
    for finding in findings:
        location = f"{finding.path}: " if finding.path else ""
        print(f"{finding.severity}: {location}{finding.message}")

    error_count = sum(1 for finding in findings if finding.severity == "ERROR")
    warning_count = sum(1 for finding in findings if finding.severity == "WARN")
    info_count = sum(1 for finding in findings if finding.severity == "INFO")
    print(
        "Summary: "
        f"{error_count} error(s), {warning_count} warning(s), {info_count} info item(s)"
    )


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    findings: list[Finding] = []

    if not root.is_dir():
        print(f"ERROR: root is not a directory: {root}", file=sys.stderr)
        return 2

    check_core(root, findings)
    check_placeholders(root, findings)
    check_wiki_links(root, findings)
    check_state_directories(root, findings)
    check_plans(root, findings)
    check_activity(root, findings)
    print_findings(root, findings)

    has_errors = any(finding.severity == "ERROR" for finding in findings)
    has_warnings = any(finding.severity == "WARN" for finding in findings)
    if has_errors or (args.strict and has_warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
