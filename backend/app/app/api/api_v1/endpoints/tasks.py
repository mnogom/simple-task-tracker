from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get('/', response_model=list[schemas.Task])
def read_tasks(db: Session = Depends(deps.get_db),
               skip: int = 0,
               limit: int = 100) -> Any:
    db_tasks = crud.get_tasks(db=db, skip=skip, limit=limit)
    return db_tasks


@router.get('/{task_id}', response_model=schemas.Task)
def get_task(task_id: int,
             db: Session = Depends(deps.get_db)) -> Any:
    db_task = crud.get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return db_task


@router.post('/', response_model=schemas.Task)
def create_task(task: schemas.TaskCreate,
                db: Session = Depends(deps.get_db)) -> Any:
    db_task = crud.create_task(db=db, task=task, user_id=1)
    if db_task is None:
        raise HTTPException(status_code=400, detail='Task was not created')
    return db_task


@router.put('/{task_id}', response_model=schemas.Task)
def update_task(task_id: int,
                updated_data: schemas.TaskUpdate,
                db: Session = Depends(deps.get_db)) -> Any:
    db_task = crud.get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail='Task was not found')
    db_task = crud.update_task(db=db, task_id=task_id, updated_data=updated_data)
    return db_task


@router.delete('/{task_id}', response_model=schemas.Task)
def delete_task(task_id: int,
                db: Session = Depends(deps.get_db)) -> Any:
    db_task = crud.get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail='Task was not found')
    db_task = crud.remove_task(db=db, task_id=task_id)
    return db_task

