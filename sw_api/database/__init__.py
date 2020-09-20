from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from sw_api.models.base import Base

_dbsession = None
_engine = None
_sqlalchemy_url = None


def set_session(sqlalchemy_url, engine=None):
    global _dbsession, _engine, _sqlalchemy_url
    _sqlalchemy_url = _sqlalchemy_url or sqlalchemy_url
    _engine = _engine or engine or create_engine(_sqlalchemy_url)
    _dbsession = scoped_session(sessionmaker(bind=_engine))

    Base.query = _dbsession.query_property()
    import sw_api.models
    Base.metadata.create_all(bind=_engine)
    return _dbsession


def commit_session(exception=None):
    if exception:
        _dbsession.rollback()
    else:
        _dbsession.commit()
    _dbsession.remove()
    if hasattr(_engine, "dispose"):
        _engine.dispose()


def rollback_session():
    _dbsession.rollback()
    _dbsession.remove()
    if hasattr(_engine, "dispose"):
        _engine.dispose()


def session():
    return _dbsession
