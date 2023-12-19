"""empty message

Revision ID: 3adb83729a4e
Revises: 0943cbb9e2cd
Create Date: 2023-12-14 01:18:30.382314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3adb83729a4e'
down_revision = '0943cbb9e2cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('user_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False,
               autoincrement=True)

    # ### end Alembic commands ###