from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import (
    CardType,
    Category,
    Payment,
    User,
)

# Assuming these are your ORM models
from app.schemas.requests import CreatePaymentRequest

router = APIRouter()


@router.post("/", description="Create payment", status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment_data: CreatePaymentRequest,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    # Check if the card_type and bank exist
    async with session:
        card_type = await session.get(CardType, payment_data.card_type_id)
        category = await session.get(Category, payment_data.category_id)
        if not card_type or not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category or Card Type not found",
            )

        # Create the card
        new_payment = Payment(
            cashback_percent=payment_data.cashback_percent,
            card_type_id=payment_data.card_type_id,
            category_id=payment_data.category_id,
            user_id=current_user.user_id,
        )

        session.add(new_payment)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating payment"
            )

        # Return the response
        return {"message": "Payment created successfully"}
