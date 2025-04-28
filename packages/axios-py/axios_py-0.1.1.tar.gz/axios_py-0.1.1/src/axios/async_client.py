"""
Async HTTP client implementation
"""

import json
import aiohttp
import asyncio
from typing import Any, Dict, Optional, Union
from .rate_limiter import RateLimitManager

class AsyncHTTPClient:
    """Async HTTP client implementation"""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limit_manager = RateLimitManager()
        
    async def __aenter__(self):
        """Enter async context manager"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context manager"""
        if self.session:
            await self.session.close()
            self.session = None
            
    async def request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        json_data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """Make an async HTTP request"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
        # Apply rate limiting
        await self.rate_limit_manager.acquire(url)
        
        try:
            async with self.session.request(
                method=method.upper(),
                url=url,
                params=params,
                data=data,
                json=json_data,
                headers=headers,
                timeout=timeout
            ) as response:
                response_data = await response.read()
                content_type = response.headers.get('Content-Type', '')
                
                # Parse response data
                if 'application/json' in content_type:
                    data = json.loads(response_data.decode('utf-8'))
                else:
                    data = response_data.decode('utf-8')
                    
                return {
                    'status': response.status,
                    'headers': dict(response.headers),
                    'data': data
                }
                
        except aiohttp.ClientError as e:
            raise Exception(f"Request failed: {str(e)}")
            
    async def get(self, url: str, **kwargs) -> Dict[str, Any]:
        """Make a GET request"""
        return await self.request('GET', url, **kwargs)
        
    async def post(self, url: str, **kwargs) -> Dict[str, Any]:
        """Make a POST request"""
        return await self.request('POST', url, **kwargs)
        
    async def put(self, url: str, **kwargs) -> Dict[str, Any]:
        """Make a PUT request"""
        return await self.request('PUT', url, **kwargs)
        
    async def delete(self, url: str, **kwargs) -> Dict[str, Any]:
        """Make a DELETE request"""
        return await self.request('DELETE', url, **kwargs)
        
    async def patch(self, url: str, **kwargs) -> Dict[str, Any]:
        """Make a PATCH request"""
        return await self.request('PATCH', url, **kwargs)
        
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