"""create_weather_ranges_table

Revision ID: aab03ac8d579
Revises: 885e808268f1
Create Date: 2024-12-26 11:43:22.671146

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "aab03ac8d579"
down_revision = "885e808268f1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "weather_ranges",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("max", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("weather_ranges", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_weather_ranges_id"), ["id"], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("weather_ranges", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_weather_ranges_id"))

    op.drop_table("weather_ranges")
    # ### end Alembic commands ###
