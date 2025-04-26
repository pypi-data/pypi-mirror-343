from typing import Optional

import httpx

from .abstract_http_client_wrapper import AbstractHttpClientWrapper
from ..enums import ApiURL, ApiVersion, HttpMethod
from ..exceptions import HttpException, HttpTimeoutException
from ..helpers import make_header, make_url
from ..responces import HttpResponse


class HttpxAsyncWrapper(AbstractHttpClientWrapper):
    async def send_request(
        self,
        path: ApiURL,
        url_params: Optional[dict] = None,
        body: dict = None,
        method: HttpMethod = HttpMethod.POST,
    ) -> HttpResponse:
        url = make_url(
            self._base_url, ApiVersion.get_default().value, path.value, url_params
        )
        http_client = httpx.AsyncClient(timeout=self._timeout, verify=self._ssl_verify)

        try:
            response = await http_client.request(
                method=method.value,
                url=url,
                headers=make_header(body, self._jwt_key, self._api_key),
                json=body,
            )

            response.raise_for_status()

            result = HttpResponse(response.status_code, response.content)
        except httpx.HTTPStatusError as e:
            result = HttpResponse(e.response.status_code, e.response.content)
        except httpx.TimeoutException:
            raise HttpTimeoutException()
        except httpx.HTTPError as e:
            raise HttpException(str(e))
        finally:
            await http_client.aclose()

        self.raise_for_status(url, result)
        self.raise_for_response(result)

        return result
