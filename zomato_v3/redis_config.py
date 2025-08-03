"""
Redis Configuration for Zomato V3
=================================

Configuration settings for Redis caching implementation.
"""

import os
from typing import Optional

class RedisConfig:
    """Redis configuration settings"""
    
    # Redis connection settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD", None)
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    
    # Redis URL for fastapi-cache2
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    
    # Enterprise Cache TTL Strategy (in seconds)
    # Static Data: Long TTL (30+ minutes)
    RESTAURANT_DETAIL_TTL: int = 1800   # 30 minutes - Restaurant details
    CUSTOMER_PROFILE_TTL: int = 1800    # 30 minutes - Customer profiles
    MENU_ITEM_TTL: int = 2100          # 35 minutes - Menu items
    
    # Dynamic Data: Short TTL (2-5 minutes)
    ORDER_STATUS_TTL: int = 180        # 3 minutes - Order status updates
    DELIVERY_TRACKING_TTL: int = 120   # 2 minutes - Delivery tracking
    LIVE_REVIEWS_TTL: int = 300        # 5 minutes - Recent reviews
    
    # Real-time Data: Very short TTL (30 seconds)
    RESTAURANT_AVAILABILITY_TTL: int = 60   # 1 minute - Restaurant capacity
    DELIVERY_SLOTS_TTL: int = 30           # 30 seconds - Available delivery slots
    LIVE_ORDERS_TTL: int = 30              # 30 seconds - Live order updates
    
    # Analytics Data: Medium TTL (15 minutes)
    POPULAR_ITEMS_TTL: int = 900       # 15 minutes - Popular menu items
    CUSTOMER_PREFERENCES_TTL: int = 900 # 15 minutes - Customer behavior
    RESTAURANT_ANALYTICS_TTL: int = 900 # 15 minutes - Restaurant performance
    REVENUE_ANALYTICS_TTL: int = 2400   # 40 minutes - Revenue metrics
    
    # Search and Lists: Medium TTL
    SEARCH_RESULTS_TTL: int = 300      # 5 minutes - Search results
    RESTAURANT_LIST_TTL: int = 600     # 10 minutes - Restaurant listings
    ACTIVE_RESTAURANTS_TTL: int = 240  # 4 minutes - Active restaurants
    
    # Enterprise Cache Namespaces
    RESTAURANT_NAMESPACE: str = "restaurants"
    MENU_NAMESPACE: str = "menu_items"
    CUSTOMER_NAMESPACE: str = "customers"
    ORDER_NAMESPACE: str = "orders"
    REVIEW_NAMESPACE: str = "reviews"
    
    # Analytics Namespaces
    ANALYTICS_RESTAURANT_NAMESPACE: str = "analytics:restaurants"
    ANALYTICS_CUSTOMER_NAMESPACE: str = "analytics:customers"
    ANALYTICS_REVENUE_NAMESPACE: str = "analytics:revenue"
    
    # Real-time Namespaces
    REALTIME_DELIVERY_NAMESPACE: str = "real-time:delivery"
    REALTIME_ORDERS_NAMESPACE: str = "real-time:orders"
    REALTIME_CAPACITY_NAMESPACE: str = "real-time:capacity"
    
    # Search Namespaces
    SEARCH_NAMESPACE: str = "search"
    SEARCH_POPULAR_NAMESPACE: str = "search:popular"
    
    # Cache key patterns
    RESTAURANT_LIST_KEY: str = "restaurant:list"
    RESTAURANT_DETAIL_KEY: str = "restaurant:detail:{id}"
    RESTAURANT_SEARCH_KEY: str = "restaurant:search:{cuisine}"
    ACTIVE_RESTAURANTS_KEY: str = "restaurant:active"

# Create global config instance
redis_config = RedisConfig()
