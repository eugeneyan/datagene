"""
Takes in a csv of titles (and optionally, sku_id and regional_key) and provides three category options.

Sample call on local:
python -m categorize.categorize_batch 2016-07-04 TH
"""
import sys
import os
from data_prep.clean_titles import load_data, encode_title, lowercase_title, tokenize_title, \
    remove_stopwords, remove_numeric, remove_one_char_words, STOP_WORDS, HTML_PARSER
from categorize.build_dict import create_ngram
from categorize.categorize_utils import load_dict, get_score, get_top_n_score
from utils.create_dir import create_dir
from utils.logger import logger


def create_options(df, title, tfidf_dict):
    df['options'] = df[title].apply(get_score, args=(tfidf_dict, 3, ))
    df['option1'] = df['options'].apply(get_top_n_score, args=(1, ))
    df['option2'] = df['options'].apply(get_top_n_score, args=(2, ))
    df['option3'] = df['options'].apply(get_top_n_score, args=(3, ))
    logger.info('Top 3 options created')
    return df


def save_results(df, output_dir, country):

    # create recategorized directory path
    recategorized_file = os.path.basename('product_{}_recategorized.csv'.format(country))
    recategorized_file_path = os.path.join(output_dir, recategorized_file)

    # Create output directory
    create_dir(output_dir)

    # Drop unnecessary columns
    df.drop(labels=['title', 'options'], axis=1, inplace=True)

    # Save to csv
    df.to_csv(recategorized_file_path, index=False)
    logger.info('Recategorized file save to csv here: {}'.format(output_dir))


if __name__ == '__main__':

    date = sys.argv[1]
    country = sys.argv[2]
    input_path = os.path.join('data/{}/product'.format(date), 'product_{}'.format(country) + '.csv')
    output_dir = os.path.join('data/{}/product/recategorized'.format(date))
    title_col = 'title'
    category_col = 'regional_key'

    # Load csv file
    df = load_data(input_path)
    logger.info('Data loaded')
    logger.debug(df.head())

    # Encode title as ascii
    df = encode_title(df, title='title', parser=HTML_PARSER)
    logger.info('Title encoded')
    logger.debug(df.head())

    # Lowercase title
    df = lowercase_title(df, title='title')
    logger.info('Title lowercased')
    logger.debug(df.head())

    # Tokenize title
    df = tokenize_title(df, title='title', excluded="-.'")
    logger.info('Title tokenize')

    # Remove stopwords (includes spam, colours)
    df = remove_stopwords(df, stopwords=STOP_WORDS, title='title')
    logger.info('Title stopwords removed')
    logger.debug(df.head())

    # Remove words that are solely numeric
    df = remove_numeric(df, title='title')
    logger.info('Title numerics removed')
    logger.debug(df.head())

    # Remove words with character length == 1
    df = remove_one_char_words(df, word_len=1, title='title')
    logger.info('Title one char words removed')
    logger.debug(df.head())

    # Create ngrams for titles
    df = create_ngram(df, title='title')
    logger.info('Title ngrams created')
    logger.debug(df.head())

    # Load dictionary
    tfidf_dict, regional_to_path_dict = load_dict('data/{}/model'.format(date), 'categorization_dict_{}'.format(country))
    logger.info('Dictionary loaded')

    # Create options
    df = create_options(df, title='title', tfidf_dict=tfidf_dict)
    logger.info('Category options created')

    # Save to csv
    save_results(df, output_dir, country)
