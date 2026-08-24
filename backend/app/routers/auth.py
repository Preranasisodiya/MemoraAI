from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app.database.database import get_db
from app.models.user import User
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    AuthResponse,
    TokenResponse,
)
from app.services.auth_service import create_access_token
from app.services.auth_dependency import get_current_user


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

password_hash = PasswordHash.recommended()


# ============================================================
# REGISTER
# ============================================================

@router.post(
    "/register",
    response_model=AuthResponse
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    # Check whether the email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email is already registered"
        )

    # Hash the password before storing it
    hashed_password = password_hash.hash(data.password)

    # Create the user
    new_user = User(
        name=data.name,
        email=data.email,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }


# ============================================================
# LOGIN
# ============================================================

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    # Find user by email
    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    # Don't reveal whether the email exists
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Verify the entered password against the stored hash
    if not password_hash.verify(
        data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create JWT access token
    access_token = create_access_token(
        user_id=user.id,
        email=user.email
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ============================================================
# CURRENT USER
# ============================================================

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "user_id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }