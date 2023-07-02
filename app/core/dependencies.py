import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import env
from app.core.constants import ALGORITHM
from app.core.models import User
from app.core.schemas import Token
from app.db import async_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)
) -> User | None:
    try:
        payload = jwt.decode(token, env.secret_key, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        user = (
            await db.execute(select(User).where(User.username == username))
        ).scalar_one_or_none()
    except jwt.exceptions.PyJWTError:
        raise credentials_exception
    return user


def get_username_from_token(token: Token):
    try:
        payload = jwt.decode(token, env.secret_key, algorithms=ALGORITHM)
        if username := payload.get("sub"):
            return username
        raise credentials_exception
    except jwt.exceptions.PyJWTError:
        raise credentials_exception
