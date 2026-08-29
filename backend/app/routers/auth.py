from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt, JWTError

from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
)

# Router
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Swagger OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Temporary storage (Day 3 me PostgreSQL se replace karenge)
users = {}


# --------- Models ---------
class UserSignup(BaseModel):
    email: str
    password: str


# --------- Signup ---------
@router.post("/signup")
def signup(user: UserSignup):
    if user.email in users:
        return {"message": "User already exists"}

    users[user.email] = hash_password(user.password)
    return {"message": "Signup successful"}


# --------- Login ---------
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password

    if email not in users:
        return {"message": "User not found"}

    if not verify_password(password, users[email]):
        return {"message": "Invalid password"}

    access_token = create_access_token({"sub": email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# --------- Protected Route ---------
@router.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            return {"message": "Invalid token"}

        return {"email": email}

    except JWTError:
        return {"message": "Invalid token"}