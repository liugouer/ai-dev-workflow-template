# 新项目初始化指南（从零搭建 AI 研发自动化闭环）

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

从本模板仓库复制以下目录和文件：

```bash
# 假设模板仓库在本地 ../ai-dev-workflow-template
cp ../ai-dev-workflow-template/.cnb.yml ./
cp ../ai-dev-workflow-template/workflow.config.example.yml ./
cp ../ai-dev-workflow-template/.gitignore ./

# 复制脚本
cp -r ../ai-dev-workflow-template/scripts/ ./

# 复制 CodeBuddy 规则
mkdir -p .codebuddy/rules
cp ../ai-dev-workflow-template/.codebuddy/rules/*.mdc .codebuddy/rules/

# 复制知识库模板
cp -r ../ai-dev-workflow-template/.codebuddy/knowledge-template/ .codebuddy/knowledge/
```

## 步骤 3：配置 TAPD 项目 ID

编辑 `.codebuddy/rules/AutonomousWorkflowRules.mdc`，替换：

```diff
- TAPD 项目 ID：{TAPD_WORKSPACE_ID}
+ TAPD 项目 ID：<你的项目ID>

- 默认迭代：{DEFAULT_ITERATION}
+ 默认迭代：<你的迭代名称>
```

详见 [TAPD_SETUP.md](./TAPD_SETUP.md)。

## 步骤 4：配置 TAPD 状态流转

在 TAPD 项目中创建以下自定义状态（按顺序）：

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

## 步骤 5：配置 CodeBuddy MCP

确保以下 MCP Server 已连接：
1. **TAPD MCP Server** — 连接你的 TAPD 项目
2. **CNB MCP Server** — 连接你的 CNB 仓库

详见 [CODEBUDDY_SETUP.md](./CODEBUDDY_SETUP.md)。

## 步骤 6：配置 CNB 密钥仓库

创建密钥仓库（用于存储 TAPD API 凭证）：

```yaml
# tapd-env.yml 示例
env:
  TAPD_API_BASE_URL: https://api.tapd.cn
  TAPD_API_USER: <你的 TAPD API 用户>
  TAPD_API_PASSWORD: <你的 TAPD API 密码>
  TAPD_COMMENT_AUTHOR: <归档评论作者>
  TAPD_ARCHIVE_ENABLED: "true"
```

在 `.cnb.yml` 的 push 流水线中引用：

```yaml
imports:
  - https://cnb.cool/<your-org>/<your-secrets-repo>/-/blob/main/tapd-env.yml
```

详见 [CNB_SETUP.md](./CNB_SETUP.md)。

## 步骤 7：配置知识库

```bash
mkdir -p .codebuddy/knowledge
```

根据 `knowledge-template.md` 创建以下知识库文件：

1. `01_项目概述.md`
2. `02_架构设计.md`
3. `03_核心模块.md`
4. `04_接口规范.md`
5. `05_开发指南.md`

> **关键：** 知识库内容必须是新项目的业务信息。

详见 [knowledge-template.md](./knowledge-template.md)。

## 步骤 8：配置 Rules

### AutonomousWorkflowRules.mdc 替换项

| 原占位符 | 替换为 |
|----------|--------|
| `{TAPD_WORKSPACE_ID}` | 新项目 TAPD workspace_id |
| `{DEFAULT_ITERATION}` | 新项目迭代名称 |
| `{BIZ_PREFIX}` | 新项目 biz_prefix |
| `main` | 新项目默认分支（如不同） |

### CodingStandardRules.mdc 替换项

- `{BUSINESS_API_PREFIX}` → 新项目接口前缀
- 响应格式 → 新项目响应格式

### GitBranchRules.mdc 替换项

- `{BIZ_PREFIX}` → 新项目 biz_prefix

详见 [rules-template.md](./rules-template.md)。

## 步骤 9：配置 /newdev 命令

编辑 `.codebuddy/commands/newdev.md`，替换默认参数。

详见 [newdev-command-template.md](./newdev-command-template.md)。

## 步骤 10：冒烟测试验证

在 CodeBuddy 中输入：
```
/newdev 冒烟测试：返回 hello world 接口
```

观察完整流程是否自动执行。

## 验收自检

| 检查项 | 状态 |
|--------|------|
| Git 仓库已创建 | ☐ |
| 模板文件已复制 | ☐ |
| TAPD 项目 ID 已替换 | ☐ |
| TAPD 状态流转已配置 | ☐ |
| CodeBuddy MCP 已连接 | ☐ |
| CNB 密钥仓库已配置 | ☐ |
| 知识库已根据新项目编写 | ☐ |
| Rules 已替换业务字段 | ☐ |
| /newdev 命令默认参数已替换 | ☐ |
| 冒烟测试需求通过完整闭环 | ☐ |

## 爱穿搭项目参考值（供对比）

| 配置项 | 爱穿搭项目值 | 你的值 |
|--------|-------------|--------|
| workspace_id | `31917999` | `_______________` |
| 迭代 | `tryon-v0.1.0-mvp` | `_______________` |
| biz_prefix | `tryon` | `_______________` |
| 接口路径 | `/api/tryon` | `_______________` |
| 密钥仓库 | `liugouer-2026/ai-tryon-workflow-secrets` | `_______________` |
