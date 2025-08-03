from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import time, datetime
from decimal import Decimal
import re

# Restaurant Schemas (Enhanced from V1)
class RestaurantBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Restaurant name")
    description: Optional[str] = Field(None, description="Restaurant description")
    cuisine_type: str = Field(..., min_length=1, max_length=50, description="Type of cuisine")
    address: str = Field(..., min_length=1, max_length=255, description="Restaurant address")
    phone_number: str = Field(..., description="Phone number")
    rating: float = Field(0.0, ge=0.0, le=5.0, description="Restaurant rating (0.0-5.0)")
    is_active: bool = Field(True, description="Whether restaurant is active")
    opening_time: time = Field(..., description="Opening time")
    closing_time: time = Field(..., description="Closing time")
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        phone_pattern = r'^[\+]?[1-9][\d\-\(\)\s]{7,15}$'
        if not re.match(phone_pattern, v.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')):
            raise ValueError('Invalid phone number format')
        return v
    
    @validator('cuisine_type')
    def validate_cuisine_type(cls, v):
        valid_cuisines = [
            'Italian', 'Chinese', 'Indian', 'Mexican', 'Thai', 'Japanese', 
            'American', 'French', 'Mediterranean', 'Fast Food', 'Vegetarian',
            'Continental', 'South Indian', 'North Indian', 'Pizza', 'Burger'
        ]
        if v not in valid_cuisines:
            raise ValueError(f'Cuisine type must be one of: {", ".join(valid_cuisines)}')
        return v
    
    @validator('closing_time')
    def validate_closing_time(cls, v, values):
        if 'opening_time' in values and v <= values['opening_time']:
            raise ValueError('Closing time must be after opening time')
        return v

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    cuisine_type: Optional[str] = Field(None, min_length=1, max_length=50)
    address: Optional[str] = Field(None, min_length=1, max_length=255)
    phone_number: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    is_active: Optional[bool] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        if v is not None:
            phone_pattern = r'^[\+]?[1-9][\d\-\(\)\s]{7,15}$'
            if not re.match(phone_pattern, v.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')):
                raise ValueError('Invalid phone number format')
        return v
    
    @validator('cuisine_type')
    def validate_cuisine_type(cls, v):
        if v is not None:
            valid_cuisines = [
                'Italian', 'Chinese', 'Indian', 'Mexican', 'Thai', 'Japanese', 
                'American', 'French', 'Mediterranean', 'Fast Food', 'Vegetarian',
                'Continental', 'South Indian', 'North Indian', 'Pizza', 'Burger'
            ]
            if v not in valid_cuisines:
                raise ValueError(f'Cuisine type must be one of: {", ".join(valid_cuisines)}')
        return v

# Menu Item Schemas
class MenuItemBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Menu item name")
    description: Optional[str] = Field(None, description="Menu item description")
    price: Decimal = Field(..., gt=0, description="Price must be positive")
    category: str = Field(..., description="Menu item category")
    is_vegetarian: bool = Field(False, description="Is the item vegetarian")
    is_vegan: bool = Field(False, description="Is the item vegan")
    is_available: bool = Field(True, description="Is the item available")
    preparation_time: int = Field(..., gt=0, description="Preparation time in minutes")
    
    @validator('category')
    def validate_category(cls, v):
        valid_categories = ['Appetizer', 'Main Course', 'Dessert', 'Beverage', 'Salad', 'Soup', 'Side Dish']
        if v not in valid_categories:
            raise ValueError(f'Category must be one of: {", ".join(valid_categories)}')
        return v
    
    @validator('is_vegan')
    def validate_vegan_vegetarian(cls, v, values):
        # If item is vegan, it must also be vegetarian
        if v and 'is_vegetarian' in values and not values['is_vegetarian']:
            raise ValueError('Vegan items must also be vegetarian')
        return v

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    category: Optional[str] = None
    is_vegetarian: Optional[bool] = None
    is_vegan: Optional[bool] = None
    is_available: Optional[bool] = None
    preparation_time: Optional[int] = Field(None, gt=0)
    
    @validator('category')
    def validate_category(cls, v):
        if v is not None:
            valid_categories = ['Appetizer', 'Main Course', 'Dessert', 'Beverage', 'Salad', 'Soup', 'Side Dish']
            if v not in valid_categories:
                raise ValueError(f'Category must be one of: {", ".join(valid_categories)}')
        return v

class MenuItemResponse(MenuItemBase):
    id: int
    restaurant_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class RestaurantResponse(RestaurantBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Nested schemas for complex responses
class MenuItemWithRestaurant(MenuItemResponse):
    restaurant: RestaurantResponse

class RestaurantWithMenu(RestaurantResponse):
    menu_items: List[MenuItemResponse] = []

class RestaurantList(BaseModel):
    restaurants: List[RestaurantResponse]
    total: int
    skip: int
    limit: int

class MenuItemList(BaseModel):
    menu_items: List[MenuItemResponse]
    total: int
    skip: int
    limit: int

class RestaurantWithMenuList(BaseModel):
    restaurants: List[RestaurantWithMenu]
    total: int
    skip: int
    limit: int
