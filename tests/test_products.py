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
