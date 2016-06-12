"""
Class for batch categorization of titles. Currently not implemented.
"""
from collections import defaultdict
import heapq
from utils.logger import logger


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


def get_score(tokens, ngram_dict, top_n):
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

    return top_n_cats


def get_top_n_score(scores, n):
    try:
        n_score = scores[n - 1]
    except IndexError:
        n_score = -1

    return n_score


def create_options(df, title, tfidf_dict):
    df['options'] = df.loc[:, title].apply(get_score, args=(tfidf_dict, 3,))
    logger.info('Test set scored')

    df['option1'] = df.loc[:, 'options'].apply(get_top_n_score, args=(1,))
    df['option2'] = df.loc[:, 'options'].apply(get_top_n_score, args=(2,))
    df['option3'] = df.loc[:, 'options'].apply(get_top_n_score, args=(3,))
    logger.info('Top 3 options created')
    return df


def validate_accuracy(df):
    df['option1_match'] = df['category_path'] == df['option1']
    df['option2_match'] = df['category_path'] == df['option2']
    df['option3_match'] = df['category_path'] == df['option3']

    score1 = df['option1_match'].sum() / float(len(df))
    score2 = df['option2_match'].sum() / float(len(df))
    score3 = df['option3_match'].sum() / float(len(df))
    score123 = score1 + score2 + score3

    print "Scores: {}, {}, {} ({})".format(score1, score2, score3, score123)
    return df