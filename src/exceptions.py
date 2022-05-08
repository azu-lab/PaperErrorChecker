class Error(Exception):
    """Base class for exception in this module."""


class NotImplementedError(Exception):
    def __init__(self, message: str = '') -> None:
        self.message = message
