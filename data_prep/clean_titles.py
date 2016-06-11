# -*- coding: utf-8 -*-
"""
Takes in SKU titles and regional category and cleans them. Returns two sets of SKU titles and regional category:
- Csv of processed SKU titles and regional categories (where the same titles have same category)
- Csv of full and processed SKU titles and regional categories (where the same processed titles have different category)

Cleans SKUs titles by:
- Removing records with no category
- Encoding title as ascii
- Lowercase titles
- Tokenize title
- Exclude stop/spam wpords
- Exclude colours
- Removing characters where len = 1
- Remove duplicate words
- Remove empty titles

Sample call:
python -m data_prep.clean_titles data title_category
"""
import pandas as pd
import numpy as np
import regex as re
from nltk.corpus import stopwords
import unicodedata
import string
import sys
import os
import matplotlib
from utils.logger import logger
from utils.create_dir import create_output_dir


# Initialize stopwords
STOP_WORDS = set(stopwords.words('english'))
SPAM_WORDS = {'import', 'export', 'day', 'week', 'month', 'year', 'new', 'free', 'international', 'intl', 'oem', ''}
COLOURS = set(matplotlib.colors.cnames.keys())
STOP_WORDS = STOP_WORDS.union(SPAM_WORDS).union(COLOURS)


# Load data
def load_data(input_file_path, sku_id='id', category='category_path', title='title'):
    """ (str, str, str, str, str) -> DataFrame

    Returns a dataframe after loading data from csv.
    Reads sku_id, category, and title as string.

    :param csv_file_dir:
    :param csv_file:
    :param sku_id:
    :param category:
    :param title:
    :return:
    """

    logger.info('Reading file from: {}'.format(input_file_path))

    product_df = pd.read_csv(input_file_path, usecols=[sku_id, title, category],
                             dtype={sku_id: 'object', category: 'object', title: 'object'})

    logger.info('Columns in input file: %s', product_df.columns)
    logger.debug(product_df.head())

    # Keep only necessary columns
    product_df = product_df[[sku_id, title, category]]

    return product_df


def create_processed_column(product_df, title='title'):
    """ (DataFrame, str) -> DataFrame

    Returns a dataframe with an additional column for the processed title, with the '_processed' suffix.

    :param product_df:
    :param title:
    :return:
    """

    # Create new title name
    title_processed = title + '_processed'

    # create column for processed title
    product_df[title_processed] = product_df[title]
    return product_df


# Calculate purity
def purity(df, category='category_path', title='title_processed_str'):
    """ (DataFrame, str, str, str) -> float

    Calculate purity (proportion of SKUs that have the same title and same category / total number of SKUs)
    I.e., SKUs that have the same title but different category are impure (at least one is categorized wrongly) and
    should be excluded from product categorization model training

    :param df:
    :param category:
    :param title:
    :return:
    """

    # Group by title and category, and count number of skus
    title_cat_count_df = df.groupby([title, category])\
        .agg({title: 'count'}).rename(columns={title: 'title_count'}).reset_index()

    # Count number of unique categories each title has
    title_unique_cat_df = title_cat_count_df.groupby(title).agg({category: 'count'}).reset_index()

    # Keep titles that have multiple categories
    title_multi_cat_df = title_unique_cat_df[title_unique_cat_df[category] > 1]

    # Merge titles (with multiple categories) with titles (with counts) to get number of titles
    # potentially wrongly categorized
    title_multi_cat_count_df = title_multi_cat_df.merge(title_cat_count_df, how='left', on=title)

    # Count total number of SKUs
    total_sku_count = title_cat_count_df['title_count'].sum()

    # Count number of titles with differing categories (given the same title)
    multi_cat_sku_count = title_multi_cat_count_df['title_count'].sum()

    # Calculate purity
    purity_score = (total_sku_count - multi_cat_sku_count) / float(total_sku_count)

    return purity_score


# Convert list/set to string for calculating title_metrics
def list_to_string(title_tokens):
    """ (list(str)) -> str

    Returns a string of list(str) concatenated with ' '

    :param title_tokens:
    :return:

    >>> list_to_string(['A', 'B', 'C'])
    'A B C'
    >>> list_to_string(['A', 'B', ''])
    'A B '
    """

    return ' '.join(title_tokens)


# Compute title_metrics
def title_metrics(df, preparation_name='Some preparation run', category='category_path',
                  title_processed='title_processed'):
    """ (Dataframe, str, str, str, str) -> NoneType

    Prints title metrics (e.g., No. of unique titles, purity, etc) given a dataframe

    :param df:
    :param preparation_name:
    :param category:
    :param title_processed:
    :return:
    """

    logger.info('Preparation step completed: {}'.format(preparation_name))

    # Convert processed titles into string
    # At this stage, it may be a string or a list of tokens
    try:
        df['title_processed_str'] = df[title_processed].apply(list_to_string)
    except TypeError:  # if the title is still a string, leave it
        df['title_processed_str'] = df[title_processed]

    # Compute metrics
    title_count = len(df)
    unique_title_count = len(df['title_processed_str'].unique())
    unique_title_proportion = unique_title_count / float(title_count)
    unique_category_count = len(df[category].unique())
    purity_score = purity(df, category, 'title_processed_str')
    logger.info('Titles: {0}, Unique titles: {1}, Unique titles/Titles: {2:.2f}, Unique categories: {3}, Purity: {4}'
                .format(title_count, unique_title_count, unique_title_proportion, unique_category_count, purity_score))


# Remove records with no category form df
def remove_no_category(df, category='category_path'):
    """ (DataFrame, str) -> DataFrame

    Returns a dataframe where the missing categories have been dropped.

    :param df:
    :param category:
    :return:
    """

    df = df[df[category] != np.nan]
    return df


# Function to encode string
def encode_string(title):
    """ (str) -> str

    Returns a string that is encoded as ascii
    Note: While unicode(title, 'utf-8', 'ignore') seems to work correctly in doctest, it has led to errors in the past.
    If so, use iso-8859-1.

    :param title:
    :return:

    >>> encode_string('Crème brûlée')
    'Creme brulee'
    >>> encode_string('åöûëî')
    'aouei'
    """

    try:
        encoded_title = unicodedata.normalize('NFKD', unicode(title, 'utf-8', 'ignore')).encode('ascii', 'ignore')
    except TypeError:  # if title is missing and a float
        encoded_title = 'NA'

    return encoded_title


# Encode titles in df
def encode_title(df, title='title_processed'):
    """ (DataFrame, str) -> DataFrame

    Returns a dataframe where the title has been encoded.

    :param df:
    :param title:
    :return:
    """

    df[title] = df[title].apply(encode_string)
    logger.info('{} encoded'.format(title))
    return df


# Lowercase titles in df
def lowercase_title(df, title='title_processed'):
    """ (DataFrame, str) -> DataFrame

    Returns a dataframe where the title has been lowercased.

    :param df:
    :param title:
    :return:
    """

    df[title] = df[title].apply(string.lower)
    logger.info('{} lowercased'.format(title))
    return df


# Tokenize strings
def tokenize_title_string(title):
    """ (str) -> list(str)

    Returns a list of string tokens given a string.
    It will exclude the following characters from the tokenization: - / . %

    :param title:
    :return:

    >>> tokenize_title_string('hello world')
    ['hello', 'world']
    >>> tokenize_title_string('test hyphen-word 0.9 20% green/blue')
    ['test', 'hyphen-word', '0.9', '20%', 'green/blue']
    """

    return re.split("[^-/.%\w]+", title)


# Tokenize titles in df
def tokenize_title(df, title='title'):
    """ (DataFrame, str) -> DataFrame

    Returns a dataframe where the title has been tokenized based on function tokenize_title_string

    :param df:
    :param title:
    :return:
    """

    df[title] = df[title].apply(tokenize_title_string)
    logger.info('{} tokenized'.format(title))
    return df


# Remove stopwords from string
def remove_words(title, words_to_remove):
    """ (list(str), set) -> list(str)

    Returns a list of tokens where the stopwords/spam words/colours have been removed

    :param title:
    :param words_to_remove:
    :return:
    >>> remove_words(['python', 'is', 'the', 'best'], STOP_WORDS)
    ['python', 'best']
    >>> remove_words(['grapes', 'come', 'in', 'purple', 'and', 'green'], STOP_WORDS)
    ['grapes', 'come']
    >>> remove_words(['spammy', 'title', 'intl', 'buyincoins', 'export'], STOP_WORDS)
    ['spammy', 'title']
    """

    return [token for token in title if token not in words_to_remove]


# Remove stopwords from df
def remove_stopwords(df, stopwords, title='title_processed'):
    """ (DataFrame, set, str) -> DataFrame

    Returns a DataFrame where the stopwords have been removed from the titles

    :param df:
    :param stopwords:
    :param title:
    :return:
    """
    df[title] = df[title].apply(remove_words, args=(stopwords, ))
    logger.info('{} stopwords removed'.format(title))
    return df


# Remove words that are fully numeric
def remove_numeric(title):
    """ (list(str)) -> list(str)

    Remove words which are fully numeric

    :param title:
    :return:

    >>> remove_numeric(['A', 'B', '1', '123', 'C'])
    ['A', 'B', 'C']
    >>> remove_numeric(['1', '2', '3', '123'])
    []
    """

    return [token for token in title if not token.isdigit()]


# Remove words that are solely numeric from df
def remove_numeric_from_df(df, title='title_processed'):
    df[title] = df[title].apply(remove_numeric)
    logger.info('{} solely numeric words removed'.format(title))
    return df


# Remove words with character count below threshold from string
def remove_chars(title, word_len=1):
    """ (list(str), int) -> list(str)

    Returns a list of str (tokenized titles) where tokens of character length =< word_len is removed.

    :param title:
    :param word_len:
    :return:

    >>> remove_chars(['what', 'remains', 'of', 'a', 'word', '!', ''], 1)
    ['what', 'remains', 'of', 'word']
    >>> remove_chars(['what', 'remains', 'of', 'a', 'word', '!', '', 'if', 'word_len', 'is', '2'], 2)
    ['what', 'remains', 'word', 'word_len']
    """

    return [token for token in title if len(token) > word_len]



# Remove words that have words == 1 char from title
def remove_one_char_words(df, word_len=1, title='title_processed'):
    """ (DataFrame, int, str) -> DataFrame

    Returns a DataFrame where tokens of character length <= word_len is removed

    :param df:
    :param word_len:
    :param title:
    :return:
    """

    df[title] = df[title].apply(remove_chars, args=(word_len, ))
    logger.info('{} tokens with char length equals {} removed'.format(title, word_len))
    return df


# Remove duplicate words from string(title)
def remove_duplicate_words(title):
    """ (list(str)) -> set(str)

    Returns a set of str, given a list of str, where duplicate strs are removed

    :param title:
    :return:
    >>> remove_duplicate_words(['A', 'B', 'A', 'C'])
    set(['A', 'C', 'B'])
    >>> remove_duplicate_words(['A', 'B', 'B', 'C', 'C', 'D', 'D'])
    set(['A', 'C', 'B', 'D'])
    """

    return set(title)


# Remove duplicate words in titles in df
def remove_duplicates(df, title='title_processed'):
    """ (DataFrame, str) -> DataFrame

    Returns a DataFrame where duplicate words in titles are removed

    :param df:
    :param title:
    :return:
    """

    df[title] = df[title].apply(remove_duplicate_words)
    return df


# Count number of tokens in title
def title_token_count(title):
    """ (lst(str)) -> int

    Returns the number of tokens in the title.

    :param title:
    :return:
    >>> title_token_count(['A', 'B', 'C'])
    3
    >>> title_token_count([])
    0
    """
    return len(title)


# Remove titles that are empty
def remove_empty_titles(df, title='title_processed'):
    """ (DataFrame, str) -> DataFrame

    Returns a DataFrame where titles with zero tokens remaining are excluded

    :param df:
    :param title:
    :return:
    """
    df['title_len'] = df[title].apply(title_token_count)
    df = df[df['title_len'] > 0]
    return df


# Split into keep and discard df
def split_to_keep_and_discard(df, title='title_processed_str', category='category_path'):
    """ (DataFrame, str, str, str) -> DataFrame, DataFrame

    Returns two DataFrames given a DataFrame:
    - keep_df: Where titles that have identical titles after cleaning all have the same category
    - remove_df: Where titles that have identical titles after cleaning have more than 1 category (i.e., unclean)

    :param df:
    :param title:
    :param category:
    :return:
    """

    # Count number of unique categories for each processed title
    cat_count_df = pd.DataFrame(df.groupby(title)[category].apply(lambda x: len(x.unique()))).reset_index()
    cat_count_df.rename(columns={category: 'category_count'}, inplace=True)

    # Count number of skus for each processed title
    sku_count_df = df.groupby(title).agg({title: 'count'}).rename(columns={title: 'sku_count'}).reset_index()

    # Merge in counts of category and sku
    df = df.merge(cat_count_df, how='left', left_on=title, right_on=title)\
         .merge(sku_count_df, how='left', left_on=title, right_on=title)

    # Split into df for keeping and discarding, and sort
    discard_df = df[df['category_count'] > 1]
    keep_df = df[df['category_count'] == 1]

    discard_df = discard_df.sort_values(by=title)
    keep_df = keep_df.sort_values(by=title)

    # Add impurity count for discard_df
    discard_df['impurity'] = discard_df['category_count'] / discard_df['sku_count']

    logger.info('Split into keep and discard')
    logger.info('Size of keep: {} | Size of discard: {}'.format(keep_df.shape[0], discard_df.shape[0]))
    return keep_df, discard_df


def save_keep_and_discard(keep_df, discard_df, data_dir, input_file):
    """ (DataFrame, DataFrame, str, str) -> NoneType

    Saves the 'keep' and 'discard' DataFrame to csv

    :param keep_df:
    :param discard_df:
    :param csv_file_dir:
    :param csv_file:
    :return:
    """

    # read output and check if empty; if not empty, use last sku processed
    output_dir_path = os.path.join(data_dir, 'output')
    logger.info(output_dir_path)

    keep_file = os.path.basename(input_file + '_keep.csv')
    keep_file_path = os.path.join(output_dir_path, keep_file)

    discard_file = os.path.basename(input_file + '_discard.csv')
    discard_file_path = os.path.join(output_dir_path, discard_file)

    # Create output directory
    create_output_dir(data_dir)

    keep_df.to_csv(keep_file_path, index=False)
    discard_df.to_csv(discard_file_path, index=False)
    logger.info('Keep and discard saved to csv here: {}'.format(output_dir_path))


if __name__ == '__main__':

    data_dir = sys.argv[1]
    input_file = sys.argv[2]
    input_path = os.path.join(data_dir, input_file + '.csv')
    title_col = 'title'
    category_col = 'category_path'

    # Load data
    df = load_data(input_path, sku_id='asin')
    df = create_processed_column(df, title=title_col)
    title_metrics(df, 'Data loaded')

    # Remove records with no category
    df = remove_no_category(df, category=category_col)
    title_metrics(df, 'Remove records with no category')

    # Encode title as ascii
    df = encode_title(df, title='title_processed')
    title_metrics(df, 'Encode title as ascii')

    # Lowercase title
    df = lowercase_title(df, title='title_processed')
    title_metrics(df, 'Lowercase titles')

    # Tokenize title
    df = tokenize_title(df, title='title_processed')
    title_metrics(df, 'Tokenize titles')

    # Remove stopwords (includes spam, colours)
    df = remove_stopwords(df, stopwords=STOP_WORDS, title='title_processed')
    title_metrics(df, 'Remove stopwords')

    # Remove words that are solely numeric
    df = remove_numeric_from_df(df, title='title_processed')
    title_metrics(df, 'Remove numerics')

    # Remove words with character length == 1
    df = remove_one_char_words(df, word_len=1, title='title_processed')
    title_metrics(df, 'Remove words with character length == 1')

    # Remove duplicate words in title
    df = remove_duplicates(df, title='title_processed')
    title_metrics(df, 'Remove duplicate words and ignore order')

    # Remove titles that are empty
    df = remove_empty_titles(df, title='title_processed')
    title_metrics(df, 'Remove empty titles')

    # Split into keep and discard
    keep_df, discard_df = split_to_keep_and_discard(df, title='title_processed_str', category=category_col)

    # Save to output directory in csv format
    save_keep_and_discard(keep_df, discard_df, data_dir, input_file)
