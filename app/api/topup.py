from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.core.errors import LedgerError
from app.models.accounts import Account
from app.models.users import User
from app.schemas.transactions import TopUpRequest, TransactionOut
from app.services.ledger import Movement, get_bank_account, post_transaction

router=APIRouter(prefix="/topups", tags=["topups"])

@router.post("",response_model=TransactionOut, status_code=201)
async def create_top_up(
    body:TopUpRequest,
    db: AsyncSession=Depends(get_db),
    user:User=Depends(get_current_user)
):
    account=await db.get(Account, body.account_id)
    if account is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Account not found")
    if account.user_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,"Not your account")
    
    try:
        bank_id=await get_bank_account(db)
        txn= await post_transaction(
            db,
            type="TOPUP",
            movements=[Movement(bank_id, account.id, body.amount)],
            description=body.description or "simulated top up"
        )
        await db.commit()
    
    except LedgerError as e:
        await db.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))
    
    await db.refresh(txn)
    return TransactionOut(
        id=txn.id,
        type=txn.type,
        status=txn.status,
        amount=body.amount,
        created_at=txn.created_at,
    )