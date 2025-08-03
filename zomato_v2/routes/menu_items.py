from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from http import HTTPStatus
from database import get_database
from schemas import (
    MenuItemCreate, MenuItemUpdate, MenuItemResponse, MenuItemList,
    MenuItemWithRestaurant
)
from crud import menu_item_crud

router = APIRouter(prefix="/menu-items", tags=["menu-items"])

@router.post("/", response_model=MenuItemResponse, status_code=HTTPStatus.CREATED)
async def create_menu_item_standalone(
    menu_item: MenuItemCreate,
    restaurant_id: int = Query(..., description="Restaurant ID for the menu item"),
    db: AsyncSession = Depends(get_database)
):
    """Create a new menu item (alternative endpoint)"""
    try:
        db_menu_item = await menu_item_crud.create_menu_item(db, restaurant_id, menu_item)
        return db_menu_item
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to create menu item"
        )

@router.get("/", response_model=MenuItemList)
async def get_menu_items(
    skip: int = Query(0, ge=0, description="Number of menu items to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of menu items to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    vegetarian: Optional[bool] = Query(None, description="Filter by vegetarian status"),
    vegan: Optional[bool] = Query(None, description="Filter by vegan status"),
    available_only: bool = Query(False, description="Show only available items"),
    db: AsyncSession = Depends(get_database)
):
    """Get all menu items with optional filters"""
    try:
        menu_items, total = await menu_item_crud.get_menu_items(
            db, skip=skip, limit=limit, category=category, 
            vegetarian=vegetarian, vegan=vegan, available_only=available_only
        )
        return MenuItemList(
            menu_items=menu_items,
            total=total,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve menu items"
        )

@router.get("/search", response_model=MenuItemList)
async def search_menu_items(
    category: Optional[str] = Query(None, description="Category to search for"),
    vegetarian: Optional[bool] = Query(None, description="Filter by vegetarian status"),
    vegan: Optional[bool] = Query(None, description="Filter by vegan status"),
    skip: int = Query(0, ge=0, description="Number of menu items to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of menu items to return"),
    db: AsyncSession = Depends(get_database)
):
    """Search menu items by category and dietary preferences"""
    try:
        menu_items, total = await menu_item_crud.get_menu_items(
            db, skip=skip, limit=limit, category=category, 
            vegetarian=vegetarian, vegan=vegan
        )
        return MenuItemList(
            menu_items=menu_items,
            total=total,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to search menu items"
        )

@router.get("/{item_id}", response_model=MenuItemResponse)
async def get_menu_item(
    item_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Get a specific menu item by ID"""
    try:
        menu_item = await menu_item_crud.get_menu_item(db, item_id)
        if not menu_item:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Menu item with ID {item_id} not found"
            )
        return menu_item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve menu item"
        )

@router.get("/{item_id}/with-restaurant", response_model=MenuItemWithRestaurant)
async def get_menu_item_with_restaurant(
    item_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Get menu item with restaurant details"""
    try:
        menu_item = await menu_item_crud.get_menu_item_with_restaurant(db, item_id)
        if not menu_item:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Menu item with ID {item_id} not found"
            )
        return menu_item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve menu item with restaurant"
        )

@router.put("/{item_id}", response_model=MenuItemResponse)
async def update_menu_item(
    item_id: int,
    menu_item_update: MenuItemUpdate,
    db: AsyncSession = Depends(get_database)
):
    """Update a menu item"""
    try:
        updated_menu_item = await menu_item_crud.update_menu_item(
            db, item_id, menu_item_update
        )
        if not updated_menu_item:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Menu item with ID {item_id} not found"
            )
        return updated_menu_item
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
            detail="Failed to update menu item"
        )

@router.delete("/{item_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_menu_item(
    item_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Delete a menu item"""
    try:
        deleted = await menu_item_crud.delete_menu_item(db, item_id)
        if not deleted:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Menu item with ID {item_id} not found"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to delete menu item"
        )

# Restaurant-specific menu item routes
restaurant_menu_router = APIRouter(prefix="/restaurants/{restaurant_id}/menu-items", tags=["restaurant-menu"])

@restaurant_menu_router.post("/", response_model=MenuItemResponse, status_code=HTTPStatus.CREATED)
async def create_menu_item_for_restaurant(
    restaurant_id: int,
    menu_item: MenuItemCreate,
    db: AsyncSession = Depends(get_database)
):
    """Add menu item to a specific restaurant"""
    try:
        db_menu_item = await menu_item_crud.create_menu_item(db, restaurant_id, menu_item)
        return db_menu_item
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to create menu item"
        )
