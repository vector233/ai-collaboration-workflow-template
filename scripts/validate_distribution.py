#!/usr/bin/env python3
"""Validate the canonical template payload through a temporary project lifecycle."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "template"
PAYLOAD_MARKER = PAYLOAD / ".ai-collaboration-workflow-template"
BOOTSTRAP = (
    ROOT
    / "skills"
    / "ai-collaboration-workflow"
    / "scripts"
    / "bootstrap_template.py"
)

REQUIRED_STATE_DIRECTORIES = (
    Path("zettelkasten/06-requirements/backlog"),
    Path("zettelkasten/06-requirements/in-progress"),
    Path("zettelkasten/06-requirements/done"),
    Path("zettelkasten/07-review/pending"),
    Path("zettelkasten/07-review/in-review"),
    Path("zettelkasten/07-review/done"),
    Path("zettelkasten/08-technical-designs/pending"),
    Path("zettelkasten/08-technical-designs/approved"),
    Path("zettelkasten/08-technical-designs/implemented"),
)

FORBIDDEN_PAYLOAD_TEXT = (
    "vector233",
    "community-publishing",
    "This repository is a template for AI-assisted project documentation",
    "REQ-20260618170000-shareable-workflow-skill",
    "TECH-20260618170500-shareable-workflow-skill",
    "REVIEW-20260618174000-shareable-workflow-skill",
)

PLACEHOLDER_VALUES = {
    "{{PROJECT_NAME}}": "ExampleSaaS",
    "{{PROJECT_NAME_SAFE}}": "ExampleSaaS",
    "{{PROJECT_DESCRIPTION}}": "A sample project used to validate template distribution",
    "{{TECH_STACK}}": "Python · SQLite · HTML",
    "{{REPO_TYPE}}": "single",
    "{{SUB_PROJECTS}}": "Not applicable for a single-project repository.",
    "{{DOMAINS}}": (
        "| Environment | Domain / port |\n"
        "|---|---|\n"
        "| Local | localhost:8000 |"
    ),
    "{{REPOS}}": "- example/example-saas",
}


class ValidationFailure(RuntimeError):
    """Raised when the distribution contract is broken."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def run(
    command: list[str],
    *,
    expected: int = 0,
    cwd: Path = ROOT,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
    )
    if result.returncode != expected:
        raise ValidationFailure(
            f"command returned {result.returncode}, expected {expected}: "
            f"{' '.join(command)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def payload_markdown_files() -> list[Path]:
    return sorted(PAYLOAD.rglob("*.md"))


def validate_payload_boundary() -> None:
    require(PAYLOAD_MARKER.is_file(), "payload marker is missing")
    require((PAYLOAD / "AGENTS.md").is_file(), "payload AGENTS.md is missing")
    require((PAYLOAD / "CLAUDE.md").is_file(), "payload CLAUDE.md is missing")
    require((PAYLOAD / "INIT.md").is_file(), "payload INIT.md is missing")

    for directory in REQUIRED_STATE_DIRECTORIES:
        require((PAYLOAD / directory).is_dir(), f"payload directory is missing: {directory}")

    for path in payload_markdown_files():
        text = path.read_text()
        for forbidden in FORBIDDEN_PAYLOAD_TEXT:
            require(
                forbidden not in text,
                f"repository-maintenance text leaked into payload: {path}: {forbidden}",
            )

    state_roots = {
        PAYLOAD / "zettelkasten/06-requirements/backlog",
        PAYLOAD / "zettelkasten/06-requirements/in-progress",
        PAYLOAD / "zettelkasten/06-requirements/done",
        PAYLOAD / "zettelkasten/07-review/pending",
        PAYLOAD / "zettelkasten/07-review/in-review",
        PAYLOAD / "zettelkasten/07-review/done",
        PAYLOAD / "zettelkasten/08-technical-designs/pending",
        PAYLOAD / "zettelkasten/08-technical-designs/approved",
        PAYLOAD / "zettelkasten/08-technical-designs/implemented",
    }
    for state_root in state_roots:
        unexpected = [
            path
            for path in state_root.iterdir()
            if path.name != ".gitkeep"
        ]
        require(not unexpected, f"maintenance artifacts found in payload: {unexpected}")


def replace_placeholders(target: Path) -> None:
    vault = target / "zettelkasten"
    for path in vault.rglob("*.md"):
        text = path.read_text()
        for placeholder, value in PLACEHOLDER_VALUES.items():
            text = text.replace(placeholder, value)
        text = re.sub(
            r"<!-- UMBRELLA-ONLY.*?<!-- /UMBRELLA-ONLY -->\n?",
            "",
            text,
            flags=re.DOTALL,
        )
        path.write_text(text)

    source_index = vault / "{{PROJECT_NAME}}.md"
    target_index = vault / "ExampleSaaS.md"
    require(source_index.is_file(), "project index placeholder file is missing")
    source_index.rename(target_index)
    shutil.rmtree(vault / "04-cross-cutting")
    (target / PAYLOAD_MARKER.name).unlink()
    (target / "INIT.md").unlink()

    for path in vault.rglob("*.md"):
        text = path.read_text()
        require(
            not re.search(r"\{\{[A-Z_]+\}\}", text),
            f"placeholder remains after sample initialization: {path}",
        )
        require(
            "UMBRELLA-ONLY" not in text,
            f"umbrella marker remains after sample initialization: {path}",
        )


def create_first_workflow_artifacts(target: Path) -> None:
    vault = target / "zettelkasten"
    requirement_id = "REQ-20260618190000-sample-change"
    technical_design_id = "TECH-20260618190100-sample-change"
    review_id = "REVIEW-20260618190200-sample-change"

    requirement = (
        vault
        / "06-requirements/in-progress"
        / f"{requirement_id}.md"
    )
    technical_design = (
        vault
        / "08-technical-designs/approved"
        / f"{technical_design_id}.md"
    )
    review = vault / "07-review/pending" / f"{review_id}.md"

    shutil.copy2(
        vault / "00-governance/templates/requirement.md",
        requirement,
    )
    shutil.copy2(
        vault / "00-governance/templates/technical-design.md",
        technical_design,
    )
    shutil.copy2(
        vault / "00-governance/templates/review.md",
        review,
    )

    common_replacements = {
        "REQ-YYYYMMDDHHMMSS-short-name": requirement_id,
        "TECH-YYYYMMDDHHMMSS-short-name": technical_design_id,
        "REVIEW-YYYYMMDDHHMMSS-short-name": review_id,
    }
    artifacts = (
        (requirement, {"status: backlog": "status: in-progress"}),
        (technical_design, {"status: pending": "status: approved"}),
        (review, {}),
    )
    for path, state_replacements in artifacts:
        text = path.read_text()
        for old, new in (common_replacements | state_replacements).items():
            text = text.replace(old, new)
        path.write_text(text)
        require(path.is_file(), f"failed to create workflow artifact: {path}")

    require("status: in-progress" in requirement.read_text(), "REQ state is incorrect")
    require("status: approved" in technical_design.read_text(), "TECH state is incorrect")
    require("status: pending" in review.read_text(), "REVIEW state is incorrect")


def wiki_index(vault: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for path in vault.rglob("*.md"):
        relative = path.relative_to(vault).with_suffix("").as_posix()
        index[relative] = path
        index.setdefault(path.stem, path)
    return index


def validate_wiki_links(vault: Path) -> None:
    index = wiki_index(vault)
    broken: list[str] = []
    for path in vault.rglob("*.md"):
        for target in re.findall(r"(?<!!)\[\[([^\]|#]+)", path.read_text()):
            if any(marker in target for marker in ("YYYY", "<", "{{")):
                continue
            if target not in index:
                broken.append(f"{path.relative_to(vault)} -> [[{target}]]")
    require(not broken, "broken wiki links:\n" + "\n".join(broken))


def validate_bootstrap_and_lifecycle() -> None:
    with tempfile.TemporaryDirectory(prefix="ai-workflow-distribution-") as temp_dir:
        target = Path(temp_dir) / "target"

        dry_run = run(
            [
                sys.executable,
                str(BOOTSTRAP),
                "--source",
                str(ROOT),
                "--target",
                str(target),
                "--dry-run",
            ]
        )
        require("Would copy:" in dry_run.stdout, "dry-run summary is missing")
        require(not target.exists(), "dry-run modified the target")

        run(
            [
                sys.executable,
                str(BOOTSTRAP),
                "--source",
                str(ROOT),
                "--target",
                str(target),
            ]
        )
        identical = run(
            [
                sys.executable,
                str(BOOTSTRAP),
                "--source",
                str(ROOT),
                "--target",
                str(target),
            ]
        )
        require("Conflicts left untouched: 0" in identical.stdout, "identical rerun conflicted")

        local_rules = "# Local project rules\n"
        (target / "AGENTS.md").write_text(local_rules)
        conflict = run(
            [
                sys.executable,
                str(BOOTSTRAP),
                "--source",
                str(ROOT),
                "--target",
                str(target),
            ],
            expected=2,
        )
        require("conflict: AGENTS.md" in conflict.stdout, "AGENTS.md conflict was not reported")
        require(
            (target / "AGENTS.md").read_text() == local_rules,
            "bootstrap overwrote a differing AGENTS.md",
        )
        shutil.copy2(PAYLOAD / "AGENTS.md", target / "AGENTS.md")

        require(
            (target / PAYLOAD_MARKER.name).is_file(),
            "bootstrap omitted the payload marker",
        )
        for directory in REQUIRED_STATE_DIRECTORIES:
            require((target / directory).is_dir(), f"bootstrap omitted: {directory}")

        run(
            [
                sys.executable,
                str(BOOTSTRAP),
                "--target",
                str(target),
                "--inspect",
            ]
        )

        replace_placeholders(target)
        create_first_workflow_artifacts(target)
        validate_wiki_links(target / "zettelkasten")

        run(
            [
                sys.executable,
                str(BOOTSTRAP),
                "--target",
                str(target),
                "--inspect",
            ]
        )


def validate_manual_copy_path() -> None:
    with tempfile.TemporaryDirectory(prefix="ai-workflow-manual-copy-") as temp_dir:
        target = Path(temp_dir) / "target"
        shutil.copytree(PAYLOAD, target)
        require((target / "INIT.md").is_file(), "manual payload copy omitted INIT.md")
        for directory in REQUIRED_STATE_DIRECTORIES:
            require(
                (target / directory).is_dir(),
                f"manual payload copy omitted: {directory}",
            )


def validate_symlink_boundary() -> None:
    with tempfile.TemporaryDirectory(prefix="ai-workflow-symlink-") as temp_dir:
        base = Path(temp_dir)
        target = base / "target"
        outside = base / "outside"
        target.mkdir()
        outside.mkdir()
        (target / "zettelkasten").symlink_to(outside, target_is_directory=True)

        result = run(
            [
                sys.executable,
                str(BOOTSTRAP),
                "--source",
                str(ROOT),
                "--target",
                str(target),
            ],
            expected=2,
        )
        require(
            "conflict: zettelkasten/AI.md" in result.stdout,
            "symlink boundary was not reported as a conflict",
        )
        require(not any(outside.iterdir()), "bootstrap wrote through a target symlink")


def validate_remote_clone_path() -> None:
    require(shutil.which("git") is not None, "git is required for remote bootstrap validation")
    with tempfile.TemporaryDirectory(prefix="ai-workflow-remote-source-") as temp_dir:
        base = Path(temp_dir)
        source = base / "source"
        target = base / "target"
        source.mkdir()
        shutil.copytree(PAYLOAD, source / "template")

        run(["git", "init", "--initial-branch", "main"], cwd=source)
        run(["git", "add", "template"], cwd=source)
        run(
            [
                "git",
                "-c",
                "user.name=Distribution Validator",
                "-c",
                "user.email=validator@example.invalid",
                "commit",
                "-m",
                "test: add template payload",
            ],
            cwd=source,
        )
        run(
            [
                sys.executable,
                str(BOOTSTRAP),
                "--repo-url",
                str(source),
                "--ref",
                "main",
                "--target",
                str(target),
            ]
        )
        require(
            (target / PAYLOAD_MARKER.name).is_file(),
            "remote bootstrap omitted the payload marker",
        )
        for directory in REQUIRED_STATE_DIRECTORIES:
            require(
                (target / directory).is_dir(),
                f"remote bootstrap omitted: {directory}",
            )


def validate_root_project_state() -> None:
    require(not (ROOT / "INIT.md").exists(), "root project still has INIT.md")
    require(
        (ROOT / "zettelkasten/AI_Collaboration_Workflow_Template.md").is_file(),
        "root project index is not initialized",
    )
    for path in (ROOT / "zettelkasten").rglob("*.md"):
        if "00-governance/templates" in path.as_posix():
            continue
        require(
            not re.search(r"\{\{[A-Z_]+\}\}", path.read_text()),
            f"root project placeholder remains: {path}",
        )


def main() -> int:
    try:
        validate_payload_boundary()
        validate_root_project_state()
        validate_manual_copy_path()
        validate_bootstrap_and_lifecycle()
        validate_symlink_boundary()
        validate_remote_clone_path()
    except ValidationFailure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("PASS: template payload and distribution lifecycle are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
