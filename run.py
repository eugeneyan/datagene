"""
Run Product API app

Sample call:
python run.py 0.0.0.0 6688
python run.py 127.0.0.1 6688
"""
import sys
from app.routes import app


if __name__ == '__main__':
    # host = sys.argv[1]
    # port_number = sys.argv[2]
    # app.run(host=host, port=int(port_number), debug=True)  # Note: this will run two instances of the app
    app.run()