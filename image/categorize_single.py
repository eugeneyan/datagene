import datetime
import numpy as np
from keras.preprocessing import image
from image_utils import load_pretrained_model
from categorize.categorize_utils import load_dict
from utils.logger import logger
from utils.decorators import timer


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
        logger.info('Image received')

    def prepare(self):
        self.image = image.load_img(self.image_path, target_size=(224, 224))
        self.image = image.img_to_array(self.image)
        self.image = np.multiply(self.image, 1. / 255)
        self.image = np.expand_dims(self.image, axis=0)
        logger.info('Image prepared')

        return self

    def categorize(self):
        preds = model.predict(self.image)

        top = 5
        results = dict()

        top_indices = (-preds).argsort()[:, :top][0]
        for i, idx in enumerate(top_indices):
            category = category_dict[idx]
            prob = preds[0][idx]
            results[i] = (category, prob)

        return results


@timer
def image_categorize_single(image_path):
    """ (str) -> dict

    Initializes given image path as Image class and returns a dictionary of top 3 options

    :param title:
    :return:
    """

    result = Image(image_path).prepare().categorize()

    return result
