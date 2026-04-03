"""add user device tokens

Revision ID: f2b8e7c9134a
Revises: 6f1d5f8de7c2
Create Date: 2026-04-03 18:20:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f2b8e7c9134a"
down_revision: Union[str, Sequence[str], None] = "6f1d5f8de7c2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_device_tokens",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("device_token", sa.String(length=512), nullable=False),
        sa.Column("platform", sa.String(length=20), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("device_token", name="uq_user_device_token_value"),
    )
    op.create_index(op.f("ix_user_device_tokens_id"), "user_device_tokens", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_user_device_tokens_id"), table_name="user_device_tokens")
    op.drop_table("user_device_tokens")
