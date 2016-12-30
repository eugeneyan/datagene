# -*- coding: utf-8 -*-
"""
Class to predict product category given a product title.
"""
from utils.logger import logger
from utils.decorators import timer
from data_prep.clean_titles import encode_string, tokenize_title_string, remove_words_list, remove_numeric_list, \
    remove_chars, STOP_WORDS, singularize_list, HTML_PARSER
from categorize_title.categorize_utils import load_dict, get_score

# Load dictionaries
tfidf_dict, int_to_category_dict = load_dict('data/model', 'categorization_dicts')
logger.info('Dictionary loaded in categorized.categorize_single')


class TitleCategorize:
    """
    Class to predict product category given a product title.
    """

    def __init__(self, title):
        self.title = title

    def prepare(self, excluded='-.'):
        """ (str) -> list(str)

        Returns the title after it has been prepared by the process from clean titles

        :return:
        >>> TitleCategorize('Crème brûlée &quot; &amp; &nbsp;').prepare()
        ['creme', 'brulee']
        >>> TitleCategorize('test hyphen-word 0.9 20% green/blue').prepare()
        ['test', 'hyphen-word', '0.9']
        >>> TitleCategorize('grapes come in purple and green').prepare()
        ['grapes', 'come']
        >>> TitleCategorize('what remains of a word ! if wordlen is 2').prepare()
        ['remains', 'word', 'wordlen']
        """

        self.title = encode_string(self.title, HTML_PARSER)
        self.title = self.title.lower()
        self.title = tokenize_title_string(self.title, excluded)
        self.title = remove_words_list(self.title, STOP_WORDS)
        self.title = remove_numeric_list(self.title)
        self.title = remove_chars(self.title, 1)
        self.title = singularize_list(self.title)
        logger.info('Title after preparation: {}'.format(self.title))
        return self

    def categorize(self):
        """ (CategorizeSingle(str)) -> dict

        Categorizes prepared title and returns a dictionary of form {1: 'Cat1', 2: 'Cat2', 3: 'Cat3}

        :return:
        >>> TitleCategorize('This is a bookshelf with wood and a clock').prepare().categorize()
        {1: 'Electronics -> Home Audio -> Stereo Components -> Speakers -> Bookshelf Speakers',
        2: 'Electronics -> Computers & Accessories -> Data Storage -> USB Flash Drives',
        3: 'Home & Kitchen -> Furniture -> Home Office Furniture -> Bookcases'}
        """
        result_list = get_score(self.title, tfidf_dict, int_to_category_dict, 3)
        result_dict = dict()
        for i, category in enumerate(result_list):
            result_dict[i + 1] = category

        return result_dict


@timer
def title_categorize(title):
    """ (str) -> dict

    Initializes given title as Title class and returns a dictionary of top 3 options.

    :param title:
    :return:
    """
    result = TitleCategorize(title).prepare().categorize()

    return result
