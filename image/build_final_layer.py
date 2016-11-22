"""
Build final layer of deep learning network (for classification of bottleneck features)

python -m image.build_final_layer images_clothes vgg16 20 subset
python -m image.build_final_layer images_clothes inception3 38
nohup python -m image.build_final_layer images_clothes inception3 68 >> final_layer.log 2>&1&
"""
import os
import sys
import numpy as np
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras.optimizers import SGD, RMSprop
from image.prep_bottleneck_feats import create_category_dict, create_labels


# Optimizers
sgd = SGD(lr=0.01, momentum=0.00, decay=0.00, nesterov=False)
rmsprop = RMSprop(lr=0.01, rho=0.9, epsilon=1e-08, decay=0.0, clipnorm=1.0, clipvalue=1.0)


def build_final_layer_vgg16(train_data, train_labels, val_data, val_labels, optimizer, nb_epoch,
                            top_model_weights_path):
    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(512, activation='relu', init='glorot_uniform'))
    model.add(Dropout(0.5))
    model.add(Dense(512, activation='relu', init='glorot_uniform'))
    model.add(Dropout(0.5))
    model.add(Dense(output_dim=train_labels.shape[1], activation='softmax'))

    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy', 'top_k_categorical_accuracy'])

    model.fit(train_data, train_labels,
              nb_epoch=nb_epoch, batch_size=32,
              validation_data=(val_data, val_labels))
    model.save_weights(top_model_weights_path)
    return model


def build_final_layer_inception3(train_data, train_labels, val_data, val_labels, optimizer, nb_epoch,
                                 top_model_weights_path):

    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(512, activation='relu', init='glorot_uniform'))
    model.add(Dropout(0.5))
    model.add(Dense(512, activation='relu', init='glorot_uniform'))
    model.add(Dropout(0.5))
    model.add(Dense(output_dim=train_labels.shape[1], activation='softmax'))

    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy', 'top_k_categorical_accuracy'])

    model.fit(train_data, train_labels,
              nb_epoch=nb_epoch, batch_size=32,
              validation_data=(val_data, val_labels))
    model.save_weights(top_model_weights_path)
    return model


def get_test_accuracy(model, test_data, test_labels):
    preds = model.predict_classes(test_data)


if __name__ == '__main__':

    main_dir = sys.argv[1]  # images_clothes
    dl_model = sys.argv[2]
    epoches = int(sys.argv[3])
    try:
        dataset = sys.argv[4]
        dataset = '_' + dataset
    except IndexError:
        dataset = ''

    train = 'train' + dataset
    val = 'val' + dataset
    test = 'test' + dataset
    bottleneck_feature_dir = dl_model + dataset

    train_dir = os.path.join('data', main_dir, train)
    val_dir = os.path.join('data', main_dir, val)
    test_dir = os.path.join('data', main_dir, test)
    train_bottleneck_path = os.path.join('data', main_dir, 'bottleneck_features', bottleneck_feature_dir,
                                         'bottleneck_feat_' + train + '.npy')
    val_bottleneck_path = os.path.join('data', main_dir, 'bottleneck_features', bottleneck_feature_dir,
                                       'bottleneck_feat_' + val + '.npy')
    # test_bottleneck_path = os.path.join('data', main_dir, 'bottleneck_features', bottleneck_feature_dir,
    #                                     'bottleneck_feat_' + test + '.npy')
    model_save_path = os.path.join('data', main_dir, 'model', 'final_layer_weights' + '_' + dl_model + dataset + '.h5')

    # Load bottleneck features
    train_data = np.load(open(train_bottleneck_path))
    val_data = np.load(open(val_bottleneck_path))
    # test_data = np.load(open(test_bottleneck_path))

    # Create category dictionary
    category_dict = create_category_dict(train_dir)

    # Create labels
    train_labels = create_labels(train_dir, category_dict)
    val_labels = create_labels(val_dir, category_dict)
    # test_labels = create_labels(test_dir, category_dict)

    # Build model
    if dl_model == 'vgg16':
        model = build_final_layer_vgg16(train_data, train_labels, val_data, val_labels, sgd, epoches, model_save_path)
    elif dl_model == 'inception3':
        model = build_final_layer_inception3(train_data, train_labels, val_data, val_labels, sgd, epoches,
                                             model_save_path)
    else:
        raise ValueError('Model should be either "vgg16" or "inception3"')