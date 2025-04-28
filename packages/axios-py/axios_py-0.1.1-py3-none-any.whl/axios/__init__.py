"""
Axios HTTP client for Python with sync and async support
"""

from .core import Axios
from .types import AxiosRequestConfig, AxiosResponse
from .http_client import HTTPClient
from .async_client import AsyncHTTPClient
from .rate_limiter import RateLimitManager, RateLimitConfig

__version__ = "0.1.0"
__all__ = [
    "Axios",
    "AxiosRequestConfig",
    "AxiosResponse",
    "HTTPClient",
    "AsyncHTTPClient",
    "RateLimitManager",
    "RateLimitConfig"
] 