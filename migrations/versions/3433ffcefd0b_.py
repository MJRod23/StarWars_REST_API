"""empty message

Revision ID: 3433ffcefd0b
Revises: c98cee4eea44
Create Date: 2022-12-23 01:57:58.283004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3433ffcefd0b'
down_revision = 'c98cee4eea44'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('user_email_key', type_='unique')
        batch_op.drop_column('password')
        batch_op.drop_column('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=80), autoincrement=False, nullable=False))
        batch_op.create_unique_constraint('user_email_key', ['email'])

    # ### end Alembic commands ###
