"""
python -m image.tune_inceptionv3.py
"""
from keras.models import Model
from keras.layers import Dense, Flatten, Dropout
from prep_bottleneck_feats import *


img_width = 299
img_height = 299
train_dir = 'data/images_clothes/train_subset'
val_dir = 'data/images_clothes/val_subset'

# create the base pre-trained model
base_model = InceptionV3(weights='imagenet', include_top=False)

# add top model
x = base_model.output
x = Flatten(name='flatten')(x)
x = Dense(512, activation='relu', init='glorot_uniform')(x)
x = Dropout(0.5)(x)
x = Dense(512, activation='relu', init='glorot_uniform')(x)
x = Dropout(0.5)(x)
pred_layer = Dense(output_dim=2, activation='softmax')(x)

model = Model(input=base_model.input, output=pred_layer)

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional InceptionV3 layers
for layer in base_model.layers:
    layer.trainable = False

# compile the model (should be done *after* setting layers to non-trainable)
model.compile(optimizer='rmsprop', loss='categorical_crossentropy')


# Load Data Genenerator
def load_data_generator():
    datagen = ImageDataGenerator(rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)
    return datagen

datagen = load_data_generator()

train_generator = datagen.flow_from_directory(train_dir,
                                              target_size=(img_width, img_height),
                                              batch_size=32,
                                              class_mode=None,
                                              shuffle=False,
                                              seed=1368)

validation_generator = datagen.flow_from_directory(val_dir,
                                              target_size=(img_width, img_height),
                                              batch_size=32,
                                              class_mode=None,
                                              shuffle=False,
                                              seed=1368)

# train the model on the new data for a few epochs
model.fit_generator(train_generator, samples_per_epoch=100000, nb_epoch=10, validation_data=validation_generator)

# at this point, the top layers are well trained and we can start fine-tuning
# convolutional layers from inception V3. We will freeze the bottom N layers
# and train the remaining top layers.

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
model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy')

# we train our model again (this time fine-tuning the top 2 inception blocks
# alongside the top Dense layers
model.fit_generator(train_generator, nb_epoch=168, validation_data=validation_generator)

model.save_weights('Inception_finetuned.h5')  # always save your weights after training or during training