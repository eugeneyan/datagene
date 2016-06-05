from data_prep.prep_title_category import *
from utils.logger import logger


def test_get_category_lvl1():

    # Test when multiple lists
    assert get_category_lvl1("[['A', 'B', 'C'], ['D', 'E', 'F', 'G']]") == 'A'

    # Test when one list
    assert get_category_lvl1("[['P1', 'P2', 'P3', 'P4']]") == 'P1'

    # Test when one item in list
    assert get_category_lvl1("[['A']]") == 'A'

    # Test when empty List
    assert get_category_lvl1("[['']]") == 'no_category'

    logger.info('Tests for get_category_lvl1 passed!')


def test_get_category_path():

    # Test when multiple lists
    assert get_category_path("[['A', 'B', 'C'], ['D', 'E', 'F', 'G']]") == 'A -> B -> C'

    # Test when one list
    assert get_category_path("[['P1', 'P2', 'P3', 'P4']]") == 'P1 -> P2 -> P3 -> P4'

    # Test when one item in list
    assert get_category_path("[['A']]") == 'A'

    # Test when empty List
    assert get_category_path("[['']]") == 'no_category'

    logger.info('Tests for get_category_lvl1 passed!')
