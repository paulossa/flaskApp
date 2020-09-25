from http import HTTPStatus

import pytest
import dill as pickle

from sw_api.database import session
from sw_api.models import Sale, Product

INITIAL_PRODUCT_COUNT = 3


@pytest.fixture
def fixture():
    """
    O teste irá fazer uso de promoções criadas no bootstrap da aplicação
    Validando que elas funcionan corretamente
    E que novas promoções podem ser adicionadas facilmente
    """
    tpd = session().query(Sale).filter(Sale.description.ilike('%por%')).one_or_none()
    assert tpd is not None

    p1l2 = session().query(Sale).filter(Sale.description.ilike('%pague%')).one_or_none()
    assert p1l2 is not None

    return type("", (), {
        "tpd_id": tpd.id,
        "p1l2_id": p1l2.id,
    })

def test_get_sales(tst):
    # Endpoint para listar promocoes
    response = tst.client.get('/sales')
    assert response.status_code == HTTPStatus.OK
    assert response.json == [
        {
            'id': 1,
            'description': '3 por 10 reais',
        },
        {
            'id': 2,
            'description': 'Pague 1 Leve 2',
        }
    ], response.json



def test_pague1_leve2(tst, fixture):
    # Segundo o bootstrap pelo menos 1 produto deve iniciar relacionado a cada promoção
    product = session().query(Product).filter_by(id_sale=fixture.p1l2_id)
    product = product.order_by(Product.created_at.asc()).first()

    assert product is not None
    assert product.name == 'Desodorante Rexona Aerosol'
    assert product.value == 15.90

    # para saber o valor do produto decidimos encapsular a lógica dentro do produto.
    # Pois ele saberá se está associado a uma promoção.

    # Para 1 produto
    # o valor cobrado deve ser normal e não deve ter uma promoção associada
    result = product.get_calculated_values(1)
    assert result == [{
        'product': product.name,
        'value': product.value,
        'sale': None,
        'quantity': 1
    }]

    # Para 2 produtos a promoção deve ser aplicada e se pago o valor de 1 produto.
    result = product.get_calculated_values(2)
    assert result == [{
        'product': product.name,
        'value': product.value,
        'sale': 'Pague 1 Leve 2',
        'quantity': 2
    }]

    # Para 3 produtos, a promoção deve ser aplicada apenas para os 2 primeiros
    result = product.get_calculated_values(3)
    assert result == [{
        'product': product.name,
        'value': product.value,
        'sale': 'Pague 1 Leve 2',
        'quantity': 2
    }, {
        'product': product.name,
        'value': product.value,
        'sale': None,
        'quantity': 1
    }]

    # para 5 produtos, 4 produtos teriam a promoção aplicada mas nao o 5º
    # ou seja, ele pegaria 4 produtos e pagaria por 2.
    # E pagaria o valor completo do quinto produto, pois não é elegível para promoção.
    result = product.get_calculated_values(5)
    assert result == [{
        'product': product.name,
        'value': product.value * 2,
        'sale': 'Pague 1 Leve 2',
        'quantity': 4
    }, {
        'product': product.name,
        'value': product.value,
        'sale': None,
        'quantity': 1
    }]


def test_tres_por_10(tst, fixture):
    product = session().query(Product).filter_by(id_sale=fixture.tpd_id)
    product = product.order_by(Product.created_at.asc()).first()

    assert product is not None
    assert product.name == 'Coca Cola'
    assert product.value == 4.00

    # para 1 produto preço normal, sem promoção relacionada
    result = product.get_calculated_values(1)
    assert result == [{
        'product': product.name,
        'value': product.value,
        'sale': None,
        'quantity': 1
    }]

    # para 2 produtos, sem promoção tbm
    result = product.get_calculated_values(2)
    assert result == [{
        'product': product.name,
        'value': product.value * 2,
        'sale': None,
        'quantity': 2
    }]

    # para 3 produtos promoção aplicada ~
    result = product.get_calculated_values(3)
    assert result == [{
        'product': product.name,
        'value': 10,
        'sale': "3 por 10 reais",
        'quantity': 3,
    }]

    # para 7 produtos promoção aplicada para os 6 primeiros, preço cheio no sétimo
    result = product.get_calculated_values(7)
    assert result == [{
        'product': product.name,
        'value': 20,
        'sale': "3 por 10 reais",
        'quantity': 6,
    }, {
        'product': product.name,
        'value': product.value,
        'sale': None,
        'quantity': 1
    }]


def test_new_sale_25_percent_off(tst):
    # Criar uma nova promoção consiste apenas em:
    # - Criar função que obedeça contrato
    # - Criar promoção serializando função de calculo de preço de produtos
    # - Associar promoção aos produtos desejados

    def sale_25_percent_off(product, quantity):
        return [{
            "product": product.name,
            "value": product.value * quantity * (1 - 0.25),
            "quantity": quantity,
            "sale": "Desconto de 25%",
        }]

    sale = Sale(description="Desconto de 25%", str_func=pickle.dumps(sale_25_percent_off))
    session().add(sale)
    session().flush()

    p = Product(identifier='i321', name="Smartphone TchauMe", value=1000, id_sale=sale.id)
    session().add(p)
    session().flush()

    assert p.get_calculated_values(1) == [
        {
            "product": 'Smartphone TchauMe',
            "value": 750.0,
            "quantity": 1,
            "sale": "Desconto de 25%",
        }
    ]
