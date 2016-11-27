"""
Utils for use in routes
"""


def allowed_file(filename):
    filename = filename.lower()
    return '.' in filename and filename.rsplit('.', 1)[1] in {'png', 'jpg', 'jpeg'}
