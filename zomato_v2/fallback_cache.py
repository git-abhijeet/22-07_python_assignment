"""
Fallback Cache Implementation for Zomato V2
===========================================

This module provides a fallback caching mechanism when Redis is not available.
It uses in-memory caching with TTL support as a backup solution.
"""

import time
import asyncio
import logging
from typing import Any, Optional, Dict, Callable
from functools import wraps

logger = logging.getLogger(__name__)

class MemoryCache:
    """Simple in-memory cache with TTL support"""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._enabled = True
    
    def set(self, key: str, value: Any, expire: int = 300):
        """Set a value in cache with TTL"""
        if not self._enabled:
            return
        
        expiry_time = time.time() + expire
        self._cache[key] = {
            'value': value,
            'expires': expiry_time
        }
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache"""
        if not self._enabled or key not in self._cache:
            return None
        
        entry = self._cache[key]
        
        # Check if expired
        if time.time() > entry['expires']:
            del self._cache[key]
            return None
        
        return entry['value']
    
    def delete(self, key: str):
        """Delete a key from cache"""
        if key in self._cache:
            del self._cache[key]
    
    def clear_namespace(self, namespace: str) -> int:
        """Clear all keys with a specific namespace prefix"""
        pattern = f"{namespace}:"
        keys_to_delete = [key for key in self._cache.keys() if key.startswith(pattern)]
        
        for key in keys_to_delete:
            del self._cache[key]
        
        return len(keys_to_delete)
    
    def clear_all(self) -> int:
        """Clear all cache entries"""
        count = len(self._cache)
        self._cache.clear()
        return count
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_keys = len(self._cache)
        
        # Count by namespace
        namespaces = {}
        for key in self._cache.keys():
            if ':' in key:
                namespace = key.split(':', 1)[0]
                namespaces[namespace] = namespaces.get(namespace, 0) + 1
        
        return {
            "cache_type": "memory",
            "total_keys": total_keys,
            "namespaces": namespaces,
            "status": "operational" if self._enabled else "disabled"
        }
    
    def disable(self):
        """Disable caching"""
        self._enabled = False
        self._cache.clear()
    
    def enable(self):
        """Enable caching"""
        self._enabled = True

# Global memory cache instance
memory_cache = MemoryCache()

def fallback_cache(namespace: str = "default", expire: int = 300):
    """
    Decorator for fallback caching when Redis is not available
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key based on function name and arguments
            cache_key = f"{namespace}:{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache
            cached_result = memory_cache.get(cache_key)
            if cached_result is not None:
                logger.info(f"MEMORY CACHE HIT - {func.__name__}")
                return cached_result
            
            # Cache miss - execute function
            start_time = time.time()
            result = await func(*args, **kwargs)
            response_time = (time.time() - start_time) * 1000
            
            # Store in cache
            memory_cache.set(cache_key, result, expire)
            
            logger.info(f"MEMORY CACHE MISS - {func.__name__} - {response_time:.3f}ms")
            return result
        
        return wrapper
    return decorator

def invalidate_cache_namespace(namespace: str):
    """Helper function to invalidate cache by namespace"""
    deleted = memory_cache.clear_namespace(namespace)
    logger.info(f"Invalidated {deleted} keys from namespace '{namespace}'")
    return deleted
