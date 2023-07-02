from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import env
from app.core.constants import ALGORITHM
from app.core.dependencies import get_current_user, get_session
from app.core.models import User
from app.core.schemas import Token, UserCreate

user_router = APIRouter(tags=["users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, env.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = (
        await db.execute(select(User).where(User.username == username))
    ).scalar_one_or_none()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@user_router.post("/register/")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return {"message": "You are successfully registered"}


@user_router.post("/login/", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=env.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/refresh-token/")
async def refresh_token(
    current_user: User = Depends(get_current_user),
):
    new_token = create_access_token(
        data={"sub": current_user.username},
        expires_delta=timedelta(minutes=env.access_token_expire_minutes),
    )
    return {"access_token": new_token, "token_type": "bearer"}
