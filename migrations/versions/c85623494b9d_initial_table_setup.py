"""initial table setup

Revision ID: c85623494b9d
Revises: 
Create Date: 2022-01-31 22:29:47.439981

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c85623494b9d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('starred_repos_model',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('repo_id', sa.Integer(), nullable=True),
                    sa.Column('created_datetime', sa.DateTime(), nullable=True),
                    sa.Column('name', sa.Unicode(), nullable=True),
                    sa.Column('description', sa.Unicode(), nullable=True),
                    sa.Column('url', sa.Unicode(), nullable=True),
                    sa.Column('last_push_datetime', sa.DateTime(), nullable=True),
                    sa.Column('number_of_stars', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('repo_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('starred_repos_model')
    # ### end Alembic commands ###