"""
uwsgi file
"""
from app.routes import app  # uwsgi expects a variable called application
# http://stackoverflow.com/questions/12030809/flask-and-uwsgi-unable-to-load-app-0-mountpoint-callable-not-found-or-im
# To get around this, in uwsgi.ini we set callable = app


if __name__ == '__main__':
    app.run()
