from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from http import HTTPStatus
from database import get_database
from schemas import (
    RestaurantCreate, RestaurantUpdate, RestaurantResponse, RestaurantList,
    RestaurantWithMenu, MenuItemList, ReviewList, RestaurantAnalytics
)
from crud import restaurant_crud, review_crud, order_crud

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.post("/", response_model=RestaurantResponse, status_code=HTTPStatus.CREATED)
async def create_restaurant(
    restaurant: RestaurantCreate,
    db: AsyncSession = Depends(get_database)
):
    """Create a new restaurant"""
    try:
        db_restaurant = await restaurant_crud.create_restaurant(db, restaurant)
        return db_restaurant
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to create restaurant"
        )

@router.get("/", response_model=RestaurantList)
async def get_restaurants(
    skip: int = Query(0, ge=0, description="Number of restaurants to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of restaurants to return"),
    cuisine_type: Optional[str] = Query(None, description="Filter by cuisine type"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating filter"),
    location: Optional[str] = Query(None, description="Filter by location (searches in address)"),
    active_only: bool = Query(False, description="Show only active restaurants"),
    db: AsyncSession = Depends(get_database)
):
    """Get restaurants with advanced filtering"""
    try:
        restaurants, total = await restaurant_crud.get_restaurants(
            db, skip=skip, limit=limit, cuisine_type=cuisine_type,
            min_rating=min_rating, location=location, active_only=active_only
        )
        return RestaurantList(
            restaurants=restaurants,
            total=total,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve restaurants"
        )

@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Get a specific restaurant by ID"""
    try:
        restaurant = await restaurant_crud.get_restaurant(db, restaurant_id)
        if not restaurant:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Restaurant with ID {restaurant_id} not found"
            )
        return restaurant
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve restaurant"
        )

@router.get("/{restaurant_id}/reviews", response_model=ReviewList)
async def get_restaurant_reviews(
    restaurant_id: int,
    skip: int = Query(0, ge=0, description="Number of reviews to skip"),
    limit: int = Query(10, ge=1, le=50, description="Number of reviews to return"),
    db: AsyncSession = Depends(get_database)
):
    """Get reviews for a restaurant"""
    try:
        # First check if restaurant exists
        restaurant = await restaurant_crud.get_restaurant(db, restaurant_id)
        if not restaurant:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Restaurant with ID {restaurant_id} not found"
            )
        
        reviews, total = await review_crud.get_restaurant_reviews(db, restaurant_id, skip=skip, limit=limit)
        return ReviewList(
            reviews=reviews,
            total=total,
            skip=skip,
            limit=limit
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve restaurant reviews"
        )

@router.get("/{restaurant_id}/orders")
async def get_restaurant_orders(
    restaurant_id: int,
    skip: int = Query(0, ge=0, description="Number of orders to skip"),
    limit: int = Query(10, ge=1, le=50, description="Number of orders to return"),
    status: Optional[str] = Query(None, description="Filter by order status"),
    db: AsyncSession = Depends(get_database)
):
    """Get orders for a restaurant"""
    try:
        # First check if restaurant exists
        restaurant = await restaurant_crud.get_restaurant(db, restaurant_id)
        if not restaurant:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Restaurant with ID {restaurant_id} not found"
            )
        
        # Parse status filter
        from models import OrderStatus
        status_filter = None
        if status:
            try:
                status_filter = OrderStatus(status)
            except ValueError:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Invalid order status: {status}"
                )
        
        orders, total = await order_crud.get_restaurant_orders(
            db, restaurant_id, skip=skip, limit=limit, status_filter=status_filter
        )
        return {
            "orders": orders,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve restaurant orders"
        )

@router.get("/{restaurant_id}/analytics", response_model=RestaurantAnalytics)
async def get_restaurant_analytics(
    restaurant_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Get restaurant performance metrics"""
    try:
        # First check if restaurant exists
        restaurant = await restaurant_crud.get_restaurant(db, restaurant_id)
        if not restaurant:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Restaurant with ID {restaurant_id} not found"
            )
        
        analytics = await restaurant_crud.get_restaurant_analytics(db, restaurant_id)
        return analytics
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve restaurant analytics"
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
    """Delete a restaurant (will cascade delete menu items, orders, etc.)"""
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
