"""add owner to todo

Revision ID: 4b55be055bf2
Revises: ad1aa6ea83ee
Create Date: 2024-08-24 22:25:05.559889

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4b55be055bf2"
down_revision: Union[str, None] = "ad1aa6ea83ee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table("todo", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("owner", sa.String(), nullable=False, server_default="Arjun"),
        )
        batch_op.create_foreign_key(
            "fk_todo_owner_user", "user", ["owner"], ["username"]
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("todo", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_column("owner")
    # ### end Alembic commands ###
