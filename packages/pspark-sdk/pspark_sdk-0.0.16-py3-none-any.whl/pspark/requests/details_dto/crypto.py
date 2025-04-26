from dataclasses import dataclass
from typing import Optional

from ..abstract_request import AbstractRequest


@dataclass
class Crypto(AbstractRequest):
    memo: Optional[str] = None
