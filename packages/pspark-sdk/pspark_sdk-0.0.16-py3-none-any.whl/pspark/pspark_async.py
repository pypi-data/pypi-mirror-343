from .abstract_pspark import AbstractPSPark
from .enums import ApiURL
from .http_client_wrappers import HttpxAsyncWrapper
from .requests import (
    AddressRequest,
    BalanceRequest,
    BalancesRequest,
    InvoiceRequest,
    RateRequest,
    TransactionRequest,
    WithdrawalRequest,
)
from .responces import HttpResponse


class PSParkAsync(AbstractPSPark):
    def _init_client(self):
        self._client = HttpxAsyncWrapper(
            jwt_key=self._jwt_key,
            api_key=self._api_key,
            base_url=self._get_base_url(),
            timeout=self._timeout,
            ssl_verify=not self._is_debug_mode,
        )

    async def get_balances(self, balances_request: BalancesRequest) -> HttpResponse:
        return await self._client.send_request(
            path=ApiURL.BALANCES,
            body=balances_request.as_dict(),
        )

    async def get_balance(self, balance_request: BalanceRequest) -> HttpResponse:
        return await self._client.send_request(
            path=ApiURL.WALLET_BALANCE,
            url_params={"wallet_id": balance_request.wallet_id},
            body=balance_request.as_dict(),
        )

    async def create_address(self, address_request: AddressRequest) -> HttpResponse:
        return await self._client.send_request(
            path=ApiURL.WALLET_ADDRESS_CREATE,
            url_params={"wallet_id": address_request.wallet_id},
            body=address_request.as_dict(),
        )

    async def create_withdrawal(
        self, withdrawal_request: WithdrawalRequest
    ) -> HttpResponse:
        return await self._client.send_request(
            path=ApiURL.WALLET_WITHDRAWAL_CREATE,
            url_params={"wallet_id": withdrawal_request.wallet_id},
            body=withdrawal_request.as_dict(),
        )

    async def create_invoice(self, invoice_request: InvoiceRequest) -> HttpResponse:
        return await self._client.send_request(
            path=ApiURL.WALLET_INVOICE_CREATE,
            url_params={"wallet_id": invoice_request.wallet_id},
            body=invoice_request.as_dict(),
        )

    async def get_transaction_status(
        self, transaction_request: TransactionRequest
    ) -> HttpResponse:
        return await self._client.send_request(
            path=ApiURL.TRANSACTION_STATUS,
            url_params={"wallet_id": transaction_request.wallet_id},
            body=transaction_request.as_dict(),
        )

    async def get_rates(self, rates_request: RateRequest) -> HttpResponse:
        return await self._client.send_request(
            path=ApiURL.RATES,
            body=rates_request.as_dict(),
        )
