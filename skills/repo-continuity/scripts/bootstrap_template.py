#!/usr/bin/env python3
"""Safely bootstrap Repo Continuity into a repository."""

from __future__ import annotations

import argparse
import difflib
import filecmp
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


DEFAULT_REPO_URL = "https://github.com/vector233/repo-continuity.git"
DEFAULT_REF = "v4.4.0"
PAYLOAD_MARKER = Path(".repo-continuity-template")
LEGACY_PAYLOAD_MARKERS = (Path(".ai-collaboration-workflow-template"),)
PAYLOAD_MARKERS = (PAYLOAD_MARKER, *LEGACY_PAYLOAD_MARKERS)
UPGRADE_EXCLUDED_FILES = frozenset((*PAYLOAD_MARKERS, Path("INIT.md")))
BASELINE_PATTERN = re.compile(r"Template baseline:\s*`([^`]+)`")
UPGRADE_CATEGORIES = (
    "added",
    "unchanged",
    "local-modified",
    "upstream-modified",
    "both-modified",
)

PAYLOAD_REQUIRED_FILES = (
    Path("AGENTS.md"),
    Path("CLAUDE.md"),
    Path("INIT.md"),
    Path("zettelkasten/AI.md"),
    Path("zettelkasten/workflow.md"),
    Path("zettelkasten/skill-lifecycle.md"),
    Path("zettelkasten/git-collaboration.md"),
    Path("zettelkasten/templates/initiative.md"),
    Path("zettelkasten/templates/work-item.md"),
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

INSTALLED_REQUIRED_FILES = tuple(
    path for path in PAYLOAD_REQUIRED_FILES if path != Path("INIT.md")
)

REQUIRED_DIRECTORIES = (
    Path("zettelkasten/work"),
    Path("project-skills"),
)


@dataclass(frozen=True)
class InstallPlan:
    missing: tuple[Path, ...]
    identical: tuple[Path, ...]
    conflicts: tuple[Path, ...]


@dataclass(frozen=True)
class ProjectFile:
    state: str
    content: bytes | None


@dataclass(frozen=True)
class UpgradeEntry:
    path: Path
    category: str
    baseline_state: str
    local_state: str
    upstream_state: str
    local_diff: str
    upstream_diff: str


@dataclass(frozen=True)
class UpgradeAction:
    path: Path
    category: str
    action: str
    content: bytes | None = None


class BootstrapError(RuntimeError):
    """Raised when the template source or target cannot be used safely."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Copy Repo Continuity into a repository without "
            "overwriting differing existing files."
        )
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.cwd(),
        help="Target repository root (default: current directory).",
    )
    parser.add_argument(
        "--source",
        type=Path,
        help=(
            "Local repository checkout or direct template payload directory. "
            "When omitted, clone the canonical repository."
        ),
    )
    parser.add_argument(
        "--repo-url",
        default=DEFAULT_REPO_URL,
        help=f"Template Git repository (default: {DEFAULT_REPO_URL}).",
    )
    parser.add_argument(
        "--ref",
        default=DEFAULT_REF,
        help=f"Git branch or tag to clone (default: {DEFAULT_REF}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be copied without changing the target.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--inspect",
        action="store_true",
        help=(
            "Only check the initialized core and any model-routing adapter "
            "requested with --with-model-routing."
        ),
    )
    mode.add_argument(
        "--upgrade-report",
        action="store_true",
        help=(
            "Compare the target with its recorded template baseline and the "
            "selected upstream version without changing any files."
        ),
    )
    mode.add_argument(
        "--upgrade-apply",
        action="store_true",
        help=(
            "Safely apply conflict-free changes from the selected upstream "
            "version using the recorded template baseline."
        ),
    )
    parser.add_argument(
        "--baseline-ref",
        help=(
            "Baseline Git branch or tag for an upgrade operation. When omitted, "
            "read the version from target/zettelkasten/AI.md."
        ),
    )
    parser.add_argument(
        "--baseline-source",
        type=Path,
        help=(
            "Local checkout or payload for the old upstream baseline. "
            "Valid only with --upgrade-report or --upgrade-apply."
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help=(
            "Emit the upgrade report or apply result as JSON. Valid only with "
            "--upgrade-report or --upgrade-apply."
        ),
    )
    parser.add_argument(
        "--with-model-routing",
        choices=("codex", "claude", "all"),
        help=(
            "Also install or inspect an optional model-routing adapter. "
            "The default installation remains core-only."
        ),
    )
    args = parser.parse_args()
    upgrading = args.upgrade_report or args.upgrade_apply
    if (args.baseline_ref or args.baseline_source or args.json) and not upgrading:
        parser.error(
            "--baseline-ref, --baseline-source, and --json require "
            "--upgrade-report or --upgrade-apply"
        )
    if args.upgrade_report and args.dry_run:
        parser.error("--upgrade-report is already read-only; omit --dry-run")
    return args


def normalize_directory(path: Path, label: str, *, must_exist: bool) -> Path:
    resolved = path.expanduser().resolve()
    if must_exist and not resolved.is_dir():
        raise BootstrapError(f"{label} is not a directory: {resolved}")
    if not must_exist and resolved.exists() and not resolved.is_dir():
        raise BootstrapError(f"{label} is not a directory: {resolved}")
    return resolved


def missing_required_paths(root: Path, required: tuple[Path, ...]) -> list[Path]:
    return [relative for relative in required if not (root / relative).is_file()]


def missing_required_directories(root: Path) -> list[Path]:
    return [
        relative
        for relative in REQUIRED_DIRECTORIES
        if not (root / relative).is_dir()
    ]


def selected_model_routing(selection: str | None) -> tuple[str, ...]:
    if selection == "all":
        return ("codex", "claude")
    if selection:
        return (selection,)
    return ()


def inspect_target(target: Path, adapters: tuple[str, ...]) -> int:
    missing_files = missing_required_paths(target, INSTALLED_REQUIRED_FILES)
    missing_directories = missing_required_directories(target)
    missing_adapters = {
        adapter: missing_required_paths(
            target, MODEL_ROUTING_ADAPTER_FILES[adapter]
        )
        for adapter in adapters
    }
    missing_adapters = {
        adapter: paths for adapter, paths in missing_adapters.items() if paths
    }
    if missing_files or missing_directories:
        print(f"Template status: incomplete ({target})")
        for relative in missing_files:
            print(f"  missing file: {relative}")
        for relative in missing_directories:
            print(f"  missing directory: {relative}")
        if (target / "INIT.md").is_file():
            print("Initialization status: INIT.md is present; continue initialization.")
    else:
        print(f"Template status: core files present ({target})")
        if (target / "INIT.md").is_file():
            print("Initialization status: INIT.md is present; initialization is not finished.")
        else:
            print("Initialization status: INIT.md is absent; verify placeholder checks are clean.")

    for adapter in adapters:
        missing = missing_adapters.get(adapter, [])
        if missing:
            print(f"Model routing status: {adapter} adapter incomplete")
            for relative in missing:
                print(f"  missing adapter file: {relative}")
        else:
            print(f"Model routing status: {adapter} adapter present")

    return 2 if missing_files or missing_directories or missing_adapters else 0


def clone_source(repo_url: str, ref: str, destination: Path) -> Path:
    command = [
        "git",
        "clone",
        "--depth",
        "1",
        "--branch",
        ref,
        "--single-branch",
        repo_url,
        str(destination),
    ]
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError as exc:
        raise BootstrapError(
            "git is required for remote bootstrap; use --source with a local checkout"
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise BootstrapError(
            f"failed to clone {repo_url!r} at branch or tag {ref!r}"
        ) from exc
    return destination


def find_payload_marker(payload: Path) -> Path | None:
    return next(
        (marker for marker in PAYLOAD_MARKERS if (payload / marker).is_file()),
        None,
    )


def validate_payload(payload: Path) -> Path:
    marker = find_payload_marker(payload)
    if marker is None:
        expected = ", ".join(str(payload / candidate) for candidate in PAYLOAD_MARKERS)
        raise BootstrapError(f"template payload marker is missing; expected one of: {expected}")
    missing_files = missing_required_paths(payload, PAYLOAD_REQUIRED_FILES)
    missing_directories = missing_required_directories(payload)
    problems = [
        *(f"file {path}" for path in missing_files),
        *(f"directory {path}" for path in missing_directories),
    ]
    if problems:
        raise BootstrapError(
            "template payload is missing required paths: " + ", ".join(problems)
        )
    return marker


def resolve_payload_root(source: Path) -> Path:
    candidates = (source / "template", source)
    for candidate in candidates:
        if find_payload_marker(candidate) is not None:
            validate_payload(candidate)
            return candidate
    expected = " or ".join(
        str(candidate / marker)
        for candidate in candidates
        for marker in PAYLOAD_MARKERS
    )
    raise BootstrapError(
        f"no marked template payload found under {source}; expected {expected}"
    )


def template_files(source: Path) -> tuple[Path, ...]:
    marker = validate_payload(source)
    files = [
        marker,
        Path("AGENTS.md"),
        Path("CLAUDE.md"),
        Path("INIT.md"),
    ]
    for directory in ("zettelkasten", "project-skills"):
        source_directory = source / directory
        if not source_directory.is_dir():
            continue
        for candidate in sorted(source_directory.rglob("*")):
            if candidate.is_symlink():
                raise BootstrapError(f"template source contains a symlink: {candidate}")
            if candidate.is_file():
                files.append(candidate.relative_to(source))
    return tuple(files)


def resolve_baseline_payload_root(source: Path) -> Path:
    """Resolve an older payload without requiring the current release layout."""
    for candidate in (source / "template", source):
        if find_payload_marker(candidate) is not None:
            return candidate
    expected = " or ".join(
        str(candidate / marker)
        for candidate in (source / "template", source)
        for marker in PAYLOAD_MARKERS
    )
    raise BootstrapError(
        f"no marked baseline payload found under {source}; expected {expected}"
    )


def report_payload_files(payload: Path) -> tuple[Path, ...]:
    files: list[Path] = []
    for relative in (Path("AGENTS.md"), Path("CLAUDE.md")):
        candidate = payload / relative
        if candidate.is_symlink():
            raise BootstrapError(f"template source contains a symlink: {candidate}")
        if candidate.is_file():
            files.append(relative)
    for directory in ("zettelkasten", "project-skills"):
        source_directory = payload / directory
        if not source_directory.exists():
            continue
        if source_directory.is_symlink() or not source_directory.is_dir():
            raise BootstrapError(
                f"template source directory is not a regular directory: {source_directory}"
            )
        for candidate in sorted(source_directory.rglob("*")):
            if candidate.is_symlink():
                raise BootstrapError(f"template source contains a symlink: {candidate}")
            if candidate.is_file():
                relative = candidate.relative_to(payload)
                if relative not in UPGRADE_EXCLUDED_FILES:
                    files.append(relative)
    return tuple(files)


def optional_adapters_root(source: Path, payload: Path) -> Path | None:
    for candidate in (source / "adapters", payload.parent / "adapters"):
        if candidate.is_dir() and not candidate.is_symlink():
            return candidate.resolve()
    return None


def report_source_files(
    source: Path,
    payload: Path,
    adapters: tuple[str, ...],
    *,
    require_adapters: bool,
) -> dict[Path, Path]:
    files = {
        relative: payload / relative
        for relative in report_payload_files(payload)
    }
    if not adapters:
        return files

    adapters_root = optional_adapters_root(source, payload)
    if adapters_root is None:
        if require_adapters:
            raise BootstrapError(
                "model-routing adapters are unavailable from the selected target source"
            )
        return files

    for adapter in adapters:
        adapter_root = adapters_root / adapter
        if not adapter_root.is_dir() or adapter_root.is_symlink():
            if require_adapters:
                raise BootstrapError(f"model-routing adapter is missing: {adapter_root}")
            continue
        for relative in MODEL_ROUTING_ADAPTER_FILES[adapter]:
            candidate = adapter_root / relative
            if has_symlink_component(adapter_root, relative):
                raise BootstrapError(f"adapter source contains a symlink: {candidate}")
            if candidate.is_file():
                files[relative] = candidate
            elif require_adapters:
                raise BootstrapError(f"adapter file is missing: {candidate}")
    return files


def recorded_baseline_ref(target: Path) -> str:
    ai_path = target / "zettelkasten/AI.md"
    if has_symlink_component(target, Path("zettelkasten/AI.md")):
        raise BootstrapError(f"cannot read baseline through a symlink: {ai_path}")
    try:
        text = ai_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise BootstrapError(
            "cannot read the template baseline from zettelkasten/AI.md; "
            "pass --baseline-ref explicitly"
        ) from exc
    match = BASELINE_PATTERN.search(text)
    if match is None or not match.group(1).strip():
        raise BootstrapError(
            "zettelkasten/AI.md does not contain a Template baseline. "
            "The line is a machine-parsed contract and must keep its literal "
            "prefix, for example: Template baseline: `v4.4.0` "
            "(`canonical-payload-v4`). Restore that prefix, or pass "
            "--baseline-ref explicitly for this run."
        )
    return match.group(1).strip()


def read_project_file(target: Path, relative: Path) -> ProjectFile:
    candidate = target / relative
    if has_symlink_component(target, relative):
        return ProjectFile("unsafe", None)
    if not candidate.exists():
        return ProjectFile("absent", None)
    if not candidate.is_file():
        return ProjectFile("unsafe", None)
    try:
        return ProjectFile("present", candidate.read_bytes())
    except OSError:
        return ProjectFile("unreadable", None)


def content_diff(
    before: bytes | None,
    after: bytes | None,
    *,
    before_label: str,
    after_label: str,
) -> str:
    if before == after:
        return ""
    before_lines = (
        before.decode("utf-8", errors="replace").splitlines(keepends=True)
        if before is not None
        else []
    )
    after_lines = (
        after.decode("utf-8", errors="replace").splitlines(keepends=True)
        if after is not None
        else []
    )
    return "".join(
        difflib.unified_diff(
            before_lines,
            after_lines,
            fromfile=before_label if before is not None else "/dev/null",
            tofile=after_label if after is not None else "/dev/null",
        )
    )


def classify_upgrade(
    relative: Path,
    baseline: bytes | None,
    local: ProjectFile,
    upstream: bytes | None,
    *,
    baseline_label: str,
    target_label: str,
) -> UpgradeEntry:
    if local.state not in {"present", "absent"}:
        category = "both-modified"
    elif baseline is None and upstream is not None:
        if local.state == "absent":
            category = "added"
        elif local.content == upstream:
            category = "unchanged"
        else:
            category = "both-modified"
    elif baseline is not None and upstream is None:
        if local.state == "absent":
            category = "unchanged"
        elif local.content == baseline:
            category = "upstream-modified"
        else:
            category = "both-modified"
    elif baseline is None and upstream is None:
        category = "local-modified" if local.state == "present" else "unchanged"
    elif local.state == "absent":
        category = "local-modified" if upstream == baseline else "both-modified"
    elif local.content == upstream:
        category = "unchanged"
    elif local.content == baseline:
        category = "upstream-modified" if upstream != baseline else "unchanged"
    elif upstream == baseline:
        category = "local-modified"
    else:
        category = "both-modified"

    if baseline is None:
        baseline_state = "absent"
    else:
        baseline_state = "present"

    if local.state != "present":
        local_state = local.state
    elif baseline is None:
        local_state = "matches-target" if local.content == upstream else "present"
    elif local.content == baseline:
        local_state = "unchanged"
    elif local.content == upstream:
        local_state = "matches-target"
    else:
        local_state = "modified"

    if upstream is None:
        upstream_state = "absent" if baseline is None else "removed"
    elif baseline is None:
        upstream_state = "added"
    elif upstream == baseline:
        upstream_state = "unchanged"
    else:
        upstream_state = "modified"

    path_text = relative.as_posix()
    return UpgradeEntry(
        path=relative,
        category=category,
        baseline_state=baseline_state,
        local_state=local_state,
        upstream_state=upstream_state,
        local_diff=(
            content_diff(
                baseline,
                local.content if local.state == "present" else None,
                before_label=f"{baseline_label}/{path_text}",
                after_label=f"project/{path_text}",
            )
            if local.state in {"present", "absent"}
            else ""
        ),
        upstream_diff=content_diff(
            baseline,
            upstream,
            before_label=f"{baseline_label}/{path_text}",
            after_label=f"{target_label}/{path_text}",
        ),
    )


def build_upgrade_entries(
    baseline_files: dict[Path, Path],
    upstream_files: dict[Path, Path],
    target: Path,
    *,
    baseline_label: str,
    target_label: str,
) -> tuple[UpgradeEntry, ...]:
    paths = sorted(set(baseline_files) | set(upstream_files))
    entries: list[UpgradeEntry] = []
    for relative in paths:
        baseline_path = baseline_files.get(relative)
        upstream_path = upstream_files.get(relative)
        baseline = baseline_path.read_bytes() if baseline_path is not None else None
        upstream = upstream_path.read_bytes() if upstream_path is not None else None
        entries.append(
            classify_upgrade(
                relative,
                baseline,
                read_project_file(target, relative),
                upstream,
                baseline_label=baseline_label,
                target_label=target_label,
            )
        )
    return tuple(entries)


def print_upgrade_report(
    target: Path,
    baseline_ref: str,
    target_ref: str,
    entries: tuple[UpgradeEntry, ...],
    *,
    as_json: bool,
) -> None:
    counts = {
        category: sum(entry.category == category for entry in entries)
        for category in UPGRADE_CATEGORIES
    }
    if as_json:
        print(
            json.dumps(
                {
                    "read_only": True,
                    "target": str(target),
                    "baseline_ref": baseline_ref,
                    "target_ref": target_ref,
                    "summary": counts,
                    "files": [
                        {
                            "path": entry.path.as_posix(),
                            "category": entry.category,
                            "baseline_state": entry.baseline_state,
                            "local_state": entry.local_state,
                            "upstream_state": entry.upstream_state,
                            "local_diff": entry.local_diff,
                            "upstream_diff": entry.upstream_diff,
                        }
                        for entry in entries
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    print("Repo Continuity upgrade report (read-only)")
    print(f"Target: {target}")
    print(f"Baseline: {baseline_ref}")
    print(f"Target release: {target_ref}")
    print("Summary:")
    for category in UPGRADE_CATEGORIES:
        print(f"  {category}: {counts[category]}")
    for category in UPGRADE_CATEGORIES:
        matching = [entry for entry in entries if entry.category == category]
        if not matching:
            continue
        print(f"\n[{category}]")
        for entry in matching:
            print(
                f"  {entry.path} "
                f"(local={entry.local_state}, upstream={entry.upstream_state})"
            )
    changed = [
        entry
        for entry in entries
        if entry.local_diff or entry.upstream_diff
    ]
    if changed:
        print("\nDiffs:")
        for entry in changed:
            if entry.local_diff:
                print(f"\n# Local versus baseline: {entry.path}")
                print(entry.local_diff, end="" if entry.local_diff.endswith("\n") else "\n")
            if entry.upstream_diff:
                print(f"\n# Target upstream versus baseline: {entry.path}")
                print(entry.upstream_diff, end="" if entry.upstream_diff.endswith("\n") else "\n")
    print(
        "\nNo files were changed. Preview safe reconciliation with "
        "--upgrade-apply --dry-run."
    )


def merge_upgrade_content(
    local: bytes,
    baseline: bytes,
    upstream: bytes,
) -> bytes | None:
    if any(b"\0" in content for content in (local, baseline, upstream)):
        return None
    try:
        for content in (local, baseline, upstream):
            content.decode("utf-8")
    except UnicodeDecodeError:
        return None

    with tempfile.TemporaryDirectory(prefix="repo-continuity-merge-") as temp_dir:
        temporary = Path(temp_dir)
        local_path = temporary / "local"
        baseline_path = temporary / "baseline"
        upstream_path = temporary / "upstream"
        local_path.write_bytes(local)
        baseline_path.write_bytes(baseline)
        upstream_path.write_bytes(upstream)
        try:
            result = subprocess.run(
                [
                    "git",
                    "merge-file",
                    "--stdout",
                    str(local_path),
                    str(baseline_path),
                    str(upstream_path),
                ],
                check=False,
                capture_output=True,
            )
        except FileNotFoundError as exc:
            raise BootstrapError("git is required to apply a three-way upgrade") from exc
    if result.returncode == 0:
        return result.stdout
    if 0 < result.returncode < 128:
        return None
    message = result.stderr.decode("utf-8", errors="replace").strip()
    raise BootstrapError(f"git merge-file failed: {message or result.returncode}")


def preserve_baseline_gate(
    relative: Path,
    content: bytes | None,
    local: ProjectFile,
) -> bytes | None:
    if (
        relative != Path("zettelkasten/AI.md")
        or content is None
        or local.state != "present"
        or local.content is None
    ):
        return content
    try:
        local_text = local.content.decode("utf-8")
        target_text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise BootstrapError("zettelkasten/AI.md must remain UTF-8 text") from exc
    local_match = BASELINE_PATTERN.search(local_text)
    target_match = BASELINE_PATTERN.search(target_text)
    if local_match is None or target_match is None:
        raise BootstrapError(
            "cannot preserve the Template baseline gate in zettelkasten/AI.md"
        )
    preserved = (
        target_text[: target_match.start(1)]
        + local_match.group(1)
        + target_text[target_match.end(1) :]
    )
    return preserved.encode("utf-8")


def build_upgrade_actions(
    entries: tuple[UpgradeEntry, ...],
    baseline_files: dict[Path, Path],
    upstream_files: dict[Path, Path],
    target: Path,
) -> tuple[UpgradeAction, ...]:
    actions: list[UpgradeAction] = []
    for entry in entries:
        relative = entry.path
        baseline_path = baseline_files.get(relative)
        upstream_path = upstream_files.get(relative)
        baseline = baseline_path.read_bytes() if baseline_path is not None else None
        upstream = upstream_path.read_bytes() if upstream_path is not None else None
        local = read_project_file(target, relative)

        if entry.category == "unchanged":
            action = "unchanged"
            content = None
        elif entry.category == "local-modified":
            action = "preserve-local"
            content = None
        elif entry.category == "added":
            action = "add-upstream"
            content = upstream
        elif entry.category == "upstream-modified" and upstream is not None:
            action = "apply-upstream"
            content = upstream
        elif entry.category == "upstream-modified":
            action = "pending-removal"
            content = None
        elif (
            local.state == "present"
            and local.content is not None
            and baseline is not None
            and upstream is not None
        ):
            content = merge_upgrade_content(local.content, baseline, upstream)
            action = "merge-clean" if content is not None else "conflict"
        else:
            action = "conflict"
            content = None
        content = preserve_baseline_gate(relative, content, local)
        actions.append(UpgradeAction(relative, entry.category, action, content))
    return tuple(actions)


def ensure_upgrade_target_ready(target: Path) -> None:
    try:
        root_result = subprocess.run(
            ["git", "-C", str(target), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
        branch_result = subprocess.run(
            ["git", "-C", str(target), "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
        )
        status_result = subprocess.run(
            ["git", "-C", str(target), "status", "--porcelain"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise BootstrapError("git is required to apply an upgrade") from exc
    except subprocess.CalledProcessError as exc:
        raise BootstrapError(
            "--upgrade-apply requires the target to be a Git repository"
        ) from exc

    repository_root = Path(root_result.stdout.strip()).resolve()
    if repository_root != target:
        raise BootstrapError(
            "--upgrade-apply target must be the Git repository root: "
            f"{repository_root}"
        )
    branch = branch_result.stdout.strip()
    if not branch:
        raise BootstrapError("--upgrade-apply requires a named task branch")
    if branch in {"main", "master"}:
        raise BootstrapError(
            "--upgrade-apply refuses the default branch; create an upgrade task "
            "branch first"
        )
    if status_result.stdout:
        raise BootstrapError(
            "--upgrade-apply requires a clean worktree; commit the upgrade WORK "
            "checkpoint before applying changes"
        )


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".upgrade", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
        if path.exists():
            shutil.copymode(path, temporary)
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def apply_upgrade_actions(
    target: Path,
    actions: tuple[UpgradeAction, ...],
) -> None:
    writable = tuple(action for action in actions if action.content is not None)
    originals = {
        action.path: read_project_file(target, action.path)
        for action in writable
    }
    completed: list[UpgradeAction] = []
    try:
        for action in writable:
            if has_symlink_component(target, action.path):
                raise BootstrapError(
                    f"upgrade target became unsafe before write: {target / action.path}"
                )
            atomic_write(target / action.path, action.content or b"")
            completed.append(action)
    except BaseException:
        for action in reversed(completed):
            original = originals[action.path]
            destination = target / action.path
            if original.state == "present" and original.content is not None:
                atomic_write(destination, original.content)
            elif original.state == "absent":
                destination.unlink(missing_ok=True)
        raise


def print_upgrade_apply_result(
    target: Path,
    baseline_ref: str,
    target_ref: str,
    actions: tuple[UpgradeAction, ...],
    *,
    dry_run: bool,
    as_json: bool,
) -> None:
    action_names = (
        "add-upstream",
        "apply-upstream",
        "merge-clean",
        "preserve-local",
        "unchanged",
        "pending-removal",
        "conflict",
    )
    counts = {
        action: sum(item.action == action for item in actions)
        for action in action_names
    }
    blocked = counts["pending-removal"] + counts["conflict"]
    if as_json:
        print(
            json.dumps(
                {
                    "dry_run": dry_run,
                    "target": str(target),
                    "baseline_ref": baseline_ref,
                    "target_ref": target_ref,
                    "summary": counts,
                    "blocked": blocked,
                    "baseline_updated": False,
                    "files": [
                        {
                            "path": item.path.as_posix(),
                            "category": item.category,
                            "action": item.action,
                        }
                        for item in actions
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    heading = (
        "Repo Continuity upgrade preview"
        if dry_run
        else "Repo Continuity upgrade result"
    )
    print(heading)
    print(f"Target: {target}")
    print(f"Baseline: {baseline_ref}")
    print(f"Target release: {target_ref}")
    print("Summary:")
    for action in action_names:
        print(f"  {action}: {counts[action]}")
    for item in actions:
        if item.action in {"pending-removal", "conflict"}:
            print(f"  {item.action}: {item.path}")
    if dry_run:
        print("\nNo files were changed. Rerun without --dry-run to apply safe changes.")
    elif blocked:
        print(
            "\nSafe changes were applied. Resolve each pending removal or conflict, "
            "then validate the project."
        )
    else:
        print("\nAll conflict-free changes were applied. Validate the project.")
    print(
        f"After review and validation, record Template baseline `{target_ref}` in "
        "zettelkasten/AI.md. The helper never advances that gate automatically."
    )


def resolve_adapters_root(source: Path, payload: Path) -> Path:
    candidates = (source / "adapters", payload.parent / "adapters")
    for candidate in candidates:
        if candidate.is_dir():
            return candidate.resolve()
    raise BootstrapError(
        "model-routing adapters are unavailable from this source; use the "
        "canonical repository checkout or omit --with-model-routing"
    )


def validate_adapter_source(adapters_root: Path, adapter: str) -> Path:
    adapter_root = adapters_root / adapter
    if not adapter_root.is_dir():
        raise BootstrapError(f"model-routing adapter is missing: {adapter_root}")
    if adapter_root.is_symlink():
        raise BootstrapError(f"model-routing adapter is a symlink: {adapter_root}")
    for relative in MODEL_ROUTING_ADAPTER_FILES[adapter]:
        candidate = adapter_root / relative
        if has_symlink_component(adapter_root, relative):
            raise BootstrapError(f"adapter source contains a symlink: {candidate}")
        if not candidate.is_file():
            raise BootstrapError(f"adapter file is missing: {candidate}")
    return adapter_root


def has_symlink_component(target: Path, relative: Path) -> bool:
    candidate = target
    for part in relative.parts:
        candidate = candidate / part
        if candidate.is_symlink():
            return True
    return False


def build_plan(
    source: Path, target: Path, files: tuple[Path, ...]
) -> InstallPlan:
    missing: list[Path] = []
    identical: list[Path] = []
    conflicts: list[Path] = []

    for relative in files:
        source_file = source / relative
        target_file = target / relative
        if has_symlink_component(target, relative):
            conflicts.append(relative)
        elif not target_file.exists():
            missing.append(relative)
        elif target_file.is_file() and filecmp.cmp(
            source_file, target_file, shallow=False
        ):
            identical.append(relative)
        else:
            conflicts.append(relative)

    return InstallPlan(
        missing=tuple(missing),
        identical=tuple(identical),
        conflicts=tuple(conflicts),
    )


def combine_plans(plans: tuple[InstallPlan, ...]) -> InstallPlan:
    return InstallPlan(
        missing=tuple(path for plan in plans for path in plan.missing),
        identical=tuple(path for plan in plans for path in plan.identical),
        conflicts=tuple(path for plan in plans for path in plan.conflicts),
    )


def apply_plan(
    source: Path, target: Path, plan: InstallPlan, *, dry_run: bool
) -> None:
    if dry_run:
        return
    target.mkdir(parents=True, exist_ok=True)
    for relative in plan.missing:
        source_file = source / relative
        target_file = target / relative
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target_file)


def print_plan(target: Path, plan: InstallPlan, *, dry_run: bool) -> None:
    verb = "Would copy" if dry_run else "Copied"
    print(f"Target: {target}")
    print(f"{verb}: {len(plan.missing)}")
    print(f"Identical: {len(plan.identical)}")
    print(f"Conflicts left untouched: {len(plan.conflicts)}")
    for relative in plan.conflicts:
        print(f"  conflict: {relative}")

    if plan.conflicts:
        print(
            "Next: inspect each conflict, preserve repository-specific content, "
            "and merge the template guidance manually."
        )
    elif dry_run:
        print("Next: rerun without --dry-run to copy the missing template files.")
    else:
        print("Next: follow INIT.md when present, then review the installed files.")


def install_from_source(
    source: Path,
    target: Path,
    adapters: tuple[str, ...],
    *,
    dry_run: bool,
) -> int:
    payload = resolve_payload_root(source)
    components = [(payload, template_files(payload))]
    if adapters:
        adapters_root = resolve_adapters_root(source, payload)
        for adapter in adapters:
            adapter_root = validate_adapter_source(adapters_root, adapter)
            components.append(
                (adapter_root, MODEL_ROUTING_ADAPTER_FILES[adapter])
            )

    plans = tuple(
        build_plan(component_root, target, files)
        for component_root, files in components
    )
    for (component_root, _), plan in zip(components, plans):
        apply_plan(component_root, target, plan, dry_run=dry_run)
    combined = combine_plans(plans)
    print_plan(target, combined, dry_run=dry_run)
    return 2 if combined.conflicts else 0


def install(
    args: argparse.Namespace, target: Path, adapters: tuple[str, ...]
) -> int:
    if args.source:
        source = normalize_directory(args.source, "source", must_exist=True)
        return install_from_source(
            source, target, adapters, dry_run=args.dry_run
        )
    with tempfile.TemporaryDirectory(prefix="repo-continuity-template-") as temp_dir:
        source = clone_source(
            args.repo_url, args.ref, Path(temp_dir) / "template"
        )
        return install_from_source(
            source, target, adapters, dry_run=args.dry_run
        )


def upgrade_operation(
    args: argparse.Namespace,
    target: Path,
    adapters: tuple[str, ...],
    *,
    apply: bool,
) -> int:
    baseline_ref = args.baseline_ref or recorded_baseline_ref(target)
    with tempfile.TemporaryDirectory(prefix="repo-continuity-upgrade-") as temp_dir:
        temporary = Path(temp_dir)
        if args.source:
            upstream_source = normalize_directory(
                args.source, "source", must_exist=True
            )
        else:
            upstream_source = clone_source(
                args.repo_url,
                args.ref,
                temporary / "target-source",
            )
        if args.baseline_source:
            baseline_source = normalize_directory(
                args.baseline_source, "baseline source", must_exist=True
            )
        else:
            baseline_source = clone_source(
                args.repo_url,
                baseline_ref,
                temporary / "baseline-source",
            )

        upstream_payload = resolve_payload_root(upstream_source)
        baseline_payload = resolve_baseline_payload_root(baseline_source)
        upstream_files = report_source_files(
            upstream_source,
            upstream_payload,
            adapters,
            require_adapters=True,
        )
        baseline_files = report_source_files(
            baseline_source,
            baseline_payload,
            adapters,
            require_adapters=False,
        )
        entries = build_upgrade_entries(
            baseline_files,
            upstream_files,
            target,
            baseline_label=f"baseline-{baseline_ref}",
            target_label=f"upstream-{args.ref}",
        )
        if not apply:
            print_upgrade_report(
                target,
                baseline_ref,
                args.ref,
                entries,
                as_json=args.json,
            )
            return 0

        actions = build_upgrade_actions(
            entries,
            baseline_files,
            upstream_files,
            target,
        )
        if not args.dry_run:
            ensure_upgrade_target_ready(target)
            apply_upgrade_actions(target, actions)
        print_upgrade_apply_result(
            target,
            baseline_ref,
            args.ref,
            actions,
            dry_run=args.dry_run,
            as_json=args.json,
        )
        blocked = any(
            action.action in {"pending-removal", "conflict"}
            for action in actions
        )
        return 2 if blocked else 0


def main() -> int:
    args = parse_args()
    try:
        target = normalize_directory(
            args.target,
            "target",
            must_exist=args.upgrade_report or args.upgrade_apply,
        )
        adapters = selected_model_routing(args.with_model_routing)
        if args.upgrade_report:
            return upgrade_operation(args, target, adapters, apply=False)
        if args.upgrade_apply:
            return upgrade_operation(args, target, adapters, apply=True)
        if args.inspect:
            return inspect_target(target, adapters)
        return install(args, target, adapters)
    except BootstrapError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
