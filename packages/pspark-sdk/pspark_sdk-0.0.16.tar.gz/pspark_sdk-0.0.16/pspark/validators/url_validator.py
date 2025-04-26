from typing import Optional
from urllib.parse import urlparse


def validate_url(url: Optional[str]):
    if url is None:
        return

    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        raise ValueError(f"Invalid URL: {url}")
