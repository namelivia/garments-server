"""rename_activity_garment_type_table

Revision ID: 885e808268f1
Revises: bbda42584fec
Create Date: 2024-12-14 19:06:12.619105

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "885e808268f1"
down_revision = "bbda42584fec"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Rename the table from activity_garment_type to rules
    op.rename_table("activity_garment_type", "rules")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.rename_table("rules", "activity_garment_type")
    # ### end Alembic commands ###
