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


class ValidationResult:
    class Reason(enum.Enum):
        OK = "Ok."
        WRONG_NUMBER_OF_SYLLABLES = "Too many syllables."
        DOUBLE_STRESS = "Two syllables with stress in a row."
        UNKNOWN_WORD = "Unknown word."

    def __init__(self, ok: bool, at: int, reason: Reason):
        """
        :param ok: Does the sentence conform to Iambic Pentameter
        :param at: What word the failure occurred on.
        :param reason: Why there was a failure
        """
        self.reason = reason
        self.at = at
        self.ok = ok

    def __bool__(self):
        return self.ok


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

        # Convert from default dict so we get key errors when words are not found.
        self.dictionary = dict(self.dictionary)

    def _is_iambic(self, words, word_number=0, state=SyllableType.STRESSED, n_syllables=0) -> ValidationResult:

        logger.debug(f"_is_iambic({words}, {word_number}, {state}, {n_syllables})")

        # OK. Here is the thinking. Iambic pentameter can be validated using a non-finite state machine. There are
        # the two states, STRESSED and UNSTRESSED. The sentence must have 10 syllables, and we must end on a
        # STRESSED state. Each possible pronunciation of a word represents a transition between the stressed and
        # unstressed states. If it has two of the same syllable in a row, the sentence is rejected. If it has an
        # odd number of syllables, the state switches. If it has an even number of syllables, the state remains the
        # same.

        if n_syllables != 10 and len(words) == 0:
            # More or less then 10 syllables
            logger.debug("More or less than 10 syllables")
            return ValidationResult(False, word_number, ValidationResult.Reason.WRONG_NUMBER_OF_SYLLABLES)

        if n_syllables == 10 and len(words) == 0:
            # Correct number of syllables, NFA has consumed all input
            logger.debug("Accepted iambic pentameter")
            return ValidationResult(True, word_number, ValidationResult.Reason.OK)

        current = words[0]
        try:
            pronunciations = self.dictionary[current]
            print(pronunciations)
        except KeyError:
            logger.debug(f"Unknown word {current}")
            return ValidationResult(False, word_number, ValidationResult.Reason.UNKNOWN_WORD)
        last_error = None
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
                last_error = ValidationResult(False, word_number, ValidationResult.Reason.DOUBLE_STRESS)
                continue

            if pronunciation.n_transitions % 2 == 1:
                new_state = ~state
            else:
                new_state = state
            new_words = words[1:]  # Recur with current word consumed
            new_n_syllables = n_syllables + pronunciation.n_transitions
            new_word_number = word_number + 1
            last_error = self._is_iambic(new_words, new_word_number, new_state, new_n_syllables)

            if last_error:
                # Return early if accept state is found, otherwise keep looking
                return last_error

        return last_error

    def is_iambic(self, sentence: str) -> ValidationResult:
        t = time.time()
        sentence = sentence.translate(str.maketrans('', '', PUNCTUATION))
        sentence = sentence.upper()
        sentence = sentence.split()

        result = self._is_iambic(sentence)

        logging.info(f"Evaluated iambic pentameter for '{sentence}' in {time.time() - t:.2f}s")

        return result

    def is_stanza_iambic(self, stanza: str):
        sentences = stanza.strip().splitlines()
        return all(self.is_iambic(sentence) for sentence in sentences)


# Create a singleton instance to use in the real application. Load is called by create_app
validator = IambicValidator()
