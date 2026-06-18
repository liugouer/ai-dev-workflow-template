import glob
import json
import os
import sys
from typing import Any, Dict

import requests
from requests.auth import HTTPBasicAuth


def env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


TAPD_API_BASE_URL = env("TAPD_API_BASE_URL", "https://api.tapd.cn").rstrip("/")
TAPD_API_USER = env("TAPD_API_USER")
TAPD_API_PASSWORD = env("TAPD_API_PASSWORD")
TAPD_COMMENT_AUTHOR = env("TAPD_COMMENT_AUTHOR", TAPD_API_USER)


def require_enabled_and_credentials() -> None:
    if env("TAPD_ARCHIVE_ENABLED", "false").lower() != "true":
        print("TAPD archive disabled, skip.")
        sys.exit(0)

    missing = [
        name for name, value in {
            "TAPD_API_USER": TAPD_API_USER,
            "TAPD_API_PASSWORD": TAPD_API_PASSWORD,
            "TAPD_COMMENT_AUTHOR": TAPD_COMMENT_AUTHOR,
        }.items()
        if not value
    ]

    if missing:
        raise RuntimeError(f"Missing TAPD env vars: {', '.join(missing)}")


def tapd_post(path: str, data: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{TAPD_API_BASE_URL}{path}"

    response = requests.post(
        url,
        data=data,
        auth=HTTPBasicAuth(TAPD_API_USER, TAPD_API_PASSWORD),
        timeout=30,
    )
    if response.status_code >= 400:
        print(f"TAPD HTTP error: {response.status_code}")
        print(f"URL: {url}")
        print(f"Response: {response.text[:1000]}")
        response.raise_for_status()

    result = response.json()
    if str(result.get("status")) != "1":
        raise RuntimeError(f"TAPD API failed: {result}")

    return result


def update_story_status(workspace_id: str, story_id: str, status_name: str) -> None:
    print(f"Update TAPD story {story_id} status to {status_name}")

    tapd_post(
        "/stories",
        {
            "workspace_id": workspace_id,
            "id": story_id,
            "v_status": status_name,
            "current_user": TAPD_COMMENT_AUTHOR,
        },
    )


def add_story_comment(workspace_id: str, story_id: str, description: str) -> None:
    print(f"Add archive comment to TAPD story {story_id}")

    tapd_post(
        "/comments",
        {
            "workspace_id": workspace_id,
            "entry_type": "stories",
            "entry_id": story_id,
            "description": description,
            "author": TAPD_COMMENT_AUTHOR,
        },
    )


def build_comment(config: Dict[str, Any]) -> str:
    story_id = str(config.get("story_id", "unknown"))
    workspace_id = str(config.get("workspace_id", "unknown"))

    return f"""【AI研发自动化闭环归档报告】

归档标识：AI-AUTO-ARCHIVE:TAPD-{story_id}

TAPD 项目 ID：{workspace_id}
TAPD 需求 ID：{story_id}
需求标题：{config.get("title", "")}

一、质量验证结果

- pytest：{config.get("pytest_result", "")}
- 覆盖率：{config.get("coverage_result", "")}
- AI Code Review：{config.get("ai_review_result", "")}
- CNB 流水线：{config.get("cnb_pipeline_result", "")}
- 合并结果：已合并到 {config.get("target_branch", "main")}

二、分支信息

- 来源分支：{config.get("source_branch", "")}
- 目标分支：{config.get("target_branch", "main")}

三、结论

{config.get("summary", "")}

当前状态：已完成
"""


def process_archive_file(path: str) -> None:
    print(f"Process archive file: {path}")

    with open(path, "r", encoding="utf-8-sig") as file:
        config = json.load(file)

    workspace_id = str(config.get("workspace_id", ""))
    if not workspace_id:
        print(f"ERROR: Missing 'workspace_id' in {path}, skip this file")
        return

    story_id = config.get("story_id", "")
    if not story_id:
        print(f"ERROR: Missing 'story_id' in {path}, skip this file")
        return
    story_id = str(story_id)

    update_story_status(workspace_id, story_id, str(config.get("merged_status", "已合并")))
    add_story_comment(workspace_id, story_id, build_comment(config))
    update_story_status(workspace_id, story_id, str(config.get("done_status", "已完成")))

    print(f"TAPD story {story_id} archived successfully.")


def main() -> int:
    require_enabled_and_credentials()

    files = sorted(glob.glob("reports/tapd-*-archive.json"))
    if not files:
        print("No TAPD archive files found, skip.")
        return 0

    for path in files:
        process_archive_file(path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
