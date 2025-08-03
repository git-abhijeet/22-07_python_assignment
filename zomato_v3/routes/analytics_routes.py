"""
Enterprise Analytics Routes for Zomato V3
==========================================

Analytics endpoints with intelligent caching for business intelligence.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, desc, and_
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from http import HTTPStatus
import logging

from database import get_database
from models import Restaurant, MenuItem, Order, Customer, Review, OrderItem, OrderStatus
from enterprise_cache_decorators import analytics_cache, cache_aside
from redis_config import redis_config

logger = logging.getLogger(__name__)

# Analytics router
analytics_router = APIRouter(prefix="/analytics", tags=["enterprise-analytics"])

@analytics_router.get("/popular-items")
@analytics_cache(expire=redis_config.POPULAR_ITEMS_TTL)
async def get_popular_menu_items(
    request: Request,
    restaurant_id: Optional[int] = Query(None, description="Filter by restaurant"),
    limit: int = Query(10, ge=1, le=50, description="Number of items to return"),
    days: int = Query(30, ge=1, le=365, description="Days to look back"),
    db: AsyncSession = Depends(get_database)
):
    """Get most popular menu items based on order frequency"""
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Build query for popular items
        query = (
            db.query(
                MenuItem.id,
                MenuItem.name,
                MenuItem.price,
                Restaurant.name.label('restaurant_name'),
                func.count(OrderItem.id).label('order_count'),
                func.sum(OrderItem.quantity).label('total_quantity'),
                func.avg(Review.rating).label('avg_rating')
            )
            .join(OrderItem, MenuItem.id == OrderItem.menu_item_id)
            .join(Order, OrderItem.order_id == Order.id)
            .join(Restaurant, MenuItem.restaurant_id == Restaurant.id)
            .outerjoin(Review, Order.id == Review.order_id)
            .filter(Order.order_date >= start_date)
            .filter(Order.order_date <= end_date)
            .filter(Order.order_status != OrderStatus.CANCELLED)
        )
        
        if restaurant_id:
            query = query.filter(MenuItem.restaurant_id == restaurant_id)
        
        # Group and order by popularity
        popular_items = (
            query.group_by(MenuItem.id, MenuItem.name, MenuItem.price, Restaurant.name)
            .order_by(desc('total_quantity'))
            .limit(limit)
            .all()
        )
        
        result = [
            {
                "menu_item_id": item.id,
                "name": item.name,
                "price": float(item.price),
                "restaurant_name": item.restaurant_name,
                "order_count": item.order_count,
                "total_quantity": item.total_quantity,
                "avg_rating": round(float(item.avg_rating or 0), 2)
            }
            for item in popular_items
        ]
        
        return {
            "message": "Popular menu items retrieved successfully",
            "timeframe": f"Last {days} days",
            "restaurant_filter": restaurant_id,
            "total_items": len(result),
            "popular_items": result
        }
        
    except Exception as e:
        logger.error(f"Failed to get popular items: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve popular items"
        )

@analytics_router.get("/customer-insights/{customer_id}")
@analytics_cache(expire=redis_config.CUSTOMER_PREFERENCES_TTL)
async def get_customer_insights(
    customer_id: int,
    request: Request,
    days: int = Query(90, ge=1, le=365, description="Days to analyze"),
    db: AsyncSession = Depends(get_database)
):
    """Get detailed customer behavior insights"""
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Customer basic info
        customer = await db.get(Customer, customer_id)
        if not customer:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Customer {customer_id} not found"
            )
        
        # Order statistics
        orders_query = (
            db.query(Order)
            .filter(Order.customer_id == customer_id)
            .filter(Order.order_date >= start_date)
            .filter(Order.order_date <= end_date)
        )
        
        total_orders = orders_query.count()
        completed_orders = orders_query.filter(Order.order_status == OrderStatus.DELIVERED).count()
        total_spent = orders_query.with_entities(func.sum(Order.total_amount)).scalar() or 0
        
        # Favorite restaurants
        favorite_restaurants = (
            db.query(
                Restaurant.name,
                func.count(Order.id).label('order_count'),
                func.avg(Order.total_amount).label('avg_order_value')
            )
            .join(Order, Restaurant.id == Order.restaurant_id)
            .filter(Order.customer_id == customer_id)
            .filter(Order.order_date >= start_date)
            .group_by(Restaurant.id, Restaurant.name)
            .order_by(desc('order_count'))
            .limit(5)
            .all()
        )
        
        # Preferred cuisines
        preferred_cuisines = (
            db.query(
                Restaurant.cuisine_type,
                func.count(Order.id).label('order_count')
            )
            .join(Order, Restaurant.id == Order.restaurant_id)
            .filter(Order.customer_id == customer_id)
            .filter(Order.order_date >= start_date)
            .group_by(Restaurant.cuisine_type)
            .order_by(desc('order_count'))
            .limit(3)
            .all()
        )
        
        return {
            "message": "Customer insights retrieved successfully",
            "customer": {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email
            },
            "timeframe": f"Last {days} days",
            "order_statistics": {
                "total_orders": total_orders,
                "completed_orders": completed_orders,
                "completion_rate": round((completed_orders / total_orders * 100) if total_orders > 0 else 0, 2),
                "total_spent": float(total_spent),
                "average_order_value": round(float(total_spent / total_orders) if total_orders > 0 else 0, 2)
            },
            "favorite_restaurants": [
                {
                    "name": rest.name,
                    "order_count": rest.order_count,
                    "avg_order_value": round(float(rest.avg_order_value), 2)
                }
                for rest in favorite_restaurants
            ],
            "preferred_cuisines": [
                {
                    "cuisine_type": cuisine.cuisine_type,
                    "order_count": cuisine.order_count
                }
                for cuisine in preferred_cuisines
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get customer insights: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve customer insights"
        )

@analytics_router.get("/restaurant-performance/{restaurant_id}")
@analytics_cache(expire=redis_config.RESTAURANT_ANALYTICS_TTL)
async def get_restaurant_performance(
    restaurant_id: int,
    request: Request,
    days: int = Query(30, ge=1, le=365, description="Days to analyze"),
    db: AsyncSession = Depends(get_database)
):
    """Get restaurant performance analytics"""
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Restaurant basic info
        restaurant = await db.get(Restaurant, restaurant_id)
        if not restaurant:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Restaurant {restaurant_id} not found"
            )
        
        # Order analytics
        orders_query = (
            db.query(Order)
            .filter(Order.restaurant_id == restaurant_id)
            .filter(Order.order_date >= start_date)
            .filter(Order.order_date <= end_date)
        )
        
        total_orders = orders_query.count()
        completed_orders = orders_query.filter(Order.order_status == OrderStatus.DELIVERED).count()
        cancelled_orders = orders_query.filter(Order.order_status == OrderStatus.CANCELLED).count()
        total_revenue = orders_query.with_entities(func.sum(Order.total_amount)).scalar() or 0
        
        # Average rating
        avg_rating = (
            db.query(func.avg(Review.rating))
            .filter(Review.restaurant_id == restaurant_id)
            .filter(Review.created_at >= start_date)
            .scalar()
        ) or 0
        
        # Popular items for this restaurant
        popular_items = (
            db.query(
                MenuItem.name,
                func.sum(OrderItem.quantity).label('total_quantity')
            )
            .join(OrderItem, MenuItem.id == OrderItem.menu_item_id)
            .join(Order, OrderItem.order_id == Order.id)
            .filter(MenuItem.restaurant_id == restaurant_id)
            .filter(Order.order_date >= start_date)
            .filter(Order.order_status != OrderStatus.CANCELLED)
            .group_by(MenuItem.id, MenuItem.name)
            .order_by(desc('total_quantity'))
            .limit(5)
            .all()
        )
        
        return {
            "message": "Restaurant performance retrieved successfully",
            "restaurant": {
                "id": restaurant.id,
                "name": restaurant.name,
                "cuisine_type": restaurant.cuisine_type
            },
            "timeframe": f"Last {days} days",
            "performance_metrics": {
                "total_orders": total_orders,
                "completed_orders": completed_orders,
                "cancelled_orders": cancelled_orders,
                "completion_rate": round((completed_orders / total_orders * 100) if total_orders > 0 else 0, 2),
                "cancellation_rate": round((cancelled_orders / total_orders * 100) if total_orders > 0 else 0, 2),
                "total_revenue": float(total_revenue),
                "average_order_value": round(float(total_revenue / completed_orders) if completed_orders > 0 else 0, 2),
                "average_rating": round(float(avg_rating), 2)
            },
            "top_selling_items": [
                {
                    "name": item.name,
                    "quantity_sold": item.total_quantity
                }
                for item in popular_items
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get restaurant performance: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve restaurant performance"
        )

@analytics_router.get("/revenue-analytics")
@analytics_cache(expire=redis_config.REVENUE_ANALYTICS_TTL)
async def get_revenue_analytics(
    request: Request,
    days: int = Query(30, ge=1, le=365, description="Days to analyze"),
    restaurant_id: Optional[int] = Query(None, description="Filter by restaurant"),
    db: AsyncSession = Depends(get_database)
):
    """Get revenue analytics and trends"""
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Build base query
        revenue_query = (
            db.query(Order)
            .filter(Order.order_date >= start_date)
            .filter(Order.order_date <= end_date)
            .filter(Order.order_status == OrderStatus.DELIVERED)
        )
        
        if restaurant_id:
            revenue_query = revenue_query.filter(Order.restaurant_id == restaurant_id)
        
        # Total revenue
        total_revenue = revenue_query.with_entities(func.sum(Order.total_amount)).scalar() or 0
        total_orders = revenue_query.count()
        
        # Daily revenue trend (last 7 days)
        daily_revenue = (
            revenue_query.filter(Order.order_date >= (end_date - timedelta(days=7)))
            .with_entities(
                func.date(Order.order_date).label('order_date'),
                func.sum(Order.total_amount).label('daily_revenue'),
                func.count(Order.id).label('order_count')
            )
            .group_by(func.date(Order.order_date))
            .order_by('order_date')
            .all()
        )
        
        # Top revenue restaurants
        top_restaurants = (
            db.query(
                Restaurant.name,
                func.sum(Order.total_amount).label('restaurant_revenue'),
                func.count(Order.id).label('order_count')
            )
            .join(Order, Restaurant.id == Order.restaurant_id)
            .filter(Order.order_date >= start_date)
            .filter(Order.order_status == OrderStatus.DELIVERED)
            .group_by(Restaurant.id, Restaurant.name)
            .order_by(desc('restaurant_revenue'))
            .limit(10)
            .all()
        )
        
        return {
            "message": "Revenue analytics retrieved successfully",
            "timeframe": f"Last {days} days",
            "restaurant_filter": restaurant_id,
            "summary": {
                "total_revenue": float(total_revenue),
                "total_orders": total_orders,
                "average_order_value": round(float(total_revenue / total_orders) if total_orders > 0 else 0, 2)
            },
            "daily_trend": [
                {
                    "date": str(day.order_date),
                    "revenue": float(day.daily_revenue),
                    "orders": day.order_count
                }
                for day in daily_revenue
            ],
            "top_restaurants": [
                {
                    "name": rest.name,
                    "revenue": float(rest.restaurant_revenue),
                    "orders": rest.order_count,
                    "avg_order_value": round(float(rest.restaurant_revenue / rest.order_count), 2)
                }
                for rest in top_restaurants
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to get revenue analytics: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve revenue analytics"
        )

@analytics_router.get("/cache-performance")
async def get_cache_performance_analytics(request: Request):
    """Get cache performance metrics and analytics"""
    try:
        from cache_utils import cache_manager
        
        # Get cache statistics
        cache_stats = await cache_manager.get_cache_stats()
        
        # Calculate performance metrics
        total_requests = cache_stats.get('performance_stats', {}).get('total_requests', 0)
        cache_hits = cache_stats.get('performance_stats', {}).get('cache_hits', 0)
        cache_misses = cache_stats.get('performance_stats', {}).get('cache_misses', 0)
        
        hit_ratio = round((cache_hits / total_requests * 100) if total_requests > 0 else 0, 2)
        
        return {
            "message": "Cache performance analytics retrieved successfully",
            "cache_type": cache_stats.get('cache_type', 'unknown'),
            "performance_metrics": {
                "total_requests": total_requests,
                "cache_hits": cache_hits,
                "cache_misses": cache_misses,
                "hit_ratio_percentage": hit_ratio,
                "slow_queries": cache_stats.get('performance_stats', {}).get('slow_queries', 0)
            },
            "namespace_statistics": cache_stats.get('namespaces', {}),
            "recommendations": [
                "Excellent cache performance" if hit_ratio >= 80 else "Consider optimizing cache strategy",
                "Cache hit ratio is healthy" if hit_ratio >= 60 else "Cache hit ratio needs improvement",
                "Monitor slow queries" if cache_stats.get('performance_stats', {}).get('slow_queries', 0) > 0 else "No slow queries detected"
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to get cache performance analytics: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve cache performance analytics"
        )
