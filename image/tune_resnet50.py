"""
python -m image.tune_resnet50
nohup python -m image.tune_inceptionv3.py >> fine_resnet50.log 2>&1&
"""
from keras.models import Model
from keras.layers import Dense, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
from dl_models.resnet50 import ResNet50
from utils.logger import logger


img_width = 224
img_height = 224
train_dir = 'data/images_clothes/train'
val_dir = 'data/images_clothes/val'

# create the base pre-trained model
base_model = ResNet50(include_top=False, weights='imagenet', input_tensor=None)

print (base_model.layers)

logger.info('Base model loaded')

# add top model
x = base_model.output
x = Flatten(name='flatten')(x)
x = Dense(512, activation='relu', init='glorot_uniform')(x)
x = Dropout(0.5)(x)
x = Dense(512, activation='relu', init='glorot_uniform')(x)
x = Dropout(0.5)(x)
pred_layer = Dense(output_dim=65, activation='softmax')(x)

model = Model(input=base_model.input, output=pred_layer)

logger.info('Pred layer added')

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional InceptionV3 layers
for layer in base_model.layers:
    layer.trainable = False

# compile the model (should be done *after* setting layers to non-trainable)
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy', 'top_k_categorical_accuracy'])

logger.info('Full model compiled')

# Load Data Genenerator
def load_data_generator():
    datagen = ImageDataGenerator(rescale=1./255,
                                 rotation_range=15,
                                 shear_range=0.2,
                                 zoom_range=0.2,
                                 horizontal_flip=True)
    return datagen

train_datagen = load_data_generator()

validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(train_dir,
                                                    target_size=(img_width, img_height),
                                                    batch_size=38,
                                                    class_mode='categorical',
                                                    shuffle=True,
                                                    seed=1368)

validation_generator = validation_datagen.flow_from_directory(val_dir,
                                                              target_size=(img_width, img_height),
                                                              batch_size=38,
                                                              class_mode='categorical',
                                                              shuffle=True,
                                                              seed=1368)

logger.info('Train and val generators created')
logger.info('Train samples: {}'.format(train_generator.N))
logger.info('Validation samples: {}'.format(validation_generator.N))

# train the model on the new data for a few epochs
model.fit_generator(train_generator, samples_per_epoch=train_generator.N, nb_epoch=18,
                    validation_data=validation_generator,
                    nb_val_samples=validation_generator.N,
                    max_q_size=20, nb_worker=4)

logger.info('Pred layer trained. Starting fine-tuning')

# at this point, the top layers are well trained and we can start fine-tuning
# convolutional layers from inception V3. We will freeze the bottom N layers
# and train the remaining top layers.

# let's visualize layer names and layer indices to see how many layers
# we should freeze:
for i, layer in enumerate(base_model.layers):
   print(i, layer.name)

# we chose to train the top 2 inception blocks, i.e. we will freeze
# the first 172 layers and unfreeze the rest:
for layer in model.layers[:154]:
   layer.trainable = False
for layer in model.layers[154:]:
   layer.trainable = True

# we need to recompile the model for these modifications to take effect
# we use SGD with a low learning rate
from keras.optimizers import SGD
model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy', metrics=['accuracy', 'top_k_categorical_accuracy'])

logger.info('Model to be fine-tuned compiled')

# we train our model again (this time fine-tuning the top 2 inception blocks
# alongside the top Dense layers
model.fit_generator(train_generator, samples_per_epoch=train_generator.N, nb_epoch=38,
                    validation_data=validation_generator,
                    nb_val_samples=validation_generator.N,
                    max_q_size=20, nb_worker=4)

logger.info('Model fine-tuned')

model.save_weights('data/images_clothes/model/resnet_finetuned.h5')  # always save your weights after training or
# during training

logger.info('Weights saved')