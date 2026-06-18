# Rules 模板说明

## 概述

`.codebuddy/rules/` 包含 7 个规则文件，驱动 CodeBuddy 遵循项目的开发规范。

## 规则文件总览

| 文件 | 用途 | 复用难度 | 说明 |
|------|------|----------|------|
| `AutonomousWorkflowRules.mdc` | 自动研发闭环总控 | ⚠️ 需改 | 替换项目ID等参数 |
| `CodingStandardRules.mdc` | 代码规范 | ⚠️ 需改 | 替换接口定义 |
| `DesignSpecRules.mdc` | Spec 规范 | ✅ 基本不改 | 通用设计规范 |
| `GitBranchRules.mdc` | 分支规范 | ⚠️ 需改 | 替换 biz_prefix |
| `SecurityRules.mdc` | 安全规范 | ✅ 不改 | 通用安全要求 |
| `UnitTestRules.mdc` | 测试规范 | ✅ 不改 | 通用测试要求 |
| `WorkflowRules.mdc` | 流程规范 | ✅ 基本不改 | 通用流程规范 |

## 详细修改指南

### 1. AutonomousWorkflowRules.mdc（必须修改）

最核心的规则文件，需要替换以下参数：

```diff
- ## 1. 目标
- 本规则用于驱动 CodeBuddy 自动完成「{BUSINESS_NAME}」的 AI 研发闭环。
+ 本规则用于驱动 CodeBuddy 自动完成「<你的项目功能>」的 AI 研发闭环。

- TAPD 项目 ID：{TAPD_WORKSPACE_ID}
+ TAPD 项目 ID：<你的项目ID>

- 默认迭代：{DEFAULT_ITERATION}
+ 默认迭代：<你的迭代名称>

- feature/{BIZ_PREFIX}-v{version}_{feature-desc}
+ feature/<biz_prefix>-v{version}_{feature-desc}
```

> **注意：** 保持规则编号和结构不变，只替换业务相关值。

### 2. CodingStandardRules.mdc（按需修改）

如果新项目使用不同的技术栈，需要重写：

```diff
- 接口路径使用 {BUSINESS_API_PREFIX}
+ 接口路径使用 <你的接口路径>

- 请求参数必须为 <你的参数定义>
+ <你的需求边界>
```

### 3. GitBranchRules.mdc（简单替换）

```diff
- {BIZ_PREFIX}
+ <你的业务前缀>
```

### 4. DesignSpecRules.mdc（基本不改）

Spec 的设计规范是通用的，通常不需要修改。

### 5. SecurityRules.mdc（不改）

安全规范是通用的，适用于任何项目。

### 6. UnitTestRules.mdc（基本不改）

测试规范通用，按项目技术栈调整测试命令。

### 7. WorkflowRules.mdc（基本不改）

工作流程通用：读取需求 → Spec → 分支 → 实现 → 测试 → Review → MR → 归档。

## 修改后验证

1. 检查所有规则文件中的 TAPD 项目 ID 是否已替换
2. 检查所有规则文件中的迭代名称是否已替换
3. 检查 biz_prefix 是否一致
4. 检查接口路径是否与新项目匹配
5. 过时的参考项目示例是否已替换
