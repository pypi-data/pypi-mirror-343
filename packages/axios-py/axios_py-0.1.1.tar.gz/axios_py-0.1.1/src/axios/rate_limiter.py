"""
Rate limiter implementation using token bucket algorithm
"""

import time
import asyncio
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class RateLimitConfig:
    """Configuration for rate limiting"""
    requests_per_second: float = 1.0
    burst_size: int = 1
    max_queue_size: int = 100

class RateLimiter:
    """Rate limiter using token bucket algorithm"""
    
    def __init__(self, config: Optional[RateLimitConfig] = None):
        self.config = config or RateLimitConfig()
        self.tokens = self.config.burst_size
        self.last_update = time.time()
        self.lock = asyncio.Lock()
        
    async def acquire(self) -> None:
        """Acquire a token, waiting if necessary"""
        async with self.lock:
            while self.tokens <= 0:
                now = time.time()
                time_passed = now - self.last_update
                new_tokens = time_passed * self.config.requests_per_second
                
                if new_tokens > 0:
                    self.tokens = min(
                        self.config.burst_size,
                        self.tokens + new_tokens
                    )
                    self.last_update = now
                    
                if self.tokens <= 0:
                    await asyncio.sleep(1.0 / self.config.requests_per_second)
                    
            self.tokens -= 1
            
    def update_config(self, config: RateLimitConfig) -> None:
        """Update rate limit configuration"""
        self.config = config
        self.tokens = min(self.tokens, config.burst_size)

class RateLimitManager:
    """Manages rate limits for different endpoints"""
    
    def __init__(self):
        self.limiters: Dict[str, RateLimiter] = {}
        self.default_limiter = RateLimiter()
        
    def get_limiter(self, endpoint: str) -> RateLimiter:
        """Get or create a rate limiter for an endpoint"""
        if endpoint not in self.limiters:
            self.limiters[endpoint] = RateLimiter()
        return self.limiters[endpoint]
        
    def set_endpoint_limit(
        self,
        endpoint: str,
        requests_per_second: float,
        burst_size: int = 1
    ) -> None:
        """Set rate limit for a specific endpoint"""
        config = RateLimitConfig(
            requests_per_second=requests_per_second,
            burst_size=burst_size
        )
        self.get_limiter(endpoint).update_config(config)
        
    def set_default_limit(
        self,
        requests_per_second: float,
        burst_size: int = 1
    ) -> None:
        """Set default rate limit"""
        config = RateLimitConfig(
            requests_per_second=requests_per_second,
            burst_size=burst_size
        )
        self.default_limiter.update_config(config)
        
    async def acquire(self, endpoint: Optional[str] = None) -> None:
        """Acquire a token for an endpoint"""
        if endpoint and endpoint in self.limiters:
            await self.limiters[endpoint].acquire()
        else:
            await self.default_limiter.acquire() 