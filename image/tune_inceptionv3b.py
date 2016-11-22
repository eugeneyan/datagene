"""
python -m image.tune_inceptionv3b
nohup python -m image.tune_inceptionv3.py >> finetune.log 2>&1&
"""
from keras.models import Model, Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
from dl_models.inception_v3 import InceptionV3
from utils.logger import logger


img_width = 299
img_height = 299
train_dir = 'data/images_clothes/train'
val_dir = 'data/images_clothes/val'

# create the base pre-trained model
base_model = InceptionV3(include_top=False, weights='imagenet', input_tensor=None)

logger.info('Base model loaded')

# Create top model
top_model = Sequential()
top_model.add(Flatten(input_shape=(1, 1, 2048)))
top_model.add(Dense(512, activation='relu', init='glorot_uniform'))
top_model.add(Dropout(0.5))
top_model.add(Dense(512, activation='relu', init='glorot_uniform'))
top_model.add(Dropout(0.5))
top_model.add(Dense(output_dim=65, activation='softmax'))

# Load weights
top_model.load_weights('data/images_clothes/model/final_layer_weights_inception3.h5')

model = Model(input=base_model.input, output=top_model(base_model.output))

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

# train_datagen = load_data_generator()

train_datagen = ImageDataGenerator(rescale=1./255)
validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(train_dir,
                                                    target_size=(img_width, img_height),
                                                    batch_size=128,
                                                    class_mode='categorical',
                                                    shuffle=True,
                                                    seed=1368)

validation_generator = validation_datagen.flow_from_directory(val_dir,
                                                              target_size=(img_width, img_height),
                                                              batch_size=128,
                                                              class_mode='categorical',
                                                              shuffle=True,
                                                              seed=1368)

logger.info('Train and val generators created')

# let's visualize layer names and layer indices to see how many layers
# we should freeze:
for i, layer in enumerate(base_model.layers):
   print(i, layer.name)

# we chose to train the top 2 inception blocks, i.e. we will freeze
# the first 172 layers and unfreeze the rest:
for layer in model.layers[:172]:
   layer.trainable = False
for layer in model.layers[172:]:
   layer.trainable = True

# we need to recompile the model for these modifications to take effect
# we use SGD with a low learning rate
from keras.optimizers import SGD
model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy', metrics=['accuracy', 'top_k_categorical_accuracy'])

logger.info('Model to be fine-tuned compiled')

# we train our model again (this time fine-tuning the top 2 inception blocks
# alongside the top Dense layers
model.fit_generator(train_generator, samples_per_epoch=train_generator.N, nb_epoch=168,
                    validation_data=validation_generator,
                    nb_val_samples=validation_generator.N)

logger.info('Model fine-tuned')

model.save_weights('Inception_finetuned.h5')  # always save your weights after training or during training

logger.info('Weights saved')