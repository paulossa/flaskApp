from flask_restplus import Namespace, Resource

from sw_api.database import session
from sw_api.models import Product
from sw_api.schemas.product import ProductGetSchema

products_ns = Namespace('products')


@products_ns.route('')
class ProductsEndpoint(Resource):
    @staticmethod
    def get():
        products = session().query(Product).all()
        return ProductGetSchema().dump(products, many=True)

