# wordsmith.py

import nltk
from nltk.corpus import cmudict
import itertools
from more_itertools import partitions
from typing import List, Tuple, Dict, Any
import argparse


# Type-checking
WordPronunciation = List[str]
WordsPronunciationsList = List[List[WordPronunciation]]
PhrasePronunciationList = List[List[str]]
PhraseList = List[str]

# Carnegie Mellon Pronuncing Dictionary maps words to lists of pronunciations
CMPD = cmudict.dict()


def invert_CMPD(CMPD: dict = CMPD) -> Dict[tuple, list]:
    """
    Creates a dictionary whose keys are 'pronunciations' (i.e. lists of strs
    representing phonemes) and whose values are words that correspond to thoses
    pronunciations. Essentially flips the CMPD, accounting for the fact that
    multiple words can have the same pronunciation.
    """
    inverted: Dict[tuple, list] = {}

    for word, its_pronunciations in CMPD.items():
        for pronunciation in its_pronunciations:
            pronunciation = tuple(pronunciation)  # Make hashable

            inverted[pronunciation] = inverted.get(pronunciation, [])
            inverted[pronunciation].append(word)

    return inverted


CMPD_INVERTED = invert_CMPD()  # Bit annoyed that I've put this down here but oh well


def get_word_pronunciations(words: List[str], CMPD: dict = CMPD) -> WordsPronunciationsList:
    """Gets every pronunciation of every word in `words`.

    Parameters
    ----------
    words:
        List of strs representing words.
    CMPD:
        The Carnegie Mellon Pronuncing Dictionary.

    Returns
    -------
    word_pronunciation_list:
        Each sub-list corresponds to a word. Each sub-sub-list corresponds to a
        distinct pronunciation of that word.
    """

    def get_pronunciation(word: str) -> List[List[str]]:
        try:
            return CMPD[word]
        except KeyError:
            raise

    result = list(map(get_pronunciation, words))
    return result


def get_phrase_pronunciations(word_pronunciations: WordsPronunciationsList) -> PhrasePronunciationList:
    """Gets every possible combination of pronunciations from the given list.

    Parameters
    ----------
    word_pronunciations:
        Each sub-list corresponds to a word. Each sub-sub-list corresponds to a
        distinct pronunciation of that word.

    Returns
    -------
    phrase_pronunciation_list:
        Each sub-list of strs represents a distinct pronunciation of the 
        original phrase.

    Example
    -------
    >>> word_pronunciations = [[['P', 'AH0', 'JH', 'AA1', 'M', 'AH0', 'Z'], ['P', 'AH0', 'JH', 'AE1', 'M', 'AH0', 'Z']], [['HH', 'IY1', 'R']]]
    >>> get_phrase_pronunciations(word_pronunciations)
    [['P', 'AH0', 'JH', 'AA1', 'M', 'AH0', 'Z', 'HH', 'IY1', 'R'], ['P', 'AH0', 'JH', 'AE1', 'M', 'AH0', 'Z', 'HH', 'IY1', 'R']]
    """
    combos = itertools.product(*word_pronunciations)

    def flatten_combo(combo):
        return [phoneme for word in combo for phoneme in word]

    result = list(map(flatten_combo, combos))
    return result


def part_to_phrases(partition: List[List[str]]) -> PhraseList:
    """
    Attempts to find words that correspond to given partitioning of a phrase.
    See example to perhaps make it clearer.

    Example
    -------
    >>> partition = [['P', 'AH0', 'JH', 'AA1', 'M', 'AH0', 'Z'], ['HH', 'IY1', 'R']]
    >>> part_to_phrase(partition)
    [['pajamas'], ['hear', 'here']]
    """
    word_pronunciations = []

    for word in partition:
        try:
            word_pronunciations.append(CMPD_INVERTED[tuple(word)])
        except KeyError:
            raise

    # Get every combination of word pronunciation sequences
    phrases = list(itertools.product(*word_pronunciations))

    # Convert all of these tuples into simple strings
    phrases = [' '.join(phrase) for phrase in phrases]

    return phrases


def get_phrases(phrase_pronunciations: PhrasePronunciationList) -> PhraseList:
    """
    Finally convert pronunciations of phrases back into english phrases consisting of words.
    """
    phrases = []

    print(
        f'Looking over {len(phrase_pronunciations)} different pronunciations of sentence...')
    for pronunciation in phrase_pronunciations:
        for part in partitions(pronunciation):
            try:
                phrases.extend(part_to_phrases(part))
            except KeyError:
                pass

    return phrases


def wordsmith(phrase: str) -> PhraseList:
    """
    Return a list of homophonous phrases, i.e. phrases whose phonetics match
    that of the given `phrase`.

    Example
    -------
    >>> wordsmith(phrase='Ice cream')
    Looking over 1 different pronunciations of sentence...
    32it [00:00, 62747.89it/s]
    ai scream
    ay scream
    aye scream
    eye scream
    i scream
    i. scream
    ice cream
    ice creme
    # Note that you don't necessarily get a word-for-word match. The result may
    # have more or less words if we find words 'blended' between multiple words
    # in original `phrase`.
    """
    phrase = phrase.lower()

    words = nltk.word_tokenize(phrase)
    word_pronunciations = get_word_pronunciations(words)
    phrase_pronunciations = get_phrase_pronunciations(word_pronunciations)
    phrases = get_phrases(phrase_pronunciations)

    return phrases


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find homopohonous phrases.')
    parser.add_argument('phrase', type=str, nargs=1)

    args = parser.parse_args()
    phrase = args.phrase[0]

    print(f'Finding phrases homophonous to {phrase}...\n')

    phrases = wordsmith(phrase)

    print('\nDone! See below:')
    for phrase in phrases:
        print(f'{phrase}')
