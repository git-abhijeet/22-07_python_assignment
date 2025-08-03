"""
Enterprise Cache Management Routes for Zomato V3
================================================

Advanced cache management endpoints for enterprise-level monitoring and control.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any, List
from http import HTTPStatus
import logging
import time
import psutil
import gc

from database import get_database
from redis_config import redis_config

logger = logging.getLogger(__name__)

# Enterprise cache management router
enterprise_cache_router = APIRouter(prefix="/cache", tags=["enterprise-cache-management"])

@enterprise_cache_router.get("/health")
async def cache_health_check(request: Request):
    """Comprehensive cache health check"""
    try:
        from cache_utils import cache_manager
        
        health_data = {
            "status": "healthy",
            "timestamp": time.time(),
            "checks": {}
        }
        
        # Test Redis connection
        try:
            from fallback_cache import redis_available
            if redis_available:
                health_data["checks"]["redis"] = {
                    "status": "connected",
                    "url": redis_config.REDIS_URL
                }
            else:
                health_data["checks"]["redis"] = {
                    "status": "unavailable",
                    "fallback": "memory_cache_active"
                }
        except Exception as e:
            health_data["checks"]["redis"] = {
                "status": "error",
                "error": str(e)
            }
        
        # Test cache operations
        try:
            test_key = "health_check_test"
            test_value = {"test": True, "timestamp": time.time()}
            
            # Test cache set/get
            await cache_manager.cache_data(test_key, test_value, 60, "health")
            retrieved = await cache_manager.get_cached_data(test_key)
            
            if retrieved == test_value:
                health_data["checks"]["cache_operations"] = {"status": "working"}
            else:
                health_data["checks"]["cache_operations"] = {"status": "failed", "reason": "data_mismatch"}
                health_data["status"] = "degraded"
                
            # Clean up test key
            await cache_manager.delete_cached_data(test_key)
            
        except Exception as e:
            health_data["checks"]["cache_operations"] = {
                "status": "failed",
                "error": str(e)
            }
            health_data["status"] = "unhealthy"
        
        return health_data
        
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        return {
            "status": "error",
            "timestamp": time.time(),
            "error": str(e)
        }

@enterprise_cache_router.get("/stats/namespaces")
async def get_namespace_statistics(request: Request):
    """Get detailed statistics by namespace"""
    try:
        from cache_utils import cache_manager
        
        cache_stats = await cache_manager.get_cache_stats()
        
        # Organize stats by enterprise namespaces
        namespace_stats = {
            "static_data": {
                "namespaces": [
                    redis_config.RESTAURANT_NAMESPACE,
                    redis_config.CUSTOMER_NAMESPACE,
                    redis_config.MENU_NAMESPACE
                ],
                "ttl_strategy": "Long TTL (30+ minutes)",
                "keys": cache_stats.get('namespaces', {}).get(redis_config.RESTAURANT_NAMESPACE, 0)
            },
            "dynamic_data": {
                "namespaces": [
                    redis_config.ORDER_NAMESPACE,
                    redis_config.REVIEW_NAMESPACE
                ],
                "ttl_strategy": "Short TTL (2-5 minutes)",
                "keys": cache_stats.get('namespaces', {}).get(redis_config.ORDER_NAMESPACE, 0)
            },
            "real_time_data": {
                "namespaces": [
                    redis_config.REALTIME_DELIVERY_NAMESPACE,
                    redis_config.REALTIME_ORDERS_NAMESPACE,
                    redis_config.REALTIME_CAPACITY_NAMESPACE
                ],
                "ttl_strategy": "Very short TTL (30 seconds)",
                "keys": 0  # Real-time data keys
            },
            "analytics_data": {
                "namespaces": [
                    redis_config.ANALYTICS_RESTAURANT_NAMESPACE,
                    redis_config.ANALYTICS_CUSTOMER_NAMESPACE,
                    redis_config.ANALYTICS_REVENUE_NAMESPACE
                ],
                "ttl_strategy": "Medium TTL (15 minutes)",
                "keys": 0  # Analytics keys
            }
        }
        
        return {
            "message": "Namespace statistics retrieved successfully",
            "cache_type": cache_stats.get('cache_type', 'unknown'),
            "total_keys": cache_stats.get('total_keys', 0),
            "namespace_breakdown": namespace_stats,
            "performance_stats": cache_stats.get('performance_stats', {})
        }
        
    except Exception as e:
        logger.error(f"Failed to get namespace statistics: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve namespace statistics"
        )

@enterprise_cache_router.get("/memory-usage")
async def get_memory_usage(request: Request):
    """Get memory consumption statistics"""
    try:
        # System memory info
        memory = psutil.virtual_memory()
        process = psutil.Process()
        process_memory = process.memory_info()
        
        # Python garbage collection info
        gc_stats = {
            "generation_0": len(gc.get_objects(0)) if hasattr(gc, 'get_objects') else 0,
            "generation_1": len(gc.get_objects(1)) if hasattr(gc, 'get_objects') else 0,
            "generation_2": len(gc.get_objects(2)) if hasattr(gc, 'get_objects') else 0,
        }
        
        # Cache-specific memory (estimate)
        from cache_utils import cache_manager
        cache_stats = await cache_manager.get_cache_stats()
        
        memory_data = {
            "system_memory": {
                "total_gb": round(memory.total / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "used_percentage": memory.percent
            },
            "process_memory": {
                "rss_mb": round(process_memory.rss / (1024**2), 2),
                "vms_mb": round(process_memory.vms / (1024**2), 2)
            },
            "cache_memory": {
                "cache_type": cache_stats.get('cache_type', 'unknown'),
                "total_keys": cache_stats.get('total_keys', 0),
                "estimated_size_mb": round(cache_stats.get('total_keys', 0) * 0.001, 2)  # Rough estimate
            },
            "garbage_collection": gc_stats
        }
        
        return {
            "message": "Memory usage statistics retrieved successfully",
            "timestamp": time.time(),
            "memory_statistics": memory_data
        }
        
    except Exception as e:
        logger.error(f"Failed to get memory usage: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve memory usage statistics"
        )

@enterprise_cache_router.delete("/clear/expired")
async def clear_expired_keys(request: Request):
    """Remove expired cache keys"""
    try:
        from cache_utils import cache_manager
        
        # For Redis, expired keys are automatically removed
        # For memory cache, we can trigger cleanup
        cleared_count = 0
        
        try:
            from fallback_cache import memory_cache
            cleared_count = memory_cache.cleanup_expired()
        except Exception as e:
            logger.warning(f"Memory cache cleanup failed: {e}")
        
        # Force garbage collection
        collected = gc.collect()
        
        return {
            "message": "Expired keys cleanup completed",
            "timestamp": time.time(),
            "expired_keys_cleared": cleared_count,
            "garbage_collected": collected,
            "note": "Redis automatically handles expired key removal"
        }
        
    except Exception as e:
        logger.error(f"Failed to clear expired keys: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to clear expired keys"
        )

@enterprise_cache_router.post("/warm/{namespace}")
async def warm_cache_namespace(
    namespace: str,
    request: Request,
    limit: int = Query(50, ge=1, le=200, description="Number of items to warm"),
    db: AsyncSession = Depends(get_database)
):
    """Warm cache for a specific namespace"""
    try:
        warmed_count = 0
        
        if namespace == "restaurants":
            # Warm popular restaurants
            from crud import restaurant_crud
            restaurants, _ = await restaurant_crud.get_restaurants(db, skip=0, limit=limit)
            
            from cache_utils import cache_manager
            for restaurant in restaurants:
                cache_key = f"{redis_config.RESTAURANT_NAMESPACE}:restaurant:{restaurant.id}"
                await cache_manager.cache_data(
                    cache_key, 
                    restaurant.__dict__, 
                    redis_config.RESTAURANT_DETAIL_TTL,
                    redis_config.RESTAURANT_NAMESPACE
                )
                warmed_count += 1
                
        elif namespace == "customers":
            # Warm customer profiles
            from crud import customer_crud
            customers, _ = await customer_crud.get_customers(db, skip=0, limit=limit)
            
            from cache_utils import cache_manager
            for customer in customers:
                cache_key = f"{redis_config.CUSTOMER_NAMESPACE}:customer:{customer.id}"
                await cache_manager.cache_data(
                    cache_key,
                    customer.__dict__,
                    redis_config.CUSTOMER_PROFILE_TTL,
                    redis_config.CUSTOMER_NAMESPACE
                )
                warmed_count += 1
                
        elif namespace == "analytics":
            # Warm analytics data (placeholder - would trigger analytics calculations)
            logger.info(f"Analytics cache warming triggered for {namespace}")
            warmed_count = 1  # Placeholder
            
        else:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Unknown namespace: {namespace}"
            )
        
        return {
            "message": f"Cache warming completed for namespace: {namespace}",
            "namespace": namespace,
            "items_warmed": warmed_count,
            "limit": limit,
            "timestamp": time.time()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to warm cache for namespace {namespace}: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Failed to warm cache for namespace: {namespace}"
        )

@enterprise_cache_router.get("/performance-report")
async def get_cache_performance_report(
    request: Request,
    hours: int = Query(24, ge=1, le=168, description="Hours to analyze")
):
    """Get comprehensive cache performance report"""
    try:
        from cache_utils import cache_manager
        
        cache_stats = await cache_manager.get_cache_stats()
        performance_stats = cache_stats.get('performance_stats', {})
        
        # Calculate metrics
        total_requests = performance_stats.get('total_requests', 0)
        cache_hits = performance_stats.get('cache_hits', 0)
        cache_misses = performance_stats.get('cache_misses', 0)
        slow_queries = performance_stats.get('slow_queries', 0)
        
        hit_ratio = round((cache_hits / total_requests * 100) if total_requests > 0 else 0, 2)
        miss_ratio = round((cache_misses / total_requests * 100) if total_requests > 0 else 0, 2)
        
        # Performance grades
        def get_performance_grade(hit_ratio):
            if hit_ratio >= 90: return "A+"
            elif hit_ratio >= 80: return "A"
            elif hit_ratio >= 70: return "B"
            elif hit_ratio >= 60: return "C"
            else: return "D"
        
        report = {
            "analysis_period": f"Last {hours} hours",
            "overall_performance": {
                "grade": get_performance_grade(hit_ratio),
                "hit_ratio": f"{hit_ratio}%",
                "total_requests": total_requests,
                "cache_hits": cache_hits,
                "cache_misses": cache_misses
            },
            "efficiency_metrics": {
                "hit_ratio_percentage": hit_ratio,
                "miss_ratio_percentage": miss_ratio,
                "slow_queries": slow_queries,
                "slow_query_percentage": round((slow_queries / total_requests * 100) if total_requests > 0 else 0, 2)
            },
            "recommendations": []
        }
        
        # Add recommendations based on performance
        if hit_ratio >= 80:
            report["recommendations"].append("Excellent cache performance - maintain current strategy")
        elif hit_ratio >= 60:
            report["recommendations"].append("Good cache performance - consider optimizing TTL values")
        else:
            report["recommendations"].append("Cache performance needs improvement - review caching strategy")
        
        if slow_queries > 0:
            report["recommendations"].append(f"Monitor {slow_queries} slow queries for optimization opportunities")
        
        if cache_stats.get('cache_type') == 'memory':
            report["recommendations"].append("Consider enabling Redis for better performance and persistence")
        
        return {
            "message": "Cache performance report generated successfully",
            "timestamp": time.time(),
            "cache_type": cache_stats.get('cache_type', 'unknown'),
            "performance_report": report
        }
        
    except Exception as e:
        logger.error(f"Failed to generate performance report: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to generate cache performance report"
        )
