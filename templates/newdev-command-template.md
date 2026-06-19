# /newdev 命令模板

## 概述

`/newdev` 是 CodeBuddy 命令，用于创建 TAPD 需求并自动执行完整研发闭环。

## 文件配置

将此内容复制到 `.codebuddy/commands/newdev.md`，替换所有占位符。

## 启动前强制预检

CodeBuddy 执行 `/newdev` 前必须先输出以下检查结果：

| # | 检查项 | 说明 |
|---|--------|------|
| 1 | 读取 `.codebuddy/rules/` | 列出全部已读取规则文件 |
| 2 | 读取 `.codebuddy/knowledge/` | 列出全部已读取知识库文件 |
| 3 | 当前仓库路径 | 输出工作目录绝对路径 |
| 4 | 当前分支 | `git branch --show-current` |
| 5 | git status | 是否有未提交改动、未跟踪文件 |
| 6 | 是否需要创建 TAPD 需求 | 判断是已有需求还是 `/newdev` 创建 |
| 7 | 是否需要创建分支 | 当前在 main 则必须创建；在功能分支则可继续 |
| 8 | 是否需要 commit / push / MR | 判断当前工作区状态 |
| 9 | 最终必须输出闭环报告 | 每个操作完成后必须输出完整报告 |

如果未读取规则和知识库，不允许开始 `/newdev` 流程。

## 命令行为

输入 `/newdev <需求主题>` 后，CodeBuddy 自动：

1. 执行上述启动前强制预检
2. 读取知识库和规则
3. 生成标准 TAPD 需求标题和正文
4. 展示预览等待用户确认（或 `--yes` 跳过确认）
5. 通过 TAPD MCP 创建需求
6. 自动启动完整研发闭环

## 命令格式

```
/newdev <需求主题描述>
/newdev --yes <需求主题描述>        # 跳过确认直接创建
```

---

## 模板内容（复制到 .codebuddy/commands/newdev.md）

```markdown
---
description: 创建 TAPD 需求并自动完成 Spec、开发、测试、Review、MR 和自动合并
---

# /newdev 创建并开发 TAPD 需求

你是本项目的 AI 研发自动化总控 Agent。

用户输入的是一个需求主题，例如：

/newdev 增加用户登录接口

或者：

/newdev --yes 增加用户登录接口

## 启动前强制预检

执行前必须输出：

1. `.codebuddy/rules/` 已读取规则文件清单
2. `.codebuddy/knowledge/` 已读取知识库文件清单
3. 当前仓库路径
4. 当前分支
5. 当前 git status
6. 是否需要创建 TAPD 需求
7. 是否需要创建分支
8. 是否需要 commit / push / MR
9. 最终必须输出闭环报告

未读取规则和知识库，不允许开始流程。

## 执行流程

请执行以下流程：

1. 读取 `.codebuddy/knowledge` 下的项目知识库
2. 读取 `.codebuddy/rules` 下的全部规则
3. 特别遵守 `.codebuddy/rules/AutonomousWorkflowRules.mdc`
4. 特别遵守 `.codebuddy/rules/ExecutionGuardRules.mdc`
5. 特别遵守 `.codebuddy/rules/EffectFeedbackLoopRules.mdc`
6. 特别遵守 `.codebuddy/rules/ExperienceLayeringRules.mdc`
7. 特别遵守 `.codebuddy/rules/WorkflowCompletionRules.mdc`
8. 从用户输入中提取需求主题
9. 判断该主题是否可以作为一个最小需求单元
10. 如果过大，拆分为多个最小需求并等待用户选择
11. 如果符合最小需求单元，生成 TAPD 标题和标准需求正文
12. 如果用户没有输入 --yes，先展示标题和正文，等待用户确认
13. 如果用户输入了 --yes，则直接创建 TAPD 需求
14. 优先使用 TAPD MCP 创建需求
15. 创建成功后，读取新需求，获取短需求 ID 和完整 story_id
16. 自动启动该需求的完整研发闭环
17. 自动生成 Spec
18. 自动实现代码
19. 自动编写或更新测试
20. 自动运行测试和覆盖率
21. 自动执行 AI Code Review
22. 自动修复 Low / Medium 问题
23. Critical 问题必须暂停
24. 自动生成 Review 报告和 TAPD 归档 JSON
25. 自动 commit 和 push
26. 自动创建 MR
27. 等待 CNB 状态检查
28. 状态检查通过后自动合并 MR
29. 合并后确认 main push 流水线成功
30. 确认 TAPD 自动归档为「已完成」
31. 执行经验分层沉淀检查
32. 输出完整闭环报告

默认参数：

- TAPD 项目 ID：{TAPD_WORKSPACE_ID}
- 默认迭代：{DEFAULT_ITERATION}
- 初始状态：待AI分析
- 优先级：高
- 目标分支：main
- 覆盖率门禁：>= 90%
- AI Code Review 门禁：>= 95
- 允许自动合并：是
- 自动合并前必须确认状态检查通过

最终输出闭环报告，包含：

1. TAPD 需求标题
2. TAPD 短需求 ID
3. TAPD 完整 story_id
4. 分支名
5. Spec 路径
6. 测试结果
7. 覆盖率
8. AI Review 分数
9. MR 链接
10. 是否已自动合并
11. TAPD 是否已归档完成
12. 经验沉淀结果
```

## 替换清单

| 占位符 | 说明 |
|--------|------|
| `{TAPD_WORKSPACE_ID}` | 你的 TAPD 项目 ID |
| `{DEFAULT_ITERATION}` | 你的默认迭代名称 |
| 示例命令中的业务描述 | 替换为你的业务示例 |

## 验证

在新项目中输入 `/newdev --yes hello world 测试`，确认完整闭环自动执行。
