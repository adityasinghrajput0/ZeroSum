import uuid
from datetime import datetime
from sqlalchemy import Boolean, CheckConstraint, DateTime, Index, func, text,ForeignKey,BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class LedgerEntry(Base):
    __tablename__="LedgerEntry"
    __table_args__=(
        CheckConstraint("amount <> 0", name="ck_LedgerEntry_amount_zero"),
        Index("ix_LedgerEntry_account_created","account_id","created_at"),
        Index("ix_LedgerEntry_transaction_id", "transaction_id")
    )
    
    id:Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    
    transaction_id: Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid=True),
        ForeignKey("transactions.id",ondelete="RESTRICT"),
        nullable=False
    )
    account_id:Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id",ondelete="RESTRICT"),
        nullable=False
    )
    
    amount:Mapped[int]=mapped_column(
        BigInteger,
        nullable=False
    )
    
    created_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )