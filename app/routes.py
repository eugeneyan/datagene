from app import app
from flask import request, jsonify, render_template
from categorize.categorize_single import categorize_single
from utils.logger import logger


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/categorize_web', methods=['GET', 'POST'])
def categorize_web():
    """

    Returns top three category options for the title in web. If input form is empty, returns result suggesting user
    to type something in input form.

    :return:
    """
    if request.method == 'POST':
        logger.info('Title form input: {}'.format(request.form['title']))

        # Read the posted values
        _title = request.form['title'].encode('utf-8')  # encode to utf 8
        logger.debug('title from form: {}; type({})'.format(_title, type(_title)))
        result = categorize_single(_title)
    else:
        result = {0: 'Type something in the Product Title field =)'}

    for key, value in result.iteritems():
        logger.info('Result {}: {}'.format(key, value))

    return render_template('categorize_web.html', result=result)


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
