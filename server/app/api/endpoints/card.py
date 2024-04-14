from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import (
    Bank,
    BankCard,
    CardType,
    User,
)

# Assuming these are your ORM models
from app.schemas.requests import CardCreateRequest

router = APIRouter()


@router.post("/", description="Create card", status_code=status.HTTP_201_CREATED)
async def create_card(
    card_data: CardCreateRequest,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    # Check if the card_type and bank exist
    async with session:
        card_type = await session.get(CardType, card_data.card_type_id)
        bank = await session.get(Bank, card_data.bank_id)
        if not card_type or not bank:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bank or Card Type not found",
            )

        # Create the card
        new_card = BankCard(
            card_number=card_data.card_number,
            card_type_id=card_data.card_type_id,
            bank_id=card_data.bank_id,
            user_id=current_user.user_id,  # Assuming your user model has a user_id field
        )
        session.add(new_card)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating card"
            )

        # Return the response
        return {"message": "Card created successfully"}
