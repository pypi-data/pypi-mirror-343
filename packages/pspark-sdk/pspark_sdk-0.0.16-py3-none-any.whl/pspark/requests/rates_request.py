import time
from dataclasses import dataclass

from .abstract_request import AbstractRequest


@dataclass
class RateRequest(AbstractRequest):
    currency_from: str
    currency_to: str
    nonce: int = time.time_ns()
