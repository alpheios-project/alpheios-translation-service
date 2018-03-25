import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import config
from .errors import register_error_handler

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()


def create_app(config_name="dev", config_objects=config):
    """ Create the application and returns it's instance and DB """
    app = Flask(
        __name__
    )
    app.config.from_object(config_objects[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    config[config_name].init_app(app)

    # Set up extensions
    db.init_app(app)

    # Register Jinja template functions
    from .main.latin import latin_api
    app.register_blueprint(latin_api)

    # Register error handler
    register_error_handler(app)

    return app, db
