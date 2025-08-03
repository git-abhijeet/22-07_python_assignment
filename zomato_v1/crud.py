from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_, or_, func
from models import Restaurant
from schemas import RestaurantCreate, RestaurantUpdate
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
    
    async def get_active_restaurants(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 10
    ) -> tuple[List[Restaurant], int]:
        """Get only active restaurants"""
        return await self.get_restaurants(db, skip, limit, active_only=True)
    
    async def search_restaurants_by_cuisine(
        self, 
        db: AsyncSession, 
        cuisine_type: str, 
        skip: int = 0, 
        limit: int = 10
    ) -> tuple[List[Restaurant], int]:
        """Search restaurants by cuisine type"""
        return await self.get_restaurants(db, skip, limit, cuisine_type=cuisine_type)
    
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
        """Delete a restaurant"""
        db_restaurant = await self.get_restaurant(db, restaurant_id)
        if not db_restaurant:
            return False
        
        await db.delete(db_restaurant)
        await db.commit()
        return True

# Create a global instance
restaurant_crud = RestaurantCRUD()
