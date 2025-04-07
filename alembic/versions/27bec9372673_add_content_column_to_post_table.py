"""add content column to post table

Revision ID: 27bec9372673
Revises: 3407722a3a61
Create Date: 2025-04-07 12:11:24.315096

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27bec9372673'
down_revision: Union[str, None] = '3407722a3a61'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
