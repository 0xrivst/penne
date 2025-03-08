import sys
from app import create_app
from config import config

if __name__ == "__main__":
    config_name = sys.argv[1] if len(sys.argv) > 1 else "dev"

    app = create_app(config[config_name])
    app.run()
