from __future__ import annotations

import sys
import types
from typing import Any, Callable, List, overload

__all__: List[str] = ["expose", "reexpose"]
__version__ = "0.1.0"

_ModuleType = types.ModuleType

def __dir__():
    return __all__

def _ensure_module_dir_hook(module: _ModuleType) -> None:
    if getattr(module, "_expose_dir_patched", False):
        return

    def _dir() -> List[str]:
        return list(getattr(module, "__all__", []))

    module.__dir__ = _dir  # type: ignore[assignment]
    module._expose_dir_patched = True  # type: ignore[attr-defined]


def _register_symbol(module: _ModuleType, name: str) -> None:
    all_list: List[str] = module.__dict__.setdefault("__all__", [])
    if name not in all_list:
        all_list.append(name)
    _ensure_module_dir_hook(module)


@overload
def expose(obj: Callable[..., Any]) -> Callable[..., Any]: ...
@overload
def expose(*, name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


def expose(
    obj: Callable[..., Any] | None = None, *, name: str | None = None
) -> Callable[..., Any]:
    def _decorator(target: Callable[..., Any]) -> Callable[..., Any]:
        module = sys.modules[target.__module__]
        export_name = name or target.__name__
        _register_symbol(module, export_name)
        if name:
            module.__dict__[export_name] = target
        return target

    return _decorator if obj is None else _decorator(obj)


def reexpose(obj: Any, *, name: str | None = None) -> Any:
    module = sys.modules[obj.__module__]
    if not hasattr(module, "__all__"):
        raise RuntimeError(f"{obj} was not exposed in its original module")

    this_module = sys.modules[sys._getframe(1).f_globals["__name__"]]
    export_name = name or obj.__name__
    this_module.__dict__[export_name] = obj
    _register_symbol(this_module, export_name)
    return obj

