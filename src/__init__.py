"""Image Zoom: enlarge or shrink the images on cards during review, without
zooming the text around them."""

from __future__ import annotations

import json
from typing import Callable

from aqt import gui_hooks, mw
from aqt.reviewer import Reviewer
from aqt.utils import tooltip
from aqt.webview import WebContent

# the zoom level (number of steps from 100%) is kept per profile rather than
# in config.json, so that the config dialog only holds settings the user chose
STATE_KEY = "image_zoom_addon:level"
STYLE_ID = "image-zoom-addon"


def _config() -> dict:
    return mw.addonManager.getConfig(__name__) or {}


def _level() -> int:
    return int(mw.pm.meta.get(STATE_KEY, 0))


def _factor(level: int) -> float:
    conf = _config()
    factor = conf.get("step", 1.25) ** level
    return min(max(factor, conf.get("min_zoom", 0.5)), conf.get("max_zoom", 10.0))


def _css(factor: float) -> str:
    # at 100% no rule applies at all, so rendering is unchanged
    if factor == 1.0:
        return ""
    # Scoped to #qa so it outranks a note type's own `.card img` rules. The
    # max-width: 100% that fits large images to the card is a percentage,
    # which zoom doesn't scale, so it is scaled here to keep growth smooth;
    # max-height is in vh, which zoom already scales. Image occlusion sizes
    # its images from the container, and whiteboard drawings carry their own
    # fixed zoom, so both are left alone.
    return (
        "#qa img:not(#image-occlusion-container img):not(.drawing)"
        f" {{ zoom: {factor}; max-width: calc(100% * {factor}); }}"
    )


def _on_webview_will_set_content(web_content: WebContent, context: object) -> None:
    if isinstance(context, Reviewer):
        web_content.head += f'<style id="{STYLE_ID}">{_css(_factor(_level()))}</style>'


def _set_level(level: int) -> None:
    factor = _factor(level)
    mw.pm.meta[STATE_KEY] = level
    # the reviewer only reloads its page when a session starts, so update the
    # injected stylesheet in place
    mw.reviewer.web.eval(
        f"document.getElementById({json.dumps(STYLE_ID)}).textContent"
        f" = {json.dumps(_css(factor))};"
    )
    # the only feedback available, as there is no menu item
    tooltip(f"Image zoom {round(factor * 100)}%", period=1000)


def _adjust_zoom(delta: int) -> None:
    level = _level()
    # don't step past a limit, so a single press always reverses the last one;
    # steps back toward 100% always count, in case the limits were lowered
    if delta * level < 0 or _factor(level + delta) != _factor(level):
        level += delta
    _set_level(level)


def _on_state_shortcuts_will_change(
    state: str, shortcuts: list[tuple[str, Callable]]
) -> None:
    if state != "review":
        return
    conf = _config()
    actions: list[tuple[str, Callable[[], None]]] = [
        ("zoom_in_shortcuts", lambda: _adjust_zoom(1)),
        ("zoom_out_shortcuts", lambda: _adjust_zoom(-1)),
        ("reset_shortcuts", lambda: _set_level(0)),
    ]
    for key, action in actions:
        for keys in conf.get(key, []):
            shortcuts.append((keys, action))


gui_hooks.webview_will_set_content.append(_on_webview_will_set_content)
gui_hooks.state_shortcuts_will_change.append(_on_state_shortcuts_will_change)
