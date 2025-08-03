"""
Zomato V3 - Complete Food Delivery System
=========================================

A comprehensive food delivery management system built with FastAPI.

Features:
- Customer Management: Registration, authentication, profile management
- Restaurant Management: Menu items, availability, ratings  
- Order Management: Complex order workflow with status tracking
- Review System: Customer reviews for completed orders
- Analytics: Business intelligence and reporting
- Relationship Management: Many-to-many associations with complex business logic

Technical Stack:
- FastAPI: Modern async web framework
- SQLAlchemy 2.0: Advanced ORM with async support
- SQLite: Database with async operations
- Pydantic 2.5: Data validation and serialization

Business Logic:
- Order workflow: pending -> confirmed -> preparing -> out_for_delivery -> delivered -> cancelled
- Review validation: Only completed orders can be reviewed
- Analytics: Customer insights, restaurant performance, order statistics
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_tables
from routes import restaurants, menu_items, customers, orders, reviews
import uvicorn

# Database initialization
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    await create_tables()
    print("📊 Database initialized successfully")
    print("🚀 Zomato V3 Food Delivery System is ready!")
    yield
    # Shutdown
    print("🛑 Shutting down Zomato V3...")

# FastAPI application
app = FastAPI(
    title="Zomato V3 - Complete Food Delivery System",
    description=__doc__,
    version="3.0.0",
    contact={
        "name": "Zomato V3 API",
        "email": "support@zomato-v3.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(restaurants.router)
app.include_router(menu_items.router)
app.include_router(customers.router)
app.include_router(orders.router)
app.include_router(orders.customer_order_router)  # Customer order routes
app.include_router(reviews.router)
app.include_router(reviews.order_review_router)   # Order review routes

@app.get("/")
async def root():
    """Welcome endpoint with system information"""
    return {
        "message": "🍕 Welcome to Zomato V3 - Complete Food Delivery System!",
        "version": "3.0.0",
        "features": [
            "Customer Management",
            "Restaurant & Menu Management", 
            "Complex Order Workflow",
            "Review System",
            "Advanced Analytics",
            "Relationship Management"
        ],
        "api_docs": "/docs",
        "endpoints": {
            "restaurants": "/restaurants",
            "menu_items": "/menu-items", 
            "customers": "/customers",
            "orders": "/orders",
            "reviews": "/reviews"
        },
        "business_logic": {
            "order_workflow": "pending → confirmed → preparing → out_for_delivery → delivered",
            "review_policy": "Only completed orders can be reviewed",
            "analytics": "Customer insights, restaurant performance, order statistics"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Zomato V3 Food Delivery System",
        "version": "3.0.0"
    }

if __name__ == "__main__":
    print("🍕 Starting Zomato V3 - Complete Food Delivery System...")
    print("📚 API Documentation: http://localhost:8002/docs")
    print("🔍 Interactive API: http://localhost:8002/redoc")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )
