from enum import Enum


class ApiURL(Enum):
    RATES = "rates"
    BALANCES = "balances"
    WALLET_BALANCE = "wallet/:wallet_id/balance"
    WALLET_ADDRESS_CREATE = "wallet/:wallet_id/address/create"
    WALLET_INVOICE_CREATE = "wallet/:wallet_id/invoice/create"
    WALLET_INVOICE_S2S_CREATE = "wallet/:wallet_id/invoice-s2s/create"
    WALLET_WITHDRAWAL_CREATE = "wallet/:wallet_id/withdrawal/create"
    TRANSACTION_STATUS = "wallet/:wallet_id/transaction/status"

    def with_wallet_id(self, wallet_id: str) -> str:
        return self.value.replace(":wallet_id", wallet_id)
