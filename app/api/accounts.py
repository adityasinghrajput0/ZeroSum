import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.models.accounts import Account
from app.models.users import User
from app.schemas.account import BalanceOut
from app.schemas.auth import AccountOut

router=APIRouter(prefix="/accounts", tags=["accounts"])

async def get_owned_account(
    account_id:uuid.UUID,
    db:AsyncSession=Depends(get_db),
    user:User=Depends(get_current_user),
)-> Account:
    # Load an account and make sure the logged-in user owns it.
    account=await db.get(Account, account_id)
    if account is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,"Account not found")
    if account.user_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,"Not your account")
    return account

@router.get("",response_model=list[AccountOut])
async def list_accounts(
    db:AsyncSession=Depends(get_db),
    user:User=Depends(get_current_user)
):
    result=await db.scalars(select (Account).where(Account.user_id==user.id).order_by(Account.created_at))
    return result.all()
    
@router.post("",response_model=AccountOut, status_code=201)
async def create_account(
    db:AsyncSession=Depends(get_db),
    user: User=Depends(get_current_user)
):
    wallet=Account(user_id=user.id, type="USER", currency="INR")
    db.add(wallet)
    await db.commit()
    await db.refresh(wallet)
    return wallet

@router.get("/{account_id}/balance", response_model=BalanceOut)
async def get_balance(account:Account=Depends(get_owned_account)):
    return BalanceOut(
        account_id=account.id,
        currency=account.currency,
        balance=account.cached_balance,
    )