from dataclasses import dataclass
from typing import Optional

from .abstract_request import AbstractRequest
from .details_dto import (
    Bank,
    BillingInfo,
    CardData,
    Crypto,
    Customer,
    EscrowPayment,
    Ui,
    WebData,
)


@dataclass
class Details(AbstractRequest):
    customer: Optional[Customer] = None
    billing_info: Optional[BillingInfo] = None
    crypto: Optional[Crypto] = None
    bank: Optional[Bank] = None
    escrow_payment: Optional[EscrowPayment] = None
    ui: Optional[Ui] = None
    web_data: Optional[WebData] = None
    card_data: Optional[CardData] = None
