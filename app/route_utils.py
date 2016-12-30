"""
Utilities for use in app serving
"""


def allowed_file(filename):
    filename = filename.lower()
    return '.' in filename and filename.rsplit('.', 1)[1] in {'png', 'jpg', 'jpeg'}
