from app import app
from flask import request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from categorize.categorize_single import categorize_single
from image.categorize_single import image_categorize_single
from route_utils import allowed_file
from utils.logger import logger


# Set image upload folder
image_upload_folder = 'data/images_clothes/pred_images'


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


@app.route('/image_categorize_web', methods=['GET', 'POST'])
def image_categorize_web():
    """

    Returns top three category options for uploaded image in web. If input form is empty, returns result suggesting user
    to type something in input form.

    :return:
    """
    if request.method == 'POST':
        _image = request.files['image']
        logger.debug('Image received: {}'.format(_image.filename))

        # Check if file is allowed
        if _image and allowed_file(_image.filename):
            _image_filename = secure_filename(_image.filename)
            _image_savepath = os.path.join(image_upload_folder, _image_filename)
            _image.save(_image_savepath)

            # Read the posted values
            result, elapsed_time = image_categorize_single(_image_savepath)

        else:
            result = {0: ('Image should have either .png, .jpg, or .jpeg extensions (case-insensitive)', 0)}
            elapsed_time = 0

    else:
        result = {0: ('Select an image', 0)}
        elapsed_time = 0

    for key, value in result.iteritems():
        logger.info('Result {}: {}'.format(key, value))
        logger.info('Time taken: {} sec'.format(elapsed_time))

    return render_template('image_categorize_web.html', result=result, elapsed_time=elapsed_time)
