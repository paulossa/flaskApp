import json
from http import HTTPStatus

import pytest

from sw_api.database import session
from sw_api.models import Product

HEADERS = {'Content-Type': 'application/json'}


@pytest.fixture
def fixture():
    products = [
        Product(name=f"prod {i}")
        for i in range(10)
    ]

    session().add_all(products)
    session().flush()

    return type("", (), {
        "total_products": len(products),
        "products_ids": [str(p.id) for p in products],
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
    response = tst.client.post('/products', headers=HEADERS, data=json.dumps(payload))

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {
        'id': 1,
        'name': 'Novo Produto',
        'value': 340.5
    }
    assert session().query(Product).count() == 1


def test_post_product_badrequest(tst):
    payload = {
        'name': 'Novo Produto Inválido',
        'value': -10.50
    }
    response = tst.client.post('/products', headers=HEADERS, data=json.dumps(payload))

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {
        "message": {"value": ["Não pode ser negativo"]}
    }

    # Ajusta payload mas não envia nome
    payload["value"] = 100
    del payload["name"]
    response = tst.client.post('/products', headers=HEADERS, data=json.dumps(payload))
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {
        "message": {"name": ["Campo obrigatório"]}
    }


def test_delete_products_success(tst, fixture):
    assert session().query(Product).count() == fixture.total_products

    target_id = 6
    response = tst.client.delete(f'/products/{target_id}')

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert session().query(Product).count() == fixture.total_products - 1
    assert session().query(Product).get(target_id) is None

    target_id = 6
    response = tst.client.delete(f'/products/{target_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {
        "message": "Produto não encontrado"
    }


def test_update_products_success(tst, fixture):
    target_id = 7
    payload = {
        "name": "prod 6 - edited",
        "value": 99.99
    }

    product = session().query(Product).get(target_id)
    assert product.name == "prod 6"
    assert product.value == 0.0

    response = tst.client.put(f'/products/{target_id}', headers=HEADERS, data=payload)
    assert response.status_code == HTTPStatus.OK, response.json
    assert response.json == {
        "id": target_id,
        **payload
    }


    product = session().query(Product).get(target_id)
    assert product.name == payload['name']
    assert product.value == payload['value']






