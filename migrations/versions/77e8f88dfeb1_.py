"""empty message

Revision ID: 77e8f88dfeb1
Revises: 72b1b08a2fbf
Create Date: 2022-08-08 17:59:40.876584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77e8f88dfeb1'
down_revision = '72b1b08a2fbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('donation', sa.Column('received', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('donation', 'received')
    # ### end Alembic commands ###