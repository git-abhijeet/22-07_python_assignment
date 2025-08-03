from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List
from datetime import time, datetime
from decimal import Decimal
from enum import Enum
import re

# Enums
class OrderStatusEnum(str, Enum):
    PLACED = "placed"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

# Restaurant Schemas (from V2)
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

class RestaurantResponse(RestaurantBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Menu Item Schemas (from V2)
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

class MenuItemResponse(MenuItemBase):
    id: int
    restaurant_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Customer Schemas
class CustomerBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Customer name")
    email: EmailStr = Field(..., description="Customer email address")
    phone_number: str = Field(..., description="Phone number")
    address: str = Field(..., min_length=10, max_length=500, description="Customer address")
    is_active: bool = Field(True, description="Whether customer is active")
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        phone_pattern = r'^[\+]?[1-9][\d\-\(\)\s]{7,15}$'
        if not re.match(phone_pattern, v.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')):
            raise ValueError('Invalid phone number format')
        return v

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[str] = Field(None, min_length=10, max_length=500)
    is_active: Optional[bool] = None

class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Order Item Schemas
class OrderItemBase(BaseModel):
    menu_item_id: int = Field(..., description="ID of the menu item")
    quantity: int = Field(..., gt=0, description="Quantity of the item")
    special_requests: Optional[str] = Field(None, description="Special requests for the item")

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    menu_item_id: int
    quantity: int
    item_price: Decimal
    special_requests: Optional[str]
    created_at: datetime
    menu_item: MenuItemResponse
    
    class Config:
        from_attributes = True

# Order Schemas
class OrderBase(BaseModel):
    delivery_address: str = Field(..., min_length=10, max_length=500, description="Delivery address")
    special_instructions: Optional[str] = Field(None, description="Special instructions for the order")

class OrderCreate(OrderBase):
    restaurant_id: int = Field(..., description="ID of the restaurant")
    items: List[OrderItemCreate] = Field(..., min_items=1, description="List of order items")

class OrderStatusUpdate(BaseModel):
    order_status: OrderStatusEnum = Field(..., description="New order status")
    delivery_time: Optional[datetime] = Field(None, description="Delivery time (for delivered status)")

class OrderResponse(OrderBase):
    id: int
    customer_id: int
    restaurant_id: int
    order_status: OrderStatusEnum
    total_amount: Decimal
    order_date: datetime
    delivery_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    customer: CustomerResponse
    restaurant: RestaurantResponse
    order_items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True

# Review Schemas
class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: Optional[str] = Field(None, max_length=1000, description="Review comment")

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    customer_id: int
    restaurant_id: int
    order_id: int
    created_at: datetime
    customer: CustomerResponse
    order: OrderResponse
    
    class Config:
        from_attributes = True

# Analytics Schemas
class RestaurantAnalytics(BaseModel):
    total_orders: int
    total_revenue: Decimal
    average_order_value: Decimal
    average_rating: float
    total_reviews: int
    popular_items: List[dict]
    orders_by_status: dict

class CustomerAnalytics(BaseModel):
    total_orders: int
    total_spent: Decimal
    average_order_value: Decimal
    favorite_restaurants: List[dict]
    order_frequency: dict

# List Schemas
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

class CustomerList(BaseModel):
    customers: List[CustomerResponse]
    total: int
    skip: int
    limit: int

class OrderList(BaseModel):
    orders: List[OrderResponse]
    total: int
    skip: int
    limit: int

class ReviewList(BaseModel):
    reviews: List[ReviewResponse]
    total: int
    skip: int
    limit: int

# Complex Response Schemas
class RestaurantWithMenu(RestaurantResponse):
    menu_items: List[MenuItemResponse] = []

class CustomerWithOrders(CustomerResponse):
    orders: List[OrderResponse] = []

class MenuItemWithRestaurant(MenuItemResponse):
    restaurant: RestaurantResponse
