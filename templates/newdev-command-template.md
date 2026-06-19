# /newdev 命令模板

## 概述

`/newdev` 是 CodeBuddy 命令，用于创建 TAPD 需求并自动执行完整研发闭环。

## 文件配置

将此内容复制到 `.codebuddy/commands/newdev.md`，替换所有占位符。

## 命令行为

输入 `/newdev <需求主题>` 后，CodeBuddy 自动：

1. 读取知识库和规则
2. 生成标准 TAPD 需求标题和正文
3. 展示预览等待用户确认（或 `--yes` 跳过确认）
4. 通过 TAPD MCP 创建需求
5. 自动启动完整研发闭环

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

请执行以下流程：

1. 读取 `.codebuddy/knowledge` 下的项目知识库
2. 读取 `.codebuddy/rules` 下的全部规则
3. 特别遵守 `.codebuddy/rules/AutonomousWorkflowRules.mdc` 和 `.codebuddy/rules/HumanInterventionRules.mdc`
4. 从用户输入中提取需求主题
5. 判断该主题是否可以作为一个最小需求单元
6. 如果过大，拆分为多个最小需求并等待用户选择
7. 如果符合最小需求单元，生成 TAPD 标题和标准需求正文
8. 如果用户没有输入 --yes，先展示标题和正文，等待用户确认
9. 如果用户输入了 --yes，则直接创建 TAPD 需求
10. 优先使用 TAPD MCP 创建需求
11. 创建成功后，读取新需求，获取短需求 ID 和完整 story_id
12. 自动启动该需求的完整研发闭环
13. 自动生成 Spec
14. 自动实现代码
15. 自动编写或更新测试
16. 自动运行测试和覆盖率
17. 自动执行 AI Code Review
18. 自动修复 Low / Medium 问题
19. Critical 问题必须暂停
20. 自动生成 Review 报告和 TAPD 归档 JSON
21. 自动 commit 和 push
22. 自动创建 MR
23. 等待 CNB 状态检查
24. 状态检查通过后自动合并 MR
25. 合并后确认 main push 流水线成功
26. 确认 TAPD 自动归档为"已完成"

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

最终只输出：

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
```

## 替换清单

| 占位符 | 说明 |
|--------|------|
| `{TAPD_WORKSPACE_ID}` | 你的 TAPD 项目 ID |
| `{DEFAULT_ITERATION}` | 你的默认迭代名称 |
| 示例命令中的业务描述 | 替换为你的业务示例 |

## 验证

在新项目中输入 `/newdev --yes hello world 测试`，确认完整闭环自动执行。
