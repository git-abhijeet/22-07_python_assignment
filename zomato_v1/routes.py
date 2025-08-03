from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from http import HTTPStatus
from database import get_database
from schemas import RestaurantCreate, RestaurantUpdate, RestaurantResponse, RestaurantList
from crud import restaurant_crud

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
    db: AsyncSession = Depends(get_database)
):
    """Get all restaurants with pagination"""
    try:
        restaurants, total = await restaurant_crud.get_restaurants(db, skip=skip, limit=limit)
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

@router.get("/active", response_model=RestaurantList)
async def get_active_restaurants(
    skip: int = Query(0, ge=0, description="Number of restaurants to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of restaurants to return"),
    db: AsyncSession = Depends(get_database)
):
    """Get only active restaurants"""
    try:
        restaurants, total = await restaurant_crud.get_active_restaurants(db, skip=skip, limit=limit)
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
    cuisine: str = Query(..., description="Cuisine type to search for"),
    skip: int = Query(0, ge=0, description="Number of restaurants to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of restaurants to return"),
    db: AsyncSession = Depends(get_database)
):
    """Search restaurants by cuisine type"""
    try:
        restaurants, total = await restaurant_crud.search_restaurants_by_cuisine(
            db, cuisine_type=cuisine, skip=skip, limit=limit
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
            detail="Failed to search restaurants"
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
    """Delete a restaurant"""
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
