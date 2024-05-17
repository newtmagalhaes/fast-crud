from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


__DATABASE_URL = environ["DATABASE_URL"]

__engine = create_engine(__DATABASE_URL)

__SessionLocal = sessionmaker(__engine)


def get_db():
    db = __SessionLocal()
    try:
        yield db
    finally:
        db.close()
