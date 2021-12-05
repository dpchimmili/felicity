"""renmed mtm keys

Revision ID: 23e960248fb1
Revises: b1097c414193
Create Date: 2021-12-05 13:48:14.892281

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '23e960248fb1'
down_revision = 'b1097c414193'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message_thread_delete', sa.Column('message_thread_uid', sa.Integer(), nullable=False))
    op.drop_constraint('message_thread_delete_thread_uid_fkey', 'message_thread_delete', type_='foreignkey')
    op.create_foreign_key(None, 'message_thread_delete', 'messagethread', ['message_thread_uid'], ['uid'])
    op.drop_column('message_thread_delete', 'thread_uid')
    op.add_column('message_thread_recipient', sa.Column('message_thread_uid', sa.Integer(), nullable=False))
    op.drop_constraint('message_thread_recipient_thread_uid_fkey', 'message_thread_recipient', type_='foreignkey')
    op.create_foreign_key(None, 'message_thread_recipient', 'messagethread', ['message_thread_uid'], ['uid'])
    op.drop_column('message_thread_recipient', 'thread_uid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message_thread_recipient', sa.Column('thread_uid', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'message_thread_recipient', type_='foreignkey')
    op.create_foreign_key('message_thread_recipient_thread_uid_fkey', 'message_thread_recipient', 'messagethread', ['thread_uid'], ['uid'])
    op.drop_column('message_thread_recipient', 'message_thread_uid')
    op.add_column('message_thread_delete', sa.Column('thread_uid', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'message_thread_delete', type_='foreignkey')
    op.create_foreign_key('message_thread_delete_thread_uid_fkey', 'message_thread_delete', 'messagethread', ['thread_uid'], ['uid'])
    op.drop_column('message_thread_delete', 'message_thread_uid')
    # ### end Alembic commands ###