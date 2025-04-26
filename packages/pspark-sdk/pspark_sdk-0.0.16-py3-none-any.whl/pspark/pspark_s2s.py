from .pspark_async import PSParkAsync
from .pspark import PSPark
from .enums import ApiURL
from .requests import InvoiceRequest
from .responces import HttpResponse


class PSParkS2s(PSPark):
    def create_invoice(self, invoice_request: InvoiceRequest) -> HttpResponse:
        return self._client.send_request(
            path=ApiURL.WALLET_INVOICE_S2S_CREATE,
            url_params={"wallet_id": invoice_request.wallet_id},
            body=invoice_request.as_dict(),
        )


class PSParkS2sAsync(PSParkAsync):
    async def create_invoice(self, invoice_request: InvoiceRequest) -> HttpResponse:
        return await self._client.send_request(
            path=ApiURL.WALLET_INVOICE_S2S_CREATE,
            url_params={"wallet_id": invoice_request.wallet_id},
            body=invoice_request.as_dict(),
        )
