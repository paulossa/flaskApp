from sqlalchemy import Column, String

from sw_api.models import Product
from sw_api.models.base import Base


class Sale(Base):
    __tablename__ = 'sale'
    description = Column(String, nullable=False)
    str_func = Column(String, nullable=False)

# ------- Adicionar funções de calculo de promoções aqui para centralizar lógica ----


def trespor10_func(product: Product, quantity: int) -> list:
    out = []
    has_promo = quantity >= 3
    remainder = quantity % 3

    if has_promo:
        items_in_promo = quantity - (quantity % 3)
        out.append({
            'product': product.name,
            'value': (items_in_promo // 3) * 10,
            'quantity': items_in_promo,
            'sale': product.sale.description
        })

    if remainder:
        out.append({
            'product': product.name,
            'value': remainder * product.value,
            'quantity': remainder,
            'sale': None
        })

    return out


def pague1leve2_func(product: Product, quantity: int) -> list:
    out = []
    has_promo = quantity >= 2
    remainder = quantity % 2

    if has_promo:
        items_in_promo = quantity - (quantity % 2)
        out.append({
            'product': product.name,
            'value': items_in_promo//2 * product.value,
            'quantity': items_in_promo,
            'sale': product.sale.description
        })
    if remainder:
        out.append({
            'product': product.name,
            'value': remainder * product.value,
            'quantity': remainder,
            'sale': None
        })

    return out
