"""empty message

Revision ID: 507852b6b55b
Revises: None
Create Date: 2014-12-08 21:24:10.640664

"""

# revision identifiers, used by Alembic.
revision = '507852b6b55b'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user__preferences',
    sa.Column('nickname', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=False),
    sa.Column('preferences', sa.String(length=1000), nullable=True),
    sa.Column('last_accessed', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('email')
    )
    op.create_index(op.f('ix_user__preferences_email'), 'user__preferences', ['email'], unique=False)
    op.create_index(op.f('ix_user__preferences_nickname'), 'user__preferences', ['nickname'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('image', sa.String(length=200), nullable=True),
    sa.Column('gender', sa.String(length=10), nullable=True),
    sa.Column('country', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=10), nullable=True),
    sa.Column('timezone', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_image'), 'user', ['image'], unique=False)
    op.create_index(op.f('ix_user_nickname'), 'user', ['nickname'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_nickname'), table_name='user')
    op.drop_index(op.f('ix_user_image'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_user__preferences_nickname'), table_name='user__preferences')
    op.drop_index(op.f('ix_user__preferences_email'), table_name='user__preferences')
    op.drop_table('user__preferences')
    ### end Alembic commands ###
