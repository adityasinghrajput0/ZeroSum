import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AccountNotFoundError, InsufficientFundsError, InvalidEntryError
from app.models.accounts import Account
from app.models.transactions import Transaction
from app.services.ledger import Movement, post_transaction

async def transfer(
    db:AsyncSession,
    *,
    from_account_id:uuid.UUID,
    to_acccount_id:uuid.UUID,
    amount:int,
    description:str | None=None
)->Transaction:
    source=await db.get(Account, from_account_id)
    dest=await db.get(Account, to_acccount_id)
    if source is None or dest is None:
        raise AccountNotFoundError("Account not found")
    if dest.type != "USER":
        raise InvalidEntryError("Destination must be a user wallet")
    if dest.currency != source.currency:
        raise InvalidEntryError("Currency Mismatch!")
    if source.cached_balance<amount:
        raise InsufficientFundsError("Insufficient Balance")
    return await post_transaction(
        db,
        type="TRANSFER",
        movements=[Movement(source.id, dest.id, amount)],
        description=description,
)