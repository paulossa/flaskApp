from sqlalchemy.orm import validates

from sw_api.models.base import Base

from sqlalchemy import Column, String, Float


class Product(Base):
    __tablename__ = "product"
    name = Column(String)
    value = Column(Float, nullable=False, default=0)

    @validates('value')
    def value_validation(self, key, value):
        assert value >= 0, 'Valor não pode ser negativo'
        return value
