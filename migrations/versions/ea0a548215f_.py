"""6th update that adds a 'frozen' column to games

Revision ID: ea0a548215f
Revises: 2b7d1717f5cb
Create Date: 2015-11-18 16:21:46.576059

"""

# revision identifiers, used by Alembic.
revision = 'ea0a548215f'
down_revision = '2b7d1717f5cb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('frozen', sa.Boolean(), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('games', 'frozen')
    ### end Alembic commands ###
