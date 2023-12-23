from typing import Type, Generic

from core.schema import SCH

from .gen_property import gen_property


__all__ = ["BaseSchemaGenerator"]


class BaseSchemaGenerator(Generic[SCH]):
    schema_cls: Type[SCH]

    def schema_kwargs(self):
        # key of this dict is name in schema, value is generator property name
        # this example result is properties = {'name_in_schema': '_some_other_name'}
        # @gen_property('name_in_schema')
        # def _some_other_name(self): ...
        properties = {}
        for base_bases in self.__class__.__mro__[::-1]:
            for k, v in base_bases.__dict__.items():
                if isinstance(v, gen_property):
                    properties[v.name] = k

        return {key: getattr(self, prop_name) for key, prop_name in properties.items()}

    def schema(self) -> SCH:
        return self.get_schema_cls()(**self.schema_kwargs())

    def get_schema_cls(self) -> Type[SCH]:
        return self.schema_cls
