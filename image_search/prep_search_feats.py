"""
Prepare image features for image search

python -m image_search.prep_search_feats images train_top_level >> prep.log 2>&1
python -m image_search.prep_search_feats images_sample train_top_level
"""
import sys
import os
import numpy as np
from categorize_image.prep_bottleneck_feats import load_data_generator, largest_divisor
from dl_models.inception_v3_flatterned import InceptionV3
from utils.create_dir import create_dir
from utils.logger import logger


# Count number of images
def get_image_count(train_dir):
    image_count_total = 0

    for image_dir in os.listdir(train_dir):
        if not image_dir.startswith('.'):
            image_names = os.listdir(os.path.join(train_dir, image_dir))
            image_names = [image_name for image_name in image_names if not image_name.startswith('.')]
            image_count = len(image_names)
            image_count_total += image_count

    logger.info('No. of images: {}'.format(image_count_total))
    return image_count_total


# Create bottleneck features
def create_search_features(datagen, load_dir, model, image_count, save_path, img_width=299, img_height=299):
    generator = datagen.flow_from_directory(
        load_dir,
        target_size=(img_width, img_height),
        batch_size=largest_divisor(image_count, 100),
        class_mode=None,
        shuffle=False,
        seed=1368)
    search_features = model.predict_generator(generator, val_samples=image_count)
    np.save(open(save_path, 'w'), search_features)
    logger.info('{} search features created'.format(load_dir))


if __name__ == '__main__':
    main_dir = sys.argv[1]  # images
    train_dir = sys.argv[2]  # train_top_level

    train_dir = os.path.join('data', main_dir, train_dir)

    # Create dir for bottleneck features
    bottleneck_dir = 'search_features'
    create_dir(os.path.join('data', main_dir, bottleneck_dir))
    search_features_path = os.path.join('data', main_dir, bottleneck_dir, 'search_features.npy')

    # Use InceptionV3 as it has small output side with reasonable search effectiveness
    model = InceptionV3(include_top=False, weights='imagenet', input_tensor=None)
    img_width = 299
    img_height = 299

    # Load data generator
    datagen = load_data_generator()

    # Get number of images for batch size
    image_count = get_image_count(train_dir)

    # Create bottleneck features
    create_search_features(datagen, train_dir, model, image_count, search_features_path, img_width, img_height)
