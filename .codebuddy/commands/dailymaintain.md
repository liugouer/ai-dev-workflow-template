# /dailymaintain 命令

## 命名空间

`/dailymaintain`

## 触发语

以下自然语言也识别为本命令：

- `/dailymaintain`
- `执行今日维护`
- `检查今日研发闭环状态`
- `每日检查`
- `今天有什么需要处理的`

## 检查清单

CodeBuddy 必须执行以下 10 项检查：

| # | 检查项 | 操作 |
|---|--------|------|
| 1 | 当前未完成 TAPD 需求 | 查询所有非「已完成」需求 |
| 2 | 当前阻塞 TAPD 需求 | 查询「阻塞-需人工处理」需求 |
| 3 | 当前未合并 MR | 查询所有 open MR |
| 4 | 当前失败 CNB 流水线 | 检查 PR/Push 流水线状态 |
| 5 | 当前未提交文件 | `git status` |
| 6 | 当前未 push commit | `git log --branches --not --remotes` |
| 7 | 当前知识库是否需要更新 | 对比 commit 时间与知识库更新时间 |
| 8 | 当前是否产生通用经验 | 检查 `.codebuddy/knowledge/` 更新差异 |
| 9 | 是否需要同步模板仓库 | 通用经验是否已达同步阈值 |
| 10 | 是否存在人工介入事项 | 依据 `HumanInterventionRules.mdc` |

## 默认参数

- TAPD 项目 ID：{TAPD_WORKSPACE_ID}
- 默认迭代：{DEFAULT_ITERATION}

## 执行要求

1. 执行前必须读取 `.codebuddy/rules/IterationLifecycleRules.mdc` §5
2. 执行前必须读取 `.codebuddy/rules/` 下全部规则
3. 执行前必须读取 `.codebuddy/knowledge/` 下全部知识库
4. 发现可自动修复问题 → 进入修复闭环
5. 发现需人工处理问题 → 进入 `HumanInterventionRules.mdc`
6. 修复后必须重新运行本地验证（pytest + 覆盖率）
7. 维护结束必须输出维护报告
8. 必须遵守 `ExecutionGuardRules.mdc` 执行护栏

## 自动修复规则

- 未提交文件 → `git add . && git commit -m "chore: daily maintain auto-fix"`
- 未 push → `git push`
- 测试失败且可自动修复 → 依据 `EffectFeedbackLoopRules.mdc` 修复
- 同一问题连续修复 3 次仍失败 → 暂停，转入人工介入

## 维护报告格式

```text
每日维护报告

检查时间：YYYY-MM-DD HH:MM
迭代版本：{version}

检查结果：
- [✅/⚠️/❌] 未完成 TAPD 需求：
- [✅/⚠️/❌] 阻塞需求：
- [✅/⚠️/❌] 未合并 MR：
- [✅/⚠️/❌] 失败流水线：
- [✅/⚠️/❌] 未提交文件：
- [✅/⚠️/❌] 未 push commit：
- [✅/⚠️/❌] 知识库状态：
- [✅/⚠️/❌] 通用经验：
- [✅/⚠️/❌] 模板同步：
- [✅/⚠️/❌] 人工介入：

自动修复记录：

迭代进度：n/m 需求已完成

需人工处理：

下一步建议：
```

## 禁止行为

1. 禁止跳过检查直接报告一切正常
2. 禁止发现问题不尝试修复直接转入人工
3. 禁止隐瞒失败信息
4. 禁止在无 MR 情况下报告 MR 正常
5. 禁止跳过规则和知识库读取
