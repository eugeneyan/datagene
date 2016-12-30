"""
Prepares the image directory for image search by:
- Copying all images from the train dir and sub dir into a single folder

python -m image_search.prep_image_dir images
"""
import os
import sys
import shutil
from utils.logger import logger


# Copy images from directory and sub directories into a single new directory.
# Used for ease of serving images for categorize_image search
# NOT USED
def copy_to_single_dir(current_dir, new_dir):
    """

    Copies all images from current dir and sub dir into a single new dir

    :param current_dir:
    :param new_dir:
    :return:
    """
    images_copied = 0

    for image_dir in os.listdir(current_dir):
        if not image_dir.startswith('.'):
            image_paths = os.listdir(os.path.join(current_dir, image_dir))
            image_count = len(image_paths)

            logger.info('{}: {} being copied'.format(image_dir, image_count))

            for image in image_paths:
                if not image.startswith('.'):
                    original_image_path = os.path.join(current_dir, image_dir, image)
                    new_image_path = os.path.join(new_dir, image)
                    shutil.copy(original_image_path, new_image_path)

            images_copied += image_count
            logger.info('{} images copied so far'.format(images_copied))


def create_top_level_dir(train_dir, train_top_level_dir):
    top_level_dict = dict()

    for image_dir in os.listdir(train_dir):
        if not image_dir.startswith('.'):
            top_level_category = image_dir.split('->')[0].strip()
            try:
                top_level_dict[top_level_category] += 1
            except:
                top_level_dict[top_level_category] = 1

    for top_level_category in top_level_dict.keys():
        try:
            os.makedirs(os.path.join(train_top_level_dir, top_level_category))
        except OSError:
            logger.info('{} already exists in {}'.format(top_level_category, train_top_level_dir))


def copy_to_top_level_dir(train_dir, train_top_level_dir):
    images_copied = 0

    for image_dir in os.listdir(train_dir):
        if not image_dir.startswith('.'):
            image_paths = os.listdir(os.path.join(train_dir, image_dir))
            image_paths = [image_path for image_path in image_paths if not image_path.startswith('.')]
            image_count = len(image_paths)
            top_level_image_dir = image_dir.split('->')[0].strip()

            logger.info('{}: {} being copied'.format(image_dir, image_count))

            for image in image_paths:
                if not image.startswith('.'):
                    original_image_path = os.path.join(train_dir, image_dir, image)
                    new_image_path = os.path.join(train_top_level_dir, top_level_image_dir, image)
                    shutil.copy(original_image_path, new_image_path)

            images_copied += image_count
            logger.info('{} images copied so far'.format(images_copied))


if __name__ == '__main__':
    main_dir = sys.argv[1]

    train_dir = os.path.join('data', main_dir, 'train')
    train_top_level_dir = os.path.join('data', main_dir, 'train_top_level')

    create_top_level_dir(train_dir, train_top_level_dir)
    copy_to_top_level_dir(train_dir, train_top_level_dir)
