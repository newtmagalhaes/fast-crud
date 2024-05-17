from datetime import datetime, timedelta
from http import HTTPStatus
from os import environ
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import get_db
from .models.user import User
from .schemas.auth import TokenData

_SECRET_KEY = environ["SECRET_KEY"]
_ALGORITHM = 'HS256'
_ACCESS_TOKEN_EXPIRE_MINUTES = 30
_pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = (
        datetime.now(tz=ZoneInfo('UTC'))
        + timedelta(minutes=_ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({'exp': expire})

    return encode(to_encode, _SECRET_KEY, algorithm=_ALGORITHM)


def hash_password(password: str) -> str:
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _pwd_context.verify(plain_password, hashed_password)


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload: dict = decode(token, _SECRET_KEY, algorithms=[_ALGORITHM])
        username: str | None = payload.get('sub')
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except DecodeError as e:
        raise credentials_exception from e

    # TODO: create and use cache
    user = db.scalar(select(User).where(User.email == token_data.username))

    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found'
        )

    return user
