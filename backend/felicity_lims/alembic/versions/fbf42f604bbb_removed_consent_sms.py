"""removed consent sms

Revision ID: fbf42f604bbb
Revises: c0a120db23c1
Create Date: 2021-02-20 12:56:19.146435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbf42f604bbb'
down_revision = 'c0a120db23c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('district', 'consent_email')
    op.drop_column('district', 'consent_sms')
    op.drop_column('province', 'consent_email')
    op.drop_column('province', 'consent_sms')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('province', sa.Column('consent_sms', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('province', sa.Column('consent_email', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('district', sa.Column('consent_sms', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('district', sa.Column('consent_email', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
