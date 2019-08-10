from flask import Flask
from flask import redirect, url_for
import os
import logging


# Create flask app and configure it
def create_app(config_class: str):
    app = Flask(__name__, static_url_path='/app/')
    app.config.from_object(f'iambic.config.{config_class.capitalize()}')

    from .resources import api
    api.init_app(app)

    from .models import db
    db.init_app(app)

    from .exceptions import register_handlers
    register_handlers(app)

    from .logic import validator
    validator.load(app.config['DICTIONARY_PATH'])

    logging.basicConfig(level=app.config['LOGGING_LEVEL'])

    @app.route('/')
    def index():
        return redirect(url_for('static', filename='index.html'))

    return app

if __name__ == '__main__':
    environment = os.environ.get('IAMBIC_ENV', 'development')
    print(environment)
    app = create_app(environment)
    app.run()
