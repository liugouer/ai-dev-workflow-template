# CNB 流水线模板说明

## 概述

`.cnb.yml` 是 CNB 平台的流水线配置文件，定义 MR 质量门禁和 main 分支 push 后的归档流程。

## 完整模板

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

## 需要替换的部分

| 占位符 | 说明 | 示例 |
|--------|------|------|
| `<your-docker-image>` | 运行环境 Docker 镜像 | `python:3.11-slim`, `node:20-alpine` |
| `<install-commands>` | 依赖安装命令 | `pip install -r requirements.txt`, `npm ci` |
| `<test-commands>` | 测试与覆盖率命令 | `pytest --cov=src --cov-report=term-missing --cov-report=xml` |
| `<your-org>/<your-secrets-repo>` | 密钥仓库路径 | `my-org/my-project-secrets` |

## 流水线执行流程说明

```
┌─ pull_request（MR 创建时触发）─────────────────┐
│  1. Install dependencies                       │
│  2. Run tests with coverage                    │
│  3. Check coverage gate                        │
│  ✅ 全部通过 → MR 状态变为 "success"            │
│  ❌ 任一失败 → MR 状态变为 "failure"            │
└────────────────────────────────────────────────┘
                    ↓
            CNB 状态检查通过
                    ↓
            CodeBuddy 自动合并
                    ↓
┌─ push to main（合并到 main 后触发）─────────────┐
│  1. Install dependencies                       │
│  2. Run tests with coverage                    │
│  3. Check coverage gate                        │
│  4. Archive TAPD                               │
│  归档脚本自动：                                 │
│  - 读取 reports/tapd-*-archive.json            │
│  - 更新 TAPD 状态: 已合并 → 已完成              │
│  - 写入归档评论                                 │
└────────────────────────────────────────────────┘
```

## 跨语言项目适配

### Python 项目
```yaml
image: python:3.11-slim
script: pip install -r requirements.txt
script: pytest --cov=src --cov-report=term-missing --cov-report=xml
```

### Node.js 项目
```yaml
image: node:20-alpine
script: npm ci
script: npm test -- --coverage
```

### Java 项目
```yaml
image: maven:3.9-eclipse-temurin-17
script: mvn verify
```

> **注意：** 非 Python 项目需要调整 `check_coverage.py` 和 `tapd_archive.py` 的实现方式，或提供等效的脚本。

## check_coverage.py 说明

该脚本解析 `coverage.xml` 文件，检查覆盖率是否达标。**无需修改。** 如果使用其他语言，需提供等效脚本。

## tapd_archive.py 说明

该脚本独立于语言/框架，只依赖 Python + requests + TAPD API。**无需修改。**

## 爱穿搭项目实际配置（参考）

```yaml
main:
  pull_request:
    - name: TAPD AI workflow MR quality gate
      docker:
        image: python:3.11-slim
      stages:
        - name: Install dependencies
          script: |
            python -m pip install --upgrade pip
            pip install -r requirements.txt
        - name: Run pytest with coverage
          script: |
            pytest --cov=src --cov-report=term-missing --cov-report=xml
        - name: Check coverage gate
          script: |
            python scripts/check_coverage.py

  push:
    - name: Main branch verification
      docker:
        image: python:3.11-slim
      imports:
        - https://cnb.cool/liugouer-2026/ai-tryon-workflow-secrets/-/blob/main/tapd-env.yml
      stages:
        - name: Install dependencies
          script: |
            python -m pip install --upgrade pip
            pip install -r requirements.txt
        - name: Run pytest with coverage
          script: |
            pytest --cov=src --cov-report=term-missing --cov-report=xml
        - name: Check coverage gate
          script: |
            python scripts/check_coverage.py
        - name: Archive TAPD result
          script: |
            python scripts/tapd_archive.py
```
