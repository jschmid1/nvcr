"""empty message

Revision ID: 9ef32a11645a
Revises: e13d5277b7d8
Create Date: 2018-01-26 15:47:03.131152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ef32a11645a'
down_revision = 'e13d5277b7d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_bill_id_key', 'user_bill', type_='unique')
    op.drop_column('user_bill', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_bill', sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_unique_constraint('user_bill_id_key', 'user_bill', ['id'])
    # ### end Alembic commands ###
