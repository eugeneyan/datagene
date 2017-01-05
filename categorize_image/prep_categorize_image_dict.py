"""
Creates image categorization dicts {0: Image category} and save to directory

python -m categorize_image.prep_categorize_image_dict images_clothes
"""

import os
import pickle
import sys
from utils.create_dir import create_dir
from utils.logger import logger


# Create dictionary mapping index to category path {0: Belts, 1: Shoes, ...}
def create_category_dict(train_dir):
    categories = os.listdir(train_dir)

    # Initialize category dict
    category_dict = dict()
    idx = 0
    for category in categories:
        if not category.startswith('.'):
            category_dict[idx] = category
            idx += 1

    return category_dict


# Save category dict as pickle
def save_dict(image_category_dict, output_dir, output_name):
    """ (defaultdict, dict, str, str) -> NoneType

    Saves the dictionaries (tfidf_dict, int_to_category_dict) into pickle format

    :param tfidf_dict:
    :param int_to_category_dict:
    :param output_dir:
    :param output_name:
    :return:
    """
    output_dir_path = os.path.join(output_dir, output_name + '.pickle')

    with open(output_dir_path, 'wb') as handle:
        pickle.dump(image_category_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        logger.info('Dict saved in {}'.format(output_dir_path))


if __name__ == '__main__':

    main_dir = sys.argv[1]  # images_clothes
    try:
        dataset = sys.argv[2]
        dataset = '_' + dataset
    except IndexError:
        dataset = ''

    train = 'train' + dataset
    train_dir = os.path.join('data', main_dir, train)
    output_dir = os.path.join('data', main_dir, 'image_categorize_dicts')
    output_name = 'image_categorize_dicts'
    create_dir(output_dir)

    # Create category dict
    image_category_dict = create_category_dict(train_dir)

    # Save category dict
    save_dict(image_category_dict, output_dir, output_name)
