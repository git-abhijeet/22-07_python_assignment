from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_, or_, func, desc
from models import Restaurant, MenuItem, Customer, Order, OrderItem, Review, OrderStatus
from schemas import (
    RestaurantCreate, RestaurantUpdate, MenuItemCreate, MenuItemUpdate,
    CustomerCreate, CustomerUpdate, OrderCreate, OrderStatusUpdate, ReviewCreate
)
from utils.business_logic import BusinessLogic
from typing import Optional, List, Dict, Any
from decimal import Decimal
from datetime import datetime, timedelta

class RestaurantCRUD:
    
    async def create_restaurant(self, db: AsyncSession, restaurant: RestaurantCreate) -> Restaurant:
        """Create a new restaurant"""
        existing = await self.get_restaurant_by_name(db, restaurant.name)
        if existing:
            raise ValueError(f"Restaurant with name '{restaurant.name}' already exists")
        
        db_restaurant = Restaurant(**restaurant.dict())
        db.add(db_restaurant)
        await db.commit()
        await db.refresh(db_restaurant)
        return db_restaurant
    
    async def get_restaurant(self, db: AsyncSession, restaurant_id: int) -> Optional[Restaurant]:
        """Get a restaurant by ID"""
        result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
        return result.scalar_one_or_none()
    
    async def get_restaurant_by_name(self, db: AsyncSession, name: str) -> Optional[Restaurant]:
        """Get a restaurant by name"""
        result = await db.execute(select(Restaurant).where(Restaurant.name == name))
        return result.scalar_one_or_none()
    
    async def get_restaurants(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 10,
        cuisine_type: Optional[str] = None,
        min_rating: Optional[float] = None,
        location: Optional[str] = None,
        active_only: bool = False
    ) -> tuple[List[Restaurant], int]:
        """Get restaurants with advanced filtering"""
        query = select(Restaurant)
        count_query = select(func.count(Restaurant.id))
        
        filters = []
        if cuisine_type:
            filters.append(Restaurant.cuisine_type == cuisine_type)
        if min_rating:
            filters.append(Restaurant.rating >= min_rating)
        if location:
            filters.append(Restaurant.address.ilike(f"%{location}%"))
        if active_only:
            filters.append(Restaurant.is_active == True)
        
        if filters:
            query = query.where(and_(*filters))
            count_query = count_query.where(and_(*filters))
        
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        query = query.order_by(desc(Restaurant.rating), Restaurant.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        restaurants = result.scalars().all()
        
        return restaurants, total
    
    async def update_restaurant(
        self, 
        db: AsyncSession, 
        restaurant_id: int, 
        restaurant_update: RestaurantUpdate
    ) -> Optional[Restaurant]:
        """Update a restaurant"""
        db_restaurant = await self.get_restaurant(db, restaurant_id)
        if not db_restaurant:
            return None
        
        if restaurant_update.name and restaurant_update.name != db_restaurant.name:
            existing = await self.get_restaurant_by_name(db, restaurant_update.name)
            if existing:
                raise ValueError(f"Restaurant with name '{restaurant_update.name}' already exists")
        
        update_data = restaurant_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_restaurant, field, value)
        
        await db.commit()
        await db.refresh(db_restaurant)
        return db_restaurant
    
    async def delete_restaurant(self, db: AsyncSession, restaurant_id: int) -> bool:
        """Delete a restaurant"""
        db_restaurant = await self.get_restaurant(db, restaurant_id)
        if not db_restaurant:
            return False
        
        await db.delete(db_restaurant)
        await db.commit()
        return True
    
    async def get_restaurant_analytics(self, db: AsyncSession, restaurant_id: int) -> Dict[str, Any]:
        """Get comprehensive restaurant analytics"""
        # Total orders
        total_orders_result = await db.execute(
            select(func.count(Order.id)).where(Order.restaurant_id == restaurant_id)
        )
        total_orders = total_orders_result.scalar() or 0
        
        # Total revenue
        revenue = await BusinessLogic.get_restaurant_revenue(db, restaurant_id)
        
        # Average order value
        avg_order_result = await db.execute(
            select(func.avg(Order.total_amount))
            .where(and_(Order.restaurant_id == restaurant_id, Order.order_status == OrderStatus.DELIVERED))
        )
        avg_order_value = avg_order_result.scalar() or 0
        
        # Average rating
        avg_rating = await BusinessLogic.calculate_restaurant_rating(db, restaurant_id)
        
        # Total reviews
        total_reviews_result = await db.execute(
            select(func.count(Review.id)).where(Review.restaurant_id == restaurant_id)
        )
        total_reviews = total_reviews_result.scalar() or 0
        
        # Popular items
        popular_items = await BusinessLogic.get_popular_menu_items(db, restaurant_id)
        
        # Orders by status
        orders_by_status = await BusinessLogic.get_order_analytics_by_status(db, restaurant_id)
        
        return {
            "total_orders": total_orders,
            "total_revenue": revenue,
            "average_order_value": Decimal(str(avg_order_value)) if avg_order_value else Decimal('0.00'),
            "average_rating": avg_rating,
            "total_reviews": total_reviews,
            "popular_items": popular_items,
            "orders_by_status": orders_by_status
        }

class MenuItemCRUD:
    
    async def create_menu_item(
        self, 
        db: AsyncSession, 
        restaurant_id: int, 
        menu_item: MenuItemCreate
    ) -> MenuItem:
        """Create a new menu item for a restaurant"""
        restaurant_crud = RestaurantCRUD()
        restaurant = await restaurant_crud.get_restaurant(db, restaurant_id)
        if not restaurant:
            raise ValueError(f"Restaurant with ID {restaurant_id} not found")
        
        db_menu_item = MenuItem(**menu_item.dict(), restaurant_id=restaurant_id)
        db.add(db_menu_item)
        await db.commit()
        await db.refresh(db_menu_item)
        return db_menu_item
    
    async def get_menu_item(self, db: AsyncSession, item_id: int) -> Optional[MenuItem]:
        """Get a menu item by ID"""
        result = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
        return result.scalar_one_or_none()
    
    async def get_menu_items_by_ids(self, db: AsyncSession, item_ids: List[int]) -> Dict[int, MenuItem]:
        """Get multiple menu items by IDs"""
        result = await db.execute(select(MenuItem).where(MenuItem.id.in_(item_ids)))
        items = result.scalars().all()
        return {item.id: item for item in items}

class CustomerCRUD:
    
    async def create_customer(self, db: AsyncSession, customer: CustomerCreate) -> Customer:
        """Create a new customer"""
        existing = await self.get_customer_by_email(db, customer.email)
        if existing:
            raise ValueError(f"Customer with email '{customer.email}' already exists")
        
        db_customer = Customer(**customer.dict())
        db.add(db_customer)
        await db.commit()
        await db.refresh(db_customer)
        return db_customer
    
    async def get_customer(self, db: AsyncSession, customer_id: int) -> Optional[Customer]:
        """Get a customer by ID"""
        result = await db.execute(select(Customer).where(Customer.id == customer_id))
        return result.scalar_one_or_none()
    
    async def get_customer_by_email(self, db: AsyncSession, email: str) -> Optional[Customer]:
        """Get a customer by email"""
        result = await db.execute(select(Customer).where(Customer.email == email))
        return result.scalar_one_or_none()
    
    async def get_customers(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 10,
        active_only: bool = False
    ) -> tuple[List[Customer], int]:
        """Get customers with pagination"""
        query = select(Customer)
        count_query = select(func.count(Customer.id))
        
        if active_only:
            query = query.where(Customer.is_active == True)
            count_query = count_query.where(Customer.is_active == True)
        
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        query = query.order_by(Customer.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        customers = result.scalars().all()
        
        return customers, total
    
    async def update_customer(
        self, 
        db: AsyncSession, 
        customer_id: int, 
        customer_update: CustomerUpdate
    ) -> Optional[Customer]:
        """Update a customer"""
        db_customer = await self.get_customer(db, customer_id)
        if not db_customer:
            return None
        
        if customer_update.email and customer_update.email != db_customer.email:
            existing = await self.get_customer_by_email(db, customer_update.email)
            if existing:
                raise ValueError(f"Customer with email '{customer_update.email}' already exists")
        
        update_data = customer_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_customer, field, value)
        
        await db.commit()
        await db.refresh(db_customer)
        return db_customer
    
    async def delete_customer(self, db: AsyncSession, customer_id: int) -> bool:
        """Delete a customer"""
        db_customer = await self.get_customer(db, customer_id)
        if not db_customer:
            return False
        
        await db.delete(db_customer)
        await db.commit()
        return True
    
    async def get_customer_analytics(self, db: AsyncSession, customer_id: int) -> Dict[str, Any]:
        """Get customer analytics"""
        # Total orders
        total_orders_result = await db.execute(
            select(func.count(Order.id)).where(Order.customer_id == customer_id)
        )
        total_orders = total_orders_result.scalar() or 0
        
        # Total spent
        total_spent = await BusinessLogic.get_customer_spending(db, customer_id)
        
        # Average order value
        avg_order_result = await db.execute(
            select(func.avg(Order.total_amount))
            .where(and_(Order.customer_id == customer_id, Order.order_status == OrderStatus.DELIVERED))
        )
        avg_order_value = avg_order_result.scalar() or 0
        
        # Favorite restaurants
        favorite_restaurants = await BusinessLogic.get_customer_favorite_restaurants(db, customer_id)
        
        # Order frequency (orders per month)
        monthly_orders_result = await db.execute(
            select(func.count(Order.id))
            .where(and_(
                Order.customer_id == customer_id,
                Order.order_date >= datetime.now() - timedelta(days=30)
            ))
        )
        monthly_orders = monthly_orders_result.scalar() or 0
        
        return {
            "total_orders": total_orders,
            "total_spent": total_spent,
            "average_order_value": Decimal(str(avg_order_value)) if avg_order_value else Decimal('0.00'),
            "favorite_restaurants": favorite_restaurants,
            "order_frequency": {"orders_last_30_days": monthly_orders}
        }

class OrderCRUD:
    
    async def create_order(
        self, 
        db: AsyncSession, 
        customer_id: int, 
        order_data: OrderCreate
    ) -> Order:
        """Create a new order"""
        # Validate customer exists
        customer_crud = CustomerCRUD()
        customer = await customer_crud.get_customer(db, customer_id)
        if not customer:
            raise ValueError(f"Customer with ID {customer_id} not found")
        
        # Validate restaurant exists
        restaurant_crud = RestaurantCRUD()
        restaurant = await restaurant_crud.get_restaurant(db, order_data.restaurant_id)
        if not restaurant:
            raise ValueError(f"Restaurant with ID {order_data.restaurant_id} not found")
        
        # Get menu items and validate
        menu_item_crud = MenuItemCRUD()
        menu_item_ids = [item.menu_item_id for item in order_data.items]
        menu_items = await menu_item_crud.get_menu_items_by_ids(db, menu_item_ids)
        
        # Validate menu items
        errors = []
        for item in order_data.items:
            menu_item = menu_items.get(item.menu_item_id)
            if not menu_item:
                errors.append(f"Menu item with ID {item.menu_item_id} not found")
            elif not menu_item.is_available:
                errors.append(f"Menu item '{menu_item.name}' is not available")
            elif menu_item.restaurant_id != order_data.restaurant_id:
                errors.append(f"Menu item '{menu_item.name}' does not belong to the selected restaurant")
        
        if errors:
            raise ValueError("; ".join(errors))
        
        # Calculate total amount
        total_amount = Decimal('0.00')
        for item in order_data.items:
            menu_item = menu_items[item.menu_item_id]
            total_amount += menu_item.price * item.quantity
        
        # Create order
        db_order = Order(
            customer_id=customer_id,
            restaurant_id=order_data.restaurant_id,
            total_amount=total_amount,
            delivery_address=order_data.delivery_address,
            special_instructions=order_data.special_instructions,
            order_status=OrderStatus.PLACED
        )
        db.add(db_order)
        await db.flush()  # Get the order ID
        
        # Create order items
        for item in order_data.items:
            menu_item = menu_items[item.menu_item_id]
            db_order_item = OrderItem(
                order_id=db_order.id,
                menu_item_id=item.menu_item_id,
                quantity=item.quantity,
                item_price=menu_item.price,
                special_requests=item.special_requests
            )
            db.add(db_order_item)
        
        await db.commit()
        await db.refresh(db_order)
        return db_order
    
    async def get_order(self, db: AsyncSession, order_id: int) -> Optional[Order]:
        """Get order with full details"""
        result = await db.execute(
            select(Order)
            .options(
                selectinload(Order.customer),
                selectinload(Order.restaurant),
                selectinload(Order.order_items).selectinload(OrderItem.menu_item)
            )
            .where(Order.id == order_id)
        )
        return result.scalar_one_or_none()
    
    async def update_order_status(
        self, 
        db: AsyncSession, 
        order_id: int, 
        status_update: OrderStatusUpdate
    ) -> Optional[Order]:
        """Update order status"""
        db_order = await self.get_order(db, order_id)
        if not db_order:
            return None
        
        # Validate status transition
        if not BusinessLogic.validate_order_status_transition(db_order.order_status, status_update.order_status):
            raise ValueError(f"Cannot change order status from {db_order.order_status.value} to {status_update.order_status.value}")
        
        db_order.order_status = status_update.order_status
        if status_update.delivery_time:
            db_order.delivery_time = status_update.delivery_time
        elif status_update.order_status == OrderStatus.DELIVERED:
            db_order.delivery_time = datetime.now()
        
        await db.commit()
        await db.refresh(db_order)
        return db_order
    
    async def get_customer_orders(
        self, 
        db: AsyncSession, 
        customer_id: int, 
        skip: int = 0, 
        limit: int = 10,
        status_filter: Optional[OrderStatus] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> tuple[List[Order], int]:
        """Get customer's order history"""
        query = select(Order).where(Order.customer_id == customer_id)
        count_query = select(func.count(Order.id)).where(Order.customer_id == customer_id)
        
        filters = []
        if status_filter:
            filters.append(Order.order_status == status_filter)
        if start_date:
            filters.append(Order.order_date >= start_date)
        if end_date:
            filters.append(Order.order_date <= end_date)
        
        if filters:
            query = query.where(and_(*filters))
            count_query = count_query.where(and_(*filters))
        
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        query = query.options(
            selectinload(Order.restaurant),
            selectinload(Order.order_items).selectinload(OrderItem.menu_item)
        ).order_by(desc(Order.order_date)).offset(skip).limit(limit)
        
        result = await db.execute(query)
        orders = result.scalars().all()
        
        return orders, total
    
    async def get_restaurant_orders(
        self, 
        db: AsyncSession, 
        restaurant_id: int, 
        skip: int = 0, 
        limit: int = 10,
        status_filter: Optional[OrderStatus] = None
    ) -> tuple[List[Order], int]:
        """Get restaurant's orders"""
        query = select(Order).where(Order.restaurant_id == restaurant_id)
        count_query = select(func.count(Order.id)).where(Order.restaurant_id == restaurant_id)
        
        if status_filter:
            query = query.where(Order.order_status == status_filter)
            count_query = count_query.where(Order.order_status == status_filter)
        
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        query = query.options(
            selectinload(Order.customer),
            selectinload(Order.order_items).selectinload(OrderItem.menu_item)
        ).order_by(desc(Order.order_date)).offset(skip).limit(limit)
        
        result = await db.execute(query)
        orders = result.scalars().all()
        
        return orders, total

class ReviewCRUD:
    
    async def create_review(
        self, 
        db: AsyncSession, 
        customer_id: int, 
        order_id: int, 
        review_data: ReviewCreate
    ) -> Review:
        """Create a review for a completed order"""
        # Get order and validate
        order_crud = OrderCRUD()
        order = await order_crud.get_order(db, order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} not found")
        
        if order.customer_id != customer_id:
            raise ValueError("You can only review your own orders")
        
        if not BusinessLogic.can_review_order(order.order_status):
            raise ValueError("You can only review completed orders")
        
        # Check if review already exists
        existing_review = await db.execute(
            select(Review).where(Review.order_id == order_id)
        )
        if existing_review.scalar_one_or_none():
            raise ValueError("Review already exists for this order")
        
        # Create review
        db_review = Review(
            customer_id=customer_id,
            restaurant_id=order.restaurant_id,
            order_id=order_id,
            **review_data.dict()
        )
        db.add(db_review)
        await db.commit()
        await db.refresh(db_review)
        
        # Update restaurant rating
        await self._update_restaurant_rating(db, order.restaurant_id)
        
        return db_review
    
    async def _update_restaurant_rating(self, db: AsyncSession, restaurant_id: int):
        """Update restaurant's average rating"""
        avg_rating = await BusinessLogic.calculate_restaurant_rating(db, restaurant_id)
        restaurant_crud = RestaurantCRUD()
        restaurant = await restaurant_crud.get_restaurant(db, restaurant_id)
        if restaurant:
            restaurant.rating = avg_rating
            await db.commit()
    
    async def get_restaurant_reviews(
        self, 
        db: AsyncSession, 
        restaurant_id: int, 
        skip: int = 0, 
        limit: int = 10
    ) -> tuple[List[Review], int]:
        """Get reviews for a restaurant"""
        query = select(Review).where(Review.restaurant_id == restaurant_id)
        count_query = select(func.count(Review.id)).where(Review.restaurant_id == restaurant_id)
        
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        query = query.options(
            selectinload(Review.customer),
            selectinload(Review.order)
        ).order_by(desc(Review.created_at)).offset(skip).limit(limit)
        
        result = await db.execute(query)
        reviews = result.scalars().all()
        
        return reviews, total
    
    async def get_customer_reviews(
        self, 
        db: AsyncSession, 
        customer_id: int, 
        skip: int = 0, 
        limit: int = 10
    ) -> tuple[List[Review], int]:
        """Get reviews by a customer"""
        query = select(Review).where(Review.customer_id == customer_id)
        count_query = select(func.count(Review.id)).where(Review.customer_id == customer_id)
        
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        query = query.options(
            selectinload(Review.restaurant),
            selectinload(Review.order)
        ).order_by(desc(Review.created_at)).offset(skip).limit(limit)
        
        result = await db.execute(query)
        reviews = result.scalars().all()
        
        return reviews, total

# Create global instances
restaurant_crud = RestaurantCRUD()
menu_item_crud = MenuItemCRUD()
customer_crud = CustomerCRUD()
order_crud = OrderCRUD()
review_crud = ReviewCRUD()
