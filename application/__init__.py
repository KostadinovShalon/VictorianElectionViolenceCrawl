import os
import crochet
from flask import Flask
from flask_cors import CORS

from db import db_session
import logging
import sys
import configuration


crochet.setup()


def create_app():
    db_var = configuration.db_variables()
    db_session.change_session_data(db_var["user"], db_var["password"], db_var["host"])
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

    from . import search, setup, candidates, portal
    app.register_blueprint(search.bp)
    app.register_blueprint(setup.bp)
    app.register_blueprint(candidates.bp)
    app.register_blueprint(portal.bp)

    CORS(app)

    return app
