"""
Advanced Cache Manager for Zomato V2 - Restaurant-Menu System
=============================================================

Sophisticated caching utilities with hierarchical invalidation,
performance monitoring, and multi-level cache strategies.
"""

import time
import logging
import hashlib
from typing import Optional, List, Dict, Any, Tuple
from functools import wraps

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

class AdvancedCacheManager:
    """Advanced cache management with hierarchical invalidation"""
    
    def __init__(self):
        self.redis_client: Optional[Redis] = None
        self.performance_stats = {
            "cache_hits": 0,
            "cache_misses": 0,
            "total_requests": 0,
            "total_response_time": 0,
            "slow_queries": 0
        }
    
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
            logger.info("Advanced Redis client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Redis client: {e}")
            self.redis_client = None
    
    def generate_cache_key(self, namespace: str, key_pattern: str, **kwargs) -> str:
        """Generate consistent cache keys with namespace"""
        key = key_pattern.format(**kwargs)
        return f"{namespace}:{key}"
    
    def generate_search_key(self, query_params: Dict[str, Any]) -> str:
        """Generate deterministic key for search queries"""
        # Sort parameters for consistent hashing
        sorted_params = sorted(query_params.items())
        param_string = str(sorted_params)
        query_hash = hashlib.md5(param_string.encode()).hexdigest()[:12]
        return query_hash
    
    async def hierarchical_invalidate_restaurant(self, restaurant_id: int):
        """Hierarchical cache invalidation for restaurant updates"""
        if not REDIS_AVAILABLE or not self.redis_client:
            return await self._fallback_invalidate_restaurant(restaurant_id)
        
        try:
            # Build invalidation patterns
            patterns_to_clear = [
                f"{redis_config.RESTAURANT_NAMESPACE}:*{restaurant_id}*",
                f"{redis_config.RESTAURANT_MENUS_NAMESPACE}:*{restaurant_id}*",
                f"{redis_config.SEARCH_RESULTS_NAMESPACE}:*",  # Clear all searches
                f"{redis_config.ANALYTICS_NAMESPACE}:*{restaurant_id}*",
                f"{redis_config.CATEGORIES_NAMESPACE}:*{restaurant_id}*",
                f"{redis_config.DIETARY_NAMESPACE}:*{restaurant_id}*"
            ]
            
            total_cleared = 0
            for pattern in patterns_to_clear:
                keys = self.redis_client.keys(pattern)
                if keys:
                    cleared = self.redis_client.delete(*keys)
                    total_cleared += cleared
            
            logger.info(f"Hierarchical invalidation: cleared {total_cleared} keys for restaurant {restaurant_id}")
            return total_cleared
            
        except Exception as e:
            logger.error(f"Failed hierarchical invalidation for restaurant {restaurant_id}: {e}")
            return 0
    
    async def hierarchical_invalidate_menu_item(self, menu_item_id: int, restaurant_id: int):
        """Hierarchical cache invalidation for menu item updates"""
        if not REDIS_AVAILABLE or not self.redis_client:
            return await self._fallback_invalidate_menu_item(menu_item_id, restaurant_id)
        
        try:
            # Build invalidation patterns for menu item changes
            patterns_to_clear = [
                f"{redis_config.MENU_ITEMS_NAMESPACE}:*{menu_item_id}*",
                f"{redis_config.RESTAURANT_MENUS_NAMESPACE}:*{restaurant_id}*",
                f"{redis_config.SEARCH_RESULTS_NAMESPACE}:*",  # Clear all searches
                f"{redis_config.CATEGORIES_NAMESPACE}:*{restaurant_id}*",
                f"{redis_config.DIETARY_NAMESPACE}:*{restaurant_id}*",
                f"{redis_config.POPULAR_NAMESPACE}:*"  # Clear popular items
            ]
            
            total_cleared = 0
            for pattern in patterns_to_clear:
                keys = self.redis_client.keys(pattern)
                if keys:
                    cleared = self.redis_client.delete(*keys)
                    total_cleared += cleared
            
            logger.info(f"Menu item invalidation: cleared {total_cleared} keys for item {menu_item_id}")
            return total_cleared
            
        except Exception as e:
            logger.error(f"Failed menu item invalidation for item {menu_item_id}: {e}")
            return 0
    
    async def clear_namespace(self, namespace: str) -> int:
        """Clear all keys in a specific namespace"""
        if not REDIS_AVAILABLE or not self.redis_client:
            return await self._fallback_clear_namespace(namespace)
                
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
    
    async def get_detailed_cache_stats(self) -> Dict[str, Any]:
        """Get detailed cache statistics by namespace"""
        if not REDIS_AVAILABLE or not self.redis_client:
            return await self._fallback_detailed_stats()
                
        try:
            info = self.redis_client.info()
            
            # Get detailed stats by namespace
            namespace_details = {}
            namespaces = [
                redis_config.RESTAURANT_NAMESPACE,
                redis_config.MENU_ITEMS_NAMESPACE,
                redis_config.RESTAURANT_MENUS_NAMESPACE,
                redis_config.SEARCH_RESULTS_NAMESPACE,
                redis_config.DIETARY_NAMESPACE,
                redis_config.ANALYTICS_NAMESPACE,
                redis_config.CATEGORIES_NAMESPACE,
                redis_config.POPULAR_NAMESPACE
            ]
            
            for namespace in namespaces:
                pattern = f"{namespace}:*"
                keys = self.redis_client.keys(pattern)
                
                # Calculate memory usage for this namespace (approximate)
                memory_usage = 0
                if keys:
                    for key in keys[:10]:  # Sample first 10 keys
                        try:
                            memory_usage += self.redis_client.memory_usage(key) or 0
                        except:
                            pass
                
                namespace_details[namespace] = {
                    "key_count": len(keys),
                    "sample_keys": keys[:5] if keys else [],
                    "estimated_memory_bytes": memory_usage,
                    "ttl_info": self._get_ttl_info(keys[:5]) if keys else {}
                }
            
            # Calculate cache hit ratio
            hit_ratio = self._calculate_hit_ratio()
            
            return {
                "cache_type": "Redis",
                "redis_info": {
                    "used_memory": info.get("used_memory_human"),
                    "connected_clients": info.get("connected_clients"),
                    "total_commands_processed": info.get("total_commands_processed"),
                    "keyspace_hits": info.get("keyspace_hits"),
                    "keyspace_misses": info.get("keyspace_misses"),
                    "uptime_in_seconds": info.get("uptime_in_seconds")
                },
                "namespace_details": namespace_details,
                "performance_stats": self.performance_stats,
                "cache_hit_ratio": hit_ratio,
                "total_namespaces": len(namespace_details),
                "active_keys": sum(ns["key_count"] for ns in namespace_details.values())
            }
        except Exception as e:
            logger.error(f"Failed to get detailed cache stats: {e}")
            return {"error": str(e)}
    
    def _get_ttl_info(self, sample_keys: List[str]) -> Dict[str, Any]:
        """Get TTL information for sample keys"""
        if not self.redis_client:
            return {}
        
        ttl_info = {"sample_ttls": []}
        for key in sample_keys:
            try:
                ttl = self.redis_client.ttl(key)
                ttl_info["sample_ttls"].append({"key": key, "ttl_seconds": ttl})
            except:
                pass
        
        return ttl_info
    
    def _calculate_hit_ratio(self) -> float:
        """Calculate cache hit ratio from performance stats"""
        total_requests = self.performance_stats["total_requests"]
        if total_requests == 0:
            return 0.0
        
        hit_ratio = (self.performance_stats["cache_hits"] / total_requests) * 100
        return round(hit_ratio, 2)
    
    def track_performance(self, is_cache_hit: bool, response_time: float):
        """Track cache performance metrics"""
        if redis_config.ENABLE_PERFORMANCE_MONITORING:
            self.performance_stats["total_requests"] += 1
            self.performance_stats["total_response_time"] += response_time
            
            if is_cache_hit:
                self.performance_stats["cache_hits"] += 1
            else:
                self.performance_stats["cache_misses"] += 1
            
            if response_time > redis_config.SLOW_QUERY_THRESHOLD:
                self.performance_stats["slow_queries"] += 1
                if redis_config.LOG_SLOW_QUERIES:
                    logger.warning(f"Slow query detected: {response_time:.3f}ms")
    
    def log_cache_performance(self, endpoint: str, cache_hit: bool, response_time: float):
        """Log cache performance with detailed metrics"""
        status = "HIT" if cache_hit else "MISS"
        self.track_performance(cache_hit, response_time)
        
        hit_ratio = self._calculate_hit_ratio()
        logger.info(
            f"CACHE {status} - {endpoint} - {response_time:.3f}ms - "
            f"Hit Ratio: {hit_ratio}% - Total Requests: {self.performance_stats['total_requests']}"
        )
    
    # Fallback methods for when Redis is not available
    async def _fallback_invalidate_restaurant(self, restaurant_id: int):
        """Fallback restaurant invalidation using memory cache"""
        try:
            from fallback_cache import memory_cache
            cleared = 0
            cleared += memory_cache.clear_namespace(redis_config.RESTAURANT_NAMESPACE)
            cleared += memory_cache.clear_namespace(redis_config.RESTAURANT_MENUS_NAMESPACE)
            cleared += memory_cache.clear_namespace(redis_config.SEARCH_RESULTS_NAMESPACE)
            return cleared
        except Exception:
            return 0
    
    async def _fallback_invalidate_menu_item(self, menu_item_id: int, restaurant_id: int):
        """Fallback menu item invalidation using memory cache"""
        try:
            from fallback_cache import memory_cache
            cleared = 0
            cleared += memory_cache.clear_namespace(redis_config.MENU_ITEMS_NAMESPACE)
            cleared += memory_cache.clear_namespace(redis_config.RESTAURANT_MENUS_NAMESPACE)
            cleared += memory_cache.clear_namespace(redis_config.SEARCH_RESULTS_NAMESPACE)
            return cleared
        except Exception:
            return 0
    
    async def _fallback_clear_namespace(self, namespace: str):
        """Fallback namespace clearing using memory cache"""
        try:
            from fallback_cache import memory_cache
            return memory_cache.clear_namespace(namespace)
        except Exception:
            return 0
    
    async def _fallback_detailed_stats(self):
        """Fallback detailed stats using memory cache"""
        try:
            from fallback_cache import memory_cache
            stats = memory_cache.get_stats()
            stats["performance_stats"] = self.performance_stats
            stats["cache_hit_ratio"] = self._calculate_hit_ratio()
            return stats
        except Exception:
            return {"error": "No cache available", "performance_stats": self.performance_stats}
    
    async def initialize(self):
        """Initialize the cache manager and establish connections"""
        try:
            # Test Redis connection
            if self.redis_client:
                await self.redis_client.ping()
                logger.info("Redis connection established successfully")
            else:
                logger.warning("Redis not available, using fallback cache only")
                
            # Initialize performance tracking
            if redis_config.ENABLE_PERFORMANCE_MONITORING:
                logger.info("Performance monitoring enabled")
                
        except Exception as e:
            logger.warning(f"Cache initialization warning: {e}")
    
    async def cleanup(self):
        """Cleanup cache connections"""
        try:
            if self.redis_client:
                await self.redis_client.close()
                logger.info("Redis connection closed")
        except Exception as e:
            logger.warning(f"Cache cleanup warning: {e}")

# Global advanced cache manager instance
advanced_cache_manager = AdvancedCacheManager()

def advanced_cache_decorator(namespace: str, expire: int, key_pattern: Optional[str] = None):
    """
    Advanced cache decorator with performance tracking
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            if key_pattern:
                cache_key = advanced_cache_manager.generate_cache_key(
                    namespace, key_pattern, **kwargs
                )
            else:
                cache_key = f"{namespace}:{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            start_time = time.time()
            
            # Try to get from cache (Redis or fallback)
            cached_result = None
            if REDIS_AVAILABLE and advanced_cache_manager.redis_client:
                try:
                    cached_result = await FastAPICache.get(cache_key)
                except Exception:
                    pass
            
            if cached_result is None:
                try:
                    from fallback_cache import memory_cache
                    cached_result = memory_cache.get(cache_key)
                except Exception:
                    pass
            
            if cached_result is not None:
                response_time = (time.time() - start_time) * 1000
                advanced_cache_manager.log_cache_performance(func.__name__, True, response_time)
                return cached_result
            
            # Cache miss - execute function
            result = await func(*args, **kwargs)
            response_time = (time.time() - start_time) * 1000
            
            # Store in cache
            if REDIS_AVAILABLE and advanced_cache_manager.redis_client:
                try:
                    await FastAPICache.set(cache_key, result, expire=expire)
                except Exception:
                    pass
            else:
                try:
                    from fallback_cache import memory_cache
                    memory_cache.set(cache_key, result, expire)
                except Exception:
                    pass
            
            advanced_cache_manager.log_cache_performance(func.__name__, False, response_time)
            return result
        
        return wrapper
    return decorator
