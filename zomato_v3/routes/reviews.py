from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus
from database import get_database
from schemas import ReviewCreate, ReviewResponse
from crud import review_crud, order_crud

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(
    review_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Get a specific review"""
    try:
        review = await review_crud.get_review(db, review_id)
        if not review:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Review with ID {review_id} not found"
            )
        return review
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve review"
        )

# Order-specific review routes  
order_review_router = APIRouter(prefix="/orders/{order_id}/review", tags=["order-reviews"])

@order_review_router.post("/", response_model=ReviewResponse, status_code=HTTPStatus.CREATED)
async def create_review(
    order_id: int,
    review_data: ReviewCreate,
    db: AsyncSession = Depends(get_database)
):
    """Create a review for a completed order"""
    try:
        # First check if order exists and is completed
        order = await order_crud.get_order(db, order_id)
        if not order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Order with ID {order_id} not found"
            )
        
        db_review = await review_crud.create_review(db, order_id, review_data)
        return db_review
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to create review"
        )

@order_review_router.get("/", response_model=ReviewResponse)
async def get_order_review(
    order_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Get the review for a specific order"""
    try:
        review = await review_crud.get_review_by_order(db, order_id)
        if not review:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"No review found for order {order_id}"
            )
        return review
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve order review"
        )
