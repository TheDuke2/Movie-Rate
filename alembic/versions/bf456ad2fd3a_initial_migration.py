"""initial migration

Revision ID: bf456ad2fd3a
Revises: 
Create Date: 2024-08-01 17:41:27.037692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf456ad2fd3a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('movies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('genre', sa.String(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_movies_id'), 'movies', ['id'], unique=False)
    op.create_table('comments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('contents', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)
    op.create_table('ratings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ratings_id'), 'ratings', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ratings_id'), table_name='ratings')
    op.drop_table('ratings')
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')
    op.drop_index(op.f('ix_movies_id'), table_name='movies')
    op.drop_table('movies')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
