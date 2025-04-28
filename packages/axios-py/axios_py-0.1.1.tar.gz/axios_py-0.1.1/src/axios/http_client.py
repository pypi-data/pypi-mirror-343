"""
Custom HTTP client implementation
"""

import json
import urllib.parse
import urllib.request
import urllib.error
from typing import Any, Dict, Optional, Union
from urllib.error import HTTPError, URLError

class HTTPClient:
    """Custom HTTP client implementation"""
    
    def __init__(self, timeout: Optional[float] = None):
        self.timeout = timeout
        
    def request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        json_data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """Make an HTTP request"""
        # Prepare request data
        request_data = None
        if data is not None:
            if isinstance(data, (dict, list)):
                request_data = json.dumps(data).encode('utf-8')
            elif isinstance(data, str):
                request_data = data.encode('utf-8')
            elif isinstance(data, bytes):
                request_data = data
                
        # Prepare request headers
        request_headers = headers or {}
        if 'Content-Type' not in request_headers and request_data is not None:
            request_headers['Content-Type'] = 'application/json'
            
        # Add query parameters to URL
        if params:
            from urllib.parse import urlencode
            url += '?' + urlencode(params)
                
        # Create request
        req = urllib.request.Request(
            url,
            data=request_data,
            headers=request_headers,
            method=method.upper()
        )
        
        # Make request
        try:
            with urllib.request.urlopen(req, timeout=timeout or self.timeout) as response:
                response_data = response.read()
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
                
        except HTTPError as e:
            return {
                'status': e.code,
                'headers': dict(e.headers),
                'data': e.read().decode('utf-8') if e.read() else None
            }
        except URLError as e:
            # Return a more informative error response
            return {
                'status': 0,
                'headers': {},
                'data': None,
                'error': str(e)
            }
            
    def get(self, url: str, **kwargs) -> Dict[str, Any]:
        """Make a GET request"""
        return self.request('GET', url, **kwargs)
        
    def post(self, url: str, **kwargs) -> Dict[str, Any]:
        """Make a POST request"""
        return self.request('POST', url, **kwargs)
        
    def put(self, url: str, **kwargs) -> Dict[str, Any]:
        """Make a PUT request"""
        return self.request('PUT', url, **kwargs)
        
    def delete(self, url: str, **kwargs) -> Dict[str, Any]:
        """Make a DELETE request"""
        return self.request('DELETE', url, **kwargs)
        
    def patch(self, url: str, **kwargs) -> Dict[str, Any]:
        """Make a PATCH request"""
        return self.request('PATCH', url, **kwargs) 