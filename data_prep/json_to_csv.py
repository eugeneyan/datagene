"""
Reads zipped json data into a pandas dataframe and saves:
- Full dataframe in metadata.csv
- Dataframe with only title and category in metadata_categories_only.csv

python -m data_prep.json_to_csv data metadata
"""
import pandas as pd
import gzip
import sys
import os
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
    df_dict = {}
    for d in parse(path):
        df_dict[i] = d
        i += 1
        if i % 10000 == 0:
            logger.info('{} rows processed'.format(i))
    return pd.DataFrame.from_dict(df_dict, orient='index')


if __name__ == '__main__':

    data_dir = sys.argv[1]
    json_file = sys.argv[2]
    csv_path = os.path.join(data_dir, json_file + '.csv')
    csv_categories_path = os.path.join(data_dir, json_file + '_categories_only.csv')

    # Get pandas dataframe from metadata json zip file
    df = get_df(os.path.join(data_dir, json_file + '.json.gz'))
    logger.info('df created')

    # Save full data to csv
    df.to_csv(csv_path, index=False)
    logger.info('full df saved')

    # Save only title and categories to csv
    df = df[['asin', 'title', 'categories']]
    df.to_csv(csv_categories_path, index=False)
    logger.info('category df saved')
