from http import HTTPStatus

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas import auth as auth_schema
from ..security import create_access_token, verify_password


def get_access_token(
        form_data: OAuth2PasswordRequestForm,
        db: Session,
        ) -> auth_schema.Token:
    user = db.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found'
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password'
        )

    access_token = create_access_token(data={'sub': user.email})

    return auth_schema.Token(access_token=access_token, token_type='bearer')
