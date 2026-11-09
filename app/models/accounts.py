import uuid
from datetime import datetime
from sqlalchemy import Boolean, CheckConstraint, DateTime, String, func, text, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class Account(Base):
    __tablename__="accounts"
    __table_args__=(
        CheckConstraint(
            "type IN ('USER','SYSTEM')",
            name="ck_accounts_type"
        ),
        CheckConstraint(
            "(type='USER' AND user_id IS NOT NULL) OR"
            "(type='SYSTEM' AND user_id IS NULL)",
            name="ck_accounts_owner_match_type"
        ),
        CheckConstraint(
            "type='SYSTEM' OR cached_balance>=0",
            name="ck_accounts_balance_nonnegative"
        ),
        CheckConstraint(
            "(type = 'USER' AND code IS NULL) OR (type = 'SYSTEM' AND code IS NOT NULL)",
            name="code_match_type",
        )
    )
    
    id:Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id:Mapped[uuid.UUID | None]=mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id",ondelete="RESTRICT"),
        nullable=True,
        index=True
    )
    type:Mapped[str]=mapped_column(
        String(6),
        nullable=False,
    )
    code:Mapped[str | None]=mapped_column(
        String(20),
        unique=True,
        nullable=True,
    )
    currency:Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="INR"
    )
    cached_balance:Mapped[int]=mapped_column(
        BigInteger,
        nullable=False,
        default=0,
    )
    created_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )