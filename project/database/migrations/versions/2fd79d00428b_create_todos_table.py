"""create todos table

Revision ID: 2fd79d00428b
Revises:
Create Date: 2020-02-20 20:20:20.202020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fd79d00428b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'todos',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('completed', sa.Boolean(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('todos')
