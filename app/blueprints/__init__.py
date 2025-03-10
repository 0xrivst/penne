"""
Views package initialization.
"""

from app.blueprints.paste import paste_bp
from app.blueprints.auth import auth_bp
from app.blueprints.index import index_bp

blueprints = [paste_bp, auth_bp, index_bp]


def register_blueprints(app):
    """
    Register application blueprints.

    Args:
        app: Application instance
    """

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
