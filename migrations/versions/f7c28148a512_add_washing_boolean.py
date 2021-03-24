"""Add washing boolean

Revision ID: f7c28148a512
Revises: 938a751b70ed
Create Date: 2021-03-17 17:03:10.822037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f7c28148a512"
down_revision = "938a751b70ed"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("garments", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("washing", sa.Boolean(), nullable=False, server_default="FALSE")
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("garments", schema=None) as batch_op:
        batch_op.drop_column("washing")

    # ### end Alembic commands ###