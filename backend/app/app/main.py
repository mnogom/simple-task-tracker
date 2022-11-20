from typing import Generator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db.base_class import Base
from app.db.session import SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def read_root():
    return {'message': 'Hello, World!'}


@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate,
                db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return crud.create_user(db=db, user=user)


@app.get('/users/', response_model=list[schemas.User])
def get_users(skip: int = 0,
              limit: int = 100,
              db: Session = Depends(get_db)):
    db_users = crud.get_users(db=db, skip=skip, limit=limit)
    return db_users


@app.get('/users/{user_id}/', response_model=schemas.User)
def get_user(user_id: int,
             db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@app.put('users/{user_id}/', response_model=schemas.User)
def update_user(user_id: int,
                user: schemas.UserUpdate,
                db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user=user)
    return db_user


@app.post('/users/{user_id}/tasks/', response_model=schemas.Task)
def create_task(user_id: int,
                task: schemas.TaskCreate,
                db: Session = Depends(get_db)):
    db_task = crud.create_user_task(db=db, task=task, user_id=user_id)
    if db_task is None:
        raise HTTPException(status_code=400, detail='task was not created')
    return db_task


@app.get('/users/{user_id}/tasks/', response_model=list[schemas.Task])
def get_tasks_by_user(user_id: int,
                      skip: int = 0,
                      limit: int = 100,
                      db: Session = Depends(get_db)):
    db_tasks = crud.get_user_tasks(db=db, user_id=user_id, skip=skip, limit=limit)
    return db_tasks


@app.get('/tasks/', response_model=list[schemas.Task])
def get_tasks(db: Session = Depends(get_db)):
    db_tasks = crud.get_tasks(db=db, skip=0, limit=10)
    return db_tasks
