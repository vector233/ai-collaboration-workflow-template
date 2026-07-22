#!/usr/bin/env python3
"""Evaluate externally captured core-versus-routing agent runs."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "examples/evaluations/model-routing-cases.json"
COHORTS = {
    "codex": ("codex-core", "codex-routing"),
    "claude": ("claude-core", "claude-routing"),
}
EVIDENCE_KINDS = {"real-agent-run", "synthetic-harness-fixture"}


class EvaluationError(RuntimeError):
    pass


@dataclass(frozen=True)
class CohortResult:
    name: str
    core_variant: str
    routing_variant: str
    core_passes: int
    routing_passes: int
    core_high_risk_misses: int
    routing_high_risk_misses: int
    core_duration_median: float
    routing_duration_median: float
    core_quota_units: float | None
    routing_quota_units: float | None


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvaluationError(f"cannot read JSON from {path}: {exc}") from exc


def load_cases(path: Path) -> list[dict[str, object]]:
    value = load_json(path)
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise EvaluationError(f"expected an array of case objects: {path}")
    if len(value) < 5:
        raise EvaluationError("model-routing evaluation requires at least five tasks")
    ids = [str(item.get("id", "")) for item in value]
    if any(not case_id for case_id in ids) or len(ids) != len(set(ids)):
        raise EvaluationError("case IDs must be non-empty and unique")
    for item in value:
        for field in ("required_routed_roles", "allowed_routed_roles"):
            roles = item.get(field)
            if not isinstance(roles, list) or not all(
                isinstance(role, str) and role for role in roles
            ):
                raise EvaluationError(
                    f"{item['id']}: {field} must be an array of role names"
                )
        if not set(item["required_routed_roles"]).issubset(
            set(item["allowed_routed_roles"])
        ):
            raise EvaluationError(f"{item['id']}: required roles must also be allowed")
    return value


def load_run(path: Path) -> tuple[dict[str, object], list[dict[str, object]]]:
    value = load_json(path)
    if not isinstance(value, dict):
        raise EvaluationError(f"expected a run-suite object: {path}")
    suite = value.get("suite")
    runs = value.get("runs")
    if (
        not isinstance(suite, dict)
        or not isinstance(runs, list)
        or not all(isinstance(item, dict) for item in runs)
    ):
        raise EvaluationError("run file needs a suite object and a runs array")
    for field in (
        "suite_id",
        "evidence_kind",
        "repository_commit",
        "template_version",
        "captured_at",
    ):
        if not isinstance(suite.get(field), str) or not str(suite[field]).strip():
            raise EvaluationError(f"suite metadata needs a non-empty {field}")
    if suite["evidence_kind"] not in EVIDENCE_KINDS:
        raise EvaluationError(
            "suite evidence_kind must be real-agent-run or synthetic-harness-fixture"
        )
    return suite, runs


def non_negative_number(value: object) -> bool:
    return (
        isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0
    )


def non_negative_integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def validate_run_shape(
    run: dict[str, object],
    *,
    real_evidence: bool,
) -> list[str]:
    failures: list[str] = []
    label = f"{run.get('task_id', '?')}/{run.get('variant', '?')}"
    for field in ("task_id", "variant", "agent", "model", "session_id", "captured_at"):
        if not isinstance(run.get(field), str) or not str(run[field]).strip():
            failures.append(f"{label}: missing non-empty {field}")
    if not isinstance(run.get("passed_acceptance"), bool):
        failures.append(f"{label}: passed_acceptance must be boolean")
    for field in ("high_risk_misses", "files_loaded"):
        if not non_negative_integer(run.get(field)):
            failures.append(f"{label}: {field} must be a non-negative integer")
    if not non_negative_number(run.get("duration_seconds")):
        failures.append(f"{label}: duration_seconds must be a non-negative number")
    calls = run.get("specialist_calls")
    if not isinstance(calls, list) or not all(isinstance(item, dict) for item in calls):
        failures.append(f"{label}: specialist_calls must be an array of objects")
    else:
        for index, call in enumerate(calls):
            if not isinstance(call.get("role"), str) or not call["role"].strip():
                failures.append(f"{label}: specialist call {index} is missing role")
            if not isinstance(call.get("model"), str) or not call["model"].strip():
                failures.append(f"{label}: specialist call {index} is missing model")
    usage = run.get("usage")
    if usage is not None:
        if not isinstance(usage, dict):
            failures.append(f"{label}: usage must be an object when present")
        else:
            for field in ("input_tokens", "output_tokens"):
                if field in usage and not non_negative_integer(usage[field]):
                    failures.append(
                        f"{label}: usage.{field} must be a non-negative integer"
                    )
            if "quota_units" in usage and not non_negative_number(usage["quota_units"]):
                failures.append(f"{label}: usage.quota_units must be non-negative")
    if real_evidence:
        for field in ("raw_evidence", "acceptance_evidence"):
            value = run.get(field)
            if not isinstance(value, str) or not value.strip():
                failures.append(f"{label}: real runs require {field} provenance")
    return failures


def quota_total(runs: list[dict[str, object]]) -> float | None:
    values: list[float] = []
    for run in runs:
        usage = run.get("usage")
        if not isinstance(usage, dict) or not non_negative_number(
            usage.get("quota_units")
        ):
            return None
        values.append(float(usage["quota_units"]))
    return sum(values)


def evaluate(
    cases: list[dict[str, object]],
    suite: dict[str, object],
    runs: list[dict[str, object]],
    *,
    require_cost_improvement: bool,
) -> tuple[list[str], list[CohortResult], list[str]]:
    failures: list[str] = []
    notes: list[str] = []
    real_evidence = suite["evidence_kind"] == "real-agent-run"
    for run in runs:
        failures.extend(validate_run_shape(run, real_evidence=real_evidence))
    has_quota = any(
        isinstance(run.get("usage"), dict) and "quota_units" in run["usage"]
        for run in runs
    )
    if real_evidence and has_quota:
        for field in ("quota_metric", "quota_source"):
            if not isinstance(suite.get(field), str) or not str(suite[field]).strip():
                failures.append(
                    f"suite metadata needs non-empty {field} when quota_units are used"
                )
    if failures:
        return failures, [], []

    case_by_id = {str(case["id"]): case for case in cases}
    known_variants = {variant for pair in COHORTS.values() for variant in pair}
    keys = [(str(run.get("task_id")), str(run.get("variant"))) for run in runs]
    if len(keys) != len(set(keys)):
        failures.append("each task and variant pair must appear exactly once")
    unknown_tasks = sorted({task for task, _ in keys} - set(case_by_id))
    unknown_variants = sorted({variant for _, variant in keys} - known_variants)
    if unknown_tasks:
        failures.append("unknown task IDs: " + ", ".join(unknown_tasks))
    if unknown_variants:
        failures.append("unknown variants: " + ", ".join(unknown_variants))

    variants_present = {variant for _, variant in keys}
    selected_cohorts: list[tuple[str, str, str]] = []
    for name, (core, routing) in COHORTS.items():
        present = {core, routing} & variants_present
        if present and present != {core, routing}:
            failures.append(f"{name}: core and routing variants must both be present")
        elif present:
            selected_cohorts.append((name, core, routing))
    if not selected_cohorts:
        failures.append("no complete Codex or Claude comparison cohort was supplied")

    run_by_key = {
        (str(run.get("task_id")), str(run.get("variant"))): run for run in runs
    }
    results: list[CohortResult] = []
    for name, core_variant, routing_variant in selected_cohorts:
        cohort_runs: dict[str, list[dict[str, object]]] = {
            core_variant: [],
            routing_variant: [],
        }
        for case_id, case in case_by_id.items():
            core = run_by_key.get((case_id, core_variant))
            routing = run_by_key.get((case_id, routing_variant))
            if core is None:
                failures.append(f"{case_id}: missing {core_variant} run")
                continue
            if routing is None:
                failures.append(f"{case_id}: missing {routing_variant} run")
                continue
            cohort_runs[core_variant].append(core)
            cohort_runs[routing_variant].append(routing)

            core_calls = core.get("specialist_calls")
            routing_calls = routing.get("specialist_calls")
            if isinstance(core_calls, list) and core_calls:
                failures.append(
                    f"{case_id}/{core_variant}: core-only control used specialists"
                )
            if isinstance(routing_calls, list):
                roles = {
                    str(call.get("role"))
                    for call in routing_calls
                    if isinstance(call, dict)
                }
                allowed = set(case["allowed_routed_roles"])
                required = set(case["required_routed_roles"])
                unexpected = sorted(roles - allowed)
                missing = sorted(required - roles)
                if unexpected:
                    failures.append(
                        f"{case_id}/{routing_variant}: unexpected specialist roles: "
                        + ", ".join(unexpected)
                    )
                if missing:
                    failures.append(
                        f"{case_id}/{routing_variant}: missing expected specialist roles: "
                        + ", ".join(missing)
                    )

            if (
                core.get("passed_acceptance") is True
                and routing.get("passed_acceptance") is not True
            ):
                failures.append(
                    f"{case_id}/{name}: routing failed acceptance that core passed"
                )
            core_misses = core.get("high_risk_misses")
            routing_misses = routing.get("high_risk_misses")
            if non_negative_number(core_misses) and non_negative_number(routing_misses):
                if float(routing_misses) > float(core_misses):
                    failures.append(
                        f"{case_id}/{name}: routing increased high-risk misses"
                    )

        complete_core = cohort_runs[core_variant]
        complete_routing = cohort_runs[routing_variant]
        if len(complete_core) != len(cases) or len(complete_routing) != len(cases):
            continue
        core_passes = sum(run["passed_acceptance"] is True for run in complete_core)
        routing_passes = sum(
            run["passed_acceptance"] is True for run in complete_routing
        )
        if routing_passes < core_passes:
            failures.append(f"{name}: routing pass count is below core-only")
        core_misses = sum(int(run["high_risk_misses"]) for run in complete_core)
        routing_misses = sum(int(run["high_risk_misses"]) for run in complete_routing)
        core_quota = quota_total(complete_core)
        routing_quota = quota_total(complete_routing)
        if core_quota is None or routing_quota is None:
            notes.append(
                f"{name}: cost inconclusive; comparable quota_units are missing"
            )
            if require_cost_improvement:
                failures.append(
                    f"{name}: --require-cost-improvement needs quota_units for every run"
                )
        elif routing_quota >= core_quota:
            notes.append(
                f"{name}: routing quota did not improve ({routing_quota:g} >= {core_quota:g})"
            )
            if require_cost_improvement:
                failures.append(f"{name}: routing quota usage did not improve")
        else:
            reduction = (
                (core_quota - routing_quota) / core_quota * 100 if core_quota else 0
            )
            notes.append(f"{name}: routing quota improved by {reduction:.1f}%")
        results.append(
            CohortResult(
                name=name,
                core_variant=core_variant,
                routing_variant=routing_variant,
                core_passes=core_passes,
                routing_passes=routing_passes,
                core_high_risk_misses=core_misses,
                routing_high_risk_misses=routing_misses,
                core_duration_median=statistics.median(
                    float(run["duration_seconds"]) for run in complete_core
                ),
                routing_duration_median=statistics.median(
                    float(run["duration_seconds"]) for run in complete_routing
                ),
                core_quota_units=core_quota,
                routing_quota_units=routing_quota,
            )
        )

    if real_evidence:
        session_ids = [
            str(run.get("session_id")) for run in runs if run.get("session_id")
        ]
        if len(session_ids) != len(set(session_ids)):
            failures.append(
                "real runs must use a separate fresh session per task and variant"
            )
    return failures, results, notes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--runs", type=Path, required=True)
    parser.add_argument(
        "--require-cost-improvement",
        action="store_true",
        help="Fail unless every supplied cohort reports lower comparable quota_units.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        cases = load_cases(args.cases)
        suite, runs = load_run(args.runs)
        failures, results, notes = evaluate(
            cases,
            suite,
            runs,
            require_cost_improvement=args.require_cost_improvement,
        )
    except EvaluationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    for result in results:
        print(
            f"{result.name}: acceptance {result.routing_passes}/{len(cases)} routing "
            f"vs {result.core_passes}/{len(cases)} core; high-risk misses "
            f"{result.routing_high_risk_misses} vs {result.core_high_risk_misses}; "
            f"median duration {result.routing_duration_median:g}s vs "
            f"{result.core_duration_median:g}s"
        )
    for note in notes:
        print(f"NOTE: {note}")
    if suite["evidence_kind"] == "synthetic-harness-fixture":
        print(
            "HARNESS MATCH: synthetic fixture satisfied the evaluator; "
            "this is not model-routing effectiveness evidence"
        )
    else:
        print(
            "EVIDENCE PASS: routing preserved the recorded quality floor; "
            "cost is supported only for cohorts with sourced, improved quota_units"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
