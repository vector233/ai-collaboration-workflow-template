# Workflow Behavior Evaluation

Use this evaluation to test whether a fresh agent applies the workflow policy, not only whether template files are structurally valid.

## Procedure

1. Give a fresh agent `AGENTS.md`, `skills/ai-collaboration-workflow/SKILL.md`, and `project-skills/INDEX.md` from an initialized fixture.
2. Present each prompt from `examples/evaluations/workflow-cases.json` independently.
3. Ask for a JSON array containing `id`, `route`, `artifacts`, `isolation`, `project_skills`, and `promote_project_skill`.
4. Save the response and run:

```bash
python3 scripts/evaluate_workflow_behavior.py --responses <responses.json>
```

The cases check both positive and negative behavior: Direct work creates no artifacts, Tracked work creates only WORK, governed permission work adds independent review, parallel work chooses a worktree, matching procedural memory wakes, and a one-off incident does not create a project Skill.

Record unnecessary files loaded by the agent separately. Correct routing with excessive context is still a retrieval regression.
