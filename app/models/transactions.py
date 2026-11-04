import uuid
from datetime import datetime
from sqlalchemy import Boolean, CheckConstraint, DateTime, String, func, text,ForeignKey,BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class transactions(Base):
    __tablename__="transactions"
    __table_args__=(
        CheckConstraint(
            "type IN ('TOPUP','TRANSFER','REVERSAL')",
            name="ck_transactions_type_check"
        ),
        CheckConstraint(
            "status IN ('PENDING', 'COMPLETED', 'FAILED' , 'REVERSED')",
            name="ck_transactions_status_check"
        ),
        CheckConstraint(
            "amount>=0",
            name="ck_transactions_amount_check"
        ),
    )
    
    id:Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    type:Mapped[str]=mapped_column(
        String(10),
        nullable=False
    )
    status:Mapped[str]=mapped_column(
        String(10),
        nullable=False,
        default="PENDING"
    )
    amount:Mapped[int]=mapped_column(
        BigInteger,
        nullable=False
    )
    currency:Mapped[str]=mapped_column(
        String(3),
        default="INR"
    )
    reverse_transaction_id:Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid=True),
        ForeignKey("transactions.id", ondelete="RESTRICT"),
        nullable=True,
        unique=True
    )
    description:Mapped[str]=mapped_column(
        String(200),
        nullable=True
    )
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())