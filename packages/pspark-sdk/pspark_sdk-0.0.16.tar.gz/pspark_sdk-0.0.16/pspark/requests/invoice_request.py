import time
from dataclasses import dataclass
from typing import Optional

from .abstract_request import AbstractRequest
from .details import Details
from ..validators import validate_url


@dataclass
class InvoiceRequest(AbstractRequest):
    wallet_id: str
    reference: str
    amount: float
    return_url: str
    details: Optional[Details] = None
    title: Optional[str] = None
    description: Optional[str] = None
    callback_url: Optional[str] = None
    nonce: int = time.time_ns()

    def __post_init__(self):
        validate_url(self.callback_url)
        validate_url(self.return_url)

    def _get_excluded_properties(self):
        return ["wallet_id"]
