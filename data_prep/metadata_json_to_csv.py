"""
Reads zipped json data into a pandas dataframe and saves:
- Full dataframe in metadata.csv
- Dataframe with only title and category in metadata_categories_only.csv

python -m data_prep.metadata_json_to_csv
"""
import pandas as pd
import gzip
from utils.logger import logger


def parse(path):
    """
    (path) -> generator

    Parses path to gzip folder (containing json data) and returns a generator that yields each line of json\

    :param path: path to zipped json data
    :return: generator yielding each line of json
    """
    g = gzip.open(path, 'rb')
    for l in g:
        yield eval(l)


def get_df(path):
    """
    (path) -> pandas dataframe

    Parses path to gzip folder (containing json data) and returns pandas dataframe of json data

    :param path:
    :return: pandas dataframe containing json data
    """
    i = 0
    df = {}
    for d in parse(path):
        df[i] = d
        i += 1
        if i % 10000 == 0:
            logger.info('{} rows processed'.format(i))
    return pd.DataFrame.from_dict(df, orient='index')


if __name__ == '__main__':

    # Get pandas dataframe from metadata json zip file
    df = get_df('data/metadata.json.gz')
    logger.info('df created')

    # Save full data to csv
    df.to_csv('data/metadata.csv', index=False)
    logger.info('full df saved')

    # Save only title and categories to csv
    df = df[['title', 'categories']]
    df.to_csv('data/metadata_categories_only.csv', index=False)
    logger.info('category df saved')
