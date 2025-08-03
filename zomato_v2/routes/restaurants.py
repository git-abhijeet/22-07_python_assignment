from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from http import HTTPStatus
import logging
import time

from database import get_database
from schemas import (
    RestaurantCreate, RestaurantUpdate, RestaurantResponse, RestaurantList,
    RestaurantWithMenu, RestaurantWithMenuList, MenuItemList
)
from crud import restaurant_crud, menu_item_crud
from advanced_cache_manager import advanced_cache_manager
from redis_config import redis_config

# Setup logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.post("/", response_model=RestaurantResponse, status_code=HTTPStatus.CREATED)
async def create_restaurant(
    restaurant: RestaurantCreate,
    request: Request,
    db: AsyncSession = Depends(get_database)
):
    """Create a new restaurant with advanced cache invalidation"""
    try:
        # Create restaurant
        db_restaurant = await restaurant_crud.create_restaurant(db, restaurant)
        
        # Hierarchical cache invalidation for new restaurant
        await advanced_cache_manager.invalidate_hierarchical([
            f"{redis_config.RESTAURANT_NAMESPACE}:list",  # Clear restaurant lists
            f"{redis_config.RESTAURANT_NAMESPACE}:active",  # Clear active restaurant lists
            f"{redis_config.ANALYTICS_NAMESPACE}:count",  # Clear count analytics
            f"{redis_config.SEARCH_RESULTS_NAMESPACE}:cuisine:{restaurant.cuisine_type}"  # Clear cuisine searches
        ])
        
        logger.info(f"Created restaurant {db_restaurant.id} with cache invalidation")
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
    db: AsyncSession = Depends(get_database)
):
    """Get all restaurants with pagination and multi-level caching"""
    try:
        # Multi-level cache key with pagination
        cache_key = f"{redis_config.RESTAURANT_NAMESPACE}:list:skip:{skip}:limit:{limit}"
        
        # Try to get from cache first
        cached_data = await advanced_cache_manager.get_cached_data(cache_key)
        if cached_data:
            logger.info(f"Cache hit for restaurant list: skip={skip}, limit={limit}")
            return RestaurantList(**cached_data)
        
        # Cache miss - fetch from database
        start_time = time.time()
        restaurants, total = await restaurant_crud.get_restaurants(db, skip=skip, limit=limit)
        
        result = RestaurantList(
            restaurants=restaurants,
            total=total,
            skip=skip,
            limit=limit
        )
        
        # Cache the result with restaurant list TTL
        await advanced_cache_manager.cache_data(
            key=cache_key,
            data=result.dict(),
            ttl=redis_config.RESTAURANT_LIST_TTL,
            namespace=redis_config.RESTAURANT_NAMESPACE
        )
        
        # Performance logging
        fetch_time = (time.time() - start_time) * 1000
        logger.info(f"Database fetch for restaurant list took {fetch_time:.3f}ms")
        
        return result
    except Exception as e:
        logger.error(f"Failed to retrieve restaurants: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve restaurants"
        )

@router.get("/with-menu", response_model=RestaurantWithMenuList)
async def get_restaurants_with_menu(
    request: Request,
    skip: int = Query(0, ge=0, description="Number of restaurants to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of restaurants to return"),
    db: AsyncSession = Depends(get_database)
):
    """Get restaurants with their complete menu - Advanced Q2 Caching"""
    try:
        # Restaurant-menu combination cache key (Q2 requirement)
        cache_key = f"{redis_config.RESTAURANT_MENUS_NAMESPACE}:with_menu:skip:{skip}:limit:{limit}"
        
        # Check cache first
        cached_data = await advanced_cache_manager.get_cached_data(cache_key)
        if cached_data:
            logger.info(f"Cache hit for restaurants with menu: skip={skip}, limit={limit}")
            return RestaurantWithMenuList(**cached_data)
        
        # Complex database query - measure performance
        start_time = time.time()
        restaurants, total = await restaurant_crud.get_restaurants_with_menu(db, skip=skip, limit=limit)
        
        result = RestaurantWithMenuList(
            restaurants=restaurants,
            total=total,
            skip=skip,
            limit=limit
        )
        
        # Cache with restaurant-menu specific TTL (Q2 strategy)
        await advanced_cache_manager.cache_data(
            key=cache_key,
            data=result.dict(),
            ttl=redis_config.RESTAURANT_MENU_TTL,  # 15 minutes for complex queries
            namespace=redis_config.RESTAURANT_MENUS_NAMESPACE
        )
        
        # Performance metrics
        fetch_time = (time.time() - start_time) * 1000
        logger.info(f"Complex restaurant-menu query took {fetch_time:.3f}ms")
        
        return result
    except Exception as e:
        logger.error(f"Failed to retrieve restaurants with menu: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve restaurants with menu"
        )

@router.get("/active", response_model=RestaurantList)
async def get_active_restaurants(
    skip: int = Query(0, ge=0, description="Number of restaurants to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of restaurants to return"),
    db: AsyncSession = Depends(get_database)
):
    """Get only active restaurants"""
    try:
        restaurants, total = await restaurant_crud.get_restaurants(db, skip=skip, limit=limit, active_only=True)
        return RestaurantList(
            restaurants=restaurants,
            total=total,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve active restaurants"
        )

@router.get("/search", response_model=RestaurantList)
async def search_restaurants_by_cuisine(
    request: Request,
    cuisine: str = Query(..., description="Cuisine type to search for"),
    skip: int = Query(0, ge=0, description="Number of restaurants to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of restaurants to return"),
    db: AsyncSession = Depends(get_database)
):
    """Search restaurants by cuisine type with search result caching"""
    try:
        # Search-specific cache key (Q2 requirement)
        cache_key = f"{redis_config.SEARCH_RESULTS_NAMESPACE}:cuisine:{cuisine}:skip:{skip}:limit:{limit}"
        
        # Check search cache
        cached_results = await advanced_cache_manager.get_cached_data(cache_key)
        if cached_results:
            logger.info(f"Cache hit for cuisine search: {cuisine}")
            return RestaurantList(**cached_results)
        
        # Perform search query
        start_time = time.time()
        restaurants, total = await restaurant_crud.get_restaurants(
            db, skip=skip, limit=limit, cuisine_type=cuisine
        )
        
        result = RestaurantList(
            restaurants=restaurants,
            total=total,
            skip=skip,
            limit=limit
        )
        
        # Cache search results with shorter TTL (search results change more frequently)
        await advanced_cache_manager.cache_data(
            key=cache_key,
            data=result.dict(),
            ttl=redis_config.SEARCH_RESULTS_TTL,  # 5 minutes for search results
            namespace=redis_config.SEARCH_RESULTS_NAMESPACE
        )
        
        # Search performance tracking
        search_time = (time.time() - start_time) * 1000
        logger.info(f"Cuisine search for '{cuisine}' took {search_time:.3f}ms")
        
        return result
    except Exception as e:
        logger.error(f"Failed to search restaurants: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to search restaurants"
        )

@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(
    restaurant_id: int,
    request: Request,
    db: AsyncSession = Depends(get_database)
):
    """Get a specific restaurant by ID with individual restaurant caching"""
    try:
        # Individual restaurant cache key
        cache_key = f"{redis_config.RESTAURANT_NAMESPACE}:restaurant:{restaurant_id}"
        
        # Check individual restaurant cache
        cached_restaurant = await advanced_cache_manager.get_cached_data(cache_key)
        if cached_restaurant:
            logger.info(f"Cache hit for restaurant {restaurant_id}")
            return RestaurantResponse(**cached_restaurant)
        
        # Fetch from database
        start_time = time.time()
        restaurant = await restaurant_crud.get_restaurant(db, restaurant_id)
        
        if not restaurant:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Restaurant with ID {restaurant_id} not found"
            )
        
        # Convert to response model
        restaurant_data = RestaurantResponse.from_orm(restaurant)
        
        # Cache individual restaurant with standard TTL
        await advanced_cache_manager.cache_data(
            key=cache_key,
            data=restaurant_data.dict(),
            ttl=redis_config.RESTAURANT_TTL,  # 10 minutes for individual restaurants
            namespace=redis_config.RESTAURANT_NAMESPACE
        )
        
        # Performance logging
        fetch_time = (time.time() - start_time) * 1000
        logger.info(f"Database fetch for restaurant {restaurant_id} took {fetch_time:.3f}ms")
        
        return restaurant_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve restaurant {restaurant_id}: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve restaurant"
        )

@router.get("/{restaurant_id}/with-menu", response_model=RestaurantWithMenu)
async def get_restaurant_with_menu(
    restaurant_id: int,
    request: Request,
    db: AsyncSession = Depends(get_database)
):
    """Get restaurant with all its menu items - Q2 Advanced Restaurant-Menu Caching"""
    try:
        # Restaurant-menu specific cache key (Q2 core requirement)
        cache_key = f"{redis_config.RESTAURANT_MENUS_NAMESPACE}:restaurant:{restaurant_id}:with_menu"
        
        # Check restaurant-menu cache
        cached_data = await advanced_cache_manager.get_cached_data(cache_key)
        if cached_data:
            logger.info(f"Cache hit for restaurant {restaurant_id} with menu")
            return RestaurantWithMenu(**cached_data)
        
        # Complex query to get restaurant with menu
        start_time = time.time()
        restaurant = await restaurant_crud.get_restaurant_with_menu(db, restaurant_id)
        
        if not restaurant:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Restaurant with ID {restaurant_id} not found"
            )
        
        # Convert to response model
        restaurant_data = RestaurantWithMenu.from_orm(restaurant)
        
        # Cache with restaurant-menu TTL (Q2 strategy - 15 minutes)
        await advanced_cache_manager.cache_data(
            key=cache_key,
            data=restaurant_data.dict(),
            ttl=redis_config.RESTAURANT_MENU_TTL,
            namespace=redis_config.RESTAURANT_MENUS_NAMESPACE
        )
        
        # Performance metrics for complex query
        fetch_time = (time.time() - start_time) * 1000
        logger.info(f"Complex restaurant-menu query for {restaurant_id} took {fetch_time:.3f}ms")
        
        return restaurant_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve restaurant {restaurant_id} with menu: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve restaurant with menu"
        )

@router.get("/{restaurant_id}/menu", response_model=MenuItemList)
async def get_restaurant_menu(
    restaurant_id: int,
    skip: int = Query(0, ge=0, description="Number of menu items to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of menu items to return"),
    db: AsyncSession = Depends(get_database)
):
    """Get all menu items for a restaurant"""
    try:
        # First check if restaurant exists
        restaurant = await restaurant_crud.get_restaurant(db, restaurant_id)
        if not restaurant:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Restaurant with ID {restaurant_id} not found"
            )
        
        menu_items, total = await menu_item_crud.get_restaurant_menu(db, restaurant_id, skip=skip, limit=limit)
        return MenuItemList(
            menu_items=menu_items,
            total=total,
            skip=skip,
            limit=limit
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve restaurant menu"
        )

@router.get("/{restaurant_id}/average-price")
async def get_restaurant_average_price(
    restaurant_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Calculate average menu price for a restaurant"""
    try:
        # First check if restaurant exists
        restaurant = await restaurant_crud.get_restaurant(db, restaurant_id)
        if not restaurant:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Restaurant with ID {restaurant_id} not found"
            )
        
        avg_price = await restaurant_crud.calculate_average_menu_price(db, restaurant_id)
        return {
            "restaurant_id": restaurant_id,
            "restaurant_name": restaurant.name,
            "average_price": avg_price
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to calculate average price"
        )

@router.put("/{restaurant_id}", response_model=RestaurantResponse)
async def update_restaurant(
    restaurant_id: int,
    restaurant_update: RestaurantUpdate,
    db: AsyncSession = Depends(get_database)
):
    """Update a restaurant"""
    try:
        updated_restaurant = await restaurant_crud.update_restaurant(
            db, restaurant_id, restaurant_update
        )
        if not updated_restaurant:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Restaurant with ID {restaurant_id} not found"
            )
        return updated_restaurant
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to update restaurant"
        )

@router.delete("/{restaurant_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Delete a restaurant (will also delete all its menu items)"""
    try:
        deleted = await restaurant_crud.delete_restaurant(db, restaurant_id)
        if not deleted:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Restaurant with ID {restaurant_id} not found"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to delete restaurant"
        )
