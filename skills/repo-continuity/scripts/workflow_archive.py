#!/usr/bin/env python3
"""Archive repository knowledge and maintain small, Markdown-only work routes."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import date
from pathlib import Path


WORK_ROOT = Path("zettelkasten/work")
ACTIVE_ROOT = WORK_ROOT / "active"
ARCHIVE_ROOT = Path("zettelkasten/archive")
ARTIFACT_ID = re.compile(r"^(?:WORK|INITIATIVE)-[0-9]{14}-[a-z0-9][a-z0-9-]*$")
OPEN_STATES = {"backlog", "active", "blocked", "review"}
TERMINAL_STATES = {"done", "cancelled"}
ROUTE_README = "# Open Work Routes\n\nRouting status: ready\n\nEach `*.ref.md` points to one open WORK or Initiative. Status and task state remain in the stable source. See [[knowledge-lifecycle]].\n"


class ArchiveError(RuntimeError):
    """A lifecycle change or scoped lookup cannot be completed safely."""


def safe_path(root: Path, relative: Path | str) -> Path:
    relative = Path(relative)
    if relative.is_absolute() or ".." in relative.parts or not relative.parts:
        raise ArchiveError(f"expected a repository-relative path: {relative}")
    path = root
    for part in relative.parts:
        path = path / part
        if path.is_symlink():
            raise ArchiveError(f"symlink is outside the lifecycle contract: {relative}")
    return path


def stable_artifacts(root: Path) -> list[Path]:
    directory = safe_path(root, WORK_ROOT)
    if not directory.is_dir():
        return []
    return [safe_path(root, p.relative_to(root)) for p in sorted(directory.iterdir())
            if p.suffix == ".md" and ARTIFACT_ID.fullmatch(p.stem)]


def route_path(root: Path, source: Path) -> Path:
    return safe_path(root, ACTIVE_ROOT / f"{source.stem}.ref.md")


def route_text(source: Path, text: str) -> str:
    from workflow_doctor import field_value

    branch = field_value(text, "branch") or "coordination"
    return (f"# {source.stem}\n\nBranch hint: `{branch}`\n\n"
            f"Source: [[work/{source.stem}]]\n\n"
            "Routing only; read the source for authoritative state.\n")


def route_matches(source: Path, text: str, pointer: str) -> bool:
    from workflow_doctor import field_value

    branch = field_value(text, "branch") or "coordination"
    return (f"Branch hint: `{branch}`" in pointer.splitlines()
            and f"Source: [[work/{source.stem}]]" in pointer.splitlines())


def routing_ready(readme: Path) -> bool:
    return readme.is_file() and [line for line in readme.read_text().splitlines()
                                if line.startswith("Routing status:")] == ["Routing status: ready"]


def open_artifacts(root: Path) -> list[Path]:
    directory = safe_path(root, ACTIVE_ROOT)
    readme = safe_path(root, ACTIVE_ROOT / "README.md")
    if not routing_ready(readme):
        raise ArchiveError("open-work routing is missing; run workflow_archive.py reindex --dry-run, review, then reindex (or create the Markdown routes manually)")
    paths: list[Path] = []
    for route in sorted(directory.iterdir()):
        if route.name == "README.md":
            continue
        identifier = route.name.removesuffix(".ref.md")
        if not route.name.endswith(".ref.md") or not ARTIFACT_ID.fullmatch(identifier):
            raise ArchiveError(f"unexpected open-work route: {route.relative_to(root)}")
        safe_path(root, route.relative_to(root))
        if not route.is_file():
            raise ArchiveError(f"open-work route must be a regular file: {route.name}")
        source = safe_path(root, WORK_ROOT / f"{identifier}.md")
        if not source.is_file():
            raise ArchiveError(f"open-work route has no source: {route.relative_to(root)}")
        paths.append(source)
    return paths


def scoped_artifacts(root: Path) -> list[Path]:
    """Open records plus their exact dependency/parent paths; never enumerate history."""
    from workflow_doctor import field_list, field_value, read_text

    result = open_artifacts(root)
    seen = set(result)
    for source in result:
        text = read_text(source)
        if field_value(text, "status") in TERMINAL_STATES:
            continue  # Historical prerequisites belong to a full audit, not daily resume.
        ids = list(field_list(text, "depends_on"))
        parent = field_value(text, "initiative_id") if source.stem.startswith("WORK-") else None
        if parent:
            ids.append(parent)
        for identifier in ids:
            if not ARTIFACT_ID.fullmatch(identifier):
                continue  # The structural validator reports the invalid reference.
            path = safe_path(root, WORK_ROOT / f"{identifier}.md")
            if path.is_file() and path not in seen:
                seen.add(path)
                result.append(path)
    return result


def apply_changes(root: Path, changes: dict[Path, bytes | None], dry_run: bool) -> None:
    """Preflight every path, use atomic replacements, and roll back on write failure."""
    previous: dict[Path, bytes | None] = {}
    for path in changes:
        safe_path(root, path.relative_to(root))
        if path.exists() and not path.is_file():
            raise ArchiveError(f"expected a regular file: {path.relative_to(root)}")
        previous[path] = path.read_bytes() if path.exists() else None
    if dry_run:
        return
    touched: list[Path] = []
    try:
        for path, content in changes.items():
            if content == previous[path]:
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            touched.append(path)
            if content is None:
                path.unlink(missing_ok=True)
            else:
                temporary = path.with_name(path.name + ".lifecycle-tmp")
                if temporary.exists() or temporary.is_symlink():
                    raise ArchiveError(f"temporary lifecycle file already exists: {temporary}")
                try:
                    with temporary.open("xb") as stream:
                        stream.write(content)
                    os.replace(temporary, path)
                finally:
                    temporary.unlink(missing_ok=True)
    except (OSError, ArchiveError):
        for path in reversed(touched):
            if previous[path] is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(previous[path])
        raise


def write_artifact(root: Path, source: Path, text: str) -> None:
    from workflow_doctor import field_value

    readme = safe_path(root, ACTIVE_ROOT / "README.md")
    if not routing_ready(readme):
        raise ArchiveError("open-work routing is missing; review workflow_archive.py reindex --dry-run before updating work")
    route = route_path(root, source)
    pointer = route_text(source, text).encode() if field_value(text, "status") in OPEN_STATES else None
    apply_changes(root, {source: text.encode(), route: pointer}, False)


def archive_target(root: Path, value: str) -> Path:
    relative = WORK_ROOT / f"{value}.md" if ARTIFACT_ID.fullmatch(value) else Path(value)
    path = safe_path(root, relative)
    if not path.is_file() or path.suffix != ".md":
        raise ArchiveError("archive target must be an existing Markdown file")
    if relative.parts[0] != "zettelkasten" or any(part in {"archive", "active", "templates"} for part in relative.parts[1:]):
        raise ArchiveError("archive only stable work records or retired knowledge notes under zettelkasten")
    if path.name in {"README.md", "AI.md", "knowledge-lifecycle.md", "workflow.md", "git-collaboration.md", "skill-lifecycle.md", "validation-policy.md"}:
        raise ArchiveError("required navigation and workflow contracts cannot be archived")
    return path


def archive_reference(root: Path, text: str) -> Path:
    from workflow_doctor import field_value

    ref = field_value(text, "archive_ref") or ""
    if not ref.startswith(ARCHIVE_ROOT.as_posix() + "/"):
        raise ArchiveError("archive_ref must name a file under zettelkasten/archive")
    path = safe_path(root, ref)
    if not path.is_file():
        raise ArchiveError(f"archive snapshot is missing: {ref}")
    return path


def validate_terminal_evidence(source: Path, text: str) -> None:
    """Validate the record being compacted without reading unrelated historical work."""
    from workflow_doctor import (EXPERIENCE_DECISIONS, WORK_REQUIRED_SECTIONS,
                                 INITIATIVE_REQUIRED_SECTIONS, experience_candidate_rows,
                                 field_value, find_heading, has_pending_governed_gate,
                                 has_pending_initiative_gate, PROMOTION_COMPLETE_RE,
                                 section_body)

    kind = "work_id" if source.stem.startswith("WORK-") else "initiative_id"
    if field_value(text, kind) != source.stem:
        raise ArchiveError(f"{kind} must match the stable source filename")
    if field_value(text, "status") not in TERMINAL_STATES:
        raise ArchiveError("only done or cancelled work can be archived")
    sections = WORK_REQUIRED_SECTIONS if kind == "work_id" else INITIATIVE_REQUIRED_SECTIONS
    if any(find_heading(text, heading) is None for heading in sections):
        raise ArchiveError("complete required work sections before archival")
    if kind == "work_id":
        if field_value(text, "route") not in {"tracked", "governed"}:
            raise ArchiveError("WORK route must be tracked or governed")
        rows = experience_candidate_rows(text)
        if not PROMOTION_COMPLETE_RE.search(text) or not rows or any(
            cells[2].strip().lower() not in EXPERIENCE_DECISIONS - {"pending"}
            or not cells[0].strip() or not cells[4].strip()
            or (cells[2].strip().lower() in {"promoted", "updated", "no-op"} and not cells[3].strip())
            for cells in rows
        ):
            raise ArchiveError("finish the Learning Check and decide every candidate before archival")
        if field_value(text, "route") == "governed" and has_pending_governed_gate(text):
            raise ArchiveError("resolve or explicitly waive pending governed gates before archival")
        if not re.search(r"^- Integration result:[ \t]*\S.*$", section_body(text, "Closure"), re.MULTILINE):
            raise ArchiveError("record the integration result or cancellation disposition before archival")
        if field_value(text, "status") == "done":
            for label in ("Acceptance complete", "Required gates closed", "Durable writeback complete"):
                if not re.search(rf"^- {label}: yes\s*$", section_body(text, "Closure"), re.MULTILINE | re.IGNORECASE):
                    raise ArchiveError(f"closed work is missing {label}: yes")
            acceptance = section_body(text, "Goal And Acceptance")
            if re.search(r"^- \[ \]", acceptance, re.MULTILINE):
                raise ArchiveError("resolve unchecked acceptance criteria before archival")
    else:
        if has_pending_initiative_gate(text):
            raise ArchiveError("resolve pending shared gates before archival")
        if not re.search(r"^- Final outcome:[ \t]*\S.*$", section_body(text, "Integration And Closure"), re.MULTILINE):
            raise ArchiveError("record the Initiative final outcome or cancellation disposition")
        if field_value(text, "status") == "done" and re.search(r"^- \[ \]", section_body(text, "Overall Acceptance"), re.MULTILINE):
            raise ArchiveError("resolve unchecked overall acceptance before archival")


def archive_plan(root: Path, source: Path, summary: str, reason: str) -> dict[Path, bytes | None]:
    from workflow_doctor import field_value, strip_code
    from workflow_task import FRONTMATTER_RE, set_frontmatter_field

    original = source.read_bytes()
    text = original.decode("utf-8")
    if field_value(text, "archive_ref"):
        snapshot = archive_reference(root, text)
        if hashlib.sha256(snapshot.read_bytes()).hexdigest() != field_value(text, "archive_sha256"):
            raise ArchiveError("archive checksum mismatch")
        return {}  # Repeating archive never creates another snapshot.
    if not summary.strip() or not reason.strip():
        raise ArchiveError("archive needs a concise outcome summary and a reason")
    status = field_value(text, "status")
    is_work = source.parent == root / WORK_ROOT and ARTIFACT_ID.fullmatch(source.stem)
    if source.parent == root / WORK_ROOT and not is_work:
        raise ArchiveError("work records must have a valid stable WORK or Initiative ID")
    if is_work:
        validate_terminal_evidence(source, text)
        if source.stem.startswith("INITIATIVE-"):
            from workflow_doctor import check_artifacts

            findings = []
            check_artifacts(root, findings, full=True)
            errors = [item.message for item in findings if item.severity == "ERROR" and item.path == source.relative_to(root)]
            if errors:
                raise ArchiveError("resolve Initiative children, acceptance, and shared gates before archival: " + "; ".join(errors))
            for child in stable_artifacts(root):
                if child.stem.startswith("WORK-"):
                    child_text = child.read_text()
                    if field_value(child_text, "initiative_id") == source.stem and field_value(child_text, "status") not in TERMINAL_STATES:
                        raise ArchiveError("an Initiative with open children cannot be archived")
    elif status not in {"superseded", "deprecated", "retired"}:
        raise ArchiveError("knowledge must be superseded, deprecated, or retired after useful facts are promoted")
    digest = hashlib.sha256(original).hexdigest()
    relative = source.relative_to(root / "zettelkasten").with_suffix("")
    snapshot = safe_path(root, ARCHIVE_ROOT / relative / f"{digest}.md")
    if snapshot.exists() and snapshot.read_bytes() != original:
        raise ArchiveError("existing archive snapshot differs; refusing to overwrite evidence")
    for key, value in {
        "archive_ref": snapshot.relative_to(root).as_posix(),
        "archive_sha256": digest,
        "archived_at": date.today().isoformat(),
        "archive_summary": summary,
        "archive_reason": reason,
    }.items():
        text = set_frontmatter_field(text, key, value)
    header = text[:text.index("\n---", 4) + 5]
    title = field_value(text, "title") or source.stem
    snapshot_link = os.path.relpath(snapshot, source.parent).replace(os.sep, "/")
    # Preserve existing heading anchors so section links still land at the stable path.
    original_text = original.decode()
    original_header = FRONTMATTER_RE.match(original_text)
    anchors = re.findall(r"^#{1,6} .+$", strip_code(original_text[original_header.end():]), re.MULTILINE)
    first_heading = anchors[0] if anchors else f"# {title}"
    body = (f"\n{first_heading}\n\n**Archive summary**\n\n{summary.strip()}\n\n"
            f"Reason: {reason.strip()}\n\n"
            f"Historical evidence: [original record]({snapshot_link}). Read it only for an explicit historical question or a full audit.\n\n"
            "The frontmatter here remains authoritative for identity, status, parent, and dependencies. The snapshot is historical evidence.\n")
    for heading in anchors[1:]:
        body += f"\n{heading}\n\nSee the historical evidence linked above.\n"
    changes: dict[Path, bytes | None] = {snapshot: original, source: (header + body).encode()}
    if is_work:
        changes[route_path(root, source)] = None
    return changes


def reindex_plan(root: Path) -> dict[Path, bytes | None]:
    from workflow_doctor import field_value

    directory = safe_path(root, ACTIVE_ROOT)
    changes: dict[Path, bytes | None] = {}
    readme = safe_path(root, ACTIVE_ROOT / "README.md")
    readme_text = readme.read_text() if readme.exists() else ROUTE_README
    status_lines = re.findall(r"^Routing status:.*$", readme_text, re.MULTILINE)
    if len(status_lines) > 1:
        raise ArchiveError("resolve duplicate routing status declarations before reindexing")
    if status_lines:
        readme_text = readme_text.replace(status_lines[0], "Routing status: ready", 1)
    else:
        readme_text += "\nRouting status: ready\n"
    desired: set[Path] = set()
    for source in safe_path(root, WORK_ROOT).iterdir():
        if source.is_file() and source.name not in {"README.md", ".gitkeep"} and (source.suffix != ".md" or not ARTIFACT_ID.fullmatch(source.stem)):
            raise ArchiveError(f"resolve unexpected work artifact before reindexing: {source.name}")
    for source in stable_artifacts(root):
        text = source.read_text()
        status = field_value(text, "status")
        if status not in OPEN_STATES | TERMINAL_STATES:
            raise ArchiveError(f"resolve invalid status before reindexing: {source.name}")
        if status in OPEN_STATES:
            if field_value(text, "archive_ref"):
                raise ArchiveError(f"restore archived content before reopening: {source.name}")
            pointer = route_path(root, source)
            desired.add(pointer)
            changes[pointer] = route_text(source, text).encode()
    if directory.is_dir():
        for path in directory.iterdir():
            if path.name == "README.md":
                continue
            if not path.name.endswith(".ref.md") or not ARTIFACT_ID.fullmatch(path.name.removesuffix(".ref.md")):
                raise ArchiveError(f"unexpected route file; preserve and resolve manually: {path.name}")
            if path not in desired:
                changes[path] = None
    # Publish readiness last, after all routes have been written successfully.
    changes[readme] = readme_text.encode()
    return changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("archive", "restore", "reindex"):
        sub = commands.add_parser(command)
        if command != "reindex":
            sub.add_argument("target", help="WORK/Initiative ID or repository-relative note path")
        if command == "archive":
            sub.add_argument("--summary", required=True)
            sub.add_argument("--reason", required=True)
        sub.add_argument("--root", type=Path, default=Path.cwd())
        sub.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        from workflow_task import current_branch, repository_root
        from workflow_doctor import field_value

        root = repository_root(args.root)
        if not args.dry_run and current_branch(root) in {"main", "master"}:
            raise ArchiveError("use a task branch for lifecycle changes")
        if args.command == "reindex":
            changes = reindex_plan(root)
        else:
            source = archive_target(root, args.target)
            if args.command == "archive":
                changes = archive_plan(root, source, args.summary, args.reason)
            else:
                text = source.read_text()
                snapshot = archive_reference(root, text)
                original = snapshot.read_bytes()
                if hashlib.sha256(original).hexdigest() != field_value(text, "archive_sha256"):
                    raise ArchiveError("archive checksum mismatch; refusing to restore")
                changes = {source: original}
                # Restoring content preserves its terminal/retired state. Reopening is separate.
        actual = {path: data for path, data in changes.items()
                  if (path.read_bytes() if path.is_file() else None) != data}
        apply_changes(root, actual, args.dry_run)
        print(json.dumps({"command": args.command, "dry_run": args.dry_run,
                          "changes": {p.relative_to(root).as_posix(): "remove" if data is None else "write"
                                      for p, data in actual.items()}}, indent=2))
        return 0
    except (ArchiveError, OSError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
