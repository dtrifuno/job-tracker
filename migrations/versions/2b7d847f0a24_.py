"""empty message

Revision ID: 2b7d847f0a24
Revises: a5cee1880545
Create Date: 2020-05-13 02:25:04.430967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b7d847f0a24'
down_revision = 'a5cee1880545'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('education_job_relationship_table',
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('education_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['education_id'], ['education.id'], ),
    sa.ForeignKeyConstraint(['job_id'], ['job.id'], ),
    sa.PrimaryKeyConstraint('job_id', 'education_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('education_job_relationship_table')
    # ### end Alembic commands ###
