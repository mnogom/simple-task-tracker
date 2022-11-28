from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get('/', response_model=list[schemas.User])
def read_users(db: Session = Depends(deps.get_db),
               skip: int = 0,
               limit: int = 100) -> Any:
    db_users = crud.get_users(db=db, skip=skip, limit=limit)
    return db_users


@router.get('/{user_id}', response_model=schemas.User)
def read_user(user_id: int,
              db: Session = Depends(deps.get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@router.post('/', response_model=schemas.User)
def create_user(user: schemas.UserCreate,
                db: Session = Depends(deps.get_db)) -> Any:
    db_user = crud.create_user(db=db, user=user)
    if db_user is None:
        raise HTTPException(status_code=400, detail='User was not created')
    return db_user


@router.put('/{user_id}', response_model=schemas.User)
def update_user(user_id: int,
                updated_data: schemas.UserUpdate,
                db: Session = Depends(deps.get_db)) -> Any:
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    db_user = crud.update_user(db=db, user_id=user_id, updated_data=updated_data)
    return db_user


@router.delete('/{user_id}', response_model=schemas.User)
def delete_user(user_id: int,
                db: Session = Depends(deps.get_db)) -> Any:
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    db_user = crud.remove_user(db=db, user_id=user_id)
    return db_user
