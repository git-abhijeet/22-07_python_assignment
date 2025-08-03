# Zomato V1 - Restaurant Management System

A basic restaurant listing system built with FastAPI, SQLAlchemy, and SQLite. This is the foundation version of a progressive food delivery application.

## Features

-   Complete CRUD operations for restaurants
-   Restaurant data validation and error handling
-   Async database operations with SQLite
-   Pagination support
-   Search functionality by cuisine type
-   Active restaurant filtering
-   Comprehensive API documentation
-   Input validation for phone numbers, ratings, and time constraints

## Restaurant Model

The system manages restaurants with the following attributes:

-   **id**: Primary key (auto-generated)
-   **name**: Restaurant name (3-100 characters, unique)
-   **description**: Optional text description
-   **cuisine_type**: Type of cuisine (validated against predefined list)
-   **address**: Restaurant address (required)
-   **phone_number**: Contact number (with format validation)
-   **rating**: Float rating (0.0-5.0, default 0.0)
-   **is_active**: Boolean status (default True)
-   **opening_time**: Restaurant opening time
-   **closing_time**: Restaurant closing time
-   **created_at**: Timestamp of creation
-   **updated_at**: Timestamp of last update

## API Endpoints

### Restaurant Management

| Method | Endpoint                                     | Description                            |
| ------ | -------------------------------------------- | -------------------------------------- |
| POST   | `/restaurants/`                              | Create new restaurant                  |
| GET    | `/restaurants/`                              | List all restaurants (with pagination) |
| GET    | `/restaurants/{restaurant_id}`               | Get specific restaurant                |
| PUT    | `/restaurants/{restaurant_id}`               | Update restaurant                      |
| DELETE | `/restaurants/{restaurant_id}`               | Delete restaurant                      |
| GET    | `/restaurants/search?cuisine={cuisine_type}` | Search by cuisine                      |
| GET    | `/restaurants/active`                        | List only active restaurants           |

### System Endpoints

| Method | Endpoint  | Description                   |
| ------ | --------- | ----------------------------- |
| GET    | `/`       | Welcome message and API info  |
| GET    | `/health` | Health check endpoint         |
| GET    | `/docs`   | Interactive API documentation |
| GET    | `/redoc`  | Alternative API documentation |

## Installation & Setup

### Prerequisites

-   Python 3.8+
-   pip package manager

### Installation Steps

1. **Navigate to the project directory:**

    ```bash
    cd zomato_v1
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
    uvicorn main:app --reload --host 127.0.0.1 --port 8000
    ```

5. **Access the application:**
    - API: http://127.0.0.1:8000
    - Interactive Documentation: http://127.0.0.1:8000/docs
    - Alternative Documentation: http://127.0.0.1:8000/redoc

## Usage Examples

### Create a Restaurant

```bash
curl -X POST "http://127.0.0.1:8000/restaurants/" \
-H "Content-Type: application/json" \
-d '{
  "name": "Pizza Palace",
  "description": "Authentic Italian pizzas with fresh ingredients",
  "cuisine_type": "Italian",
  "address": "123 Main Street, Downtown",
  "phone_number": "+1-555-0123",
  "rating": 4.5,
  "is_active": true,
  "opening_time": "10:00:00",
  "closing_time": "22:00:00"
}'
```

### Get All Restaurants with Pagination

```bash
curl "http://127.0.0.1:8000/restaurants/?skip=0&limit=10"
```

### Search Restaurants by Cuisine

```bash
curl "http://127.0.0.1:8000/restaurants/search?cuisine=Italian&skip=0&limit=10"
```

### Get Active Restaurants Only

```bash
curl "http://127.0.0.1:8000/restaurants/active?skip=0&limit=10"
```

### Update a Restaurant

```bash
curl -X PUT "http://127.0.0.1:8000/restaurants/1" \
-H "Content-Type: application/json" \
-d '{
  "rating": 4.8,
  "description": "Updated description"
}'
```

### Delete a Restaurant

```bash
curl -X DELETE "http://127.0.0.1:8000/restaurants/1"
```

## Validation Rules

### Phone Number

-   Must match pattern: `^[\+]?[1-9][\d\-\(\)\s]{7,15}$`
-   Allows international format with optional country code
-   Supports common formatting characters (-, (), spaces)

### Cuisine Types

Valid cuisine types include:

-   Italian, Chinese, Indian, Mexican, Thai, Japanese
-   American, French, Mediterranean, Fast Food, Vegetarian
-   Continental, South Indian, North Indian, Pizza, Burger

### Rating

-   Must be between 0.0 and 5.0 (inclusive)
-   Decimal values allowed

### Time Validation

-   Closing time must be after opening time
-   Uses 24-hour format (HH:MM:SS)

### Restaurant Name

-   Must be 3-100 characters long
-   Must be unique across all restaurants

## Database

-   **Type**: SQLite (with async support via aiosqlite)
-   **ORM**: SQLAlchemy with async sessions
-   **File**: `zomato.db` (created automatically)
-   **Migrations**: Tables created automatically on startup

## Error Handling

The API provides comprehensive error handling with appropriate HTTP status codes:

-   **400 Bad Request**: Validation errors, duplicate names
-   **404 Not Found**: Restaurant not found
-   **500 Internal Server Error**: Server-side errors

## Project Structure

```
zomato_v1/
├── main.py              # FastAPI application entry point
├── database.py          # Database configuration and session management
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic models for request/response validation
├── crud.py              # Database operations (Create, Read, Update, Delete)
├── routes.py            # API route definitions
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── zomato.db            # SQLite database file (created automatically)
```

## Development

### Running in Development Mode

The application runs with auto-reload enabled by default when using `python main.py`.

### API Documentation

FastAPI automatically generates interactive API documentation available at:

-   Swagger UI: http://127.0.0.1:8000/docs
-   ReDoc: http://127.0.0.1:8000/redoc

### Testing the API

You can test the API using:

-   The interactive documentation at `/docs`
-   curl commands (examples provided above)
-   HTTP clients like Postman or Insomnia
-   Python requests library

## Future Enhancements (V2 & V3)

This is Version 1 of the Zomato application. Future versions will include:

-   Menu management system
-   Order processing
-   User authentication
-   Payment integration
-   Advanced search and filtering
-   Restaurant ratings and reviews

## License

This project is part of an educational assignment and is intended for learning purposes.
