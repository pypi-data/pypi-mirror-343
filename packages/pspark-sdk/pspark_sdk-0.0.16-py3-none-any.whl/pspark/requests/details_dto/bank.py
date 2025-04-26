from dataclasses import dataclass
from typing import Optional

from ..abstract_request import AbstractRequest


@dataclass
class Bank(AbstractRequest):
    id: Optional[str] = None
    name: Optional[str] = None
    account: Optional[str] = None
    bic_code: Optional[str] = None
