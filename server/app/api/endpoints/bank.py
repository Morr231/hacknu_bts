from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.api import deps
from app.models import Bank, User
from app.schemas.responses import BankResponse, CardTypeResponse, ListBankResponse

router = APIRouter()


@router.get("/", response_model=ListBankResponse, description="Get banks")
async def get_banks(
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
) -> ListBankResponse:
    # Execute query with joined load for card types
    async with session:
        result = await session.execute(select(Bank).options(joinedload(Bank.types)))
        banks = result.scalars().unique().all()

    # Manual mapping from ORM models to Pydantic models
    bank_list = []
    for bank in banks:
        card_types = [CardTypeResponse(id=ct.id, name=ct.name) for ct in bank.types]
        bank_list.append(
            BankResponse(id=bank.id, name=bank.name, card_types=card_types)
        )

    # Return the response
    return ListBankResponse(banks=bank_list)
