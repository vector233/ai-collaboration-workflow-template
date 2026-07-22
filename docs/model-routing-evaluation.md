# Model-Routing A/B Evaluation

Use this evaluation to test whether optional specialist routing reduces comparable quota use without lowering delivery quality. It does not execute Codex or Claude Code and it does not infer correctness from a model's self-report. It validates externally captured runs after project-native tests or an independent reviewer supplies the acceptance result.

## Comparison Design

Run the six task classes in `examples/evaluations/model-routing-cases.json` from the same repository commit and equivalent clean worktrees. Compare at least one complete cohort:

- `codex-core` versus `codex-routing`;
- `claude-core` versus `claude-routing`.

Use a fresh session for every task and variant. Keep the root model, prompt, repository commit, permissions, and acceptance checks equivalent within each cohort. The core control must not have the optional adapter installed. The routing variant must use the matching adapter without changing the root-session model.

The default cases cover a small Direct task, read-only discovery, scoped implementation, security review, architecture, and implementation followed by review. Replace the generic prompt with an equivalent reproducible task when a fixture or real project is used, but keep the case ID and role boundary.

## Capture Contract

Keep unedited outputs, test logs, session identifiers, and any usage export outside this repository. Give every run a stable `raw_evidence` path or URL. Record `passed_acceptance` only after project-native validation or independent review. Record every high-risk defect the run missed in `high_risk_misses`.

Create one JSON file shaped like this:

```json
{
  "suite": {
    "suite_id": "2026-07-routing-a-b",
    "evidence_kind": "real-agent-run",
    "repository_commit": "full commit SHA",
    "template_version": "vX.Y.Z",
    "captured_at": "2026-07-23T10:00:00Z",
    "quota_metric": "provider-exported comparable unit",
    "quota_source": "/external/evidence/provider-usage-export.json"
  },
  "runs": [
    {
      "task_id": "direct-small-doc-fix",
      "variant": "codex-core",
      "agent": "Codex",
      "model": "root model identifier",
      "session_id": "unique session identifier",
      "captured_at": "2026-07-23T10:05:00Z",
      "duration_seconds": 90,
      "passed_acceptance": true,
      "high_risk_misses": 0,
      "specialist_calls": [],
      "files_loaded": 2,
      "usage": {
        "input_tokens": 1000,
        "output_tokens": 300,
        "quota_units": 1.0
      },
      "raw_evidence": "/external/evidence/codex-core-direct.txt",
      "acceptance_evidence": "/external/evidence/codex-core-direct-verification.txt"
    }
  ]
}
```

Repeat the run object for every case in both variants of a cohort. `raw_evidence` identifies the unedited Agent output; `acceptance_evidence` identifies the project-native test or independent review that assigned the acceptance result and high-risk miss count. `input_tokens` and `output_tokens` are descriptive only. Use `quota_units` only when the provider exposes a comparable measure across the two variants, and record its metric and export in `quota_metric` and `quota_source`; do not invent a conversion from tokens to subscription quota.

## Evaluate

```bash
python3 scripts/evaluate_model_routing.py --runs /external/evidence/runs.json
```

To make lower comparable quota a hard gate:

```bash
python3 scripts/evaluate_model_routing.py \
  --runs /external/evidence/runs.json \
  --require-cost-improvement
```

The evaluator requires:

- at least five paired tasks;
- a complete core/routing pair for every selected cohort;
- no specialist in the core-only control;
- no unnecessary delegation for the Direct case;
- the expected low-cost or high-confidence role for each routed case;
- routing acceptance at least as strong as core-only;
- no increase in recorded high-risk misses.

If comparable `quota_units` are absent, quality and routing can pass but cost remains explicitly inconclusive. A synthetic fixture may test the evaluator and prints `HARNESS MATCH`; it must never be presented as fresh-Agent or cost-saving evidence.

## Report Results

Keep raw private evidence outside the distribution repository. A sanitized summary may record the repository commit, client and model identifiers, case IDs, acceptance counts, high-risk misses, specialist calls, median duration, comparable quota result, and evaluator command. Do not publish prompts, logs, or project details without user approval.
