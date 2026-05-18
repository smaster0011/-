# -*- coding: utf-8 -*-
from .version import APP_RELEASE_CHANNEL, APP_VERSION


RELEASE_PAGE_URL = ""


def get_current_version():
    """Return the local version string without contacting any network service."""
    return APP_VERSION


def get_update_policy_text():
    """Describe the current non-network update policy for UI or docs reuse."""
    return (
        f"当前版本：v{APP_VERSION}\n"
        f"发布通道：{APP_RELEASE_CHANNEL}\n\n"
        "v1.0.0 不会自动联网检查更新。\n"
        "未来版本可能提供由用户主动触发的检查更新功能。\n"
        "更新信息以 CHANGELOG.md 和发布页面为准。"
    )


def open_release_page():
    """Reserved for a future user-triggered release page action."""
    return False
