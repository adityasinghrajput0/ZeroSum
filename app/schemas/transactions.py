import uuid
from datetime import datetime

from pydantic import BaseModel, Field, model_validator

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
    
class TransferRequest(BaseModel):
    from_account_id:uuid.UUID
    to_account_id: uuid.UUID
    amount:int=Field(gt=0, le=100_000_000)
    description: str| None=Field(default=None, max_length=255)

    @model_validator(mode="after")
    def account_must_differ(self):
        if self.from_account_id==self.to_account_id:
            raise ValueError("Cannot transfer to same account")
        return self