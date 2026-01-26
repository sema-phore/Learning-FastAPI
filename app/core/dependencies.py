# Dependency injection logic for API key and JWT token validation
from fastapi import Header, HTTPException, status
from app.core.config import settings
from app.core.security import verify_token

# Verify api key
def verify_api_key(api_key: str = Header(...)):
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid API_KEY!'
        )
    
# Verify and get the user
def get_current_user(token: str = Header(...)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= 'Invalid JWT Token'
        )
    return payload

# detail="Authentication failed"
# Instead of revealing whether API key or JWT failed.