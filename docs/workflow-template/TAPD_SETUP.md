# TAPD 配置指南

## 概述

TAPD 是 AI 研发自动化闭环的需求管理入口和状态同步目标。

## 1. TAPD 项目创建

### 1.1 创建新项目

在 TAPD 中创建项目后，获取 `workspace_id`（在 URL 中可见）：

```
https://www.tapd.cn/<workspace_id>/...
```

### 1.2 创建迭代

创建第一个迭代（例如 `v0.1.0-mvp`），获取 `iteration_id`。

> **参考：** 爱穿搭项目使用 `tryon-v0.1.0-mvp`。

### 1.3 配置需求类型

确认使用默认的「需求 (stories)」类型。如果创建自定义类型，需要同步更新 Rules 中的 `entity_type`。

## 2. 状态流转配置

### 2.1 需要的自定义状态

| 状态 | 用途 | 阶段 |
|------|------|------|
| **待AI分析** | 需求等待 AI 处理 | 入口 |
| **AI生成Spec中** | AI 正在编写设计文档 | Spec |
| **AI开发中** | AI 正在编写代码 | 实现 |
| **AI测试中** | AI 正在运行测试 | 测试 |
| **AI审核中** | AI 正在执行 Code Review | Review |
| **AI自动修复中** | AI 正在修复 Review 问题 | 修复 |
| **待自动合并** | MR 已创建等待状态检查 | 合并 |
| **已合并** | MR 已成功合并到 main | 归档 |
| **已完成** | 完整闭环归档完成 | 终态 |

### 2.2 配置方法

1. TAPD 项目 → 设置 → 需求类型 → 编辑状态
2. 按序添加上表的自定义状态
3. 确保状态流转方向正确

### 2.3 与 Rules 的对应关系

`AutonomousWorkflowRules.mdc` 中的状态名称必须与 TAPD 中配置的名称**完全一致**：

```
待AI分析 → AI生成Spec中 → AI开发中 → AI测试中 → AI审核中 → AI自动修复中 → 待自动合并 → 已合并 → 已完成
```

## 3. 需求模板

### 3.1 最小需求单元模板

每个 TAPD 需求应包含以下字段：

```markdown
## User Story
作为 <角色>，我希望 <功能>，以便 <价值>

## 最小需求单元
<是/否>。<说明>

## 本次只做
1. ...
2. ...

## 本次不做
- ...

## 输入
- ...

## 输出
- ...

## 验收标准
1. ...
2. ...

## AI 执行要求
- 必须使用 AutonomousWorkflowRules 自动研发闭环执行

## 自动化状态字段
- 初始状态：待AI分析
- 迭代：<迭代名>
- 优先级：高
```

### 3.2 需求拆分原则

当需求涉及以下多个维度时，必须拆分：
- 多个 API 接口
- 前端 + 后端
- 业务逻辑 + 持久化
- 多个独立功能模块

每个需求只完成一个最小功能单元。

## 4. TAPD MCP 配置

### 4.1 CodeBuddy MCP 连接

在 CodeBuddy IDE 中确保 TAPD MCP Server 已连接并配置正确的 workspace_id。

### 4.2 支持的工具

| 工具 | 用途 |
|------|------|
| `create_story_or_task` | 创建需求 |
| `get_stories_or_tasks` | 查询需求 |
| `update_story_or_task` | 更新需求状态/内容 |
| `get_iterations` | 查询迭代信息 |
| `get_workflows_status_map` | 查询状态流转映射 |
| `create_comments` | 添加归档评论 |

### 4.3 API 归档凭证

CNB 流水线中通过密钥仓库注入以下环境变量：

```yaml
TAPD_API_BASE_URL: https://api.tapd.cn
TAPD_API_USER: <API 用户>
TAPD_API_PASSWORD: <API 密码>
TAPD_COMMENT_AUTHOR: <评论作者名>
TAPD_ARCHIVE_ENABLED: "true"
```

## 5. 爱穿搭项目参考值（供对比）

| 配置项 | 爱穿搭项目值 | 新项目替换为 |
|--------|-------------|-------------|
| workspace_id | `31917999` | `<你的项目ID>` |
| iteration | `tryon-v0.1.0-mvp` | `<你的迭代名>` |
| entity_type | `stories` | 保持 `stories` |
| 初始状态 | `待AI分析` | 保持一致 |
| 优先级 | `高` | 按需调整 |

## 6. 常见问题

**Q: 状态名称可以用英文吗？**
A: 可以，但必须与 Rules 中使用的名称完全一致。

**Q: 如果项目已经有很多自定义状态怎么办？**
A: 至少需要配置表中的 9 个状态。可以复用已有的语义等价状态，同时更新 Rules 中的名称。

**Q: API 归档失败怎么办？**
A: 检查 `TAPD_API_USER` / `TAPD_API_PASSWORD` 是否有正确的 TAPD API 权限。
