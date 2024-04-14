"""init

Revision ID: 690976affbfc
Revises: 6f1b04dd74c6
Create Date: 2024-04-14 07:30:35.074118

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "690976affbfc"
down_revision = "6f1b04dd74c6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "payment",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("category_id", sa.BigInteger(), nullable=False),
        sa.Column("card_type_id", sa.BigInteger(), nullable=False),
        sa.Column("cashback_percent", sa.Float(), nullable=False),
        sa.Column(
            "create_time",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "update_time",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["card_type_id"], ["card_type.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["category_id"], ["category.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("payment")
    # ### end Alembic commands ###