#!/usr/bin/env python3
"""Compare an externally captured agent run with expected workflow behavior."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "examples/evaluations/workflow-cases.json"
FIELDS = (
    "route",
    "artifacts",
    "isolation",
    "project_skills",
    "promote_project_skill",
    "requires_helper",
    "feedback_action",
    "feedback_scope",
)


class EvaluationError(RuntimeError):
    pass


def load_json(path: Path) -> object:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvaluationError(f"cannot read JSON from {path}: {exc}") from exc
    return value


def load_cases(path: Path) -> list[dict[str, object]]:
    value = load_json(path)
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise EvaluationError(f"expected a JSON array of case objects: {path}")
    return value


def load_response_run(path: Path) -> tuple[dict[str, str], list[dict[str, object]]]:
    value = load_json(path)
    if not isinstance(value, dict):
        raise EvaluationError(f"expected a response-run object: {path}")
    run = value.get("run")
    responses = value.get("responses")
    if not isinstance(run, dict) or not all(
        isinstance(run.get(field), str) and run[field].strip()
        for field in ("run_id", "agent", "generated_at")
    ):
        raise EvaluationError("response run needs non-empty run_id, agent, and generated_at metadata")
    if not isinstance(responses, list) or not all(isinstance(item, dict) for item in responses):
        raise EvaluationError("response run needs a responses array of objects")
    return {str(key): str(item) for key, item in run.items()}, responses


def evaluate(cases: list[dict[str, object]], responses: list[dict[str, object]]) -> list[str]:
    failures: list[str] = []
    response_by_id = {str(item.get("id")): item for item in responses}
    if len(response_by_id) != len(responses):
        failures.append("response IDs must be unique")
    for case in cases:
        case_id = str(case.get("id"))
        expected = case.get("expected")
        response = response_by_id.get(case_id)
        if not isinstance(expected, dict):
            failures.append(f"{case_id}: case is missing expected behavior")
            continue
        if response is None:
            failures.append(f"{case_id}: response is missing")
            continue
        for field in FIELDS:
            if response.get(field) != expected.get(field):
                failures.append(
                    f"{case_id}: {field} expected {expected.get(field)!r}, got {response.get(field)!r}"
                )
    unknown = sorted(set(response_by_id) - {str(case.get("id")) for case in cases})
    if unknown:
        failures.append("unknown response IDs: " + ", ".join(unknown))
    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--responses", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        cases = load_cases(args.cases)
        run, responses = load_response_run(args.responses)
        failures = evaluate(cases, responses)
    except EvaluationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print(
        f"MATCH: {len(cases)} workflow behavior case(s) matched "
        f"for run {run['run_id']} ({run['agent']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
