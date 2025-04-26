from dataclasses import dataclass
from typing import Optional

from ..abstract_request import AbstractRequest


@dataclass
class Ui(AbstractRequest):
    language: Optional[str] = None
