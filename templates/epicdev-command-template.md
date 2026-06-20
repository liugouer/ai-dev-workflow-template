# /epicdev 命令模板 — 大功能拆解与批量执行

> 本文件是模板，用于复制到新业务项目的 `.codebuddy/commands/epicdev.md`。
> 新项目复制后需要替换所有 `{占位符}` 为实际值。

## 用途

将大功能目标拆解为多个最小需求单元，创建 TAPD 需求，并按顺序自动执行每个需求的完整研发闭环。

## 命令格式

```
/epicdev <大功能描述>
/epicdev --plan <大功能描述>       # 仅拆解，输出计划，不执行
/epicdev --yes <大功能描述>        # 拆解、创建需求并顺序执行
```

## 启动前强制预检

在开始执行任何操作前，CodeBuddy 必须先输出以下预检表：

| # | 检查项 | 说明 |
|---|--------|------|
| 1 | 当前仓库路径 | `pwd` |
| 2 | 当前 Git 分支 | `git branch --show-current` |
| 3 | 当前 git status | `git status --short` |
| 4 | 是否在 main 分支 | 是则禁止直接修改 |
| 5 | 是否有未提交改动 | 如果存在，说明内容 |
| 6 | 已读取规则文件清单 | `.codebuddy/rules/` |
| 7 | 已读取知识库文件清单 | `.codebuddy/knowledge/` |

## 执行流程

### 第一步：拆解大功能

1. 读取 `EpicRequirementDecompositionRules.mdc`
2. 分析用户输入的大功能描述
3. 将大功能拆解为最小需求单元（默认不超过 5 个）
4. 输出拆解计划表格
5. 如果大功能过于复杂，提示用户确认是否继续拆第二批

### 第二步：用户确认

- 如果是 `--plan` 模式：仅输出拆解计划，等待用户确认
- 如果是 `--yes` 模式：直接进入执行
- 默认模式：输出拆解计划等待用户确认后执行

### 第三步：创建 TAPD 需求

使用 TAPD MCP `create_story_or_task` 逐个创建需求：

* `entity_type`: `"tasks"`（优先使用任务类型；TAPD 任务工作流为 open→progressing→done→end，更适合 AI 自动化闭环。仅在任务类型不可用时使用 `"stories"`）
* `workspace_id`: `{TAPD_WORKSPACE_ID}`
* `name`: 拆解后的需求标题
* `description`: 需求正文
* `status`: `"open"`
* `iteration`: `{DEFAULT_ITERATION}`

### 第四步：顺序执行需求闭环

按依赖顺序逐个执行每个需求的完整研发闭环。

**每个需求必须走完完整闭环后才能进入下一个需求。**

### 第五步：分批执行

- 一次最多自动执行 3 个需求
- 超过 3 个需求时，分批次执行

### 第六步：项目自检

根据当前项目类型执行项目自检命令：

- 若当前项目是模板仓库 → 运行 `python scripts/validate_template.py`
- 若当前项目是业务仓库 → 运行 pytest、coverage 和 check_coverage

## 必须遵守的规则

1. `EpicRequirementDecompositionRules.mdc` — 大功能拆解规则
2. `AutonomousWorkflowRules.mdc` — 总控规则
3. `ExecutionGuardRules.mdc` — 执行护栏
4. `EffectFeedbackLoopRules.mdc` — 效果反馈修复闭环
5. `ExperienceLayeringRules.mdc` — 经验分层沉淀
6. `WorkflowCompletionRules.mdc` — 闭环完成判定
7. `HumanInterventionRules.mdc` — 人工介入断点

## 最终报告

执行结束后输出完整的 Epic 报告。
