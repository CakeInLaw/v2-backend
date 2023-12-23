from typing import Self, Union

from ._base import ValidationError


__all__ = ["ObjectErrors", "ListErrors", "RootError"]


class RootError(ValidationError):
    pass


class ListErrors(Exception):
    def __init__(self):
        self._objects_map: dict[int, "ObjectErrors"] = {}

    def export(self):
        return {k: err.export() for k, err in self._objects_map.items()}

    def add(self, idx: int, err: Union["ObjectErrors", ValidationError]):
        self._objects_map[idx] = err

    def __bool__(self):
        return len(self._objects_map) > 0

    def __contains__(self, item: int):
        return item in self._objects_map

    def __getitem__(self, item: int):
        return self._objects_map[item]


class ObjectErrors(Exception):
    def __init__(self):
        super().__init__()
        self._errors: dict[str, ListErrors | ValidationError | Self] = {}
        self._root: list[RootError] = []

    def export(self):
        errors = {key: error.export() for key, error in self._errors.items()}
        if self._root:
            errors['__root__'] = [err.export() for err in self._root]
        return errors

    def add(self, field: str, error: ValidationError | ListErrors | Self) -> Self:
        if field == '__root__':
            assert isinstance(error, RootError)
            self._root.append(error)
        else:
            self._errors[field] = error
        return self

    def merge(self, obj_error: Self) -> Self:
        self._errors.update(obj_error._errors)
        self._root.extend(obj_error._root)
        return self

    def __bool__(self) -> bool:
        return not not (self._errors or self._root)
