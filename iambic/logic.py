import itertools
import time
from collections import defaultdict
from typing import Dict, List, Iterable, Tuple, Set
import string
import enum
import logging

logger = logging.getLogger(__name__)

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

    def __invert__(self):
        if self == SyllableType.UNSTRESSED:
            return SyllableType.STRESSED
        elif self == SyllableType.STRESSED:
            return SyllableType.UNSTRESSED
        else:
            return SyllableType.ANY


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

def _pairwise(iterable):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    https://stackoverflow.com/a/5764807
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def _is_iambicable(accent_pattern):
    """
    Returns True if an accent pattern could ever appear in an iambic pentameter sentance.
    (if the word has no same syllables in a row)
    """

    for s1, s2 in _pairwise(accent_pattern):
        # 2 of the same accent in a row (and not any)
        if s1 == s2 and s1 != SyllableType.ANY:
            return False

    return True


class Pronunciation:

    def __init__(self, phonemes: List[str]):
        """
        Create a new Pronunciation object from a list of phonemes in cmudict format.
        >>> Pronunciation(["P", "AY1", "TH", "AA0", "N"])
        :param syllables:
        """
        self.phonemes = phonemes
        self.accent_pattern = _build_accent_pattern_from_phonemes(self.phonemes)
        self.valid = _is_iambicable(self.accent_pattern)


    @property
    def start_state(self):
        return self.accent_pattern[0]

    @property
    def n_transitions(self):
        return len(self.accent_pattern)

    def __repr__(self):
        return f'<Pronunciation {",".join(self.phonemes)}>'

def _is_valid_transition(pronunciation: Pronunciation, state: SyllableType):
    logger.debug(f"_is_valid_transition with {','.join(pronunciation.phonemes)} on state {state}")
    return pronunciation.start_state != state

class IambicValidator:

    def __init__(self):
        self.dictionary: Dict[str, List[Pronunciation]] = defaultdict(list)

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
            self.dictionary[key].append(Pronunciation(pronunciation))

    def _is_iambic(self, words, state = SyllableType.STRESSED, n_syllables = 0):

        logger.debug(f"_is_iambic({words}, {state}, {n_syllables})")

        # OK. Here is the thinking. Iambic pentameter can be validated using a non-finite state machine. There are
        # the two states, STRESSED and UNSTRESSED. The sentence must have 10 syllables, and we must end on a
        # STRESSED state. Each possible pronunciation of a word represents a transition between the stressed and
        # unstressed states. If it has two of the same syllable in a row, the sentence is rejected. If it has an
        # odd number of syllables, the state switches. If it has an even number of syllables, the state remains the
        # same.

        if n_syllables != 10 and len(words) == 0:
            # More or less then 10 syllables
            logger.debug("More or less than 10 syllables")
            return False

        if n_syllables == 10 and len(words) == 0:
            # Correct number of syllables, NFA has consumed all input
            logger.debug("Accepted iambic pentameter")
            return True

        current = words[0]
        pronunciations = self.dictionary[current]
        any_ok = False  # Store if any branch of the NFA has found an accept state
        for pronunciation in pronunciations:
            # if not pronunciation.valid:
            #     # Turns out if you leave this rule in, Sonnet 18 breaks, and I don't want to break it
            #     # Double syllable somewhere in the word, reject.
            #     logger.debug("Double syllable in word")
            #     logger.debug(pronunciation)
            #     continue
            if not _is_valid_transition(pronunciation, state):
                # Double syllable between last word and current, reject.
                logger.debug("Double syllables between words")
                continue

            if pronunciation.n_transitions % 2 == 1:
                new_state = ~state
            else:
                new_state = state
            new_words = words[1:]   # Recur with current word consumed
            new_n_syllables = n_syllables + pronunciation.n_transitions
            any_ok |= self._is_iambic(new_words, new_state, new_n_syllables)

            if any_ok:
                # Return early if accept state is found, otherwise keep looking
                return True

        return any_ok


    def is_iambic(self, sentence: str):
        t = time.time()
        sentence = sentence.translate(str.maketrans('', '', PUNCTUATION))
        sentence = sentence.upper()
        sentence = sentence.split()

        logging.info(f"Evaluated iambic pentameter for '{sentence}' in {time.time() - t:.2f}s")

        return self._is_iambic(sentence)

    def is_stanza_iambic(self, stanza: str):
        sentences = stanza.strip().splitlines()
        return all(self.is_iambic(sentence) for sentence in sentences)
