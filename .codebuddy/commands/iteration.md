# /iteration 命令

## 命名空间

`/iteration`

## 命令变体

| 命令 | 说明 | 规则引用 |
|------|------|----------|
| `/iteration --start {version}` | 启动迭代 | IterationLifecycleRules.mdc §2 |
| `/iteration --status [version]` | 检查迭代状态 | IterationLifecycleRules.mdc §3 |
| `/iteration --release {version}` | 收口迭代 | IterationLifecycleRules.mdc §6 |

## 触发语

以下自然语言也识别为本命令：

- `启动 {version} 迭代` → `/iteration --start`
- `开始 {version} 迭代` → `/iteration --start`
- `查询迭代状态` → `/iteration --status`
- `检查迭代进度` → `/iteration --status`
- `收口 {version} 迭代` → `/iteration --release`
- `完成 {version} 迭代` → `/iteration --release`
- `发布 {version} 迭代` → `/iteration --release`

## 默认参数

- TAPD 项目 ID：{TAPD_WORKSPACE_ID}
- 默认迭代：{DEFAULT_ITERATION}
- 目标分支：main

## 执行要求

1. 执行前必须读取 `.codebuddy/rules/IterationLifecycleRules.mdc`
2. 执行前必须读取 `.codebuddy/rules/` 下全部规则
3. 执行前必须读取 `.codebuddy/knowledge/` 下全部知识库
4. 迭代启动（--start）必须先拆解再输出计划，等待用户确认
5. 迭代状态（--status）必须输出完整状态报告
6. 迭代收口（--release）必须满足全部完成条件才允许标记完成
7. 所有阶段必须遵守 `ExecutionGuardRules.mdc` 执行护栏

## 禁止行为

1. 禁止跳过规则和知识库读取
2. 禁止在迭代启动未确认时直接创建需求
3. 禁止在未收口时启动下一迭代
4. 禁止在未完成需求时标记迭代收口
5. 禁止跳过经验沉淀
6. 禁止在多迭代并行时混淆需求归属
