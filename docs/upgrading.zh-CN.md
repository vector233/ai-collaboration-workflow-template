# 升级已经初始化的仓库

初始化后的 Repo Continuity 项目在同一批文件中同时保存两类价值：上游流程改进，以及项目自己维护的事实、规则和已沉淀流程。普通模板覆盖无法区分二者，因此 Repo Continuity 使用三方协调：

```text
记录的旧上游 + 当前已初始化项目 + 目标上游
                         |
                         v
                 可 Review 的任务分支 Diff
```

## 升级契约

旧上游版本来自 `zettelkasten/AI.md` 中的 `Template baseline`，目标版本来自已安装 Companion Skill 固定的 release；当前项目对于本地事实和更严格策略始终具有权威性。

协调器会执行以下动作：

| 情况 | 动作 |
|---|---|
| 上游新增、本地不存在 | 加入新文件 |
| 上游已修改、本地仍等于旧基线 | 采用上游版本 |
| 本地已修改、上游仍等于旧基线 | 保留本地版本 |
| 双方修改位于互不重叠的文本区域 | 自动完成干净的三方合并 |
| 双方修改冲突、本地路径不安全或新增文件碰撞 | 保持冲突文件不变 |
| 上游删除文件 | 保持文件不变，标记为待确认删除 |

最后两种情况需要判断，因为删除或重叠内容可能属于项目知识。任何命令都不会自动推进模板基线。

## 推荐流程

1. 安装目标 release 的 Companion Skill。
2. 在任务分支创建一个 Tracked 或 Governed 升级 WORK，记录旧版本、目标版本、owned paths、验证计划和回滚计划；提交升级前 checkpoint，使 worktree 保持干净。
3. 生成详细报告和应用预览：

   ```bash
   python3 "$SKILL_ROOT/scripts/bootstrap_template.py" --target . --upgrade-report
   python3 "$SKILL_ROOT/scripts/bootstrap_template.py" --target . --upgrade-apply --dry-run
   ```

4. 应用安全子集：

   ```bash
   python3 "$SKILL_ROOT/scripts/bootstrap_template.py" --target . --upgrade-apply
   ```

   退出码 0 表示不存在阻塞路径；退出码 2 表示安全变更已经应用，但仍有待确认删除或冲突；退出码 1 表示安全前置条件失败，计划中的文件没有被写入。

5. 处理待确认删除与冲突，保留已验证的项目事实、更严格的本地规则和有价值的项目经验，不要恢复 `INIT.md` 或 payload marker。
6. 运行项目验证、Repo Continuity Doctor 或等价结构检查，并检查完整 Git Diff。
7. 只有结果验收后才把 `Template baseline` 更新为目标版本。在同一个 WORK 中记录验证和升级决策，完成 Learning Check 并提交。

只有显式传入 `--with-model-routing codex`、`claude` 或 `all` 时，才会把可选模型路由 overlay 纳入升级。Agent 可使用 `--json` 获取机器可读结果；只有仓库记录的基线无法解析时才使用 `--baseline-ref`。

## 安全与恢复

`--upgrade-apply` 要求目标是 Git 仓库根目录、当前位于非 `main`/`master` 的命名分支并且 worktree 干净。计划写入以事务方式执行：某次写入失败时，该次命令已经写入的文件会恢复。目标 symlink 和非普通文件永远不会被跟随。

任务分支和升级前提交就是回滚边界。在推进基线前，重新生成报告仍会使用旧版本做三方比较。升级成功后，新基线成为下一次协调的参考，但不会抹除项目 Git 历史或本地所有权。

## 迁移未结束任务入口

旧项目没有 `zettelkasten/work/active/` 入口时，保留原 WORK 文件与本地规则。协调合并生命周期和阅读入口规则后，显式清点一次稳定任务文件，为每个未结束记录建立一个 `*.ref.md`。可以手工维护，也可以先运行 `workflow_archive.py reindex --root <repo-root> --dry-run`，检查预览并与其他写入者协调后，在升级分支运行 `reindex`。

使用 `workflow_doctor.py --root <repo-root> --full --strict` 检查遗漏入口和历史完整性，审阅入口文件后再启用日常精简发现流程。普通状态查询发现入口缺失时必须报告修复需求，不能悄悄读取所有旧任务。升级和重建入口不会归档、删除或改写项目证据；历史正文需要在保留当前有效知识后单独归档。参见[知识生命周期](../template/zettelkasten/knowledge-lifecycle.md)。
