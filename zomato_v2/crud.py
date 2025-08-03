from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_, or_, func
from models import Restaurant, MenuItem
from schemas import RestaurantCreate, RestaurantUpdate, MenuItemCreate, MenuItemUpdate
from typing import Optional, List

class RestaurantCRUD:
    
    async def create_restaurant(self, db: AsyncSession, restaurant: RestaurantCreate) -> Restaurant:
        """Create a new restaurant"""
        # Check if restaurant with same name already exists
        existing = await self.get_restaurant_by_name(db, restaurant.name)
        if existing:
            raise ValueError(f"Restaurant with name '{restaurant.name}' already exists")
        
        db_restaurant = Restaurant(**restaurant.dict())
        db.add(db_restaurant)
        await db.commit()
        await db.refresh(db_restaurant)
        return db_restaurant
    
    async def get_restaurant(self, db: AsyncSession, restaurant_id: int) -> Optional[Restaurant]:
        """Get a restaurant by ID"""
        result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
        return result.scalar_one_or_none()
    
    async def get_restaurant_with_menu(self, db: AsyncSession, restaurant_id: int) -> Optional[Restaurant]:
        """Get a restaurant with all its menu items"""
        result = await db.execute(
            select(Restaurant)
            .options(selectinload(Restaurant.menu_items))
            .where(Restaurant.id == restaurant_id)
        )
        return result.scalar_one_or_none()
    
    async def get_restaurant_by_name(self, db: AsyncSession, name: str) -> Optional[Restaurant]:
        """Get a restaurant by name"""
        result = await db.execute(select(Restaurant).where(Restaurant.name == name))
        return result.scalar_one_or_none()
    
    async def get_restaurants(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 10,
        cuisine_type: Optional[str] = None,
        active_only: bool = False
    ) -> tuple[List[Restaurant], int]:
        """Get restaurants with pagination and optional filters"""
        query = select(Restaurant)
        count_query = select(func.count(Restaurant.id))
        
        # Apply filters
        filters = []
        if cuisine_type:
            filters.append(Restaurant.cuisine_type == cuisine_type)
        if active_only:
            filters.append(Restaurant.is_active == True)
        
        if filters:
            query = query.where(and_(*filters))
            count_query = count_query.where(and_(*filters))
        
        # Get total count
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination and ordering
        query = query.order_by(Restaurant.created_at.desc()).offset(skip).limit(limit)
        
        result = await db.execute(query)
        restaurants = result.scalars().all()
        
        return restaurants, total
    
    async def get_restaurants_with_menu(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 10
    ) -> tuple[List[Restaurant], int]:
        """Get restaurants with their menu items"""
        query = select(Restaurant).options(selectinload(Restaurant.menu_items))
        count_query = select(func.count(Restaurant.id))
        
        # Get total count
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination and ordering
        query = query.order_by(Restaurant.created_at.desc()).offset(skip).limit(limit)
        
        result = await db.execute(query)
        restaurants = result.scalars().all()
        
        return restaurants, total
    
    async def update_restaurant(
        self, 
        db: AsyncSession, 
        restaurant_id: int, 
        restaurant_update: RestaurantUpdate
    ) -> Optional[Restaurant]:
        """Update a restaurant"""
        db_restaurant = await self.get_restaurant(db, restaurant_id)
        if not db_restaurant:
            return None
        
        # Check for name conflicts if name is being updated
        if restaurant_update.name and restaurant_update.name != db_restaurant.name:
            existing = await self.get_restaurant_by_name(db, restaurant_update.name)
            if existing:
                raise ValueError(f"Restaurant with name '{restaurant_update.name}' already exists")
        
        # Update fields
        update_data = restaurant_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_restaurant, field, value)
        
        await db.commit()
        await db.refresh(db_restaurant)
        return db_restaurant
    
    async def delete_restaurant(self, db: AsyncSession, restaurant_id: int) -> bool:
        """Delete a restaurant (will cascade delete menu items)"""
        db_restaurant = await self.get_restaurant(db, restaurant_id)
        if not db_restaurant:
            return False
        
        await db.delete(db_restaurant)
        await db.commit()
        return True
    
    async def calculate_average_menu_price(self, db: AsyncSession, restaurant_id: int) -> float:
        """Calculate average menu price for a restaurant"""
        result = await db.execute(
            select(func.avg(MenuItem.price))
            .where(MenuItem.restaurant_id == restaurant_id)
        )
        avg_price = result.scalar()
        return float(avg_price) if avg_price else 0.0


class MenuItemCRUD:
    
    async def create_menu_item(
        self, 
        db: AsyncSession, 
        restaurant_id: int, 
        menu_item: MenuItemCreate
    ) -> MenuItem:
        """Create a new menu item for a restaurant"""
        # Verify restaurant exists
        restaurant_crud = RestaurantCRUD()
        restaurant = await restaurant_crud.get_restaurant(db, restaurant_id)
        if not restaurant:
            raise ValueError(f"Restaurant with ID {restaurant_id} not found")
        
        db_menu_item = MenuItem(**menu_item.dict(), restaurant_id=restaurant_id)
        db.add(db_menu_item)
        await db.commit()
        await db.refresh(db_menu_item)
        return db_menu_item
    
    async def get_menu_item(self, db: AsyncSession, item_id: int) -> Optional[MenuItem]:
        """Get a menu item by ID"""
        result = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
        return result.scalar_one_or_none()
    
    async def get_menu_item_with_restaurant(self, db: AsyncSession, item_id: int) -> Optional[MenuItem]:
        """Get a menu item with restaurant details"""
        result = await db.execute(
            select(MenuItem)
            .options(selectinload(MenuItem.restaurant))
            .where(MenuItem.id == item_id)
        )
        return result.scalar_one_or_none()
    
    async def get_menu_items(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 10,
        category: Optional[str] = None,
        vegetarian: Optional[bool] = None,
        vegan: Optional[bool] = None,
        available_only: bool = False
    ) -> tuple[List[MenuItem], int]:
        """Get menu items with pagination and optional filters"""
        query = select(MenuItem)
        count_query = select(func.count(MenuItem.id))
        
        # Apply filters
        filters = []
        if category:
            filters.append(MenuItem.category == category)
        if vegetarian is not None:
            filters.append(MenuItem.is_vegetarian == vegetarian)
        if vegan is not None:
            filters.append(MenuItem.is_vegan == vegan)
        if available_only:
            filters.append(MenuItem.is_available == True)
        
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
        
        return menu_items, total
    
    async def get_restaurant_menu(
        self, 
        db: AsyncSession, 
        restaurant_id: int, 
        skip: int = 0, 
        limit: int = 50
    ) -> tuple[List[MenuItem], int]:
        """Get all menu items for a specific restaurant"""
        query = select(MenuItem).where(MenuItem.restaurant_id == restaurant_id)
        count_query = select(func.count(MenuItem.id)).where(MenuItem.restaurant_id == restaurant_id)
        
        # Get total count
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination and ordering
        query = query.order_by(MenuItem.category, MenuItem.name).offset(skip).limit(limit)
        
        result = await db.execute(query)
        menu_items = result.scalars().all()
        
        return menu_items, total
    
    async def update_menu_item(
        self, 
        db: AsyncSession, 
        item_id: int, 
        menu_item_update: MenuItemUpdate
    ) -> Optional[MenuItem]:
        """Update a menu item"""
        db_menu_item = await self.get_menu_item(db, item_id)
        if not db_menu_item:
            return None
        
        # Update fields
        update_data = menu_item_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_menu_item, field, value)
        
        await db.commit()
        await db.refresh(db_menu_item)
        return db_menu_item
    
    async def delete_menu_item(self, db: AsyncSession, item_id: int) -> bool:
        """Delete a menu item"""
        db_menu_item = await self.get_menu_item(db, item_id)
        if not db_menu_item:
            return False
        
        await db.delete(db_menu_item)
        await db.commit()
        return True

# Create global instances
restaurant_crud = RestaurantCRUD()
menu_item_crud = MenuItemCRUD()
