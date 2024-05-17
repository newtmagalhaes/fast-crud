from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas import user as user_schema
from ..security import hash_password


def validate_and_insert(user: user_schema.RegisterUser, db: Session):
    result = get_user_id_by_email_or_username(user.email, user.username, db)

    if result is not None:
        raise HTTPException(HTTPStatus.CONFLICT, detail="Username or email already used")

    new_user = User(
        **user.model_dump(exclude={"password"}),
        hashed_password=hash_password(user.password.get_secret_value()),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_id_by_email_or_username(email: str, username: str, db: Session) -> int|None:
    sql = (
        select(User.id)
        .where(User.email.like(email) | User.username.like(username))
        .limit(1)
    )
    return db.execute(sql).scalar_one_or_none()


def update_user(data: user_schema.UpdateUser, user: User, db: Session):
    user_id = db.scalar(
        select(User.id)
        .where(User.username.like(data.username) & (User.id != user.id))
        .limit(1)
    )
    if user_id is not None:
        raise HTTPException(HTTPStatus.CONFLICT, detail="Username or email already used")

    user.username = data.username
    user.nickname = data.nickname
    db.commit()
    return user


def delete_user(user, db: Session):
    db.delete(user)
    db.commit()
