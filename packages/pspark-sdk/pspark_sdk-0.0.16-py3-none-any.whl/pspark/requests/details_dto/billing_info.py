from dataclasses import dataclass
from typing import Optional

from ..abstract_request import AbstractRequest


@dataclass
class BillingInfo(AbstractRequest):
    address: Optional[str] = None
    country_code: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    post_code: Optional[str] = None
    region: Optional[str] = None
    state: Optional[str] = None
    payment_purpose: Optional[str] = None
    street: Optional[str] = None
