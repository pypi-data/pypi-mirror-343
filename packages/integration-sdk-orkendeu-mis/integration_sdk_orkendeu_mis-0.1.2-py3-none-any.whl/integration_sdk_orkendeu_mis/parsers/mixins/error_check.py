from typing import Any


class ParserError(Exception):
    pass


class ServiceUnavailableError(ParserError):
    pass


class SubjectNotFoundError(ParserError):
    pass


class ServerUnknownError(ParserError):
    def __init__(self, message: str, *, data: Any = None):
        super().__init__(message)
        self.data = data
