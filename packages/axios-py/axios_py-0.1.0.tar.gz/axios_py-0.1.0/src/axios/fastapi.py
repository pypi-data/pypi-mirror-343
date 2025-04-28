"""
FastAPI integration for axios-py
"""

from typing import Optional
from fastapi import Depends
from .core import Axios
from .types import AxiosRequestConfig

class AxiosDependency:
    """FastAPI dependency for Axios client"""
    
    def __init__(self, config: Optional[AxiosRequestConfig] = None):
        self.config = config
        
    async def __call__(self) -> Axios:
        """Create and return an Axios instance"""
        async with Axios(config=self.config) as client:
            yield client

def get_axios(config: Optional[AxiosRequestConfig] = None) -> AxiosDependency:
    """Get an Axios dependency for FastAPI"""
    return AxiosDependency(config) 