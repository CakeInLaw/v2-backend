from typing import Type, cast

from pydantic import BaseModel

from core.settings import settings
from core.db.models import MODEL, ListModel
from .enums import EnumDescription, collect_enums
from .models import DirectorySchema, collect_directories, DocumentSchema, collect_documents, M_SCH, ObjectSchema


__all__ = ["AppSchema", "get_app_schema", "get_model_schema"]


class AppInfo(BaseModel):
    version: str


class AppSchema(BaseModel):
    info: AppInfo

    enums: list[EnumDescription]
    directories: list[DirectorySchema]
    documents: list[DocumentSchema]


_default_app_schema = None


def get_app_schema() -> AppSchema:
    global _default_app_schema
    if _default_app_schema is None:
        _default_app_schema = AppSchema.model_construct(
            info=AppInfo(version=settings.app.VERSION),
            enums=collect_enums(),
            directories=collect_directories(),
            documents=collect_documents(),
        )
    return _default_app_schema


def get_model_schema(model: Type[MODEL]) -> M_SCH:
    from sqlalchemy import Table
    if issubclass(model, ListModel):
        parent: ObjectSchema = get_model_schema(model.__OWNER__)
        table = cast(Table, model.__table__)
        return list(filter(lambda x: x.name == table.name, parent.lists))[0]
    table = cast(Table, model.__table__)
    return list(filter(lambda x: x.name == table.name, getattr(get_app_schema(), table.schema)))[0]
