# 复用检查清单

迁移到新项目时，逐项确认以下清单。

## ✅ 可复用（直接复制）

| # | 文件/目录 | 说明 | 已复制 |
|---|-----------|------|--------|
| 1 | `scripts/check_coverage.py` | 覆盖率门禁脚本，无需修改 | ☐ |
| 2 | `scripts/tapd_archive.py` | TAPD 归档脚本，需配置环境变量 | ☐ |
| 3 | `.cnb.yml` | CNB 流水线，需替换 Docker 镜像和密钥 URL | ☐ |
| 4 | `.codebuddy/rules/SecurityRules.mdc` | 安全规范，通用 | ☐ |
| 5 | `.codebuddy/rules/UnitTestRules.mdc` | 测试规范，通用 | ☐ |
| 6 | `.codebuddy/rules/WorkflowRules.mdc` | 流程规范，通用 | ☐ |
| 7 | `.codebuddy/rules/DesignSpecRules.mdc` | Spec 规范，通用 | ☐ |
| 8 | `.codebuddy/rules/ExecutionGuardRules.mdc` | 执行护栏规则，通用 | ☐ |
| 9 | `.codebuddy/rules/EffectFeedbackLoopRules.mdc` | 效果反馈修复闭环，通用 | ☐ |
| 10 | `.codebuddy/rules/ExperienceLayeringRules.mdc` | 经验分层沉淀，通用 | ☐ |
| 11 | `.codebuddy/rules/WorkflowCompletionRules.mdc` | 闭环完成判定，通用 | ☐ |
| 12 | `.codebuddy/rules/HumanInterventionRules.mdc` | 人工介入断点，通用 | ☐ |
| 13 | `.codebuddy/rules/EpicRequirementDecompositionRules.mdc` | 大功能拆解，通用 | ☐ |
| 14 | `.codebuddy/rules/IterationLifecycleRules.mdc` | 迭代生命周期，通用 | ☐ |

## ⚠️ 需要修改后使用

| # | 文件/目录 | 需要修改的内容 | 已完成 |
|---|-----------|---------------|--------|
| 1 | `.codebuddy/rules/AutonomousWorkflowRules.mdc` | TAPD 项目ID、迭代名、biz_prefix | ☐ |
| 2 | `.codebuddy/rules/CodingStandardRules.mdc` | 接口路径、响应格式、需求边界 | ☐ |
| 3 | `.codebuddy/rules/GitBranchRules.mdc` | biz_prefix、版本号 | ☐ |
| 4 | `.codebuddy/commands/newdev.md` | TAPD 项目ID、迭代名 | ☐ |
| 5 | `.codebuddy/commands/epicdev.md` | TAPD 项目ID、迭代名 | ☐ |
| 6 | `.codebuddy/commands/iteration.md` | TAPD 项目ID、迭代名 | ☐ |
| 7 | `.codebuddy/commands/dailymaintain.md` | TAPD 项目ID、迭代名 | ☐ |
| 8 | `.cnb.yml` | Docker 镜像、密钥仓库 URL | ☐ |
| 9 | `requirements.txt` | 新项目依赖列表 | ☐ |
| 10 | `README.md` | 新项目介绍 | ☐ |

## 🔄 必须完全重写

| # | 文件/目录 | 说明 | 已完成 |
|---|-----------|------|--------|
| 1 | `.codebuddy/knowledge/01_项目概述.md` | 新项目概述 | ☐ |
| 2 | `.codebuddy/knowledge/02_架构设计.md` | 新项目架构 | ☐ |
| 3 | `.codebuddy/knowledge/03_核心模块.md` | 新项目核心模块 | ☐ |
| 4 | `.codebuddy/knowledge/04_接口规范.md` | 新项目接口 | ☐ |
| 5 | `.codebuddy/knowledge/05_开发指南.md` | 新项目开发指南 | ☐ |
| 6 | `src/` 全部代码 | 新项目业务代码 | ☐ |
| 7 | `tests/` 全部测试 | 新项目业务测试 | ☐ |

## ❌ 禁止复制

| # | 内容 | 原因 | 已确认 |
|---|------|------|--------|
| 1 | TAPD API 密钥/密码 | 安全 | ☐ |
| 2 | CNB 密钥仓库内容 | 安全 | ☐ |
| 3 | 真实 API Token | 安全 | ☐ |
| 4 | 私有服务 URL | 安全 | ☐ |
| 5 | 用户上传的测试图片 | 隐私 | ☐ |
| 6 | `.env` 或任何含密钥的文件 | 安全 | ☐ |
| 7 | `reports/` 下的业务报告 | 无关 | ☐ |
| 8 | `specs/` 下的业务 Spec | 无关 | ☐ |

## 🔌 平台配置

| # | 配置项 | 说明 | 已配置 |
|---|--------|------|--------|
| 1 | TAPD 项目创建 | 获取 workspace_id | ☐ |
| 2 | TAPD 迭代创建 | 获取 iteration_id | ☐ |
| 3 | TAPD 状态流转配置 | 配置 9 个状态 | ☐ |
| 4 | CodeBuddy MCP (TAPD) | 连接 TAPD | ☐ |
| 5 | CodeBuddy MCP (CNB) | 连接 CNB | ☐ |
| 6 | CNB 密钥仓库 | tapd-env.yml | ☐ |
| 7 | CNB 流水线启用 | .cnb.yml 生效 | ☐ |

## 🧪 冒烟测试验证

| # | 验证项 | 预期结果 | 通过 |
|---|--------|----------|------|
| 1 | `/newdev 冒烟测试需求` | TAPD 需求自动创建 | ☐ |
| 2 | Spec 自动生成 | specs/ 下生成 Spec 文件 | ☐ |
| 3 | 分支自动创建 | feature/ 分支创建成功 | ☐ |
| 4 | 执行护栏预检通过 | 规则、知识库、分支、git status 预检 | ☐ |
| 5 | 代码自动实现 | 代码完成功能 | ☐ |
| 6 | pytest 全部通过 | 0 failed | ☐ |
| 7 | 覆盖率 >= 90% | 门禁通过 | ☐ |
| 8 | AI Review >= 95 | 无 Critical | ☐ |
| 9 | MR 自动创建 | CNB 上有 MR | ☐ |
| 10 | MR 自动合并 | 合并到 main | ☐ |
| 11 | TAPD 归档完成 | 状态变为「已完成」 | ☐ |
| 12 | 闭环报告输出 | 包含经验沉淀段落 | ☐ |

## 快速参考：爱穿搭→新项目映射表

| 爱穿搭项目 | 新项目（填写） |
|------------|--------------|
| `ai-tryon-workflow` | `_______________` |
| `31917999` | `_______________` |
| `tryon-v0.1.0-mvp` | `_______________` |
| `tryon` (biz_prefix) | `_______________` |
| `/api/tryon` | `_______________` |
| `person_image, cloth_image` | `_______________` |
| `liugouer-2026/ai-tryon-workflow` | `_______________` |
| `liugouer-2026/ai-tryon-workflow-secrets` | `_______________` |
