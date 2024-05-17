from datetime import datetime, timedelta
from os import environ
from zoneinfo import ZoneInfo

from jwt import encode
from passlib.context import CryptContext
from pydantic import SecretStr

_SECRET_KEY = environ["SECRET_KEY"]
_ALGORITHM = 'HS256'
_ACCESS_TOKEN_EXPIRE_MINUTES = 30
_pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


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
