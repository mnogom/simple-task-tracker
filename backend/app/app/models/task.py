import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Statuses(enum.Enum):
    not_started = 'Not started'
    in_progress = 'In progress'
    finished = 'Finished'
    canceled = 'Canceled'


class Task(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    status = Column(Enum(Statuses), default=Statuses.not_started, nullable=False)
    created_at = Column(Date, default=func.now(), nullable=False)
    deadline = Column(Date)

    owner = relationship('User', back_populates='tasks')
