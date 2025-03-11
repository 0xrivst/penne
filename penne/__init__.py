"""
The main module where the Flask app is created.
"""

import os
from flask import Flask
from penne.blueprints import register_blueprints
from penne.service.pyrebase import pyrebase
from penne.service.asset import AssetManager
from penne.service.crypto import crypto
from penne.service.firebase import firebase
from penne.util.filters import register_filters
from penne.config import config

config_name = os.environ.get("FLASK_CONFIG", "dev")


def create_app():
    """
    Initializes the Flask app
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    with app.app_context():
        AssetManager().init_asset_manager()
        crypto.init_crypto()
        pyrebase.init_pyrebase()
        firebase.init_firebase()
        register_filters()

    register_blueprints(app)

    return app
