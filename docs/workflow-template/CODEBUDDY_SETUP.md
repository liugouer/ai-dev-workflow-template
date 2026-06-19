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

## 6. 国内网络适配（gradio_client / HuggingFace Space）

当通过 `gradio_client` 调用境外 HuggingFace Space 时，国内环境需要额外网络配置。

### 问题

企业网络代理会拦截 `gradio_client` 对 `*.hf.space` 的 WebSocket 连接，导致超时或连接失败。

### 解决方案

```bash
# 启动前设置
export NO_PROXY="*"                       # 禁用代理
export HF_HUB_DISABLE_SSL_VERIFY=1        # 禁用 SSL 验证
```

代码中也需要额外配置：

```python
import gradio_client

client = gradio_client.Client(
    space_url,
    hf_token=token,
    ssl_verify=False,                     # gradio_client 级 SSL 禁用
)
```

### 完整启动命令示例

```bash
# Windows PowerShell
$env:{BIZ_PREFIX}_MODEL_MODE="hf"
$env:NO_PROXY="*"
uvicorn src.main:app --reload

# macOS / Linux
export {BIZ_PREFIX}_MODEL_MODE=hf
export NO_PROXY=*
uvicorn src.main:app --reload
```

### 测试注意事项

测试 HuggingFace Space 客户端时，必须 mock 所有外部网络调用，确保测试不依赖真实网络：

```python
@patch("{biz}.services.model_adapter.gradio_client.Client")
@patch("PIL.Image.open")
def test_hf_success(self, mock_pil_open, mock_client_cls):
    mock_client = MagicMock()
    mock_client.predict.return_value = "result_path"
    mock_client_cls.return_value = mock_client
    # ...
```

### 常见错误处理

| 错误消息 | 原因 | 处理 |
|----------|------|------|
| `no space is running` | Space 休眠中（ZeroGPU）| 等待 1-2 分钟重试 |
| `quota exceeded` | ZeroGPU 配额用尽 | 换时段或用 HF Token 提额 |
| `queue is full` | 并发请求过多 | 等待后重试 |
| `ConnectionError` | 代理拦截 | 设置 `NO_PROXY=*` |
| `SSLError` | SSL 验证失败 | 设置 `ssl_verify=False` |

## 7. 爱穿搭项目参考（供对比）

### Rules 中需要替换的值

| 文件 | 参数 | 原值 | 说明 |
|------|------|------|------|
| AutonomousWorkflowRules.mdc | TAPD 项目 ID | `31917999` | 项目唯一标识 |
| AutonomousWorkflowRules.mdc | 默认迭代 | `tryon-v0.1.0-mvp` | 迭代名称 |
| AutonomousWorkflowRules.mdc | biz_prefix | `tryon` | 分支前缀 |
| CodingStandardRules.mdc | 接口路径 | `/api/tryon` | API 路径 |
| GitBranchRules.mdc | biz_prefix | `tryon` | 分支前缀 |
