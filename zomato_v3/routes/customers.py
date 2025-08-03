from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from http import HTTPStatus
from database import get_database
from schemas import (
    CustomerCreate, CustomerUpdate, CustomerResponse, CustomerList,
    CustomerWithOrders, OrderList, ReviewList, CustomerAnalytics
)
from crud import customer_crud, order_crud, review_crud

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/", response_model=CustomerResponse, status_code=HTTPStatus.CREATED)
async def create_customer(
    customer: CustomerCreate,
    db: AsyncSession = Depends(get_database)
):
    """Create a new customer"""
    try:
        db_customer = await customer_crud.create_customer(db, customer)
        return db_customer
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to create customer"
        )

@router.get("/", response_model=CustomerList)
async def get_customers(
    skip: int = Query(0, ge=0, description="Number of customers to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of customers to return"),
    active_only: bool = Query(False, description="Show only active customers"),
    db: AsyncSession = Depends(get_database)
):
    """Get customers with pagination"""
    try:
        customers, total = await customer_crud.get_customers(
            db, skip=skip, limit=limit, active_only=active_only
        )
        return CustomerList(
            customers=customers,
            total=total,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve customers"
        )

@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Get a specific customer by ID"""
    try:
        customer = await customer_crud.get_customer(db, customer_id)
        if not customer:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Customer with ID {customer_id} not found"
            )
        return customer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve customer"
        )

@router.get("/{customer_id}/orders", response_model=OrderList)
async def get_customer_orders(
    customer_id: int,
    skip: int = Query(0, ge=0, description="Number of orders to skip"),
    limit: int = Query(10, ge=1, le=50, description="Number of orders to return"),
    status: Optional[str] = Query(None, description="Filter by order status"),
    start_date: Optional[str] = Query(None, description="Start date filter (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date filter (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_database)
):
    """Get customer's order history"""
    try:
        # First check if customer exists
        customer = await customer_crud.get_customer(db, customer_id)
        if not customer:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Customer with ID {customer_id} not found"
            )
        
        # Parse filters
        from models import OrderStatus
        from datetime import datetime
        
        status_filter = None
        if status:
            try:
                status_filter = OrderStatus(status)
            except ValueError:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Invalid order status: {status}"
                )
        
        start_date_obj = None
        end_date_obj = None
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Invalid start date format. Use YYYY-MM-DD"
                )
        
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Invalid end date format. Use YYYY-MM-DD"
                )
        
        orders, total = await order_crud.get_customer_orders(
            db, customer_id, skip=skip, limit=limit, 
            status_filter=status_filter, start_date=start_date_obj, end_date=end_date_obj
        )
        
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
            detail="Failed to retrieve customer orders"
        )

@router.get("/{customer_id}/reviews", response_model=ReviewList)
async def get_customer_reviews(
    customer_id: int,
    skip: int = Query(0, ge=0, description="Number of reviews to skip"),
    limit: int = Query(10, ge=1, le=50, description="Number of reviews to return"),
    db: AsyncSession = Depends(get_database)
):
    """Get customer's reviews"""
    try:
        # First check if customer exists
        customer = await customer_crud.get_customer(db, customer_id)
        if not customer:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Customer with ID {customer_id} not found"
            )
        
        reviews, total = await review_crud.get_customer_reviews(db, customer_id, skip=skip, limit=limit)
        return ReviewList(
            reviews=reviews,
            total=total,
            skip=skip,
            limit=limit
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve customer reviews"
        )

@router.get("/{customer_id}/analytics", response_model=CustomerAnalytics)
async def get_customer_analytics(
    customer_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Get customer order analytics"""
    try:
        # First check if customer exists
        customer = await customer_crud.get_customer(db, customer_id)
        if not customer:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Customer with ID {customer_id} not found"
            )
        
        analytics = await customer_crud.get_customer_analytics(db, customer_id)
        return analytics
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve customer analytics"
        )

@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: AsyncSession = Depends(get_database)
):
    """Update a customer"""
    try:
        updated_customer = await customer_crud.update_customer(
            db, customer_id, customer_update
        )
        if not updated_customer:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Customer with ID {customer_id} not found"
            )
        return updated_customer
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
            detail="Failed to update customer"
        )

@router.delete("/{customer_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Delete a customer"""
    try:
        deleted = await customer_crud.delete_customer(db, customer_id)
        if not deleted:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Customer with ID {customer_id} not found"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to delete customer"
        )
