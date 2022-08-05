"""empty message

Revision ID: 86161ba9224e
Revises: 6069a467e453
Create Date: 2022-07-19 12:34:31.574086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86161ba9224e'
down_revision = '6069a467e453'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('moderators', sa.Column('key', sa.String(), nullable=True))
    op.add_column('moderators', sa.Column('salt', sa.String(), nullable=True))
    op.drop_column('moderators', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('moderators', sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('moderators', 'salt')
    op.drop_column('moderators', 'key')
    # ### end Alembic commands ###
