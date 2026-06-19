# AI 研发自动化工作流模板仓库

## 这是什么？

本仓库是一套**通用 AI 研发自动化闭环工作流模板**，从「爱穿搭 AI 试衣」项目 (`ai-tryon-workflow`) 的实际落地经验中萃取而来。

适用于通过 **TAPD** 管理需求、**CodeBuddy** 辅助开发、**CNB** 管理 CI/CD 的任意项目。

## 自动研发闭环流程

```
TAPD 需求 / 自动创建需求
    → CodeBuddy 读取知识库与规则
    → 判断最小需求单元
    → AI生成Spec中（TAPD 状态同步）
    → 生成 Spec 设计文档
    → AI开发中（TAPD 状态同步）
    → 创建功能分支
    → 自动实现代码
    → AI测试中（TAPD 状态同步）
    → pytest + 覆盖率检查
    → AI审核中（TAPD 状态同步）
    → AI Code Review
    → AI自动修复中（按需）
    → 待自动合并（TAPD 状态同步）
    → 创建 MR → CNB 状态检查 → 自动合并
    → CNB main push 流水线
    → TAPD 自动归档为「已完成」
```

## 三种内容分类

### ✅ 可直接复用

| 文件/配置 | 说明 |
|-----------|------|
| `scripts/check_coverage.py` | 覆盖率门禁脚本（无需修改） |
| `scripts/tapd_archive.py` | TAPD 自动归档脚本（需配置环境变量） |
| TAPD 状态流转设计 | 待AI分析→...→已完成（9 状态） |
| Spec 规范 | 设计文档模板 |
| AI Review 规范 | 代码审查标准 |
| 质量门禁规范 | 覆盖率>=90%、AI Review>=95 |
| CNB 流水线结构 | pull_request 质量门禁 + push 归档（模板见 templates/cnb-pipeline-template.yml） |
| 执行护栏规则 | 强制预检 + 分支保护 + 本地验证 + 推送 + MR + 闭环报告 |
| 效果反馈修复闭环 | 问题复现 → 修复 → 验证 → 推送 → CNB 检查 |
| 经验分层沉淀规则 | 业务经验/通用经验/混合经验分层沉淀 |
| 闭环完成判定规则 | PR 流水线 + Push 流水线全部通过才算完成 |
| 人工介入断点规则 | 暂停条件、密钥处理、恢复执行规则 |

### ⚠️ 必须替换

| 内容 | 替换目标 |
|------|----------|
| `{TAPD_WORKSPACE_ID}` | 你的 TAPD 项目 ID |
| `{DEFAULT_ITERATION}` | 你的迭代名称 |
| `{BIZ_PREFIX}` | 你的业务前缀（如 order、chatbot） |
| `{BUSINESS_NAME}` | 你的业务名称 |
| `.codebuddy/knowledge/` | **完全重写**为你的项目知识库 |
| `src/`、`tests/` | 你的业务代码 |

### ❌ 禁止复制到新项目

| 内容 | 原因 |
|------|------|
| 真实 API 密钥 | 安全 |
| CNB 密钥仓库内容 | 安全 |
| 用户数据/图片 | 隐私 |
| 真实模型 Token/URL | 安全 |
| 私有服务地址 | 安全 |

## 快速开始

1. [新项目初始化指南](./NEW_PROJECT_SETUP.md) — 从零搭建
2. [复用检查清单](./docs/workflow-template/REUSE_CHECKLIST.md) — 逐项确认
3. [TAPD 配置](./docs/workflow-template/TAPD_SETUP.md) — 项目与状态配置
4. [CodeBuddy 配置](./docs/workflow-template/CODEBUDDY_SETUP.md) — MCP 与 Rules
5. [CNB 配置](./docs/workflow-template/CNB_SETUP.md) — 流水线与密钥

## 目录结构

```
ai-dev-workflow-template/
├── .cnb.yml                             # 模板仓库自检流水线（不可用于业务项目）
├── workflow.config.example.yml          # 工作流配置示例
├── README.md                            # 本文件
├── NEW_PROJECT_SETUP.md                 # 新项目初始化指南
├── .gitignore
├── scripts/
│   ├── check_coverage.py                # 覆盖率门禁脚本
│   └── tapd_archive.py                  # TAPD 自动归档脚本
├── .codebuddy/
│   ├── rules/                           # CodeBuddy 规则模板
│   │   ├── AutonomousWorkflowRules.mdc  #   总控规则（必须替换参数）
│   │   ├── CodingStandardRules.mdc      #   代码规范（按需替换）
│   │   ├── DesignSpecRules.mdc          #   Spec 规范
│   │   ├── EffectFeedbackLoopRules.mdc  #   效果反馈修复闭环规则
│   │   ├── ExecutionGuardRules.mdc      #   执行护栏规则（强制预检+流水线检查）
│   │   ├── ExperienceLayeringRules.mdc  #   经验分层沉淀规则
│   │   ├── GitBranchRules.mdc           #   分支规范（替换 biz_prefix）
│   │   ├── HumanInterventionRules.mdc   #   人工介入断点规则（暂停条件+密钥处理）
│   │   ├── SecurityRules.mdc            #   安全规范
│   │   ├── UnitTestRules.mdc            #   测试规范
│   │   ├── WorkflowCompletionRules.mdc  #   闭环完成判定规则
│   │   └── WorkflowRules.mdc            #   流程规范
│   └── knowledge-template/              # 知识库模板（新项目必须重写）
│       ├── 01_项目概述.md
│       ├── 02_架构设计.md
│       ├── 03_核心模块.md
│       ├── 04_接口规范.md
│       └── 05_开发指南.md
├── docs/
│   └── workflow-template/               # 完整配置文档
├── templates/                           # 独立模板文件
│   ├── tapd-requirement-template.md
│   ├── newdev-command-template.md
│   ├── autonomous-workflow-rules-template.mdc
│   ├── cnb-pipeline-template.yml        # CNB 流水线模板（新业务项目复制此文件）
│   ├── rules/                           # 通用规则模板（新项目复制到 .codebuddy/rules/）
│   │   ├── ExecutionGuardRules.mdc
│   │   ├── EffectFeedbackLoopRules.mdc
│   │   ├── ExperienceLayeringRules.mdc
│   │   ├── WorkflowCompletionRules.mdc
│   │   └── HumanInterventionRules.mdc
│   └── knowledge-files/
└── reports/                             # 归档报告（.gitignore 忽略）
```

## 技术栈支持

本模板以 **Python/FastAPI** 为主要示例，但工作流设计不绑定语言：

| 组件 | 语言无关 |
|------|----------|
| TAPD 需求管理 | ✅ |
| CodeBuddy AI 开发 | ✅ |
| TAPD 状态流转 | ✅ |
| Spec 设计规范 | ✅ |
| AI Code Review | ✅ |
| CNB 流水线框架 | ✅ |
| `/newdev` 命令 | ✅ |
| TAPD 归档脚本 | ✅ (Python 脚本可独立运行) |
| 覆盖率门禁 | 需替换为对应语言的覆盖率工具 |
| 测试命令 | 需替换为对应语言的测试框架 |

## 参考项目

本模板的参考实现：[ai-tryon-workflow](https://cnb.cool/liugouer-2026/ai-tryon-workflow) — 「爱穿搭」AI 试衣项目，所有需求均通过本模板描述的工作流自动完成。

## License

本模板使用 MIT License。参考项目中的业务代码为参考项目所有。
