from sqlalchemy.orm import Session

from app import models, schemas


def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[models.Task]:
    return db.query(models.Task).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: int) -> models.Task:
    return db.query(models.Task).get(task_id)


def get_user_tasks(db: Session,
                   user_id: int,
                   skip: int = 0,
                   limit: int = 100) -> list[models.Task]:
    return (db
            .query(models.Task)
            .where(models.Task.owner_id == user_id)
            .offset(skip)
            .limit(limit)
            .all())


def create_task(db: Session,
                task: schemas.TaskCreate,
                user_id: int) -> models.Task:
    db_task = models.Task(
        **task.dict(),
        owner_id=user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session,
                task_id,
                updated_data: schemas.TaskUpdate) -> models.Task:
    db_task = get_task(db=db, task_id=task_id)
    task_data = updated_data.dict(exclude_none=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    db.add(task_data)
    db.commit()
    db.refresh(task_data)
    return db_task


def remove_task(db: Session,
                task_id: int) -> models.Task:
    db_task = get_task(db=db, task_id=task_id)
    db.delete(db_task)
    db.commit()
    return db_task


