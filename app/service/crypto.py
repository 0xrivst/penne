"""
Crypto manager

This module contains a class for managing encryption and decryption of pastes.
"""

import os
import base64
from flask import current_app
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV

NONCE_SIZE_BYTES = 12


class CryptoService:
    """
    Encryption service instance.

    Attributes:
        _key: Encryption key
        _aes_gcm_siv: AES-GCM-SIV cipher instance
    """

    def __init__(self):
        self._key = None
        self._aes_gcm_siv = None

    def init_crypto(self):
        """
        Initialize the encryption and decryption keys from the configuration.

        Args:
            app: The Flask app
        """
        self._key = base64.b64decode(
            bytes(current_app.config["ENCRYPTION_KEY"], "utf-8")
        )
        self._aes_gcm_siv = AESGCMSIV(self._key)

    def encrypt(self, plaintext):
        """
        Encrypt a given plaintext string.

        Args:
            plaintext: The plaintext string

        Returns:
            Base64-encoded ciphertext
        """
        nonce = os.urandom(NONCE_SIZE_BYTES)
        ciphertext = self._aes_gcm_siv.encrypt(nonce, plaintext.encode(), None)

        return base64.b64encode(bytearray(nonce + ciphertext)).decode()

    def decrypt(self, ciphertext):
        """
        Decrypt a given ciphertext string.

        Args:
            ciphertext: Base64-encoded ciphertext

        Returns:
            Decrypted plaintext
        """
        ciphertext_dec = base64.b64decode(ciphertext.encode())
        nonce = ciphertext_dec[:12]
        text = ciphertext_dec[12:]

        return self._aes_gcm_siv.decrypt(nonce, text, None).decode()


crypto = CryptoService()
