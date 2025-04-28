"""
Type definitions for Axios
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Union, Callable

@dataclass
class AxiosRequestConfig:
    """Configuration for Axios requests"""
    url: str = ""
    method: str = "GET"
    headers: Optional[Dict[str, str]] = None
    params: Optional[Dict[str, Any]] = None
    data: Optional[Union[Dict[str, Any], str, bytes]] = None
    json: Optional[Any] = None
    timeout: Optional[float] = None
    response_type: str = "json"
    validate_status: Optional[Callable[[int], bool]] = None

@dataclass
class AxiosResponse:
    """Response from Axios request"""
    data: Any
    status: int
    status_text: str
    headers: Dict[str, str]
    config: AxiosRequestConfig 