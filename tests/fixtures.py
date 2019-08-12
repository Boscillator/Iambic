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

@pytest.fixture()
def sonnet_18_text():
    return """
    Shall I compare thee to a summer's day?
    Thou art more lovely and more temperate:
    Rough winds do shake the darling buds of May,
    And summer's lease hath all too short a date;
    """
