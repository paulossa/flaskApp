from http import HTTPStatus

from flask_restplus import Namespace, Resource

from sw_api.database import session
from sw_api.models import Product
from sw_api.schemas.product import ProductSchema
from sw_api.utils.check_body import check_body

products_ns = Namespace('products')


@products_ns.route('')
class ProductsEndpoint(Resource):
    def get(self):
        products = session().query(Product).all()
        return ProductSchema().dump(products, many=True)

    print('---------------alooooooooooo-----------------')

    @check_body(ProductSchema)
    def post(self, data):
        product = Product(**data)
        session().add(product)
        session().flush()
        return ProductSchema().dump(product).data, HTTPStatus.CREATED
