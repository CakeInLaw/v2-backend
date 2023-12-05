from alembic.operations.ops import MigrationScript


__all__ = ["disallow_empty_migration"]


def disallow_empty_migration(directives: list[MigrationScript]):
    if len(directives) == 1:
        script = directives[0]
        if (
                len(script.upgrade_ops_list) == 0
                or all([ops.is_empty() for ops in script.upgrade_ops_list])
        ):
            directives[:] = []
    else:
        raise ValueError(f'directives len is not equal to 1 ({directives})')
