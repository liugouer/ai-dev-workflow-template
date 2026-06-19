# 新项目初始化指南

从零搭建 AI 研发自动化闭环。

## 前提条件

- 拥有 TAPD 项目管理员权限
- 拥有 CNB / Git 仓库创建权限
- 已安装 CodeBuddy IDE 插件，已配置 MCP

## 步骤 1：创建 Git 仓库

```bash
# 在 CNB / Git 平台创建新仓库
git clone <新仓库地址>
cd <新项目名>
```

## 步骤 2：复制模板文件

从本模板仓库复制以下文件到新项目：

```bash
# 假设本模板仓库 clone 到 ../ai-dev-workflow-template
# 注意：不要复制模板仓库根目录的 .cnb.yml（那是模板仓库自检流水线）
# 应复制业务项目流水线模板
cp ../ai-dev-workflow-template/templates/cnb-pipeline-template.yml .cnb.yml
cp ../ai-dev-workflow-template/workflow.config.example.yml ./
cp ../ai-dev-workflow-template/.gitignore ./

# 复制脚本
cp -r ../ai-dev-workflow-template/scripts/ ./

# 复制 CodeBuddy 规则模板
mkdir -p .codebuddy/rules
cp ../ai-dev-workflow-template/.codebuddy/rules/*.mdc .codebuddy/rules/

# 复制命令模板
mkdir -p .codebuddy/commands
cp ../ai-dev-workflow-template/templates/newdev-command-template.md .codebuddy/commands/newdev.md
cp ../ai-dev-workflow-template/templates/epicdev-command-template.md .codebuddy/commands/epicdev.md
cp ../ai-dev-workflow-template/templates/iteration-command-template.md .codebuddy/commands/iteration.md
cp ../ai-dev-workflow-template/templates/dailymaintain-command-template.md .codebuddy/commands/dailymaintain.md

# 复制知识库模板
cp -r ../ai-dev-workflow-template/.codebuddy/knowledge-template/ .codebuddy/knowledge/
```

## 步骤 3：配置 TAPD 项目 ID

在 TAPD 中获取你的项目 `workspace_id`（URL 中可见）：

```
https://www.tapd.cn/<workspace_id>/...
```

编辑以下文件，将所有 `{TAPD_WORKSPACE_ID}` 替换为你的项目 ID：

| 文件 | 位置 |
|------|------|
| `.codebuddy/rules/AutonomousWorkflowRules.mdc` | `TAPD 项目 ID：{TAPD_WORKSPACE_ID}` |
| `workflow.config.example.yml` | `workspace_id: "<你的TAPD项目ID>"` |
| `.codebuddy/commands/newdev.md` | 默认参数区域 |

## 步骤 4：配置 TAPD 迭代

在 TAPD 项目中创建迭代，将 `{DEFAULT_ITERATION}` 替换为你的迭代名称。

**参考：** 爱穿搭项目使用 `tryon-v0.1.0-mvp`。

## 步骤 5：配置 TAPD 状态流转

在 TAPD 项目 → 设置 → 需求类型 → 编辑状态中创建以下自定义状态：

| 状态名称 | 说明 |
|----------|------|
| 待AI分析 | AI 研发闭环的入口状态 |
| AI生成Spec中 | Spec 设计阶段 |
| AI开发中 | 代码实现阶段 |
| AI测试中 | 测试与覆盖率阶段 |
| AI审核中 | AI Code Review 阶段 |
| AI自动修复中 | Review 问题修复阶段（可选） |
| 待自动合并 | MR 创建与等待合并 |
| 已合并 | MR 已合并 |
| 已完成 | 归档完成 |

> **重要：** 状态名称必须与 `AutonomousWorkflowRules.mdc` 中一致。

## 步骤 6：配置 CodeBuddy MCP

在 CodeBuddy IDE 中确保以下 MCP Server 已连接：

1. **TAPD MCP Server** — 需求管理
2. **CNB MCP Server** — 仓库与 MR 管理

验证连接：
```
查询 TAPD 项目 {你的项目ID} 的需求
```

## 步骤 7：配置 CNB 密钥仓库

1. 在 CNB 创建私有仓库 `<project>-secrets`
2. 添加 `tapd-env.yml`：

```yaml
env:
  TAPD_API_BASE_URL: https://api.tapd.cn
  TAPD_API_USER: <你的 TAPD API 用户>
  TAPD_API_PASSWORD: <你的 TAPD API 密码>
  TAPD_COMMENT_AUTHOR: <归档评论作者名>
  TAPD_ARCHIVE_ENABLED: "true"
```

3. 在 `.cnb.yml` 中替换密钥仓库 URL：

```yaml
imports:
  - https://cnb.cool/<你的org>/<你的secrets仓库>/-/blob/main/tapd-env.yml
```

## 步骤 8：编写知识库

**知识库是 CodeBuddy 理解你项目的唯一途径，必须认真编写。**

`.codebuddy/knowledge/` 中已有 5 个模板文件，将每个文件按你的项目重写：

1. `01_项目概述.md` — 项目名称、目标、迭代
2. `02_架构设计.md` — 技术栈、分层架构、目录结构
3. `03_核心模块.md` — 各模块职责
4. `04_接口规范.md` — 接口定义、参数、响应
5. `05_开发指南.md` — 环境、依赖、启动命令

> 不得出现密钥、Token、真实用户数据。

## 步骤 9：替换 Rules 中的业务参数

### AutonomousWorkflowRules.mdc

| 原占位符 | 替换为 |
|----------|--------|
| `{TAPD_WORKSPACE_ID}` | 你的 TAPD 项目 ID |
| `{DEFAULT_ITERATION}` | 你的迭代名称 |
| `{BIZ_PREFIX}` | 你的业务前缀（如 order、chatbot） |
| `{BUSINESS_NAME}` | 你的业务名称 |

### GitBranchRules.mdc

将 `{BIZ_PREFIX}` 替换为你的业务前缀。

### CodingStandardRules.mdc

将接口路径、响应格式、需求边界替换为你的业务定义。

## 步骤 10：配置 .cnb.yml 流水线

> **重要：** 模板仓库根目录的 `.cnb.yml` 是模板仓库自检流水线，不能直接用于业务项目。
> 新项目已在步骤 2 中从 `templates/cnb-pipeline-template.yml` 复制了正确的流水线模板。

将 `.cnb.yml` 中的所有占位符替换为实际值：

| 占位符 | 替换为 |
|--------|--------|
| `<your-docker-image>` | 运行环境镜像（如 python:3.11-slim） |
| `<install-commands>` | 依赖安装命令（如 pip install -r requirements.txt） |
| `<test-commands>` | 测试 + 覆盖率命令（如 pytest --cov=src --cov-report=term-missing --cov-report=xml） |
| `<your-org>/<your-secrets-repo>` | 密钥仓库路径（如 liugouer-2026/ai-tryon-workflow-secrets） |

## 步骤 11：冒烟测试验证

### 11.1 单需求模式（`/newdev`）

在 CodeBuddy 中输入：

```
/newdev 冒烟测试：返回 hello world 接口
```

### 11.2 大功能批量模式（`/epicdev`）

在 CodeBuddy 中输入：

```
/epicdev --plan 用户管理功能
```

先确认拆解计划正确，再输入：

```
/epicdev --yes 用户管理功能
```

### 11.3 迭代生命周期模式（`/iteration`）

在 CodeBuddy 中输入：

```
/iteration --start v0.1.0
```

确认迭代范围后，观察需求拆解和创建是否正常。收口时输入：

```
/iteration --release v0.1.0
```

### 11.4 每日维护模式（`/dailymaintain`）

在 CodeBuddy 中输入：

```
/dailymaintain
```

观察是否自动检查需求、MR、流水线、Git 状态并输出维护报告。

### 11.5 验收标准

观察以下流程是否全部自动完成：

- ✅ TAPD 需求创建
- ✅ Spec 生成
- ✅ 分支创建
- ✅ 代码实现
- ✅ 测试通过
- ✅ AI Review ≥ 95
- ✅ MR 自动合并
- ✅ TAPD 归档完成

对于 `/epicdev`，还需验证：
- ✅ 拆解计划合理
- ✅ 多个需求按依赖顺序执行
- ✅ 每个需求闭环独立完成
- ✅ Epic 最终报告输出完整

对于 `/iteration` 和 `/dailymaintain`，还需验证：
- ✅ 迭代启动检查完整
- ✅ 每日维护报告输出正确
- ✅ 版本收口所有检查项通过

## 验收自检

| 检查项 | 状态 |
|--------|------|
| Git 仓库已创建 | ☐ |
| 模板文件已复制 | ☐ |
| TAPD workspace_id 已替换 | ☐ |
| TAPD 迭代已创建并配置 | ☐ |
| TAPD 状态流转已配置 | ☐ |
| CodeBuddy MCP 已连接 | ☐ |
| CNB 密钥仓库已配置 | ☐ |
| 知识库已按新项目重写 | ☐ |
| Rules 中的业务参数已替换 | ☐ |
| .cnb.yml 已替换业务命令 | ☐ |
| 冒烟测试需求通过完整闭环 | ☐ |
| `/epicdev` 大功能拆解测试通过 | ☐ |
| `/iteration --start` 迭代启动测试通过 | ☐ |
| `/dailymaintain` 每日维护测试通过 | ☐ |

## 爱穿搭项目参考值（供对比）

| 配置项 | 爱穿搭项目值 | 你的值 |
|--------|-------------|--------|
| workspace_id | `31917999` | `_______________` |
| 迭代 | `tryon-v0.1.0-mvp` | `_______________` |
| biz_prefix | `tryon` | `_______________` |
| 业务名称 | 爱穿搭 AI 试衣 | `_______________` |
| 接口路径 | `/api/tryon` | `_______________` |
| 密钥仓库 | `liugouer-2026/ai-tryon-workflow-secrets` | `_______________` |
