import time
from typing import Optional

from jose import jwt


def make_url(
    base_url: str, version: str, path: str, url_params: Optional[dict] = None
) -> str:
    base_url = base_url.rstrip("/")

    if url_params is not None:
        for key, value in url_params.items():
            path = path.replace(f":{key}", value)

    return f"{base_url}/{version}/{path}"


def make_header(payload: dict, jwt_key: str, api_key: str) -> dict:
    payload["iat"] = int(time.time())
    payload["exp"] = int(time.time()) + 50
    signature = jwt.encode(payload, jwt_key, algorithm="RS256")

    return {"X-Api-Key": api_key, "Authorization": f"Bearer {signature}"}
