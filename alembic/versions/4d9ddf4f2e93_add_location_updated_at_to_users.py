"""add location_updated_at to users

Revision ID: 4d9ddf4f2e93
Revises: b07d722038a1
Create Date: 2026-04-03 09:20:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4d9ddf4f2e93"
down_revision: Union[str, Sequence[str], None] = "b07d722038a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("location_updated_at", sa.DateTime(), nullable=True))
    op.execute(
        """
        UPDATE users
        SET location_updated_at = updated_at
        WHERE current_lat IS NOT NULL
        AND current_lng IS NOT NULL
        AND updated_at IS NOT NULL
        """
    )


def downgrade() -> None:
    op.drop_column("users", "location_updated_at")
