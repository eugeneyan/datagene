import numpy as np
import itertools
from sklearn.metrics.pairwise import cosine_similarity
from dl_models.inception_v3_flatterned import InceptionV3
from categorize.categorize_utils import load_dict
from image.image_categorize_utils import prepare_image
from image_search_utils import cosine_similarity_scipy
from utils.logger import logger
from utils.decorators import timer

# Initialize main dir
MAIN_DIR = 'images'

# Load search dictionaries and features
index_asin_dict, category_index_dict, index_asin_filter_dict, asin_dict = load_dict('data/' + MAIN_DIR + '/search_dicts',
                                                                                    'search_dicts')
logger.info('Dictionary loaded in image_search.image_search')
search_features = np.load(open('data/' + MAIN_DIR + '/search_features/search_features.npy'))
logger.info('Search features loaded in image_search.image_search')

# Add index to search features
category_labels = list(itertools.chain.from_iterable([tup[0]] * tup[1] for tup in category_index_dict.values()))
category_labels.reverse()
search_features = np.insert(search_features, 0, category_labels, axis=1)

# Create list of valid categories
valid_categories = category_index_dict.keys() + ['All']

# Load model
model = InceptionV3(include_top=False, weights='imagenet', input_tensor=None)


class ImageSearch:

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

        assert self.category_filter in valid_categories, 'Category "{}" invalid'.format(self.category_filter)

    def get_category_filter_index(self):
        if self.category_filter == 'All':
            self.category_filter_index = -1
        else:
            self.category_filter_index = category_index_dict[self.category_filter][0]

        logger.info('Image (search) category filter index derived')
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
            search_features_filtered = search_features[:, 1:]
            image_lookup_dict = index_asin_dict
        else:
            category_filter = search_features[:, 0] == self.category_filter_index
            search_features_filtered = search_features[category_filter, 1:]
            image_lookup_dict = index_asin_filter_dict[self.category_filter_index]

        # Get cosine similarity
        # csim = cosine_similarity(search_image, search_features_filtered)[0]  # Uses too much memory
        csim = cosine_similarity_scipy(search_image, search_features_filtered)  # Slower but use less memory
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
            # image_path, title, category = asin_dict[asin]
            # image_path = image_path.replace('data/' + MAIN_DIR, '../static')
            # results[result_index] = (image_path, title, category)
            results[result_index] = asin_dict[asin]
            result_index += 1

        logger.info('Image (search) searched')
        logger.info('Image (search) result: {}'.format(results))
        return results


@timer
def image_search(image_path, category_filter='All'):
    """

    Initializes given image path as ImageSearch class and returns a dictionary of top 5 options

    :param image_path:
    :return:
    """
    return ImageSearch(image_path, category_filter).get_category_filter_index().prepare().search_similar()
