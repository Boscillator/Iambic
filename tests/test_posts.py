import json

from .fixtures import *

from iambic.models import Post


def test_create(app, test_client):
    """
    Test that a post can be created by sending a post request.
    Assert that this returns the correct value and changes persist to the database
    """
    req = {
        'body': 'Shall I compare thee to a summer\'s day?'
    }

    resp = test_client.post('/posts',
                            data=json.dumps(req),
                            content_type='application/json')

    resp = json.loads(resp.data)
    assert resp == {
        'body': 'Shall I compare thee to a summer\'s day?'
    }

    with app.app_context():
        assert Post.query.get(1).body == 'Shall I compare thee to a summer\'s day?'


def test_get(test_client):
    resp = test_client.get('/posts')
    resp = json.loads(resp.data)

    assert resp == [
        {'body': 'Shall I compare thee to a summer\'s day?'}
    ]
