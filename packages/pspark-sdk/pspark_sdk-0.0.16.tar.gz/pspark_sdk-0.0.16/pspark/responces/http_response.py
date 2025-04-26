import json


class HttpResponse:
    def __init__(self, status_code: int, content: bytes = None):
        self._status_code = status_code
        self._content = content

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def content(self) -> bytes:
        return self._content

    def body(self) -> str:
        return self._content.decode("utf-8") if self._content is not None else ""

    def json(self) -> dict:
        try:
            return json.loads(self._content)
        except json.JSONDecodeError:
            raise ValueError("The content is not valid JSON")
