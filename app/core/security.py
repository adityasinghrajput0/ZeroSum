from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from app.core.config import settings

ALGO= "HS256"

def hash_password(password:str)->str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password:str, passwordHash:str)->bool:
    return bcrypt.checkpw(password.encode(), passwordHash.encode())

def create_access_token(user_id:str) ->str:
    expire=datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_access_ttl_min)
    return jwt.encode({"sub":user_id, "exp": expire}, settings.jwt_secret, algorithm=ALGO)
# sub = Subject → Who does this token belong to?
# exp = Expiration → When does this token expire?

def decode_access_token(token:str)->str:
    # raises jwt.pyjwt error if expired or invalid.
    return jwt.decode(token, settings.jwt_secret, algorithms=[ALGO])["sub"]

