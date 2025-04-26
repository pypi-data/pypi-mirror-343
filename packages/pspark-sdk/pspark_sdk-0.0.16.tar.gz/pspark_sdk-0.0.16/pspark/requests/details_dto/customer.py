from dataclasses import dataclass
from typing import Optional

from ..abstract_request import AbstractRequest


@dataclass
class Customer(AbstractRequest):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    customer_id: Optional[str] = None
    national_id: Optional[str] = None
    taxpayer_identification_number: Optional[str] = None
    birthdate: Optional[str] = None
