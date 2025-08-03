# Zomato V3 - Complete Food Delivery System with Redis Caching

A comprehensive food delivery management system built with FastAPI, featuring intelligent Redis caching with automatic fallback to in-memory caching.

## 🚀 New Features in V3 with Redis Caching

### ✨ Smart Caching System

-   **Primary**: Redis with optimized TTL settings for maximum performance
-   **Fallback**: Automatic in-memory caching when Redis is unavailable
-   **Performance**: <10ms response time for cache hits
-   **Monitoring**: Real-time cache performance logging and statistics

### 🔧 Caching Implementation

#### Redis Integration

-   **Backend**: `fastapi-cache2` with Redis backend
-   **Connection**: Configurable Redis host, port, password, and database
-   **TTL Strategy**: Namespace-based caching with different expiration times
-   **Graceful Degradation**: Falls back to memory cache if Redis is unavailable

#### Cache Configuration

```python
# Cache TTL Settings (seconds)
RESTAURANT_LIST_TTL = 300     # 5 minutes
RESTAURANT_DETAIL_TTL = 600   # 10 minutes
SEARCH_RESULTS_TTL = 180      # 3 minutes
ACTIVE_RESTAURANTS_TTL = 240  # 4 minutes
```

#### Cache Namespaces

-   `restaurants`: Restaurant data and listings
-   `menu_items`: Menu item information
-   `customers`: Customer profiles and data
-   `orders`: Order information
-   `reviews`: Review and rating data

## 📋 Requirements

### Dependencies

```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
aiosqlite==0.19.0
pydantic==2.5.0
python-multipart==0.0.6
redis==5.0.1
fastapi-cache2==0.2.1
email-validator
```

### Redis Setup (Optional)

Redis is optional - the system will automatically fall back to in-memory caching if Redis is not available.

#### Option 1: Docker (Recommended)

```bash
docker run -d --name redis-zomato -p 6379:6379 redis:latest
```

#### Option 2: Windows

1. Download from: https://github.com/microsoftarchive/redis/releases
2. Extract and run `redis-server.exe`

#### Option 3: macOS

```bash
brew install redis
brew services start redis
```

#### Option 4: Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

## 🛠️ Installation & Setup

1. **Clone and Navigate**

    ```bash
    cd zomato_v3/
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Setup Redis (Optional)**

    ```bash
    python setup_redis.py
    ```

4. **Start the Application**
    ```bash
    python main_cached.py
    ```

## 🌐 API Endpoints

### Core Endpoints

-   **Restaurants**: `/restaurants/` - CRUD operations with caching
-   **Menu Items**: `/menu-items/` - Menu management
-   **Customers**: `/customers/` - Customer management
-   **Orders**: `/orders/` - Order workflow management
-   **Reviews**: `/reviews/` - Review system

### Cache Management Endpoints

-   **Cache Statistics**: `GET /cache/stats` - View cache performance metrics
-   **Clear All Cache**: `DELETE /cache/clear` - Clear entire cache
-   **Clear Restaurant Cache**: `DELETE /cache/clear/restaurants` - Clear restaurant-specific cache

### Demo & Testing Endpoints

-   **Cache Performance Test**: `GET /demo/cache-test/{restaurant_id}` - Demonstrate cache hit/miss
-   **Sample Data Creation**: `POST /demo/sample-data` - Create test restaurants

## 🎯 Cache Performance Features

### Performance Monitoring

-   **Response Time Logging**: Automatic timing for all cached endpoints
-   **Cache Hit/Miss Tracking**: Detailed logging of cache performance
-   **Statistics Dashboard**: Real-time cache metrics via `/cache/stats`

### Cache Invalidation Strategy

```python
# Automatic cache invalidation on:
- Restaurant Creation: Clear entire restaurant namespace
- Restaurant Update: Clear specific restaurant + list caches
- Restaurant Deletion: Clear specific restaurant + list caches
```

### Example Cache Behavior

```
First Request:  CACHE MISS - get_restaurant_1 - 45.235ms (Database query)
Second Request: CACHE HIT  - get_restaurant_1 - 2.157ms (Cache retrieval)
```

## 📊 Cache Statistics Example

```json
{
    "message": "Cache statistics retrieved successfully",
    "cache_type": "Memory",
    "timestamp": 1723456789.123,
    "statistics": {
        "cache_type": "memory",
        "total_keys": 15,
        "namespaces": {
            "restaurants": 12,
            "menu_items": 3
        },
        "status": "operational"
    }
}
```

## 🔄 Fallback Cache System

When Redis is unavailable, the system automatically switches to in-memory caching:

### Memory Cache Features

-   **TTL Support**: Same expiration logic as Redis
-   **Namespace Organization**: Consistent with Redis implementation
-   **Performance Monitoring**: Same logging and statistics
-   **Automatic Cleanup**: Expired entries are automatically removed

### Cache Type Detection

```python
# The system automatically detects and uses the appropriate cache:
if redis_available:
    # Use Redis with fastapi-cache2
    await FastAPICache.get(cache_key)
else:
    # Use memory cache fallback
    memory_cache.get(cache_key)
```

## 🏃‍♂️ Running the Application

### Development Mode

```bash
python main_cached.py
```

### Access Points

-   **API Documentation**: http://localhost:8002/docs
-   **Interactive API**: http://localhost:8002/redoc
-   **Cache Statistics**: http://localhost:8002/cache/stats
-   **Cache Demo**: http://localhost:8002/demo
-   **Health Check**: http://localhost:8002/health

## 📈 Performance Optimization

### Caching Best Practices Implemented

1. **Namespace-based Organization**: Logical separation of cached data
2. **Appropriate TTL Values**: Optimized based on data volatility
3. **Smart Invalidation**: Clear related caches on data changes
4. **Fallback Strategy**: Graceful degradation when Redis unavailable
5. **Performance Monitoring**: Real-time cache hit/miss tracking

### Cache Hit Optimization

-   Restaurant lists cached for 5 minutes (frequent access)
-   Individual restaurants cached for 10 minutes (less frequent updates)
-   Search results cached for 3 minutes (moderate volatility)

## 🔍 Testing Cache Performance

### Manual Testing

1. **Create Sample Data**: `POST /demo/sample-data`
2. **First Request** (Cache Miss): `GET /demo/cache-test/1`
3. **Second Request** (Cache Hit): `GET /demo/cache-test/1`
4. **Check Statistics**: `GET /cache/stats`

### Expected Performance

-   **Cache Miss**: 20-50ms (database query + cache storage)
-   **Cache Hit**: 1-10ms (cache retrieval only)
-   **Cache Storage**: <5ms (Redis) or <1ms (Memory)

## 🛡️ Error Handling

### Redis Connection Issues

-   Automatic fallback to memory cache
-   Graceful error logging without service interruption
-   Health check endpoint reports cache status

### Cache Operation Failures

-   Fallback to database queries if cache fails
-   Comprehensive error logging for debugging
-   Service continues without caching if necessary

## 📝 Configuration

### Environment Variables

```bash
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=          # Optional
REDIS_DB=0
```

### Cache Configuration

Edit `redis_config.py` to customize:

-   TTL values for different data types
-   Cache namespaces
-   Redis connection settings

## 🎉 Summary

Zomato V3 now features a robust caching system that:

-   ✅ Provides significant performance improvements with Redis
-   ✅ Gracefully falls back to memory cache when Redis unavailable
-   ✅ Includes comprehensive monitoring and statistics
-   ✅ Implements smart cache invalidation strategies
-   ✅ Maintains full API functionality regardless of cache status
-   ✅ Offers detailed performance logging and debugging tools

The system is production-ready with enterprise-grade caching capabilities while maintaining reliability through intelligent fallback mechanisms!
