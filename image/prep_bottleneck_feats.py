"""
Loads pre-trained model and prepares bottleneck features

python -m image.prep_bottleneck_feats images_clothes subset
"""
import os
import sys
import h5py
import numpy as np
import itertools
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.utils.np_utils import to_categorical
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

    logger.info('{} labels created'.format(load_dir))
    return train_labels


# Load Data Genenerator
def load_data_generator():
    datagen = ImageDataGenerator(rescale=1./255)
    return datagen


# Load VGG16 model with pre-trained weights
def load_vgg16(weights_path='data/images/model/vgg16_weights.h5', img_width=150, img_height=150):

    # build the VGG16 network
    model = Sequential()
    model.add(ZeroPadding2D((1, 1), input_shape=(3, img_width, img_height)))

    model.add(Convolution2D(64, 3, 3, activation='relu', name='conv1_1'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(64, 3, 3, activation='relu', name='conv1_2'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(128, 3, 3, activation='relu', name='conv2_1'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(128, 3, 3, activation='relu', name='conv2_2'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, 3, 3, activation='relu', name='conv3_1'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, 3, 3, activation='relu', name='conv3_2'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, 3, 3, activation='relu', name='conv3_3'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu', name='conv4_1'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu', name='conv4_2'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu', name='conv4_3'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu', name='conv5_1'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu', name='conv5_2'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu', name='conv5_3'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    # load the weights of the VGG16 networks
    # (trained on ImageNet, won the ILSVRC competition in 2014)
    # note: when there is a complete match between your model definition
    # and your weight savefile, you can simply call model.load_weights(filename)
    assert os.path.exists(weights_path), 'Model weights not found (see "weights_path" variable in script).'
    f = h5py.File(weights_path)
    for k in range(f.attrs['nb_layers']):
        if k >= len(model.layers):
            # we don't look at the last (fully-connected) layers in the savefile
            break
        g = f['layer_{}'.format(k)]
        weights = [g['param_{}'.format(p)] for p in range(g.attrs['nb_params'])]
        model.layers[k].set_weights(weights)
    f.close()
    logger.info('Model loaded.')

    return model


# Create bottleneck features
def create_bottleneck_features(datagen, load_dir, model, labels, save_path,
                               batch_size=32, img_width=150, img_height=150):
    generator = datagen.flow_from_directory(
        load_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    bottleneck_features = model.predict_generator(generator, labels.shape[0])
    np.save(open(save_path, 'w'), bottleneck_features)
    logger.info('{} bottleneck features created'.format(load_dir))


if __name__ == '__main__':

    main_dir = sys.argv[1]  # images_clothes
    try:
        dataset = sys.argv[2]
        dataset = '_' + dataset
    except IndexError:
        dataset = ''

    train = 'train' + dataset
    val = 'val' + dataset
    test = 'test' + dataset

    weights_path = 'data/images/model/vgg16_weights.h5'
    train_bottleneck_features_path = 'data/images_clothes/bottleneck_features/bottleneck_features_' + train
    img_width = 150
    img_height = 150
    batch_size = 32
    batch_size_test = 1

    train_dir = os.path.join('data', main_dir, train)
    val_dir = os.path.join('data', main_dir, val)
    test_dir = os.path.join('data', main_dir, test)
    train_bottleneck_path = os.path.join('data', main_dir, 'bottleneck_features', 'bottleneck_feat_' + train + '.npy')
    val_bottleneck_path = os.path.join('data', main_dir, 'bottleneck_features', 'bottleneck_feat_' + val + '.npy')
    test_bottleneck_path = os.path.join('data', main_dir, 'bottleneck_features', 'bottleneck_feat_' + test + '.npy')

    # Create category dictionary
    category_dict = create_category_dict(train_dir)

    # Create labels
    train_labels = create_labels(train_dir, category_dict)
    val_labels = create_labels(val_dir, category_dict)
    test_labels = create_labels(test_dir, category_dict)

    # Create data generator
    datagen = load_data_generator()

    # Load pre-trained model
    model = load_vgg16(weights_path, img_width, img_height)

    # Create bottleneck features
    create_bottleneck_features(datagen, train_dir, model, train_labels, train_bottleneck_path,
                               batch_size, img_width, img_height)
    create_bottleneck_features(datagen, val_dir, model, val_labels, val_bottleneck_path,
                               batch_size, img_width, img_height)
    create_bottleneck_features(datagen, test_dir, model, test_labels, test_bottleneck_path,
                               batch_size_test, img_width, img_height)
