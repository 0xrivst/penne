"""
Views package initialization.
"""

from app.blueprints.paste import paste_bp
from app.blueprints.auth import auth_bp
from app.blueprints.main import main_bp

blueprints = [paste_bp, auth_bp, main_bp]


def register_blueprints(app):
    """
    Register application blueprints.

    Args:
        app: Application instance
    """

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
