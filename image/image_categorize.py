from image.image_utils import prepare_image
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


class ImageCategorize:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None
        self.image_width = 224
        self.image_height = 224
        logger.info('Image (categorize) initialized')

    def prepare(self):
        self.image = prepare_image(self.image_path, self.image_width, self.image_height)
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
def image_categorize(image_path):
    """ (str) -> dict

    Initializes given image path as Image class and returns a dictionary of top 3 options

    :param title:
    :return:
    """

    result = ImageCategorize(image_path).prepare().categorize()

    return result
