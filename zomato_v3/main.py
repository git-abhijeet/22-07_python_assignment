"""
Zomato V3 - Complete Food Delivery System with Redis Caching
===========================================================

A comprehensive food delivery management system built with FastAPI and Redis caching.

Features:
- Customer Management: Registration, authentication, profile management
- Restaurant Management: Menu items, availability, ratings with caching
- Order Management: Complex order workflow with status tracking
- Review System: Customer reviews for completed orders
- Analytics: Business intelligence and reporting
- Redis Caching: Performance optimization with intelligent cache invalidation
- Relationship Management: Many-to-many associations with complex business logic

Technical Stack:
- FastAPI: Modern async web framework
- SQLAlchemy 2.0: Advanced ORM with async support
- SQLite: Database with async operations
- Redis: High-performance caching layer
- Pydantic 2.5: Data validation and serialization

Caching Strategy:
- Restaurant List: 5-minute TTL with namespace-based caching
- Restaurant Details: 10-minute TTL with individual cache keys
- Search Results: 3-minute TTL for cuisine searches
- Cache Invalidation: Automatic on create/update/delete operations

Business Logic:
- Order workflow: pending → confirmed → preparing → out_for_delivery → delivered → cancelled
- Review validation: Only completed orders can be reviewed
- Analytics: Customer insights, restaurant performance, order statistics
- Cache Performance: <10ms response time for cache hits
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache2 import FastAPICache
from fastapi_cache2.backends.redis import RedisBackend
from contextlib import asynccontextmanager
import redis.asyncio as redis
import logging

from database import create_tables
from routes import restaurants, menu_items, customers, orders, reviews
from routes.cache_routes import router as cache_router, demo_router
from redis_config import redis_config
from cache_utils import cache_manager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database and Redis initialization
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager with Redis initialization"""
    # Startup
    try:
        # Initialize database
        await create_tables()
        logger.info("📊 Database initialized successfully")
        
        # Initialize Redis cache
        redis_client = redis.from_url(
            redis_config.REDIS_URL,
            encoding="utf8",
            decode_responses=True
        )
        
        # Initialize FastAPI Cache
        FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
        logger.info("�️ Redis cache initialized successfully")
        
        # Initialize cache manager
        cache_manager.init_redis_client()
        logger.info("🔧 Cache manager initialized")
        
        logger.info("�🚀 Zomato V3 Food Delivery System with Redis Caching is ready!")
        yield
        
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        # Try to start without Redis if Redis is not available
        await create_tables()
        logger.warning("⚠️ Starting without Redis cache - some features may be limited")
        yield
    
    # Shutdown
    logger.info("🛑 Shutting down Zomato V3...")

# FastAPI application
app = FastAPI(
    title="Zomato V3 - Complete Food Delivery System with Redis Caching",
    description=__doc__,
    version="3.1.0",
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

# Cache management routes
app.include_router(cache_router)
app.include_router(demo_router)

@app.get("/")
async def root():
    """Welcome endpoint with system information including caching"""
    return {
        "message": "🍕 Welcome to Zomato V3 - Complete Food Delivery System with Redis Caching!",
        "version": "3.1.0",
        "features": [
            "Customer Management",
            "Restaurant & Menu Management", 
            "Complex Order Workflow",
            "Review System",
            "Advanced Analytics",
            "Redis Caching Layer",
            "Cache Performance Monitoring",
            "Relationship Management"
        ],
        "api_docs": "/docs",
        "endpoints": {
            "restaurants": "/restaurants",
            "menu_items": "/menu-items", 
            "customers": "/customers",
            "orders": "/orders",
            "reviews": "/reviews",
            "cache_management": "/cache",
            "cache_demo": "/demo"
        },
        "caching_strategy": {
            "restaurant_list": "5 minutes TTL",
            "restaurant_details": "10 minutes TTL",
            "search_results": "3 minutes TTL",
            "cache_invalidation": "Automatic on CRUD operations"
        },
        "business_logic": {
            "order_workflow": "pending → confirmed → preparing → out_for_delivery → delivered",
            "review_policy": "Only completed orders can be reviewed",
            "analytics": "Customer insights, restaurant performance, order statistics",
            "performance": "Cache hits < 10ms response time"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint with cache status"""
    try:
        # Try to get cache stats to verify Redis connection
        cache_stats = await cache_manager.get_cache_stats()
        cache_status = "connected" if "error" not in cache_stats else "disconnected"
    except Exception:
        cache_status = "disconnected"
    
    return {
        "status": "healthy",
        "service": "Zomato V3 Food Delivery System with Redis Caching",
        "version": "3.1.0",
        "cache_status": cache_status,
        "features": {
            "database": "operational",
            "api": "operational", 
            "cache": cache_status
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🍕 Starting Zomato V3 - Complete Food Delivery System with Redis Caching...")
    print("📚 API Documentation: http://localhost:8002/docs")
    print("🔍 Interactive API: http://localhost:8002/redoc")
    print("🗄️ Cache Management: http://localhost:8002/cache/stats")
    print("🎯 Cache Demo: http://localhost:8002/demo")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )
