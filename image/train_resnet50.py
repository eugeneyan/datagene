"""
python -m image.train_resnet50 >> train_resnet50.log 2>&1&
"""
from image_categorize_utils import *
from keras.optimizers import SGD, RMSprop
from utils.logger import logger
import os


# Parameters for retraining
train_dir = 'data/images_clothes/train'
val_dir = 'data/images_clothes/val'
model_name = 'resnet50'
output_classes = 65
model_save_path = 'data/images_clothes/model/'
img_width = 224
img_height = 224
batch_size = 3


#Initialize optimizers
sgd = SGD(lr=0.01, momentum=0.9, decay=0.00, nesterov=False)
rmsprop = RMSprop(lr=0.01, rho=0.9, epsilon=1e-08, decay=0.0, clipnorm=1.0, clipvalue=1.0)
mini_sgd = SGD(lr=0.001, momentum=0.9)

if __name__ == '__main__':

    # Load model
    model = load_untrained_model(model_name, output_classes=output_classes)
    logger.info('{} model loaded'.format(model_name))
    logger.debug(model)

    # Create train and validation data generators
    train_generator = create_train_datagen(train_dir, batch_size, img_width, img_height)
    logger.info('Train generator created')
    validation_generator = create_validation_datagen(val_dir, batch_size, img_width, img_height)
    logger.info('Validation generator created')

    # Compile and train model for 38 epoches
    compile_model(model, sgd)
    logger.info('Model compiled')

    fit_model(model, train_generator, validation_generator, epoches=32)
    logger.info('Model fitted with {} epoches'.format(32))

    weights_save_path = os.path.join(model_save_path, model_name + '_trained_' + str(32) + '.h5')
    model.save_weights(weights_save_path)
    logger.info('Weights saved here: {}'.format(weights_save_path))

    # Compile and train model for 68 epoches
    compile_model(model, sgd)
    logger.info('Model compiled')

    fit_model(model, train_generator, validation_generator, epoches=68)
    logger.info('Model fitted with {} epoches'.format(68))

    weights_save_path = os.path.join(model_save_path, model_name + '_trained_' + str(32 + 68) + '.h5')
    model.save_weights(weights_save_path)
    logger.info('Weights saved here: {}'.format(weights_save_path))

    # Compile and train model for 68 epoches
    compile_model(model, mini_sgd)
    logger.info('Model compiled')

    fit_model(model, train_generator, validation_generator, epoches=68)
    logger.info('Model fitted with {} epoches'.format(68))

    weights_save_path = os.path.join(model_save_path, model_name + '_trained_' + str(32 + 68 + 68) + '.h5')
    model.save_weights(weights_save_path)
    logger.info('Weights saved here: {}'.format(weights_save_path))

