"""empty message

Revision ID: 954cb473a8b9
Revises: 
Create Date: 2022-05-29 17:07:12.222557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '954cb473a8b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=255), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=True),
    sa.Column('author', sa.VARCHAR(length=255), nullable=True),
    sa.Column('date_posted', sa.DATETIME(), nullable=True),
    sa.Column('slug', sa.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
