from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, field_validator, Field
from enum import Enum
from decimal import Decimal
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager
import re

# Sample data and initialization
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the database with sample data on startup"""
    global next_menu_id, next_order_id
    
    # Initialize menu items
    for item_data in sample_menu_items:
        try:
            # Convert price to Decimal
            item_data['price'] = Decimal(item_data['price'])
            
            # Create FoodItem instance for validation
            food_item = FoodItem(**item_data)
            food_item.id = next_menu_id
            
            # Store in database
            menu_db[next_menu_id] = food_item.model_dump()
            next_menu_id += 1
            
        except Exception as e:
            print(f"Error adding sample item {item_data.get('name', 'Unknown')}: {e}")
    
    # Initialize sample order
    try:
        # Convert prices to Decimal
        for item in sample_order['items']:
            item['unit_price'] = Decimal(item['unit_price'])
        
        # Create Order instance for validation
        order = Order(**sample_order)
        order.id = next_order_id
        from datetime import datetime
        order.created_at = datetime.now().isoformat()
        
        # Store in database
        orders_db[next_order_id] = order.model_dump()
        next_order_id += 1
        
    except Exception as e:
        print(f"Error adding sample order: {e}")
    
    yield

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Restaurant Food Ordering System", 
    description="API for managing restaurant menu and customer orders",
    version="1.0.0", 
    lifespan=lifespan
)

# In-memory database
menu_db: Dict[int, Dict[str, Any]] = {}
orders_db: Dict[int, Dict[str, Any]] = {}
next_menu_id = 1
next_order_id = 1

# Food Category Enum
class FoodCategory(str, Enum):
    APPETIZER = "appetizer"
    MAIN_COURSE = "main_course"
    DESSERT = "dessert"
    BEVERAGE = "beverage"
    SALAD = "salad"

# Order Status Enum
class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    READY = "ready"
    DELIVERED = "delivered"

# FoodItem Pydantic Model
class FoodItem(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    category: FoodCategory
    price: Decimal = Field(..., decimal_places=2)
    is_available: bool = True
    preparation_time: int = Field(..., ge=1, le=120)
    ingredients: List[str] = Field(..., min_items=1)
    calories: Optional[int] = Field(None, gt=0)
    is_vegetarian: bool = False
    is_spicy: bool = False

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not re.match(r'^[a-zA-Z\s]+$', v):
            raise ValueError('Name should only contain letters and spaces')
        return v

    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v < Decimal('1.00') or v > Decimal('100.00'):
            raise ValueError('Price should be between $1.00 and $100.00')
        return v

    @field_validator('is_spicy')
    @classmethod
    def validate_spicy(cls, v, info):
        values = info.data
        if v and values.get('category') in [FoodCategory.DESSERT, FoodCategory.BEVERAGE]:
            raise ValueError('Desserts and beverages cannot be marked as spicy')
        return v

    @field_validator('calories')
    @classmethod
    def validate_calories(cls, v, info):
        values = info.data
        if v is not None and values.get('is_vegetarian') and v >= 800:
            raise ValueError('Vegetarian items should have calories < 800')
        return v

    @field_validator('preparation_time')
    @classmethod
    def validate_preparation_time(cls, v, info):
        values = info.data
        if values.get('category') == FoodCategory.BEVERAGE and v > 10:
            raise ValueError('Preparation time for beverages should be ≤ 10 minutes')
        return v

    @property
    def price_category(self) -> str:
        if self.price < Decimal('10.00'):
            return "Budget"
        elif self.price <= Decimal('25.00'):
            return "Mid-range"
        else:
            return "Premium"

    @property
    def dietary_info(self) -> List[str]:
        info = []
        if self.is_vegetarian:
            info.append("Vegetarian")
        if self.is_spicy:
            info.append("Spicy")
        return info

# Order-related Models
class OrderItem(BaseModel):
    """Simple nested model for items in order"""
    menu_item_id: int = Field(..., gt=0)
    menu_item_name: str = Field(..., min_length=1, max_length=100)  # Store name for easy access
    quantity: int = Field(..., gt=0, le=10)
    unit_price: Decimal = Field(..., gt=0, max_digits=6, decimal_places=2)

    @property
    def item_total(self) -> Decimal:
        """Simple computed property"""
        return self.quantity * self.unit_price

class Customer(BaseModel):
    """Simple nested customer model"""
    name: str = Field(..., min_length=2, max_length=50)
    phone: str = Field(..., pattern=r'^\d{10}$')
    address: str = Field(..., min_length=10, max_length=200)

class Order(BaseModel):
    """Main order model with nested customer and items"""
    id: Optional[int] = None
    customer: Customer
    items: List[OrderItem] = Field(..., min_items=1)
    status: OrderStatus = OrderStatus.PENDING
    delivery_fee: Decimal = Field(default=Decimal('2.99'), ge=0)
    created_at: Optional[str] = None

    @property
    def items_total(self) -> Decimal:
        """Calculate total of all items"""
        return sum(item.item_total for item in self.items)

    @property
    def total_amount(self) -> Decimal:
        """Calculate total including delivery fee"""
        return self.items_total + self.delivery_fee

    @property
    def total_items_count(self) -> int:
        """Count total number of items (considering quantities)"""
        return sum(item.quantity for item in self.items)

class FoodItemResponse(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    category: FoodCategory
    price: Decimal
    is_available: bool
    preparation_time: int
    ingredients: List[str]
    calories: Optional[int]
    is_vegetarian: bool
    is_spicy: bool
    price_category: str
    dietary_info: List[str]

    class Config:
        from_attributes = True

# Order Response Models
class OrderItemResponse(BaseModel):
    menu_item_id: int
    menu_item_name: str
    quantity: int
    unit_price: Decimal
    item_total: Decimal

class CustomerResponse(BaseModel):
    name: str
    phone: str
    address: str

class OrderResponse(BaseModel):
    id: int
    customer: CustomerResponse
    items: List[OrderItemResponse]
    status: OrderStatus
    delivery_fee: Decimal
    items_total: Decimal
    total_amount: Decimal
    total_items_count: int
    created_at: str

class OrderSummaryResponse(BaseModel):
    id: int
    customer_name: str
    status: OrderStatus
    total_amount: Decimal
    total_items_count: int
    created_at: str

class StatusUpdateRequest(BaseModel):
    status: OrderStatus

# Helper function to convert FoodItem to response format
def food_item_to_response(item: FoodItem) -> FoodItemResponse:
    item_dict = item.model_dump()
    item_dict['price_category'] = item.price_category
    item_dict['dietary_info'] = item.dietary_info
    return FoodItemResponse(**item_dict)

# Helper functions for order management
def validate_order_items(items: List[OrderItem]) -> None:
    """Validate that all menu items exist and are available"""
    for item in items:
        if item.menu_item_id not in menu_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Menu item with ID {item.menu_item_id} not found"
            )
        
        menu_item_data = menu_db[item.menu_item_id]
        if not menu_item_data.get('is_available', True):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Menu item '{menu_item_data['name']}' is not available"
            )

def order_to_response(order: Order) -> OrderResponse:
    """Convert Order model to OrderResponse"""
    items_response = []
    for item in order.items:
        items_response.append(OrderItemResponse(
            menu_item_id=item.menu_item_id,
            menu_item_name=item.menu_item_name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            item_total=item.item_total
        ))
    
    return OrderResponse(
        id=order.id,
        customer=CustomerResponse(
            name=order.customer.name,
            phone=order.customer.phone,
            address=order.customer.address
        ),
        items=items_response,
        status=order.status,
        delivery_fee=order.delivery_fee,
        items_total=order.items_total,
        total_amount=order.total_amount,
        total_items_count=order.total_items_count,
        created_at=order.created_at
    )

# API Endpoints

@app.get("/")
def root():
    return {
        "message": "Welcome to Restaurant Food Ordering System",
        "features": ["Menu Management", "Order Management"],
        "endpoints": {
            "menu": "/menu",
            "orders": "/orders",
            "docs": "/docs"
        }
    }

@app.get("/menu", response_model=List[FoodItemResponse])
def get_all_menu_items():
    """Get all menu items"""
    if not menu_db:
        return []
    
    items = []
    for item_data in menu_db.values():
        item = FoodItem(**item_data)
        items.append(food_item_to_response(item))
    return items

@app.get("/menu/{item_id}", response_model=FoodItemResponse)
def get_menu_item(item_id: int):
    """Get specific menu item by ID"""
    if item_id not in menu_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu item with ID {item_id} not found"
        )
    
    item_data = menu_db[item_id]
    item = FoodItem(**item_data)
    return food_item_to_response(item)

@app.post("/menu", response_model=FoodItemResponse, status_code=status.HTTP_201_CREATED)
def add_menu_item(food_item: FoodItem):
    """Add new menu item (staff only)"""
    global next_menu_id
    
    # Auto-generate ID
    food_item.id = next_menu_id
    
    # Store in database
    menu_db[next_menu_id] = food_item.model_dump()
    
    # Create response
    response_item = food_item_to_response(food_item)
    
    next_menu_id += 1
    return response_item

@app.put("/menu/{item_id}", response_model=FoodItemResponse)
def update_menu_item(item_id: int, food_item: FoodItem):
    """Update existing menu item"""
    if item_id not in menu_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu item with ID {item_id} not found"
        )
    
    # Set the ID to match the path parameter
    food_item.id = item_id
    
    # Update in database
    menu_db[item_id] = food_item.model_dump()
    
    return food_item_to_response(food_item)

@app.delete("/menu/{item_id}")
def delete_menu_item(item_id: int):
    """Remove menu item from menu"""
    if item_id not in menu_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu item with ID {item_id} not found"
        )
    
    deleted_item = menu_db.pop(item_id)
    return {"message": f"Menu item '{deleted_item['name']}' deleted successfully"}

@app.get("/menu/category/{category}", response_model=List[FoodItemResponse])
def get_items_by_category(category: FoodCategory):
    """Get items by category"""
    items = []
    for item_data in menu_db.values():
        if item_data['category'] == category.value:
            item = FoodItem(**item_data)
            items.append(food_item_to_response(item))
    return items

# Order Management Endpoints

@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: Order):
    """Create new order"""
    global next_order_id
    
    # Validate that all menu items exist and are available
    validate_order_items(order.items)
    
    # Auto-generate ID and timestamp
    order.id = next_order_id
    from datetime import datetime
    order.created_at = datetime.now().isoformat()
    
    # Store in database
    orders_db[next_order_id] = order.model_dump()
    
    # Create response
    response_order = order_to_response(order)
    
    next_order_id += 1
    return response_order

@app.get("/orders", response_model=List[OrderSummaryResponse])
def get_all_orders():
    """Get all orders"""
    if not orders_db:
        return []
    
    orders = []
    for order_data in orders_db.values():
        order = Order(**order_data)
        orders.append(OrderSummaryResponse(
            id=order.id,
            customer_name=order.customer.name,
            status=order.status,
            total_amount=order.total_amount,
            total_items_count=order.total_items_count,
            created_at=order.created_at
        ))
    return orders

@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order_details(order_id: int):
    """Get specific order details"""
    if order_id not in orders_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    
    order_data = orders_db[order_id]
    order = Order(**order_data)
    return order_to_response(order)

@app.put("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: int, status_update: StatusUpdateRequest):
    """Update order status"""
    if order_id not in orders_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    
    # Get current order
    order_data = orders_db[order_id]
    order = Order(**order_data)
    
    # Update status
    order.status = status_update.status
    
    # Save back to database
    orders_db[order_id] = order.model_dump()
    
    return order_to_response(order)

# Sample data for testing
sample_menu_items = [
    {
        "name": "Margherita Pizza",
        "description": "Classic pizza with tomato sauce, mozzarella cheese, and fresh basil",
        "category": "main_course",
        "price": "15.99",
        "preparation_time": 20,
        "ingredients": ["pizza dough", "tomato sauce", "mozzarella", "basil", "olive oil"],
        "calories": 650,
        "is_vegetarian": True,
        "is_spicy": False
    },
    {
        "name": "Spicy Chicken Wings",
        "description": "Crispy chicken wings tossed in our signature hot sauce",
        "category": "appetizer",
        "price": "12.50",
        "preparation_time": 15,
        "ingredients": ["chicken wings", "hot sauce", "butter", "celery salt"],
        "calories": 420,
        "is_vegetarian": False,
        "is_spicy": True
    },
    {
        "name": "Caesar Salad",
        "description": "Fresh romaine lettuce with parmesan cheese, croutons and caesar dressing",
        "category": "salad",
        "price": "9.99",
        "preparation_time": 8,
        "ingredients": ["romaine lettuce", "parmesan cheese", "croutons", "caesar dressing"],
        "calories": 280,
        "is_vegetarian": True,
        "is_spicy": False
    },
    {
        "name": "Chocolate Lava Cake",
        "description": "Warm chocolate cake with molten chocolate center served with vanilla ice cream",
        "category": "dessert",
        "price": "8.50",
        "preparation_time": 12,
        "ingredients": ["dark chocolate", "butter", "eggs", "flour", "sugar", "vanilla ice cream"],
        "calories": 520,
        "is_vegetarian": True,
        "is_spicy": False
    },
    {
        "name": "Fresh Orange Juice",
        "description": "Freshly squeezed orange juice served chilled",
        "category": "beverage",
        "price": "4.99",
        "preparation_time": 3,
        "ingredients": ["fresh oranges"],
        "calories": 110,
        "is_vegetarian": True,
        "is_spicy": False
    }
]

# Sample order data for testing
sample_order = {
    "customer": {
        "name": "Alice Smith",
        "phone": "5551234567",
        "address": "123 Oak Street, Springfield"
    },
    "items": [
        {
            "menu_item_id": 1,  # Reference to Margherita Pizza
            "menu_item_name": "Margherita Pizza",  # Store name for easy access
            "quantity": 1,
            "unit_price": "15.99"
        },
        {
            "menu_item_id": 2,  # Reference to Chicken Wings
            "menu_item_name": "Spicy Chicken Wings",
            "quantity": 2,
            "unit_price": "12.50"
        }
    ]
}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)