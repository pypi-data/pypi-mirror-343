import os
from abc import ABC, abstractmethod

from .constants import (
    BASE_URL,
    CUSTOM_BASE_URL_OPTION,
    DEBUG_MODE_OPTION,
    REQUEST_TIMEOUT,
)


class AbstractPSPark(ABC):
    def __init__(
        self,
        jwt_key: str,
        api_key: str,
        timeout: float = REQUEST_TIMEOUT,
        options: dict = None,
    ):
        self._jwt_key = jwt_key
        self._api_key = api_key
        self._timeout = timeout
        self._options = options if options is not None else {}
        self._is_debug_mode = (
            (DEBUG_MODE_OPTION in self._options)
            and (self._options[DEBUG_MODE_OPTION])
            and (os.getenv("TYPE_ENV") != "production")
        )

        self._init_client()

    @abstractmethod
    def _init_client(self):
        """Abstract method that must be implemented in subclasses"""
        pass

    def _get_base_url(self) -> str:
        if CUSTOM_BASE_URL_OPTION in self._options:
            return self._options[CUSTOM_BASE_URL_OPTION]

        return BASE_URL
