import itertools
from collections import defaultdict
from typing import Dict, List, Iterable, Tuple, Set
import string
import enum

# We need to remove all punctuation except for apostrophes (because they change pronunciation)
PUNCTUATION = string.punctuation.replace('\'', '')


class SyllableType(enum.Enum):
    STRESSED = enum.auto()
    UNSTRESSED = enum.auto()
    ANY = enum.auto()

    def generalize(self, other):
        """
        Returns ANY if a and b are different. Otherwise returns what a and b do.
        :param other:
        :return:
        """
        if self != other:
            return SyllableType.ANY
        return self


def _build_accent_pattern_from_phonemes(phonemes) -> Tuple[SyllableType, ...]:
    """
    Returns a list of syllable stress indicators
    :return:
    """
    result = []
    for phoneme in phonemes:
        if phoneme.endswith("0"):
            result.append(SyllableType.UNSTRESSED)
        elif phoneme.endswith("1") or phoneme.endswith("2"):
            result.append(SyllableType.STRESSED)
        else:
            # A sylable is defined as containing one and only one vowel, therefor we ignore consents
            continue

    if len(result) == 1:
        # One syllable words can have any stress
        return (SyllableType.ANY,)

    return tuple(result)


class Pronunciation:

    def __init__(self, phonemes: List[str]):
        """
        Create a new Pronunciation object from a list of phonemes in cmudict format.
        >>> Pronunciation(["P", "AY1", "TH", "AA0", "N"])
        :param syllables:
        """
        self.phonemes = phonemes
        self.accent_pattern = _build_accent_pattern_from_phonemes(self.phonemes)

    def update(self, phonemes):
        """
        Add an alternative pronunciation
        :param phonemes: List of phonemes in cmudict format
        """
        new_pattern = _build_accent_pattern_from_phonemes(phonemes)
        # change the new accent pattern to be any where different pronunciations disagree
        self.accent_pattern = tuple(a.generalize(b) for a, b in zip(new_pattern, self.accent_pattern))

    def __repr__(self):
        return f'<Pronunciation {",".join(self.phonemes)}>'

def match(a: Tuple[SyllableType,...], b: Tuple[SyllableType,...]) -> bool:
    """
    Return true if two accent patterns are equivalent
    """

    if len(a) != len(b):
        # Sentences cannot have the same accent pattern if they have a different number of syllables
        return False

    for s1, s2 in zip(a,b):
        # Only fail when a,b are unequal and neither is ANY
        if s1 != s2 and s1 != SyllableType.ANY and s2 != SyllableType.ANY:
            return False
    return True

class IambicValidator:

    def __init__(self):
        self.dictionary: Dict[str, Pronunciation] = {}

    def load(self, path):
        dict_file = open(path)
        for line in dict_file:
            if line.startswith(';;;'):
                # Skip comment lines
                continue

            if line[0] not in string.ascii_uppercase:
                # Ignore punctuation for now
                continue

            tokens = line.split()
            key = tokens[0]
            key = key.split('(')[0]  # Ignore differentiators for alternate pronunciations
            # they are handled by a list of Pronunciations
            pronunciation = tokens[1:]

            if key not in self.dictionary:
                self.dictionary[key] = Pronunciation(pronunciation)
            else:
                self.dictionary[key].update(pronunciation)

    def is_iambic(self, sentence: str):
        sentence = sentence.translate(str.maketrans('', '', PUNCTUATION))
        sentence = sentence.upper()
        sentence = sentence.split()
        sentence = tuple(itertools.chain(*[self.dictionary[word].accent_pattern for word in sentence]))
        print("")
        print(sentence)

        pattern = 5*(SyllableType.UNSTRESSED, SyllableType.STRESSED)    # 5 Iambs
        return match(sentence, pattern)

