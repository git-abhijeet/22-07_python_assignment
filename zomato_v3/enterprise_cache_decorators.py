"""
Enterprise Cache Decorators for Zomato V3
==========================================

Advanced caching patterns including session-based, conditional, 
write-through, and cache-aside patterns.
"""

import time
import json
import logging
from typing import Optional, Callable, Any, Dict
from functools import wraps
from redis_config import redis_config

logger = logging.getLogger(__name__)

def session_cache(namespace: str, expire: int, key_builder: Optional[Callable] = None):
    """
    Session-based caching decorator for customer-specific data
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # Build cache key based on customer session
                if key_builder:
                    cache_key = key_builder(*args, **kwargs)
                else:
                    customer_id = kwargs.get('customer_id') or (args[1] if len(args) > 1 else None)
                    cache_key = f"{namespace}:customer:{customer_id}"
                
                # Try cache first
                from cache_utils import cache_manager
                cached_result = await cache_manager.get_cached_data(cache_key)
                
                if cached_result is not None:
                    logger.info(f"SESSION CACHE HIT - {func.__name__} - customer:{customer_id}")
                    return cached_result
                
                # Execute function and cache result
                start_time = time.time()
                result = await func(*args, **kwargs)
                response_time = (time.time() - start_time) * 1000
                
                # Cache the result
                await cache_manager.cache_data(cache_key, result, expire, namespace)
                
                logger.info(f"SESSION CACHE MISS - {func.__name__} - {response_time:.3f}ms - customer:{customer_id}")
                return result
                
            except Exception as e:
                logger.error(f"Session cache error for {func.__name__}: {e}")
                return await func(*args, **kwargs)
        
        return wrapper
    return decorator

def conditional_cache(namespace: str, expire: int, condition: Callable):
    """
    Conditional caching - only cache if condition is met
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # Execute function first
                start_time = time.time()
                result = await func(*args, **kwargs)
                response_time = (time.time() - start_time) * 1000
                
                # Check if we should cache this result
                should_cache = condition(result) if callable(condition) else condition
                
                if should_cache:
                    # Generate cache key
                    cache_key = f"{namespace}:{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
                    
                    from cache_utils import cache_manager
                    await cache_manager.cache_data(cache_key, result, expire, namespace)
                    
                    logger.info(f"CONDITIONAL CACHE STORED - {func.__name__} - {response_time:.3f}ms")
                else:
                    logger.info(f"CONDITIONAL CACHE SKIPPED - {func.__name__} - {response_time:.3f}ms")
                
                return result
                
            except Exception as e:
                logger.error(f"Conditional cache error for {func.__name__}: {e}")
                return await func(*args, **kwargs)
        
        return wrapper
    return decorator

def write_through_cache(namespace: str, expire: int, key_pattern: str):
    """
    Write-through caching - update cache immediately after database update
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # Execute the database operation
                start_time = time.time()
                result = await func(*args, **kwargs)
                response_time = (time.time() - start_time) * 1000
                
                # Update cache immediately
                cache_key = key_pattern.format(**kwargs)
                if not cache_key.startswith(namespace):
                    cache_key = f"{namespace}:{cache_key}"
                
                from cache_utils import cache_manager
                await cache_manager.cache_data(cache_key, result, expire, namespace)
                
                logger.info(f"WRITE-THROUGH CACHE UPDATED - {func.__name__} - {response_time:.3f}ms")
                return result
                
            except Exception as e:
                logger.error(f"Write-through cache error for {func.__name__}: {e}")
                return await func(*args, **kwargs)
        
        return wrapper
    return decorator

def cache_aside(namespace: str, expire: int, key_pattern: Optional[str] = None):
    """
    Cache-aside pattern - check cache first, then calculate and cache if miss
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # Generate cache key
                if key_pattern:
                    cache_key = key_pattern.format(**kwargs)
                else:
                    cache_key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
                
                if not cache_key.startswith(namespace):
                    cache_key = f"{namespace}:{cache_key}"
                
                from cache_utils import cache_manager
                
                # Try cache first
                cached_result = await cache_manager.get_cached_data(cache_key)
                if cached_result is not None:
                    logger.info(f"CACHE-ASIDE HIT - {func.__name__}")
                    return cached_result
                
                # Cache miss - calculate and store
                start_time = time.time()
                result = await func(*args, **kwargs)
                response_time = (time.time() - start_time) * 1000
                
                # Store in cache
                await cache_manager.cache_data(cache_key, result, expire, namespace)
                
                logger.info(f"CACHE-ASIDE MISS - {func.__name__} - {response_time:.3f}ms")
                return result
                
            except Exception as e:
                logger.error(f"Cache-aside error for {func.__name__}: {e}")
                return await func(*args, **kwargs)
        
        return wrapper
    return decorator

def analytics_cache(expire: int = redis_config.POPULAR_ITEMS_TTL):
    """
    Specialized caching for analytics data
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # Generate analytics cache key
                cache_key = f"analytics:{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
                
                from cache_utils import cache_manager
                
                # Check cache
                cached_result = await cache_manager.get_cached_data(cache_key)
                if cached_result is not None:
                    logger.info(f"ANALYTICS CACHE HIT - {func.__name__}")
                    return cached_result
                
                # Calculate analytics
                start_time = time.time()
                result = await func(*args, **kwargs)
                response_time = (time.time() - start_time) * 1000
                
                # Cache analytics
                await cache_manager.cache_data(
                    cache_key, result, expire, 
                    redis_config.ANALYTICS_RESTAURANT_NAMESPACE
                )
                
                logger.info(f"ANALYTICS CACHE MISS - {func.__name__} - {response_time:.3f}ms")
                return result
                
            except Exception as e:
                logger.error(f"Analytics cache error for {func.__name__}: {e}")
                return await func(*args, **kwargs)
        
        return wrapper
    return decorator

def realtime_cache(expire: int = redis_config.LIVE_ORDERS_TTL):
    """
    Real-time data caching with very short TTL
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # Generate real-time cache key
                cache_key = f"realtime:{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
                
                from cache_utils import cache_manager
                
                # Check cache (very short TTL)
                cached_result = await cache_manager.get_cached_data(cache_key)
                if cached_result is not None:
                    logger.info(f"REALTIME CACHE HIT - {func.__name__}")
                    return cached_result
                
                # Get real-time data
                start_time = time.time()
                result = await func(*args, **kwargs)
                response_time = (time.time() - start_time) * 1000
                
                # Cache with short TTL
                await cache_manager.cache_data(
                    cache_key, result, expire, 
                    redis_config.REALTIME_ORDERS_NAMESPACE
                )
                
                logger.info(f"REALTIME CACHE MISS - {func.__name__} - {response_time:.3f}ms")
                return result
                
            except Exception as e:
                logger.error(f"Real-time cache error for {func.__name__}: {e}")
                return await func(*args, **kwargs)
        
        return wrapper
    return decorator

# Utility functions for cache key building
def customer_key_builder(*args, **kwargs) -> str:
    """Build cache key for customer-specific data"""
    customer_id = kwargs.get('customer_id') or (args[1] if len(args) > 1 else None)
    return f"{redis_config.CUSTOMER_NAMESPACE}:customer:{customer_id}"

def restaurant_key_builder(*args, **kwargs) -> str:
    """Build cache key for restaurant-specific data"""
    restaurant_id = kwargs.get('restaurant_id') or (args[1] if len(args) > 1 else None)
    return f"{redis_config.RESTAURANT_NAMESPACE}:restaurant:{restaurant_id}"

def order_key_builder(*args, **kwargs) -> str:
    """Build cache key for order-specific data"""
    order_id = kwargs.get('order_id') or (args[1] if len(args) > 1 else None)
    return f"{redis_config.ORDER_NAMESPACE}:order:{order_id}"

# Condition functions for conditional caching
def cache_if_delivered(order_data) -> bool:
    """Only cache if order is delivered"""
    if isinstance(order_data, dict):
        return order_data.get('order_status') == 'delivered'
    return hasattr(order_data, 'order_status') and order_data.order_status.value == 'delivered'

def cache_if_active_restaurant(restaurant_data) -> bool:
    """Only cache if restaurant is active"""
    if isinstance(restaurant_data, dict):
        return restaurant_data.get('is_active', False)
    return hasattr(restaurant_data, 'is_active') and restaurant_data.is_active

def cache_if_positive_rating(review_data) -> bool:
    """Only cache if review rating is 4 or higher"""
    if isinstance(review_data, dict):
        return review_data.get('rating', 0) >= 4
    return hasattr(review_data, 'rating') and review_data.rating >= 4
