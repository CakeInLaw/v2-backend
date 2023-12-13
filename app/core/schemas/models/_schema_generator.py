from typing import TypeVar, Generic, Type, Any, Callable, overload

from pydantic import BaseModel as PydanticBaseModel

from core.db.models import MODEL


__all__ = ["kw_property", "BaseSchemaGenerator", "SCH", "GEN"]

SCH = TypeVar("SCH", bound=PydanticBaseModel)
GEN = TypeVar("GEN", bound="BaseSchemaGenerator")


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
