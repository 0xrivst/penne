import PasteMeta


class Paste:
    """
    Class representing the Paste object.
    """

    def __init__(self, meta: PasteMeta, title, contents=None, to_encrypt=False):
        self.meta = meta
        self.title = encrypt(title) if to_encrypt else title
        self.contents = encrypt(contents) if to_encrypt else contents
