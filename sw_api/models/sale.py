from sqlalchemy import Column, String

from sw_api.models.base import Base


class Sale(Base):
    __tablename__ = 'sale'
    identifier = Column(String, unique=True, primary_key=True, nullable=False)
    description = Column(String, nullable=False)
    str_func = Column(String, nullable=False)
