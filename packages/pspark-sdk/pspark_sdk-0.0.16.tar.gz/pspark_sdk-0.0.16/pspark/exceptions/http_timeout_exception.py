from .http_exception import HttpException


class HttpTimeoutException(HttpException):
    def __init__(self):
        super().__init__("The requests timeout was reached.")
