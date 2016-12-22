"""
Prepares the image directory for image search by:
- Copying all images from the train dir and sub dir into a single folder

python -m image_search.prep_image_dir images
"""
import os
import sys
from image.prep_image_dir import copy_to_single_dir


if __name__ == '__main__':

    main_dir = sys.argv[1]

    train_dir = os.path.join('data', main_dir, 'train')
    new_dir = os.path.join('data', main_dir, 'all_images')

    copy_to_single_dir(train_dir, new_dir)
