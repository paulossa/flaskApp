from flask_restplus import Resource, Namespace

from sw_api.database import session
from sw_api.models import Sale
from sw_api.schemas.sales import SalesSchema

sales_ns = Namespace("sales")


@sales_ns.route('')
class SalesEndpoint(Resource):
    @staticmethod
    def get():
        sales = session().query(Sale).order_by(Sale.description.asc())
        return SalesSchema().dump(sales, many=True).data
