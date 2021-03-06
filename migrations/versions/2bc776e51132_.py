"""empty message

Revision ID: 2bc776e51132
Revises: f2ee6bf69d54
Create Date: 2022-01-12 00:10:12.446475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bc776e51132'
down_revision = 'f2ee6bf69d54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('image_set', 'vehicle_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('image_set', 'vehicle_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
