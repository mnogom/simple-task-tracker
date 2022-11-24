from datetime import date

from pydantic import BaseModel
from app.models.task import Statuses


class TaskBase(BaseModel):
    name: str | None
    description: str | None = None
    status: Statuses | None
    deadline: date | None


class TaskCreate(TaskBase):
    name: str
    status: Statuses = Statuses.not_started
    deadline: date


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    owner_id: int
    created_at: date

    class Config:
        orm_mode = True
