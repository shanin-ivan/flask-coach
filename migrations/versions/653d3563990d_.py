"""empty message

Revision ID: 653d3563990d
Revises: 
Create Date: 2022-11-22 12:42:59.178142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '653d3563990d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('goal', sa.String(length=15), nullable=False),
    sa.Column('time', sa.String(length=10), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('tel', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teacher',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('about', sa.Text(), nullable=False),
    sa.Column('rating', sa.Float(), nullable=False),
    sa.Column('picture', sa.String(length=100), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('goals', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('free', sa.JSON(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('booking',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('weekday', sa.String(length=10), nullable=False),
    sa.Column('time', sa.Time(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('client_name', sa.String(length=50), nullable=False),
    sa.Column('client_phone', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('booking')
    op.drop_table('teacher')
    op.drop_table('request')
    # ### end Alembic commands ###
