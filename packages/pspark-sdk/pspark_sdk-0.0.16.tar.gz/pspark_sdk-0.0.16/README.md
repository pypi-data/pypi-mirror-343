# PSPark Python SDK usage

You should have jwt-key and api-key keys to be able to use our API via this SDK. A jwt-key is a CSR file.

## Generating a CSR file

A Certificate Signing Request (.csr) file is required to authenticate an API user and to get your API-Key. The .csr file contains your API public key that will be used to validate the request signature. To generate your RSA 4096 private key (stored in pspakr_secret.key) for signing requests, use the following command line:

```
openssl req -new -newkey rsa:4096 -nodes -keyout pspakr_secret.key -out pspark_public_key.csr
```

Make sure you keep the API secret key (**pspark_secret.key**) safe and secure. Do not share your API secret key with anyone. To get your API-key you should upload your pspark_public_key in the [cabinet.pspark.io](https://cabinet.pspark.io).

## Installation

`pip install pspark-sdk`

## Request examples

Bellow shown a simple example of SDK usage.

```python
from pspark import PSPark
from pspark.requests import BalancesRequest


sdk = PSPark(jwt_key='jwt-key', api_key='api-key')

response = sdk.get_balances(BalancesRequest())
```

For async request you have to use `PSParkAsync`.

```python
import asyncio
from pspark import PSParkAsync
from pspark.requests import TransactionRequest


sdk = PSParkAsync(jwt_key='jwt-key', api_key='api-key')

async def async_main():
    response = await sdk.get_transaction_status(TransactionRequest(
        wallet_id="08a03be1-aefa-4695-8186-b52411b4f240",
        reference="7555e4a7-f464-43b1-859e-950f445dc7d4",
    ))


asyncio.run(async_main())
```

> More request examples can find [here](docs).

## Validation errors

The API doesn't implement all RESTFull API requirements and has its own response structure.

All HTTP responses from the server will have 200 status code. So, if your request will have some validation errors, the code, and it's description will be presented in the response body as shown bellow.

Response Example

```json
{
  "code": 1002,
  "message": "error description",
  "data": {
    //... some data
  }
}
```

Each time when the server's response will have some validation errors, the SDK will throw `ResponseValidationError`.
