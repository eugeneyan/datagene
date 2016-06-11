# -*- coding: utf-8 -*-
from data_prep.clean_titles import *
from utils.logger import logger


def test_list_to_string():

    assert list_to_string(['A', 'B', 'C']) == 'A B C'
    assert list_to_string(['A', 'B', '']) == 'A B '
    logger.info('Tests for list to string passed!')


def test_encode_string():

    assert encode_string('crème brûlée') == 'creme brulee'
    assert encode_string('åöûëî') == 'aouei'
    logger.info('Tests for encode string passed!')


def test_tokenize_title_string():

    # Test regular tokenization of words
    assert tokenize_title_string('hello world') == ['hello', 'world']

    # Test tokenization with special characters
    assert tokenize_title_string('test hyphen-word 0.9 20% green/blue') == \
        ['test', 'hyphen-word', '0.9', '20%', 'green/blue']

    logger.info('Tests for tokenize string passed!')


def test_remove_words():

    # Test removal of stop words
    assert remove_words(['python', 'is', 'the', 'best'], STOP_WORDS) == ['python', 'best']

    # Test removal of colours
    assert remove_words(['grapes', 'come', 'in', 'purple', 'and', 'green'], STOP_WORDS) == ['grapes', 'come']

    # Test removal of spam words
    assert remove_words(['spammy', 'title', 'intl', 'import', 'export'], STOP_WORDS) == ['spammy', 'title']

    logger.info('Test for removal of stop words passed!')


def test_remove_chars():

    # Test removal of 1 char words
    assert remove_chars(['what', 'remains', 'of', 'a', 'word', '!', ''], 1) == ['what', 'remains', 'of', 'word']

    # Test removal of 2 char words
    assert remove_chars(['what', 'remains', 'of', 'a', 'word', '!', '', 'if', 'word_len', 'is', '2'], 2) == \
        ['what', 'remains', 'word', 'word_len']

    logger.info('Test for removal of words with x char length passed!')


def test_remove_duplicate_words():

    assert remove_duplicate_words(['A', 'B', 'A', 'C']) == set(['A', 'C', 'B'])
    assert remove_duplicate_words(['A', 'B', 'B', 'C', 'C', 'D', 'D']) == set(['A', 'C', 'B', 'D'])
    logger.info('Test for removal of duplicate words passed!')


def test_title_token_count():

    assert title_token_count(['A', 'B', 'C']) == 3
    assert title_token_count([]) == 0
    logger.info('Test for title token count passed!')
