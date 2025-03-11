"""
Paste model

This module contains a class for representing a paste.
"""

import datetime
from dataclasses import dataclass
from app.service.crypto import crypto


@dataclass
class PasteMeta:
    """
    Utility fields of a Paste.
    """

    user_id: str
    created_at: datetime
    expires_at: datetime


class Paste:
    """
    Class representing a paste.
    """

    def __init__(self, meta: PasteMeta, title, contents=None, to_encrypt=False):
        self.meta = meta
        self.title = crypto.encrypt(title) if to_encrypt else title
        self.contents = crypto.encrypt(contents) if to_encrypt else contents

    def to_dict(self, to_decrypt=False):
        """Return Paste as a dictionary.

        Args:
           to_decrypt: Flag signaling wether to decrypt encrypted fields (optional).
        """

        return {
            "user_id": self.meta.user_id,
            "created_at": self.meta.created_at,
            "expires_at": self.meta.expires_at,
            "title": crypto.decrypt(self.title) if to_decrypt else self.title,
            "contents": (
                crypto.decrypt(self.contents)
                if to_decrypt and self.contents
                else self.contents
            ),
        }

    @staticmethod
    def from_dict(source, encrypted):
        """Reconstruct Paste from the dictionary.

        Args:
           encrypted: Flag signaling wether the dictionary contains encrypted fields.
        """

        user_id = source.get("user_id")
        created_at = source.get("created_at")
        expires_at = source.get("expires_at")
        title = (
            crypto.decrypt(source.get("title")) if encrypted else source.get("title")
        )
        contents = (
            crypto.decrypt(source.get("contents"))
            if encrypted
            else source.get("contents", None)
        )
        return Paste(
            PasteMeta(user_id, created_at, expires_at),
            title,
            contents,
        )
