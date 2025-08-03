from decimal import Decimal
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_, desc
from datetime import datetime, timedelta
from models import Order, OrderItem, MenuItem, Restaurant, Customer, Review, OrderStatus

class BusinessLogic:
    
    @staticmethod
    def calculate_order_total(order_items: List[Dict[str, Any]], menu_items: Dict[int, MenuItem]) -> Decimal:
        """Calculate total amount for an order"""
        total = Decimal('0.00')
        for item in order_items:
            menu_item = menu_items.get(item['menu_item_id'])
            if menu_item:
                total += menu_item.price * item['quantity']
        return total
    
    @staticmethod
    def validate_order_status_transition(current_status: OrderStatus, new_status: OrderStatus) -> bool:
        """Validate if order status transition is allowed"""
        allowed_transitions = {
            OrderStatus.PLACED: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
            OrderStatus.CONFIRMED: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
            OrderStatus.PREPARING: [OrderStatus.OUT_FOR_DELIVERY, OrderStatus.CANCELLED],
            OrderStatus.OUT_FOR_DELIVERY: [OrderStatus.DELIVERED, OrderStatus.CANCELLED],
            OrderStatus.DELIVERED: [],  # No transitions from delivered
            OrderStatus.CANCELLED: []   # No transitions from cancelled
        }
        
        return new_status in allowed_transitions.get(current_status, [])
    
    @staticmethod
    def can_review_order(order_status: OrderStatus) -> bool:
        """Check if an order can be reviewed"""
        return order_status == OrderStatus.DELIVERED
    
    @staticmethod
    async def calculate_restaurant_rating(db: AsyncSession, restaurant_id: int) -> float:
        """Calculate average rating for a restaurant"""
        result = await db.execute(
            select(func.avg(Review.rating))
            .where(Review.restaurant_id == restaurant_id)
        )
        avg_rating = result.scalar()
        return float(avg_rating) if avg_rating else 0.0
    
    @staticmethod
    async def get_popular_menu_items(db: AsyncSession, restaurant_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Get most popular menu items for a restaurant"""
        result = await db.execute(
            select(
                MenuItem.id,
                MenuItem.name,
                func.sum(OrderItem.quantity).label('total_ordered'),
                func.count(OrderItem.id).label('order_count')
            )
            .join(OrderItem, MenuItem.id == OrderItem.menu_item_id)
            .join(Order, OrderItem.order_id == Order.id)
            .where(MenuItem.restaurant_id == restaurant_id)
            .group_by(MenuItem.id, MenuItem.name)
            .order_by(desc(func.sum(OrderItem.quantity)))
            .limit(limit)
        )
        
        return [
            {
                "menu_item_id": row.id,
                "name": row.name,
                "total_ordered": int(row.total_ordered),
                "order_count": int(row.order_count)
            }
            for row in result.fetchall()
        ]
    
    @staticmethod
    async def get_restaurant_revenue(db: AsyncSession, restaurant_id: int, days: int = 30) -> Decimal:
        """Calculate restaurant revenue for specified days"""
        start_date = datetime.now() - timedelta(days=days)
        
        result = await db.execute(
            select(func.sum(Order.total_amount))
            .where(
                and_(
                    Order.restaurant_id == restaurant_id,
                    Order.order_date >= start_date,
                    Order.order_status.in_([OrderStatus.DELIVERED])
                )
            )
        )
        
        revenue = result.scalar()
        return Decimal(str(revenue)) if revenue else Decimal('0.00')
    
    @staticmethod
    async def get_customer_spending(db: AsyncSession, customer_id: int) -> Decimal:
        """Calculate total customer spending"""
        result = await db.execute(
            select(func.sum(Order.total_amount))
            .where(
                and_(
                    Order.customer_id == customer_id,
                    Order.order_status == OrderStatus.DELIVERED
                )
            )
        )
        
        spending = result.scalar()
        return Decimal(str(spending)) if spending else Decimal('0.00')
    
    @staticmethod
    async def get_customer_favorite_restaurants(db: AsyncSession, customer_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Get customer's favorite restaurants based on order frequency"""
        result = await db.execute(
            select(
                Restaurant.id,
                Restaurant.name,
                func.count(Order.id).label('order_count'),
                func.sum(Order.total_amount).label('total_spent')
            )
            .join(Order, Restaurant.id == Order.restaurant_id)
            .where(Order.customer_id == customer_id)
            .group_by(Restaurant.id, Restaurant.name)
            .order_by(desc(func.count(Order.id)))
            .limit(limit)
        )
        
        return [
            {
                "restaurant_id": row.id,
                "name": row.name,
                "order_count": int(row.order_count),
                "total_spent": float(row.total_spent)
            }
            for row in result.fetchall()
        ]
    
    @staticmethod
    def validate_menu_items_availability(menu_items: Dict[int, MenuItem], order_items: List[Dict[str, Any]]) -> List[str]:
        """Validate if all menu items in order are available"""
        errors = []
        
        for item in order_items:
            menu_item = menu_items.get(item['menu_item_id'])
            if not menu_item:
                errors.append(f"Menu item with ID {item['menu_item_id']} not found")
            elif not menu_item.is_available:
                errors.append(f"Menu item '{menu_item.name}' is not available")
            elif menu_item.restaurant_id != order_items[0].get('restaurant_id'):
                errors.append(f"Menu item '{menu_item.name}' belongs to a different restaurant")
        
        return errors
    
    @staticmethod
    async def get_order_analytics_by_status(db: AsyncSession, restaurant_id: int) -> Dict[str, int]:
        """Get order count by status for a restaurant"""
        result = await db.execute(
            select(
                Order.order_status,
                func.count(Order.id).label('count')
            )
            .where(Order.restaurant_id == restaurant_id)
            .group_by(Order.order_status)
        )
        
        return {row.order_status.value: int(row.count) for row in result.fetchall()}
