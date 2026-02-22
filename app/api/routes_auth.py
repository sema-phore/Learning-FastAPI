import re
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, field_validator

from app.core.security import hash_password, verify_password, create_token
from app.db.database import create_user, get_user_by_email, email_exists

router = APIRouter()

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[a-z]{2,}$", re.IGNORECASE)


# ── Schemas ──────────────────────────────────────────────────────────────────

class SignupInput(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def valid_email(cls, v: str) -> str:
        if not EMAIL_RE.match(v.strip()):
            raise ValueError("Enter a valid Gmail / email address")
        return v.strip().lower()

    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class LoginInput(BaseModel):
    email: str
    password: str


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: SignupInput):
    """Register a new user with email + password."""
    if email_exists(user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )
    create_user(user.email, hash_password(user.password))
    return {"message": f"Account created for {user.email}. You can now log in."}


@router.post("/login")
def login(user: LoginInput):
    """Authenticate and receive a JWT token."""
    db_user = get_user_by_email(user.email.strip().lower())

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    token = create_token({"sub": db_user["email"]})
    return {"access_token": token, "token_type": "bearer"}