from datetime import date

from pydantic import BaseModel
from app.models.task import Statuses


class TaskBase(BaseModel):
    name: str
    description: str | None = None
    status: Statuses
    deadline: date


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    owner_id: int
    created_at: date

    class Config:
        orm_mode = True
