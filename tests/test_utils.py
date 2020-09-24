from http import HTTPStatus

from sw_api.database import session
from sw_api.models import Product


def test_check_body(tst):
    """
    Quando check_body é acionado, Content-Type: application/json
    é obrigatório nos headers
    """

    response = tst.client.put('/products/1', data={'description': 'Invalid'})
    assert response.status_code == HTTPStatus.BAD_REQUEST, response.json
    assert response.json == {
        "message": "Content-Type must be \"application/json\""
    }


def test_model_repr(tst):
    p = session().query(Product).get(1)
    assert p is not None
    assert repr(p) == '<Product 1>'
