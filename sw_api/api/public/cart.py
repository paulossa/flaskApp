from flask_restplus import Resource, Namespace

cart_ns = Namespace("cart")


@cart_ns.route('checkout')
class CartCheckoutEndpoint(Resource):
    def get(self):
        return 'hello miserave'