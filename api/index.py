"""
Vercel entry point for the Flask app
"""

import sys
from pathlib import Path
from penne import create_app

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

app = create_app()


def handler(event, context):
    return app(event, context)


if __name__ == "__main__":
    app.run(debug=True)
