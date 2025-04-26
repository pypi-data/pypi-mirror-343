from __future__ import annotations

from .lisa import _register_all, get_cmap, list_cmaps

__version__ = "1.0.0"

__all__ = ["get_cmap", "list_cmaps"]

_register_all()
