"""
Loads pre-trained model and prepares bottleneck features

python -m image.prep_bottleneck_feats images_clothes vgg16 samp
python -m image.prep_bottleneck_feats images_clothes inception3
nohup python -m image.prep_bottleneck_feats images_clothes inception3 samp >> bottleneck.log 2>&1&
"""
import os
import sys
import numpy as np
import itertools
from keras.preprocessing.image import ImageDataGenerator
from keras.utils.np_utils import to_categorical
from dl_models.vgg16 import VGG16
from dl_models.inception_v3 import InceptionV3
from utils.logger import logger
from utils.create_dir import create_dir


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


# Create labels for training and testing.
def create_labels(load_dir, category_dict):
    train_tuples = list()

    # Create tuples of category index and counts
    for image_dir in os.listdir(load_dir):
        if not image_dir.startswith('.'):
            image_count = len(os.listdir(os.path.join(load_dir, image_dir)))
            train_tuples.append((category_dict.keys()[category_dict.values().index(image_dir)], image_count))

    # Create training labels
    train_labels = to_categorical(list(itertools.chain.from_iterable([[tup[0]] * tup[1] for tup in train_tuples])))

    logger.info('{} labels created ({})'.format(load_dir, len(train_tuples)))
    return train_labels


# Load Data Genenerator
def load_data_generator():
    datagen = ImageDataGenerator(rescale=1./255)
    return datagen

# Get biggest divisor below threshold for batch_size
def largest_divisor(n, threshold=100):
    factors_set = set(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))
    factors_list = [i for i in factors_set if i <= threshold]
    factors_list.sort()
    return factors_list[-1]


# Create bottleneck features
def create_bottleneck_features(datagen, load_dir, model, labels, save_path, img_width=299, img_height=299):
    logger.info('No. of labels: {}; Largest divisor: {}'.format(labels.shape[0], largest_divisor(labels.shape[0])))
    generator = datagen.flow_from_directory(
        load_dir,
        target_size=(img_width, img_height),
        batch_size=largest_divisor(labels.shape[0], 100),
        class_mode=None,
        shuffle=False,
        seed=1368)
    bottleneck_features = model.predict_generator(generator, labels.shape[0])
    np.save(open(save_path, 'w'), bottleneck_features)
    logger.info('{} bottleneck features created'.format(load_dir))


if __name__ == '__main__':

    main_dir = sys.argv[1]  # images_clothes
    dl_model = sys.argv[2]
    try:
        dataset = sys.argv[3]
        dataset = '_' + dataset
    except IndexError:
        dataset = ''

    # Load pre-trained model
    if dl_model == 'vgg16':
        model = VGG16(include_top=False, weights='imagenet', input_tensor=None)
        img_width = 224
        img_height = 224
    elif dl_model == 'inception3':
        model = InceptionV3(include_top=False, weights='imagenet', input_tensor=None)
        img_width = 299
        img_height = 299
    else:
        raise ValueError('Model should be either "vgg16" or "inception3"')

    train = 'train' + dataset
    val = 'val' + dataset
    test = 'test' + dataset
    bottleneck_feature_dir = dl_model + dataset
    create_dir(os.path.join('data', main_dir, 'bottleneck_features', bottleneck_feature_dir))

    train_dir = os.path.join('data', main_dir, train)
    val_dir = os.path.join('data', main_dir, val)
    test_dir = os.path.join('data', main_dir, test)
    train_bottleneck_path = os.path.join('data', main_dir, 'bottleneck_features', bottleneck_feature_dir,
                                         'bottleneck_feat_' + train + '.npy')
    val_bottleneck_path = os.path.join('data', main_dir, 'bottleneck_features', bottleneck_feature_dir,
                                       'bottleneck_feat_' + val + '.npy')
    # test_bottleneck_path = os.path.join('data', main_dir, 'bottleneck_features', bottleneck_feature_dir,
    #                                     'bottleneck_feat_' + test + '.npy')

    # Create category dictionary
    category_dict = create_category_dict(train_dir)

    # Create labels
    train_labels = create_labels(train_dir, category_dict)
    val_labels = create_labels(val_dir, category_dict)
    # test_labels = create_labels(test_dir, category_dict)

    # Create data generator
    datagen = load_data_generator()

    # Create bottleneck features
    create_bottleneck_features(datagen, train_dir, model, train_labels, train_bottleneck_path, img_width, img_height)
    create_bottleneck_features(datagen, val_dir, model, val_labels, val_bottleneck_path, img_width, img_height)
    # create_bottleneck_features(datagen, test_dir, model, test_labels, test_bottleneck_path, img_width, img_height)
