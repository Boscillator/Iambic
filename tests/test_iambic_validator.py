import itertools
from pprint import pprint

import pytest

from iambic.logic import IambicValidator, ValidationResult


@pytest.fixture(scope='module')
def dictionary():
    validator = IambicValidator()
    validator.load('data/cmudict-0.7b.txt')
    return validator


def test_iambic_validator_true(dictionary):
    assert dictionary.is_iambic('Shall I compare thee to a summer\'s day?')
    assert dictionary.is_iambic('To swell the gourd, and plump the hazel shells')


def test_iambic_validator_false(dictionary):
    assert not dictionary.is_iambic("This is not valid text.")


def test_validation_reasons(dictionary):
    assert dictionary.is_iambic("Not valid.").reason == ValidationResult.Reason.WRONG_NUMBER_OF_SYLLABLES
    assert dictionary.is_iambic("ASDF").reason == ValidationResult.Reason.UNKNOWN_WORD
    assert dictionary.is_iambic("Tenenbaum Duplication Syllable").reason == ValidationResult.Reason.DOUBLE_STRESS


def test_validation_at(dictionary):
    assert dictionary.is_iambic("Not valid.").at == 2
    assert dictionary.is_iambic("ASDF").at == 0
    assert dictionary.is_iambic("Tenenbaum Duplication Syllable").at == 0


def test_is_stanza_iambic(dictionary):
    text = """
    Shall I compare thee to a summer's day?
    Thou art more lovely and more temperate:
    Rough winds do shake the darling buds of May,
    And summer's lease hath all too short a date;
    """

    assert dictionary.is_stanza_iambic(text)
