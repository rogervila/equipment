"""create example table

Revision ID: 0797374c92af
Revises:
Create Date: 2021-06-07 14:58:43.762044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0797374c92af'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
        sa.Column('price', sa.Integer, default=0, nullable=False),
    )


def downgrade():
    op.drop_table('products')
