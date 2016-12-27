import numpy as np
from keras.models import Model
from keras.layers import Dense, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from dl_models.resnet50 import ResNet50
from utils.logger import logger


# Conv blocks for retraining
conv_block = {'resnet50': {0: 176, 1: 164, 2: 154, 3: 142, 4: 132, 5: 122, 6: 112, 7: 102, 8: 92, 9: 80}}


def load_untrained_model(model_name, output_classes):
    # Load base model
    if model_name == 'resnet50':
        base_model = ResNet50(include_top=False, weights=None, input_tensor=None)
        logger.info('Untrained {} loaded'.format(model_name))
    else:
        raise Exception('Base model not loaded correctly')

    # Create top block
    x = base_model.output
    x = Flatten(name='flatten')(x)
    x = Dense(512, activation='relu', init='glorot_uniform', name='relu_1')(x)
    x = Dropout(0.5)(x)
    x = Dense(512, activation='relu', init='glorot_uniform', name='relu_2')(x)
    x = Dropout(0.5)(x)
    pred_layer = Dense(output_dim=output_classes, activation='softmax', name='softmax_output')(x)

    # Create overall model
    model = Model(input=base_model.input, output=pred_layer)

    return model


def load_pretrained_model(model_name, output_classes, weights_path='original'):
    # Load base model
    if model_name == 'resnet50' and weights_path == 'original':
        base_model = ResNet50(include_top=False, weights='imagenet', input_tensor=None)
        logger.info('Base model loaded with original weights')
    elif model_name == 'resnet50' and weights_path != 'original':
        base_model = ResNet50(include_top=False, weights=None, input_tensor=None)
        weights_path = weights_path
        logger.info('Base model loaded with weights in {}'.format(weights_path))
    else:
        raise Exception('Base model not loaded correctly')

    # Create top block
    x = base_model.output
    x = Flatten(name='flatten')(x)
    x = Dense(512, activation='relu', init='glorot_uniform', name='relu_1')(x)
    x = Dropout(0.5)(x)
    x = Dense(512, activation='relu', init='glorot_uniform', name='relu_2')(x)
    x = Dropout(0.5)(x)
    pred_layer = Dense(output_dim=output_classes, activation='softmax', name='softmax_output')(x)

    # Create overall model
    model = Model(input=base_model.input, output=pred_layer)

    # Load weights if not original weights
    if weights_path != 'original':
        model.load_weights(weights_path)

    return model


def set_trainable_blocks(model_name, model, blocks=2):
    """
    Sets the number of trainable blocks, starting from the end.
    The pred layer is considered as block 0.
    """
    for layer in model.layers[:conv_block[model_name][blocks]]:
        layer.trainable = False
    for layer in model.layers[conv_block[model_name][blocks]:]:
        layer.trainable = True

    return model


def create_train_datagen(train_dir, batch_size, img_width, img_height):
    datagen = ImageDataGenerator(rescale=1. / 255,
                                 rotation_range=15,
                                 shear_range=0.2,
                                 zoom_range=0.2,
                                 horizontal_flip=True)

    train_datagen = datagen.flow_from_directory(train_dir,
                                                target_size=(img_width, img_height),
                                                batch_size=batch_size,
                                                class_mode='categorical',
                                                shuffle=True,
                                                seed=1368)

    return train_datagen


def create_validation_datagen(val_dir, batch_size, img_width, img_height):
    datagen = ImageDataGenerator(rescale=1. / 255)

    val_datagen = datagen.flow_from_directory(val_dir,
                                              target_size=(img_width, img_height),
                                              batch_size=batch_size,
                                              class_mode='categorical',
                                              shuffle=True,
                                              seed=1368)

    return val_datagen


def compile_model(model, optimizer):
    model.compile(optimizer=optimizer,
                  loss='categorical_crossentropy',
                  metrics=['accuracy', 'top_k_categorical_accuracy'])


def fit_model(model, train_generator, validation_generator, epoches):
    model.fit_generator(train_generator, samples_per_epoch=train_generator.N, nb_epoch=epoches,
                        validation_data=validation_generator,
                        nb_val_samples=validation_generator.N,
                        max_q_size=20, nb_worker=4)


def prepare_image(image_path, img_width, img_height):
    """

    Returns an image array given of the image in path

    :param image_path:
    :param img_width:
    :param img_height:
    :return:
    """
    img = image.load_img(image_path, target_size=(img_width, img_height))
    img = image.img_to_array(img)
    img = np.multiply(img, 1. / 255)
    img = np.expand_dims(img, axis=0)

    return img
