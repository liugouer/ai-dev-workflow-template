---
description: 每日维护命令模板，检查未完成需求、未合并 MR、失败流水线、未提交代码、知识库同步状态、经验沉淀状态
---

# /dailymaintain 每日维护

你是本项目的 AI 研发自动化总控 Agent。

用户执行每日维护检查，例如：

```
/dailymaintain
执行今日维护
检查今日研发闭环状态
```

## 启动前强制预检（不可跳过）

执行 `/dailymaintain` **之前**，必须完成以下全部预检步骤并输出结果。

### 预检步骤

1. **读取规则**：读取 `.codebuddy/rules/` 下全部规则文件（.mdc），特别关注 `IterationLifecycleRules.mdc`
2. **读取知识库**：读取 `.codebuddy/knowledge/` 下全部知识库文件
3. **输出当前仓库路径**
4. **输出当前 Git 分支**
5. **输出当前 git status**（至少摘要）
6. **输出当前日期**

---

## 执行流程

预检通过后，按以下顺序逐项检查：

### 1. TAPD 需求检查

- 查询所有非「已完成」状态的 TAPD 需求
- 列出每项需求：ID、标题、当前状态、所属迭代
- 标记状态为「阻塞-需人工处理」的需求

### 2. MR 检查

- 查询所有未合并 MR（state = "open"）
- 列出每项 MR
- **如果 MR 满足自动合并条件，自动调用 `cnb_merge_pull` 合并**
- 如果不满足，输出原因

### 3. CNB 流水线检查

- 检查最近 pull_request 和 push 流水线状态
- **如果流水线失败，分析原因并尝试自动修复**
- 如果是环境配置问题，进入 HumanInterventionRules

### 4. Git 状态检查

- 检查未提交改动（git status）
- **如果有待提交的完整改动，自动 commit**
- 检查未 push 的 commit
- **如果有未 push 的 commit，自动 push 到当前分支**

### 5. 知识库同步检查

- 对比 `.codebuddy/knowledge/` 与实际代码/接口/架构
- **如果发现不一致，自动更新知识库对应文件**

### 6. 经验沉淀检查

- 检查是否有未同步的通用经验建议
- 提示用户同步到 `ai-dev-workflow-template`

### 7. 人工介入事项检查

- 汇总所有需要人工处理的事项
- 如果有，按 HumanInterventionRules 格式输出

---

## 输出格式

执行完成后，输出完整的每日维护报告（详见 IterationLifecycleRules.mdc 第 4.4 节）。

---

## 必须遵守的执行护栏

1. `.codebuddy/rules/ExecutionGuardRules.mdc`
2. `.codebuddy/rules/HumanInterventionRules.mdc`
3. `.codebuddy/rules/IterationLifecycleRules.mdc`
4. `.codebuddy/rules/EffectFeedbackLoopRules.mdc`
5. `.codebuddy/rules/AutonomousWorkflowRules.mdc`
6. `.codebuddy/rules/ExperienceLayeringRules.mdc`
7. `.codebuddy/rules/WorkflowCompletionRules.mdc`
8. `.codebuddy/knowledge/` 下全部知识库

---

## 禁止行为

1. 禁止跳过任何检查项
2. 禁止在未检查 MR 门禁前自动合并
3. 禁止在未确认安全前自动 push
4. 禁止在 main 分支直接修改代码
5. 禁止忽略人工介入事项
