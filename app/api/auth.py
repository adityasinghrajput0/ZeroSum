from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import AccountOut

from app.api.dependencies import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.accounts import Account
from app.models.users import User
from app.schemas.auth import (
    LoginRequest, RegisterRequest, RegisterResponse, TokenResponse,
)

router= APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=RegisterResponse, status_code=201)
async def register(body: RegisterRequest, db: AsyncSession=Depends(get_db)):
    curr_email = body.email.lower()

    existing = await db.scalar(select(User).where(User.email == curr_email))
    if existing:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")

    user = User(email=curr_email, password_hash=hash_password(body.password))
    db.add(user)
    try:
        await db.flush()  # INSERT the user so user.id has a value (not committed yet)
        wallet = Account(user_id=user.id, type="USER", currency="INR")
        db.add(wallet)
        await db.commit()  # user and wallet commit together, or not at all
    except IntegrityError as e:
        await db.rollback()
        # only a duplicate email is a client error; anything else is a real bug
        if "email" in str(e.orig).lower():
            raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
        raise

    await db.refresh(wallet)
    return RegisterResponse(
        user_id=user.id,
        email=user.email,
        account=AccountOut.model_validate(wallet),
    )

@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession=Depends(get_db)):
    user=await db.scalar(select (User). where(User.email==body.email))
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid Email or password")
    return TokenResponse(access_token=create_access_token(str(user.id)))
