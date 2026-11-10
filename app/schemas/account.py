import uuid
from pydantic import BaseModel

class BalanceOut(BaseModel):
    account_id: uuid.UUID
    currency: str
    balance: int