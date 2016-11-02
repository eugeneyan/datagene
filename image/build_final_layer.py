"""
Build final layer of deep learning network (for classification of bottleneck features)

python -m image.build_final_layer images_clothes 10 subset
"""
import os
import sys
import numpy as np
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from image.prep_bottleneck_feats import create_category_dict, create_labels


def build_final_layer(train_data, train_labels, val_data, val_labels, nb_epoch, top_model_weights_path):
    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(output_dim=9, activation='sigmoid'))

    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

    model.fit(train_data, train_labels,
              nb_epoch=nb_epoch, batch_size=32,
              validation_data=(val_data, val_labels))
    model.save_weights(top_model_weights_path)
    return model


def get_test_accuracy(model, test_data, test_labels):
    preds = model.predict_classes(test_data)


if __name__ == '__main__':

    main_dir = sys.argv[1]  # images_clothes
    epoches = int(sys.argv[2])
    try:
        dataset = sys.argv[3]
        dataset = '_' + dataset
    except IndexError:
        dataset = ''

    train = 'train' + dataset
    val = 'val' + dataset
    test = 'test' + dataset

    train_dir = os.path.join('data', main_dir, train)
    val_dir = os.path.join('data', main_dir, val)
    test_dir = os.path.join('data', main_dir, test)
    train_bottleneck_path = os.path.join('data', main_dir, 'bottleneck_features', 'bottleneck_feat_' + train + '.npy')
    val_bottleneck_path = os.path.join('data', main_dir, 'bottleneck_features', 'bottleneck_feat_' + val + '.npy')
    test_bottleneck_path = os.path.join('data', main_dir, 'bottleneck_features', 'bottleneck_feat_' + test + '.npy')
    model_save_path = os.path.join('data', main_dir, 'model', 'final_layer_weights' + dataset + '.h5')

    # Load bottleneck features
    train_data = np.load(open(train_bottleneck_path))
    val_data = np.load(open(val_bottleneck_path))
    test_data = np.load(open(test_bottleneck_path))

    # Create category dictionary
    category_dict = create_category_dict(train_dir)

    # Create labels
    train_labels = create_labels(train_dir, category_dict)
    val_labels = create_labels(val_dir, category_dict)
    test_labels = create_labels(test_dir, category_dict)

    # Build model
    model = build_final_layer(train_data, train_labels, val_data, val_labels, epoches, model_save_path)
