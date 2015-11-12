"""Initial upgrade with Scores

Revision ID: 52feb4cd3e65
Revises: None
Create Date: 2015-09-28 18:06:28.036193

"""

# revision identifiers, used by Alembic.
revision = '52feb4cd3e65'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('scores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scores_tag'), 'scores', ['tag'], unique=False)
    op.create_index(op.f('ix_scores_user_id'), 'scores', ['user_id'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_scores_user_id'), table_name='scores')
    op.drop_index(op.f('ix_scores_tag'), table_name='scores')
    op.drop_table('scores')
