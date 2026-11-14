import uuid
from datetime import datetime

from pydantic import BaseModel, Field

class TopUpRequest(BaseModel):
    account_id: uuid.UUID
    amount:int=Field(gt=0, le=100_000_000)
    description:str | None=Field(default=None, max_length=255)

class TransactionOut(BaseModel):
    id: uuid.UUID
    type:str
    status:str
    amount:int
    created_at:datetime