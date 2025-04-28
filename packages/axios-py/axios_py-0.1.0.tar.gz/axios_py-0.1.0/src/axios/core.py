"""
Core Axios implementation with sync and async support
"""

from typing import Any, Dict, Optional, Union
from .types import AxiosRequestConfig, AxiosResponse
from .http_client import HTTPClient
from .async_client import AsyncHTTPClient
from .rate_limiter import RateLimitManager

class Axios:
    """Axios HTTP client implementation with sync and async support"""
    
    def __init__(self, config: Optional[AxiosRequestConfig] = None):
        self.config = config or AxiosRequestConfig()
        self.http_client = HTTPClient()
        self.async_client = AsyncHTTPClient()
        self.rate_limit_manager = RateLimitManager()
        
    async def __aenter__(self):
        """Enter async context manager"""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context manager"""
        if hasattr(self.async_client, 'session') and self.async_client.session:
            await self.async_client.session.close()
            self.async_client.session = None
        
    def request(self, config: AxiosRequestConfig) -> AxiosResponse:
        """Make a synchronous HTTP request"""
        # Merge instance config with request config
        merged_config = self._merge_configs(self.config, config)
        
        # Make request using HTTP client
        response = self.http_client.request(
            method=merged_config.method,
            url=merged_config.url,
            params=merged_config.params,
            data=merged_config.data,
            json_data=merged_config.json,
            headers=merged_config.headers,
            timeout=merged_config.timeout
        )
        
        # Create AxiosResponse
        return AxiosResponse(
            data=response['data'],
            status=response['status'],
            status_text="OK" if 200 <= response['status'] < 300 else "Error",
            headers=response['headers'],
            config=merged_config
        )
        
    async def arequest(self, config: AxiosRequestConfig) -> AxiosResponse:
        """Make an asynchronous HTTP request"""
        # Merge instance config with request config
        merged_config = self._merge_configs(self.config, config)
        
        # Make request using async HTTP client
        response = await self.async_client.request(
            method=merged_config.method,
            url=merged_config.url,
            params=merged_config.params,
            data=merged_config.data,
            json_data=merged_config.json,
            headers=merged_config.headers,
            timeout=merged_config.timeout
        )
        
        # Create AxiosResponse
        return AxiosResponse(
            data=response['data'],
            status=response['status'],
            status_text="OK" if 200 <= response['status'] < 300 else "Error",
            headers=response['headers'],
            config=merged_config
        )
    
    # Synchronous methods
    def get(self, url: str, config: Optional[AxiosRequestConfig] = None) -> AxiosResponse:
        """Make a synchronous GET request"""
        if config is None:
            config = AxiosRequestConfig()
        config.method = 'GET'
        config.url = url
        return self.request(config)
    
    def post(self, url: str, data: Optional[Any] = None, config: Optional[AxiosRequestConfig] = None) -> AxiosResponse:
        """Make a synchronous POST request"""
        if config is None:
            config = AxiosRequestConfig()
        config.method = 'POST'
        config.url = url
        config.data = data
        return self.request(config)
    
    def put(self, url: str, data: Optional[Any] = None, config: Optional[AxiosRequestConfig] = None) -> AxiosResponse:
        """Make a synchronous PUT request"""
        if config is None:
            config = AxiosRequestConfig()
        config.method = 'PUT'
        config.url = url
        config.data = data
        return self.request(config)
    
    def delete(self, url: str, config: Optional[AxiosRequestConfig] = None) -> AxiosResponse:
        """Make a synchronous DELETE request"""
        if config is None:
            config = AxiosRequestConfig()
        config.method = 'DELETE'
        config.url = url
        return self.request(config)
    
    def patch(self, url: str, data: Optional[Any] = None, config: Optional[AxiosRequestConfig] = None) -> AxiosResponse:
        """Make a synchronous PATCH request"""
        if config is None:
            config = AxiosRequestConfig()
        config.method = 'PATCH'
        config.url = url
        config.data = data
        return self.request(config)
    
    # Asynchronous methods
    async def aget(self, url: str, config: Optional[AxiosRequestConfig] = None) -> AxiosResponse:
        """Make an asynchronous GET request"""
        if config is None:
            config = AxiosRequestConfig()
        config.method = 'GET'
        config.url = url
        return await self.arequest(config)
    
    async def apost(self, url: str, data: Optional[Any] = None, config: Optional[AxiosRequestConfig] = None) -> AxiosResponse:
        """Make an asynchronous POST request"""
        if config is None:
            config = AxiosRequestConfig()
        config.method = 'POST'
        config.url = url
        config.data = data
        return await self.arequest(config)
    
    async def aput(self, url: str, data: Optional[Any] = None, config: Optional[AxiosRequestConfig] = None) -> AxiosResponse:
        """Make an asynchronous PUT request"""
        if config is None:
            config = AxiosRequestConfig()
        config.method = 'PUT'
        config.url = url
        config.data = data
        return await self.arequest(config)
    
    async def adelete(self, url: str, config: Optional[AxiosRequestConfig] = None) -> AxiosResponse:
        """Make an asynchronous DELETE request"""
        if config is None:
            config = AxiosRequestConfig()
        config.method = 'DELETE'
        config.url = url
        return await self.arequest(config)
    
    async def apatch(self, url: str, data: Optional[Any] = None, config: Optional[AxiosRequestConfig] = None) -> AxiosResponse:
        """Make an asynchronous PATCH request"""
        if config is None:
            config = AxiosRequestConfig()
        config.method = 'PATCH'
        config.url = url
        config.data = data
        return await self.arequest(config)
    
    def set_rate_limit(
        self,
        endpoint: Optional[str] = None,
        requests_per_second: float = 1.0,
        burst_size: int = 1
    ) -> None:
        """Set rate limit for an endpoint or globally"""
        if endpoint:
            self.rate_limit_manager.set_endpoint_limit(
                endpoint,
                requests_per_second,
                burst_size
            )
        else:
            self.rate_limit_manager.set_default_limit(
                requests_per_second,
                burst_size
            )
        self.async_client.set_rate_limit(endpoint, requests_per_second, burst_size)
    
    def _merge_configs(self, base: AxiosRequestConfig, override: AxiosRequestConfig) -> AxiosRequestConfig:
        """Merge two config objects, with override taking precedence"""
        merged = AxiosRequestConfig()
        
        # Copy base config
        for field in merged.__annotations__:
            setattr(merged, field, getattr(base, field))
        
        # Override with non-None values from override config
        for field in merged.__annotations__:
            override_value = getattr(override, field)
            if override_value is not None:
                setattr(merged, field, override_value)
        
        return merged 