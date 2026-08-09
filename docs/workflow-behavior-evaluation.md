# Workflow Behavior Evaluation

Use this evaluation to test whether a fresh agent applies the workflow policy, not only whether template files are structurally valid.

## Procedure

1. Give a fresh agent `AGENTS.md`, `skills/repo-continuity/SKILL.md`, and `project-skills/INDEX.md` from an initialized fixture.
2. Present each prompt from `examples/evaluations/workflow-cases.json` independently.
3. Ask for a JSON object with run provenance and responses. Do not give the agent the `expected` fields or an earlier response file:

```json
{
  "run": {
    "run_id": "unique-run-id",
    "agent": "agent and model identifier",
    "generated_at": "ISO-8601 timestamp"
  },
  "responses": [
    {
      "id": "case-id",
      "route": "direct",
      "artifacts": [],
      "gates": [],
      "isolation": "current-branch",
      "project_skills": [],
      "promote_project_skill": false,
      "learning_action": "none",
      "requires_helper": false,
      "feedback_action": "none",
      "feedback_scope": "none",
      "decomposition": "none",
      "hierarchy_depth": 0,
      "load_siblings": false
    }
  ]
}
```

4. Capture the unedited response outside this repository, then run:

```bash
python3 scripts/evaluate_workflow_behavior.py --responses <responses.json>
```

The evaluator reports `MATCH`, not a distribution-validation `PASS`. It verifies only that the supplied output matches the case contract; it cannot prove that the output came from a fresh agent. Repository validation tests that the evaluator accepts a conforming fixture and rejects a deliberately wrong one, but does not count that fixture as Agent behavior evidence.

The cases check both positive and negative behavior: Direct work creates no WORK or learning artifact when no verified lesson exists; each bounded Tracked delivery creates only one WORK and records an explicit Learning Check outcome; governed permission work records an independent approval gate in that WORK; a multi-deliverable requirement prefers an external Epic or one bounded local Initiative with independent child WORK records instead of recursive task trees; child resume does not load siblings; parallel work chooses a worktree; matching procedural memory wakes and records a no-op instead of duplicating knowledge; repeated evidence can promote one project Skill; a one-off incident does not create a Skill; and no route requires a companion helper. Normal work records no template feedback, while repeated evidence-backed helper dependency records one local template-wide observation without upstream transmission.

Record unnecessary files loaded by the agent separately. Correct routing with excessive context is still a retrieval regression.
