"""empty message

Revision ID: 6069a467e453
Revises: c72822195249
Create Date: 2022-07-19 07:39:52.056398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6069a467e453'
down_revision = 'c72822195249'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('device_user_id_fkey', 'device', type_='foreignkey')
    op.create_foreign_key(None, 'device', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'device', type_='foreignkey')
    op.create_foreign_key('device_user_id_fkey', 'device', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
