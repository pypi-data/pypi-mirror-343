class ResponseValidationException(Exception):
    def __init__(self, message: str, code: int) -> None:
        self.message = message
        self.code = code

        super().__init__(message, code)
