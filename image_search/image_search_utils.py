"""
Utility functions used in image search
"""
import numpy as np
from scipy.spatial.distance import cosine


def get_cosine_similarity_scipy(row, search_image_features):
    """

    Returns cosine similarity between two 1-row arrays

    :param row:
    :param search_image_features:
    :return:
    """
    return 1 - cosine(row, search_image_features)


def cosine_similarity_scipy(search_image_features, search_features):
    """

    Return cosine similarity between search image features (1-row array) and search features (n-row array)

    :param search_image_features:
    :param search_features:
    :return:
    """
    return np.apply_along_axis(get_cosine_similarity_scipy, axis=1, arr=search_features,
                               search_image_features=search_image_features)
