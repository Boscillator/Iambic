import pytest


@pytest.fixture(scope='module')
def app():
    from iambic import create_app
    app = create_app('Testing')

    from iambic.models import db
    with app.app_context():
        db.create_all()

    return app


@pytest.fixture(scope='module')
def test_client(app):
    return app.test_client()


@pytest.fixture(scope='module')
def db(test_client):
    from iambic.models import db
    return db
