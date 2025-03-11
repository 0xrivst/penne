"""
Views package initialization.
"""

from penne.blueprints.paste import paste_bp
from penne.blueprints.auth import auth_bp
from penne.blueprints.main import main_bp

blueprints = [paste_bp, auth_bp, main_bp]


def register_blueprints(app):
    """
    Register application blueprints.

    Args:
        app: Application instance
    """

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
