from sqlalchemy import Column, Boolean, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)
    # TODO: Fix user can create itself with is_superuser = True
    is_superuser = Column(Boolean, default=False, nullable=False)

    tasks = relationship('Task', back_populates='owner')
