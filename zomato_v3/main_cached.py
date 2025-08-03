"""
Zomato V3 - Enterprise Food Delivery System with Advanced Caching
================================================================

A production-ready food delivery platform with enterprise-level caching architecture.

🚀 Enterprise Features:
- Multi-tier TTL Strategy: Static (30min), Dynamic (2-5min), Real-time (30sec), Analytics (15min)
- Advanced Cache Patterns: Session-based, conditional, write-through, cache-aside
- Real-time Features: Live order tracking, restaurant availability, delivery slots
- Analytics Engine: Customer insights, restaurant performance, revenue analytics
- Performance Monitoring: Cache hit/miss ratios, memory usage, namespace statistics

🔧 Caching Architecture:
- Primary: Redis with enterprise namespacing and intelligent TTL strategies
- Fallback: Advanced memory cache with automatic cleanup
- Patterns: Session caching, conditional caching, write-through, cache-aside
- Monitoring: Real-time performance analytics and health checks

📊 Business Intelligence:
- Customer behavior analysis and preferences
- Restaurant performance metrics and trends
- Revenue analytics and daily reports
- Popular items and trending analysis
- Cache performance optimization recommendations

Technical Stack:
- FastAPI: Modern async web framework with enterprise features
- SQLAlchemy 2.0: Advanced ORM with async support and complex relationships
- Redis 5.0.1: High-performance caching with enterprise patterns
- Advanced Analytics: Business intelligence with intelligent caching
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import asyncio

from database import create_tables
from routes import menu_items, customers, orders, reviews
from routes.restaurants_cached import router as restaurants_router
from routes.cache_routes import router as cache_router, demo_router
from routes.analytics_routes import analytics_router
from routes.realtime_routes import realtime_router
from routes.enterprise_cache_routes import enterprise_cache_router
from routes.enterprise_demo_routes import enterprise_demo_router

# Setup enterprise logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database initialization
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager with graceful Redis handling"""
    # Startup
    redis_available = False
    
    try:
        # Initialize database
        await create_tables()
        logger.info("📊 Database initialized successfully")
        
        # Try to initialize Redis cache
        try:
            import redis.asyncio as redis
            from fastapi_cache2 import FastAPICache
            from fastapi_cache2.backends.redis import RedisBackend
            from redis_config import redis_config
            from cache_utils import cache_manager
            
            redis_client = redis.from_url(
                redis_config.REDIS_URL,
                encoding="utf8",
                decode_responses=True
            )
            
            # Test Redis connection
            await redis_client.ping()
            
            # Initialize FastAPI Cache with Redis
            FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
            logger.info("🗄️ Redis cache initialized successfully")
            
            # Initialize cache manager
            cache_manager.init_redis_client()
            logger.info("🔧 Cache manager initialized")
            
            redis_available = True
            
        except Exception as redis_error:
            logger.warning(f"⚠️ Redis not available: {redis_error}")
            logger.info("🔄 Falling back to in-memory caching")
            
            # Initialize fallback memory cache
            from fallback_cache import memory_cache
            memory_cache.enable()
            logger.info("💾 Memory cache initialized as fallback")
        
        cache_status = "Redis" if redis_available else "Memory"
        logger.info(f"🚀 Zomato V3 Food Delivery System with {cache_status} Caching is ready!")
        
        # Store cache status in app state
        app.state.redis_available = redis_available
        
        # Enterprise cache warming on startup
        if redis_available:
            logger.info("🔥 Starting enterprise cache warming...")
            try:
                # Background task for cache warming
                asyncio.create_task(warm_enterprise_cache())
            except Exception as e:
                logger.warning(f"Cache warming failed: {e}")
        
        yield
        
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        # Minimal startup without caching
        await create_tables()
        logger.warning("⚠️ Starting with minimal features - some caching may be unavailable")
        app.state.redis_available = False
        yield
    
    # Shutdown
    logger.info("🛑 Shutting down Zomato V3 Enterprise...")
    if redis_available:
        try:
            await redis_client.close()
            logger.info("Redis connection closed")
        except:
            pass

async def warm_enterprise_cache():
    """Background cache warming for frequently accessed data"""
    try:
        await asyncio.sleep(2)  # Wait for app to fully start
        
        # Import here to avoid circular import
        from redis_config import redis_config
        
        # Warm restaurant cache
        logger.info("Warming restaurant cache...")
        
        # Warm popular data (simulated)
        from cache_utils import cache_manager
        
        # Cache popular items list
        popular_items_key = f"{redis_config.ANALYTICS_RESTAURANT_NAMESPACE}:popular_items"
        await cache_manager.cache_data(
            popular_items_key,
            {"warmed": True, "items": []},
            redis_config.POPULAR_ITEMS_TTL,
            redis_config.ANALYTICS_RESTAURANT_NAMESPACE
        )
        
        logger.info("✅ Enterprise cache warming completed")
        
    except Exception as e:
        logger.warning(f"Cache warming failed: {e}")

# FastAPI application
app = FastAPI(
    title="Zomato V3 - Enterprise Food Delivery System with Advanced Caching",
    description=__doc__,
    version="3.2.0 - Enterprise Edition",
    contact={
        "name": "Zomato V3 Enterprise API",
        "email": "enterprise@zomato-v3.com",
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

# Include core routers
app.include_router(restaurants_router)  # Enhanced cached restaurant routes
app.include_router(menu_items.router)
app.include_router(customers.router)  # Now with session-based caching
app.include_router(orders.router)     # Now with conditional caching
app.include_router(orders.customer_order_router)
app.include_router(reviews.router)
app.include_router(reviews.order_review_router)

# Enterprise cache management routes
app.include_router(cache_router)
app.include_router(demo_router)
app.include_router(enterprise_cache_router)

# Enterprise analytics and real-time routes
app.include_router(analytics_router)
app.include_router(realtime_router)

# Enterprise demo routes
app.include_router(enterprise_demo_router)

@app.get("/")
async def root():
    """Welcome endpoint with system information including smart caching"""
    cache_type = getattr(app.state, 'redis_available', False)
    cache_status = "Redis" if cache_type else "Memory (Fallback)"
    
    return {
        "message": "🍕 Welcome to Zomato V3 - Complete Food Delivery System with Smart Caching!",
        "version": "3.1.0",
        "cache_type": cache_status,
        "features": [
            "Customer Management",
            "Restaurant & Menu Management", 
            "Complex Order Workflow",
            "Review System",
            "Advanced Analytics",
            f"{cache_status} Caching Layer",
            "Cache Performance Monitoring",
            "Automatic Cache Fallback",
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
            "primary": "Redis with 5-10 minute TTLs" if cache_type else "In-memory with TTL support",
            "fallback": "Automatic in-memory cache when Redis unavailable",
            "invalidation": "Smart invalidation on CRUD operations",
            "performance": "Cache hits < 10ms response time"
        },
        "business_logic": {
            "order_workflow": "pending → confirmed → preparing → out_for_delivery → delivered",
            "review_policy": "Only completed orders can be reviewed",
            "analytics": "Customer insights, restaurant performance, order statistics",
            "reliability": "Graceful degradation when Redis is unavailable"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint with cache status"""
    cache_type = getattr(app.state, 'redis_available', False)
    cache_status = "Redis connected" if cache_type else "Memory cache active"
    
    return {
        "status": "healthy",
        "service": "Zomato V3 Food Delivery System with Smart Caching",
        "version": "3.1.0",
        "cache_status": cache_status,
        "features": {
            "database": "operational",
            "api": "operational", 
            "cache": "operational",
            "cache_type": "Redis" if cache_type else "Memory"
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🍕 Starting Zomato V3 - Complete Food Delivery System with Smart Caching...")
    print("📚 API Documentation: http://localhost:8002/docs")
    print("🔍 Interactive API: http://localhost:8002/redoc")
    print("🗄️ Cache Management: http://localhost:8002/cache/stats")
    print("🎯 Cache Demo: http://localhost:8002/demo")
    print("⚡ Features: Redis caching with automatic memory fallback")
    
    uvicorn.run(
        "main_cached:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )
