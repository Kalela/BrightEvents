"""empty message

Revision ID: 37bc8244afa3
Revises: 482606376e75
Create Date: 2018-02-14 18:13:29.972000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '37bc8244afa3'
down_revision = '482606376e75'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'date_modified')
    op.drop_column('user', 'date_modified')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('date_modified', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('event', sa.Column('date_modified', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
