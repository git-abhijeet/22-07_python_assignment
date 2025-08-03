"""
Real-time Features Routes for Zomato V3
========================================

Real-time order tracking, restaurant availability, and live updates with short TTL caching.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, and_, or_
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from http import HTTPStatus
import logging
import random

from database import get_database
from models import Restaurant, Order, OrderStatus
from enterprise_cache_decorators import realtime_cache, cache_aside
from redis_config import redis_config

logger = logging.getLogger(__name__)

# Real-time router
realtime_router = APIRouter(prefix="/real-time", tags=["real-time-features"])

@realtime_router.get("/order-tracking/{order_id}")
@realtime_cache(expire=redis_config.LIVE_ORDERS_TTL)
async def track_order_live(
    order_id: int,
    request: Request,
    db: AsyncSession = Depends(get_database)
):
    """Live order tracking with 30-second cache"""
    try:
        # Get order details
        order = await db.get(Order, order_id)
        if not order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Order {order_id} not found"
            )
        
        # Simulate real-time tracking data
        tracking_data = {
            "order_id": order.id,
            "status": order.order_status.value,
            "customer_id": order.customer_id,
            "restaurant_id": order.restaurant_id,
            "order_date": order.order_date.isoformat(),
            "total_amount": float(order.total_amount),
            "delivery_address": order.delivery_address
        }
        
        # Add status-specific tracking info
        if order.order_status == OrderStatus.PLACED:
            tracking_data.update({
                "estimated_preparation_time": "15-20 minutes",
                "current_stage": "Order received by restaurant",
                "next_update_in": "5 minutes"
            })
        elif order.order_status == OrderStatus.PREPARING:
            tracking_data.update({
                "estimated_preparation_time": "10-15 minutes remaining",
                "current_stage": "Food being prepared",
                "next_update_in": "3 minutes"
            })
        elif order.order_status == OrderStatus.OUT_FOR_DELIVERY:
            tracking_data.update({
                "estimated_delivery_time": "15-25 minutes",
                "current_stage": "Out for delivery",
                "delivery_person": f"Driver #{random.randint(1001, 9999)}",
                "next_update_in": "2 minutes"
            })
        elif order.order_status == OrderStatus.DELIVERED:
            tracking_data.update({
                "delivered_at": order.delivery_time.isoformat() if order.delivery_time else None,
                "current_stage": "Order delivered successfully",
                "delivery_completed": True
            })
        
        return {
            "message": "Live order tracking retrieved successfully",
            "last_updated": datetime.now().isoformat(),
            "cache_ttl": f"{redis_config.LIVE_ORDERS_TTL} seconds",
            "tracking": tracking_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get live order tracking: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve live order tracking"
        )

@realtime_router.get("/restaurant-availability/{restaurant_id}")
@realtime_cache(expire=redis_config.RESTAURANT_AVAILABILITY_TTL)
async def get_restaurant_availability(
    restaurant_id: int,
    request: Request,
    db: AsyncSession = Depends(get_database)
):
    """Real-time restaurant availability and capacity"""
    try:
        # Get restaurant
        restaurant = await db.get(Restaurant, restaurant_id)
        if not restaurant:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Restaurant {restaurant_id} not found"
            )
        
        # Calculate current load (orders in last hour)
        one_hour_ago = datetime.now() - timedelta(hours=1)
        current_orders = (
            await db.execute(
                db.query(Order)
                .filter(Order.restaurant_id == restaurant_id)
                .filter(Order.order_date >= one_hour_ago)
                .filter(or_(
                    Order.order_status == OrderStatus.PLACED,
                    Order.order_status == OrderStatus.CONFIRMED,
                    Order.order_status == OrderStatus.PREPARING
                ))
            )
        ).scalars().all()
        
        current_load = len(current_orders)
        max_capacity = 20  # Simulated max capacity
        
        # Calculate availability metrics
        capacity_percentage = min(100, (current_load / max_capacity) * 100)
        is_accepting_orders = current_load < max_capacity and restaurant.is_active
        
        # Estimate wait times based on load
        if capacity_percentage < 50:
            estimated_prep_time = "15-20 minutes"
            wait_status = "low"
        elif capacity_percentage < 80:
            estimated_prep_time = "25-35 minutes"
            wait_status = "medium"
        else:
            estimated_prep_time = "45-60 minutes"
            wait_status = "high"
        
        availability_data = {
            "restaurant_id": restaurant.id,
            "restaurant_name": restaurant.name,
            "is_active": restaurant.is_active,
            "is_accepting_orders": is_accepting_orders,
            "current_load": current_load,
            "max_capacity": max_capacity,
            "capacity_percentage": round(capacity_percentage, 1),
            "wait_status": wait_status,
            "estimated_preparation_time": estimated_prep_time,
            "current_time": datetime.now().isoformat(),
            "opening_time": str(restaurant.opening_time),
            "closing_time": str(restaurant.closing_time)
        }
        
        return {
            "message": "Restaurant availability retrieved successfully",
            "last_updated": datetime.now().isoformat(),
            "cache_ttl": f"{redis_config.RESTAURANT_AVAILABILITY_TTL} seconds",
            "availability": availability_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get restaurant availability: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve restaurant availability"
        )

@realtime_router.get("/delivery-slots")
@realtime_cache(expire=redis_config.DELIVERY_SLOTS_TTL)
async def get_available_delivery_slots(
    request: Request,
    restaurant_id: Optional[int] = Query(None, description="Filter by restaurant"),
    hours_ahead: int = Query(4, ge=1, le=12, description="Hours to look ahead"),
    db: AsyncSession = Depends(get_database)
):
    """Get available delivery time slots with 30-second cache"""
    try:
        current_time = datetime.now()
        end_time = current_time + timedelta(hours=hours_ahead)
        
        # Generate delivery slots (every 30 minutes)
        slots = []
        slot_time = current_time + timedelta(minutes=30)  # Start 30 min from now
        
        while slot_time <= end_time:
            # Simulate slot availability (random for demo)
            slot_capacity = random.randint(5, 15)
            
            # Count orders for this slot (simulate)
            orders_in_slot = random.randint(0, slot_capacity)
            available = orders_in_slot < slot_capacity
            
            slot_data = {
                "delivery_time": slot_time.isoformat(),
                "formatted_time": slot_time.strftime("%I:%M %p"),
                "available": available,
                "remaining_capacity": max(0, slot_capacity - orders_in_slot),
                "total_capacity": slot_capacity
            }
            
            slots.append(slot_data)
            slot_time += timedelta(minutes=30)
        
        # Filter by restaurant availability if specified
        available_slots = slots
        if restaurant_id:
            restaurant = await db.get(Restaurant, restaurant_id)
            if restaurant and restaurant.is_active:
                # Filter slots based on restaurant hours
                opening_hour = restaurant.opening_time.hour
                closing_hour = restaurant.closing_time.hour
                
                available_slots = [
                    slot for slot in slots 
                    if opening_hour <= datetime.fromisoformat(slot["delivery_time"]).hour < closing_hour
                ]
        
        return {
            "message": "Available delivery slots retrieved successfully",
            "current_time": current_time.isoformat(),
            "hours_ahead": hours_ahead,
            "restaurant_filter": restaurant_id,
            "cache_ttl": f"{redis_config.DELIVERY_SLOTS_TTL} seconds",
            "total_slots": len(available_slots),
            "available_slots": available_slots[:10]  # Limit to first 10 slots
        }
        
    except Exception as e:
        logger.error(f"Failed to get delivery slots: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve delivery slots"
        )

@realtime_router.get("/live-orders")
@realtime_cache(expire=redis_config.LIVE_ORDERS_TTL)
async def get_live_orders(
    request: Request,
    restaurant_id: Optional[int] = Query(None, description="Filter by restaurant"),
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(20, ge=1, le=100, description="Number of orders to return"),
    db: AsyncSession = Depends(get_database)
):
    """Get live orders with real-time updates"""
    try:
        # Build query for active orders
        query = (
            db.query(Order)
            .filter(or_(
                Order.order_status == OrderStatus.PLACED,
                Order.order_status == OrderStatus.CONFIRMED,
                Order.order_status == OrderStatus.PREPARING,
                Order.order_status == OrderStatus.OUT_FOR_DELIVERY
            ))
            .order_by(Order.order_date.desc())
        )
        
        if restaurant_id:
            query = query.filter(Order.restaurant_id == restaurant_id)
        
        if status_filter:
            try:
                status_enum = OrderStatus(status_filter)
                query = query.filter(Order.order_status == status_enum)
            except ValueError:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Invalid status: {status_filter}"
                )
        
        orders = (await db.execute(query.limit(limit))).scalars().all()
        
        # Format live orders data
        live_orders = []
        for order in orders:
            order_data = {
                "order_id": order.id,
                "customer_id": order.customer_id,
                "restaurant_id": order.restaurant_id,
                "status": order.order_status.value,
                "total_amount": float(order.total_amount),
                "order_time": order.order_date.isoformat(),
                "minutes_ago": int((datetime.now() - order.order_date).total_seconds() / 60)
            }
            
            # Add estimated completion time
            if order.order_status == OrderStatus.PLACED:
                order_data["estimated_completion"] = "15-20 minutes"
            elif order.order_status == OrderStatus.PREPARING:
                order_data["estimated_completion"] = "10-15 minutes"
            elif order.order_status == OrderStatus.OUT_FOR_DELIVERY:
                order_data["estimated_completion"] = "5-15 minutes"
            
            live_orders.append(order_data)
        
        return {
            "message": "Live orders retrieved successfully",
            "last_updated": datetime.now().isoformat(),
            "filters": {
                "restaurant_id": restaurant_id,
                "status": status_filter
            },
            "cache_ttl": f"{redis_config.LIVE_ORDERS_TTL} seconds",
            "total_orders": len(live_orders),
            "orders": live_orders
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get live orders: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve live orders"
        )

@realtime_router.post("/update-order-status/{order_id}")
async def update_order_status_realtime(
    order_id: int,
    new_status: str,
    request: Request,
    db: AsyncSession = Depends(get_database)
):
    """Update order status and invalidate related caches"""
    try:
        # Get order
        order = await db.get(Order, order_id)
        if not order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Order {order_id} not found"
            )
        
        # Validate status
        try:
            status_enum = OrderStatus(new_status)
        except ValueError:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Invalid status: {new_status}"
            )
        
        # Update status
        old_status = order.order_status
        order.order_status = status_enum
        order.updated_at = datetime.now()
        
        if status_enum == OrderStatus.DELIVERED:
            order.delivery_time = datetime.now()
        
        await db.commit()
        
        # Invalidate related caches
        from cache_utils import cache_manager
        cache_keys_to_clear = [
            f"realtime:track_order_live:{order_id}",
            f"realtime:get_live_orders",
            f"analytics:customer_insights:{order.customer_id}",
            f"analytics:restaurant_performance:{order.restaurant_id}"
        ]
        
        for key in cache_keys_to_clear:
            try:
                await cache_manager.delete_cached_data(key)
            except Exception as e:
                logger.warning(f"Failed to clear cache key {key}: {e}")
        
        return {
            "message": "Order status updated successfully",
            "order_id": order.id,
            "old_status": old_status.value,
            "new_status": status_enum.value,
            "updated_at": order.updated_at.isoformat(),
            "caches_invalidated": len(cache_keys_to_clear)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update order status: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to update order status"
        )
