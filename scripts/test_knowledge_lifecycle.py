#!/usr/bin/env python3
"""Exercise archival in bootstrapped projects; instrument I/O, not just output filters."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/repo-continuity/scripts"
sys.path.insert(0, str(SCRIPTS))
import workflow_archive as archive
import workflow_doctor as doctor
import workflow_task as task


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="repo-continuity-lifecycle-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "project"
        self.call("bootstrap_template.py", "--source", str(ROOT), "--target", str(self.root), root=ROOT)
        replacements = {
            "{{PROJECT_NAME}}": "ExampleSaaS", "{{PROJECT_DESCRIPTION}}": "Fictional lifecycle fixture",
            "{{TECH_STACK}}": "Python", "{{DOMAINS}}": "Local only", "{{REPOS}}": "ExampleSaaS",
            "YYYY-MM-DD": date.today().isoformat(), "Routing status: pending": "Routing status: ready",
        }
        for path in (self.root / "zettelkasten").rglob("*.md"):
            text = path.read_text()
            for old, new in replacements.items():
                text = text.replace(old, new)
            path.write_text(text)
        (self.root / "INIT.md").unlink()
        (self.root / ".repo-continuity-template").unlink()
        self.git("init", "--initial-branch", "main")
        self.git("add", ".")
        self.git("-c", "user.name=Validator", "-c", "user.email=validator@example.invalid", "commit", "-m", "test: initialize")
        self.git("switch", "-c", "task/lifecycle")

    def git(self, *args):
        result = subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def call(self, script, *args, expected=0, root=None):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run([sys.executable, "-B", str(SCRIPTS / script), *args],
                                cwd=root or self.root, capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def make_work(self, slug="finished", *, close=True, route="tracked"):
        identifier = f"WORK-20260905120000-{slug}"
        self.call("workflow_task.py", "new", slug, "--id", identifier, "--route", route,
                  "--owned-path", f"src/{slug}")
        path = self.root / archive.WORK_ROOT / f"{identifier}.md"
        text = path.read_text().replace("- [ ] Criterion 1", "- [x] Criterion 1").replace("- [ ] Criterion 2", "- [x] Criterion 2")
        text += "\n## Investigation Detail\n\n" + ("Historical experiment already superseded.\n" * 150)
        archive.write_artifact(self.root, path, text)
        if close:
            self.call("workflow_task.py", "learn-none", identifier, "--reason", "No additional reusable lesson")
            if route == "governed":
                text = path.read_text().replace("|  |  |  | pending |", "| Review | owner | evidence | approved |")
                archive.write_artifact(self.root, path, text)
            self.call("workflow_task.py", "close", identifier, "--acceptance-complete", "--gates-closed",
                      "--promotion-complete", "--writeback-complete", "--integration-result", "Verified fixture")
        return path

    def archive(self, path, *args, expected=0):
        return self.call("workflow_archive.py", "archive", str(path.relative_to(self.root)),
                         "--summary", "Completed; current constraints remain in architecture.md",
                         "--reason", "Historical experiments are no longer needed for routine work",
                         *args, expected=expected)

    def snapshot(self, path):
        return self.root / doctor.field_value(path.read_text(), "archive_ref")

    def check(self, full=False):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code = doctor.run_checks(argparse.Namespace(root=self.root, full=full, strict=True,
                                                        status=False, all_worktrees=False, json=False))
        return code, output.getvalue()

    def test_round_trip_dry_run_idempotence_and_stable_anchors(self):
        path = self.make_work()
        original = path.read_bytes()
        self.assertFalse(archive.route_path(self.root, path).exists())
        before = self.git("status", "--porcelain").stdout
        self.archive(path, "--dry-run")
        self.assertEqual(original, path.read_bytes())
        self.assertEqual(before, self.git("status", "--porcelain").stdout)
        self.archive(path)
        snapshot = self.snapshot(path)
        self.assertEqual(original, snapshot.read_bytes())
        self.assertEqual(hashlib.sha256(original).hexdigest(), doctor.field_value(path.read_text(), "archive_sha256"))
        self.assertLess(len(path.read_bytes()), len(original))
        self.assertIn("## Investigation Detail", path.read_text())
        self.assertIn("status: \"done\"", path.read_text())
        archived = path.read_bytes()
        self.archive(path)
        self.assertEqual(archived, path.read_bytes())
        self.assertEqual(self.check(full=True)[0], 0, self.check(full=True)[1])
        self.call("workflow_archive.py", "restore", path.stem, "--dry-run")
        self.assertEqual(archived, path.read_bytes())
        self.call("workflow_archive.py", "restore", path.stem)
        self.assertEqual(original, path.read_bytes())
        self.assertTrue(snapshot.exists())
        self.assertFalse(archive.route_path(self.root, path).exists())

    def test_default_discovery_and_validation_never_open_history(self):
        historical = self.make_work("old")
        self.archive(historical)
        snapshot = self.snapshot(historical)
        current = self.make_work("current", close=False)
        unrelated = self.root / archive.WORK_ROOT / "WORK-20260904120000-unrelated.md"
        unrelated.write_text("Historical body must never be opened by default.\n" * 100)
        original_text, original_bytes, original_iterdir = Path.read_text, Path.read_bytes, Path.iterdir

        def guard(path):
            if path in {historical, unrelated, snapshot} or path.is_relative_to(self.root / archive.ARCHIVE_ROOT):
                raise AssertionError(f"default path read history: {path}")

        def read_text(path, *args, **kwargs):
            guard(path)
            return original_text(path, *args, **kwargs)

        def read_bytes(path, *args, **kwargs):
            guard(path)
            return original_bytes(path, *args, **kwargs)

        def iterdir(path):
            if path == self.root / archive.WORK_ROOT or path.is_relative_to(self.root / archive.ARCHIVE_ROOT):
                raise AssertionError(f"default path enumerated historical storage: {path}")
            return original_iterdir(path)

        with patch.object(Path, "read_text", read_text), patch.object(Path, "read_bytes", read_bytes), patch.object(Path, "iterdir", iterdir):
            result = doctor.status_payload(self.root, False)
            self.assertEqual([row["work_id"] for row in result["active_work"]], [current.stem])
            code, output = self.check()
            self.assertEqual(code, 0, output)

    def test_exact_archived_dependency_uses_summary_without_snapshot(self):
        dependency = self.make_work("dependency")
        self.archive(dependency)
        current = self.make_work("dependent", close=False)
        text = task.set_frontmatter_field(current.read_text(), "depends_on", [dependency.stem])
        archive.write_artifact(self.root, current, text)
        original = Path.read_bytes

        def read_bytes(path, *args, **kwargs):
            self.assertFalse(path.is_relative_to(self.root / archive.ARCHIVE_ROOT), "dependency loaded archive body")
            return original(path, *args, **kwargs)

        with patch.object(Path, "read_bytes", read_bytes):
            code, output = self.check()
            self.assertEqual(code, 0, output)
        self.snapshot(dependency).write_text("tampered")
        code, output = self.check(full=True)
        self.assertEqual(code, 1)
        self.assertIn("archive checksum mismatch", output)
        original_summary = dependency.read_bytes()
        self.call("workflow_archive.py", "restore", dependency.stem, expected=1)
        self.assertEqual(dependency.read_bytes(), original_summary)

    def test_active_and_unresolved_work_cannot_be_archived(self):
        path = self.make_work(close=False)
        original = path.read_bytes()
        self.archive(path, expected=1)
        self.assertEqual(original, path.read_bytes())
        path.write_text(task.set_frontmatter_field(path.read_text(), "status", "cancelled"))
        result = self.archive(path, expected=1)
        self.assertIn("Learning Check", result.stderr)

    def test_pending_governed_gate_cannot_be_hidden(self):
        path = self.make_work(route="governed")
        text = path.read_text().replace("| Review | owner | evidence | approved |", "| Review | owner | evidence | pending |")
        path.write_text(text)
        result = self.archive(path, expected=1)
        self.assertIn("pending governed gates", result.stderr)

    def test_retired_note_archives_but_current_fact_does_not(self):
        note = self.root / "zettelkasten/old-decision.md"
        note.write_text("---\ntitle: Old decision\nstatus: active\n---\n\n# Old decision\n\n" + "Old details.\n" * 100)
        self.archive(note, expected=1)
        note.write_text(note.read_text().replace("status: active", "status: superseded"))
        original = note.read_bytes()
        self.archive(note)
        self.assertEqual(self.snapshot(note).read_bytes(), original)
        self.assertIn("architecture.md", note.read_text())
        self.call("workflow_archive.py", "restore", str(note.relative_to(self.root)))
        self.assertEqual(note.read_bytes(), original)

    def test_missing_routes_require_explicit_migration(self):
        path = self.make_work(close=False)
        shutil.rmtree(self.root / archive.ACTIVE_ROOT)
        result = self.call("workflow_doctor.py", "--status", expected=1)
        self.assertIn("reindex --dry-run", result.stderr)
        original = path.read_bytes()
        self.call("workflow_archive.py", "reindex", "--dry-run")
        self.assertFalse((self.root / archive.ACTIVE_ROOT).exists())
        self.call("workflow_archive.py", "reindex")
        self.assertEqual(original, path.read_bytes())
        self.assertTrue(archive.route_path(self.root, path).is_file())
        self.call("workflow_doctor.py", "--status")
        self.assertEqual(self.check(full=True)[0], 0, self.check(full=True)[1])

    def test_full_audit_detects_omitted_or_stale_route(self):
        path = self.make_work(close=False)
        route = archive.route_path(self.root, path)
        route.unlink()
        code, output = self.check(full=True)
        self.assertEqual(code, 1)
        self.assertIn("route disagrees", output)
        self.call("workflow_archive.py", "reindex")
        route.write_text(route.read_text().replace("task/lifecycle", "task/stale"))
        code, output = self.check()
        self.assertEqual(code, 1)
        self.assertIn("stale work routing hint", output)

    def test_copied_but_uninitialized_routes_cannot_hide_existing_work(self):
        path = self.make_work(close=False)
        shutil.rmtree(self.root / archive.ACTIVE_ROOT)
        shutil.copytree(ROOT / "template" / archive.ACTIVE_ROOT, self.root / archive.ACTIVE_ROOT)
        result = self.call("workflow_doctor.py", "--status", expected=1)
        self.assertIn("routing is missing", result.stderr)
        self.call("workflow_archive.py", "reindex", "--dry-run")
        self.assertIn("Routing status: pending", (self.root / archive.ACTIVE_ROOT / "README.md").read_text())
        self.call("workflow_archive.py", "reindex")
        self.assertTrue(archive.route_path(self.root, path).exists())
        self.call("workflow_doctor.py", "--status")

    def test_independent_work_routes_do_not_share_a_write_target(self):
        first = self.make_work("one", close=False)
        pointer = archive.route_path(self.root, first)
        before = pointer.read_bytes()
        second = self.make_work("two", close=False)
        self.assertEqual(before, pointer.read_bytes())
        self.assertNotEqual(pointer, archive.route_path(self.root, second))

    def test_symlinks_and_path_escape_are_rejected_without_mutation(self):
        path = self.make_work()
        original = path.read_bytes()
        external = Path(self.temporary.name) / "external"
        external.mkdir()
        shutil.rmtree(self.root / archive.ARCHIVE_ROOT)
        (self.root / archive.ARCHIVE_ROOT).symlink_to(external, target_is_directory=True)
        self.archive(path, expected=1)
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(list(external.iterdir()), [])
        self.call("workflow_archive.py", "archive", "zettelkasten/../AGENTS.md", "--summary", "x", "--reason", "x", expected=1)

    def test_write_failure_restores_source_and_route(self):
        path = self.make_work()
        original = path.read_bytes()
        changes = archive.archive_plan(self.root, path, "Completed", "Historical")
        replace = os.replace

        def fail_source(source, target):
            if target == path:
                raise OSError("injected write failure")
            return replace(source, target)

        with patch.object(os, "replace", fail_source):
            with self.assertRaises(OSError):
                archive.apply_changes(self.root, changes, False)
        self.assertEqual(path.read_bytes(), original)
        self.assertFalse(any(p.exists() for p in changes if p.is_relative_to(self.root / archive.ARCHIVE_ROOT)))

    def test_archived_work_cannot_be_mutated_without_restoring(self):
        path = self.make_work()
        self.archive(path)
        original = path.read_bytes()
        result = self.call("workflow_task.py", "learn-none", path.stem, "--reason", "new lesson", expected=1)
        self.assertIn("restore", result.stderr)
        self.assertEqual(path.read_bytes(), original)

    def test_unchecked_acceptance_cannot_be_hidden_by_closure_flags(self):
        path = self.make_work()
        path.write_text(path.read_text().replace("- [x] Criterion 2", "- [ ] Criterion 2"))
        result = self.archive(path, expected=1)
        self.assertIn("unchecked acceptance", result.stderr)

    def test_repeated_headings_keep_their_original_anchor_order(self):
        note = self.root / "zettelkasten/old-details.md"
        note.write_text("---\ntitle: Old details\nstatus: retired\n---\n\n# Old details\n\n## Detail\n\nOld A\n\n## Detail\n\nOld B\n")
        self.archive(note)
        self.assertEqual(note.read_text().count("\n## Detail\n"), 2)

    def test_cancelled_initiative_cannot_hide_an_open_child(self):
        identifier = "INITIATIVE-20260905120000-migration"
        self.call("workflow_task.py", "initiative-new", "migration", "--id", identifier)
        parent = self.root / archive.WORK_ROOT / f"{identifier}.md"
        child = self.make_work("child", close=False)
        archive.write_artifact(self.root, child, task.set_frontmatter_field(child.read_text(), "initiative_id", identifier))
        text = task.set_frontmatter_field(parent.read_text(), "status", "cancelled")
        text = text.replace("- Final outcome:", "- Final outcome: Cancelled; partial work needs disposition.")
        archive.write_artifact(self.root, parent, text)
        result = self.archive(parent, expected=1)
        self.assertIn("open children", result.stderr)

    def test_terminal_initiative_archives_and_retains_child_membership(self):
        identifier = "INITIATIVE-20260905120000-migration"
        self.call("workflow_task.py", "initiative-new", "migration", "--id", identifier)
        parent = self.root / archive.WORK_ROOT / f"{identifier}.md"
        child = self.make_work("child")
        archive.write_artifact(self.root, child, task.set_frontmatter_field(child.read_text(), "initiative_id", identifier))
        text = task.set_frontmatter_field(parent.read_text(), "status", "done")
        text = text.replace("- [ ]", "- [x]").replace("- Final outcome:", "- Final outcome: Independent child accepted.")
        archive.write_artifact(self.root, parent, text)
        self.archive(parent)
        self.assertFalse(archive.route_path(self.root, parent).exists())
        code, output = self.check(full=True)
        self.assertEqual(code, 0, output)
        payload = doctor.status_payload(self.root, False, full=True)
        self.assertEqual(payload["initiatives"][0]["children"][0]["work_id"], child.stem)

    def test_tampered_evidence_is_rejected_even_on_repeated_archive(self):
        path = self.make_work()
        self.archive(path)
        self.snapshot(path).write_text("tampered")
        result = self.archive(path, expected=1)
        self.assertIn("checksum mismatch", result.stderr)

    def test_main_allows_preview_but_requires_a_task_branch_to_apply(self):
        path = self.make_work()
        self.git("switch", "main")
        self.archive(path, "--dry-run")
        result = self.archive(path, expected=1)
        self.assertIn("task branch", result.stderr)

    def test_terminal_dependency_does_not_expand_into_a_historical_chain(self):
        ancient = self.make_work("ancient")
        dependency = self.make_work("dependency")
        archive.write_artifact(self.root, dependency, task.set_frontmatter_field(dependency.read_text(), "depends_on", [ancient.stem]))
        self.archive(dependency)
        current = self.make_work("current", close=False)
        archive.write_artifact(self.root, current, task.set_frontmatter_field(current.read_text(), "depends_on", [dependency.stem]))
        original = Path.read_text

        def read_text(path, *args, **kwargs):
            self.assertNotEqual(path, ancient, "resume expanded a completed prerequisite's history")
            return original(path, *args, **kwargs)

        with patch.object(Path, "read_text", read_text):
            code, output = self.check()
            self.assertEqual(code, 0, output)
            self.assertEqual(len(doctor.status_payload(self.root, False)["active_work"]), 1)
        self.assertEqual(self.check(full=True)[0], 0, self.check(full=True)[1])


if __name__ == "__main__":
    unittest.main()
