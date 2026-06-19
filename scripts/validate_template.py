#!/usr/bin/env python3
"""模板仓库自检脚本。

检查模板仓库是否符合通用模板要求。
不包含任何业务测试或 TAPD 操作。
"""

import os
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def check_required_files() -> list[str]:
    """检查必须存在的模板文件。"""
    errors: list[str] = []

    required = [
        "README.md",
        "NEW_PROJECT_SETUP.md",
        "workflow.config.example.yml",
        "templates/autonomous-workflow-rules-template.mdc",
        "templates/newdev-command-template.md",
        "templates/epicdev-command-template.md",
        "templates/iteration-command-template.md",
        "templates/dailymaintain-command-template.md",
        "templates/tapd-requirement-template.md",
        "templates/cnb-pipeline-template.yml",
        "docs/workflow-template/REUSE_CHECKLIST.md",
        ".codebuddy/commands/newdev.md",
        ".codebuddy/commands/epicdev.md",
        ".codebuddy/commands/iteration.md",
        ".codebuddy/commands/dailymaintain.md",
    ]

    for path in required:
        full = REPO_ROOT / path
        if full.is_file():
            print(f"  OK: {path}")
        else:
            print(f"  MISSING: {path}")
            errors.append(f"Missing required file: {path}")

    return errors


def check_rules_dir() -> list[str]:
    """检查 .codebuddy/rules/ 是否存在并包含必要的规则文件。"""
    errors: list[str] = []

    rules_dir = REPO_ROOT / ".codebuddy" / "rules"
    if not rules_dir.is_dir():
        print("  WARNING: .codebuddy/rules/ does not exist")
        errors.append("Missing directory: .codebuddy/rules/")
        return errors

    expected_rules = [
        "AutonomousWorkflowRules.mdc",
        "CodingStandardRules.mdc",
        "DesignSpecRules.mdc",
        "EffectFeedbackLoopRules.mdc",
        "EpicRequirementDecompositionRules.mdc",
        "ExecutionGuardRules.mdc",
        "ExperienceLayeringRules.mdc",
        "GitBranchRules.mdc",
        "HumanInterventionRules.mdc",
        "IterationLifecycleRules.mdc",
        "SecurityRules.mdc",
        "UnitTestRules.mdc",
        "WorkflowCompletionRules.mdc",
        "WorkflowRules.mdc",
    ]

    for rule in expected_rules:
        full = rules_dir / rule
        if full.is_file():
            print(f"  OK: .codebuddy/rules/{rule}")
        else:
            print(f"  MISSING: .codebuddy/rules/{rule}")
            errors.append(f"Missing rule file: .codebuddy/rules/{rule}")

    return errors


def check_templates_rules_dir() -> list[str]:
    """检查 templates/rules/ 是否存在并包含必要的模板规则文件。"""
    errors: list[str] = []

    templates_rules = REPO_ROOT / "templates" / "rules"
    if not templates_rules.is_dir():
        print("  MISSING: templates/rules/ directory")
        errors.append("Missing directory: templates/rules/")
        return errors

    print("  OK: templates/rules/ exists")

    expected = [
        "ExecutionGuardRules.mdc",
        "EffectFeedbackLoopRules.mdc",
        "ExperienceLayeringRules.mdc",
        "WorkflowCompletionRules.mdc",
        "HumanInterventionRules.mdc",
        "EpicRequirementDecompositionRules.mdc",
        "IterationLifecycleRules.mdc",
    ]

    for f in expected:
        full = templates_rules / f
        if full.is_file():
            print(f"  OK: templates/rules/{f}")
        else:
            print(f"  MISSING: templates/rules/{f}")
            errors.append(f"Missing template rule: templates/rules/{f}")

    return errors


def check_templates_dir() -> list[str]:
    """检查 templates/ 目录结构。"""
    errors: list[str] = []

    templates_dir = REPO_ROOT / "templates"
    if not templates_dir.is_dir():
        print("  MISSING: templates/ directory")
        errors.append("Missing directory: templates/")
        return errors

    print("  OK: templates/ exists")

    # 检查 knowledge-files 目录
    kf_dir = templates_dir / "knowledge-files"
    if kf_dir.is_dir():
        print("  OK: templates/knowledge-files/ exists")
    else:
        print("  MISSING: templates/knowledge-files/ directory")
        errors.append("Missing directory: templates/knowledge-files/")

    return errors


def check_forbidden_dirs() -> list[str]:
    """检查不应存在的业务目录。"""
    errors: list[str] = []

    forbidden = ["src", "tests", "specs", "reports"]
    for d in forbidden:
        full = REPO_ROOT / d
        if full.is_dir():
            print(f"  WARNING: {d}/ should not exist in template repo")
            errors.append(f"Forbidden directory exists: {d}/")
        else:
            print(f"  OK: {d}/ not found (as expected)")

    return errors


def check_forbidden_files() -> list[str]:
    """检查不应存在的构建产物和缓存文件。"""
    errors: list[str] = []

    forbidden = ["coverage.xml", ".coverage"]
    for f in forbidden:
        full = REPO_ROOT / f
        if full.is_file():
            print(f"  WARNING: {f} should not exist in template repo")
            errors.append(f"Forbidden file exists: {f}")
        else:
            print(f"  OK: {f} not found (as expected)")

    cache_dir = REPO_ROOT / ".pytest_cache"
    if cache_dir.is_dir():
        print("  WARNING: .pytest_cache/ should not exist in template repo")
        errors.append("Forbidden cache directory exists: .pytest_cache/")
    else:
        print("  OK: .pytest_cache/ not found (as expected)")

    return errors


def check_cnb_yml() -> list[str]:
    """检查根目录 .cnb.yml 是否为模板自检流水线(不含业务占位符)。"""
    errors: list[str] = []

    cnb_yml = REPO_ROOT / ".cnb.yml"
    if not cnb_yml.is_file():
        print("  MISSING: .cnb.yml")
        errors.append("Missing: .cnb.yml")
        return errors

    content = cnb_yml.read_text(encoding="utf-8")

    # 禁止出现的业务占位符
    forbidden_placeholders = [
        "<your-docker-image>",
        "<install-commands>",
        "<test-commands>",
        "<your-org>/<your-secrets-repo>",
    ]

    for placeholder in forbidden_placeholders:
        if placeholder in content:
            print(f"  WARNING: .cnb.yml contains business placeholder: {placeholder}")
            errors.append(f".cnb.yml contains forbidden placeholder: {placeholder}")

    if errors:
        return errors

    print("  OK: .cnb.yml is clean (no business placeholders)")
    return []


def check_secrets_in_repo() -> list[str]:
    """检查仓库中是否疑似包含敏感信息。"""
    errors: list[str] = []

    # 检查 .codebuddy/ 和 *.md *.yml *.json 中的疑似密钥
    sensitive_patterns = [
        "TAPD_API_USER",
        "TAPD_API_PASSWORD",
        "TAPD_API_TOKEN",
        "TAPD_API_SECRET",
        "TAPD_API_KEY",
    ]

    scan_dirs = [".codebuddy"]
    scan_globs = ["*.md", "*.yml", "*.json"]

    for pattern in sensitive_patterns:
        for root_dir in scan_dirs:
            rdir = REPO_ROOT / root_dir
            if not rdir.is_dir():
                continue
            for dirpath, _subdirs, filenames in os.walk(rdir):
                for fname in filenames:
                    fpath = Path(dirpath) / fname
                    try:
                        text = fpath.read_text(encoding="utf-8", errors="ignore")
                        # 排除占位符 <...> 包裹的内容
                        for line in text.splitlines():
                            if pattern in line:
                                # 如果包含角括号包围的占位符，跳过
                                if "<" in line and ">" in line:
                                    continue
                                # 如果包含冒号后仍有真实值（非占位符），警告
                                parts = line.split(":", 1)
                                if len(parts) > 1:
                                    val = parts[1].strip()
                                    if val and not val.startswith("{") and not val.startswith("<"):
                                        print(f"  WARNING: potential secret in {fpath.relative_to(REPO_ROOT)}: {pattern}")
                                        errors.append(f"Potential secret: {pattern} in {fpath.relative_to(REPO_ROOT)}")
                    except Exception:
                        continue

    if not errors:
        print("  OK: no hardcoded secrets detected")

    return errors


def main() -> int:
    print("=" * 60)
    print("模板仓库自检")
    print("=" * 60)

    all_errors: list[str] = []

    print("\n--- 1. 必须存在的模板文件 ---")
    all_errors.extend(check_required_files())

    print("\n--- 2. .codebuddy/rules/ 规则文件 ---")
    all_errors.extend(check_rules_dir())

    print("\n--- 3. templates/rules/ 模板规则文件 ---")
    all_errors.extend(check_templates_rules_dir())

    print("\n--- 4. templates/ 目录结构 ---")
    all_errors.extend(check_templates_dir())

    print("\n--- 5. 不应存在的业务目录 ---")
    all_errors.extend(check_forbidden_dirs())

    print("\n--- 6. 不应存在的构建产物 ---")
    all_errors.extend(check_forbidden_files())

    print("\n--- 7. .cnb.yml 检查 ---")
    all_errors.extend(check_cnb_yml())

    print("\n--- 8. 敏感信息检查 ---")
    all_errors.extend(check_secrets_in_repo())

    print("\n" + "=" * 60)
    if all_errors:
        print(f"自检失败: {len(all_errors)} 个问题")
        for e in all_errors:
            print(f"  - {e}")
        return 1
    else:
        print("自检全部通过")
        return 0


if __name__ == "__main__":
    sys.exit(main())
