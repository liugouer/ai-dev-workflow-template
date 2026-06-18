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
cp ../ai-dev-workflow-template/.cnb.yml ./
cp ../ai-dev-workflow-template/workflow.config.example.yml ./
cp ../ai-dev-workflow-template/.gitignore ./

# 复制脚本
cp -r ../ai-dev-workflow-template/scripts/ ./

# 复制 CodeBuddy 规则模板
mkdir -p .codebuddy/rules
cp ../ai-dev-workflow-template/.codebuddy/rules/*.mdc .codebuddy/rules/

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

| 占位符 | 替换为 |
|--------|--------|
| `<your-docker-image>` | 运行环境镜像 |
| `<install-commands>` | 依赖安装命令 |
| `<test-commands>` | 测试 + 覆盖率命令 |
| `<your-org>/<your-secrets-repo>` | 密钥仓库路径 |

## 步骤 11：冒烟测试验证

在 CodeBuddy 中输入：

```
/newdev 冒烟测试：返回 hello world 接口
```

观察以下流程是否全部自动完成：

- ✅ TAPD 需求创建
- ✅ Spec 生成
- ✅ 分支创建
- ✅ 代码实现
- ✅ 测试通过
- ✅ AI Review ≥ 95
- ✅ MR 自动合并
- ✅ TAPD 归档完成

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

## 爱穿搭项目参考值（供对比）

| 配置项 | 爱穿搭项目值 | 你的值 |
|--------|-------------|--------|
| workspace_id | `31917999` | `_______________` |
| 迭代 | `tryon-v0.1.0-mvp` | `_______________` |
| biz_prefix | `tryon` | `_______________` |
| 业务名称 | 爱穿搭 AI 试衣 | `_______________` |
| 接口路径 | `/api/tryon` | `_______________` |
| 密钥仓库 | `liugouer-2026/ai-tryon-workflow-secrets` | `_______________` |
