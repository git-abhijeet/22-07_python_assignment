"""
Enhanced Restaurant Routes with Fallback Caching for Zomato V3
==============================================================

Restaurant management routes with Redis caching and memory fallback support.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from http import HTTPStatus
import time
import logging

from database import get_database
from schemas import (
    RestaurantCreate, RestaurantUpdate, RestaurantResponse, RestaurantList,
    RestaurantWithMenu, MenuItemList, ReviewList, RestaurantAnalytics
)
from crud import restaurant_crud, review_crud, order_crud
from redis_config import redis_config

# Setup logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

def get_cache_decorator(request: Request):
    """Get appropriate cache decorator based on Redis availability"""
    if hasattr(request.app.state, 'redis_available') and request.app.state.redis_available:
        # Use Redis cache
        try:
            from fastapi_cache2 import cache
            return cache
        except ImportError:
            pass
    
    # Use memory cache fallback
    from fallback_cache import fallback_cache
    return fallback_cache

def log_cache_performance(endpoint: str, cache_hit: bool, response_time: float):
    """Log cache performance"""
    status = "HIT" if cache_hit else "MISS"
    logger.info(f"CACHE {status} - {endpoint} - {response_time:.3f}ms")

async def invalidate_restaurant_caches(request: Request, restaurant_id: Optional[int] = None):
    """Invalidate restaurant caches with fallback support"""
    try:
        if hasattr(request.app.state, 'redis_available') and request.app.state.redis_available:
            # Use Redis cache manager
            from cache_utils import cache_manager
            await cache_manager.invalidate_restaurant_cache(restaurant_id)
        else:
            # Use memory cache fallback
            from fallback_cache import invalidate_cache_namespace
            invalidate_cache_namespace(redis_config.RESTAURANT_NAMESPACE)
    except Exception as e:
        logger.warning(f"Cache invalidation failed: {e}")

@router.post("/", response_model=RestaurantResponse, status_code=HTTPStatus.CREATED)
async def create_restaurant(
    restaurant: RestaurantCreate,
    request: Request,
    db: AsyncSession = Depends(get_database)
):
    """Create a new restaurant and invalidate related caches"""
    try:
        start_time = time.time()
        
        db_restaurant = await restaurant_crud.create_restaurant(db, restaurant)
        
        # Invalidate restaurant caches after creation
        await invalidate_restaurant_caches(request)
        
        response_time = (time.time() - start_time) * 1000
        log_cache_performance("create_restaurant", False, response_time)
        
        return db_restaurant
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to create restaurant: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to create restaurant"
        )

@router.get("/", response_model=RestaurantList)
async def get_restaurants(
    request: Request,
    skip: int = Query(0, ge=0, description="Number of restaurants to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of restaurants to return"),
    cuisine_type: Optional[str] = Query(None, description="Filter by cuisine type"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating filter"),
    location: Optional[str] = Query(None, description="Filter by location (searches in address)"),
    active_only: bool = Query(False, description="Show only active restaurants"),
    db: AsyncSession = Depends(get_database)
):
    """Get restaurants with advanced filtering and caching"""
    
    # Create cache key based on parameters
    cache_key = f"restaurants_list_{skip}_{limit}_{cuisine_type}_{min_rating}_{location}_{active_only}"
    start_time = time.time()
    
    # Check if we should use caching
    use_redis = hasattr(request.app.state, 'redis_available') and request.app.state.redis_available
    cached_result = None
    
    if use_redis:
        try:
            from fastapi_cache2 import FastAPICache
            cached_result = await FastAPICache.get(f"{redis_config.RESTAURANT_NAMESPACE}:{cache_key}")
        except Exception:
            pass
    else:
        try:
            from fallback_cache import memory_cache
            cached_result = memory_cache.get(f"{redis_config.RESTAURANT_NAMESPACE}:{cache_key}")
        except Exception:
            pass
    
    if cached_result is not None:
        response_time = (time.time() - start_time) * 1000
        log_cache_performance("get_restaurants", True, response_time)
        return cached_result
    
    try:
        # Cache miss - fetch from database
        restaurants, total = await restaurant_crud.get_restaurants(
            db, skip=skip, limit=limit, cuisine_type=cuisine_type,
            min_rating=min_rating, location=location, active_only=active_only
        )
        
        result = RestaurantList(
            restaurants=restaurants,
            total=total,
            skip=skip,
            limit=limit
        )
        
        # Store in cache
        if use_redis:
            try:
                from fastapi_cache2 import FastAPICache
                await FastAPICache.set(
                    f"{redis_config.RESTAURANT_NAMESPACE}:{cache_key}", 
                    result, 
                    expire=redis_config.RESTAURANT_LIST_TTL
                )
            except Exception:
                pass
        else:
            try:
                from fallback_cache import memory_cache
                memory_cache.set(
                    f"{redis_config.RESTAURANT_NAMESPACE}:{cache_key}", 
                    result, 
                    redis_config.RESTAURANT_LIST_TTL
                )
            except Exception:
                pass
        
        response_time = (time.time() - start_time) * 1000
        log_cache_performance("get_restaurants", False, response_time)
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to retrieve restaurants: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve restaurants"
        )

@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(
    restaurant_id: int,
    request: Request,
    db: AsyncSession = Depends(get_database)
):
    """Get a specific restaurant by ID with caching"""
    
    cache_key = f"restaurant_detail_{restaurant_id}"
    start_time = time.time()
    
    # Check cache
    use_redis = hasattr(request.app.state, 'redis_available') and request.app.state.redis_available
    cached_result = None
    
    if use_redis:
        try:
            from fastapi_cache2 import FastAPICache
            cached_result = await FastAPICache.get(f"{redis_config.RESTAURANT_NAMESPACE}:{cache_key}")
        except Exception:
            pass
    else:
        try:
            from fallback_cache import memory_cache
            cached_result = memory_cache.get(f"{redis_config.RESTAURANT_NAMESPACE}:{cache_key}")
        except Exception:
            pass
    
    if cached_result is not None:
        response_time = (time.time() - start_time) * 1000
        log_cache_performance(f"get_restaurant_{restaurant_id}", True, response_time)
        return cached_result
    
    try:
        # Cache miss - fetch from database
        restaurant = await restaurant_crud.get_restaurant(db, restaurant_id)
        if not restaurant:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Restaurant with ID {restaurant_id} not found"
            )
        
        # Store in cache
        if use_redis:
            try:
                from fastapi_cache2 import FastAPICache
                await FastAPICache.set(
                    f"{redis_config.RESTAURANT_NAMESPACE}:{cache_key}", 
                    restaurant, 
                    expire=redis_config.RESTAURANT_DETAIL_TTL
                )
            except Exception:
                pass
        else:
            try:
                from fallback_cache import memory_cache
                memory_cache.set(
                    f"{redis_config.RESTAURANT_NAMESPACE}:{cache_key}", 
                    restaurant, 
                    redis_config.RESTAURANT_DETAIL_TTL
                )
            except Exception:
                pass
        
        response_time = (time.time() - start_time) * 1000
        log_cache_performance(f"get_restaurant_{restaurant_id}", False, response_time)
        
        return restaurant
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve restaurant {restaurant_id}: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve restaurant"
        )

@router.put("/{restaurant_id}", response_model=RestaurantResponse)
async def update_restaurant(
    restaurant_id: int,
    restaurant_update: RestaurantUpdate,
    request: Request,
    db: AsyncSession = Depends(get_database)
):
    """Update a restaurant and invalidate related caches"""
    try:
        start_time = time.time()
        
        updated_restaurant = await restaurant_crud.update_restaurant(
            db, restaurant_id, restaurant_update
        )
        if not updated_restaurant:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Restaurant with ID {restaurant_id} not found"
            )
        
        # Invalidate restaurant caches after update
        await invalidate_restaurant_caches(request, restaurant_id)
        
        response_time = (time.time() - start_time) * 1000
        log_cache_performance(f"update_restaurant_{restaurant_id}", False, response_time)
        
        return updated_restaurant
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update restaurant {restaurant_id}: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to update restaurant"
        )

@router.delete("/{restaurant_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_restaurant(
    restaurant_id: int,
    request: Request,
    db: AsyncSession = Depends(get_database)
):
    """Delete a restaurant and invalidate related caches"""
    try:
        start_time = time.time()
        
        deleted = await restaurant_crud.delete_restaurant(db, restaurant_id)
        if not deleted:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Restaurant with ID {restaurant_id} not found"
            )
        
        # Invalidate restaurant caches after deletion
        await invalidate_restaurant_caches(request, restaurant_id)
        
        response_time = (time.time() - start_time) * 1000
        log_cache_performance(f"delete_restaurant_{restaurant_id}", False, response_time)
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete restaurant {restaurant_id}: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to delete restaurant"
        )
