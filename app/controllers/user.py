from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..schemas import user as user_schema
from ..services import user as user_service

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/", status_code=HTTPStatus.CREATED, response_model=user_schema.CreatedUser)
def create_user(user: user_schema.RegisterUser, db: Session = Depends(get_db)):
    return user_service.validate_and_insert(user, db)
