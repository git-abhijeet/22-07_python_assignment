# Zomato V2 - Restaurant & Menu Management System

An advanced restaurant and menu management system built with FastAPI, SQLAlchemy, and SQLite. This version extends V1 with menu item management and demonstrates one-to-many relationships between restaurants and their menu items.

## New Features in V2

-   **Menu Item Management** - Complete CRUD operations for menu items
-   **One-to-Many Relationships** - Restaurants can have multiple menu items
-   **Advanced Querying** - Efficient relationship loading with selectinload
-   **Dietary Filtering** - Filter by vegetarian/vegan preferences
-   **Category Search** - Search menu items by category
-   **Price Calculations** - Calculate average menu prices per restaurant
-   **Cascade Operations** - Deleting restaurants removes their menu items

## Models

### Restaurant Model

Same as V1 with added relationship to menu items:

-   All V1 fields plus relationship to menu items
-   Cascade delete functionality

### Menu Item Model

-   **id**: Primary key (auto-generated)
-   **name**: Menu item name (3-100 characters, required)
-   **description**: Optional description
-   **price**: Decimal price with 2 decimal places (must be positive)
-   **category**: Category (Appetizer, Main Course, Dessert, Beverage, Salad, Soup, Side Dish)
-   **is_vegetarian**: Boolean (default False)
-   **is_vegan**: Boolean (default False, must be vegetarian if True)
-   **is_available**: Boolean (default True)
-   **preparation_time**: Integer (minutes, must be positive)
-   **restaurant_id**: Foreign key to Restaurant
-   **created_at**: Timestamp
-   **updated_at**: Timestamp

## API Endpoints

### Restaurant Endpoints

| Method | Endpoint                                | Description                                |
| ------ | --------------------------------------- | ------------------------------------------ |
| POST   | `/restaurants/`                         | Create new restaurant                      |
| GET    | `/restaurants/`                         | List all restaurants (with pagination)     |
| GET    | `/restaurants/with-menu`                | Get restaurants with their complete menu   |
| GET    | `/restaurants/active`                   | List only active restaurants               |
| GET    | `/restaurants/search?cuisine={cuisine}` | Search by cuisine                          |
| GET    | `/restaurants/{id}`                     | Get specific restaurant                    |
| GET    | `/restaurants/{id}/with-menu`           | Get restaurant with all menu items         |
| GET    | `/restaurants/{id}/menu`                | Get all menu items for restaurant          |
| GET    | `/restaurants/{id}/average-price`       | Calculate average menu price               |
| PUT    | `/restaurants/{id}`                     | Update restaurant                          |
| DELETE | `/restaurants/{id}`                     | Delete restaurant (cascades to menu items) |
| POST   | `/restaurants/{id}/menu-items/`         | Add menu item to restaurant                |

### Menu Item Endpoints

| Method | Endpoint                                              | Description                           |
| ------ | ----------------------------------------------------- | ------------------------------------- |
| POST   | `/menu-items/?restaurant_id={id}`                     | Create menu item for restaurant       |
| GET    | `/menu-items/`                                        | List all menu items (with filters)    |
| GET    | `/menu-items/search?category={cat}&vegetarian={bool}` | Search with filters                   |
| GET    | `/menu-items/{id}`                                    | Get specific menu item                |
| GET    | `/menu-items/{id}/with-restaurant`                    | Get menu item with restaurant details |
| PUT    | `/menu-items/{id}`                                    | Update menu item                      |
| DELETE | `/menu-items/{id}`                                    | Delete menu item                      |

### System Endpoints

| Method | Endpoint    | Description                     |
| ------ | ----------- | ------------------------------- |
| GET    | `/`         | Welcome message and features    |
| GET    | `/health`   | Health check                    |
| GET    | `/api-info` | Complete API endpoint reference |
| GET    | `/docs`     | Interactive API documentation   |
| GET    | `/redoc`    | Alternative API documentation   |

## Installation & Setup

### Prerequisites

-   Python 3.8+
-   pip package manager

### Installation Steps

1. **Navigate to the project directory:**

    ```bash
    cd zomato_v2
    ```

2. **Create and activate virtual environment:**

    ```bash
    # Create virtual environment
    python -m venv venv

    # Activate on Windows
    venv\Scripts\activate

    # Activate on macOS/Linux
    source venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application:**

    ```bash
    python main.py
    ```

    Or using uvicorn directly:

    ```bash
    uvicorn main:app --reload --host 127.0.0.1 --port 8001
    ```

5. **Access the application:**
    - API: http://127.0.0.1:8001
    - Interactive Documentation: http://127.0.0.1:8001/docs
    - Alternative Documentation: http://127.0.0.1:8001/redoc

## Usage Examples

### Create a Restaurant

```bash
curl -X POST "http://127.0.0.1:8001/restaurants/" \
-H "Content-Type: application/json" \
-d '{
  "name": "Italiano Bistro",
  "description": "Authentic Italian cuisine in a cozy atmosphere",
  "cuisine_type": "Italian",
  "address": "456 Food Street, Gourmet District",
  "phone_number": "+1-555-0456",
  "rating": 4.7,
  "is_active": true,
  "opening_time": "11:00:00",
  "closing_time": "23:00:00"
}'
```

### Add Menu Item to Restaurant

```bash
curl -X POST "http://127.0.0.1:8001/restaurants/1/menu-items/" \
-H "Content-Type: application/json" \
-d '{
  "name": "Margherita Pizza",
  "description": "Classic pizza with fresh mozzarella, tomato sauce, and basil",
  "price": 18.99,
  "category": "Main Course",
  "is_vegetarian": true,
  "is_vegan": false,
  "is_available": true,
  "preparation_time": 15
}'
```

### Search Vegetarian Menu Items

```bash
curl "http://127.0.0.1:8001/menu-items/search?vegetarian=true&category=Main%20Course"
```

### Get Restaurant with Complete Menu

```bash
curl "http://127.0.0.1:8001/restaurants/1/with-menu"
```

### Get Average Menu Price

```bash
curl "http://127.0.0.1:8001/restaurants/1/average-price"
```

### Filter Menu Items by Dietary Preferences

```bash
# Get vegan items
curl "http://127.0.0.1:8001/menu-items/?vegan=true"

# Get vegetarian desserts
curl "http://127.0.0.1:8001/menu-items/?vegetarian=true&category=Dessert"

# Get available items only
curl "http://127.0.0.1:8001/menu-items/?available_only=true"
```

## Validation Rules

### Menu Item Validation

-   **Price**: Must be positive (> 0)
-   **Category**: Must be one of predefined categories
-   **Preparation Time**: Must be positive integer (minutes)
-   **Vegan Logic**: If item is vegan, it must also be vegetarian
-   **Name**: 3-100 characters required

### Restaurant Validation

-   Same as V1 (phone number format, cuisine types, time validation, etc.)

## Database Relationships

-   **One Restaurant → Many Menu Items**
-   **Foreign Key**: menu_items.restaurant_id references restaurants.id
-   **Cascade Delete**: Deleting a restaurant removes all its menu items
-   **Efficient Loading**: Uses SQLAlchemy selectinload for optimal query performance

## Advanced Features

### Relationship Loading

```python
# Efficient loading of restaurant with menu items
restaurant = await crud.get_restaurant_with_menu(db, restaurant_id)

# Efficient loading of menu item with restaurant details
menu_item = await crud.get_menu_item_with_restaurant(db, item_id)
```

### Complex Filtering

```python
# Multiple filters on menu items
menu_items = await crud.get_menu_items(
    db, category="Main Course", vegetarian=True, available_only=True
)
```

### Aggregation Functions

```python
# Calculate average price per restaurant
avg_price = await crud.calculate_average_menu_price(db, restaurant_id)
```

## Project Structure

```
zomato_v2/
├── main.py                    # FastAPI application entry point
├── database.py                # Database configuration
├── models.py                  # SQLAlchemy models with relationships
├── schemas.py                 # Pydantic schemas including nested models
├── crud.py                    # Enhanced CRUD operations
├── routes/
│   ├── __init__.py           # Routes package init
│   ├── restaurants.py        # Restaurant API routes
│   └── menu_items.py         # Menu item API routes
├── requirements.txt           # Dependencies
├── README.md                  # This documentation
└── zomato_v2.db              # SQLite database (auto-created)
```

## API Response Examples

### Restaurant with Menu Response

```json
{
    "id": 1,
    "name": "Italiano Bistro",
    "cuisine_type": "Italian",
    "menu_items": [
        {
            "id": 1,
            "name": "Margherita Pizza",
            "price": "18.99",
            "category": "Main Course",
            "is_vegetarian": true,
            "preparation_time": 15
        }
    ]
}
```

### Menu Item with Restaurant Response

```json
{
    "id": 1,
    "name": "Margherita Pizza",
    "price": "18.99",
    "category": "Main Course",
    "restaurant": {
        "id": 1,
        "name": "Italiano Bistro",
        "cuisine_type": "Italian"
    }
}
```

## Performance Optimizations

-   **Lazy Loading**: Relationships loaded only when needed
-   **Eager Loading**: Efficient selectinload for complex queries
-   **Indexing**: Strategic database indexes on foreign keys and search fields
-   **Pagination**: All list endpoints support pagination

## Error Handling

-   **Relationship Validation**: Ensures menu items can only be created for existing restaurants
-   **Cascade Safety**: Proper handling of dependent record deletion
-   **Data Integrity**: Foreign key constraints and validation
-   **Business Logic**: Validation for vegan/vegetarian logic

## Testing

The API can be tested using:

-   Interactive documentation at `/docs`
-   Alternative documentation at `/redoc`
-   curl commands (examples provided above)
-   HTTP clients like Postman or Insomnia
-   API info endpoint at `/api-info` for complete reference

## Differences from V1

1. **New Menu Item Model** with full CRUD operations
2. **Relationship Management** between restaurants and menu items
3. **Enhanced Queries** with efficient relationship loading
4. **Dietary Filtering** for vegetarian/vegan preferences
5. **Category-based Search** for menu items
6. **Price Calculations** and aggregations
7. **Modular Route Structure** with separate route files
8. **Cascade Operations** for data consistency

## Future Enhancements (V3)

Version 3 will include:

-   User authentication and authorization
-   Order management system
-   Payment processing
-   Advanced search and filtering
-   Restaurant ratings and reviews
-   Multi-tenant architecture

## License

This project is part of an educational assignment and is intended for learning purposes.
