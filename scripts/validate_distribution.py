#!/usr/bin/env python3
"""Validate the canonical payload through bootstrap and realistic temporary projects."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "template"
MARKER = PAYLOAD / ".ai-collaboration-workflow-template"
BOOTSTRAP = ROOT / "skills/ai-collaboration-workflow/scripts/bootstrap_template.py"

REQUIRED_FILES = (
    Path("AGENTS.md"),
    Path("CLAUDE.md"),
    Path("INIT.md"),
    Path("scripts/workflow_doctor.py"),
    Path("scripts/task_worktree.py"),
    Path("zettelkasten/AI.md"),
    Path("zettelkasten/00-governance/ai-workflow.md"),
    Path("zettelkasten/00-governance/skill-lifecycle.md"),
    Path("zettelkasten/00-governance/git-collaboration.md"),
    Path("zettelkasten/00-governance/templates/work-item.md"),
    Path("zettelkasten/00-governance/templates/project-skill.md"),
    Path("zettelkasten/06-work/README.md"),
    Path("project-skills/INDEX.md"),
)

REQUIRED_DIRECTORIES = (
    Path("scripts"),
    Path("zettelkasten/06-work"),
    Path("project-skills"),
)

LEGACY_PATHS = (
    Path("zettelkasten/CURRENT.md"),
    Path("zettelkasten/06-requirements"),
    Path("zettelkasten/07-review"),
    Path("zettelkasten/08-technical-designs"),
    Path("zettelkasten/09-implementation-plans"),
)

FORBIDDEN_PAYLOAD_TEXT = (
    "vector233",
    "community-publishing",
    "REQ-20260618170000-shareable-workflow-skill",
)

PLACEHOLDERS = {
    "{{PROJECT_NAME}}": "ExampleSaaS",
    "{{PROJECT_NAME_SAFE}}": "ExampleSaaS",
    "{{PROJECT_DESCRIPTION}}": "A sample project used to validate distribution",
    "{{TECH_STACK}}": "Python, SQLite, HTML",
    "{{REPO_TYPE}}": "single",
    "{{SUB_PROJECTS}}": "Not applicable.",
    "{{DOMAINS}}": "| Environment | Domain / port |\n|---|---|\n| Local | localhost:8000 |",
    "{{REPOS}}": "- example/example-saas",
}


class ValidationFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def run(command: list[str], *, cwd: Path = ROOT, expected: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if result.returncode != expected:
        raise ValidationFailure(
            f"command returned {result.returncode}, expected {expected}: {' '.join(command)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def validate_payload() -> None:
    require(MARKER.is_file(), "payload marker is missing")
    require(MARKER.read_text().strip() == "canonical-payload-v2", "payload marker version is incorrect")
    for path in REQUIRED_FILES:
        require((PAYLOAD / path).is_file(), f"payload file is missing: {path}")
    for path in REQUIRED_DIRECTORIES:
        require((PAYLOAD / path).is_dir(), f"payload directory is missing: {path}")
    for path in LEGACY_PATHS:
        require(not (PAYLOAD / path).exists(), f"legacy moving-state path remains: {path}")

    agents = (PAYLOAD / "AGENTS.md").read_text()
    require("## Workflow Routing" in agents, "AGENTS.md is missing workflow routing")
    require("## Project Skills And Experience" in agents, "AGENTS.md is missing project-Skill routing")
    require("## Git Isolation And Commits" in agents, "AGENTS.md is missing Git isolation")
    require("Each agent context" in agents, "AGENTS.md is missing context commit policy")
    require((PAYLOAD / "CLAUDE.md").read_text().lstrip().startswith("@AGENTS.md"), "CLAUDE.md is not an adapter")

    workflow = (PAYLOAD / "zettelkasten/00-governance/ai-workflow.md").read_text()
    for expected in ("## Route Decision", "Direct", "Tracked", "Governed", "## Stable Work Artifacts", "## Experience Promotion Check"):
        require(expected in workflow, f"workflow is missing {expected}")

    skill_template = (PAYLOAD / "zettelkasten/00-governance/templates/project-skill.md").read_text()
    for section in ("## Use", "## Do Not Use", "## Procedure", "## Validation", "## Recovery", "## Provenance"):
        require(section in skill_template, f"project Skill template is missing {section}")

    doctor = (PAYLOAD / "scripts/workflow_doctor.py").read_text()
    require("project-skills" in doctor and "ACTIVE_WORK_STATES" in doctor, "doctor does not validate the new model")

    for path in PAYLOAD.rglob("*.md"):
        text = path.read_text()
        for forbidden in FORBIDDEN_PAYLOAD_TEXT:
            require(forbidden not in text, f"maintenance text leaked into payload: {path}: {forbidden}")


def initialize_target(target: Path) -> None:
    vault = target / "zettelkasten"
    for path in vault.rglob("*.md"):
        text = path.read_text()
        for placeholder, value in PLACEHOLDERS.items():
            text = text.replace(placeholder, value)
        text = re.sub(r"<!-- UMBRELLA-ONLY.*?<!-- /UMBRELLA-ONLY -->\n?", "", text, flags=re.DOTALL)
        path.write_text(text)

    source_index = vault / "{{PROJECT_NAME}}.md"
    require(source_index.is_file(), "project index placeholder file is missing")
    source_index.rename(vault / "ExampleSaaS.md")
    shutil.rmtree(vault / "04-cross-cutting")
    (target / MARKER.name).unlink()
    (target / "INIT.md").unlink()

    for path in vault.rglob("*.md"):
        text = path.read_text()
        require(not re.search(r"\{\{[A-Z_]+\}\}", text), f"placeholder remains: {path}")
        require("UMBRELLA-ONLY" not in text, f"umbrella marker remains: {path}")


def copy_artifact(target: Path, template: str, output: str, replacements: dict[str, str]) -> Path:
    source = target / f"zettelkasten/00-governance/templates/{template}"
    destination = target / f"zettelkasten/06-work/{output}"
    shutil.copy2(source, destination)
    text = destination.read_text()
    for old, new in replacements.items():
        text = text.replace(old, new)
    destination.write_text(text)
    return destination


def create_workflow_state(target: Path) -> None:
    work_id = "WORK-20260712120000-sample-change"
    work = copy_artifact(
        target,
        "work-item.md",
        f"{work_id}.md",
        {
            "WORK-YYYYMMDDHHMMSS-short-name": work_id,
            "status: backlog": "status: active",
            "route: tracked": "route: governed",
            "branch: task/work-id-short-name": f"branch: task/{work_id.lower()}",
            "next_action: clarify acceptance criteria": "next_action: implement slice S1",
            "- Selected route: tracked / governed": "- Selected route: governed",
            "- Separate TECH required: no / yes, because": "- Separate TECH required: yes, because schema compatibility",
            "- Separate PLAN required: no / yes, because": "- Separate PLAN required: yes, because dependent slices",
            "- Separate REVIEW required: no / yes, because": "- Separate REVIEW required: yes, because independent approval",
        },
    )
    require("status: active" in work.read_text(), "active WORK was not created")

    copy_artifact(
        target,
        "technical-design.md",
        "TECH-20260712120100-sample-change.md",
        {
            "TECH-YYYYMMDDHHMMSS-short-name": "TECH-20260712120100-sample-change",
            "WORK-YYYYMMDDHHMMSS-short-name": work_id,
            "status: pending": "status: approved",
        },
    )
    copy_artifact(
        target,
        "implementation-plan.md",
        "PLAN-20260712120200-sample-change.md",
        {
            "PLAN-YYYYMMDDHHMMSS-short-name": "PLAN-20260712120200-sample-change",
            "WORK-YYYYMMDDHHMMSS-short-name": work_id,
            "status: draft": "status: ready",
        },
    )
    copy_artifact(
        target,
        "review.md",
        "REVIEW-20260712120300-sample-change.md",
        {
            "REVIEW-YYYYMMDDHHMMSS-short-name": "REVIEW-20260712120300-sample-change",
            "WORK-YYYYMMDDHHMMSS-short-name": work_id,
        },
    )

    done_id = "WORK-20260712121000-closed-change"
    copy_artifact(
        target,
        "work-item.md",
        f"{done_id}.md",
        {
            "WORK-YYYYMMDDHHMMSS-short-name": done_id,
            "status: backlog": "status: done",
            "branch: task/work-id-short-name": f"branch: task/{done_id.lower()}",
            "next_action: clarify acceptance criteria": "next_action: none",
            "|  | rule / gotcha / fact / runbook / project-skill | pending |  |  |": "| No reusable lesson | fact | not-promoted | work item | one-off sample |",
            "- Acceptance complete: yes / no": "- Acceptance complete: yes",
            "- Required gates closed: yes / no": "- Required gates closed: yes",
            "- Experience Promotion complete: yes / no": "- Experience Promotion complete: yes",
            "- Durable writeback complete: yes / no": "- Durable writeback complete: yes",
        },
    )


def create_project_skill(target: Path) -> None:
    skill_name = "reset-sample-sandbox"
    directory = target / "project-skills" / skill_name
    directory.mkdir()
    shutil.copy2(target / "zettelkasten/00-governance/templates/project-skill.md", directory / "SKILL.md")
    skill_file = directory / "SKILL.md"
    text = skill_file.read_text().replace("project-procedure-name", skill_name).replace(
        "Describe what this procedure does and the concrete repository situations that should trigger it.",
        "Reset the sample sandbox when integration tests reuse stale provider state or resend flows return an old token.",
    )
    skill_file.write_text(text)
    index = target / "project-skills/INDEX.md"
    index.write_text(
        index.read_text().replace(
            "| None |  |  |  |  |",
            f"| {skill_name} | stale provider state or old resend token | local unit tests | active | 2026-07-12 |",
        )
    )


def wiki_index(vault: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for path in vault.rglob("*.md"):
        index[path.relative_to(vault).with_suffix("").as_posix()] = path
        index.setdefault(path.stem, path)
    return index


def validate_wiki_links(vault: Path) -> None:
    index = wiki_index(vault)
    broken: list[str] = []
    for path in vault.rglob("*.md"):
        for raw in re.findall(r"(?<!!)\[\[([^\]|#]+)", path.read_text()):
            target = raw.strip().removesuffix(".md")
            if any(marker in target for marker in ("YYYY", "<", "{{")):
                continue
            if target not in index:
                broken.append(f"{path.relative_to(vault)} -> [[{target}]]")
    require(not broken, "broken wiki links:\n" + "\n".join(broken))


def validate_worktree_helper(target: Path) -> None:
    run(["git", "init", "--initial-branch", "main"], cwd=target)
    run(["git", "add", "."], cwd=target)
    run(
        ["git", "-c", "user.name=Validator", "-c", "user.email=validator@example.invalid", "commit", "-m", "test: initialize target"],
        cwd=target,
    )
    destination = target.parent / "task-worktree"
    dry_run = run(
        [sys.executable, "scripts/task_worktree.py", "create", "WORK-20260712122000-helper", "--slug", "helper", "--path", str(destination), "--dry-run"],
        cwd=target,
    )
    require("Dry run:" in dry_run.stdout, "worktree helper dry-run is missing")
    run(
        [sys.executable, "scripts/task_worktree.py", "create", "WORK-20260712122000-helper", "--slug", "helper", "--path", str(destination)],
        cwd=target,
    )
    require((destination / ".git").is_file(), "task worktree was not created")


def validate_bootstrap_lifecycle() -> None:
    with tempfile.TemporaryDirectory(prefix="ai-workflow-distribution-") as temp_dir:
        target = Path(temp_dir) / "target"
        dry_run = run([sys.executable, str(BOOTSTRAP), "--source", str(ROOT), "--target", str(target), "--dry-run"])
        require("Would copy:" in dry_run.stdout and not target.exists(), "bootstrap dry-run changed the target")
        run([sys.executable, str(BOOTSTRAP), "--source", str(ROOT), "--target", str(target)])
        identical = run([sys.executable, str(BOOTSTRAP), "--source", str(ROOT), "--target", str(target)])
        require("Conflicts left untouched: 0" in identical.stdout, "identical bootstrap rerun conflicted")

        local_rules = "# Local rules\n"
        (target / "AGENTS.md").write_text(local_rules)
        conflict = run([sys.executable, str(BOOTSTRAP), "--source", str(ROOT), "--target", str(target)], expected=2)
        require("conflict: AGENTS.md" in conflict.stdout, "bootstrap did not report AGENTS conflict")
        require((target / "AGENTS.md").read_text() == local_rules, "bootstrap overwrote local rules")
        shutil.copy2(PAYLOAD / "AGENTS.md", target / "AGENTS.md")

        run([sys.executable, str(BOOTSTRAP), "--target", str(target), "--inspect"])
        initialize_target(target)
        clean = run([sys.executable, "scripts/workflow_doctor.py", "--strict"], cwd=target)
        require("PASS: workflow state looks consistent" in clean.stdout, "doctor failed on clean target")

        create_workflow_state(target)
        create_project_skill(target)
        validate_wiki_links(target / "zettelkasten")
        active = run([sys.executable, "scripts/workflow_doctor.py", "--strict"], cwd=target)
        require("active work:" in active.stdout, "doctor did not report active WORK")
        status = run([sys.executable, "scripts/workflow_doctor.py", "--status"], cwd=target)
        require("WORK-20260712120000-sample-change.md" in status.stdout, "status did not route active WORK")
        validate_worktree_helper(target)


def validate_manual_copy() -> None:
    with tempfile.TemporaryDirectory(prefix="ai-workflow-copy-") as temp_dir:
        target = Path(temp_dir) / "target"
        shutil.copytree(PAYLOAD, target)
        for path in REQUIRED_FILES:
            require((target / path).is_file(), f"manual copy omitted {path}")
        for path in REQUIRED_DIRECTORIES:
            require((target / path).is_dir(), f"manual copy omitted {path}")


def validate_symlink_boundary() -> None:
    with tempfile.TemporaryDirectory(prefix="ai-workflow-symlink-") as temp_dir:
        base = Path(temp_dir)
        target = base / "target"
        outside = base / "outside"
        target.mkdir()
        outside.mkdir()
        (target / "zettelkasten").symlink_to(outside, target_is_directory=True)
        result = run([sys.executable, str(BOOTSTRAP), "--source", str(ROOT), "--target", str(target)], expected=2)
        require("conflict: zettelkasten/AI.md" in result.stdout, "symlink conflict was not reported")
        require(not any(outside.iterdir()), "bootstrap wrote through a symlink")


def validate_remote_source() -> None:
    with tempfile.TemporaryDirectory(prefix="ai-workflow-remote-") as temp_dir:
        base = Path(temp_dir)
        source = base / "source"
        target = base / "target"
        source.mkdir()
        shutil.copytree(PAYLOAD, source / "template")
        run(["git", "init", "--initial-branch", "main"], cwd=source)
        run(["git", "add", "template"], cwd=source)
        run(["git", "-c", "user.name=Validator", "-c", "user.email=validator@example.invalid", "commit", "-m", "test: add payload"], cwd=source)
        run([sys.executable, str(BOOTSTRAP), "--repo-url", str(source), "--ref", "main", "--target", str(target)])
        require((target / "project-skills/INDEX.md").is_file(), "remote bootstrap omitted project Skills")


def validate_repository_layout() -> None:
    require(not (ROOT / "zettelkasten").exists(), "root zettelkasten must not exist")
    require((ROOT / "docs/fresh-agent-resume-evaluation.md").is_file(), "resume evaluation is missing")
    require((ROOT / "examples/practical-scenarios/README.md").is_file(), "practical scenarios are missing")
    require((ROOT / "skills/ai-collaboration-workflow/references/routing.md").is_file(), "Skill routing reference is missing")


def main() -> int:
    try:
        validate_payload()
        validate_repository_layout()
        validate_manual_copy()
        validate_bootstrap_lifecycle()
        validate_symlink_boundary()
        validate_remote_source()
    except ValidationFailure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("PASS: template payload and distribution lifecycle are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
