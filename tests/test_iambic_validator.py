import itertools
from pprint import pprint

import pytest

from iambic.logic import Pronunciation, IambicValidator, SyllableType, match

@pytest.fixture(scope='module')
def dictionary():
    validator = IambicValidator()
    validator.load('data/cmudict-0.7b.txt')
    return validator

def test_pronunciation_accent_pattern():
    assert Pronunciation(["Y", "UW1", "N", "AH0", "T"]).accent_pattern == (SyllableType.STRESSED, SyllableType.UNSTRESSED)
    assert Pronunciation(["T", "EH1", "S", "T"]).accent_pattern == (SyllableType.ANY, )

def test_pronunciation_update():
    p = Pronunciation(["Y", "UW1", "N", "AH0", "T"])
    print(p.accent_pattern)
    p.update(["Y", "UW0", "N", "AH0", "T"])
    print(p.accent_pattern)
    assert p.accent_pattern == (SyllableType.ANY, SyllableType.UNSTRESSED)

def test_match():
    p1 = (SyllableType.ANY, SyllableType.ANY)
    p2 = (SyllableType.STRESSED, SyllableType.UNSTRESSED)
    p3 = (SyllableType.ANY, SyllableType.STRESSED)
    p4 = (SyllableType.ANY, SyllableType.ANY, SyllableType.ANY)

    assert match(p1, p1)
    assert match(p1, p2)
    assert match(p1, p3)
    assert match(p2,p2)
    assert not match(p2, p3)
    assert not match(p1,p4)
    assert not match(p2, p4)

def test_iambic_validator_true(dictionary):
    assert dictionary.is_iambic('Shall I compare thee to a summer\'s day?')
    assert dictionary.is_iambic('To swell the gourd, and plump the hazel shells')

def test_iambic_validator_false(dictionary):
    assert not dictionary.is_iambic("This is not valid text.")
