"""
Prepares title and category data by:
- Extracting category level 1
- Excluding categories we're not interested in
- Extracting category paths

python -m data_prep.prep_image_category metadata_images image_category
"""
import pandas as pd
import sys
import os
from sklearn.cross_validation import train_test_split
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
    except IndexError:  # Error if the outer list is empty
        return 'no_category'
    except TypeError:  # Error if the outer list is missing
        return 'no_category'


if __name__ == '__main__':

    data_dir = 'data'
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    selected_category_file = 'categories_to_keep'
    input_file_path = os.path.join(data_dir, input_file + '.csv')
    output_file_path = os.path.join(data_dir, output_file + '.csv')
    output_category_file_path = os.path.join(data_dir, 'categories_available' + '.csv')
    selected_category_file_path = os.path.join(data_dir, selected_category_file + '.csv')

    # Read data
    df = pd.read_csv(input_file_path)
    logger.info('No. of rows in data: {}'.format(df.shape[0]))
    logger.info(df.columns)

    # Read selected_category_file
    filter_df = pd.read_csv(selected_category_file_path)
    logger.info('No. of categories in selected_category_file_path: {}'.format(filter_df.shape[0]))

    # Drop rows where title is missing
    df.dropna(how='any', inplace=True)
    logger.info('No. of rows after dropping columns with missing values: {}'.format(df.shape[0]))

    # Create column for category
    df['category_lvl1'] = df['categories'].apply(get_category_lvl1)
    logger.info('Category level 1 created')

    # Drop columns that have no category data
    df = df[df['category_lvl1'] != 'no_category']
    logger.info('No. of products after dropping columns with no category data: {}'.format(df.shape[0]))

    # Create df of category counts
    category_df = df.groupby('category_lvl1').agg({'asin': 'count'})\
        .sort_values(by='asin', ascending=False).reset_index()

    # Exclude categories where titles are not indicative of category
    category_df = category_df[category_df['category_lvl1'] != 'Books']
    category_df = category_df[category_df['category_lvl1'] != 'CDs & Vinyl']
    category_df = category_df[category_df['category_lvl1'] != 'Movies & TV']

    # Exclude some other categories to make data smaller
    category_df = category_df[category_df['category_lvl1'] != 'Musical Instruments']
    category_df = category_df[category_df['category_lvl1'] != 'Amazon Fashion']
    category_df = category_df[category_df['category_lvl1'] != 'All Electronics']
    category_df = category_df[category_df['category_lvl1'] != 'All Beauty']
    category_df = category_df[category_df['category_lvl1'] != 'Collectibles & Fine Art']

    # # Keep only rows where the category is in category_df
    df = df[df['category_lvl1'].isin(category_df['category_lvl1'])]
    logger.info('No. of products after dropping certain top level categories: {}'.format(df.shape[0]))

    # Create column for category path
    df['category_path'] = df['categories'].apply(get_category_path)
    logger.info('Category path created')

    # Create df of category path counts
    category_path_df = df.groupby('category_path').agg({'asin': 'count'})\
        .sort_values(by='asin', ascending=False).reset_index()

    # Exclude category paths where category_path is at top level
    category_path_df = category_path_df[category_path_df['category_path'].str.contains('->')]
    logger.info('No. of category_paths after excluding top level categories: {}'.format(category_path_df.shape[0]))

    # Drop category_paths where the count of products > 1000
    category_path_df = category_path_df[category_path_df['asin'] >= 1000]  # We need a lot of image data
    logger.info('No. of category_paths after excluding those with < 1000 products: {}'.format(category_path_df.shape[
                                                                                                  0]))
    # Exclude categories that are not deepest category
    category_path_df.sort_values(by='category_path', inplace=True)
    category_path_df['category_path_next'] = category_path_df['category_path'].shift(-1)
    category_path_df.fillna('no_comparison', inplace=True)

    # Create list of category_paths which are deepest category
    category_path_list = []
    for i, value in category_path_df.iterrows():
        category_path = value['category_path']
        category_path_next = value['category_path_next']
        if category_path not in category_path_next:
            category_path_list.append(category_path)

    # Create df of category_path
    category_path_df = pd.DataFrame(category_path_list, columns=['category_path'])
    logger.info('No. of category_paths at deepest category: {}'.format(category_path_df.shape[0]))

    # Keep only rows where category in filter_df (only specific to Amazon data)
    category_path_df = category_path_df.merge(filter_df, how='inner', left_on='category_path', right_on='category_path')
    category_path_df.dropna(inplace=True)
    logger.info('No. of categories after excluding categories based on categories_to_keep.csv: {}'.format(
        category_path_df.shape[0]))

    # Keep only rows where the category is in category_df
    df = df[df['category_path'].isin(category_path_df['category_path'])]
    logger.info('No. of rows in deepest category: {}'.format(df.shape[0]))

    # Count number of products in each category path
    category_counts = df[['category_path', 'asin']].groupby('category_path').count().sort_values(by='asin',
                                                                                  ascending=False).reset_index()
    category_counts.rename(columns={'asin': 'count'}, inplace=True)

    # # Keep only rows where category in filter_df (only specific to Amazon data)
    # df = df.merge(filter_df, how='inner', left_on='category_path', right_on='category_path')
    # df.dropna(inplace=True)
    # logger.info('No. of rows after excluding categories based on categories_to_keep.csv: {}'.format(df.shape[0]))

    # # Sample and only keep 33% of data (to keep the data small)
    # df, discard = train_test_split(df, train_size=0.33, stratify=df['category_path'], random_state=1368)
    # logger.info('No. of rows in after taking 50% sample: {}'.format(df.shape[0]))

    # Take only the 1000 products from each category path to keep training fast
    # df = df.groupby('category_path').head(1000).reset_index(drop=True)
    # logger.info('No. of rows after taking top 1000 products: {}'.format(df.shape[0]))

    # Save prepared asin and category data to csv
    df.drop(labels='categories', axis=1, inplace=True)
    df.to_csv(output_file_path, index=False)
    logger.info(df.columns)

    # Save category_path_df which contains all category paths in data
    # category_path_df.to_csv(output_category_file_path, index=False)
    category_counts.to_csv(output_category_file_path, index=False)
