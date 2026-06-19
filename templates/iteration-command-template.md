---
description: 迭代生命周期命令模板，支持迭代启动、状态查询和版本收口
---

# /iteration 迭代生命周期管理

你是本项目的 AI 研发自动化总控 Agent。

用户输入的是迭代管理命令，例如：

```
/iteration --start v0.1.0
/iteration --release v0.1.0
/iteration --status
启动 v0.1.0 迭代
收口 v0.1.0 迭代
查看迭代状态
```

## 启动前强制预检（不可跳过）

执行 `/iteration` **之前**，必须完成以下全部预检步骤并输出结果。

### 预检步骤

1. **读取规则**：读取 `.codebuddy/rules/` 下全部规则文件（.mdc），特别关注 `IterationLifecycleRules.mdc`
2. **读取知识库**：读取 `.codebuddy/knowledge/` 下全部知识库文件
3. **输出当前仓库路径**
4. **输出当前 Git 分支**
5. **输出当前 git status**（至少摘要）
6. **判断子命令**：`--start` / `--release` / `--status`
7. **输出当前业务现状**（从知识库提取）

---

## 执行流程

### `--start {version}` — 迭代启动

1. 读取全部规则和知识库
2. 输出当前业务现状摘要
3. 明确本轮迭代目标和非目标
4. 检查 TAPD 项目是否存在
5. 检查 TAPD 目标迭代是否存在
6. 检查 CNB MCP、TAPD MCP 是否可用
7. 检查密钥配置是否就绪
8. 拆解本轮最小需求单元
9. 输出拆解需求清单和执行顺序表格
10. 标记人工介入点
11. **等待用户确认后再创建 TAPD 需求**
12. 用户确认后，批量创建 TAPD 需求（状态 = "待AI分析"）
13. 输出创建汇总

### `--release {version}` — 迭代收口

1. 检查本轮 TAPD 需求是否全部完成
2. 检查所有 MR 是否合并
3. 检查 main push 流水线是否通过
4. 检查 TAPD 是否全部归档
5. 检查业务知识库是否已更新
6. 检查是否产生通用经验
7. 生成版本变更记录
8. 生成迭代归档报告
9. 输出下一轮迭代建议

### `--status` — 状态查询

1. 查询当前迭代所有 TAPD 需求
2. 统计各状态需求数量
3. 查询当前未合并 MR
4. 检查最近 CNB 流水线状态
5. 计算迭代进度
6. 输出完整状态报告

---

## 必须遵守的执行护栏

1. `.codebuddy/rules/ExecutionGuardRules.mdc`
2. `.codebuddy/rules/HumanInterventionRules.mdc`
3. `.codebuddy/rules/IterationLifecycleRules.mdc`
4. `.codebuddy/rules/EpicRequirementDecompositionRules.mdc`
5. `.codebuddy/rules/AutonomousWorkflowRules.mdc`
6. `.codebuddy/rules/ExperienceLayeringRules.mdc`
7. `.codebuddy/rules/WorkflowCompletionRules.mdc`
8. `.codebuddy/knowledge/` 下全部知识库

---

## 禁止行为

1. 禁止在未确认迭代范围前直接创建需求
2. 禁止在未检查环境和配置前开始开发
3. 禁止在存在未完成需求时报告版本完成
4. 禁止跳过任何检查项
5. 禁止在 main 分支直接开发
