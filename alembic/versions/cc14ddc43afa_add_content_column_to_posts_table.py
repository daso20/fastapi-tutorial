"""add content column to posts table

Revision ID: cc14ddc43afa
Revises: ec16a0d08beb
Create Date: 2023-11-27 15:47:43.712750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc14ddc43afa'
down_revision: Union[str, None] = 'ec16a0d08beb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass