"""empty message

Revision ID: 62a9f007447b
Revises: 050e1d592303
Create Date: 2022-07-08 07:02:35.187193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62a9f007447b'
down_revision = '050e1d592303'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_location_id_fkey', 'users', type_='foreignkey')
    op.create_foreign_key(None, 'users', 'locations', ['location_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.create_foreign_key('users_location_id_fkey', 'users', 'locations', ['location_id'], ['id'])
    # ### end Alembic commands ###
