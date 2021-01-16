"""Initial migration

Revision ID: 03fb00023626
Revises: 
Create Date: 2021-01-16 15:54:48.129958

"""
from alembic import op
import sqlalchemy as sa
from fastapi_utils.guid_type import GUID


# revision identifiers, used by Alembic.
revision = "03fb00023626"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "garments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("garment_type", sa.String(), nullable=False),
        sa.Column("color", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("journaling_key", GUID(), nullable=False),
        sa.Column("image", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("garments", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_garments_id"), ["id"], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("garments", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_garments_id"))

    op.drop_table("garments")
    # ### end Alembic commands ###
