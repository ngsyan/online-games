"""update database migration

Revision ID: 9821b784b0ad
Revises: e4c72de28a64
Create Date: 2019-04-05 17:39:46.785094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9821b784b0ad'
down_revision = 'e4c72de28a64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('username', table_name='users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('username', 'users', ['username'], unique=True)
    # ### end Alembic commands ###
