# -*- coding: utf-8 -*-
import json
from pathlib import Path


DEFAULT_WIDTH = 760
DEFAULT_HEIGHT = 90
DEFAULT_ALPHA = 0.75
DEFAULT_SHOW_TIP = False
DEFAULT_LOCKED = False
MIN_WIDTH = 240
MIN_HEIGHT = 48
BOTTOM_OFFSET = 80
CONFIG_PATH = Path.home() / ".subtitle_masker_config.json"


def load_config():
    """Read config safely; invalid or broken files fall back to defaults."""
    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return {}

    return data if isinstance(data, dict) else {}


def save_config(data):
    """Persist config data and ignore write failures."""
    try:
        with CONFIG_PATH.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError:
        pass


def config_int(config, key, default, minimum=None):
    try:
        value = int(config.get(key, default))
    except (TypeError, ValueError):
        value = default

    return max(minimum, value) if minimum is not None else value


def config_float(config, key, default, minimum=None, maximum=None):
    try:
        value = float(config.get(key, default))
    except (TypeError, ValueError):
        value = default

    if minimum is not None:
        value = max(minimum, value)
    if maximum is not None:
        value = min(maximum, value)
    return value


def config_bool(config, key, default):
    value = config.get(key, default)
    return value if isinstance(value, bool) else default


def config_position(config):
    x = config.get("x")
    y = config.get("y")
    if isinstance(x, int) and not isinstance(x, bool) and isinstance(y, int) and not isinstance(y, bool):
        return x, y
    return None


def is_geometry_on_screen(x, y, width, height, screen_width, screen_height):
    """Reject saved geometry that would start off-screen or exceed the display."""
    return (
        width <= screen_width
        and height <= screen_height
        and x >= 0
        and y >= 0
        and x + width <= screen_width
        and y + height <= screen_height
    )
