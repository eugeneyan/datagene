"""
python -m image.sample_tunevgg1

"""
import os
import h5py
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers import Activation, Dropout, Flatten, Dense
from dl_models.vgg16 import VGG16


# path to the model weights file.
weights_path = 'data/images_clothes/model/vgg16_weights.h5'
top_model_weights_path = 'data/images_clothes/model/bottleneck_fc_model.h5'
# dimensions of our images.
img_width, img_height = 224, 224

train_data_dir = 'data/images_clothes/train_subset'
validation_data_dir = 'data/images_clothes/val_subset'
nb_train_samples = 950
nb_validation_samples = 50
nb_epoch = 38


def largest_divisor(n, threshold=100):
    factors_set = set(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))
    factors_list = [i for i in factors_set if i <= threshold]
    factors_list.sort()
    return factors_list[-1]


def save_bottleneck_features():
    datagen = ImageDataGenerator(rescale=1./255)

    # # build the VGG16 network
    # model = Sequential()
    # model.add(ZeroPadding2D((1, 1), input_shape=(3, img_width, img_height)))
    #
    # model.add(Convolution2D(64, 3, 3, activation='relu', name='conv1_1'))
    # model.add(ZeroPadding2D((1, 1)))
    # model.add(Convolution2D(64, 3, 3, activation='relu', name='conv1_2'))
    # model.add(MaxPooling2D((2, 2), strides=(2, 2)))
    #
    # model.add(ZeroPadding2D((1, 1)))
    # model.add(Convolution2D(128, 3, 3, activation='relu', name='conv2_1'))
    # model.add(ZeroPadding2D((1, 1)))
    # model.add(Convolution2D(128, 3, 3, activation='relu', name='conv2_2'))
    # model.add(MaxPooling2D((2, 2), strides=(2, 2)))
    #
    # model.add(ZeroPadding2D((1, 1)))
    # model.add(Convolution2D(256, 3, 3, activation='relu', name='conv3_1'))
    # model.add(ZeroPadding2D((1, 1)))
    # model.add(Convolution2D(256, 3, 3, activation='relu', name='conv3_2'))
    # model.add(ZeroPadding2D((1, 1)))
    # model.add(Convolution2D(256, 3, 3, activation='relu', name='conv3_3'))
    # model.add(MaxPooling2D((2, 2), strides=(2, 2)))
    #
    # model.add(ZeroPadding2D((1, 1)))
    # model.add(Convolution2D(512, 3, 3, activation='relu', name='conv4_1'))
    # model.add(ZeroPadding2D((1, 1)))
    # model.add(Convolution2D(512, 3, 3, activation='relu', name='conv4_2'))
    # model.add(ZeroPadding2D((1, 1)))
    # model.add(Convolution2D(512, 3, 3, activation='relu', name='conv4_3'))
    # model.add(MaxPooling2D((2, 2), strides=(2, 2)))
    #
    # model.add(ZeroPadding2D((1, 1)))
    # model.add(Convolution2D(512, 3, 3, activation='relu', name='conv5_1'))
    # model.add(ZeroPadding2D((1, 1)))
    # model.add(Convolution2D(512, 3, 3, activation='relu', name='conv5_2'))
    # model.add(ZeroPadding2D((1, 1)))
    # model.add(Convolution2D(512, 3, 3, activation='relu', name='conv5_3'))
    # model.add(MaxPooling2D((2, 2), strides=(2, 2)))
    #
    # # load the weights of the VGG16 networks
    # # (trained on ImageNet, won the ILSVRC competition in 2014)
    # # note: when there is a complete match between your model definition
    # # and your weight savefile, you can simply call model.load_weights(filename)
    # assert os.path.exists(weights_path), 'Model weights not found (see "weights_path" variable in script).'
    # f = h5py.File(weights_path)
    # for k in range(f.attrs['nb_layers']):
    #     if k >= len(model.layers):
    #         # we don't look at the last (fully-connected) layers in the savefile
    #         break
    #     g = f['layer_{}'.format(k)]
    #     weights = [g['param_{}'.format(p)] for p in range(g.attrs['nb_params'])]
    #     model.layers[k].set_weights(weights)
    # f.close()
    model = VGG16(include_top=False, weights='imagenet', input_tensor=None)
    print('Model loaded.')

    datagen = ImageDataGenerator(rescale=1./255)

    generator_train = datagen.flow_from_directory(
        train_data_dir,
        target_size=(224, 224),
        batch_size=largest_divisor(nb_train_samples),
        class_mode=None,
        shuffle=False,
        seed=1368)
    bottleneck_features_train = model.predict_generator(generator_train, nb_train_samples)
    np.save(open('bottleneck_features_train.npy', 'w'), bottleneck_features_train)
    print ('Train bottleneck features created')

    generator_val = datagen.flow_from_directory(
        validation_data_dir,
        target_size=(224, 224),
        batch_size=largest_divisor(nb_validation_samples),
        class_mode=None,
        shuffle=False,
        seed=1368)
    bottleneck_features_val = model.predict_generator(generator_val, nb_validation_samples)
    np.save(open('bottleneck_features_val.npy', 'w'), bottleneck_features_val)
    print ('Val bottleneck features created')


def train_top_model():
    train_data = np.load(open('bottleneck_features_train.npy'))
    train_labels = np.array([0] * (nb_train_samples / 2) + [1] * (nb_train_samples / 2))

    validation_data = np.load(open('bottleneck_features_val.npy'))
    validation_labels = np.array([0] * (nb_validation_samples / 2) + [1] * (nb_validation_samples / 2))

    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(train_data, train_labels,
              nb_epoch=nb_epoch, batch_size=32,
              validation_data=(validation_data, validation_labels))
    model.save_weights(top_model_weights_path)


if __name__ == '__main__':

    save_bottleneck_features()
    train_top_model()