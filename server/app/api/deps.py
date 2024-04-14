from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.api import api_messages
from app.core import database_session
from app.core.security.jwt import verify_jwt_token
from app.models import Bank, BankCard, CardType, Payment, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/access-token")


@asynccontextmanager
async def get_session_celery() -> AsyncGenerator[AsyncSession, None]:
    async with database_session.get_async_session() as session:
        yield session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with database_session.get_async_session() as session:
        yield session


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> User:
    token_payload = verify_jwt_token(token)

    # Update options to load card types related to each bank, and now include payments with card type and bank name
    user = await session.scalar(
        select(User)
        .options(
            selectinload(User.bank_cards)
            .selectinload(BankCard.bank)
            .selectinload(Bank.types),  # Loading types of each bank
            selectinload(User.bank_cards).selectinload(BankCard.card_type),
            selectinload(User.city),
            selectinload(User.payments).selectinload(  # Eagerly load payments
                Payment.category
            ),  # Eagerly load categories related to payments
            selectinload(User.payments)
            .selectinload(
                Payment.card_type
            )  # Eagerly load card types related to payments
            .selectinload(CardType.bank),  # Eagerly load the bank of the card type
        )
        .where(User.user_id == token_payload.sub)
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=api_messages.JWT_ERROR_USER_REMOVED,
        )
    return user
