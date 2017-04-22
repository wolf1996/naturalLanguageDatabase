class Error(Exception):
    """Base exception for this module"""
    pass


class SyntaxNetError(Error):
    """Exception raised if syntaxnet fails.

    Attributes:
        expression -- input expression in which the error occurred
        message -- error log
    """
    def __init__(self, message):
        self.message = message
