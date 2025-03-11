from flask import Flask

from app.blueprints import register_blueprints
from app.service.pyrebase import pyrebase
from app.service.asset import AssetManager
from app.service.crypto import crypto
from app.service.firebase import firebase
from app.util.filters import register_filters


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    with app.app_context():
        AssetManager().init_asset_manager()
        crypto.init_crypto()
        pyrebase.init_pyrebase()
        firebase.init_firebase()
        register_filters()

    register_blueprints(app)

    return app
