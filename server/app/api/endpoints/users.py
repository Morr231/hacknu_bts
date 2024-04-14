from fastapi import APIRouter, Depends, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core.security.password import get_password_hash
from app.models import User
from app.schemas.requests import UserUpdatePasswordRequest
from app.schemas.responses import (
    BankCardResponse,
    BankResponse,
    CardTypeResponse,
    CategoryResponse,
    CityResponse,
    PaymentResponse,
    UserResponse,
)

router = APIRouter()


@router.get("/me", response_model=UserResponse, description="Get current user")
async def read_current_user(
    current_user: User = Depends(deps.get_current_user),
) -> UserResponse:
    city_resp = CityResponse(
        id=current_user.city.id,
        name=current_user.city.name,
    )
    bank_cards_resp = [
        BankCardResponse(
            id=card.id,
            card_number=card.card_number,
            bank=BankResponse(
                id=card.bank.id,
                name=card.bank.name,
                card_types=[
                    CardTypeResponse(id=type.id, name=type.name)
                    for type in card.bank.types
                ],
            ),
            card_type=CardTypeResponse(id=card.card_type.id, name=card.card_type.name),
        )
        for card in current_user.bank_cards
    ]
    payment_resp = [
        PaymentResponse(
            id=payment.id,
            bank_name=payment.card_type.bank.name,
            card_type=CardTypeResponse(
                id=payment.card_type.id, name=payment.card_type.name
            ),
            cashback_percent=payment.cashback_percent,
            category=CategoryResponse(
                id=payment.category.id, name=payment.category.name
            ),
            created_at=str(payment.create_time.timestamp()),
        )
        for payment in current_user.payments
    ]
    return UserResponse(
        user_id=str(current_user.user_id),
        email=current_user.email,
        full_name=current_user.full_name,
        phone_number=current_user.phone_number,
        city=city_resp,
        bank_cards=bank_cards_resp,
        payments=payment_resp,
    )


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete current user",
)
async def delete_current_user(
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
) -> None:
    await session.execute(delete(User).where(User.user_id == current_user.user_id))
    await session.commit()


@router.post(
    "/reset-password",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Update current user password",
)
async def reset_current_user_password(
    user_update_password: UserUpdatePasswordRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
) -> None:
    current_user.hashed_password = get_password_hash(user_update_password.password)
    session.add(current_user)
    await session.commit()
