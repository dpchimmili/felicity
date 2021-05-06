"""added markdown tables

Revision ID: 4dfcd34ba782
Revises: 74e388f5fcf6
Create Date: 2021-05-06 17:12:19.174055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4dfcd34ba782'
down_revision = '74e388f5fcf6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('documentcategory',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_documentcategory_uid'), 'documentcategory', ['uid'], unique=False)
    op.create_table('documenttag',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_documenttag_uid'), 'documenttag', ['uid'], unique=False)
    op.create_table('document',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('subtitle', sa.String(), nullable=True),
    sa.Column('document_id', sa.String(), nullable=True),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('version', sa.String(), nullable=True),
    sa.Column('department_uid', sa.Integer(), nullable=True),
    sa.Column('date_archived', sa.DateTime(), nullable=True),
    sa.Column('created_by_uid', sa.Integer(), nullable=True),
    sa.Column('modified_by_uid', sa.Integer(), nullable=True),
    sa.Column('archived_by_uid', sa.Integer(), nullable=True),
    sa.Column('date_recalled', sa.DateTime(), nullable=True),
    sa.Column('recalled_by_uid', sa.Integer(), nullable=True),
    sa.Column('date_effected', sa.DateTime(), nullable=True),
    sa.Column('effected_by_uid', sa.Integer(), nullable=True),
    sa.Column('date_approved', sa.DateTime(), nullable=True),
    sa.Column('approved_by_uid', sa.Integer(), nullable=True),
    sa.Column('last_accessed', sa.DateTime(), nullable=True),
    sa.Column('last_accessed_by_uid', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['approved_by_uid'], ['user.uid'], ),
    sa.ForeignKeyConstraint(['archived_by_uid'], ['user.uid'], ),
    sa.ForeignKeyConstraint(['created_by_uid'], ['user.uid'], ),
    sa.ForeignKeyConstraint(['department_uid'], ['department.uid'], ),
    sa.ForeignKeyConstraint(['effected_by_uid'], ['user.uid'], ),
    sa.ForeignKeyConstraint(['last_accessed_by_uid'], ['user.uid'], ),
    sa.ForeignKeyConstraint(['modified_by_uid'], ['user.uid'], ),
    sa.ForeignKeyConstraint(['recalled_by_uid'], ['user.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_document_uid'), 'document', ['uid'], unique=False)
    op.create_table('docauthors',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('document_uid', sa.Integer(), nullable=False),
    sa.Column('user_uid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['document_uid'], ['document.uid'], ),
    sa.ForeignKeyConstraint(['user_uid'], ['user.uid'], ),
    sa.PrimaryKeyConstraint('uid', 'document_uid', 'user_uid')
    )
    op.create_index(op.f('ix_docauthors_uid'), 'docauthors', ['uid'], unique=False)
    op.create_table('docreads',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('document_uid', sa.Integer(), nullable=False),
    sa.Column('user_uid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['document_uid'], ['document.uid'], ),
    sa.ForeignKeyConstraint(['user_uid'], ['user.uid'], ),
    sa.PrimaryKeyConstraint('uid', 'document_uid', 'user_uid')
    )
    op.create_index(op.f('ix_docreads_uid'), 'docreads', ['uid'], unique=False)
    op.create_table('doctags',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('document_uid', sa.Integer(), nullable=False),
    sa.Column('tag_uid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['document_uid'], ['document.uid'], ),
    sa.ForeignKeyConstraint(['tag_uid'], ['documenttag.uid'], ),
    sa.PrimaryKeyConstraint('uid', 'document_uid', 'tag_uid')
    )
    op.create_index(op.f('ix_doctags_uid'), 'doctags', ['uid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_doctags_uid'), table_name='doctags')
    op.drop_table('doctags')
    op.drop_index(op.f('ix_docreads_uid'), table_name='docreads')
    op.drop_table('docreads')
    op.drop_index(op.f('ix_docauthors_uid'), table_name='docauthors')
    op.drop_table('docauthors')
    op.drop_index(op.f('ix_document_uid'), table_name='document')
    op.drop_table('document')
    op.drop_index(op.f('ix_documenttag_uid'), table_name='documenttag')
    op.drop_table('documenttag')
    op.drop_index(op.f('ix_documentcategory_uid'), table_name='documentcategory')
    op.drop_table('documentcategory')
    # ### end Alembic commands ###
