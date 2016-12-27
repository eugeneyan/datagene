"""
Prepares dictionaries for looking up images to serve.
- index_path_dict: {Image index (in search features): Image path}
- category_index_dict: {Category: (Category index, count of images in category)}
- index_path_filter_dict: {Category index: {Image index (in category): Image path}}

python -m image_search.prep_search_dicts images_sample train_top_level
python -m image_search.prep_search_dicts images train_top_level
"""
import os
import cPickle as pickle
from collections import defaultdict
import sys
from utils.logger import logger
from utils.create_dir import create_dir

def create_index_path_dict(train_top_level_dir):
    """

    Returns a dictionary of each image's index mapped to each image's path.
    {Image index (in search features): Image path}

    :param train_top_level_dir:
    :return:
    """
    index_path_dict = defaultdict()
    index = 0

    for image_dir in os.listdir(train_top_level_dir):
        if not image_dir.startswith('.'):  # Remove .DS_Store
            image_names = os.listdir(os.path.join(train_top_level_dir, image_dir))

            for image_name in image_names:
                if not image_name.startswith('.'):  # Remove .DS_Store
                    image_path = os.path.join(train_top_level_dir, image_dir, image_name)
                    index_path_dict[index] = image_path
                    index += 1

    logger.info('Index path dictionary created with {} entries'.format(len(index_path_dict)))
    return index_path_dict


def create_category_index_dict(train_top_level_dir):
    """

    Returns a dictionary of each category's index and count of images
    {Category: (Category index, Count of images in category)}

    :param train_top_level_dir:
    :return:
    """
    category_index_dict = defaultdict()
    index = 0

    for image_dir in os.listdir(train_top_level_dir):
        if not image_dir.startswith('.'):
            image_names = os.listdir(os.path.join(train_top_level_dir, image_dir))
            image_count = len([img for img in image_names if not img.startswith('.')])

            category_index_dict[image_dir] = (index, image_count)
            index += 1

    logger.info('Category index dictionary created with {} entries'.format(len(category_index_dict)))
    return category_index_dict


def create_index_path_filter_dict(train_top_level_dir, category_index_dict):
    """

    Returns a dictionary, of dictionaries, of each image's index mapped to each image's path, where category
    index is the main dictionary's key
    {Category index: {Image index (in category): Image path}}

    :param train_top_level_dir:
    :param category_index_dict: Category Index dict to get index for each category
    :return:
    """
    index_path_filter_dict = defaultdict()

    for image_dir in os.listdir(train_top_level_dir):
        if not image_dir.startswith('.'):
            image_dir_index = category_index_dict[image_dir][0]

            index_path_filter_dict[image_dir_index] = defaultdict()
            image_index = 0

            image_names = os.listdir(os.path.join(train_top_level_dir, image_dir))

            for image_name in image_names:
                if not image_name.startswith('.'):
                    image_path = os.path.join(train_top_level_dir, image_dir, image_name)
                    index_path_filter_dict[image_dir_index][image_index] = image_path
                    image_index += 1

    logger.info('Index path filter dictionary created with {} entries'.format(len(index_path_filter_dict)))
    return index_path_filter_dict


def save_search_dicts(index_path_dict, category_index_dict, index_path_filter_dict, output_dir, output_name):
    """

    Saves search dictionaries into pickle format, in output dir with output name

    :param index_path_dict:
    :param category_index_dict:
    :param index_path_filter_dict:
    :param output_dir:
    :param output_name:
    :return:
    """
    output_path = os.path.join(output_dir, output_name + '.pickle')

    with open(output_path, 'wb') as handle:
        pickle.dump((index_path_dict, category_index_dict, index_path_filter_dict), handle, protocol=2)
        logger.info('Search dictionaries saved in {}'.format(output_path))


if __name__ == '__main__':

    main_dir = sys.argv[1]  # images_sample
    train_dir = sys.argv[2]  # train_top_level

    main_dir = os.path.join('data', main_dir)
    train_dir = os.path.join(main_dir, train_dir)
    output_dir = os.path.join(main_dir, 'search_dicts')
    output_name = 'search_dicts'

    # Create output directory
    create_dir(output_dir)

    # Create dictionaries
    index_path_dict = create_index_path_dict(train_dir)
    category_index_dict = create_category_index_dict(train_dir)
    index_path_filter_dict = create_index_path_filter_dict(train_dir, category_index_dict)

    # Save dictionaries
    save_search_dicts(index_path_dict, category_index_dict, index_path_filter_dict, output_dir, output_name)
