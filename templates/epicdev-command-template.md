# /epicdev 命令模板

## 概述

`/epicdev` 是 CodeBuddy 命令，用于将大功能拆解为多个最小需求单元，批量创建 TAPD 需求并按依赖顺序执行完整研发闭环。

## 文件配置

将此内容复制到 `.codebuddy/commands/epicdev.md`，替换所有占位符。

## 命令行为

输入 `/epicdev <大功能描述>` 后，CodeBuddy 自动：

1. 读取知识库和规则
2. 分析大功能并拆解为最小需求单元
3. 输出拆解计划表格（plan 模式）或拆解 + 创建需求 + 顺序执行（yes 模式）
4. 每个子需求走 `/newdev` 完整闭环

## 与 `/newdev` 的区别

| 特性 | `/newdev` | `/epicdev` |
|------|----------|-----------|
| 适用场景 | 单一最小需求单元 | 大功能（多个最小需求单元的集合） |
| 流程 | 一次闭环 | 多次闭环（逐个执行） |
| TAPD 需求创建 | 创建 1 个 | 批量创建多个 |
| 分支 | 1 个功能分支 | 每个需求独立分支 |
| 报告 | 1 个闭环报告 | Epic 最终汇总报告 |

## 命令格式

```
/epicdev <大功能描述>                     # plan 模式，只拆解不执行
/epicdev --plan <大功能描述>               # plan 模式（显式）
/epicdev --yes <大功能描述>                # yes 模式，拆解 + 创建 + 顺序执行
```

## 模板内容（复制到 .codebuddy/commands/epicdev.md）

```markdown
---
description: 大功能拆解为多个最小需求单元，批量创建 TAPD 需求并顺序执行自动研发闭环
---

# /epicdev 大功能拆解与批量研发

你是本项目的 AI 研发自动化总控 Agent。

用户输入的是一个较大的功能目标，例如：

/epicdev --plan {业务示例大功能}
/epicdev --yes {业务示例大功能}
/epicdev {业务示例大功能}

## 启动前强制预检（不可跳过）

执行 `/epicdev` **之前**，必须完成以下全部预检步骤并输出结果。

### 预检步骤

1. **读取规则**：读取 `.codebuddy/rules/` 下全部规则文件（.mdc），特别关注 `EpicRequirementDecompositionRules.mdc`
2. **读取知识库**：读取 `.codebuddy/knowledge/` 下全部知识库文件
3. **输出当前仓库路径**
4. **输出当前 Git 分支**
5. **输出当前 git status**（至少摘要）
6. **输出本次大功能描述**（从用户输入中提取）
7. **判断模式**：
   - 包含 `--plan` 或无任何模式标记 → plan 模式（只拆解，不创建不开发）
   - 包含 `--yes` → yes 模式（拆解 + 创建需求 + 顺序执行闭环）
8. **判断大功能是否需要拆解**：如果已经是单一最小需求单元，提示用户用 `/newdev` 替代

### 预检输出格式

```text
/epicdev 启动前预检

- 仓库路径：
- 当前分支：
- git status：
- 已读取规则：[列出所有文件名]
- 已读取知识库：[列出所有文件名]
- 本次大功能描述：
- 执行模式：plan / yes
- 是否需要拆解：是 / 否（如果否，建议用 /newdev）
- 预检结论：通过 / 未通过（原因）
```

## 执行流程

### plan 模式（默认）

1. 读取规则和知识库
2. 分析大功能，理解其完整范围
3. 按照 `EpicRequirementDecompositionRules.mdc` 的拆解标准拆解为最小需求单元
4. 输出拆解计划表格
5. 输出执行顺序和依赖关系图
6. 输出关键风险和人工介入点
7. 等待用户确认
8. **禁止在 plan 模式下创建 TAPD 需求或修改代码**

### yes 模式

1. 执行 plan 模式的 1-6 步
2. 生成标准 TAPD 需求标题和正文
3. 按依赖顺序逐个创建 TAPD 需求
4. 每创建一个需求后，记录短 ID、完整 story_id 和链接
5. 输出创建汇总表格
6. 按依赖顺序逐个执行 `/newdev` 闭环
7. 每完成一个需求，输出该需求的闭环摘要
8. 任一需求阻塞时暂停整个批量流程
9. 所有需求完成后输出 epic 最终报告

## 批量执行约束

1. 一次最多自动执行 3 个需求
2. 默认最多拆解 5 个需求
3. 超过 5 个时询问用户是否继续拆第二批
4. 每个需求独立分支、独立 Spec、独立测试、独立 Review、独立 MR、独立归档
5. 上一个需求未完成，不允许进入下一个
6. 任一需求阻塞时，整个批量流程暂停

## 必须遵守的执行护栏

执行本命令前，必须读取并遵守：

1. `.codebuddy/rules/ExecutionGuardRules.mdc`
2. `.codebuddy/rules/HumanInterventionRules.mdc`
3. `.codebuddy/rules/EffectFeedbackLoopRules.mdc`
4. `.codebuddy/rules/ExperienceLayeringRules.mdc`
5. `.codebuddy/rules/WorkflowCompletionRules.mdc`
6. `.codebuddy/rules/AutonomousWorkflowRules.mdc`
7. `.codebuddy/rules/EpicRequirementDecompositionRules.mdc`
8. `.codebuddy/knowledge/` 下全部知识库

## 最终输出

所有需求执行完成后（或阻塞暂停时），输出 epic 最终报告。

默认参数：

- TAPD 项目 ID：{TAPD_WORKSPACE_ID}
- 默认迭代：{DEFAULT_ITERATION}
- 初始状态：待AI分析
- 优先级：高
- 目标分支：main
- 覆盖率门禁：>= 90%
- AI Code Review 门禁：>= 95
```

## 替换清单

| 占位符 | 说明 |
|--------|------|
| `{TAPD_WORKSPACE_ID}` | 你的 TAPD 项目 ID |
| `{DEFAULT_ITERATION}` | 你的默认迭代名称 |
| `{业务示例大功能}` | 替换为你的业务示例 |

## 验证

在新项目中输入 `/epicdev --plan 用户管理功能`，确认：
1. 规则和知识库已读取
2. 拆解计划表格正确输出
3. 没有创建任何 TAPD 需求或修改代码
