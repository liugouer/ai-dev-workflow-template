# CodeBuddy 配置指南

## 概述

CodeBuddy 是 AI 研发自动化闭环的执行引擎，通过 MCP 连接 TAPD 和 CNB，通过 Rules 和 Knowledge 驱动自动决策。

## 1. MCP 连接配置

### 1.1 TAPD MCP Server

用于创建/读取/更新 TAPD 需求，同步状态流转。

### 1.2 CNB MCP Server

用于创建 MR、合并 MR、管理仓库。

### 1.3 验证连接

在 CodeBuddy 中测试：
```
查询 TAPD 项目 {你的项目ID} 的需求
```
确认能正常返回结果。

## 2. 目录结构

新项目必须创建以下 CodeBuddy 目录结构：

```
.codebuddy/
├── rules/
│   ├── AutonomousWorkflowRules.mdc   # 总控规则（必须替换项目ID等参数）
│   ├── CodingStandardRules.mdc       # 代码规范（按需替换业务接口）
│   ├── DesignSpecRules.mdc           # Spec 规范（通常不需大改）
│   ├── GitBranchRules.mdc            # 分支规范（替换 biz_prefix）
│   ├── SecurityRules.mdc             # 安全规范（通常不需改）
│   ├── UnitTestRules.mdc             # 测试规范（通常不需改）
│   └── WorkflowRules.mdc             # 流程规范（通常不需改）
├── knowledge/
│   ├── 01_项目概述.md                # 必须全部重写
│   ├── 02_架构设计.md                # 必须全部重写
│   ├── 03_核心模块.md                # 必须全部重写
│   ├── 04_接口规范.md                # 必须全部重写
│   └── 05_开发指南.md                # 必须全部重写
├── commands/
│   └── newdev.md                     # /newdev 命令（替换默认参数）
└── automations/                      # 自动化任务（可选）
```

## 3. Rules 配置详情

### 3.1 AutonomousWorkflowRules.mdc 必须替换的参数

```yaml
# 原始（模板占位符）
TAPD 项目 ID：{TAPD_WORKSPACE_ID}
默认迭代：{DEFAULT_ITERATION}
分支前缀：{BIZ_PREFIX}

# 替换为你的实际值
TAPD 项目 ID：<你的项目ID>
默认迭代：<你的迭代名>
分支前缀：<你的项目缩写>
```

### 3.2 CodingStandardRules.mdc 必须替换的部分

- **接口路径**: `{BUSINESS_API_PREFIX}` → 新项目接口
- **响应格式**: 按新项目规范修改
- **当前需求边界**: 按新项目需求更新

### 3.3 GitBranchRules.mdc 必须替换

```
feature/{BIZ_PREFIX}-v{version}_{feature_desc}
```

将 `{BIZ_PREFIX}` 替换为新项目的业务前缀。

### 3.4 不需要修改的 Rules

- `SecurityRules.mdc` — 安全规则通用
- `UnitTestRules.mdc` — 测试规范通用
- `WorkflowRules.mdc` — 流程规范通用
- `DesignSpecRules.mdc` — Spec 规范通用（按需微调）

## 4. Knowledge 知识库配置

**知识库是 CodeBuddy 了解项目业务的唯一途径，必须完整、准确。**

详见 [knowledge-template.md](./knowledge-template.md)。

### 4.1 编写原则

1. 每篇精炼准确
2. 包含具体的接口定义、目录结构、模块职责
3. 不得包含密钥、Token、真实用户数据
4. 描述当前阶段的架构，不要写"未来规划"

### 4.2 典型问题

| 问题 | 影响 |
|------|------|
| 知识库过旧未更新 | AI 按过时信息生成错误代码 |
| 接口描述不完整 | AI 可能实现出不符合规范的接口 |
| 缺少目录结构 | AI 可能把代码放到错误位置 |

## 5. /newdev 命令配置

### 5.1 文件位置

```
.codebuddy/commands/newdev.md
```

### 5.2 必须替换的参数

```diff
- TAPD 项目 ID：{TAPD_WORKSPACE_ID}
+ TAPD 项目 ID：<你的项目ID>

- 默认迭代：{DEFAULT_ITERATION}
+ 默认迭代：<你的迭代名称>
```

### 5.3 命令行为

输入 `/newdev xxx` 后，CodeBuddy 会：
1. 读取知识库和规则
2. 生成 TAPD 需求标题和正文
3. (非 `--yes`) 展示预览等待确认
4. 创建 TAPD 需求
5. 自动执行完整研发闭环

## 6. 爱穿搭项目参考（供对比）

### Rules 中需要替换的值

| 文件 | 参数 | 原值 | 说明 |
|------|------|------|------|
| AutonomousWorkflowRules.mdc | TAPD 项目 ID | `31917999` | 项目唯一标识 |
| AutonomousWorkflowRules.mdc | 默认迭代 | `tryon-v0.1.0-mvp` | 迭代名称 |
| AutonomousWorkflowRules.mdc | biz_prefix | `tryon` | 分支前缀 |
| CodingStandardRules.mdc | 接口路径 | `/api/tryon` | API 路径 |
| GitBranchRules.mdc | biz_prefix | `tryon` | 分支前缀 |
