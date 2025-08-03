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
    restaurant_id: Optional[int] = Query(None, description="Filter by restaurant"),
    db: AsyncSession = Depends(get_database)
):
    """Get all menu items with optional filters"""
    try:
        from crud import MenuItemCRUD
        from sqlalchemy.future import select
        from sqlalchemy import and_, func
        from models import MenuItem
        
        # Build query with filters
        query = select(MenuItem)
        count_query = select(func.count(MenuItem.id))
        
        filters = []
        if category:
            filters.append(MenuItem.category == category)
        if vegetarian is not None:
            filters.append(MenuItem.is_vegetarian == vegetarian)
        if vegan is not None:
            filters.append(MenuItem.is_vegan == vegan)
        if available_only:
            filters.append(MenuItem.is_available == True)
        if restaurant_id:
            filters.append(MenuItem.restaurant_id == restaurant_id)
        
        if filters:
            query = query.where(and_(*filters))
            count_query = count_query.where(and_(*filters))
        
        # Get total count
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination and ordering
        query = query.order_by(MenuItem.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        menu_items = result.scalars().all()
        
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
    price_min: Optional[float] = Query(None, ge=0, description="Minimum price"),
    price_max: Optional[float] = Query(None, ge=0, description="Maximum price"),
    restaurant_id: Optional[int] = Query(None, description="Filter by restaurant"),
    skip: int = Query(0, ge=0, description="Number of menu items to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of menu items to return"),
    db: AsyncSession = Depends(get_database)
):
    """Advanced search for menu items"""
    try:
        from sqlalchemy.future import select
        from sqlalchemy import and_, func
        from models import MenuItem
        
        # Build query with filters
        query = select(MenuItem)
        count_query = select(func.count(MenuItem.id))
        
        filters = []
        if category:
            filters.append(MenuItem.category == category)
        if vegetarian is not None:
            filters.append(MenuItem.is_vegetarian == vegetarian)
        if vegan is not None:
            filters.append(MenuItem.is_vegan == vegan)
        if price_min is not None:
            filters.append(MenuItem.price >= price_min)
        if price_max is not None:
            filters.append(MenuItem.price <= price_max)
        if restaurant_id:
            filters.append(MenuItem.restaurant_id == restaurant_id)
        
        # Only show available items by default
        filters.append(MenuItem.is_available == True)
        
        if filters:
            query = query.where(and_(*filters))
            count_query = count_query.where(and_(*filters))
        
        # Get total count
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination and ordering
        query = query.order_by(MenuItem.name).offset(skip).limit(limit)
        result = await db.execute(query)
        menu_items = result.scalars().all()
        
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
        from sqlalchemy.future import select
        from sqlalchemy.orm import selectinload
        from models import MenuItem
        
        result = await db.execute(
            select(MenuItem)
            .options(selectinload(MenuItem.restaurant))
            .where(MenuItem.id == item_id)
        )
        menu_item = result.scalar_one_or_none()
        
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
        from crud import MenuItemCRUD
        menu_crud = MenuItemCRUD()
        
        # Get current menu item
        db_menu_item = await menu_crud.get_menu_item(db, item_id)
        if not db_menu_item:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Menu item with ID {item_id} not found"
            )
        
        # Update fields
        update_data = menu_item_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_menu_item, field, value)
        
        await db.commit()
        await db.refresh(db_menu_item)
        return db_menu_item
        
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
        menu_item = await menu_item_crud.get_menu_item(db, item_id)
        if not menu_item:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Menu item with ID {item_id} not found"
            )
        
        await db.delete(menu_item)
        await db.commit()
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
