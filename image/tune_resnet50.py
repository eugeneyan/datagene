"""
python -m image.tune_resnet50
python -m image.tune_resnet50 >> tune_resnet50b.log 2>&1&
"""
from image_categorize_utils import *
from keras.optimizers import SGD
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
batch_size = 38

# Initialize optimizer
mini_sgd = SGD(lr=0.0001, momentum=0.9)


if __name__ == '__main__':

    # Load model
    model = load_pretrained_model(model_name, output_classes=output_classes,
                                  weights_path=os.path.join(model_save_path, 'resnet_finetuned.h5'))
    logger.info('{} model loaded'.format(model_name))
    logger.debug(model)

    # Create train and validation data generators
    train_generator = create_train_datagen(train_dir, batch_size, img_width, img_height)
    logger.info('Train generator created')
    validation_generator = create_validation_datagen(val_dir, batch_size, img_width, img_height)
    logger.info('Validation generator created')

    for i in range(4, 10):

        # Train pred layer first
        model = set_trainable_blocks(model_name, model, i)
        logger.info('{} trainable block(s) for model set'.format(i))
        logger.debug(model)

        # Compile and train model for i * 5 epoches
        compile_model(model, mini_sgd)
        logger.info('Model compiled with {} trainable block(s)'.format(i))

        logger.info('Model training with {} trainable blocks for {} epoches'.format(i, i*5))
        fit_model(model, train_generator, validation_generator, epoches=i*5)
        logger.info('Model fitted with {} trainable block(s)'.format(i))

        # Save weights
        weights_save_path = os.path.join(model_save_path, model_name + '_finetuned_' + str(i) + 'block.h5')
        model.save_weights(weights_save_path)
        logger.info('Weights saved here: {}'.format(weights_save_path))

    # Fit model again and train for many epoches
    fit_model(model, train_generator, validation_generator, epoches=38)

    # Save weights
    weights_save_path = os.path.join(model_save_path, model_name + '_finetuned_' + 'final' + 'block.h5')
    model.save_weights(weights_save_path)
    logger.info('Weights saved here: {}'.format(weights_save_path))
