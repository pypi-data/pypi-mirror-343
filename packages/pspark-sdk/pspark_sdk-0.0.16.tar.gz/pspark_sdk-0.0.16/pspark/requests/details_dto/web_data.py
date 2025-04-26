from dataclasses import dataclass
from typing import Optional

from ..abstract_request import AbstractRequest


@dataclass
class WebData(AbstractRequest):
    ip: Optional[str] = None
    user_agent: Optional[str] = None
    browser_color_depth: Optional[int] = None
    browser_language: Optional[str] = None
    browser_screen_height: Optional[int] = None
    browser_screen_width: Optional[int] = None
    browser_timezone: Optional[str] = None
    browser_timezone_offset: Optional[int] = None
    browser_java_enabled: Optional[bool] = None
    browser_java_script_enabled: Optional[bool] = None
    browser_accept_header: Optional[str] = None
