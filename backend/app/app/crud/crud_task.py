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


def create_user_task(db: Session,
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
