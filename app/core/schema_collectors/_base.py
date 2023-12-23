from abc import ABC, abstractmethod
from typing import Generic, Iterator

from core.schema import SCH, AppSchema

__all__ = ["BaseSchemaCollector"]


class BaseSchemaCollector(Generic[SCH], ABC):

    def __init__(self, app_schema: AppSchema):
        self.app_schema = app_schema

    def collect(self):
        for schema in self:
            self.add_in_schema(schema=schema)

    @abstractmethod
    def __iter__(self) -> Iterator[SCH]:
        raise NotImplementedError

    @abstractmethod
    def add_in_schema(self, schema: SCH):
        raise NotImplementedError
