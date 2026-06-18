# CNB 配置指南

## 概述

CNB 在本工作流中承担 CI/CD 角色：自动运行测试、检查覆盖率门禁、执行 TAPD 自动归档。

## 1. CNB 仓库创建

1. 在 CNB 平台创建仓库
2. 将模板文件推送到仓库
3. 确保 `.cnb.yml` 存在于仓库根目录

## 2. `.cnb.yml` 流水线模板

### 2.1 完整模板

```yaml
main:
  pull_request:
    - name: AI workflow MR quality gate
      docker:
        image: <your-docker-image>
      stages:
        - name: Install dependencies
          script: |
            <install-commands>
        - name: Run tests with coverage
          script: |
            <test-commands>
        - name: Check coverage gate
          script: |
            python scripts/check_coverage.py

  push:
    - name: Main branch verification
      docker:
        image: <your-docker-image>
      imports:
        - https://cnb.cool/<your-org>/<your-secrets-repo>/-/blob/main/tapd-env.yml
      stages:
        - name: Install dependencies
          script: |
            <install-commands>
        - name: Run tests with coverage
          script: |
            <test-commands>
        - name: Check coverage gate
          script: |
            python scripts/check_coverage.py
        - name: Archive TAPD result
          script: |
            python scripts/tapd_archive.py
```

### 2.2 需要替换的部分

| 原值 | 替换为 |
|------|--------|
| `<your-docker-image>` | 新项目的 Docker 镜像 |
| `<install-commands>` | 新项目的依赖安装命令 |
| `<test-commands>` | 新项目的测试命令 |
| `<your-org>/<your-secrets-repo>` | 新项目的密钥仓库 URL |

### 2.3 流水线阶段说明

| 阶段 | 触发条件 | 作用 |
|------|----------|------|
| `pull_request` | MR 创建/更新 | 质量门禁：pytest + 覆盖率 |
| `push` (main) | 合并到 main | 验证 + TAPD 归档 |

## 3. 密钥仓库配置

### 3.1 创建密钥仓库

1. 在 CNB 创建私有仓库 `<project>-secrets`
2. 添加 `tapd-env.yml` 文件

### 3.2 `tapd-env.yml` 模板

```yaml
env:
  TAPD_API_BASE_URL: https://api.tapd.cn
  TAPD_API_USER: <your-tapd-api-user>
  TAPD_API_PASSWORD: <your-tapd-api-password>
  TAPD_COMMENT_AUTHOR: <archive-comment-author-name>
  TAPD_ARCHIVE_ENABLED: "true"
```

### 3.3 引用密钥仓库

在 `.cnb.yml` 的 push 流水线中：

```yaml
imports:
  - https://cnb.cool/<your-org>/<your-secrets-repo>/-/blob/main/tapd-env.yml
```

> **安全提醒：** 密钥仓库必须设为私有。

## 4. 质量门禁脚本

### 4.1 `scripts/check_coverage.py`

该脚本读取 `coverage.xml`，检查覆盖率是否达标（默认 90%）。

**可直接复用，无需修改。**

### 4.2 `scripts/tapd_archive.py`

该脚本在 main push 后自动执行，处理 `reports/tapd-*-archive.json`：
1. 读取归档 JSON
2. 调用 TAPD API 更新状态为「已合并」
3. 写入归档评论
4. 更新状态为「已完成」

**可直接复用，无需修改代码。** 只需配置环境变量。

## 5. CNB MCP 工具

| 工具 | 用途 |
|------|------|
| `cnb_get_pull` | 查询 MR 状态 |
| `cnb_create_pull` | 创建 MR |
| `cnb_merge_pull` | 合并 MR |
| `cnb_list_pulls` | 列出 MR |

## 6. MR 自动合并条件

CodeBuddy 在以下条件全部满足时自动合并 MR：

1. pytest 全部通过
2. 覆盖率 >= 90%
3. AI Code Review 分数 >= 95
4. 无 Critical 问题
5. MR 无 Git 冲突
6. TAPD 归档 JSON 已生成
7. 目标分支为 main

## 7. 爱穿搭项目参考值（供对比）

| 配置项 | 爱穿搭项目值 |
|--------|-------------|
| CNB 仓库 | `liugouer-2026/ai-tryon-workflow` |
| 密钥仓库 | `liugouer-2026/ai-tryon-workflow-secrets` |
| Docker 镜像 | `python:3.11-slim` |
| 覆盖率门禁 | `>= 90%` |
| TAPD 归档脚本 | `scripts/tapd_archive.py` |
| 目标分支 | `main` |

## 8. 跨语言项目适配

### Python 项目
```yaml
image: python:3.11-slim
script: pytest --cov=src --cov-report=term-missing --cov-report=xml
```

### Node.js 项目
```yaml
image: node:20-alpine
script: npm test -- --coverage
```

### Java 项目
```yaml
image: maven:3.9-eclipse-temurin-17
script: mvn verify
```

> **注意：** 非 Python 项目需调整覆盖率脚本的实现。
