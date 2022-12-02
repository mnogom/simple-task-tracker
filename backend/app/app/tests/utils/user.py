from sqlalchemy.orm import Session

from app.models import User
from app import schemas
from app import crud


def create_test_user(db: Session) -> User:
    email = 'test_user@booble.com'
    password = 'password'
    full_name = 'John Doe'
    user = schemas.UserCreate(email=email,
                              password=password,
                              full_name=full_name)
    user_db = crud.create_user(db=db, user=user)
    return user_db
