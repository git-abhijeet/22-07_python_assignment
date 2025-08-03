from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from http import HTTPStatus
from database import get_database
from schemas import (
    OrderCreate, OrderResponse, OrderList, OrderStatusUpdate
)
from crud import order_crud, customer_crud

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Get order with full details"""
    try:
        order = await order_crud.get_order(db, order_id)
        if not order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Order with ID {order_id} not found"
            )
        return order
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve order"
        )

@router.put("/{order_id}/status")
async def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: AsyncSession = Depends(get_database)
):
    """Update order status"""
    try:
        updated_order = await order_crud.update_order_status(db, order_id, status_update)
        if not updated_order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Order with ID {order_id} not found"
            )
        return {
            "message": "Order status updated successfully",
            "order_id": order_id,
            "new_status": status_update.order_status.value,
            "order": updated_order
        }
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to update order status"
        )

@router.get("/", response_model=OrderList)
async def get_orders(
    skip: int = Query(0, ge=0, description="Number of orders to skip"),
    limit: int = Query(10, ge=1, le=50, description="Number of orders to return"),
    status: Optional[str] = Query(None, description="Filter by order status"),
    customer_id: Optional[int] = Query(None, description="Filter by customer ID"),
    restaurant_id: Optional[int] = Query(None, description="Filter by restaurant ID"),
    db: AsyncSession = Depends(get_database)
):
    """Get orders with filtering (admin endpoint)"""
    try:
        from sqlalchemy.future import select
        from sqlalchemy.orm import selectinload
        from sqlalchemy import and_, func, desc
        from models import Order, OrderStatus
        
        # Build query with filters
        query = select(Order).options(
            selectinload(Order.customer),
            selectinload(Order.restaurant),
            selectinload(Order.order_items).selectinload(Order.order_items)
        )
        count_query = select(func.count(Order.id))
        
        filters = []
        if status:
            try:
                status_filter = OrderStatus(status)
                filters.append(Order.order_status == status_filter)
            except ValueError:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Invalid order status: {status}"
                )
        if customer_id:
            filters.append(Order.customer_id == customer_id)
        if restaurant_id:
            filters.append(Order.restaurant_id == restaurant_id)
        
        if filters:
            query = query.where(and_(*filters))
            count_query = count_query.where(and_(*filters))
        
        # Get total count
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination and ordering
        query = query.order_by(desc(Order.order_date)).offset(skip).limit(limit)
        result = await db.execute(query)
        orders = result.scalars().all()
        
        return OrderList(
            orders=orders,
            total=total,
            skip=skip,
            limit=limit
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve orders"
        )

# Customer-specific order routes
customer_order_router = APIRouter(prefix="/customers/{customer_id}/orders", tags=["customer-orders"])

@customer_order_router.post("/", response_model=OrderResponse, status_code=HTTPStatus.CREATED)
async def place_order(
    customer_id: int,
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_database)
):
    """Place a new order for a customer"""
    try:
        db_order = await order_crud.create_order(db, customer_id, order_data)
        
        # Fetch the complete order with relationships
        complete_order = await order_crud.get_order(db, db_order.id)
        return complete_order
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to place order"
        )
