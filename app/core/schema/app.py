from pydantic import BaseModel, Field

from core.settings import settings
from core.utils import import_string
from .enums import EnumSchema, ENUM_SCH
from .models import DirectorySchema, DIR_SCH, DocumentSchema, DOC_SCH


__all__ = ["AppSchema", "create_default_app_schema", "get_default_app_schema"]


class AppInfo(BaseModel):
    version: str


class AppSchema(BaseModel):
    info: AppInfo

    enums: list[ENUM_SCH] = Field(default_factory=list)
    directories: list[DIR_SCH] = Field(default_factory=list)
    documents: list[DOC_SCH] = Field(default_factory=list)

    def add_enum(self, schema: ENUM_SCH):
        assert isinstance(schema, EnumSchema)
        assert not list(filter(lambda sch: sch.name == schema.name, self.enums))
        self.enums.append(schema)

    def add_directory(self, schema: DIR_SCH):
        assert isinstance(schema, DirectorySchema)
        assert not list(filter(lambda sch: sch.name == schema.name, self.directories))
        self.directories.append(schema)

    def add_document(self, schema: DOC_SCH):
        assert isinstance(schema, DocumentSchema)
        assert not list(filter(lambda sch: sch.name == schema.name, self.documents))
        self.documents.append(schema)


_default_app_schema = None


def create_default_app_schema():
    global _default_app_schema
    assert _default_app_schema is None
    _default_app_schema = AppSchema(info=AppInfo(version=settings.app.VERSION))
    for collector in settings.schema_collectors:
        import_string(collector)(app_schema=_default_app_schema).collect()


def get_default_app_schema() -> AppSchema:
    global _default_app_schema
    assert isinstance(_default_app_schema, AppSchema)
    return _default_app_schema
