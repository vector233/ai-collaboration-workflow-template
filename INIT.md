# INIT.md — 初始化知识库

> <EXTREMELY-IMPORTANT>
> 本文件由 AI 助手（推荐 Claude Code）执行。请按下列步骤**严格顺序**执行，不要跳步。完成后**必须删除本文件**。
> </EXTREMELY-IMPORTANT>

## 0. 触发口令

用户在 Claude Code（或等价 AI 助手）中说：

> 请按 INIT.md 初始化此知识库

或

> Initialize this knowledge base by following INIT.md.

收到口令后，按下文 §1 → §6 顺序执行。

---

## 1. 占位符总清单

执行替换时确保覆盖以下所有占位符：

| 占位符 | 含义 | 示例 |
|---|---|---|
| `{{PROJECT_NAME}}` | 项目名（用于标题、文件名） | `AcctBridge` |
| `{{PROJECT_DESCRIPTION}}` | 一句话项目描述 | `SaaS API gateway for on-prem accounting software` |
| `{{TECH_STACK}}` | 技术栈摘要 | `Go · Gin · MySQL · Next.js · .NET 8` |
| `{{REPO_TYPE}}` | `umbrella` 或 `single` | `umbrella` |
| `{{SUB_PROJECTS}}` | 仅 umbrella：子项目表格（Markdown 多行） | 见下方示例 |
| `{{DOMAINS}}` | 域名 / 端口表（Markdown 多行） | 见下方示例 |
| `{{REPOS}}` | Git 仓库列表（Markdown 多行） | 见下方示例 |

### 多行占位符示例值（用户没明确时可参考结构）

`{{SUB_PROJECTS}}` 示例：

```markdown
| 子项目 | 路径 | 仓库 |
|---|---|---|
| Backend | backend/ | example-owner/foo-backend |
| Portal  | portal/  | example-owner/foo-portal  |
```

`{{DOMAINS}}` 示例：

```markdown
| 环境 | 域名 |
|---|---|
| Production | foo.example.com |
| Local API  | localhost:8080 |
```

`{{REPOS}}` 示例：

```markdown
- example-owner/foo-backend
- example-owner/foo-portal
```

---

## 2. 询问用户

按顺序询问下列问题。**每个问题问一次，等用户回答后再问下一个**。如果用户已经在触发口令中提供了部分答案，跳过对应问题。

1. **项目叫什么名字？** 用于 `{{PROJECT_NAME}}`，建议 PascalCase 或品牌名（例：`AcctBridge`、`FooBridge`）
2. **一句话描述这个项目是什么？** 用于 `{{PROJECT_DESCRIPTION}}`
3. **项目的主要技术栈是什么？** 列出 3-6 项即可（用于 `{{TECH_STACK}}`）
4. **这是伞形项目还是单项目仓库？** umbrella = 一个仓库托管多个子项目的规划/文档；single = 单一代码仓库
5. **如果 umbrella：列出子项目**（每个：名字 / 路径 / Git 仓库）
6. **项目主要的域名和端口？**（生产 / 本地 / 管理后台等，给出 Markdown 表格或行列表）
7. **项目对应的 Git 仓库列表？**

> 提示：如果用户回答 6/7 时只给了零散信息，主动用 Markdown 表格 / 列表格式化。

---

## 3. 执行替换

完成询问后，**按以下顺序**执行。

### 3.1 重命名项目主索引文件

使用 Bash：

```bash
cd <repo-root>
PROJECT_NAME_SAFE="$(echo '<用户输入的 PROJECT_NAME>' | tr ' ' '_')"
mv 'zettelkasten/{{PROJECT_NAME}}.md' "zettelkasten/${PROJECT_NAME_SAFE}.md"
```

> 若 `PROJECT_NAME` 含空格，文件名用下划线（例：`My Project` → `My_Project.md`）。

### 3.2 批量替换占位符

对 `zettelkasten/` 下所有 `.md` 文件，依次替换：

- `{{PROJECT_NAME}}` → 用户输入
- `{{PROJECT_DESCRIPTION}}` → 用户输入
- `{{TECH_STACK}}` → 用户输入
- `{{DOMAINS}}` → 用户输入（多行 Markdown 表格，保持表格格式）
- `{{REPOS}}` → 用户输入（多行 Markdown 列表）
- `{{REPO_TYPE}}` → `umbrella` 或 `single`
- `{{SUB_PROJECTS}}` → 用户输入（umbrella）或空字符串（single）

简单单行占位符可用 sed：

```bash
find zettelkasten -type f -name '*.md' -exec \
  sed -i.bak \
    -e 's/{{PROJECT_NAME}}/<value>/g' \
    -e 's/{{PROJECT_DESCRIPTION}}/<value>/g' \
    -e 's/{{TECH_STACK}}/<value>/g' \
    -e 's/{{REPO_TYPE}}/<umbrella-or-single>/g' \
    {} \;
find zettelkasten -name '*.bak' -delete
```

多行占位符（`{{DOMAINS}}` / `{{REPOS}}` / `{{SUB_PROJECTS}}`）必须用 Edit/Write 工具逐文件处理，**不要用 sed 处理多行**。

### 3.3 处理伞形/单仓分支

**如果 `{{REPO_TYPE}} == single`**：

```bash
rm -rf zettelkasten/04-cross-cutting
```

并对所有 `.md` 文件：**删除所有被 `<!-- UMBRELLA-ONLY` 和 `<!-- /UMBRELLA-ONLY -->` 包裹的段落**（连同标记一起删除）。

可以用 sed：

```bash
find zettelkasten -name '*.md' -exec \
  sed -i.bak '/<!-- UMBRELLA-ONLY/,/<!-- \/UMBRELLA-ONLY -->/d' {} \;
find zettelkasten -name '*.bak' -delete
```

**如果 `{{REPO_TYPE}} == umbrella`**：保留 UMBRELLA-ONLY 标记之间的内容，但**删除 `<!-- UMBRELLA-ONLY ... -->` 和 `<!-- /UMBRELLA-ONLY -->` 标记本身**：

```bash
find zettelkasten -name '*.md' -exec \
  sed -i.bak \
    -e '/<!-- UMBRELLA-ONLY/d' \
    -e '/<!-- \/UMBRELLA-ONLY -->/d' \
    {} \;
find zettelkasten -name '*.bak' -delete
```

---

## 4. 生成首批 note 实际内容

根据用户答案，**改写**以下文件，使其包含具体内容（不再是占位符或泛例）：

### 4.1 `zettelkasten/00-governance/project-overview.md`

基于用户的 `{{PROJECT_DESCRIPTION}}`、`{{TECH_STACK}}`、`{{SUB_PROJECTS}}` 答案，把"产品定位"、"技术栈"、"子项目"几节改写为具体内容（保留"核心约束"和"参见"两节作为待用户后续补充的骨架）。

### 4.2 `zettelkasten/01-overview/quick-reference.md`

向用户**额外询问** 2-3 条最高频的开发命令（如 `make run`、`npm run dev`），填入"常用命令"节。`{{DOMAINS}}` 和 `{{REPOS}}` 已在 §3.2 替换。

### 4.3 `zettelkasten/01-overview/product-vision.md`

基于 `{{PROJECT_DESCRIPTION}}` 写 1 段"当前定位"，其他节保留 placeholder 由用户日后补充。

### 4.4 其他文件

`glossary.md` / `decisions.md` / `gotchas.md` / 各工作流 README / 模板 / `03-roadmap/phases.md` / `02-architecture/README.md` / `05-reference/README.md` — **保持当前内容不变**，由用户日后按需填充。

---

## 5. 自检

```bash
cd <repo-root>

# 1. 不应有占位符残留
grep -rE '\{\{[A-Z_]+\}\}' zettelkasten/ && echo "FAIL: 仍有占位符" || echo "OK: 无占位符"

# 2. 不应有 UMBRELLA-ONLY 标记残留
grep -r 'UMBRELLA-ONLY' zettelkasten/ && echo "FAIL: 仍有 UMBRELLA-ONLY 标记" || echo "OK"

# 3. 单仓模式下不应有 04-cross-cutting/（仅 REPO_TYPE == single 时检查）
test -d zettelkasten/04-cross-cutting && echo "如 REPO_TYPE == single 则 FAIL" || echo "OK"

# 4. 项目主索引文件应已重命名
test -f "zettelkasten/{{PROJECT_NAME}}.md" && echo "FAIL: 未重命名" || echo "OK"
```

**任一 FAIL 必须修复后才能进入下一步**。

---

## 6. 收尾

### 6.1 删除 INIT.md 自身

```bash
rm INIT.md
```

### 6.2 首次 commit

```bash
git add -A
git commit -m "chore: initialize knowledge base for <PROJECT_NAME>"
```

---

完成。后续按 `zettelkasten/CLAUDE.md` 的"接任务后的标准流程"使用知识库。
