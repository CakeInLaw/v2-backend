from alembic.migration import MigrationContext
from alembic.operations import MigrationScript

from . import schemas
from .disallow_empty import disallow_empty_migration

__all__ = ["process_revision_directives"]


def process_revision_directives(context: MigrationContext, revision: str, directives: list[MigrationScript]):
    if context.config.cmd_opts.autogenerate:
        disallow_empty_migration(directives)
