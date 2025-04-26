import time
from dataclasses import dataclass
from typing import Optional

from .abstract_request import AbstractRequest
from ..validators import validate_url


@dataclass
class AddressRequest(AbstractRequest):
    wallet_id: str
    reference: str
    title: Optional[str] = None
    description: Optional[str] = None
    time_limit: Optional[int] = None
    callback_url: Optional[str] = None
    nonce: int = time.time_ns()

    def __post_init__(self):
        validate_url(self.callback_url)

    def _get_excluded_properties(self):
        return ["wallet_id"]
