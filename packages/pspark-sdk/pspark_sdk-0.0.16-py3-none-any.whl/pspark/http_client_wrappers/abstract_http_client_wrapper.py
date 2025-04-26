from abc import ABC

from ..exceptions import (
    HttpClientException,
    HttpRedirectionException,
    HttpServerException,
    ResponseValidationException,
)
from ..responces import HttpResponse


class AbstractHttpClientWrapper(ABC):  # noqa: B024
    def __init__(
        self,
        jwt_key: str,
        api_key: str,
        base_url: str,
        timeout: float,
        ssl_verify: bool = True,
    ):
        self._jwt_key = jwt_key
        self._api_key = api_key
        self._base_url = base_url
        self._timeout = timeout
        self._ssl_verify = ssl_verify

    @staticmethod
    def raise_for_status(url: str, response: HttpResponse):
        if response.status_code >= 500:
            raise HttpServerException(url, response)
        elif response.status_code >= 400:
            raise HttpClientException(url, response)
        elif response.status_code >= 300:
            raise HttpRedirectionException(url, response)

    @staticmethod
    def raise_for_response(response: HttpResponse):
        response_data = response.json()

        if "code" in response_data and response_data["code"] != 0:
            raise ResponseValidationException(
                response_data["message"], response_data["code"]
            )
