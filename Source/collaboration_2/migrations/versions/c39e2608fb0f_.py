"""empty message

Revision ID: c39e2608fb0f
Revises: 
Create Date: 2019-01-30 14:06:58.974251

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c39e2608fb0f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('spec_projectmember',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=32), nullable=True),
    sa.Column('project_name', sa.String(length=2048), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='spec'
    )
    op.drop_table('ds_doc_old', schema='ds')
    op.drop_table('ds_section_temp', schema='ds')
    op.drop_table('ds_section_old', schema='ds')
    op.drop_constraint('consider_doc_id_fkey', 'consider', type_='foreignkey')
    op.create_foreign_key(None, 'consider', 'docs', ['doc_id'], ['doc_id'], source_schema='public', referent_schema='public')
    op.drop_constraint('doc_tags_doc_id_fkey', 'doc_tags', type_='foreignkey')
    op.drop_constraint('doc_tags_tag_id_fkey', 'doc_tags', type_='foreignkey')
    op.create_foreign_key(None, 'doc_tags', 'docs', ['doc_id'], ['doc_id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'doc_tags', 'doc_tag_category', ['tag_id'], ['tag_id'], source_schema='public', referent_schema='public')
    op.drop_constraint('failure_mode_doc_id_fkey', 'failure_mode', type_='foreignkey')
    op.create_foreign_key(None, 'failure_mode', 'docs', ['doc_id'], ['doc_id'], source_schema='public', referent_schema='public')
    op.drop_constraint('journal_briefs_journalized_id_fkey', 'journal_briefs', type_='foreignkey')
    op.create_foreign_key(None, 'journal_briefs', 'journals', ['journalized_id'], ['journalized_id'], source_schema='public', referent_schema='public')
    op.drop_constraint('journal_details_j_brief_id_fkey', 'journal_details', type_='foreignkey')
    op.create_foreign_key(None, 'journal_details', 'journal_briefs', ['j_brief_id'], ['j_brief_id'], source_schema='public', referent_schema='public')
    op.drop_constraint('role_permissions_perm_id_fkey', 'role_permissions', type_='foreignkey')
    op.drop_constraint('role_permissions_role_id_fkey', 'role_permissions', type_='foreignkey')
    op.create_foreign_key(None, 'role_permissions', 'permission', ['perm_id'], ['perm_id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'role_permissions', 'role', ['role_id'], ['role_id'], source_schema='public', referent_schema='public')
    op.drop_constraint('user_roles_user_id_fkey', 'user_roles', type_='foreignkey')
    op.drop_constraint('user_roles_role_id_fkey', 'user_roles', type_='foreignkey')
    op.create_foreign_key(None, 'user_roles', 'users', ['user_id'], ['user_id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'user_roles', 'role', ['role_id'], ['role_id'], source_schema='public', referent_schema='public')
    op.add_column('users', sa.Column('work_id', sa.String(length=100), nullable=True))
    op.drop_constraint('ds_model_tag_rel_tag_id_fkey', 'ds_model_tag_rel', schema='ds', type_='foreignkey')
    op.create_foreign_key(None, 'ds_model_tag_rel', 'doc_tag_category', ['tag_id'], ['tag_id'], source_schema='ds', referent_schema='public')
    op.drop_constraint('ds_section_tag_rel_tag_id_fkey', 'ds_section_tag_rel', schema='ds', type_='foreignkey')
    op.create_foreign_key(None, 'ds_section_tag_rel', 'doc_tag_category', ['tag_id'], ['tag_id'], source_schema='ds', referent_schema='public')
    op.drop_constraint('project_tags_tag_id_fkey', 'project_tags', schema='ds', type_='foreignkey')
    op.create_foreign_key(None, 'project_tags', 'doc_tag_category', ['tag_id'], ['tag_id'], source_schema='ds', referent_schema='public')
    op.add_column('spec_headerfile', sa.Column('status', sa.String(length=10), nullable=True), schema='spec')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('spec_headerfile', 'status', schema='spec')
    op.drop_constraint(None, 'project_tags', schema='ds', type_='foreignkey')
    op.create_foreign_key('project_tags_tag_id_fkey', 'project_tags', 'doc_tag_category', ['tag_id'], ['tag_id'], source_schema='ds')
    op.drop_constraint(None, 'ds_section_tag_rel', schema='ds', type_='foreignkey')
    op.create_foreign_key('ds_section_tag_rel_tag_id_fkey', 'ds_section_tag_rel', 'doc_tag_category', ['tag_id'], ['tag_id'], source_schema='ds')
    op.drop_constraint(None, 'ds_model_tag_rel', schema='ds', type_='foreignkey')
    op.create_foreign_key('ds_model_tag_rel_tag_id_fkey', 'ds_model_tag_rel', 'doc_tag_category', ['tag_id'], ['tag_id'], source_schema='ds')
    op.drop_column('users', 'work_id')
    op.drop_constraint(None, 'user_roles', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'user_roles', schema='public', type_='foreignkey')
    op.create_foreign_key('user_roles_role_id_fkey', 'user_roles', 'role', ['role_id'], ['role_id'])
    op.create_foreign_key('user_roles_user_id_fkey', 'user_roles', 'users', ['user_id'], ['user_id'])
    op.drop_constraint(None, 'role_permissions', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'role_permissions', schema='public', type_='foreignkey')
    op.create_foreign_key('role_permissions_role_id_fkey', 'role_permissions', 'role', ['role_id'], ['role_id'])
    op.create_foreign_key('role_permissions_perm_id_fkey', 'role_permissions', 'permission', ['perm_id'], ['perm_id'])
    op.drop_constraint(None, 'journal_details', schema='public', type_='foreignkey')
    op.create_foreign_key('journal_details_j_brief_id_fkey', 'journal_details', 'journal_briefs', ['j_brief_id'], ['j_brief_id'])
    op.drop_constraint(None, 'journal_briefs', schema='public', type_='foreignkey')
    op.create_foreign_key('journal_briefs_journalized_id_fkey', 'journal_briefs', 'journals', ['journalized_id'], ['journalized_id'])
    op.drop_constraint(None, 'failure_mode', schema='public', type_='foreignkey')
    op.create_foreign_key('failure_mode_doc_id_fkey', 'failure_mode', 'docs', ['doc_id'], ['doc_id'])
    op.drop_constraint(None, 'doc_tags', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'doc_tags', schema='public', type_='foreignkey')
    op.create_foreign_key('doc_tags_tag_id_fkey', 'doc_tags', 'doc_tag_category', ['tag_id'], ['tag_id'])
    op.create_foreign_key('doc_tags_doc_id_fkey', 'doc_tags', 'docs', ['doc_id'], ['doc_id'])
    op.drop_constraint(None, 'consider', schema='public', type_='foreignkey')
    op.create_foreign_key('consider_doc_id_fkey', 'consider', 'docs', ['doc_id'], ['doc_id'])
    op.create_table('ds_section_old',
    sa.Column('sec_id', sa.INTEGER(), server_default=sa.text("nextval('ds.ds_section_old_sec_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('sec_type', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ver', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('doc_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('required', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('parent_sec_id', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=False),
    sa.Column('micro_ver', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('sec_id', name='ds_section_old_pkey'),
    schema='ds'
    )
    op.create_table('ds_section_temp',
    sa.Column('sec_id', sa.INTEGER(), server_default=sa.text("nextval('ds.ds_section_temp_sec_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('sec_type', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ver', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('doc_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('required', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('parent_sec_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('micro_ver', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('complement', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('explain', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('sec_title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('old_doc_id', sa.INTEGER(), autoincrement=False, nullable=True),
    schema='ds'
    )
    op.create_table('ds_doc_old',
    sa.Column('doc_id', sa.INTEGER(), server_default=sa.text("nextval('ds.ds_doc_old_doc_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('doc_type', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('title', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('ver', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('model_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('create_time', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('update_time', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('creator', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('editor', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('summary', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('proj_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('major_ver', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('minor_ver', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('micro_ver', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('status', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('doc_id', name='ds_doc_old_pkey'),
    schema='ds'
    )
    op.drop_table('spec_projectmember', schema='spec')
    # ### end Alembic commands ###
