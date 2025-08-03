"""
Cache Management Utilities for Zomato V3
========================================

Utilities for Redis cache management, invalidation, and monitoring.
"""

import time
import logging
from typing import Optional, List, Dict, Any

try:
    from fastapi_cache2 import FastAPICache
    FASTAPI_CACHE2_AVAILABLE = True
except ImportError:
    FASTAPI_CACHE2_AVAILABLE = False

try:
    from redis import Redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from redis_config import redis_config

# Setup logging
logger = logging.getLogger(__name__)

class CacheManager:
    """Cache management utilities"""
    
    def __init__(self):
        self.redis_client: Optional[Redis] = None
    
    def init_redis_client(self):
        """Initialize Redis client for direct operations"""
        if not REDIS_AVAILABLE:
            logger.warning("Redis not available - cache operations will be limited")
            return
            
        try:
            self.redis_client = Redis(
                host=redis_config.REDIS_HOST,
                port=redis_config.REDIS_PORT,
                password=redis_config.REDIS_PASSWORD,
                db=redis_config.REDIS_DB,
                decode_responses=True
            )
            # Test connection
            self.redis_client.ping()
            logger.info("Redis client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Redis client: {e}")
            self.redis_client = None
    
    async def clear_namespace(self, namespace: str) -> int:
        """Clear all keys in a specific namespace"""
        if not REDIS_AVAILABLE or not self.redis_client:
            logger.warning("Redis not available - using fallback cache clearing")
            try:
                from fallback_cache import memory_cache
                return memory_cache.clear_namespace(namespace)
            except Exception:
                return 0
                
        try:
            pattern = f"{namespace}:*"
            keys = self.redis_client.keys(pattern)
            
            if keys:
                deleted = self.redis_client.delete(*keys)
                logger.info(f"Cleared {deleted} keys from namespace '{namespace}'")
                return deleted
            return 0
        except Exception as e:
            logger.error(f"Failed to clear namespace '{namespace}': {e}")
            return 0
    
    async def clear_all_cache(self) -> Dict[str, int]:
        """Clear all caches and return statistics"""
        if not REDIS_AVAILABLE or not self.redis_client:
            logger.warning("Redis not available - using fallback cache clearing")
            try:
                from fallback_cache import memory_cache
                cleared = memory_cache.clear_all()
                return {"total": cleared}
            except Exception:
                return {}
                
        try:
            stats = {}
            namespaces = [
                redis_config.RESTAURANT_NAMESPACE,
                redis_config.MENU_NAMESPACE,
                redis_config.CUSTOMER_NAMESPACE,
                redis_config.ORDER_NAMESPACE,
                redis_config.REVIEW_NAMESPACE
            ]
            
            for namespace in namespaces:
                deleted = await self.clear_namespace(namespace)
                stats[namespace] = deleted
            
            logger.info("Cleared all caches")
            return stats
        except Exception as e:
            logger.error(f"Failed to clear all caches: {e}")
            return {}
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if not REDIS_AVAILABLE or not self.redis_client:
            logger.info("Redis not available - returning fallback cache stats")
            try:
                from fallback_cache import memory_cache
                return memory_cache.get_stats()
            except Exception:
                return {"error": "No cache available"}
                
        try:
            info = self.redis_client.info()
            
            # Get keys by namespace
            namespace_stats = {}
            namespaces = [
                redis_config.RESTAURANT_NAMESPACE,
                redis_config.MENU_NAMESPACE,
                redis_config.CUSTOMER_NAMESPACE,
                redis_config.ORDER_NAMESPACE,
                redis_config.REVIEW_NAMESPACE
            ]
            
            for namespace in namespaces:
                pattern = f"{namespace}:*"
                keys = self.redis_client.keys(pattern)
                namespace_stats[namespace] = {
                    "key_count": len(keys),
                    "keys": keys[:10] if keys else []  # Show first 10 keys
                }
            
            return {
                "redis_info": {
                    "used_memory": info.get("used_memory_human"),
                    "connected_clients": info.get("connected_clients"),
                    "total_commands_processed": info.get("total_commands_processed"),
                    "keyspace_hits": info.get("keyspace_hits"),
                    "keyspace_misses": info.get("keyspace_misses"),
                    "uptime_in_seconds": info.get("uptime_in_seconds")
                },
                "namespace_stats": namespace_stats,
                "cache_hit_ratio": self._calculate_hit_ratio(info)
            }
        except Exception as e:
            logger.error(f"Failed to get cache stats: {e}")
            return {"error": str(e)}
    
    def _calculate_hit_ratio(self, info: Dict) -> float:
        """Calculate cache hit ratio"""
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total = hits + misses
        
        if total == 0:
            return 0.0
        
        return round((hits / total) * 100, 2)
    
    async def invalidate_restaurant_cache(self, restaurant_id: Optional[int] = None):
        """Invalidate restaurant-related caches"""
        try:
            if restaurant_id:
                # Clear specific restaurant cache
                key = f"{redis_config.RESTAURANT_NAMESPACE}:detail:{restaurant_id}"
                if self.redis_client:
                    self.redis_client.delete(key)
                logger.info(f"Invalidated cache for restaurant {restaurant_id}")
            
            # Clear list and search caches
            await self.clear_namespace(redis_config.RESTAURANT_NAMESPACE)
        except Exception as e:
            logger.error(f"Failed to invalidate restaurant cache: {e}")
    
    def log_cache_performance(self, endpoint: str, cache_hit: bool, response_time: float):
        """Log cache performance metrics"""
        status = "HIT" if cache_hit else "MISS"
        logger.info(
            f"CACHE {status} - Endpoint: {endpoint} - Response Time: {response_time:.3f}ms"
        )

# Global cache manager instance
cache_manager = CacheManager()

def timing_decorator(func):
    """Decorator to measure response time"""
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Log timing info
        func_name = func.__name__
        logger.info(f"Function {func_name} executed in {response_time:.3f}ms")
        
        return result
    return wrapper
