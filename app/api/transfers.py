from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.core.errors import AccountNotFoundError, InsufficientFundsError, LedgerError
from app.models.accounts import Account
from app.models.users import User
from app.schemas.transactions import TransactionOut, TransferRequest
from app.services.transfer import transfer

router=APIRouter(prefix="/transfers", tags=["transfers"])

@router.post("",response_model=TransactionOut,status_code=201)
async def create_transfer(
    body:TransferRequest,
    db:AsyncSession=Depends(get_db),
    user:User=Depends(get_current_user),
):
    source=await db.get(Account, body.from_account_id)
    if source is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Account not found")
    if source.user_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your account")
    
    try:
        txn= await transfer (
            db,
            from_account_id=source.id,
            to_acccount_id=body.to_account_id,
            amount=body.amount,
            description=body.description,
        )
        await db.commit()
    except InsufficientFundsError:
        await db.rollback()
        raise HTTPException(status.HTTP_402_PAYMENT_REQUIRED,"Insufficient Funds")
    except AccountNotFoundError:
        await db.rollback()
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Account not found")
    except LedgerError as e:
        await db.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))

    await db.refresh(txn)
    return TransactionOut(
        id=txn.id, type=txn.type, status=txn.status,
        amount=body.amount, created_at=txn.created_at,
    )