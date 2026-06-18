# AI 研发自动化工作流模板文档

## 概述

本目录包含从「爱穿搭 AI 试衣」项目 (`ai-tryon-workflow`) 中萃取的工作流模板，适用于任何通过 TAPD 管理需求、CodeBuddy 辅助开发、CNB 管理 CI/CD 的项目。

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

## 快速导航

| 文档 | 用途 | 优先阅读人群 |
|------|------|-------------|
| [NEW_PROJECT_SETUP.md](../../NEW_PROJECT_SETUP.md) | 新项目从零初始化 | 所有人 |
| [TAPD_SETUP.md](./TAPD_SETUP.md) | TAPD 项目配置 | 项目管理员 |
| [CODEBUDDY_SETUP.md](./CODEBUDDY_SETUP.md) | CodeBuddy MCP 与命令配置 | 开发者 |
| [CNB_SETUP.md](./CNB_SETUP.md) | CNB 流水线配置 | DevOps |
| [REUSE_CHECKLIST.md](./REUSE_CHECKLIST.md) | 复用检查清单 | 所有人 |
| [knowledge-template.md](./knowledge-template.md) | 知识库模板 | 项目维护者 |
| [rules-template.md](./rules-template.md) | Rules 规则模板 | 项目维护者 |
| [newdev-command-template.md](./newdev-command-template.md) | /newdev 命令模板 | 开发者 |
| [cnb-pipeline-template.md](./cnb-pipeline-template.md) | CNB 流水线模板 | DevOps |

## 三类内容速查表

### ✅ 可复用（直接复制到新项目）

| 文件/配置 | 说明 |
|-----------|------|
| `.codebuddy/rules/AutonomousWorkflowRules.mdc` | 自动研发闭环总控规则（需替换参数） |
| `.cnb.yml` | CNB 流水线配置（需替换业务依赖） |
| `scripts/check_coverage.py` | 覆盖率门禁脚本（无需修改） |
| `scripts/tapd_archive.py` | TAPD 自动归档脚本（需替换环境变量） |
| TAPD 状态流转设计 | 待AI分析→AI生成Spec中→...→已完成 |
| `/newdev` 命令 | 创建并开发需求命令 |
| Spec 规范 | 设计文档模板 |
| AI Review 规范 | 代码审查标准 |
| 质量门禁规范 | 覆盖率>=90%、AI Review>=95 |

### ⚠️ 必须替换

| 文件/配置 | 是否替换 | 替换内容 |
|-----------|---------|----------|
| `.codebuddy/knowledge/` | **全部替换** | 改为新项目的业务知识库 |
| TAPD 项目 ID | **必须替换** | `{TAPD_WORKSPACE_ID}` → 新项目 ID |
| TAPD 迭代名称 | **必须替换** | `{DEFAULT_ITERATION}` → 新迭代名 |
| TAPD 状态字段 | **按需替换** | 确保自定义状态名称一致 |
| `src/` 业务代码 | **全部替换** | 新项目业务代码 |
| `tests/` 业务测试 | **全部替换** | 新项目业务测试 |
| `README.md` | **必须替换** | 新项目介绍 |
| 业务接口规范 | **全部替换** | 新项目接口定义 |
| 业务验收标准 | **全部替换** | 新项目验收条件 |
| `requirements.txt` | **按需替换** | 新项目依赖 |

### ❌ 禁止复制

| 内容 | 原因 |
|------|------|
| 真实 API 密钥 | 安全 |
| CNB 密钥仓库内容 | 安全 |
| 用户上传的测试图片 | 隐私 |
| 真实模型 Token / URL | 安全 |
| 私有服务地址 | 安全 |
| 任何包含真实用户数据的文件 | 隐私 |
| `.env` 文件内容 | 安全 |

## 新项目初始化 10 步

1. 创建 Git 仓库
2. 复制模板文件
3. 配置 TAPD 项目 ID
4. 配置 TAPD 状态流转
5. 配置 CodeBuddy MCP
6. 配置 CNB 密钥仓库
7. 配置 `.codebuddy/knowledge`
8. 配置 `.codebuddy/rules`
9. 配置 `/newdev` 命令
10. 创建冒烟测试需求验证闭环

详细步骤见 [NEW_PROJECT_SETUP.md](../../NEW_PROJECT_SETUP.md)。

## 参考项目

本模板参考项目：[ai-tryon-workflow](https://cnb.cool/liugouer-2026/ai-tryon-workflow)

该项目实现了「上传人物图+衣服图返回试衣效果图」的完整 AI 研发自动化闭环，所有需求均通过本模板描述的工作流自动完成。
