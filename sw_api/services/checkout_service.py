from sw_api.database import session
from sw_api.models import Product


def calculate_checkout(cart):
    """
    Usado para calcular o valor dos items em um carrinho
    :param cart: Lista de items no formato {id_product:str, quantity: int}
    :return: Lista de items no formato {product:str, value: flaot, sale: Optional[str], quantity: int}
    """
    out = []
    for item in cart:
        product = session().query(Product).get(item.get('id_product'))
        if product:
            out += product.get_calculated_values(item.get('quantity'))

    return out
