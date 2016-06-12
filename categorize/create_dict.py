"""
Takes in titles and category data, cleans them, and creates a dictionary model to categorize products based on title.
Returns dictionary model in pickle format.

Cleans and prepares titles via the same approach in data_prep.clean titles

Sample call:
python -m categorize.create_dict data/output title_category_keep_samp tfidf_dict
"""
import pandas as pandas
import math
import os
import sys
import cPickle as pickle
from collections import defaultdict
from data_prep.clean_titles import load_data, remove_no_category, encode_title, lowercase_title, tokenize_title, \
    remove_stopwords, remove_numeric, remove_one_char_words, remove_empty_titles, STOP_WORDS
from utils.logger import logger


def find_ngrams(input_list, n):
    """ list, int -> list(tuples)

    Return a list of ngram tuples, where each tuple contains n unigrams

    :param input_list:
    :param n:
    :return:
    >>> find_ngrams(['A', 'B', 'C', 'D'], 2)
    [('A', 'B'), ('B', 'C'), ('C', 'D')]
    >>> find_ngrams(['A', 'B', 'C', 'D'], 3)
    [('A', 'B', 'C'), ('B', 'C', 'D')]
    """
    return zip(*[input_list[i:] for i in range(n)])


def create_ngram_from_tokens(tokens):
    """ list(str) -> list(str)

    Returns a list of ngram strings from a list of ngram tokens

    :param tokens:
    :return:
    >>> create_ngram_from_tokens(['A', 'B', 'C', 'D'])
    ['A', 'B', 'C', 'D', 'A_B', 'B_C', 'C_D', 'A_B_C', 'B_C_D']
    """

    bigram_list = find_ngrams(tokens, 2)
    trigram_list = find_ngrams(tokens, 3)

    bigrams = [tuple[0] + '_' + tuple[1] for tuple in bigram_list]
    trigrams = [tuple[0] + '_' + tuple[1] + '_' + tuple[2] for tuple in trigram_list]

    ngram_list = tokens + bigrams + trigrams
    return ngram_list


def create_ngram(df, title='title'):
    """ (DataFrame) -> DataFrame

    Returns a DataFrame where the title is converted from str to ngrams

    :param df:
    :param title:
    :return:
    """

    df[title] = df[title].apply(create_ngram_from_tokens)
    logger.info('{}: ngrams created'.format(title))
    return df


def create_tfidf_dict(train, title='title', category='regional_key'):
    """ (DataFrame, str, str) -> defaultdict

    Returns a tf-idf dict given a dataframe containing title and regional_key

    :param train:
    :param title:
    :param category:
    :return:
    """

    # Create tf dictionary (though the name is tfidf, it's only tf for now)
    ngram_dict_tfidf = defaultdict()

    # For each token in the titles, create a dict as its value
    for i, row in train.iterrows():
        tokens = row[title]
        for token in tokens:
            ngram_dict_tfidf[token] = defaultdict()

    logger.info('TF dict phase 1 done')

    # For each token in the titles, add the token frequency to the value of the token key
    # Token frequency = token count / total number of tokens in title
    for i, row in train.iterrows():
        tokens = row[title]
        regional_id = row[category]
        for token in tokens:
            token_tf = tokens.count(token) / float(len(tokens))
            try:
                ngram_dict_tfidf[token][regional_id] += token_tf
            except KeyError:
                ngram_dict_tfidf[token][regional_id] = token_tf

    logger.info('TF dict phase 2 done')

    # create idf dictionary and count the number of titles in train
    ngram_dict_idf = defaultdict()
    no_of_skus = len(train)

    # For each token in the title, add one to the value of the token key
    for i, row in train.iterrows():
        tokens = set(row[title])
        for token in tokens:
            try:
                ngram_dict_idf[token] += 1
            except KeyError:
                ngram_dict_idf[token] = 1

    # For each token in idf dict, divide the total number of skus (logged) by the count of token value
    # Add 1 to the numerator to prevent zero divison error
    for term, count in ngram_dict_idf.iteritems():
        ngram_dict_idf[term] = math.log(no_of_skus) / float(1 + count)

    logger.info('IDF dict done')

    # Multiple values in tf dictionary with idf dictionary to get tf-idf dictionary
    for ngram, cat_dict in ngram_dict_tfidf.iteritems():
        # print ngram
        ngram_idf = ngram_dict_idf[ngram]
        # print ngram_idf
        for regional_key, count in cat_dict.iteritems():
            ngram_dict_tfidf[ngram][regional_key] = count * ngram_idf

    logger.info('TF-IDF dict done')
    return ngram_dict_tfidf


def save_dict(tfidf_dict, output_dir, output_name):
    """ (defaultdict, str, str) -> NoneType

    Saves the dictionary (tfidf_dict) into pickle format

    :param tfidf_dict:
    :param output_dir:
    :param output_name:
    :return:
    """
    output_dir_path = os.path.join(output_dir, output_name + '.pickle')

    with open(output_dir_path, 'wb') as handle:
        pickle.dump(tfidf_dict, handle, protocol=2)
        logger.info('Dict saved in {}'.format(output_dir_path))


if __name__ == '__main__':

    data_dir = sys.argv[1]
    input_file = sys.argv[2]
    output_dict_name = sys.argv[3]
    input_path = os.path.join(data_dir, input_file + '.csv')
    title_col = 'title'
    category_col = 'category_path'

    # Load data
    df = load_data(input_path, sku_id='asin')

    # Remove records with no category
    df = remove_no_category(df, category=category_col)

    # Encode title as ascii
    df = encode_title(df, title='title')

    # Lowercase title
    df = lowercase_title(df, title='title')

    # Tokenize title
    df = tokenize_title(df, title='title', excluded='-.')

    # Remove stopwords (includes spam, colours)
    df = remove_stopwords(df, stopwords=STOP_WORDS, title='title')

    # Remove words that are solely numeric
    df = remove_numeric(df, title='title')

    # Remove words with character length == 1
    df = remove_one_char_words(df, word_len=1, title='title')

    # Remove titles that are empty
    df = remove_empty_titles(df, title='title')

    # Create ngrams for titles
    df = create_ngram(df, title='title')

    # Create tf-idf model dictionary
    tfidf_dict = create_tfidf_dict(df, title='title', category='category_path')

    # Save dict to pickle file
    save_dict(tfidf_dict, data_dir, output_dict_name)
