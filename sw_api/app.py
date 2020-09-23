# Ajuste para erro de import como descrito em: https://github.com/jarus/flask-testing/issues/143#issuecomment-687167825
from flask import Flask
from flask_cors import CORS
import werkzeug

from sw_api.database import set_session, commit_session, session
from sw_api.models import Product
from sw_api.utils.bootstrap import bootstrap_data

werkzeug.cached_property = werkzeug.utils.cached_property
from sw_api.api.public.api import public_bp


def make_app(engine=None):
    _app = Flask(__name__)
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://db.sqlite"
    CORS(_app)

    database(_app, engine)

    # Register routes
    _app.register_blueprint(public_bp)

    return _app


def database(application, engine=None):
    set_session("sqlite://", engine=engine)

    product_count = session().query(Product).count()
    if product_count == 0:
        bootstrap_data()



    @application.teardown_appcontext
    def finish_session(exception=None):
        commit_session(exception)


if __name__ == '__main__':
    app = make_app()
