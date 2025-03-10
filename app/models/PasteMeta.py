import datetime
from dataclasses import dataclass


@dataclass
class PasteMeta:
    """
    Utility fields of a Paste.
    """

    user_id: str
    created_at: datetime
    expires_at: datetime
    paste_id: str = None
