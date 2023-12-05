from typing import TypeVar, Generic, Type, Any, Callable, overload

from pydantic import BaseModel as PydanticBaseModel

from core.db.models import MODEL, Model


__all__ = ["kw_property", "BaseSchemaGenerator", "BaseAttrSchemaGenerator", "AttrSchemaGeneratorDispatcher"]

SCH = TypeVar("SCH", bound=PydanticBaseModel)
GEN = TypeVar("GEN", bound="BaseSchemaGenerator")
T = TypeVar("T")
ATTR = TypeVar("ATTR")


class SchemaGeneratorMeta(type):
    def __new__(cls, name: str, bases: tuple[type, ...], params: dict[str, Any]):
        # key is key name in pydantic schema, value - property name in generator class
        params['_schema_kwargs_keys'] = schema_kwargs_keys = {}
        for name, par in params.items():
            if getattr(par, '_schema_kwargs_key', False):
                par: KWProperty
                schema_kwargs_keys[name] = par.name
        return super().__new__(cls, name, bases, params)


class KWProperty:
    _schema_kwargs_key: bool = True

    def __init__(self, getter: Callable[[GEN], Any], name: str = None):
        self.getter = getter
        # name in pydantic schema
        self.name = name or getter.__name__

    def __get__(self, instance: GEN, owner: Type[GEN]):
        if instance is None:
            return self
        return self.getter(instance)


@overload
def kw_property(getter_or_name: Callable[[GEN], Any]) -> KWProperty: ...


@overload
def kw_property(getter_or_name: str) -> Callable[[Callable[[GEN], Any]], KWProperty]: ...


def kw_property(
        getter_or_name: Callable[[GEN], Any] | str
) -> Callable[[Callable[[GEN], Any]], KWProperty] | KWProperty:
    if isinstance(getter_or_name, str):

        def kw_property_with_name(getter: Callable[[GEN], Any]):
            return KWProperty(getter, name=getter_or_name)

        return kw_property_with_name

    return KWProperty(getter=getter_or_name)


class BaseSchemaGenerator(Generic[SCH, MODEL], metaclass=SchemaGeneratorMeta):
    schema_cls: Type[SCH]

    def __init__(self, model: Type[MODEL]):
        self._model = model

    def schema_kwargs(self):
        keys = {}
        for base in self.__class__.__mro__:
            if k := getattr(base, '_schema_kwargs_keys', None):
                keys.update(k)
        return {key: getattr(self, prop_name) for prop_name, key in keys.items()}

    def schema(self):
        return self.get_schema_cls()(**self.schema_kwargs())

    def get_schema_cls(self) -> Type[SCH]:
        return self.schema_cls


class BaseAttrSchemaGenerator(BaseSchemaGenerator[SCH, MODEL], Generic[SCH, MODEL, ATTR]):

    def __init__(self, model: Type[MODEL], attr: ATTR):
        super().__init__(model=model)
        self._attr = attr


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
