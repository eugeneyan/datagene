"""
Prepares title and category data by:
- Extracting category level 1
- Excluding categories we're not interested in
- Extracting category paths

python -m data_prep.prep_title_category
"""
import pandas as pd
from utils.logger import logger


def get_category_lvl1(category_path_list):
    """
    (Str of list of list(s)) -> str

    Returns the top level category given a string of a list of lists of categories.
    If there are more than one list of categories provided, returns the top level category from the first list.

    >>> get_category_lvl1("[['A', 'B', 'C'], ['D', 'E', 'F', 'G']]")
    'A'
    >>> get_category_lvl1("[['P1', 'P2', 'P3', 'P4']]")
    'P1'
    >>> get_category_lvl1("[['']]")
    ''

    :type category_path_list: str
    :param category_path_list: A string containing a list of at least one list of categories
    :return: A string showing the full category path of the FIRST category in the list (assumed to be primary category)
    """
    try:
        return eval(category_path_list)[0][0]
    except IndexError:
        return 'no_category'
    except TypeError:
        return 'no_category'


def get_category_path(category_path_list):
    """
    (Str of list of list(s)) -> str

    Returns the category path given a string of list of lists of categories.
    If there are more than one list of categories provided, returns the category path from the first list.

    >>> get_category_path("[['A', 'B', 'C'], ['D', 'E', 'F', 'G']]")
    'A -> B -> C'
    >>> get_category_path("[['P1', 'P2', 'P3', 'P4']]")
    'P1 -> P2 -> P3 -> P4'

    :type category_path_list: str
    :param category_path_list: A string containing a list of at least one list of categories
    :return: A string showing the full category path of the FIRST category in the list (assumed to be primary category)
    """
    try:
        return ' -> '.join(eval(category_path_list)[0])
    except IndexError:
        return 'no_category'
    except TypeError:
        return 'no_category'


if __name__ == '__main__':

    # Read data
    df = pd.read_csv('data/metadata_categories_only.csv', )
    logger.info('No. of rows in data: {}'.format(df.shape[0]))

    # Drop rows where title is missing
    df.dropna(how='any', inplace=True)
    logger.info('No. of rows after dropping columns with missing values: {}'.format(df.shape[0]))

    # Create df of category counts
    category_df = df.groupby('category_lvl1').agg({'title': 'count'})\
        .sort_values(by='title', ascending=False).reset_index()

    # # Keep categories where the count of titles > 1500
    category_df = category_df[category_df['title'] > 1500]

    # # Keep only rows where the category is in category_df
    df = df[df['category_lvl1'].isin(category_df['category_lvl1'])]
    logger.info('No. of rows after dropping categories where count < 1500: {}'.format(df.shape[0]))

    # Create column for category
    df['category_lvl1'] = df['categories'].apply(get_category_lvl1)
    logger.info('Category level 1 created')

    # Drop columns that have no category data
    df = df[df['category_lvl1'] != '']
    logger.info('No. of rows after dropping columns with no category data: {}'.format(df.shape[0]))

    # Create column for category path
    df['category_path'] = df['categories'].apply(get_category_path)
    logger.info('Category path created')

    # Create df of category path counts
    category_path_df = df.groupby('category_path').agg({'title': 'count'})\
        .sort_values(by='title', ascending=False).reset_index()

    # Drop category_paths where the count of titles < 10
    category_path_df = category_path_df[category_path_df['title'] >= 10]

    # Keep only rows where the category is in category_df
    df = df[df['category_path'].isin(category_path_df['category_path'])]
    logger.info('No. of rows after dropping category_paths where count < 10: {}'.format(df.shape[0]))

    # Save prepared title and category data to csv
    df.drop(labels='categories', axis=1, inplace=True)
    df.to_csv('data/title_category.csv', index=False)
