import uuid
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str= Field(min_length=8, max_length=72)
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
# response access_token on successful login
class TokenResponse(BaseModel): 
    access_token:str
    token_type: str="bearer"
    
# return account data as response 
class AccountOut(BaseModel):
    # read values directly from object's attributes
    model_config=ConfigDict(form_attributes=True)
    id:uuid.UUID
    type:str
    currency:str
    cached_balance:str
  
# response generated after successful user registration   
class RegisterResponse(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    account: AccountOut
