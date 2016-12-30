"""
Class to suggest similar images and products given an input image.
"""
import numpy as np
import itertools
from sklearn.metrics.pairwise import cosine_similarity
from dl_models.inception_v3_flatterned import InceptionV3
from categorize_title.categorize_utils import load_dict
from categorize_image.image_categorize_utils import prepare_image
from image_search_utils import cosine_similarity_scipy, cdist_scipy
from scipy.spatial.distance import cdist
from utils.logger import logger
from utils.decorators import timer

# Initialize main dir
MAIN_DIR = 'images'

# Load search dictionaries and features
index_asin_dict, category_index_dict, index_asin_filter_dict, asin_dict = load_dict(
    'data/' + MAIN_DIR + '/search_dicts', 'search_dicts')
logger.info('Dictionary loaded in image_search.image_search')

search_features_path = 'data/' + MAIN_DIR + '/search_features/search_features.npy'
logger.info('Loading image features from {}'.format(search_features_path))
search_features = np.load(open(search_features_path))
logger.info('Search features loaded in image_search.image_search')

# Add index to search features
category_labels = list(itertools.chain.from_iterable([tup[0]] * tup[1] for tup in category_index_dict.values()))
category_labels.sort()
search_features = np.insert(search_features, 0, category_labels, axis=1)
logger.info('Category labels added in search features')

# Create list of valid categories
valid_categories = category_index_dict.keys() + ['All']

# Load model
model = InceptionV3(include_top=False, weights='imagenet', input_tensor=None)
logger.info('InceptionV3 loaded in image_search.image_search')


class ImageSearch:
    """
    Class to suggest similar images and products given an input image.
    """

    def __init__(self, image_path, category_filter='All'):
        self.image_path = image_path
        self.image = None
        self.image_width = 299
        self.image_height = 299
        self.category_filter = category_filter
        self.category_filter_index = -1
        self.similarity_threshold = 0.60
        self.n_results = 12
        logger.info('Image (search) initialized')

        # If category_filter missing, set to 'All'
        if self.category_filter == '':
            self.category_filter = 'All'

        assert self.category_filter in valid_categories, 'Category "{}" invalid'.format(self.category_filter)

    def get_category_filter_index(self):
        logger.info('Category filter: {}'.format(self.category_filter))
        if self.category_filter == 'All':
            self.category_filter_index = -1
        else:
            self.category_filter_index = category_index_dict[self.category_filter][0]

        logger.info('Image (search) category filter index derived: {}'.format(self.category_filter_index))
        return self

    def prepare(self):
        self.image = prepare_image(self.image_path, self.image_width, self.image_height)
        logger.info('Image (search) prepared')
        return self

    def search_similar(self):

        # Featurize search image
        search_image = model.predict(self.image)
        logger.info('Image (search) featurized')

        # Filter search features if necessary
        if self.category_filter_index == -1:
            logger.info('No filter applied')
            search_features_filtered = search_features[:, 1:]
            image_lookup_dict = index_asin_dict
        else:
            logger.info('Filter applied: {}'.format(self.category_filter_index))
            category_filter = search_features[:, 0] == self.category_filter_index
            search_features_filtered = search_features[category_filter, 1:]
            image_lookup_dict = index_asin_filter_dict[self.category_filter_index]

        # Get cosine similarity
        csim = cosine_similarity(search_image, search_features_filtered)[0]  # Fastest with using most memory
        # csim = cosine_similarity_scipy(search_image, search_features_filtered)  # Slowest but use least memory
        # csim = cdist_scipy(search_image, search_features_filtered)  # Faster with moderate memory use
        logger.info('Image (search) cosine similiarity calculated')

        # Get index of similar features
        similar_images = np.argsort(-csim)[:self.n_results]

        # Exclude similar images below the similarity threshold
        similar_images = [idx for idx in similar_images if csim[idx] > self.similarity_threshold]
        logger.info('Image (search) indices: {}'.format(similar_images))

        # Initialize result dict
        results = dict()
        result_index = 0

        for index in similar_images:
            asin = image_lookup_dict[index]
            results[result_index] = asin_dict[asin]
            result_index += 1

        logger.info('Image (search) searched')
        logger.debug('Image (search) result: {}'.format(results))
        return results


@timer
def image_search(image_path, category_filter='All'):
    """

    Initializes given image path as ImageSearch class and returns a dictionary of top 5 options

    :param image_path:
    :return:
    """
    return ImageSearch(image_path, category_filter).get_category_filter_index().prepare().search_similar()
