from sqlalchemy.orm import validates, relationship

from sw_api.models.base import Base

from sqlalchemy import Column, Integer, Float, ForeignKey, String


class Product(Base):
    __tablename__ = "product"
    name = Column(String)
    value = Column(Float, nullable=False, default=0)
    id_sale = Column(Integer, ForeignKey("sale.id"), nullable=True)

    sale = relationship(
        "Sale", primaryjoin="Product.id_sale == Sale.id"
    )

    @validates('value')
    def value_validation(self, key, value):
        assert value >= 0, 'Valor não pode ser negativo'
        return value
