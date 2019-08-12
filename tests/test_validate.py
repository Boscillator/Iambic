from .fixtures import *
import json


def _validate(test_client, text):
    req = {
        'body': text
    }
    resp = test_client.post('/validate',
                            data=json.dumps(req),
                            content_type='application/json')
    resp = json.loads(resp.data)
    return resp


def test_validate_sonnet_18(test_client, sonnet_18_text):
    resp = _validate(test_client, sonnet_18_text)
    print("===resp===")
    print(resp)
    assert resp[0]['ok']
    assert resp[0]['reason'] == 'Ok.'
    assert resp[1]['ok']
    assert len(resp) == 4


def test_validate_tenenbaum(test_client):
    resp = _validate(test_client, "Tenenbaum")
    assert not resp[0]['ok']
    assert resp[0]['reason'] == 'Two syllables with stress in a row.'
