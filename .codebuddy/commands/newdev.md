---
description: 创建 TAPD 需求并自动完成 Spec、开发、测试、Review、MR 和自动合并。模板仓库自用版，包含 validate_template.py 自检。
---

# /newdev 创建并开发 TAPD 需求

你是本项目的 AI 研发自动化总控 Agent。

当前工作区为 **ai-dev-workflow-template 模板仓库**。

用户输入的是一个需求主题，例如：

/newdev 增加人工介入断点规则

或者：

/newdev --yes 增加人工介入断点规则

## 启动前强制预检

执行前必须输出：

1. `.codebuddy/rules/` 已读取规则文件清单
2. `.codebuddy/knowledge/` 已读取知识库文件清单（如果存在）
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

1. 读取 `.codebuddy/knowledge` 下的项目知识库（如果存在）
2. 读取 `.codebuddy/rules` 下的全部规则
3. 特别遵守以下规则文件：
   - `AutonomousWorkflowRules.mdc`
   - `ExecutionGuardRules.mdc`
   - `EffectFeedbackLoopRules.mdc`
   - `ExperienceLayeringRules.mdc`
   - `WorkflowCompletionRules.mdc`
   - `HumanInterventionRules.mdc`
   - `AutoMergeFallbackRules.mdc`
4. 从用户输入中提取需求主题
5. 判断该主题是否可以作为一个最小需求单元
6. 如果过大，拆分为多个最小需求并等待用户选择
7. 如果符合最小需求单元，生成 TAPD 标题和标准需求正文
8. 如果用户没有输入 --yes，先展示标题和正文，等待用户确认
9. 如果用户输入了 --yes，则直接创建 TAPD 需求
10. 优先使用 TAPD MCP 创建需求（create_story_or_task）
11. 创建成功后，读取新需求，获取短需求 ID 和完整 story_id
12. 自动启动该需求的完整研发闭环
13. 自动生成 Spec
14. 自动实现代码（规则/命令/模板/文档修改）
15. 自动运行模板自检：`python scripts/validate_template.py`
16. 自动执行 AI Code Review
17. 自动修复 Low / Medium 问题
18. Critical 问题必须暂停（参照 HumanInterventionRules）
19. 自动 commit 和 push
20. 自动创建 MR
21. 等待 CNB 状态检查
22. 状态检查通过后自动合并 MR
23. 如果合并失败 → 进入 `AutoMergeFallbackRules.mdc` §4 自动修复（最多 3 轮）→ 修复成功后重新合并
24. 如果 PR 流水线通过但 MR 未自动合并，进入 `AutoMergeFallbackRules.mdc` 执行兜底合并
25. 合并后确认 main push 流水线成功（如果失败 → 进入 `AutoMergeFallbackRules.mdc` §4.1 第 4 类自动修复）
26. 执行经验分层沉淀检查（参照 ExperienceLayeringRules）
27. 输出完整闭环报告

## 模板仓库专属收尾检查

模板仓库完成前必须执行：

- `python scripts/validate_template.py` — 确保模板文件完整性
- 检查 `.cnb.yml` 是否不包含业务占位符
- 检查 `templates/` 目录结构完整性
- 检查无敏感信息泄露

## 默认参数

- TAPD 项目 ID：{TAPD_WORKSPACE_ID}
- 默认迭代：{DEFAULT_ITERATION}
- 初始状态：待AI分析
- 优先级：高
- 目标分支：main
- 覆盖率门禁：>= 90%
- AI Code Review 门禁：>= 95
- 允许自动合并：是
- 自动合并前必须确认状态检查通过

## 最终输出闭环报告

包含：

1. TAPD 需求标题 / 短需求 ID / 完整 story_id
2. 状态流转记录
3. 分支名 / Spec 路径
4. 修改文件摘要
5. validate_template.py 自检结果
6. AI Review 分数
7. MR 链接 / 是否自动合并
8. CNB PR 流水线 / main push 流水线状态
9. 经验沉淀结果
10. 结论（成功/失败/需要人工处理的事项）
