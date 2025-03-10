"""
Pyrebase manager

This module contains a class for managing Pyrebase operations.
"""

from pyrebase import initialize_app
from flask import current_app


class PyrebaseManager:
    """
    Pyrebase manager instance.

    Attributes:
        _firebase (pyrebase.Pyrebase): The Pyrebase object
        _firebase_auth (pyrebase.Auth): The Pyrebase authentication object
        _firebase_db (pyrebase.Database): The Pyrebase database object
    """

    def __init__(self):
        self._firebase = None
        self._firebase_auth = None
        self._firebase_db = None

    def init_pyrebase(self):
        """
        Initialize Pyrebase object.

        Args:
            app (flask.Flask): The Flask app
        """
        config = {
            "apiKey": current_app.config["BASE_API_KEY"],
            "authDomain": current_app.config["BASE_AUTH_DOMAIN"],
            "databaseURL": current_app.config["BASE_DB_URL"],
            "storageBucket": current_app.config["BASE_BUCKET"],
            # https://github.com/thisbejim/Pyrebase/issues/52#issuecomment-298182589
            "serviceAccount": {
                "client_email": current_app.config["FIREBASE_CLIENT_EMAIL"],
                "client_id": current_app.config["FIREBASE_CLIENT_ID"],
                "private_key": current_app.config["FIREBASE_PRIVATE_KEY"].replace(
                    "\\n", "\n"
                ),
                "private_key_id": current_app.config["FIREBASE_PRIVATE_KEY_ID"],
                "type": "service_account",
            },
        }

        self._firebase = initialize_app(config)
        self._firebase_auth = self._firebase.auth()
        self._firebase_db = self._firebase.database()

    def get_firebase(self):
        """Get Firebase object"""
        return self._firebase

    def get_firebase_auth(self):
        """Get Firebase auth object"""
        return self._firebase_auth

    def get_firebase_db(self):
        """Get Firebase database object"""
        return self._firebase_db


pyrebase = PyrebaseManager()
