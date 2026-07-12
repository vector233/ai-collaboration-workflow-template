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

REQUIRED_PAYLOAD_DIRECTORIES = REQUIRED_STATE_DIRECTORIES + (
    Path("scripts"),
    Path("zettelkasten/09-implementation-plans"),
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
    require(
        (PAYLOAD / "scripts/workflow_doctor.py").is_file(),
        "payload workflow doctor is missing",
    )
    claude_adapter = (PAYLOAD / "CLAUDE.md").read_text()
    require(
        claude_adapter.lstrip().startswith("@AGENTS.md"),
        "payload CLAUDE.md does not import AGENTS.md",
    )
    agents_text = (PAYLOAD / "AGENTS.md").read_text()
    require(
        "## Cross-Agent Collaboration Contract" in agents_text,
        "payload AGENTS.md is missing the cross-agent contract",
    )
    require(
        "## Optional External Process Skills" in agents_text,
        "payload AGENTS.md is missing optional external Skill rules",
    )
    require(
        "External process skills, plugins, and agent frameworks are optional"
        in agents_text,
        "payload AGENTS.md does not keep external Skills optional",
    )
    require(
        "Rule Promotion Check" in agents_text,
        "payload AGENTS.md is missing rule promotion guidance",
    )
    ai_entry = (PAYLOAD / "zettelkasten/AI.md").read_text()
    require(
        "## Cross-Agent Entry Points" in ai_entry,
        "payload AI.md is missing cross-agent entry points",
    )
    require(
        (PAYLOAD / "zettelkasten/CURRENT.md").is_file(),
        "payload CURRENT.md is missing",
    )
    require(
        "[[CURRENT]]" in ai_entry,
        "payload AI.md does not point to CURRENT.md",
    )
    interoperability = (
        PAYLOAD
        / "zettelkasten/00-governance/external-skill-interoperability.md"
    )
    require(
        interoperability.is_file(),
        "payload external Skill interoperability note is missing",
    )
    interoperability_text = interoperability.read_text()
    require(
        "## No External Skill Installed" in interoperability_text,
        "external Skill interoperability does not define the no-plugin path",
    )
    require(
        "No external command, plugin, directory, or document is required."
        in interoperability_text,
        "external Skill interoperability introduces an implicit dependency",
    )
    for expected_mapping in (
        "Treat the REQ plus selected technical-readiness content as the requested spec output",
        "do not create `docs/superpowers/plans/`",
        "The REQ's delivery-path decision defines implementation readiness",
    ):
        require(
            expected_mapping in interoperability_text,
            f"external Skill mapping is incomplete: {expected_mapping}",
        )
    require(
        not (PAYLOAD / "docs/superpowers").exists(),
        "tool-specific Superpowers workflow tree leaked into payload",
    )
    review_template = (
        PAYLOAD / "zettelkasten/00-governance/templates/review.md"
    ).read_text()
    require(
        "## Resume Context" in review_template,
        "payload review template is missing resume context",
    )
    require(
        "## Rule Promotion Check" in review_template,
        "payload review template is missing the Rule Promotion Check",
    )
    workflow_text = (
        PAYLOAD / "zettelkasten/00-governance/ai-workflow.md"
    ).read_text()
    require(
        "## Rule Promotion Check" in workflow_text,
        "payload workflow is missing the Rule Promotion Check",
    )
    require(
        "## Delivery Paths" in workflow_text and "Task weight" in workflow_text,
        "payload workflow is missing task-weight guidance",
    )
    require(
        "Use this destination matrix to avoid bloating `AGENTS.md`" in workflow_text,
        "payload workflow is missing the rule-promotion destination matrix",
    )
    gotchas_text = (
        PAYLOAD / "zettelkasten/00-governance/gotchas.md"
    ).read_text()
    require(
        "**Prevention rule**" in gotchas_text,
        "payload gotchas template is missing prevention-rule guidance",
    )
    doctor_text = (PAYLOAD / "scripts/workflow_doctor.py").read_text()
    require(
        "Rule Promotion Check" in doctor_text,
        "payload workflow doctor does not check rule promotion state",
    )
    require(
        (
            PAYLOAD
            / "zettelkasten/00-governance/templates/implementation-plan.md"
        ).is_file(),
        "payload implementation plan template is missing",
    )
    require(
        (PAYLOAD / "zettelkasten/09-implementation-plans/README.md").is_file(),
        "payload implementation plan workflow is missing",
    )

    for directory in REQUIRED_PAYLOAD_DIRECTORIES:
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


def create_full_workflow_artifacts(target: Path) -> None:
    vault = target / "zettelkasten"
    requirement_id = "REQ-20260618190000-sample-change"
    technical_design_id = "TECH-20260618190100-sample-change"
    plan_id = "PLAN-20260618190200-sample-change"
    review_id = "REVIEW-20260618190300-sample-change"
    closed_review_id = "REVIEW-20260618190400-sample-change-closed"

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
    plan = vault / "09-implementation-plans" / f"{plan_id}.md"
    review = vault / "07-review/pending" / f"{review_id}.md"
    closed_review = vault / "07-review/done" / f"{closed_review_id}.md"

    shutil.copy2(
        vault / "00-governance/templates/requirement.md",
        requirement,
    )
    shutil.copy2(
        vault / "00-governance/templates/technical-design.md",
        technical_design,
    )
    shutil.copy2(
        vault / "00-governance/templates/implementation-plan.md",
        plan,
    )
    shutil.copy2(
        vault / "00-governance/templates/review.md",
        review,
    )
    shutil.copy2(
        vault / "00-governance/templates/review.md",
        closed_review,
    )

    common_replacements = {
        "REQ-YYYYMMDDHHMMSS-short-name": requirement_id,
        "TECH-YYYYMMDDHHMMSS-short-name": technical_design_id,
        "PLAN-YYYYMMDDHHMMSS-short-name": plan_id,
        "REVIEW-YYYYMMDDHHMMSS-short-name": review_id,
    }
    artifacts = (
        (
            requirement,
            {
                "status: backlog": "status: in-progress",
                "- Standalone TECH: required / not required": "- Standalone TECH: required",
                "- Standalone PLAN: required / not required": "- Standalone PLAN: required",
            },
        ),
        (technical_design, {"status: pending": "status: approved"}),
        (
            plan,
            {
                "status: draft": "status: ready",
                "related_technical_design:\n": (
                    "related_technical_design:\n"
                    f'  - "[[08-technical-designs/approved/{technical_design_id}]]"\n'
                ),
            },
        ),
        (review, {}),
        (
            closed_review,
            {
                "status: pending": "status: done",
                review_id: closed_review_id,
                "- Promote to durable rule: yes / no": "- Promote to durable rule: no",
                "- Reason:": "- Reason: no recurring lesson in this sample closure",
                "- Rule or summary written:": "- Rule or summary written: not applicable",
            },
        ),
    )
    for path, state_replacements in artifacts:
        text = path.read_text()
        for old, new in (common_replacements | state_replacements).items():
            text = text.replace(old, new)
        path.write_text(text)
        require(path.is_file(), f"failed to create workflow artifact: {path}")

    require("status: in-progress" in requirement.read_text(), "REQ state is incorrect")
    require("status: approved" in technical_design.read_text(), "TECH state is incorrect")
    require("status: ready" in plan.read_text(), "PLAN state is incorrect")
    require("status: pending" in review.read_text(), "REVIEW state is incorrect")
    require("status: done" in closed_review.read_text(), "closed REVIEW state is incorrect")


def create_bounded_bug_artifacts(target: Path) -> None:
    vault = target / "zettelkasten"
    requirement_id = "REQ-20260618191000-bounded-bug"
    review_id = "REVIEW-20260618191100-bounded-bug"
    requirement = (
        vault
        / "06-requirements/in-progress"
        / f"{requirement_id}.md"
    )
    review = vault / "07-review/pending" / f"{review_id}.md"

    shutil.copy2(
        vault / "00-governance/templates/requirement.md",
        requirement,
    )
    shutil.copy2(
        vault / "00-governance/templates/review.md",
        review,
    )

    replacements = {
        "REQ-YYYYMMDDHHMMSS-short-name": requirement_id,
        "REVIEW-YYYYMMDDHHMMSS-short-name": review_id,
        "status: backlog": "status: in-progress",
        "- Task weight: bounded / standard / complex / high-risk": "- Task weight: bounded",
        "- Tiny waiver used before this REQ: yes / no": "- Tiny waiver used before this REQ: no",
        "- Standalone TECH: required / not required": "- Standalone TECH: not required",
        "- TECH decision reason:": "- TECH decision reason: confirmed local cause and bounded behavior",
        "- Standalone PLAN: required / not required": "- Standalone PLAN: not required",
        "- PLAN decision reason:": "- PLAN decision reason: one bounded slice",
        "- Why inline readiness is sufficient:": (
            "- Why inline readiness is sufficient: local low-risk fix"
        ),
        "- Confirmed root cause or technical approach:": (
            "- Confirmed root cause or technical approach: add a focused guard"
        ),
        "- Affected paths and behavior boundaries:": (
            "- Affected paths and behavior boundaries: one module and its tests"
        ),
        "- Focused validation plan:": (
            "- Focused validation plan: affected unit test and regression smoke"
        ),
        "- Slice 1:": "- Slice 1: implement guard, test, and validate",
    }
    for path in (requirement, review):
        text = path.read_text()
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text)

    requirement_text = requirement.read_text()
    require("Task weight: bounded" in requirement_text, "bounded bug task weight is missing")
    require("Standalone TECH: not required" in requirement_text, "bounded bug requires TECH")
    require("Standalone PLAN: not required" in requirement_text, "bounded bug requires PLAN")
    require(
        not any(
            path.name.endswith("-bounded-bug.md")
            for path in (vault / "08-technical-designs").rglob("TECH-*.md")
        ),
        "bounded bug unexpectedly created a TECH",
    )
    require(
        not (vault / "09-implementation-plans/PLAN-20260618191000-bounded-bug.md").exists(),
        "bounded bug unexpectedly created a PLAN",
    )


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
        require(
            (
                target
                / "zettelkasten/00-governance/external-skill-interoperability.md"
            ).is_file(),
            "bootstrap omitted optional external Skill interoperability",
        )
        require(
            not (target / "docs/superpowers").exists(),
            "bootstrap created a Superpowers-specific workflow tree",
        )
        require(
            (target / "scripts/workflow_doctor.py").is_file(),
            "bootstrap omitted the workflow doctor",
        )
        for directory in REQUIRED_PAYLOAD_DIRECTORIES:
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
        clean_doctor = run(
            [
                sys.executable,
                "scripts/workflow_doctor.py",
                "--strict",
            ],
            cwd=target,
        )
        require(
            "PASS: workflow state looks consistent" in clean_doctor.stdout,
            "workflow doctor did not pass on clean initialized target",
        )
        create_bounded_bug_artifacts(target)
        create_full_workflow_artifacts(target)
        validate_wiki_links(target / "zettelkasten")
        active_doctor = run(
            [
                sys.executable,
                "scripts/workflow_doctor.py",
            ],
            cwd=target,
        )
        require(
            "open review blocks the next implementation slice" in active_doctor.stdout,
            "workflow doctor did not report open review routing",
        )

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
        require(
            (target / "scripts/workflow_doctor.py").is_file(),
            "manual payload copy omitted workflow doctor",
        )
        require(
            (
                target
                / "zettelkasten/00-governance/external-skill-interoperability.md"
            ).is_file(),
            "manual payload copy omitted optional external Skill interoperability",
        )
        require(
            not (target / "docs/superpowers").exists(),
            "manual payload copy created a Superpowers-specific workflow tree",
        )
        for directory in REQUIRED_PAYLOAD_DIRECTORIES:
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
        require(
            (target / "scripts/workflow_doctor.py").is_file(),
            "remote bootstrap omitted the workflow doctor",
        )
        for directory in REQUIRED_PAYLOAD_DIRECTORIES:
            require(
                (target / directory).is_dir(),
                f"remote bootstrap omitted: {directory}",
            )


def validate_repository_layout() -> None:
    require(
        not (ROOT / "zettelkasten").exists(),
        "root zettelkasten must not exist; template/ is the canonical payload",
    )
    require(
        (ROOT / "docs/community-publishing.md").is_file(),
        "community publishing runbook is missing",
    )
    require(
        (ROOT / "docs/fresh-agent-resume-evaluation.md").is_file(),
        "fresh-agent resume evaluation is missing",
    )
    require(
        (ROOT / "examples/practical-scenarios/README.md").is_file(),
        "practical scenario examples are missing",
    )


def main() -> int:
    try:
        validate_payload_boundary()
        validate_repository_layout()
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
