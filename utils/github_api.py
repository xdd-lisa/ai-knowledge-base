from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any

import requests

logger = logging.getLogger(__name__)

_HTTP_SUCCESS = 200
_EXPECTED_REPO_PARTS = 2


@dataclass
class RepoInfo:
    full_name: str
    description: str
    stars: int
    forks: int
    url: str


def fetch_repo_info(repo_full_name: str) -> RepoInfo:
    """从 GitHub API 获取指定仓库的基本信息。

    Args:
        repo_full_name: 仓库全名，格式为 "owner/repo"，如 "langchain-ai/langgraph"。

    Returns:
        RepoInfo: 包含仓库全名、描述、Star 数、Fork 数、URL 的数据对象。

    Raises:
        ValueError: 仓库全名格式无效。
        requests.RequestException: API 请求失败或返回非 200 状态码。
    """
    parts = repo_full_name.split("/")
    if "/" not in repo_full_name or len(parts) != _EXPECTED_REPO_PARTS:
        msg = (
            f"Invalid repo full name: {repo_full_name!r}, expected format 'owner/repo'"
        )
        raise ValueError(msg)

    token = os.environ.get("GITHUB_TOKEN")
    headers: dict[str, str] = {
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"https://api.github.com/repos/{repo_full_name}"
    logger.info("Fetching repo info from %s", url)

    resp = requests.get(url, headers=headers, timeout=15)
    if resp.status_code != _HTTP_SUCCESS:
        msg = (
            f"GitHub API returned {resp.status_code} for {repo_full_name}: "
            f"{resp.json().get('message', 'unknown error')}"
        )
        raise requests.RequestException(msg)

    data: dict[str, Any] = resp.json()
    repo_info = RepoInfo(
        full_name=data["full_name"],
        description=data.get("description") or "",
        stars=data["stargazers_count"],
        forks=data["forks_count"],
        url=data["html_url"],
    )
    logger.info(
        "Got repo %s: stars=%s, forks=%s",
        repo_info.full_name,
        repo_info.stars,
        repo_info.forks,
    )
    return repo_info
