# -*- coding: utf-8 -*-
"""
Takes in a single title and provides three category options
"""
import cPickle as pickle
import os
from collections import defaultdict
import heapq
from utils.logger import logger
from data_prep.clean_titles import encode_string, tokenize_title_string, remove_words_list, remove_numeric_list, \
    remove_chars, STOP_WORDS, HTML_PARSER


def load_dict(dict_dir='categorize', dict_name='tfidf_dict'):
    """ (str, str) -> defaultdict

    Loads a dictionary for categorization into memory

    :param tfidf_dict:
    :param dict_dir:
    :param dict_name:
    :return:
    """
    output_dir_path = os.path.join(dict_dir, dict_name + '.pickle')

    with open(output_dir_path, 'rb') as handle:
        logger.info('Dictionary loading from: {}/{}.pickle'.format(dict_dir, dict_name))
        return pickle.load(handle)


# Load dictionaries
tfidf_dict, int_to_category_dict = load_dict('data/model', 'categorization_dicts_small')
logger.info('Dictionary loaded in categorized.categorize_single')


def merge_dicts(dicts, defaultdict=defaultdict, int=int):
    """ (list(dict), type, type) -> dict

    Returns a single dictionary given a list of dictionaries.
    Values with the same keys are summed and assigned to the key.

    :param dicts:
    :param defaultdict:
    :param int:
    :return:

    >>> merge_dicts([{'A': 1}, {'B': 2}])
    defaultdict(<type 'int'>, {'A': 1, 'B': 2})
    >>> merge_dicts([{'A': 1}, {'B': 2}, {'C': 3}, {'A': 10}])
    defaultdict(<type 'int'>, {'A': 11, 'C': 3, 'B': 2})
    """

    merged = defaultdict(int)
    for d in dicts:
        for k in d:
            merged[k] += d[k]

    return merged


def get_score(tokens, ngram_dict, int_to_category_dict, top_n):
    dict_list = []

    # get list of dictionaries based on tokens
    for token in tokens:
        try:
            dict_list.append(ngram_dict[token])
        except KeyError:
            pass

    # Merge list of dicts together and add values
    score = merge_dicts(dict_list)

    # Get top n regional ids based on score
    top_n_cats = heapq.nlargest(top_n, score, key=score.get)

    # Convert integers back to categories
    top_n_cats = [int_to_category_dict[idx] for idx in top_n_cats]

    return top_n_cats


class Title:

    def __init__(self, title):
        self.title = title

    def prepare(self, excluded='-.'):
        """ (str) -> list(str)

        Returns the title after it has been prepared by the process from clean titles

        :return:
        >>> Title('Crème brûlée &quot; &amp; &nbsp;').prepare()
        ['creme', 'brulee']
        >>> Title('test hyphen-word 0.9 20% green/blue').prepare()
        ['test', 'hyphen-word', '0.9']
        >>> Title('grapes come in purple and green').prepare()
        ['grapes', 'come']
        >>> Title('what remains of a word ! if wordlen is 2').prepare()
        ['remains', 'word', 'wordlen']
        """

        self.title = encode_string(self.title, HTML_PARSER)
        self.title = self.title.lower()
        self.title = tokenize_title_string(self.title, excluded)
        self.title = remove_words_list(self.title, STOP_WORDS)
        self.title = remove_numeric_list(self.title)
        self.title = remove_chars(self.title, 1)
        logger.info('Title after preparation: {}'.format(self.title))
        return self

    def categorize(self):
        """ (CategorizeSingle(str)) -> dict

        Categorizes prepared title and returns a dictionary of form {1: 'Cat1', 2: 'Cat2', 3: 'Cat3}

        :return:
        >>> Title('This is a bookshelf with wood and a clock').prepare().categorize()
        {1: 'Electronics -> Home Audio -> Stereo Components -> Speakers -> Bookshelf Speakers',
        2: 'Electronics -> Computers & Accessories -> Data Storage -> USB Flash Drives',
        3: 'Home & Kitchen -> Furniture -> Home Office Furniture -> Bookcases'}
        """

        result_list = get_score(self.title, tfidf_dict, int_to_category_dict, 3)
        result_dict = dict()
        for i, category in enumerate(result_list):
            result_dict[i + 1] = category

        return result_dict


def categorize_single(title):
    """ (str) -> dict

    Initializes given title as CategorizeSingle class and returns a dictionary of top 3 options

    :param title:
    :return:
    """
    return Title(title).prepare().categorize()
