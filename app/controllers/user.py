from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models.user import User
from ..schemas import user as user_schema
from ..security import get_current_user
from ..services import user as user_service

router = APIRouter(prefix="/user", tags=["User"])


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
    response_model=user_schema.CreatedUser
)
def create_user(user: user_schema.RegisterUser, db: Session = Depends(get_db)):
    return user_service.validate_and_insert(user, db)


@router.get("/me", response_model=user_schema.CreatedUser)
def get_self_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=user_schema.CreatedUser)
def update_self_user(
        data: user_schema.UpdateUser,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
        ):
    return user_service.update_user(data, current_user, db)


@router.delete("/me", status_code=HTTPStatus.NO_CONTENT)
def delete_self_user(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
        ):
    return user_service.delete_user(current_user, db)
