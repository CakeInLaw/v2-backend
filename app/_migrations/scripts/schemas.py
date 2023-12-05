from sqlalchemy.sql.ddl import CreateSchema, DropSchema
from alembic.autogenerate import renderers, comparators
from alembic.autogenerate.api import AutogenContext
from alembic.operations import MigrateOperation, Operations
from alembic.operations.ops import UpgradeOps

from core.db.models import Model
from . import utils

__all__ = []


@comparators.dispatch_for("schema")
def watch_schemas(
        autogen_context: AutogenContext,
        upgrade_ops: UpgradeOps,
        existed_schemas: set[str | None]
):
    create_schemas_ops = []
    for schema in Model.available_namespaces:
        if schema not in existed_schemas:
            create_schemas_ops.append(CreateSchemaOp(schema))
    if create_schemas_ops:
        upgrade_ops.ops[:0] = create_schemas_ops


@Operations.register_operation('create_schema')
class CreateSchemaOp(MigrateOperation):

    def __init__(self, schema: str):
        self.schema = schema

    @classmethod
    def create_schema(cls, operations: Operations, schema: str):
        return operations.invoke(CreateSchemaOp(schema))

    def reverse(self):
        return DropSchemaOp(self.schema)


@renderers.dispatch_for(CreateSchemaOp)
def render_create_schema(autogen_context: AutogenContext, op: CreateSchemaOp):
    return f"{utils.op_prefix(autogen_context)}create_schema('{op.schema}')"


@Operations.implementation_for(CreateSchemaOp)
def create_schema(operations: Operations, operation: CreateSchemaOp):
    utils.execute_ddl_elem(operations, CreateSchema(operation.schema))


@Operations.register_operation('drop_schema')
class DropSchemaOp(MigrateOperation):

    def __init__(self, schema: str):
        self.schema = schema

    @classmethod
    def drop_schema(cls, operations: Operations, schema: str):
        return operations.invoke(DropSchemaOp(schema))

    def reverse(self):
        return CreateSchemaOp(self.schema)


@renderers.dispatch_for(DropSchemaOp)
def render_drop_schema(autogen_context: AutogenContext, op: CreateSchemaOp):
    return f"{utils.op_prefix(autogen_context)}drop_schema('{op.schema}')"


@Operations.implementation_for(DropSchemaOp)
def drop_schema(operations: Operations, operation: DropSchemaOp):
    utils.execute_ddl_elem(operations, DropSchema(operation.schema))
