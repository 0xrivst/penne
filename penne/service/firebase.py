"""
Firebase manager

This module contains a class for managing Firebase admin operations.
"""

from flask import current_app
from firebase_admin.credentials import Certificate
from firebase_admin import firestore, initialize_app


class FirebaseManager:
    """
    Firebase admin instance.

    Attributes:
        _firebase: Firebase admin object
        _firestore: Firebase firestore object
        _pastes_collection: Firebase collection for pastes
    """

    def __init__(self):
        self._firebase = None
        self._firestore = None
        self._pastes_collection = None

    def init_firebase(self):
        """
        Initialize Firebase admin object.

        Args:
            app: The Flask app
        """
        credentials = {
            "type": "service_account",
            "project_id": current_app.config["FIREBASE_PROJECT_ID"],
            "private_key_id": current_app.config["FIREBASE_PRIVATE_KEY_ID"],
            "private_key": current_app.config["FIREBASE_PRIVATE_KEY"].replace(
                r"\n", "\n"
            ),
            "client_email": current_app.config["FIREBASE_CLIENT_EMAIL"],
            "client_id": current_app.config["FIREBASE_CLIENT_ID"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": current_app.config[
                "FIREBASE_AUTH_PROVIDER_X509_CERT_URL"
            ],
            "client_x509_cert_url": current_app.config["AUTH_PROVIDER_X509_CERT_URL"],
        }
        certificate = Certificate(credentials)
        self._firebase = initialize_app(certificate)
        self._firestore = firestore.client()
        self._pastes_collection = self._firestore.collection("pastes")

    def get_firebase(self):
        """Get Firebase admin object"""
        return self._firebase

    def get_firestore(self):
        """Get Firebase firestore object"""
        return self._firestore

    def get_pastes_collection(self):
        """Get Firebase collection for pastes"""
        return self._pastes_collection


firebase = FirebaseManager()
