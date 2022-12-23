"""empty message

Revision ID: c98cee4eea44
Revises: c2a4c2e276a5
Create Date: 2022-12-23 00:51:53.394205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c98cee4eea44'
down_revision = 'c2a4c2e276a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_planets', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('favorite_people', sa.String(length=200), nullable=True))
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False))
        batch_op.drop_column('favorite_people')
        batch_op.drop_column('favorite_planets')

    # ### end Alembic commands ###