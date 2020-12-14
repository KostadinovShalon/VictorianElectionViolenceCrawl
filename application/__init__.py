import os
import crochet
from flask import Flask
from flask_cors import CORS

import db_session
import logging
import sys
import configuration


crochet.setup()


def create_app():
    print(configuration.server_variables())
    print(configuration.bna_variables())
    print(configuration.db_variables())
    db_var = configuration.db_variables()
    db_session.change_session_data(**db_var)
    logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import search
    app.register_blueprint(search.bp)

    from . import setup
    app.register_blueprint(setup.bp)
    CORS(app)

    return app
