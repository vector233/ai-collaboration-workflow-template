# {{PROJECT_NAME}} — AI 任务驱动知识库

## 定位

给 AI agent 用，不是给人读的。目的是：**接到任何任务 → 快速查到所需信息 → 开始干活**。

---

## 核心原则（Obsidian Wiki-Link 规则）

这是 Zettelkasten，不是普通文档库。所有规则都围绕**节点间链接**展开：

1. **原子化**：一个想法 → 一个 note。不是"一份大文档"，是"一张网"。
2. **Wiki-style 双向链接**：用 `[[01-overview/quick-reference]]` 或 `[[00-governance/dev-guide]]` 互相引用。每个链接意味着两个 note 语义相关。
3. **Inbound links 即存在证明**：一个 note 如果没有任何 inbound link，说明它要么是悬空旧内容，要么需要被合并/删除。
4. **新 note 必须引用旧 note**：当你学到一个新概念，不能凭空建 note，必须找出它和哪些已有 note 语义相关，用 `[[]]` 标出来。
5. **已有 note 被更新时，链接它的 note 不变**：链接方向不变，只是被引用者的内容在原地更新。这和文档树不同。
6. **链接语法**：
   - 子目录：`[[01-overview/quick-reference]]`
   - 上级目录：`[[00-governance/dev-guide]]`
   - 同目录：`[[00-governance/gotchas]]`
   - Obsidian 全局搜索文件名（不推荐，路径不明确）：裸文件名搜索

---

## Vault 文件结构

```
zettelkasten/
  CLAUDE.md                     ← 你在这里
  00-governance/
    project-overview.md         ← {{PROJECT_NAME}} 是什么、目标、技术栈总览
    glossary.md                 ← 术语表（项目核心概念、组件名等）
    decisions.md                ← 关键架构决策及原因（why）
    gotchas.md                  ← 历史踩坑、bug、根因
  01-overview/
    quick-reference.md          ← 高频命令、域名、端点速查（最高频）
    product-vision.md           ← 核心问题、目标市场、产品定位
  02-architecture/
    request-flow.md             ← 端到端请求流程
    auth-model.md               ← API Key、JWT 等鉴权机制
    data-model.md               ← 数据库模型
    <其他架构 note>.md          ← 项目特定 note
  03-roadmap/
    phases.md                  ← Phase 1-6 进度追踪
    versioning.md              ← V1.0/V1.1/V2.0 路线图
  04-cross-cutting/
    <横切关注点 note>.md        ← 仅伞形项目使用
  05-reference/
    prd.md                     ← 外部 PRD 摘要
    architecture.md            ← 外部架构文档摘要
    task.md                    ← 任务进度索引
  06-requirements/
    README.md                  ← 后续迭代需求入口和状态迁移规则
    backlog/                   ← 已识别但尚未进入实施的需求
    in-progress/               ← 正在分析、设计、开发或联调的需求
    done/                      ← 已完成并已回写现状文档的需求
  07-review/
    README.md                  ← AI/人工 review 交互入口
    pending/                   ← 等待 reviewer 处理的阶段性交接文档
    in-review/                 ← 正在处理反馈的 review 文档
    done/                      ← 已确认关闭的 review 文档
  08-technical-designs/
    README.md                  ← 需求确认后、代码开发前的技术方案入口
    pending/                   ← 已提出但尚未确认的技术方案
    approved/                  ← 已确认，可作为开发输入的技术方案
    implemented/               ← 已实施并已回写架构现状的技术方案
```

> **目录只是物理组织**：真正重要的是 note 之间的 `[[]]` 引用链。

---

## 查找路径

### 任务分类速查

| 任务类型 | 去哪查 |
|---|---|
| 常用命令、域名、端点 | [[01-overview/quick-reference]] |
| 产品定位、目标市场、定价 | [[01-overview/product-vision]] |
| 系统架构、请求流程 | [[02-architecture/request-flow]] |
| 鉴权机制 | [[02-architecture/auth-model]] |
| 数据库模型 | [[02-architecture/data-model]] |
| 安全/数据合规 | [[04-cross-cutting/...]] |
| Phase 进度 | [[03-roadmap/phases]] |
| 版本规划 | [[03-roadmap/versioning]] |
| 后续迭代需求 | [[06-requirements/README]] |
| 待 review 文档和 review 结果 | [[07-review/README]] |
| 技术方案和架构决策 | [[08-technical-designs/README]] |
| 历史踩坑 | [[00-governance/gotchas]] |
| 术语解释 | [[00-governance/glossary]] |

### 关键文件索引

| 文件 | 用途 |
|---|---|
| [[01-overview/quick-reference]] | 所有命令、域名、API 端点速查（最高频） |
| [[01-overview/product-vision]] | 核心问题、目标市场、定价策略、竞品分析 |
| [[02-architecture/request-flow]] | 端到端请求路径全链路 |
| [[00-governance/decisions]] | 关键架构决策记录 |
| [[00-governance/gotchas]] | 历史 bug、根因、修复方式，避免重复踩坑 |
| [[06-requirements/README]] | 需求迭代入口、模板使用方式、状态迁移规则 |
| [[08-technical-designs/README]] | 技术方案入口，将需求转换为架构流程和关键决策 |
| [[07-review/README]] | 阶段性 review 交互入口、待 review 文档、review 结果 |

---

## 接任务后的标准流程

1. **分类**：新功能？Bugfix？架构问题？GTM？
2. **查需求入口**：如果是新迭代，先看 [[06-requirements/README]]，确认是否已有 backlog/in-progress 需求
3. **查技术方案状态**：需求确认后、开发前必须看 [[08-technical-designs/README]]，确认已有 approved 技术方案；没有则先创建 pending 技术方案
4. **查 review 状态**：如果上一轮阶段性交接还未关闭，先看 [[07-review/README]]，处理 pending/in-review 文档，不进入下一轮开发
5. **查相关 note**：根据上表确定去哪查
6. **确认代码位置**：
<!-- UMBRELLA-ONLY: keep this block only if {{REPO_TYPE}} == umbrella -->
   - 各子项目代码定位 → 参考各子项目自身的 CLAUDE.md
<!-- /UMBRELLA-ONLY -->
7. **实施**
8. **更新相关 note**：如果架构、流程、踩坑内容有变化，同步更新 zettelkasten，尤其是 [[02-architecture/...]]
9. **阶段性 review**：阶段性工作完成后，在 [[07-review/README]] 下输出或更新 review 文档，等待 review 关闭后再继续下一轮开发

---

## 触发更新的时机

- 架构重大决策变化
- 新 Phase 完成或计划调整
- 发现新的坑或错误理解
- 产品定位、定价策略调整
- 新增子项目或废弃已有模块

---

<!-- UMBRELLA-ONLY: keep this block only if {{REPO_TYPE}} == umbrella -->
## 与子项目文档的关系

{{PROJECT_NAME}} 是**伞形规划仓库**，各子项目有专属文档：

| 子项目 | 专属文档 |
|---|---|
<!-- {{SUB_PROJECTS}} -->

{{PROJECT_NAME}} zettelkasten (`zettelkasten/`) 负责**跨项目架构决策**和**伞形视角**（[[00-governance/]]、[[01-overview/]]、[[02-architecture/]] 等）。

各子项目 zettelkasten 负责**模块级实现细节**。
<!-- /UMBRELLA-ONLY -->
