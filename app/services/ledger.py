import uuid
from collections import defaultdict
from dataclasses import dataclass

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AccountNotFoundError, InvalidEntryError
from app.models.accounts import Account
from app.models.ledgerentry import LedgerEntry
from app.models.transactions import Transaction

@dataclass(frozen=True)
class Movement:
    from_account_id:uuid.UUID
    to_account_id:uuid.UUID
    amount:int
    
def validate_movements(movements:list[Movement])->None:
    if not movements:
        raise InvalidEntryError("A transaction needs at least one movement.")
    for m in movements:
        if isinstance(m.amount, bool) or not isinstance(m.amount, int):
            raise InvalidEntryError("Amount must be integer")
        if m.amount <= 0:
            raise InvalidEntryError("Amount must be positive")
        if (m.from_account_id==m.to_account_id):
            raise InvalidEntryError("Cannot move money to same account")

def build_entries(
    movements:list[Movement]
)->tuple[list[tuple[uuid.UUID,int]],dict[uuid.UUID,int]]:
    entries:list[tuple[uuid.UUID,int]]=[]
    net:dict[uuid.UUID,int]=defaultdict(int)
    for m in movements:
        entries.append((m.from_account_id,-m.amount))
        entries.append((m.to_account_id, m.amount))
        net[m.from_account_id]-=m.amount
        net[m.to_account_id]+=m.amount
    return entries,net

async def post_transaction(
    db:AsyncSession,
    *,
    type:str,
    movements:list[Movement],
    description: str | None=None,
    reverse_transaction_id: uuid.UUID | None =None,
)->Transaction:
    validate_movements(movements)
     # Each movement becomes two entries: sender -amount, receiver +amount
    entries,net=build_entries(movements)
    assert sum(a for _,a in entries)==0
    for account_id in sorted(net):
        result=await db.execute(
            update(Account).where (account_id==Account.id)
            .values(cached_balance=Account.cached_balance+net[account_id])
        )
        if (result.rowcount != 1):
            raise AccountNotFoundError(f"Account {account_id} not found")
    
    txn=Transaction(
        type=type,
        status="COMPLETED",
        description=description,
        reverse_transaction_id=reverse_transaction_id
    )
    db.add(txn)
    await db.flush()
    
    db.add_all(
        LedgerEntry(transaction_id=txn.id, account_id=acc_id, amount=amount)
        for acc_id, amount in entries
    )
    await db.flush()
    return txn

async def get_bank_account(db:AsyncSession)->uuid.UUID:
    bank_id=await db.scalar(select(Account.id).where(Account.code=="BANK"))
    if bank_id is None:
        raise AccountNotFoundError("Bank account not seeded")
    return bank_id


