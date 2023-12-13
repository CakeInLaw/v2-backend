from typing import Generic, TypeVar, Type, overload

from pydantic import BaseModel

from core.db.models import MODEL, Model
from ._schema_generator import BaseSchemaGenerator, GEN, kw_property
from .._enums import AttrTypes


__all__ = ["AttrSchema", "A_SCH", "AttrSchemaGenerator", "AttrSchemaGeneratorDispatcher"]


T = TypeVar("T")
ATTR = TypeVar("ATTR")
A_SCH = TypeVar("A_SCH", bound="AttrSchema")


class AttrSchema(BaseModel):
    name: str
    model: str
    attr_type: AttrTypes


class AttrSchemaGenerator(BaseSchemaGenerator[A_SCH, MODEL], Generic[A_SCH, MODEL, ATTR]):

    _attr_type: AttrTypes

    def __init__(self, model: Type[MODEL], attr: ATTR):
        super().__init__(model=model)
        self._attr = attr

    @kw_property
    def attr_type(self) -> AttrTypes:
        return self._attr_type

    @kw_property
    def model(self) -> str:
        return self._model.__full_name__


class AttrSchemaGeneratorDispatcher(Generic[GEN, T, ATTR]):
    def __init__(self, allow_model_attrs: bool = True):
        self._reg_map: dict[T | tuple[MODEL, str], Type[GEN]] = {}
        self.allow_model_attrs = allow_model_attrs

    @overload
    def dispatch_for(self, type_: T): ...

    @overload
    def dispatch_for(self, type_: Type[MODEL], name: str): ...

    def dispatch_for(self, type_: T | Type[MODEL], name: str = None):
        def registrator(generator: Type[GEN]):
            if self.should_reg_by_type(type_):
                self.reg_by_type(type_=type_, generator=generator)
            else:
                assert self.allow_model_attrs
                self.reg_by_model(model=type_, name=name, generator=generator)
            return generator

        return registrator

    def should_reg_by_type(self, type_):
        return not issubclass(type_, Model)

    def reg_by_type(self, type_, generator: Type[GEN]):
        assert type_ not in self._reg_map, f'{type_=} is already registered'
        self._reg_map[type_] = generator

    def reg_by_model(self, model: Type[MODEL], name: str, generator: Type[GEN]):
        assert issubclass(model, Model) and name
        comb = (model, name)
        assert comb not in self._reg_map, f'{model}.{name} is already registered'
        self._reg_map[comb] = generator

    def dispatch(
            self,
            model: Type[MODEL],
            attr: ATTR,
    ) -> GEN | None:
        if self.allow_model_attrs and (comb := (model, attr.key)) in self._reg_map:
            generator = self._reg_map[comb]
        else:
            generator = self._dispatch_by_attr(model=model, attr=attr)
        return generator(model=model, attr=attr) if generator else None

    def _dispatch_by_attr(self, model: Type[MODEL], attr: ATTR) -> Type[GEN] | None:
        pass
