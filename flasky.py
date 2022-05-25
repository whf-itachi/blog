
from flask_migrate import Migrate

from app import create_app, db

app = create_app()
# migrate = Migrate(app, db)
# migrate.init_app(app, db)
# if __name__ == '__main__':
#     # app.debug = True
#     app.config['JSON_AS_ASCII'] = False
#     app.run(host='0.0.0.0', port=8083, debug=True)

