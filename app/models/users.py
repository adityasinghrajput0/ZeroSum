import uuid
from datetime import datetime
from sqlalchemy import Boolean, CheckConstraint, DateTime, String, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base;

class User(Base):
    __tablename__="users"
    __table_args__=(CheckConstraint("email=lower(email)",name="email_lower"))
    
    id: Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid=true),
        primary_key=true,
        server_default=text("get_random_uuid()"),
    )
    
    email: Mapped[str]=mapped_column(unique=True, String(255), nullable=False)
    password_hash:Mapped[str] =mapped_column(String(255), nullable=False)
    isAdmin:Mapped[bool]=mapped_column(Boolean, nullable=False, server_default=False)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
