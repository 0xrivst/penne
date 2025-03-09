"""
Configuration classes for different environments.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Base configuration class for the application. See README.md for variable information."""

    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    BASE_API_KEY = os.getenv("BASE_API_KEY")
    BASE_AUTH_DOMAIN = os.getenv("BASE_AUTH_DOMAIN")
    BASE_DB_URL = os.getenv("BASE_DB_URL")
    BASE_BUCKET = os.getenv("BASE_BUCKET")
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
    FIREBASE_CLIENT_EMAIL = os.getenv("FIREBASE_CLIENT_EMAIL")
    FIREBASE_CLIENT_ID = os.getenv("FIREBASE_CLIENT_ID")
    FIREBASE_PRIVATE_KEY = os.getenv("FIREBASE_PRIVATE_KEY")
    FIREBASE_PRIVATE_KEY_ID = os.getenv("FIREBASE_PRIVATE_KEY_ID")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")


class DevConfig(BaseConfig):
    """Configuration class for development environments."""

    DEBUG = True


class ProdConfig(BaseConfig):
    """Configuration class for production environments."""

    DEBUG = False


config = {"dev": DevConfig, "prod": ProdConfig}
