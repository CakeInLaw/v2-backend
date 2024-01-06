from abc import ABC
from typing import Iterator, Generic

from core.schema import O_SCH, DIR_SCH, DOC_SCH, SCH
from ._base import BaseSchemaCollector


__all__ = [
    "DirectorySchemaCollector", "DocumentSchemaCollector",
    "SaDirectorySchemaCollector", "SaDocumentSchemaCollector",
]


class DirectorySchemaCollector(BaseSchemaCollector[DIR_SCH], ABC):

    def add_in_schema(self, schema: SCH):
        self.app_schema.add_directory(schema=schema)


class DocumentSchemaCollector(BaseSchemaCollector[DOC_SCH], ABC):

    def add_in_schema(self, schema: SCH):
        self.app_schema.add_document(schema=schema)


class ObjectSchemaCollectorMixin(Generic[O_SCH]):
    namespace: str

    def __iter__(self) -> Iterator[O_SCH]:
        from core.db import Model
        from core.schema_generators.db import model_schema_generators
        for _, model in Model.iter_models(self.namespace):
            if getattr(model, '_include_in_schema', False):
                yield model_schema_generators.dispatch(model).schema()


class SaDirectorySchemaCollector(ObjectSchemaCollectorMixin[DIR_SCH], DirectorySchemaCollector[DIR_SCH]):
    namespace = 'directories'


class SaDocumentSchemaCollector(ObjectSchemaCollectorMixin[DOC_SCH], DocumentSchemaCollector[DOC_SCH]):
    namespace = 'documents'
