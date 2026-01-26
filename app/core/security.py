from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
from app.core.config import settings
from fastapi import HTTPException, status

def create_token(data: dict, expire_minutes=30):
    to_encode = data.copy() # data to encode
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes) # Create expire time
    to_encode.update({'exp': expire}) # exp - standart claim name for jwt
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    ) # data, key and encoding algo

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms = [settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or Expired Token!'
        ) 