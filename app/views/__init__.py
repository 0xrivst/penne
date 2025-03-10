"""
Views package initialization.
"""

from app.views.paste import paste_bp
from app.views.auth import auth_bp
from app.views.index import index_bp

blueprints = [paste_bp, auth_bp, index_bp]


def register_blueprints(app):
    """
    Register application blueprints.

    Args:
        app: Application instance
    """

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
