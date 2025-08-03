from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from database import create_tables
from routes.restaurants import router as restaurant_router
from routes.menu_items import router as menu_item_router, restaurant_menu_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Creating database tables...")
    await create_tables()
    print("Database tables created successfully!")
    yield
    # Shutdown
    print("Application shutting down...")

# Create FastAPI application
app = FastAPI(
    title="Zomato V2 - Restaurant & Menu Management System",
    description="A restaurant and menu management system with one-to-many relationships",
    version="2.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include restaurant routes
app.include_router(restaurant_router)

# Include menu item routes
app.include_router(menu_item_router)

# Include restaurant-specific menu routes
app.include_router(restaurant_menu_router)

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to Zomato V2 Restaurant & Menu Management System",
        "version": "2.0.0",
        "features": [
            "Restaurant management",
            "Menu item management", 
            "One-to-many relationships",
            "Advanced querying with relationships",
            "Dietary preference filtering"
        ],
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "zomato-v2"}

# API Info endpoint
@app.get("/api-info", tags=["API Info"])
async def api_info():
    """Get API information and available endpoints"""
    return {
        "restaurant_endpoints": {
            "create": "POST /restaurants/",
            "list": "GET /restaurants/",
            "get_with_menu": "GET /restaurants/with-menu",
            "get_active": "GET /restaurants/active", 
            "search": "GET /restaurants/search?cuisine={cuisine}",
            "get_by_id": "GET /restaurants/{id}",
            "get_with_menu_by_id": "GET /restaurants/{id}/with-menu",
            "get_menu": "GET /restaurants/{id}/menu",
            "average_price": "GET /restaurants/{id}/average-price",
            "update": "PUT /restaurants/{id}",
            "delete": "DELETE /restaurants/{id}",
            "add_menu_item": "POST /restaurants/{id}/menu-items/"
        },
        "menu_item_endpoints": {
            "create": "POST /menu-items/?restaurant_id={id}",
            "list": "GET /menu-items/",
            "search": "GET /menu-items/search?category={cat}&vegetarian={bool}",
            "get_by_id": "GET /menu-items/{id}",
            "get_with_restaurant": "GET /menu-items/{id}/with-restaurant",
            "update": "PUT /menu-items/{id}",
            "delete": "DELETE /menu-items/{id}"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8001,  # Different port from V1
        reload=True,
        log_level="info"
    )
