"""
Vercel entry point for the Flask app
"""

import os
import sys
from pathlib import Path
from penne import create_app

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
os.environ.setdefault("FLASK_CONFIG", "prod")


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
