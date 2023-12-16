from typing import Type, TYPE_CHECKING, cast

from core.db.models import MODEL

if TYPE_CHECKING:
    from .models import M_GEN


__all__ = ["ModelSchemaGeneratorDispatcher", "model_schema_generators"]


class ModelSchemaGeneratorDispatcher:
    def __init__(self):
        self._reg_map: dict[Type[MODEL], Type["M_GEN"]] = {}

    def dispatch_for(self, model: Type[MODEL]):
        def registrator(gen: Type["M_GEN"]):
            self._reg_map[model] = gen
            return gen
        return registrator

    def dispatch(self, model: Type[MODEL]) -> Type["M_GEN"]:
        for base in model.__mro__:
            if base in self._reg_map:
                base = cast(Type[MODEL], base)
                return self._reg_map[base](model)
        raise Exception(f'No {model} or it`s parent registered')


model_schema_generators = ModelSchemaGeneratorDispatcher()
