"""create table TransactionModel

Revision ID: 7efa5ba1ebc1
Revises: 310b493fccdd
Create Date: 2024-01-25 22:30:21.797703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7efa5ba1ebc1'
down_revision = '310b493fccdd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quote_id', sa.String(length=100), nullable=False),
    sa.Column('transfer_id', sa.String(length=100), nullable=False),
    sa.Column('target_account_id', sa.String(length=100), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('create_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('complaint_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['complaint_id'], ['complaints.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    # ### end Alembic commands ###
