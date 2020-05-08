"""empty message

Revision ID: f68a2e6e7150
Revises: 933714c025da
Create Date: 2020-05-05 15:19:04.313786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f68a2e6e7150'
down_revision = '933714c025da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('education', sa.Column('description', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('education', 'description')
    # ### end Alembic commands ###