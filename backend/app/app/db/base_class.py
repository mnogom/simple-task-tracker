# https://docs.sqlalchemy.org/en/14/orm/mapping_api.html#sqlalchemy.orm.as_declarative

from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
