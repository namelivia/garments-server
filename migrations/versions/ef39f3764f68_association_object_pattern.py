"""association_object_pattern

Revision ID: ef39f3764f68
Revises: 333483446510
Create Date: 2024-06-10 09:51:24.337473

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ef39f3764f68"
down_revision = "333483446510"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("activity_garment_type", schema=None) as batch_op:
        batch_op.alter_column("activity_id", existing_type=sa.INTEGER(), nullable=False)
        batch_op.alter_column(
            "garment_type_id", existing_type=sa.INTEGER(), nullable=False
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("activity_garment_type", schema=None) as batch_op:
        batch_op.alter_column(
            "garment_type_id", existing_type=sa.INTEGER(), nullable=True
        )
        batch_op.alter_column("activity_id", existing_type=sa.INTEGER(), nullable=True)

    # ### end Alembic commands ###
