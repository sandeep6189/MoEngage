"""empty message

Revision ID: 3c3547095a18
Revises: 58b8586635de
Create Date: 2015-04-08 03:00:05.193317

"""

# revision identifiers, used by Alembic.
revision = '3c3547095a18'
down_revision = '58b8586635de'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('created_at', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'created_at')
    ### end Alembic commands ###
