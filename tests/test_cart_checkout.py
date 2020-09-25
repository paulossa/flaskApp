import json

HEADERS = {'Content-Type': 'application/json'}


def test_successfull_checkout(tst):
    payload = {
        'products': [
            {'id_product': 1, 'quantity': 5},
            {'id_product': 2, 'quantity': 5},
            {'id_product': 3, 'quantity': 5},
        ]
    }

    response = tst.client.post('/cart/checkout', headers=HEADERS, data=json.dumps(payload))
    assert response.status_code == 200, response.json
    assert response.json == {
        'bankslip_total': 10 + 8 + 31.8 + 15.9 + 250,
        'bankslip': [
        {
            'product': 'Coca Cola',
            'quantity': 3,
            'sale': '3 por 10 reais',
            'value': 10.0
        },
        {
            'product': 'Coca Cola',
            'quantity': 2,
            'sale': None,
            'value': 2 * 4.0
        },
        {
            'product': 'Desodorante Rexona Aerosol',
            'quantity': 4,
            'sale': 'Pague 1 Leve 2',
            'value': 2 * 15.9
        },
        {
            'product': 'Desodorante Rexona Aerosol',
            'quantity': 1,
            'sale': None,
            'value': 15.9},
        {
            'product': 'Saco de lixo 24ltrs',
            'quantity': 5,
            'sale': None,
            'value': 5 * 50.0}
    ]}
