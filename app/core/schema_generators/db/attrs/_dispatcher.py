from typing import Generic, TypeVar, Type, overload, Protocol

from core.db import Model
from core.db.models import MODEL

from ._base import ATTR_GEN


__all__ = ["AttrSchemaGeneratorDispatcher"]


class HasKey(Protocol):
    key: str


T = TypeVar('T')
ATTR = TypeVar('ATTR', bound=HasKey)


class AttrSchemaGeneratorDispatcher(Generic[ATTR_GEN, T, ATTR]):
    def __init__(self, allow_model_attrs: bool = True):
        self._reg_map: dict[T | tuple[MODEL, str], Type[ATTR_GEN]] = {}
        self.allow_model_attrs = allow_model_attrs

    @overload
    def dispatch_for(self, type_: T): ...

    @overload
    def dispatch_for(self, type_: Type[MODEL], name: str): ...

    def dispatch_for(self, type_: T | Type[MODEL], name: str = None):
        def registrator(generator: Type[ATTR_GEN]):
            if self.should_reg_by_type(type_):
                self.reg_by_type(type_=type_, generator=generator)
            else:
                assert self.allow_model_attrs
                self.reg_by_model(model=type_, name=name, generator=generator)
            return generator

        return registrator

    def should_reg_by_type(self, type_: T | Type[MODEL]):
        return not issubclass(type_, Model)

    def reg_by_type(self, type_, generator: Type[ATTR_GEN]):
        assert type_ not in self._reg_map, f'{type_=} is already registered'
        self._reg_map[type_] = generator

    def reg_by_model(self, model: Type[MODEL], name: str, generator: Type[ATTR_GEN]):
        assert issubclass(model, Model) and name
        comb = (model, name)
        assert comb not in self._reg_map, f'{model}.{name} is already registered'
        self._reg_map[comb] = generator

    def get_attr_name(self, attr: ATTR) -> str:
        return attr.key

    def dispatch(
            self,
            owner: Type[MODEL],
            attr: ATTR,
    ) -> ATTR_GEN | None:
        if self.allow_model_attrs and (comb := (owner, self.get_attr_name(attr))) in self._reg_map:
            generator = self._reg_map[comb]
        else:
            generator = self._dispatch_by_attr(model=owner, attr=attr)
        return generator(owner=owner, attr=attr) if generator else None

    def _dispatch_by_attr(self, model: Type[MODEL], attr: ATTR) -> Type[ATTR_GEN] | None:
        pass
