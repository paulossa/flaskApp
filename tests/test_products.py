from http import HTTPStatus

import pytest

from sw_api.database import session
from sw_api.models import Product


@pytest.fixture
def fixture():
    products = [
        Product(name=f"prod {i}")
        for i in range(10)
    ]

    session().add_all(products)
    session().flush()

    return type("", (), {
        "total_products": len(products)
    })


def test_get_products(tst, fixture):
    response = tst.client.get('/products')
    assert response.status_code == 200
    assert len(response.json) == fixture.total_products
    assert set(response.json[0].keys()) == {'id', 'name', 'value'}


def test_post_product_success(tst):
    assert session().query(Product).count() == 0
    # Em uma aplicação com autenticação seria necessário envio de token
    payload = {
        'name': 'Novo Produto',
        'value': 340.5
    }
    response = tst.client.post('/products', headers={'Content-Type': 'application/json'}, data=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {
        'id': 1,
        'name': 'Novo Produto',
        'value': 340.5
    }

