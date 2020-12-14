import os
import crochet
from flask import Flask
from flask_cors import CORS

import db_session
import logging
import sys


crochet.setup()


def create_app(test_config=None):

    db_session.change_session_data('root', 'marr1982', '127.0.0.1')
    logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import search
    app.register_blueprint(search.bp)
    CORS(app)

    return app
