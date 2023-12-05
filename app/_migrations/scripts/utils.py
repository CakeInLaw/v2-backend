import sqlalchemy as sa
from sqlalchemy.sql import ExecutableDDLElement
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.autogenerate.api import AutogenContext, render


__all__ = ["op_prefix", "sa_prefix"]


def op_prefix(context: AutogenContext):
    return render._alembic_autogenerate_prefix(context)


def sa_prefix(context: AutogenContext):
    return render._sqlalchemy_autogenerate_prefix(context)


def execute_ddl_elem(op: Operations, ddl_element: ExecutableDDLElement):
    op.execute(ddl_element.compile(op.get_bind()).string)


def get_table_instance(context: MigrationContext, table_name: str, schema_name: str) -> sa.Table:
    metadata: sa.MetaData = context.opts['target_metadata']
    name = f'{schema_name}.{table_name}' if schema_name else table_name
    return metadata.tables[name]
