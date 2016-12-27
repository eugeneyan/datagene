"""
python -m image.tune_resnet50a
"""
import os
from image_categorize_utils import *
from keras.optimizers import SGD
from utils.logger import logger


# Parameters for retraining
train_dir = 'data/images_clothes/train_subset'
val_dir = 'data/images_clothes/val_subset'
model_name = 'resnet50'
output_classes = 8
model_save_path = 'data/images_clothes/model/'
img_width = 224
img_height = 224
batch_size = 38
epoches = 18

# Initialize optimizers
sgd = SGD(lr=0.01, momentum=0.9, decay=0.00, nesterov=False)
mini_sgd = SGD(lr=0.0001, momentum=0.9)


if __name__ == '__main__':

    # Load model
    model = load_pretrained_model(model_name, output_classes=output_classes)
    logger.info('{} model loaded'.format(model_name))
    logger.debug(model)

    # Create train and validation data generators
    train_generator = create_train_datagen(train_dir, batch_size, img_width, img_height)
    logger.info('Train generator created')
    validation_generator = create_validation_datagen(val_dir, batch_size, img_width, img_height)
    logger.info('Validation generator created')

    # Train pred layer first
    model = set_trainable_blocks(model_name, model, 0)
    logger.info('{} trainable block(s) for model set'.format(0))
    logger.debug(model)

    # Compile and train model for 18 epoches
    compile_model(model, sgd)
    logger.info('Model compiled with {} trainable block(s)'.format(0))

    fit_model(model, train_generator, validation_generator, epoches=epoches)
    logger.info('Model fitted with {} trainable block(s)'.format(0))

    # Save weights
    weights_save_path = os.path.join(model_save_path, model_name + '_finetuned_' + str(0) + 'block.h5')
    model.save_weights(weights_save_path)
    logger.info('Weights saved here: {}'.format(weights_save_path))

    for i in range(1, 10):

        # Train conv blocks
        model = set_trainable_blocks(model_name, model, i)
        logger.info('{} trainable block(s) for model set'.format(i))
        logger.debug(model)

        # Compile and train model for 18 epoches
        compile_model(model, mini_sgd)
        logger.info('Model compiled with {} trainable block(s)'.format(i))

        fit_model(model, train_generator, validation_generator, epoches=epoches)
        logger.info('Model fitted with {} trainable block(s)'.format(i))

        # Save weights
        weights_save_path = os.path.join(model_save_path, model_name + '_finetuned_' + str(i) + 'block.h5')
        model.save_weights(weights_save_path)
        logger.info('Weights saved here: {}'.format(weights_save_path))
