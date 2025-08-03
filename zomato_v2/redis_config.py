"""
Advanced Redis Configuration for Zomato V2 - Restaurant-Menu System
===================================================================

Multi-level caching configuration with sophisticated TTL strategies
for restaurant-menu relationships and complex query caching.
"""

import os
from typing import Optional

class AdvancedRedisConfig:
    """Advanced Redis configuration for restaurant-menu system"""
    
    # Redis connection settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD", None)
    REDIS_DB: int = int(os.getenv("REDIS_DB", "1"))  # Use DB 1 for V2
    
    # Redis URL for fastapi-cache2
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    
    # Multi-Level Cache TTL settings (in seconds) - Q2 Requirements
    RESTAURANT_TTL: int = 600           # 10 minutes - Basic restaurant data
    MENU_ITEM_TTL: int = 480            # 8 minutes - More dynamic menu items
    RESTAURANT_MENU_TTL: int = 900      # 15 minutes - Expensive joins
    SEARCH_RESULTS_TTL: int = 300       # 5 minutes - Frequently changing
    
    # Specialized TTL for different data types
    DIETARY_FILTER_TTL: int = 420       # 7 minutes - Vegetarian/vegan searches
    ANALYTICS_TTL: int = 1800           # 30 minutes - Restaurant analytics
    CATEGORY_TTL: int = 600             # 10 minutes - Menu categories
    POPULAR_ITEMS_TTL: int = 900        # 15 minutes - Popular menu items
    
    # Advanced Cache namespaces - Q2 Requirements
    RESTAURANT_NAMESPACE: str = "restaurants"           # Basic restaurant data
    MENU_ITEMS_NAMESPACE: str = "menu-items"           # Individual menu items
    RESTAURANT_MENUS_NAMESPACE: str = "restaurant-menus"  # Complete combinations
    SEARCH_RESULTS_NAMESPACE: str = "search-results"   # Search and filter results
    
    # Specialized namespaces for complex scenarios
    DIETARY_NAMESPACE: str = "dietary-filters"         # Vegetarian/vegan searches
    ANALYTICS_NAMESPACE: str = "analytics"             # Business analytics
    CATEGORIES_NAMESPACE: str = "categories"           # Menu categories
    POPULAR_NAMESPACE: str = "popular"                 # Popular items/restaurants
    
    # Cache key patterns for hierarchical invalidation
    RESTAURANT_KEY_PATTERN: str = "restaurant:{id}"
    MENU_ITEM_KEY_PATTERN: str = "menu-item:{id}"
    RESTAURANT_MENU_KEY_PATTERN: str = "restaurant-menu:{restaurant_id}"
    SEARCH_KEY_PATTERN: str = "search:{query_hash}"
    CATEGORY_KEY_PATTERN: str = "category:{category}:{restaurant_id}"
    DIETARY_KEY_PATTERN: str = "dietary:{type}:{restaurant_id}"
    ANALYTICS_KEY_PATTERN: str = "analytics:{restaurant_id}:{metric}"
    
    # Cache warming settings
    CACHE_WARM_ON_STARTUP: bool = True
    CACHE_WARM_POPULAR_RESTAURANTS: int = 10
    CACHE_WARM_POPULAR_CATEGORIES: list = ["appetizers", "main-course", "desserts"]
    
    # Performance monitoring settings
    ENABLE_PERFORMANCE_MONITORING: bool = True
    TRACK_CACHE_HIT_RATIO: bool = True
    LOG_SLOW_QUERIES: bool = True
    SLOW_QUERY_THRESHOLD: float = 50.0  # milliseconds

# Create global config instance
redis_config = AdvancedRedisConfig()
