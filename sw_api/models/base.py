import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData


NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class ModelBase:
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.now(), nullable=False)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"


Base = declarative_base(cls=ModelBase, metadata=MetaData(naming_convention=NAMING_CONVENTION))

