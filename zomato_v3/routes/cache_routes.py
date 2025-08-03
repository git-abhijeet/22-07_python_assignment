"""
Cache Management Routes for Zomato V3
=====================================

API endpoints for cache management, statistics, and testing.
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from http import HTTPStatus
import time
import logging

from database import get_database
from cache_utils import cache_manager
from schemas import RestaurantCreate, RestaurantResponse
from crud import restaurant_crud

# Setup logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cache", tags=["cache-management"])

@router.get("/stats")
async def get_cache_statistics(request: Request):
    """Get comprehensive cache statistics"""
    try:
        if hasattr(request.app.state, 'redis_available') and request.app.state.redis_available:
            # Use Redis cache manager
            stats = await cache_manager.get_cache_stats()
            cache_type = "Redis"
        else:
            # Use memory cache fallback
            from fallback_cache import memory_cache
            stats = memory_cache.get_stats()
            cache_type = "Memory"
        
        return {
            "message": "Cache statistics retrieved successfully",
            "cache_type": cache_type,
            "timestamp": time.time(),
            "statistics": stats
        }
    except Exception as e:
        logger.error(f"Failed to get cache stats: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve cache statistics"
        )

@router.delete("/clear")
async def clear_entire_cache(request: Request):
    """Clear all caches across all namespaces"""
    try:
        if hasattr(request.app.state, 'redis_available') and request.app.state.redis_available:
            # Use Redis cache manager
            stats = await cache_manager.clear_all_cache()
            cache_type = "Redis"
        else:
            # Use memory cache fallback
            from fallback_cache import memory_cache
            cleared_count = memory_cache.clear_all()
            stats = {"total": cleared_count}
            cache_type = "Memory"
        
        return {
            "message": f"All {cache_type.lower()} caches cleared successfully",
            "cache_type": cache_type,
            "timestamp": time.time(),
            "cleared_keys": stats
        }
    except Exception as e:
        logger.error(f"Failed to clear all caches: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to clear caches"
        )

@router.delete("/clear/restaurants")
async def clear_restaurant_caches(request: Request):
    """Clear only restaurant-related caches"""
    try:
        from redis_config import redis_config
        
        if hasattr(request.app.state, 'redis_available') and request.app.state.redis_available:
            # Use Redis cache manager
            deleted = await cache_manager.clear_namespace(redis_config.RESTAURANT_NAMESPACE)
            cache_type = "Redis"
        else:
            # Use memory cache fallback
            from fallback_cache import memory_cache
            deleted = memory_cache.clear_namespace(redis_config.RESTAURANT_NAMESPACE)
            cache_type = "Memory"
        
        return {
            "message": f"{cache_type} restaurant caches cleared successfully",
            "cache_type": cache_type,
            "timestamp": time.time(),
            "cleared_keys": deleted
        }
    except Exception as e:
        logger.error(f"Failed to clear restaurant caches: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to clear restaurant caches"
        )

# Demo and Testing Routes
demo_router = APIRouter(prefix="/demo", tags=["cache-demo"])

@demo_router.get("/cache-test/{restaurant_id}")
async def demonstrate_cache_performance(
    restaurant_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Demonstrate cache performance with timing"""
    try:
        start_time = time.time()
        
        # Get restaurant (this will show cache hit/miss behavior)
        restaurant = await restaurant_crud.get_restaurant(db, restaurant_id)
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        
        if not restaurant:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Restaurant with ID {restaurant_id} not found"
            )
        
        # Log performance
        logger.info(f"Cache test for restaurant {restaurant_id}: {response_time:.3f}ms")
        
        return {
            "message": "Cache performance test completed",
            "restaurant_id": restaurant_id,
            "response_time_ms": round(response_time, 3),
            "restaurant": restaurant,
            "cache_note": "Check logs for CACHE HIT/MISS information"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Cache test failed: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Cache performance test failed"
        )

@demo_router.post("/sample-data")
async def create_sample_restaurants(
    db: AsyncSession = Depends(get_database)
):
    """Create sample restaurants for cache testing"""
    try:
        sample_restaurants = [
            {
                "name": "Pizza Palace",
                "description": "Authentic Italian pizza with fresh ingredients",
                "cuisine_type": "Italian",
                "address": "123 Main St, City Center",
                "phone_number": "+1-555-0101",
                "opening_time": "11:00:00",
                "closing_time": "23:00:00"
            },
            {
                "name": "Burger Barn",
                "description": "Juicy burgers and crispy fries",
                "cuisine_type": "American",
                "address": "456 Oak Ave, Downtown",
                "phone_number": "+1-555-0102",
                "opening_time": "10:00:00",
                "closing_time": "22:00:00"
            },
            {
                "name": "Sushi Zen",
                "description": "Fresh sushi and Japanese cuisine",
                "cuisine_type": "Japanese",
                "address": "789 Pine St, Uptown",
                "phone_number": "+1-555-0103",
                "opening_time": "17:00:00",
                "closing_time": "23:30:00"
            },
            {
                "name": "Taco Fiesta",
                "description": "Authentic Mexican tacos and burritos",
                "cuisine_type": "Mexican",
                "address": "321 Elm St, Midtown",
                "phone_number": "+1-555-0104",
                "opening_time": "09:00:00",
                "closing_time": "21:00:00"
            },
            {
                "name": "Curry House",
                "description": "Spicy Indian curries and naan bread",
                "cuisine_type": "Indian",
                "address": "654 Maple Dr, Eastside",
                "phone_number": "+1-555-0105",
                "opening_time": "12:00:00",
                "closing_time": "22:30:00"
            }
        ]
        
        created_restaurants = []
        for restaurant_data in sample_restaurants:
            restaurant_create = RestaurantCreate(**restaurant_data)
            
            # Check if restaurant already exists
            existing = await restaurant_crud.get_restaurant_by_name(db, restaurant_data["name"])
            if not existing:
                restaurant = await restaurant_crud.create_restaurant(db, restaurant_create)
                created_restaurants.append(restaurant)
        
        return {
            "message": f"Created {len(created_restaurants)} sample restaurants",
            "created_count": len(created_restaurants),
            "restaurants": created_restaurants,
            "note": "Use /demo/cache-test/{restaurant_id} to test cache performance"
        }
    
    except Exception as e:
        logger.error(f"Failed to create sample data: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to create sample restaurants"
        )
