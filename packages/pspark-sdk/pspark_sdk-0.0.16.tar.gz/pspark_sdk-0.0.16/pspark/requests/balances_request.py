import time
from dataclasses import dataclass

from .abstract_request import AbstractRequest


@dataclass
class BalancesRequest(AbstractRequest):
    nonce: int = time.time_ns()
