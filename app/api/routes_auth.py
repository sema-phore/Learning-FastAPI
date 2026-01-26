from fastapi import APIRouter, HTTPException, status 
from pydantic import BaseModel
from app.core.security import create_token

# Defining endpoints indirectly so APIRouter to connect
router = APIRouter()

class AuthInput(BaseModel):
    username: str
    password: str

@router.post('/login')
def login(user: AuthInput):
    if(user.username == 'admin') and (user.password == 'admin'):
        token = create_token({'sub': user.username})
        return {'accessed_token': token}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid Credentials'
    )


"""
Integrate with real DB - SQLite
Re-write the login logic 
"""