from dataclasses import make_dataclass, field
from typing import Any

from sqlalchemy.orm import composite

__all__ = ["one_of", "OneOfComposite"]


def one_of(cls_name: str, fields: tuple[str, ...], *, required: bool = False):
    cls = make_dataclass(
        cls_name=cls_name,
        fields=((f, Any, field(default=None))for f in fields),
        bases=(OneOfComposite,),
    )
    if required:
        cls.__required__ = True
    return composite(
        cls,
        *fields,
        info={'type': 'one_of'},
    )


class OneOfComposite:
    __dataclass_fields__: dict[str, Any]
    __match_args__: tuple[str, ...]
    __current_set__: str | None = None  # current active set field
    __required__ = False

    @classmethod
    def from_kv(cls, key: str, value: Any):
        self = cls(**{key: value})
        for f in self.__match_args__:
            setattr(self, f, None)
        setattr(self, key, value)
        return self

    @classmethod
    def is_one_of_arg(cls, key: str):
        return key in cls.__match_args__

    def __setattr__(self, key, value):
        if self.is_one_of_arg(key):
            if key != self.__current_set__:
                if self.__current_set__:
                    super().__setattr__(self.__current_set__, None)
                self.__current_set__ = None if value is None else key
            super().__setattr__(key, value)
        else:
            super().__setattr__(key, value)

    def __composite_values__(self):
        return tuple(getattr(self, f) if f == self.__current_set__ else None for f in self.__match_args__)
