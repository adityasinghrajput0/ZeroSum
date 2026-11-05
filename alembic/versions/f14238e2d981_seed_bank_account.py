"""seed bank account

Revision ID: f14238e2d981
Revises: 725c91631306
Create Date: 2026-11-05 18:55:31.327109

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

BANK_ACCOUNT_ID = "00000000-0000-0000-0000-000000000001"


# revision identifiers, used by Alembic.
revision: str = 'f14238e2d981'
down_revision: Union[str, Sequence[str], None] = '8cba065b8b33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
            INSERT INTO accounts (id, user_id, type, currency, cached_balance, code)
            VALUES (CAST(:id AS uuid), NULL, 'SYSTEM', 'INR', 0, 'BANK')
            ON CONFLICT (id) DO NOTHING
            """
        ).bindparams(id=BANK_ACCOUNT_ID)
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
            DELETE FROM accounts
            WHERE id = CAST(:id AS uuid)
              AND NOT EXISTS (
                  SELECT 1 FROM ledger_entries WHERE account_id = CAST(:id AS uuid)
              )
            """
        ).bindparams(id=BANK_ACCOUNT_ID)
    )