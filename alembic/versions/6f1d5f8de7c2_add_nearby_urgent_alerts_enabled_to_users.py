"""add nearby urgent alerts enabled to users

Revision ID: 6f1d5f8de7c2
Revises: 4d9ddf4f2e93
Create Date: 2026-04-03 17:10:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6f1d5f8de7c2"
down_revision: Union[str, Sequence[str], None] = "4d9ddf4f2e93"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "nearby_urgent_alerts_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "nearby_urgent_alerts_enabled")
