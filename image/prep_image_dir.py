"""
Prepares images by:
- Discarding images below threshold size
- Creating subset of images for POC
- Splitting images into train and test

python -m image.prep_image_dir images_clothes
"""
import os
import shutil
import sys
from utils.logger import logger


# Create new directory structure to directory
def mirror_dir_structure(current_dir, new_dir):
    for image_dir in os.listdir(current_dir):
        if not image_dir.startswith('.'):
            try:
                os.makedirs(os.path.join(new_dir, image_dir))
            except OSError:
                print '{} already exists in {}'.format(image_dir, new_dir)


# Discard images below threshold size
def discard_images_below_size(current_dir, discard_dir, threshold_size=4000):
    for image_dir in os.listdir(current_dir):
        if not image_dir.startswith('.'):
            image_paths = os.listdir(os.path.join(current_dir, image_dir))

            discarded_images = 0
            for image in image_paths:
                if not image.startswith('.'):
                    image_path = os.path.join(current_dir, image_dir, image)
                    image_size = os.path.getsize(image_path)

                    if image_size < threshold_size:
                        discarded_path = os.path.join(discard_dir, image_dir, image)
                        shutil.move(image_path, discarded_path)
                        discarded_images += 1

            logger.info('{} has {} images discarded'.format(image_dir, discarded_images))


# Copy images into a directory (from current dir to new dir)
def copy_to_dir(current_dir, new_dir, number_to_copy=1000):
    for image_dir in os.listdir(current_dir):
        if not image_dir.startswith('.'):
            image_paths = os.listdir(os.path.join(current_dir, image_dir))

            image_count = number_to_copy
            logger.info('{}: {} being copied'.format(image_dir, image_count))
            for image in image_paths:
                if not image.startswith('.') and image_count > 0:
                    original_image = os.path.join(current_dir, image_dir, image)
                    image_to_copy = os.path.join(new_dir, image_dir, image)
                    shutil.copy(original_image, image_to_copy)
                    image_count -= 1


# Move images into a directory (from current dir to new dir)
def move_to_dir(current_dir, new_dir, percentage_to_move=0.1):
    for image_dir in os.listdir(current_dir):
        if not image_dir.startswith('.'):
            image_paths = os.listdir(os.path.join(current_dir, image_dir))
            image_count = len(image_paths)
            move_count = image_count * percentage_to_move
            logger.debug('{} has {} images; Images to move: {}'.format(image_dir, image_count, move_count))

            moved_count = 0
            for image in image_paths:
                if not image.startswith('.') and moved_count < move_count:
                    original_image = os.path.join(current_dir, image_dir, image)
                    image_to_move = os.path.join(new_dir, image_dir, image)
                    shutil.move(original_image, image_to_move)
                    moved_count += 1

            logger.info('{} has {} images moved'.format(image_dir, moved_count))


if __name__ == '__main__':

    main_dir = sys.argv[1]  # images_clothes
    train_dir = os.path.join('data', main_dir, 'train')
    val_dir = os.path.join('data', main_dir, 'val')
    test_dir = os.path.join('data', main_dir, 'test')
    train_samp_dir = os.path.join('data', main_dir, 'train_samp')
    val_samp_dir = os.path.join('data', main_dir, 'val_samp')
    test_samp_dir = os.path.join('data', main_dir, 'test_samp')
    discard_dir = os.path.join('data', main_dir, 'discard')

    # Create dir structure for discard and discard images
    mirror_dir_structure(train_dir, discard_dir)
    discard_images_below_size(train_dir, discard_dir, 4000)

    # Create dir structure for train sample and copy 1000 images
    mirror_dir_structure(train_dir, train_samp_dir)
    copy_to_dir(train_dir, train_samp_dir, 1000)

    # Split sample into train and val, with 0.1 split
    mirror_dir_structure(train_samp_dir, val_samp_dir)
    move_to_dir(train_samp_dir, val_samp_dir, 0.1)

    # Split test sample into val and test, with 0.05 split
    mirror_dir_structure(val_samp_dir, test_samp_dir)
    move_to_dir(val_samp_dir, test_samp_dir, 0.05)
