import datetime
import numpy as np
from keras.preprocessing import image
from image_utils import load_pretrained_model
from categorize.categorize_utils import load_dict
from utils.logger import logger


# Load deep learning model and dictionary
model = load_pretrained_model(model_name='resnet50', output_classes=65,
                              weights_path='data/images_clothes/model/resnet50_finetuned_4block.h5')
category_dict = load_dict('data/images_clothes/model/', dict_name='image_category_dict')
logger.debug(category_dict)
logger.info('Deep learning model and image category dictionary loaded')


class Image:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None
        logger.debug('Image received')

    def prepare(self):
        self.image = image.load_img(self.image_path, target_size=(224, 224))
        self.image = image.img_to_array(self.image)
        self.image = np.multiply(self.image, 1. / 255)
        self.image = np.expand_dims(self.image, axis=0)
        logger.debug('Image prepared')

        return self

    def categorize(self):
        start_time = datetime.datetime.now()

        preds = model.predict(self.image)

        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        elapsed_time = elapsed_time.total_seconds()
        logger.info('Time taken: {} secs'.format(elapsed_time))

        top = 5
        results = dict()

        top_indices = (-preds).argsort()[:, :top][0]
        for i, idx in enumerate(top_indices):
            category = category_dict[idx]
            prob = preds[0][idx]
            results[i] = (category, prob)

        return results, elapsed_time


def image_categorize_single(image_path):
    return Image(image_path).prepare().categorize()
