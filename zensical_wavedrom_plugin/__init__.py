from __future__ import annotations

from zensical_wavedrom_plugin.extension import WavedromExtension


def makeExtension(**kwargs: object) -> WavedromExtension:
    """Register Markdown extension."""
    return WavedromExtension(**kwargs)
