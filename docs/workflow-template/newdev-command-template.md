# /newdev 命令模板说明

## 概述

`/newdev` 是 CodeBuddy 命令，用于创建 TAPD 需求并自动执行完整研发闭环。

文件位置：`.codebuddy/commands/newdev.md`

## 命令行为

输入 `/newdev <需求主题>` 后，CodeBuddy 自动：

1. 读取知识库和规则
2. 生成标准 TAPD 需求标题和正文
3. 展示预览等待用户确认（或 `--yes` 跳过确认）
4. 通过 TAPD MCP 创建需求
5. 自动启动完整研发闭环（Spec → 开发 → 测试 → Review → MR → 归档）

## 命令格式

```
/newdev 需求主题描述
/newdev --yes 需求主题描述        # 跳过确认直接创建
```

## 模板内容

详见 `templates/newdev-command-template.md`。

## 需要替换的部分

| 占位符 | 替换为 |
|--------|--------|
| `{TAPD_WORKSPACE_ID}` | 你的 TAPD 项目 ID |
| `{DEFAULT_ITERATION}` | 你的迭代名称 |
| `main` | 你的默认分支（如果不同） |

命令的**执行流程**无需修改，这是通用的。

## 验证

在新项目中输入 `/newdev --yes hello world 测试`，确认：
1. 命令被识别
2. TAPD 需求自动创建
3. 完整闭环自动执行
