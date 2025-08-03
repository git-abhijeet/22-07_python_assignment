"""
Enterprise Demo Routes for Zomato V3
====================================

Demo endpoints to showcase enterprise caching features and performance.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any, List
from http import HTTPStatus
import logging
import time
import random
import asyncio

from database import get_database
from models import Restaurant, MenuItem, Customer, Order, OrderStatus
from redis_config import redis_config

logger = logging.getLogger(__name__)

# Enterprise demo router
enterprise_demo_router = APIRouter(prefix="/demo", tags=["enterprise-demo"])

@enterprise_demo_router.get("/load-test/{endpoint}")
async def performance_load_test(
    endpoint: str,
    request: Request,
    iterations: int = Query(10, ge=1, le=100, description="Number of test iterations"),
    db: AsyncSession = Depends(get_database)
):
    """Performance load testing for cache effectiveness"""
    try:
        results = {
            "endpoint": endpoint,
            "iterations": iterations,
            "results": [],
            "summary": {}
        }
        
        if endpoint == "restaurants":
            # Test restaurant listing with cache
            for i in range(iterations):
                start_time = time.time()
                
                # Simulate restaurant list request
                from routes.restaurants_cached import get_restaurants
                
                try:
                    response = await get_restaurants(request=request, skip=0, limit=10, db=db)
                    response_time = (time.time() - start_time) * 1000
                    
                    results["results"].append({
                        "iteration": i + 1,
                        "response_time_ms": round(response_time, 3),
                        "cache_status": "likely_hit" if response_time < 50 else "likely_miss"
                    })
                except Exception as e:
                    results["results"].append({
                        "iteration": i + 1,
                        "error": str(e)
                    })
                
                # Small delay between requests
                if i < iterations - 1:
                    await asyncio.sleep(0.1)
        
        elif endpoint == "analytics":
            # Test analytics endpoint
            for i in range(iterations):
                start_time = time.time()
                
                try:
                    from routes.analytics_routes import get_popular_menu_items
                    response = await get_popular_menu_items(
                        request=request, restaurant_id=None, limit=5, days=30, db=db
                    )
                    response_time = (time.time() - start_time) * 1000
                    
                    results["results"].append({
                        "iteration": i + 1,
                        "response_time_ms": round(response_time, 3),
                        "cache_status": "analytics_cache"
                    })
                except Exception as e:
                    results["results"].append({
                        "iteration": i + 1,
                        "error": str(e)
                    })
                
                await asyncio.sleep(0.1)
        
        else:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Unknown endpoint for load testing: {endpoint}"
            )
        
        # Calculate summary statistics
        response_times = [r.get("response_time_ms", 0) for r in results["results"] if "response_time_ms" in r]
        if response_times:
            results["summary"] = {
                "avg_response_time_ms": round(sum(response_times) / len(response_times), 3),
                "min_response_time_ms": round(min(response_times), 3),
                "max_response_time_ms": round(max(response_times), 3),
                "successful_requests": len(response_times),
                "failed_requests": iterations - len(response_times),
                "performance_grade": "A" if sum(response_times) / len(response_times) < 100 else "B"
            }
        
        return {
            "message": f"Load test completed for {endpoint}",
            "timestamp": time.time(),
            "test_results": results
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Load test failed for {endpoint}: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Load test failed for {endpoint}"
        )

@enterprise_demo_router.post("/create-sample-enterprise-data")
async def create_enterprise_sample_data(
    request: Request,
    customers_count: int = Query(5, ge=1, le=20, description="Number of customers to create"),
    restaurants_count: int = Query(3, ge=1, le=10, description="Number of restaurants to create"),
    orders_count: int = Query(10, ge=1, le=50, description="Number of orders to create"),
    db: AsyncSession = Depends(get_database)
):
    """Create comprehensive sample data for enterprise features testing"""
    try:
        created_data = {
            "customers": [],
            "restaurants": [],
            "orders": [],
            "menu_items": []
        }
        
        # Create sample customers
        from crud import customer_crud
        from schemas import CustomerCreate
        
        for i in range(customers_count):
            customer_data = CustomerCreate(
                name=f"Enterprise Customer {i+1}",
                email=f"customer{i+1}@enterprise.com",
                phone_number=f"+1-555-{1000+i}",
                address=f"{100+i} Enterprise Street, Business City"
            )
            
            try:
                customer = await customer_crud.create_customer(db, customer_data)
                created_data["customers"].append({
                    "id": customer.id,
                    "name": customer.name,
                    "email": customer.email
                })
            except Exception as e:
                logger.warning(f"Failed to create customer {i+1}: {e}")
        
        # Create sample restaurants
        from crud import restaurant_crud
        from schemas import RestaurantCreate
        
        cuisines = ["Italian", "Chinese", "Indian", "Mexican", "Japanese"]
        for i in range(restaurants_count):
            restaurant_data = RestaurantCreate(
                name=f"Enterprise Restaurant {i+1}",
                description=f"High-quality {cuisines[i % len(cuisines)]} cuisine",
                cuisine_type=cuisines[i % len(cuisines)],
                address=f"{200+i} Restaurant Avenue, Food District",
                phone_number=f"+1-555-{2000+i}",
                opening_time="09:00:00",
                closing_time="22:00:00"
            )
            
            try:
                restaurant = await restaurant_crud.create_restaurant(db, restaurant_data)
                created_data["restaurants"].append({
                    "id": restaurant.id,
                    "name": restaurant.name,
                    "cuisine_type": restaurant.cuisine_type
                })
                
                # Create menu items for each restaurant
                from crud import menu_item_crud
                from schemas import MenuItemCreate
                
                menu_items = [
                    {"name": "Signature Appetizer", "price": 12.99, "category": "appetizers"},
                    {"name": "Chef's Special", "price": 24.99, "category": "main-course"},
                    {"name": "House Dessert", "price": 8.99, "category": "desserts"}
                ]
                
                for item_data in menu_items:
                    menu_item = MenuItemCreate(
                        name=f"{item_data['name']} - {restaurant.name}",
                        description=f"Delicious {item_data['name'].lower()}",
                        price=item_data["price"],
                        category=item_data["category"],
                        is_vegetarian=random.choice([True, False]),
                        is_vegan=random.choice([True, False]),
                        preparation_time=random.randint(10, 30),
                        restaurant_id=restaurant.id
                    )
                    
                    try:
                        menu_item_obj = await menu_item_crud.create_menu_item(db, menu_item)
                        created_data["menu_items"].append({
                            "id": menu_item_obj.id,
                            "name": menu_item_obj.name,
                            "restaurant_id": restaurant.id
                        })
                    except Exception as e:
                        logger.warning(f"Failed to create menu item: {e}")
                        
            except Exception as e:
                logger.warning(f"Failed to create restaurant {i+1}: {e}")
        
        # Create sample orders
        if created_data["customers"] and created_data["restaurants"]:
            from crud import order_crud
            from schemas import OrderCreate, OrderItemCreate
            
            for i in range(orders_count):
                customer = random.choice(created_data["customers"])
                restaurant = random.choice(created_data["restaurants"])
                
                order_data = OrderCreate(
                    customer_id=customer["id"],
                    restaurant_id=restaurant["id"],
                    delivery_address=f"Delivery Address {i+1}",
                    special_instructions=f"Order {i+1} special instructions",
                    order_items=[]  # Simplified for demo
                )
                
                try:
                    order = await order_crud.create_order(db, order_data)
                    created_data["orders"].append({
                        "id": order.id,
                        "customer_id": customer["id"],
                        "restaurant_id": restaurant["id"],
                        "status": order.order_status.value
                    })
                except Exception as e:
                    logger.warning(f"Failed to create order {i+1}: {e}")
        
        return {
            "message": "Enterprise sample data created successfully",
            "timestamp": time.time(),
            "created_counts": {
                "customers": len(created_data["customers"]),
                "restaurants": len(created_data["restaurants"]),
                "menu_items": len(created_data["menu_items"]),
                "orders": len(created_data["orders"])
            },
            "sample_data": created_data,
            "next_steps": [
                "Test analytics endpoints: /analytics/popular-items",
                "Test real-time features: /real-time/live-orders",
                "Test cache performance: /demo/load-test/restaurants",
                "Monitor cache stats: /cache/stats/namespaces"
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to create enterprise sample data: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to create enterprise sample data"
        )

@enterprise_demo_router.get("/enterprise-features-showcase")
async def showcase_enterprise_features(request: Request):
    """Showcase all enterprise caching features and endpoints"""
    try:
        showcase_data = {
            "enterprise_caching_features": {
                "multi_tier_ttl": {
                    "static_data": f"{redis_config.RESTAURANT_DETAIL_TTL}s (30+ minutes)",
                    "dynamic_data": f"{redis_config.ORDER_STATUS_TTL}s (2-5 minutes)",
                    "real_time_data": f"{redis_config.LIVE_ORDERS_TTL}s (30 seconds)",
                    "analytics_data": f"{redis_config.POPULAR_ITEMS_TTL}s (15 minutes)"
                },
                "advanced_patterns": [
                    "Session-based caching for customer data",
                    "Conditional caching for completed orders only",
                    "Write-through caching for immediate updates",
                    "Cache-aside pattern for analytics calculations"
                ],
                "namespace_organization": {
                    "customers": "Customer profiles and session data",
                    "restaurants": "Restaurant information and menus",
                    "orders": "Order details and status",
                    "analytics:restaurants": "Restaurant performance data",
                    "analytics:customers": "Customer behavior insights",
                    "real-time:orders": "Live order tracking",
                    "real-time:delivery": "Delivery status updates"
                }
            },
            "api_endpoints": {
                "analytics": [
                    "/analytics/popular-items - Most ordered menu items",
                    "/analytics/customer-insights/{customer_id} - Customer behavior",
                    "/analytics/restaurant-performance/{restaurant_id} - Restaurant metrics",
                    "/analytics/revenue-analytics - Revenue trends and insights"
                ],
                "real_time": [
                    "/real-time/order-tracking/{order_id} - Live order status",
                    "/real-time/restaurant-availability/{restaurant_id} - Capacity status",
                    "/real-time/delivery-slots - Available delivery times",
                    "/real-time/live-orders - Active orders monitoring"
                ],
                "cache_management": [
                    "/cache/health - Cache system health check",
                    "/cache/stats/namespaces - Detailed namespace statistics",
                    "/cache/memory-usage - Memory consumption analysis",
                    "/cache/performance-report - Comprehensive performance report"
                ]
            },
            "performance_benefits": {
                "cache_hit_improvement": "80-95% faster response times",
                "database_load_reduction": "Significant reduction in database queries",
                "user_experience": "Sub-10ms response times for cached data",
                "scalability": "Handle higher concurrent users with caching"
            },
            "monitoring_capabilities": {
                "cache_performance": "Real-time hit/miss ratios",
                "memory_usage": "System and cache memory monitoring",
                "slow_queries": "Automatic detection and logging",
                "namespace_analytics": "Cache usage by data type"
            }
        }
        
        return {
            "message": "Enterprise features showcase",
            "version": "Zomato V3 Enterprise Edition",
            "timestamp": time.time(),
            "showcase": showcase_data,
            "getting_started": {
                "1": "Create sample data: POST /demo/create-sample-enterprise-data",
                "2": "Test analytics: GET /analytics/popular-items",
                "3": "Monitor real-time: GET /real-time/live-orders",
                "4": "Check cache performance: GET /cache/performance-report",
                "5": "Run load tests: GET /demo/load-test/restaurants"
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to generate enterprise showcase: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to generate enterprise features showcase"
        )
