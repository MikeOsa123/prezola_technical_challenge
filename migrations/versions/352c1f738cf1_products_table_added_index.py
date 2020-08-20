"""products table added index

Revision ID: 352c1f738cf1
Revises: 9f1415d99f9a
Create Date: 2020-08-20 03:02:04.000172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '352c1f738cf1'
down_revision = '9f1415d99f9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_product_brand'), 'product', ['brand'], unique=False)
    op.create_index(op.f('ix_product_name'), 'product', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_product_name'), table_name='product')
    op.drop_index(op.f('ix_product_brand'), table_name='product')
    # ### end Alembic commands ###