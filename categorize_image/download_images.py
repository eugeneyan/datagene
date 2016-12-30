"""
Download images into directories separated by categories

python -m image.download_images image_category data/images 0 1000000
"""
import pandas as pd
import urllib
import os
import sys
from utils.logger import logger


def download_images(df, output_dir, nthreads):
    """
    (DataFrame) -> Images separated by categories into directories

    Downloads images from imUrl provided and saves them into directories
    based on the product category.

    >>> download_images(df, output_dir):
    INFO: 1,000 images downloaded
    INFO: 2,000 images downloaded
    ...
    ...
    ...
    INFO: 20,000 images downloaded
    INFO: Image downloads complete!

    :param df: Dataframe containing product ID (asin), categorize_image url (imUrl), and category (category_path)
    :param output_dir: Directory path to where to store images (../data/images)
    """

    # Start downloader and writer thread
    for i, row in df.iterrows():
        product_id = row['asin']
        url = row['imUrl']
        category_path = row['category_path']
        # logger.info('Category: {}, URL: {}'.format(category_path, url))

        dir_path = '{}/{}'.format(output_dir, category_path)

        try:
            urllib.urlretrieve(url, '{}/{}.jpg'.format(dir_path, product_id))
        except IOError:  # If category_path directory has not been created yet
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            urllib.urlretrieve(url, '{}/{}.jpg'.format(dir_path, product_id))
        except AttributeError:  # If url cannot be processed
            continue

        if i % 100 == 0:
            logger.info('{:,} images downloaded'.format(i))

    logger.info('Image downloads complete!')


if __name__ == '__main__':
    data_dir = 'data'
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    start_row = int(sys.argv[3])
    end_row = int(sys.argv[4])

    input_file_path = os.path.join(data_dir, input_file + '.csv')

    # Read data
    df = pd.read_csv(input_file_path)
    df = df.iloc[start_row:end_row, :]

    # Download images
    download_images(df, output_dir)
