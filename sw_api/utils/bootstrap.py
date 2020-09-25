import dill as pickle

from sw_api.database import session
from sw_api.models import Sale, Product
from sw_api.models.sale import trespor10_func, pague1leve2_func


def bootstrap_data():
    """
    Adiciona dados ao banco de dados quando o projeto roda e não encontra
    produtos salvos.
    """
    sales = [
        Sale(
            description="3 por 10 reais",
            str_func=pickle.dumps(trespor10_func)
        ),
        Sale(
            description='Pague 1 Leve 2',
            str_func=pickle.dumps(pague1leve2_func)
        )
    ]

    session().add_all(sales)
    session().flush()

    products = [
        Product(
            identifier='b001',
            name='Coca Cola',
            value=4.0,
            id_sale=sales[0].id
        ),
        Product(
            identifier='c001',
            name='Desodorante Rexona Aerosol',
            value=15.90,
            id_sale=sales[1].id,
        ),
        Product(
            identifier='l001',
            name='Saco de lixo 24ltrs',
            value=50
        )
    ]

    session().add_all(products)
    session().flush()
