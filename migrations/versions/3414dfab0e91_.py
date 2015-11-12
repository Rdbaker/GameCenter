"""2nd update that adds an index on the user_id column

Revision ID: 3414dfab0e91
Revises: 52feb4cd3e65
Create Date: 2015-10-09 12:16:31.095629

"""

# revision identifiers, used by Alembic.
revision = '3414dfab0e91'
down_revision = '52feb4cd3e65'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('scores', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.drop_index('ix_scores_user_id', table_name='scores')
    op.create_index(op.f('ix_scores_user_id'), 'scores', ['user_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_scores_user_id'), table_name='scores')
    op.create_index('ix_scores_user_id', 'scores', ['user_id'], unique=True)
    op.alter_column('scores', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    ### end Alembic commands ###
