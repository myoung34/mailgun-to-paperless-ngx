""" Main initializer for flask """
import logging

from flask import Flask

from config import Config

logging.basicConfig(level=logging.DEBUG)

def create_app(config_class=Config):
    """ Initialize the app from a config """
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.main import \
        BP as main_bp  # pylint:disable=import-outside-toplevel
    app.register_blueprint(main_bp)

    return app
