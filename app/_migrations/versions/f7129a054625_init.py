"""init

Revision ID: f7129a054625
Revises: 
Create Date: 2023-12-04 16:59:57.080396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from core.db import types
import enums


# revision identifiers, used by Alembic.
revision: str = "f7129a054625"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_schema("documents")
    op.create_schema("directories")
    op.create_table(
        "users",
        sa.Column("username", types.String(max_length=20), nullable=False),
        sa.Column("password_hash", types.String(max_length=200), nullable=False),
        sa.Column("password_salt", types.String(max_length=200), nullable=False),
        sa.Column("password_changed_at", types.DateTime(timezone=True), nullable=False),
        sa.Column("is_superuser", types.Boolean(), nullable=False),
        sa.Column(
            "id", types.Guid(), server_default="get_random_uuid()", nullable=False, read_only=True
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
        schema="directories",
    )
    op.create_table(
        "employees",
        sa.Column("user_id", types.Guid(), nullable=False),
        sa.Column("name", types.String(max_length=100), nullable=False),
        sa.Column(
            "id", types.Guid(), server_default="get_random_uuid()", nullable=False, read_only=True
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["directories.users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
        schema="directories",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("employees", schema="directories")
    op.drop_table("users", schema="directories")
    op.drop_schema("directories")
    op.drop_schema("documents")
    # ### end Alembic commands ###