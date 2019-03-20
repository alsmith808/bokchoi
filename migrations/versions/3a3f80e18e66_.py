"""empty message

Revision ID: 3a3f80e18e66
Revises: 0561f2c663d4
Create Date: 2019-03-18 22:53:38.317648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a3f80e18e66'
down_revision = '0561f2c663d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'howto',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=800),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'howto',
               existing_type=sa.String(length=800),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
    # ### end Alembic commands ###