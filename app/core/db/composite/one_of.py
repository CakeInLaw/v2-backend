from dataclasses import make_dataclass, field
from typing import Any, Self, cast, Type

from sqlalchemy.orm import composite

__all__ = ["one_of", "OneOfComposite"]


def one_of(cls_name: str, attrs: tuple[str, ...], *, nullable: bool = False):
    cls = cast(Type[OneOfComposite], make_dataclass(
        cls_name=cls_name,
        fields=((f, Any, field(default=None)) for f in attrs),
        bases=(OneOfComposite,),
    ))
    if nullable:
        cls.__nullable__ = True
    return composite(
        cls.__from_tuple__,
        *attrs,
        info={'type': 'one_of'},
    )


class OneOfComposite:
    __dataclass_fields__: dict[str, Any]
    __match_args__: tuple[str, ...]
    __current_set__: str | None = None  # current active set field
    __nullable__ = False

    @classmethod
    def __from_tuple__(cls, kv: tuple[str, Any] | None) -> Self:
        if kv is None:
            return cls()
        return cls.__from_kv__(*kv)

    @classmethod
    def __from_kv__(cls, key: str, value: Any) -> Self:
        return cls(**{key: value})

    @classmethod
    def __empty__(cls):
        return cls()

    def __is_empty__(self) -> bool:
        return self.__current_set__ is None

    @property
    def __current_value__(self):
        if self.__current_set__ is None:
            return None
        return getattr(self, self.__current_set__)

    @classmethod
    def _is_one_of_arg(cls, key: str):
        return key in cls.__match_args__

    def __setattr__(self, key, value):
        if self._is_one_of_arg(key):
            if key != self.__current_set__:
                if self.__current_set__:
                    super().__setattr__(self.__current_set__, None)
                self.__current_set__ = None if value is None else key
        super().__setattr__(key, value)

    def __composite_values__(self):
        return tuple(getattr(self, f) if f == self.__current_set__ else None for f in self.__match_args__)
