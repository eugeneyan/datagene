from app import app
from flask import request, jsonify
from categorize.categorize_single import categorize_single, load_dict
from utils.logger import logger


# Load dictionary
# tfidf_dict = load_dict('categorize', 'tfidf_dict_samp_small')


@app.route('/')
def index():
    """

    Returns the homepage for the Product API

    :return:
    """
    return 'Welcome to the Product API!'


@app.route('/categorize', methods=['POST'])
def categorize():
    """

    Returns top three category options for the title

    :return:
    """
    logger.info('Json received: {}'.format(request.json))

    # Read the posted values
    _title = request.json['title'].encode('utf-8')  # encode to utf 8
    logger.debug('_title from json: {}; type({})'.format(_title, type(_title)))

    # Categorize title
    result = categorize_single(_title)
    return jsonify(result)
