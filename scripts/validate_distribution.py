#!/usr/bin/env python3
"""Validate the canonical payload through bootstrap and realistic temporary projects."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "template"
ADAPTERS = ROOT / "adapters"
RELEASE_VERSION = "v4.2.0-rc.1"
CANONICAL_REPO_URL = "https://github.com/vector233/repo-continuity"
SKILL_ID = "repo-continuity"
SKILL_ROOT = ROOT / "skills" / SKILL_ID
MARKER_NAME = ".repo-continuity-template"
LEGACY_MARKER_NAME = ".ai-collaboration-workflow-template"
MARKER = PAYLOAD / MARKER_NAME
BOOTSTRAP = SKILL_ROOT / "scripts/bootstrap_template.py"
WORKFLOW_DOCTOR = SKILL_ROOT / "scripts/workflow_doctor.py"
WORKFLOW_TASK = SKILL_ROOT / "scripts/workflow_task.py"
TASK_WORKTREE = SKILL_ROOT / "scripts/task_worktree.py"
BEHAVIOR_EVALUATOR = ROOT / "scripts/evaluate_workflow_behavior.py"

REQUIRED_FILES = (
    Path("AGENTS.md"),
    Path("CLAUDE.md"),
    Path("INIT.md"),
    Path("zettelkasten/AI.md"),
    Path("zettelkasten/workflow.md"),
    Path("zettelkasten/skill-lifecycle.md"),
    Path("zettelkasten/git-collaboration.md"),
    Path("zettelkasten/templates/work-item.md"),
    Path("zettelkasten/templates/project-skill.md"),
    Path("zettelkasten/templates/workflow-observations.md"),
    Path("zettelkasten/work/README.md"),
    Path("project-skills/INDEX.md"),
)

MODEL_ROUTING_ADAPTER_FILES = {
    "codex": (
        Path(".codex/config.toml"),
        Path(".codex/agents/explorer.toml"),
        Path(".codex/agents/implementer.toml"),
        Path(".codex/agents/reviewer.toml"),
        Path(".codex/agents/architect.toml"),
    ),
    "claude": (
        Path(".claude/agents/explorer.md"),
        Path(".claude/agents/implementer.md"),
        Path(".claude/agents/reviewer.md"),
        Path(".claude/agents/architect.md"),
    ),
}

REQUIRED_DIRECTORIES = (
    Path("zettelkasten/work"),
    Path("project-skills"),
)

FORBIDDEN_PAYLOAD_TEXT = (
    "vector233",
    "community-publishing",
    "REQ-",
    "TECH-",
    "PLAN-",
    "REVIEW-",
)

PLACEHOLDERS = {
    "{{PROJECT_NAME}}": "ExampleSaaS",
    "{{PROJECT_DESCRIPTION}}": "A sample project used to validate distribution",
    "{{TECH_STACK}}": "Python, SQLite, HTML",
    "{{DOMAINS}}": "| Environment | Domain / port |\n|---|---|\n| Local | localhost:8000 |",
    "{{REPOS}}": "- example/example-saas",
}


class ValidationFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def run(
    command: list[str],
    *,
    cwd: Path = ROOT,
    expected: int = 0,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if result.returncode != expected:
        raise ValidationFailure(
            f"command returned {result.returncode}, expected {expected}: {' '.join(command)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def validate_payload() -> None:
    require(MARKER.is_file(), "payload marker is missing")
    require(
        not (PAYLOAD / LEGACY_MARKER_NAME).exists(),
        "legacy marker remains canonical in the payload",
    )
    require(
        MARKER.read_text().strip() == "canonical-payload-v4",
        "payload marker version is incorrect",
    )
    require(
        f"Template baseline: `{RELEASE_VERSION}` (`canonical-payload-v4`)."
        in (PAYLOAD / "zettelkasten/AI.md").read_text(),
        "payload release baseline is incorrect",
    )
    for path in REQUIRED_FILES:
        require((PAYLOAD / path).is_file(), f"payload file is missing: {path}")
    for path in REQUIRED_DIRECTORIES:
        require((PAYLOAD / path).is_dir(), f"payload directory is missing: {path}")
    require(
        not (PAYLOAD / ".codex").exists() and not (PAYLOAD / ".claude").exists(),
        "model-routing adapters leaked into the default core payload",
    )
    vault_directories = {
        path.name for path in (PAYLOAD / "zettelkasten").iterdir() if path.is_dir()
    }
    require(
        vault_directories == {"templates", "work"},
        f"unexpected knowledge directories: {sorted(vault_directories)}",
    )
    require(
        not any(re.match(r"^\d\d-", path.name) for path in PAYLOAD.rglob("*")),
        "numbered knowledge layout remains in the payload",
    )
    require(not (PAYLOAD / "scripts").exists(), "optional tooling leaked into the core payload")

    agents = (PAYLOAD / "AGENTS.md").read_text()
    for section in (
        "## Workflow Routing",
        "## Context Preservation",
        "## Specialist Delegation",
        "## Project Skills And Experience",
        "## Workflow Feedback",
        "## Git Isolation And Commits",
    ):
        require(section in agents, f"AGENTS.md is missing {section}")
    require("persistent changes" in agents, "AGENTS.md commit policy permits empty commits")
    require(
        (PAYLOAD / "CLAUDE.md").read_text().lstrip().startswith("@AGENTS.md"),
        "CLAUDE.md is not an adapter",
    )
    require(
        "## Optional Model-Routing Adapter" in (PAYLOAD / "CLAUDE.md").read_text(),
        "CLAUDE.md is missing the Claude Code model-routing adapter",
    )

    workflow = (PAYLOAD / "zettelkasten/workflow.md").read_text()
    for expected in (
        "## Route Decision",
        "Direct",
        "Tracked",
        "Governed",
        "## Stable Work Record",
        "## Context Preservation",
        "## Experience Promotion Check",
        "### Idempotent Writeback",
    ):
        require(expected in workflow, f"workflow is missing {expected}")

    work_template = (PAYLOAD / "zettelkasten/templates/work-item.md").read_text()
    for expected in (
        "fresh agent to resume without prior conversation",
        "The active WORK owns each pending candidate",
        "a repeated promotion should record a no-op",
    ):
        require(expected in work_template, f"WORK template is missing continuity contract: {expected}")

    validation_policy = (PAYLOAD / "zettelkasten/validation-policy.md").read_text()
    for expected in (
        "## Knowledge Recoverability",
        "Structural check",
        "Semantic Fresh-Agent Resume Probe",
        "it is not evidence that a fresh agent recovered the work",
    ):
        require(expected in validation_policy, f"validation policy is missing recovery contract: {expected}")

    skill = (SKILL_ROOT / "SKILL.md").read_text()
    require(
        skill.startswith("---\nname: repo-continuity\n"),
        "companion Skill metadata uses a stale ID",
    )
    for expected in (
        "## Preserve Context",
        "Do not checkpoint every turn",
        "make repeated promotion a no-op rather than a duplicate",
        "a synthetic expected response tests only the evaluator",
    ):
        require(expected in skill, f"companion Skill is missing continuity contract: {expected}")

    skill_template = (
        PAYLOAD / "zettelkasten/templates/project-skill.md"
    ).read_text()
    for section in (
        "## Use",
        "## Do Not Use",
        "## Procedure",
        "## Validation",
        "## Recovery",
        "## Provenance",
    ):
        require(section in skill_template, f"project Skill template is missing {section}")

    doctor = WORKFLOW_DOCTOR.read_text()
    for expected in ("--all-worktrees", "--json", "scope_overlaps", "review_after_days"):
        require(expected in doctor, f"doctor is missing {expected}")

    for path in PAYLOAD.rglob("*.md"):
        text = path.read_text()
        for required_tool in (
            "scripts/workflow_doctor.py",
            "scripts/workflow_task.py",
            "scripts/task_worktree.py",
        ):
            require(
                required_tool not in text,
                f"optional helper is required by core payload documentation: {path}: {required_tool}",
            )
        for forbidden in FORBIDDEN_PAYLOAD_TEXT:
            require(
                forbidden not in text,
                f"maintenance text leaked into payload: {path}: {forbidden}",
            )


def validate_model_routing_adapters() -> None:
    expected_roots = set(MODEL_ROUTING_ADAPTER_FILES)
    require(ADAPTERS.is_dir(), "optional adapters directory is missing")
    actual_roots = {path.name for path in ADAPTERS.iterdir()}
    require(
        actual_roots == expected_roots,
        f"unexpected model-routing adapters: {sorted(actual_roots)}",
    )

    for adapter, expected_files in MODEL_ROUTING_ADAPTER_FILES.items():
        adapter_root = ADAPTERS / adapter
        actual_files = {
            path.relative_to(adapter_root)
            for path in adapter_root.rglob("*")
            if path.is_file()
        }
        require(
            actual_files == set(expected_files),
            f"{adapter} adapter files differ: {sorted(str(path) for path in actual_files)}",
        )

    claude_agent_policies = {
        "explorer": ("model: haiku", "tools: Read, Grep, Glob"),
        "implementer": ("model: sonnet", "tools: Read, Grep, Glob, Edit, Write, Bash"),
        "reviewer": ("model: opus", "tools: Read, Grep, Glob, Bash"),
        "architect": ("model: opus", "tools: Read, Grep, Glob"),
    }
    claude_root = ADAPTERS / "claude"
    require(
        not (claude_root / ".claude/settings.json").exists(),
        "Claude Code adapter must not override the root model",
    )
    for agent, expected_values in claude_agent_policies.items():
        policy = (claude_root / f".claude/agents/{agent}.md").read_text()
        require(
            f"name: {agent}" in policy,
            f"Claude Code {agent} agent has the wrong name",
        )
        for expected in expected_values:
            require(
                expected in policy,
                f"Claude Code {agent} agent is missing {expected}",
            )

    codex_root = ADAPTERS / "codex"
    codex_config = (codex_root / ".codex/config.toml").read_text()
    require(
        not re.search(r"^\s*model(?:_reasoning_effort)?\s*=", codex_config, re.MULTILINE),
        "Codex adapter must not override the root model or reasoning effort",
    )
    for expected in ("max_threads = 3", "max_depth = 1"):
        require(expected in codex_config, f"Codex config is missing {expected}")
    codex_agent_policies = {
        "explorer": ("gpt-5.6-terra", 'sandbox_mode = "read-only"'),
        "implementer": ("gpt-5.6-terra", 'sandbox_mode = "workspace-write"'),
        "reviewer": ("gpt-5.6-sol", 'sandbox_mode = "read-only"'),
        "architect": ("gpt-5.6-sol", 'sandbox_mode = "read-only"'),
    }
    for agent, expected_values in codex_agent_policies.items():
        policy = (codex_root / f".codex/agents/{agent}.toml").read_text()
        require(
            f'name = "{agent}"' in policy,
            f"Codex {agent} agent has the wrong name",
        )
        for expected in expected_values:
            require(
                expected in policy,
                f"Codex {agent} agent is missing {expected}",
            )


def initialize_target(target: Path) -> None:
    vault = target / "zettelkasten"
    today = date.today().isoformat()
    for path in vault.rglob("*.md"):
        text = path.read_text()
        for placeholder, value in PLACEHOLDERS.items():
            text = text.replace(placeholder, value)
        text = text.replace("YYYY-MM-DD", today)
        path.write_text(text)

    (target / MARKER.name).unlink()
    legacy_marker = target / LEGACY_MARKER_NAME
    if legacy_marker.exists():
        legacy_marker.unlink()
    (target / "INIT.md").unlink()

    for path in vault.rglob("*.md"):
        text = path.read_text()
        require(not re.search(r"\{\{[A-Z_]+\}\}", text), f"placeholder remains: {path}")


def initialize_git(target: Path) -> None:
    run(["git", "init", "--initial-branch", "main"], cwd=target)
    run(["git", "add", "."], cwd=target)
    run(
        [
            "git",
            "-c",
            "user.name=Validator",
            "-c",
            "user.email=validator@example.invalid",
            "commit",
            "-m",
            "test: initialize target",
        ],
        cwd=target,
    )


def copy_artifact(
    target: Path,
    template: str,
    output: str,
    replacements: dict[str, str],
) -> Path:
    source = target / f"zettelkasten/templates/{template}"
    destination = target / f"zettelkasten/work/{output}"
    shutil.copy2(source, destination)
    text = destination.read_text()
    for old, new in replacements.items():
        text = text.replace(old, new)
    destination.write_text(text)
    return destination


def validate_tool_free_core(target: Path) -> None:
    require(not (target / "scripts").exists(), "bootstrap installed optional tools into the project")
    require(
        not (target / ".codex").exists() and not (target / ".claude").exists(),
        "core-only bootstrap installed a model-routing adapter",
    )
    work_id = "WORK-20260712115000-manual-core"
    work = copy_artifact(
        target,
        "work-item.md",
        f"{work_id}.md",
        {
            "WORK-YYYYMMDDHHMMSS-short-name": work_id,
            "status: backlog": "status: active",
            "branch: task/work-id-short-name": "branch: task/manual-core",
            "next_action: clarify acceptance criteria": "next_action: define acceptance",
        },
    )
    text = work.read_text()
    require(f"work_id: {work_id}" in text, "manual core path did not create stable WORK state")
    require("## Experience Candidates" in text, "manual core path lost knowledge writeback")
    require(
        "fresh agent to resume without prior conversation" in text,
        "manual core path lost context preservation guidance",
    )
    require(
        "a repeated promotion should record a no-op" in text,
        "manual core path lost idempotent writeback guidance",
    )
    work.unlink()

    observation_template = target / "zettelkasten/templates/workflow-observations.md"
    observation = target / "zettelkasten/workflow-observations.md"
    shutil.copy2(observation_template, observation)
    observation_text = observation.read_text()
    for expected in (
        "Scope: template-wide / vendor-specific / uncertain",
        "Reproducible evidence:",
        "Privacy reviewed: yes / no",
        "Status: candidate / repeated / prepared / reported / dismissed",
    ):
        require(expected in observation_text, f"workflow observation template is missing {expected}")
    observation.unlink()


def create_governed_and_done_state(target: Path) -> None:
    governed_id = "WORK-20260712120000-governed-change"
    governed = copy_artifact(
        target,
        "work-item.md",
        f"{governed_id}.md",
        {
            "WORK-YYYYMMDDHHMMSS-short-name": governed_id,
            "route: tracked": "route: governed",
            "branch: task/work-id-short-name": "branch: task/governed-change",
            "next_action: clarify acceptance criteria": "next_action: approve design",
            "|  |  |  | pending |": (
                "| Migration and rollback approval | release owner | reviewed decision and rollback rehearsal | approved |"
            ),
        },
    )
    require(
        "Migration and rollback approval" in governed.read_text(),
        "governed gate was not recorded in the WORK",
    )

    done_id = "WORK-20260712121000-closed-change"
    copy_artifact(
        target,
        "work-item.md",
        f"{done_id}.md",
        {
            "WORK-YYYYMMDDHHMMSS-short-name": done_id,
            "status: backlog": "status: done",
            "branch: task/work-id-short-name": "branch: task/closed-change",
            "next_action: clarify acceptance criteria": "next_action: none",
            "|  | rule / gotcha / fact / runbook / project-skill / workflow-feedback | pending |  |  |": (
                "| No reusable lesson | fact | not-promoted | work item | one-off sample |"
            ),
            "- Acceptance complete: yes / no": "- Acceptance complete: yes",
            "- Required gates closed: yes / no": "- Required gates closed: yes",
            "- Experience Promotion complete: yes / no": (
                "- Experience Promotion complete: YES"
            ),
            "- Durable writeback complete: yes / no": (
                "- Durable writeback complete: yes"
            ),
        },
    )


def create_project_skill(target: Path) -> None:
    skill_name = "reset-sample-sandbox"
    directory = target / "project-skills" / skill_name
    directory.mkdir()
    shutil.copy2(
        target / "zettelkasten/templates/project-skill.md",
        directory / "SKILL.md",
    )
    skill_file = directory / "SKILL.md"
    text = skill_file.read_text().replace("project-procedure-name", skill_name)
    text = text.replace(
        "description: Describe what this procedure does and the concrete repository situations that should trigger it.",
        "description: >\n  Reset the sample sandbox when integration tests reuse stale provider state\n  or resend flows return an old token.",
    )
    skill_file.write_text(text)
    index = target / "project-skills/INDEX.md"
    index.write_text(
        index.read_text().replace(
            "| None |  |  |  |  |  |",
            (
                f"| {skill_name} | stale provider state or old resend token \\| code | "
                f"local unit tests | active | {date.today().isoformat()} | 180 |"
            ),
        )
    )


def create_tracked_work_with_cli(target: Path) -> str:
    work_id = "WORK-20260712122000-tracked-bug"
    run(["git", "switch", "-c", "task/tracked-bug"], cwd=target)
    result = run(
        [
            sys.executable,
            str(WORKFLOW_TASK),
            "new",
            "tracked-bug",
            "--id",
            work_id,
            "--route",
            "tracked",
            "--owned-path",
            "src/shared/module",
            "--next-action",
            "implement regression fix",
            "--json",
        ],
        cwd=target,
    )
    require(json.loads(result.stdout)["work_id"] == work_id, "WORK CLI returned wrong ID")
    work_root = target / "zettelkasten/work"
    require(
        sorted(path.name for path in work_root.glob("*.md") if path.name != "README.md")
        == [f"{work_id}.md"],
        "Tracked work created more than one workflow record",
    )
    return work_id


def exercise_work_cli(target: Path, work_id: str) -> None:
    run(
        [
            sys.executable,
            str(WORKFLOW_TASK),
            "checkpoint",
            work_id,
            "--completed-step",
            "confirmed root cause",
            "--validation",
            "focused regression test failed before fix",
            "--next-action",
            "inspect \"r\u00e9sum\u00e9\" before implementing fix",
            "--owned-path",
            "src/shared/module",
            "--owned-path",
            "docs/runbooks",
        ],
        cwd=target,
    )
    text = (target / f"zettelkasten/work/{work_id}.md").read_text()
    require("- Last completed step: confirmed root cause" in text, "checkpoint was not written")
    require(
        'owned_paths: ["src/shared/module", "docs/runbooks"]' in text,
        "checkpoint did not replace owned paths",
    )
    status = run([sys.executable, str(WORKFLOW_DOCTOR), "--status"], cwd=target)
    require('next=inspect "r\u00e9sum\u00e9" before implementing fix' in status.stdout, "status did not decode YAML string escapes")
    require("\\u00e9" not in status.stdout and '\\"' not in status.stdout, "status leaked serialized YAML escapes")

    governed_id = "WORK-20260712122030-governed-cli"
    run(
        [
            sys.executable,
            str(WORKFLOW_TASK),
            "new",
            "governed-cli",
            "--id",
            governed_id,
            "--route",
            "governed",
        ],
        cwd=target,
    )
    governed_path = target / f"zettelkasten/work/{governed_id}.md"
    governed_text = governed_path.read_text()
    require("- Selected route: governed" in governed_text, "governed route bullet was not written")
    require("governed / governed" not in governed_text, "governed route replacement corrupted the template")
    governed_path.write_text(
        governed_text.replace(
            "|  | rule / gotcha / fact / runbook / project-skill / workflow-feedback | pending |  |  |",
            "| No reusable lesson | fact | not-promoted | work item | one-off sample |",
        )
    )
    pending_gate_close = run(
        [
            sys.executable,
            str(WORKFLOW_TASK),
            "close",
            governed_id,
            "--acceptance-complete",
            "--gates-closed",
            "--promotion-complete",
            "--writeback-complete",
            "--integration-result",
            "must remain open",
        ],
        cwd=target,
        expected=1,
    )
    require(
        "governed gates still contain a pending gate" in pending_gate_close.stderr,
        "WORK CLI closed governed work with a pending gate",
    )
    governed_path.unlink()

    invalid_id = "WORK-20260712122040-invalid-path"
    invalid_path = run(
        [
            sys.executable,
            str(WORKFLOW_TASK),
            "new",
            "invalid-path",
            "--id",
            invalid_id,
            "--owned-path",
            r"C:\\repo\\src",
        ],
        cwd=target,
        expected=1,
    )
    require("repository-relative" in invalid_path.stderr, "Windows absolute owned path was accepted")

    close_id = "WORK-20260712122100-close-cli"
    run(
        [
            sys.executable,
            str(WORKFLOW_TASK),
            "new",
            "close-cli",
            "--id",
            close_id,
        ],
        cwd=target,
    )
    close_path = target / f"zettelkasten/work/{close_id}.md"
    pending_close = run(
        [
            sys.executable,
            str(WORKFLOW_TASK),
            "close",
            close_id,
            "--acceptance-complete",
            "--gates-closed",
            "--promotion-complete",
            "--writeback-complete",
            "--integration-result",
            "must remain open",
        ],
        cwd=target,
        expected=1,
    )
    require("pending decision" in pending_close.stderr, "pending Decision cell was not detected")
    close_path.write_text(
        close_path.read_text().replace(
            "|  | rule / gotcha / fact / runbook / project-skill / workflow-feedback | pending |  |  |",
            "| No reusable lesson | fact | not-promoted | pending destination | one-off sample |",
        )
    )
    run(
        [
            sys.executable,
            str(WORKFLOW_TASK),
            "close",
            close_id,
            "--acceptance-complete",
            "--gates-closed",
            "--promotion-complete",
            "--writeback-complete",
            "--integration-result",
            "validated on task branch",
        ],
        cwd=target,
    )
    require('status: "done"' in close_path.read_text(), "WORK CLI did not close the task")


def validate_doctor_regressions(target: Path, work_id: str) -> None:
    work = target / f"zettelkasten/work/{work_id}.md"
    original = work.read_text()
    work.write_text(original.replace('branch: "task/tracked-bug"', "branch:"))
    blank_branch = run(
        [sys.executable, str(WORKFLOW_DOCTOR)],
        cwd=target,
        expected=1,
    )
    require("active work is missing branch" in blank_branch.stdout, "blank branch bypassed doctor")
    work.write_text(original)

    block_list = original.replace(
        'owned_paths: ["src/shared/module", "docs/runbooks"]',
        "owned_paths:\n  - src/shared/module\n  - docs/runbooks",
    )
    work.write_text(block_list)
    list_status = run(
        [sys.executable, str(WORKFLOW_DOCTOR), "--status", "--json"],
        cwd=target,
    )
    listed_work = next(
        item for item in json.loads(list_status.stdout)["active_work"] if item["work_id"] == work_id
    )
    require(
        listed_work["owned_paths"] == ["src/shared/module", "docs/runbooks"],
        "block-list owned paths were not parsed",
    )
    run(
        [
            sys.executable,
            str(WORKFLOW_TASK),
            "checkpoint",
            work_id,
            "--completed-step",
            "expanded task scope",
            "--validation",
            "scope review complete",
            "--next-action",
            "continue implementation",
            "--owned-path",
            "src/replacement",
        ],
        cwd=target,
    )
    replaced_scope = work.read_text()
    require('owned_paths: ["src/replacement"]' in replaced_scope, "checkpoint did not replace a block-list scope")
    require("\n  - src/shared/module" not in replaced_scope, "checkpoint left stale block-list items")
    work.write_text(original)

    ambiguous = target / "zettelkasten/ambiguous-link-test.md"
    ambiguous.write_text("# Ambiguous\n\n[[README]]\n")
    ambiguity = run(
        [sys.executable, str(WORKFLOW_DOCTOR)],
        cwd=target,
        expected=1,
    )
    require("ambiguous wiki link [[README]]" in ambiguity.stdout, "ambiguous wiki link passed")
    ambiguous.unlink()

    unexpected_artifact = target / "zettelkasten/work/NOTE-invalid.md"
    unexpected_artifact.write_text("# Invalid work artifact\n")
    unexpected_result = run(
        [sys.executable, str(WORKFLOW_DOCTOR)],
        cwd=target,
        expected=1,
    )
    require(
        "unexpected work artifact name" in unexpected_result.stdout,
        "doctor accepted a non-WORK file in the work directory",
    )
    unexpected_artifact.unlink()

    stale = target / "zettelkasten/stale-test.md"
    stale.write_text(
        "---\ntitle: Stale Test\nstatus: active\nlast_verified_at: 2000-01-01\n"
        "review_after_days: 1\n---\n\n# Stale Test\n"
    )
    stale_result = run([sys.executable, str(WORKFLOW_DOCTOR)], cwd=target)
    require("knowledge is stale" in stale_result.stdout, "stale knowledge was not reported")
    stale.unlink()

    invalid_interval = target / "zettelkasten/invalid-interval.md"
    invalid_interval.write_text(
        "---\ntitle: Invalid Interval\nstatus: active\nlast_verified_at: 2026-07-12\n"
        "review_after_days: 0\n---\n\n# Invalid Interval\n"
    )
    interval_result = run(
        [sys.executable, str(WORKFLOW_DOCTOR)],
        cwd=target,
        expected=1,
    )
    require("review_after_days must be positive" in interval_result.stdout, "non-positive review interval passed")
    invalid_interval.unlink()

    pending_gate_id = "WORK-20260712122500-pending-gate"
    pending_gate = copy_artifact(
        target,
        "work-item.md",
        f"{pending_gate_id}.md",
        {
            "WORK-YYYYMMDDHHMMSS-short-name": pending_gate_id,
            "status: backlog": "status: done",
            "route: tracked": "route: governed",
            "branch: task/work-id-short-name": "branch: task/pending-gate",
            "next_action: clarify acceptance criteria": "next_action: none",
            "|  | rule / gotcha / fact / runbook / project-skill / workflow-feedback | pending |  |  |": (
                "| No reusable lesson | fact | not-promoted | work item | one-off sample |"
            ),
            "- Experience Promotion complete: yes / no": "- Experience Promotion complete: yes",
        },
    )
    pending_gate_result = run(
        [sys.executable, str(WORKFLOW_DOCTOR)],
        cwd=target,
        expected=1,
    )
    require(
        "closed governed work has a pending gate" in pending_gate_result.stdout,
        "doctor accepted closed governed work with a pending gate",
    )
    pending_gate.unlink()


def validate_worktree_helper(target: Path, tracked_work_id: str) -> None:
    run(["git", "add", "."], cwd=target)
    run(
        [
            "git",
            "-c",
            "user.name=Validator",
            "-c",
            "user.email=validator@example.invalid",
            "commit",
            "-m",
            "test: add tracked workflow state",
        ],
        cwd=target,
    )
    run(["git", "branch", "task/existing", "main"], cwd=target)
    existing_path = target.parent / "existing-worktree"
    existing = run(
        [
            sys.executable,
            str(TASK_WORKTREE),
            "create",
            "WORK-existing",
            "--branch",
            "task/existing",
            "--base",
            "main",
            "--path",
            str(existing_path),
            "--dry-run",
        ],
        cwd=target,
        expected=1,
    )
    require("task branch already exists" in existing.stderr, "existing branch was silently reused")
    reused_with_base = run(
        [
            sys.executable,
            str(TASK_WORKTREE),
            "create",
            "WORK-existing",
            "--branch",
            "task/existing",
            "--base",
            "main",
            "--reuse-existing",
            "--path",
            str(existing_path),
            "--dry-run",
        ],
        cwd=target,
        expected=1,
    )
    require("--base cannot be applied" in reused_with_base.stderr, "reuse still ignored --base")

    dirty_file = target / "dirty-local.txt"
    dirty_file.write_text("preserve me\n")
    destination = target.parent / "task-worktree"
    created = run(
        [
            sys.executable,
            str(TASK_WORKTREE),
            "create",
            "WORK-20260712123000-helper",
            "--slug",
            "helper",
            "--base",
            "main",
            "--path",
            str(destination),
        ],
        cwd=target,
    )
    require("current checkout is dirty" in created.stdout, "dirty checkout warning is missing")
    require((destination / ".git").is_file(), "task worktree was not created")
    dirty_file.unlink()

    helper_branch = run(["git", "branch", "--show-current"], cwd=destination).stdout.strip()
    helper_id = "WORK-20260712123000-helper"
    helper_new = run(
        [
            sys.executable,
            str(WORKFLOW_TASK),
            "new",
            "helper",
            "--id",
            helper_id,
            "--owned-path",
            "src/shared",
        ],
        cwd=destination,
    )
    require(helper_id in helper_new.stdout, "helper WORK was not created")
    require(helper_branch.startswith("task/"), "helper worktree is not on a task branch")

    status = run(
        [
            sys.executable,
            str(WORKFLOW_DOCTOR),
            "--status",
            "--all-worktrees",
            "--json",
        ],
        cwd=target,
    )
    payload = json.loads(status.stdout)
    work_ids = {item["work_id"] for item in payload["active_work"]}
    require({tracked_work_id, helper_id}.issubset(work_ids), "all-worktree status missed active work")
    require(payload["scope_overlaps"], "owned-path overlap was not reported")
    require(not payload["unscoped_work"], "scoped parallel work was reported as unscoped")

    run(["git", "switch", "--detach"], cwd=destination)
    detached_status = run(
        [
            sys.executable,
            str(WORKFLOW_DOCTOR),
            "--status",
            "--all-worktrees",
            "--json",
        ],
        cwd=target,
    )
    detached_payload = json.loads(detached_status.stdout)
    detached_ids = [item["work_id"] for item in detached_payload["active_work"]]
    require(helper_id not in detached_ids, "detached worktree duplicated branch-owned active work")
    require(
        str(destination.resolve()) in detached_payload["detached_worktrees"],
        "detached worktree was not disclosed",
    )


def validate_wiki_links(vault: Path) -> None:
    exact: set[str] = set()
    stems: dict[str, list[Path]] = {}
    for path in sorted(vault.rglob("*.md")):
        exact.add(path.relative_to(vault).with_suffix("").as_posix())
        stems.setdefault(path.stem, []).append(path)
    broken: list[str] = []
    for path in sorted(vault.rglob("*.md")):
        for raw in re.findall(r"(?<!!)\[\[([^\]|#]+)", path.read_text()):
            target = raw.strip().removesuffix(".md")
            if any(marker in target for marker in ("YYYY", "<", "{{")):
                continue
            if "/" in target and target not in exact:
                broken.append(f"{path.relative_to(vault)} -> [[{target}]]")
            elif "/" not in target and len(stems.get(target, [])) != 1:
                broken.append(f"{path.relative_to(vault)} -> ambiguous or missing [[{target}]]")
    require(not broken, "invalid wiki links:\n" + "\n".join(broken))


def require_adapter_present(target: Path, adapter: str) -> None:
    for path in MODEL_ROUTING_ADAPTER_FILES[adapter]:
        require(
            (target / path).is_file(),
            f"bootstrap omitted {adapter} adapter file: {path}",
        )


def validate_model_routing_bootstrap(base: Path) -> None:
    payload_only = base / "payload-only"
    unavailable_target = base / "unavailable-routing-target"
    shutil.copytree(PAYLOAD, payload_only)
    unavailable = run(
        [
            sys.executable,
            str(BOOTSTRAP),
            "--source",
            str(payload_only),
            "--target",
            str(unavailable_target),
            "--with-model-routing",
            "codex",
        ],
        expected=1,
    )
    require(
        "model-routing adapters are unavailable" in unavailable.stderr,
        "payload-only source did not explain the missing adapter overlay",
    )
    require(
        not unavailable_target.exists(),
        "missing adapter source caused a partial core installation",
    )

    target = base / "routing-target"
    run([sys.executable, str(BOOTSTRAP), "--source", str(ROOT), "--target", str(target)])
    require(
        not (target / ".codex").exists() and not (target / ".claude").exists(),
        "default bootstrap enabled model routing",
    )
    missing_codex = run(
        [
            sys.executable,
            str(BOOTSTRAP),
            "--target",
            str(target),
            "--inspect",
            "--with-model-routing",
            "codex",
        ],
        expected=2,
    )
    require(
        "Model routing status: codex adapter incomplete" in missing_codex.stdout,
        "adapter inspection did not report an omitted Codex overlay",
    )

    codex_command = [
        sys.executable,
        str(BOOTSTRAP),
        "--source",
        str(ROOT),
        "--target",
        str(target),
        "--with-model-routing",
        "codex",
    ]
    run(codex_command)
    require_adapter_present(target, "codex")
    require(not (target / ".claude").exists(), "Codex opt-in installed Claude routing")
    identical_codex = run(codex_command)
    require(
        "Conflicts left untouched: 0" in identical_codex.stdout,
        "identical Codex adapter rerun conflicted",
    )

    local_codex_config = "model = \"local-model\"\n"
    codex_config = target / ".codex/config.toml"
    codex_config.write_text(local_codex_config)
    codex_conflict = run(codex_command, expected=2)
    require(
        "conflict: .codex/config.toml" in codex_conflict.stdout,
        "Codex config conflict was not reported",
    )
    require(
        codex_config.read_text() == local_codex_config,
        "local Codex config was overwritten",
    )
    shutil.copy2(ADAPTERS / "codex/.codex/config.toml", codex_config)

    claude_command = [
        sys.executable,
        str(BOOTSTRAP),
        "--source",
        str(ROOT),
        "--target",
        str(target),
        "--with-model-routing",
        "claude",
    ]
    run(claude_command)
    require_adapter_present(target, "claude")
    require(
        not (target / ".claude/settings.json").exists(),
        "Claude opt-in overrode the root model",
    )
    local_claude_agent = "---\nname: explorer\nmodel: local-model\n---\n"
    claude_agent = target / ".claude/agents/explorer.md"
    claude_agent.write_text(local_claude_agent)
    claude_conflict = run(claude_command, expected=2)
    require(
        "conflict: .claude/agents/explorer.md" in claude_conflict.stdout,
        "Claude Code agent conflict was not reported",
    )
    require(
        claude_agent.read_text() == local_claude_agent,
        "local Claude Code agent was overwritten",
    )
    shutil.copy2(
        ADAPTERS / "claude/.claude/agents/explorer.md", claude_agent
    )
    run(
        [
            sys.executable,
            str(BOOTSTRAP),
            "--target",
            str(target),
            "--inspect",
            "--with-model-routing",
            "all",
        ]
    )

    all_target = base / "all-routing-target"
    run(
        [
            sys.executable,
            str(BOOTSTRAP),
            "--source",
            str(ROOT),
            "--target",
            str(all_target),
            "--with-model-routing",
            "all",
        ]
    )
    require_adapter_present(all_target, "codex")
    require_adapter_present(all_target, "claude")


def validate_bootstrap_lifecycle() -> None:
    with tempfile.TemporaryDirectory(prefix="repo-continuity-distribution-") as temp_dir:
        base = Path(temp_dir)
        legacy_payload = base / "legacy-payload"
        legacy_target = base / "legacy-target"
        shutil.copytree(PAYLOAD, legacy_payload)
        (legacy_payload / MARKER_NAME).rename(legacy_payload / LEGACY_MARKER_NAME)
        run(
            [
                sys.executable,
                str(BOOTSTRAP),
                "--source",
                str(legacy_payload),
                "--target",
                str(legacy_target),
            ]
        )
        require(
            (legacy_target / LEGACY_MARKER_NAME).is_file(),
            "bootstrap dropped the legacy interrupted-initialization marker",
        )
        legacy_doctor = run(
            [sys.executable, str(WORKFLOW_DOCTOR), "--strict"],
            cwd=legacy_target,
            expected=1,
        )
        require(
            f"WARN: {LEGACY_MARKER_NAME}: payload marker is present" in legacy_doctor.stdout,
            "Doctor no longer recognizes the legacy payload marker",
        )

        target = base / "target"
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
        require("Would copy:" in dry_run.stdout and not target.exists(), "dry-run changed target")
        run([sys.executable, str(BOOTSTRAP), "--source", str(ROOT), "--target", str(target)])
        require(
            not (target / ".codex").exists() and not (target / ".claude").exists(),
            "default bootstrap installed optional model routing",
        )
        identical = run(
            [sys.executable, str(BOOTSTRAP), "--source", str(ROOT), "--target", str(target)]
        )
        require("Conflicts left untouched: 0" in identical.stdout, "identical rerun conflicted")

        local_rules = "# Local rules\n"
        (target / "AGENTS.md").write_text(local_rules)
        conflict = run(
            [sys.executable, str(BOOTSTRAP), "--source", str(ROOT), "--target", str(target)],
            expected=2,
        )
        require("conflict: AGENTS.md" in conflict.stdout, "AGENTS conflict was not reported")
        require((target / "AGENTS.md").read_text() == local_rules, "local rules were overwritten")
        shutil.copy2(PAYLOAD / "AGENTS.md", target / "AGENTS.md")

        run([sys.executable, str(BOOTSTRAP), "--target", str(target), "--inspect"])
        initialize_target(target)
        validate_tool_free_core(target)
        clean = run([sys.executable, str(WORKFLOW_DOCTOR), "--strict"], cwd=target)
        require("PASS: workflow state looks consistent" in clean.stdout, "clean doctor failed")

        initialize_git(target)
        tracked_id = create_tracked_work_with_cli(target)
        exercise_work_cli(target, tracked_id)
        create_governed_and_done_state(target)
        create_project_skill(target)
        validate_doctor_regressions(target, tracked_id)
        validate_wiki_links(target / "zettelkasten")
        active = run([sys.executable, str(WORKFLOW_DOCTOR), "--strict"], cwd=target)
        require("active work:" in active.stdout, "doctor did not report active WORK")
        validate_worktree_helper(target, tracked_id)
        validate_model_routing_bootstrap(base)


def validate_manual_copy() -> None:
    with tempfile.TemporaryDirectory(prefix="repo-continuity-copy-") as temp_dir:
        base = Path(temp_dir)
        target = base / "target"
        shutil.copytree(PAYLOAD, target)
        for path in REQUIRED_FILES:
            require((target / path).is_file(), f"manual copy omitted {path}")
        require(
            not (target / ".codex").exists() and not (target / ".claude").exists(),
            "manual core copy included optional model routing",
        )
        for path in REQUIRED_DIRECTORIES:
            require((target / path).is_dir(), f"manual copy omitted {path}")

        for adapter in MODEL_ROUTING_ADAPTER_FILES:
            overlay_target = base / f"{adapter}-target"
            shutil.copytree(PAYLOAD, overlay_target)
            shutil.copytree(
                ADAPTERS / adapter, overlay_target, dirs_exist_ok=True
            )
            require_adapter_present(overlay_target, adapter)
            other_adapter = "claude" if adapter == "codex" else "codex"
            other_directory = ".claude" if other_adapter == "claude" else ".codex"
            require(
                not (overlay_target / other_directory).exists(),
                f"manual {adapter} overlay included {other_adapter} routing",
            )


def validate_symlink_boundary() -> None:
    with tempfile.TemporaryDirectory(prefix="repo-continuity-symlink-") as temp_dir:
        base = Path(temp_dir)
        target = base / "target"
        outside = base / "outside"
        target.mkdir()
        outside.mkdir()
        (target / "zettelkasten").symlink_to(outside, target_is_directory=True)
        result = run(
            [sys.executable, str(BOOTSTRAP), "--source", str(ROOT), "--target", str(target)],
            expected=2,
        )
        require("conflict: zettelkasten/AI.md" in result.stdout, "symlink was not reported")
        require(not any(outside.iterdir()), "bootstrap wrote through a symlink")


def validate_remote_source() -> None:
    with tempfile.TemporaryDirectory(prefix="repo-continuity-remote-") as temp_dir:
        base = Path(temp_dir)
        source = base / "source"
        target = base / "target"
        all_target = base / "all-target"
        source.mkdir()
        shutil.copytree(PAYLOAD, source / "template")
        shutil.copytree(ADAPTERS, source / "adapters")
        run(["git", "init", "--initial-branch", "main"], cwd=source)
        run(["git", "add", "template", "adapters"], cwd=source)
        run(
            [
                "git",
                "-c",
                "user.name=Validator",
                "-c",
                "user.email=validator@example.invalid",
                "commit",
                "-m",
                "test: add payload",
            ],
            cwd=source,
        )
        run(["git", "tag", RELEASE_VERSION], cwd=source)
        run(
            [
                sys.executable,
                str(BOOTSTRAP),
                "--repo-url",
                str(source),
                "--target",
                str(target),
            ]
        )
        require((target / "project-skills/INDEX.md").is_file(), "remote omitted Skills")
        require(
            not (target / ".codex").exists() and not (target / ".claude").exists(),
            "remote default bootstrap installed optional model routing",
        )
        run(
            [
                sys.executable,
                str(BOOTSTRAP),
                "--repo-url",
                str(source),
                "--target",
                str(all_target),
                "--with-model-routing",
                "all",
            ]
        )
        require_adapter_present(all_target, "codex")
        require_adapter_present(all_target, "claude")


def validate_behavior_evaluator() -> None:
    cases = json.loads((ROOT / "examples/evaluations/workflow-cases.json").read_text())
    responses = [dict(id=case["id"], **case["expected"]) for case in cases]
    fixture = {
        "run": {
            "run_id": "distribution-validator-fixture",
            "agent": "synthetic evaluator regression fixture",
            "generated_at": "2026-07-12T00:00:00Z",
        },
        "responses": responses,
    }
    with tempfile.TemporaryDirectory(prefix="workflow-evaluator-") as temp_dir:
        response_path = Path(temp_dir) / "responses.json"
        response_path.write_text(json.dumps(fixture))
        matched = run(
            [sys.executable, str(BEHAVIOR_EVALUATOR), "--responses", str(response_path)]
        )
        require("MATCH:" in matched.stdout, "behavior evaluator rejected a conforming fixture")
        fixture["responses"][0]["route"] = "governed"
        response_path.write_text(json.dumps(fixture))
        mismatch = run(
            [sys.executable, str(BEHAVIOR_EVALUATOR), "--responses", str(response_path)],
            expected=1,
        )
        require("FAIL: direct-doc-link: route" in mismatch.stdout, "behavior evaluator accepted a known mismatch")


def validate_repository_layout() -> None:
    require(not (ROOT / "zettelkasten").exists(), "root zettelkasten must not exist")
    require((ROOT / "LICENSE").is_file(), "LICENSE is missing")
    require(SKILL_ROOT.is_dir(), "repo-continuity companion Skill is missing")
    require(
        not (ROOT / "skills/ai-collaboration-workflow").exists(),
        "legacy companion Skill directory remains installed beside repo-continuity",
    )
    openai_metadata = (SKILL_ROOT / "agents/openai.yaml").read_text()
    require(
        "$repo-continuity" in openai_metadata
        and "$ai-collaboration-workflow" not in openai_metadata,
        "companion Skill UI metadata uses a stale invocation name",
    )
    readme = (ROOT / "README.md").read_text()
    for expected in (
        "# Repo Continuity",
        "One repository. Many coding agents. One durable project memory.",
        "Resume, do not restart.",
        "Make the project learn.",
        "## Quick Start",
        f"{CANONICAL_REPO_URL}/tree/{RELEASE_VERSION}/skills/repo-continuity",
        "Use $repo-continuity to initialize this repository.",
        "npx skills add` installs the Companion Skill only",
        "npx skills remove ai-collaboration-workflow -g -y",
        "## Initialization Is Complete When",
        "## Daily Use",
        "Checkpoint only at meaningful boundaries",
        "Promotion is idempotent",
        "Semantic Fresh-Agent recovery",
        "Do not use the raw copy command over an existing",
        "--with-model-routing codex",
        "current user or session selection; not overridden",
        "adapters/",
        "## License",
    ):
        require(expected in readme, f"README is missing onboarding contract: {expected}")
    require("Why v4 Is Breaking" not in readme, "README still leads with breaking-change history")
    chinese_readme = (ROOT / "docs/zh-CN/README.md").read_text()
    for expected in (
        "# Repo Continuity",
        "一个仓库，多种 Coding Agent，一套持续演进的项目知识。",
        "接着做，而不是重新开始。",
        "让项目从开发中持续学习。",
        "## 快速开始",
        f"{CANONICAL_REPO_URL}/tree/{RELEASE_VERSION}/skills/repo-continuity",
        "使用 $repo-continuity 初始化当前仓库。",
        "npx skills add` 只会安装 Companion Skill",
        "npx skills remove ai-collaboration-workflow -g -y",
        "## 初始化完成标准",
        "## 日常使用",
        "只在有意义的边界记录 checkpoint",
        "经验固化必须是幂等的",
        "Fresh-Agent 语义恢复",
        "不要直接执行覆盖式复制",
        "--with-model-routing codex",
        "用户或当前会话选择；overlay 不覆盖",
        "adapters/",
        "## 产品边界",
        "**核心**",
        "**可选**",
        "**非目标**",
    ):
        require(expected in chinese_readme, f"Chinese guide is missing documentation contract: {expected}")
    require("为什么 v4 是破坏性更新" not in chinese_readme, "Chinese guide still leads with breaking-change history")
    publishing = (ROOT / "docs/community-publishing.md").read_text()
    require("-> Doctor" not in publishing, "publishing copy makes the optional Doctor a fixed stage")
    require("Repo Continuity" in publishing, "publishing copy is missing the product name")
    require(CANONICAL_REPO_URL in publishing, "publishing copy uses a stale repository URL")
    require(
        f'DEFAULT_REPO_URL = "{CANONICAL_REPO_URL}.git"' in BOOTSTRAP.read_text(),
        "bootstrap uses a stale canonical repository URL",
    )
    require(
        f'DEFAULT_REF = "{RELEASE_VERSION}"' in BOOTSTRAP.read_text(),
        "bootstrap default ref is not locked to the documented release",
    )
    for expected in (
        'choices=("codex", "claude", "all")',
        "The default installation remains core-only.",
    ):
        require(expected in BOOTSTRAP.read_text(), f"bootstrap is missing opt-in contract: {expected}")
    git_collaboration = (PAYLOAD / "zettelkasten/git-collaboration.md").read_text()
    require("date +%Y%m%d%H%M%S" in git_collaboration, "manual WORK ID recipe is not locally discoverable")
    feedback_guide = ROOT / "docs/workflow-feedback.md"
    require(feedback_guide.is_file(), "workflow feedback maintainer guide is missing")
    issue_form = ROOT / ".github/ISSUE_TEMPLATE/workflow-feedback.yml"
    require(issue_form.is_file(), "workflow feedback Issue form is missing")
    feedback_reference = SKILL_ROOT / "references/template-feedback.md"
    require(feedback_reference.is_file(), "companion Skill feedback reference is missing")
    resume_evaluation = ROOT / "docs/fresh-agent-resume-evaluation.md"
    for expected in (
        "## When To Run",
        "## Evidence Integrity",
        "It is not a routine per-task gate",
        "it must never be reported as Fresh-Agent behavior evidence",
    ):
        require(
            expected in resume_evaluation.read_text(),
            f"Fresh-Agent evaluation is missing evidence contract: {expected}",
        )
    cases = json.loads((ROOT / "examples/evaluations/workflow-cases.json").read_text())
    feedback_cases = [case for case in cases if case["expected"]["feedback_action"] != "none"]
    require(len(feedback_cases) == 1, "behavior cases need exactly one positive workflow-feedback case")
    require(
        feedback_cases[0]["expected"]["feedback_action"] == "record-local"
        and feedback_cases[0]["expected"]["feedback_scope"] == "template-wide",
        "positive workflow-feedback case must remain local and template-wide",
    )
    for helper in (WORKFLOW_DOCTOR, WORKFLOW_TASK, TASK_WORKTREE):
        require(helper.is_file(), f"optional Skill helper is missing: {helper.relative_to(ROOT)}")
        require(helper.stat().st_mode & 0o111, f"optional Skill helper is not executable: {helper.relative_to(ROOT)}")
    require(
        not (SKILL_ROOT / "references/migration.md").exists(),
        "unsupported migration reference remains",
    )
    for path in (
        ROOT / "docs/fresh-agent-resume-evaluation.md",
        ROOT / "docs/workflow-behavior-evaluation.md",
        feedback_guide,
        ROOT / "examples/practical-scenarios/README.md",
        ROOT / "examples/evaluations/workflow-cases.json",
        SKILL_ROOT / "references/routing.md",
        feedback_reference,
    ):
        require(path.is_file(), f"repository artifact is missing: {path.relative_to(ROOT)}")


def main() -> int:
    try:
        validate_payload()
        validate_model_routing_adapters()
        validate_repository_layout()
        validate_manual_copy()
        validate_bootstrap_lifecycle()
        validate_symlink_boundary()
        validate_remote_source()
        validate_behavior_evaluator()
    except ValidationFailure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("PASS: template payload and distribution lifecycle are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
