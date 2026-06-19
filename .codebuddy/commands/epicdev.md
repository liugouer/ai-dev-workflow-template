# /epicdev 命令 — 大功能拆解与批量执行

## 用途

将大功能目标拆解为多个最小需求单元，创建 TAPD 需求，并按顺序自动执行每个需求的完整研发闭环。

本文件是模板仓库自身的 `/epicdev` 命令入口。

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

必须先行读取：

* `.codebuddy/rules/` 下所有 `.mdc` 文件（特别是 `EpicRequirementDecompositionRules.mdc`）
* `.codebuddy/knowledge/` 下所有 `.md` 文件
* `.codebuddy/commands/` 下的命令文件

## 执行流程

### 第一步：拆解大功能

1. 读取 `EpicRequirementDecompositionRules.mdc`
2. 分析用户输入的大功能描述
3. 将大功能拆解为最小需求单元（默认不超过 5 个）
4. 输出拆解计划表格（包含序号、需求标题、类型、目标、改动范围、验收标准、依赖关系、可自动执行、需人工介入、风险等级）
5. 如果大功能过于复杂（>5 个需求），提示用户确认是否继续拆第二批

### 第二步：用户确认

- 如果是 `--plan` 模式：仅输出拆解计划，等待用户确认
- 如果是 `--yes` 模式：直接进入执行
- 默认模式（无标志）：输出拆解计划等待用户确认后执行

### 第三步：创建 TAPD 需求

确认执行后，使用 TAPD MCP `create_story_or_task` 逐个创建需求：

* `entity_type`: `"stories"`
* `workspace_id`: `{TAPD_WORKSPACE_ID}`
* `name`: 拆解后的需求标题
* `description`: 需求正文（含背景、范围、验收标准、非目标）
* `status`: `"待AI分析"`
* `iteration`: `{DEFAULT_ITERATION}`

创建后记录每个需求的短 ID、完整 story_id 和 TAPD 链接。

### 第四步：顺序执行需求闭环

按依赖顺序逐个执行每个需求的完整研发闭环：

1. 读取 TAPD 需求
2. 生成 Spec
3. 创建分支
4. 代码实现
5. 测试与覆盖率
6. AI Code Review
7. 自动修复（如需要）
8. Commit & Push
9. 创建 MR
10. CNB 检查
11. 自动合并（如 PR 流水线通过但未自动合并，进入 `AutoMergeFallbackRules.mdc` 兜底；如合并失败，先进入 §4 自动修复，最多 3 轮）
12. TAPD 归档

**每个需求必须走完完整闭环后才能进入下一个需求。**

### 第五步：分批执行

- 一次最多自动执行 3 个需求
- 超过 3 个需求时，分批次执行
- 批次之间输出中间报告

### 第六步：模板仓库专属收尾检查

因为当前仓库是模板仓库，完成前必须执行：

```
python scripts/validate_template.py
```

## 必须遵守的规则

1. `EpicRequirementDecompositionRules.mdc` — 大功能拆解规则
2. `AutonomousWorkflowRules.mdc` — 总控规则
3. `ExecutionGuardRules.mdc` — 执行护栏
4. `EffectFeedbackLoopRules.mdc` — 效果反馈修复闭环
5. `ExperienceLayeringRules.mdc` — 经验分层沉淀
6. `WorkflowCompletionRules.mdc` — 闭环完成判定
7. `AutoMergeFallbackRules.mdc` — 自动合并兜底规则
8. `HumanInterventionRules.mdc` — 人工介入断点

## 人工介入

遇到以下情况必须暂停并输出人工介入清单：

1. 大功能无法清晰拆解为最小需求单元
2. 需要配置密钥、授权 MCP
3. 涉及支付、登录、用户隐私、生产数据
4. 连续 3 次测试失败
5. CNB 或 TAPD 权限不足
6. 其他 `HumanInterventionRules.mdc` 中定义的暂停条件

暂停时 TAPD 状态更新为 `阻塞-需人工处理`。

## 最终报告

执行结束后输出：

1. 原始大功能描述
2. 拆解出的需求数量
3. 已创建的需求列表（标题 + ID）
4. 每个需求的状态、MR 链接、CNB 状态、TAPD 归档状态
5. 经验沉淀情况
6. 剩余未执行需求
7. 人工介入事项
