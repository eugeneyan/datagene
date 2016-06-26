import sys
sys.path.insert(0, '/var/www/html/datagene/flaskapp.wsgi')

from app.routes import app as application