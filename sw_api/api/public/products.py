from http import HTTPStatus

from flask_restplus import Namespace, Resource

from sw_api.database import session
from sw_api.models import Product
from sw_api.schemas.product import ProductSchema
from sw_api.utils.check_body import check_body
from sw_api.utils.responses import notfound, nocontent

products_ns = Namespace('products')


@products_ns.route('')
class ProductsEndpoint(Resource):
    @staticmethod
    def get():
        products = session().query(Product).all()
        return ProductSchema().dump(products, many=True)

    @staticmethod
    @check_body(ProductSchema)
    def post(data):
        product = Product(**data)
        session().add(product)
        session().flush()
        return ProductSchema().dump(product).data, HTTPStatus.CREATED


@products_ns.route('/<int:pid>')
class ProductsIdEndpoint(Resource):
    @staticmethod
    def get(pid):
        product = session().query(Product).get(pid)
        if not product:
            return notfound("Produto não encontrado")
        return ProductSchema().dump(product).data

    @staticmethod
    @check_body(ProductSchema)
    def put(data, pid):
        product = session().query(Product).get(pid)
        if not product:
            return notfound("Produto não encontrado")
        product.name = data['name']
        product.identifier = data['identifier']
        product.id_sale = data.get('id_sale')
        product.value = data.get('value', 0)
        session().flush()
        return ProductSchema().dump(product).data

    @staticmethod
    def delete(pid):
        product = session().query(Product).get(pid)
        if not product:
            return notfound('Produto não encontrado')

        session().delete(product)
        return nocontent()
