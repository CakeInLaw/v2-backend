from typing import Any, Callable, overload, Literal, TypeVar
from core.constants import EMPTY


__all__ = ["clean_kwargs", "default_if_none", "default_if_empty"]

T = TypeVar('T')


def clean_kwargs(*kw_dicts: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
    result_kw = {}
    for kw in *kw_dicts, kwargs:
        result_kw.update({k: v for k, v in kw.items() if v is not EMPTY})
    return result_kw


@overload
def default_if_none(obj, default: T) -> T: ...


@overload
def default_if_none(obj, default: Callable[[], T], is_factory: Literal[True]) -> T: ...


def default_if_none(obj, default: T | Callable[[], T], is_factory: bool = False) -> T:
    if obj is None:
        return default() if is_factory else default
    return obj


@overload
def default_if_empty(obj, default: T) -> T: ...


@overload
def default_if_empty(obj, default: Callable[[], T], is_factory: Literal[True]) -> T: ...


def default_if_empty(obj, default: T | Callable[[], T], is_factory: bool = False) -> T:
    if obj is EMPTY:
        return default() if is_factory else default
    return obj



