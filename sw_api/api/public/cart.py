from flask_restplus import Resource, Namespace

from sw_api.schemas.cart import CartLoadSchema, CartItemDumpSchema
from sw_api.services.checkout_service import calculate_checkout
from sw_api.utils.check_body import check_body

cart_ns = Namespace("cart")


@cart_ns.route('/checkout')
class CartCheckoutEndpoint(Resource):
    @staticmethod
    @check_body(CartLoadSchema)
    def post(data):
        cart_items = calculate_checkout(data['products'])
        bankslip = CartItemDumpSchema().dump(cart_items, many=True).data
        return {'bankslip': bankslip, 'bankslip_total': sum([item['value'] for item in bankslip])}
