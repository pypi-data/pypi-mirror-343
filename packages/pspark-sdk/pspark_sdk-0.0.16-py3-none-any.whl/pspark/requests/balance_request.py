import time
from dataclasses import dataclass

from .abstract_request import AbstractRequest


@dataclass
class BalanceRequest(AbstractRequest):
    wallet_id: str
    nonce: int = time.time_ns()

    def _get_excluded_properties(self):
        return ["wallet_id"]
