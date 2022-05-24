
import os

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app import create_app


app, db = create_app()


if __name__ == '__main__':
    # app.debug = True
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8083, debug=True)

