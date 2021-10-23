from pytest import fixture

from app import create_app
from extensions import db as _db
from config import SQLALCHEMY_DATABASE_URI_TEST


@fixture(scope='session', autouse=True)
def app(request):
    app = create_app(testing=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI_TEST
    app.config['TESTING'] = True
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


@fixture(scope="session", autouse=True)
def db(app, request):
    """Returns session-wide initialized database"""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.close()
        _db.drop_all()
