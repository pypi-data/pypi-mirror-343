class HttpException(Exception):
    def __init__(self, message: str = "Unknown HTTP exceptions") -> None:
        super().__init__(message)
