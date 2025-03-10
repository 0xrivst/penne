from flask import Flask

from app.views import register_blueprints
from app.service.pyrebase import pyrebase
from app.service.asset import AssetManager


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    with app.app_context():
        pyrebase.init_pyrebase()
        AssetManager().init_asset_manager()

    register_blueprints(app)

    return app
