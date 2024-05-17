from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.services.auth import get_access_token

from ..db import get_db
from ..security import oauth2_scheme
from ..schemas import auth as auth_schema

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=auth_schema.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return get_access_token(form_data, db)

