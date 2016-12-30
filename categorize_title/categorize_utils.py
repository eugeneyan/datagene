"""
Utilities for use in categorized single and categorize batch
"""
import pickle
import heapq
from collections import defaultdict
import os
from utils.logger import logger


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
    """

    Returns top n categories given a list of tokens (from product title).

    :param tokens:
    :param ngram_dict:
    :param int_to_category_dict:
    :param top_n:
    :return:
    """
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


def get_top_n_score(scores, n):
    """

    Returns the nth category option from the top 3 category options.

    :param scores:
    :param n:
    :return:
    """
    try:
        n_score = scores[n - 1]
    except IndexError:
        n_score = -1

    return n_score
