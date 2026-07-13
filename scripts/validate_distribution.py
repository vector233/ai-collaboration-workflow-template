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
MARKER = PAYLOAD / ".ai-collaboration-workflow-template"
BOOTSTRAP = ROOT / "skills/ai-collaboration-workflow/scripts/bootstrap_template.py"
WORKFLOW_DOCTOR = ROOT / "skills/ai-collaboration-workflow/scripts/workflow_doctor.py"
WORKFLOW_TASK = ROOT / "skills/ai-collaboration-workflow/scripts/workflow_task.py"
TASK_WORKTREE = ROOT / "skills/ai-collaboration-workflow/scripts/task_worktree.py"
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
        MARKER.read_text().strip() == "canonical-payload-v4",
        "payload marker version is incorrect",
    )
    for path in REQUIRED_FILES:
        require((PAYLOAD / path).is_file(), f"payload file is missing: {path}")
    for path in REQUIRED_DIRECTORIES:
        require((PAYLOAD / path).is_dir(), f"payload directory is missing: {path}")
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

    workflow = (PAYLOAD / "zettelkasten/workflow.md").read_text()
    for expected in (
        "## Route Decision",
        "Direct",
        "Tracked",
        "Governed",
        "## Stable Work Record",
        "## Experience Promotion Check",
    ):
        require(expected in workflow, f"workflow is missing {expected}")

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


def validate_bootstrap_lifecycle() -> None:
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
        require("Would copy:" in dry_run.stdout and not target.exists(), "dry-run changed target")
        run([sys.executable, str(BOOTSTRAP), "--source", str(ROOT), "--target", str(target)])
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
        result = run(
            [sys.executable, str(BOOTSTRAP), "--source", str(ROOT), "--target", str(target)],
            expected=2,
        )
        require("conflict: zettelkasten/AI.md" in result.stdout, "symlink was not reported")
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
        require((target / "project-skills/INDEX.md").is_file(), "remote omitted Skills")


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
    readme = (ROOT / "README.md").read_text()
    for expected in (
        "## Quick Start",
        "tree/v4.0.0/skills/ai-collaboration-workflow",
        "Use $ai-collaboration-workflow to initialize this repository.",
        "## Initialization Is Complete When",
        "## Daily Use",
        "## Why v4 Is Breaking",
        "Do not use the raw copy command over an existing",
        "## License",
    ):
        require(expected in readme, f"README is missing onboarding contract: {expected}")
    chinese_readme = (ROOT / "docs/zh-CN/README.md").read_text()
    for expected in (
        "## 快速开始",
        "tree/v4.0.0/skills/ai-collaboration-workflow",
        "使用 $ai-collaboration-workflow 初始化当前仓库。",
        "## 初始化完成标准",
        "## 日常使用",
        "## 为什么 v4 是破坏性更新",
        "不要直接执行覆盖式复制",
        "## 产品边界",
        "**核心**",
        "**可选**",
        "**非目标**",
    ):
        require(expected in chinese_readme, f"Chinese guide is missing documentation contract: {expected}")
    publishing = (ROOT / "docs/community-publishing.md").read_text()
    require("-> Doctor" not in publishing, "publishing copy makes the optional Doctor a fixed stage")
    git_collaboration = (PAYLOAD / "zettelkasten/git-collaboration.md").read_text()
    require("date +%Y%m%d%H%M%S" in git_collaboration, "manual WORK ID recipe is not locally discoverable")
    feedback_guide = ROOT / "docs/workflow-feedback.md"
    require(feedback_guide.is_file(), "workflow feedback maintainer guide is missing")
    issue_form = ROOT / ".github/ISSUE_TEMPLATE/workflow-feedback.yml"
    require(issue_form.is_file(), "workflow feedback Issue form is missing")
    feedback_reference = ROOT / "skills/ai-collaboration-workflow/references/template-feedback.md"
    require(feedback_reference.is_file(), "companion Skill feedback reference is missing")
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
        not (ROOT / "skills/ai-collaboration-workflow/references/migration.md").exists(),
        "unsupported migration reference remains",
    )
    for path in (
        ROOT / "docs/fresh-agent-resume-evaluation.md",
        ROOT / "docs/workflow-behavior-evaluation.md",
        feedback_guide,
        ROOT / "examples/practical-scenarios/README.md",
        ROOT / "examples/evaluations/workflow-cases.json",
        ROOT / "skills/ai-collaboration-workflow/references/routing.md",
        feedback_reference,
    ):
        require(path.is_file(), f"repository artifact is missing: {path.relative_to(ROOT)}")


def main() -> int:
    try:
        validate_payload()
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
