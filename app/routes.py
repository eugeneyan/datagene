from app import app
from flask import request, jsonify, render_template
from categorize.categorize_single import categorize_single
from utils.logger import logger


# Load dictionary
# tfidf_dict = load_dict('categorize', 'categorization_dicts_small')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/categorize')
def categorize_form():
    return render_template('categorize.html')


@app.route('/categorize_result', methods=['POST'])
def categorize_post():
    logger.info('Form received: {}'.format(request.form['title']))

    # Read the posted values
    _title = request.form['title'].encode('utf-8')  # encode to utf 8
    logger.debug('title from form: {}; type({})'.format(_title, type(_title)))

    # Categorize title
    result = categorize_single(_title)
    return render_template('result.html', result=result)


@app.route('/categorize_api', methods=['POST'])
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
