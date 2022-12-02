from sqlalchemy.orm import Session

from app import models, schemas
from app.core.security import get_password_hash, verify_password


def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).get(user_id)

def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(db: Session,
                user_id: int,
                updated_data: schemas.UserUpdate):
    db_user = get_user(db=db, user_id=user_id)
    user_data = updated_data.dict(exclude_none=True)

    password = user_data.pop('password', None)
    if password:
        setattr(db_user, 'hashed_password', get_password_hash(password))

    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def remove_user(db: Session,
                user_id: int) -> schemas.User:
    db_user = get_user(db=db, user_id=user_id)
    db.delete(db_user)
    db.commit()
    return db_user


def authenticate_user(db: Session,
                      email: str,
                      password: str) -> models.User | None:
    db_user = get_user_by_email(db=db, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
