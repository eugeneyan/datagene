from app import app
from flask import request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
# from categorize_title.title_categorize import title_categorize
# from categorize_image.image_categorize import image_categorize
# from image_search.image_search import image_search
from image_search.template_results import default_result, no_similar_result, bad_format_result, empty_submit_result
from route_utils import allowed_file
from utils.logger import logger

# Initialize main dir
MAIN_DIR = 'images'

# Set image upload folder
image_categorization_upload_folder = 'data/images_clothes/pred_images'
image_search_upload_folder = 'data/' + MAIN_DIR + '/search_image'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/acknowledgements')
def acknowledgements():
    return render_template('acknowledgements.html')


@app.route('/about_me')
def about_me():
    return render_template('about_me.html')


@app.route('/categorize_web', methods=['GET', 'POST'])
def categorize_web():
    """

    Returns top three category options for the title in web. If input form is empty, returns result suggesting user
    to type something in input form.

    :return:
    """
    if request.method == 'POST':
        # Read the posted values
        _title = request.form['title'].encode('utf-8')  # encode to utf 8
        logger.info('Title form input: {}'.format(_title))

        if len(_title) > 0:
            logger.debug('title from form: {}; type({})'.format(_title, type(_title)))
            result, elapsed_time = title_categorize(_title)

        else:  # No input
            result = {0: 'Enter a product title before submitting!'}
            elapsed_time = 0

    else:
        result = {0: 'Type something in the product title field.'}
        elapsed_time = 0

    for key, value in result.iteritems():
        logger.info('Result {}: {}'.format(key, value))

    logger.info('Time taken: {} ms'.format(elapsed_time))

    return render_template('categorize_web.html', result=result, elapsed_time=elapsed_time)


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
    result = title_categorize(_title)
    return jsonify(result)


@app.route('/image_categorize_web', methods=['GET', 'POST'])
def image_categorize_web():
    """

    Returns top three category options for uploaded image in web.

    :return:
    """
    if request.method == 'POST':
        _image = request.files['image']
        logger.debug('Image (categorize) received: {}'.format(_image.filename))

        # Check if file is allowed
        if _image and allowed_file(_image.filename):
            _image_filename = secure_filename(_image.filename)
            _image_savepath = os.path.join(image_categorization_upload_folder, _image_filename)
            _image.save(_image_savepath)

            # Image categorize
            result, elapsed_time = image_categorize(_image_savepath)

        elif _image and not allowed_file(_image.filename):
            result = {0: ('Image should have .png, .jpg, or .jpeg extension (case-insensitive).', 0)}
            elapsed_time = 0

        else:
            result = {0: ('Browse for an image before submitting!', 0)}
            elapsed_time = 0

    else:  # Request method is 'GET'
        result = {0: ('Select an image', 0)}
        elapsed_time = 0

    for key, value in result.iteritems():
        logger.info('Result {}: {}'.format(key, value))

    logger.info('Time taken: {} ms'.format(elapsed_time))

    return render_template('image_categorize_web.html', result=result, elapsed_time=elapsed_time)


@app.route('/image_search_web', methods=['GET', 'POST'])
def image_search_web():
    """

    Returns top ten similar image options for uploaded image in web.

    :return:
    """
    if request.method == 'POST':
        logger.debug('Request form: {}'.format(request.form))
        _category = request.form['category']
        _image = request.files['image']
        logger.info('Image (search) category received: {}'.format(_category))
        logger.debug('Image (search) image received: {}'.format(_image.filename))

        # Check if file is allowed
        if _image and allowed_file(_image.filename):
            _image_filename = secure_filename(_image.filename)
            _image_savepath = os.path.join(image_search_upload_folder, _image_filename)
            _image.save(_image_savepath)

            # Image Search
            result, elapsed_time = image_search(_image_savepath, _category)

        elif _image and not allowed_file(_image.filename):
            result = bad_format_result
            elapsed_time = 0

        else:
            result = empty_submit_result
            elapsed_time = 0

    else:  # Request method is 'GET'
        result = default_result
        elapsed_time = 0

    # Check if empty results

    if len(result) == 0:
        result = no_similar_result

    logger.debug('Result: {}'.format(result))
    for key, value in result.iteritems():
        logger.info('Result {}: {}'.format(key, value[1]))

    logger.info('Time taken: {} ms'.format(elapsed_time))

    return render_template('image_search_web.html', result=result, elapsed_time=elapsed_time)
