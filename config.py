import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")


class DevConfig(BaseConfig):
    DEBUG = True


class ProdConfig(BaseConfig):
    DEBUG = False


config = {"dev": DevConfig, "prod": ProdConfig}
