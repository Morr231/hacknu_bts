from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api import deps
from app.models import Partner, User
from app.schemas.requests import SearchPartnerRequest
from app.schemas.responses import SearchPartnersResponse

router = APIRouter()


@router.post(
    "/partners",
    response_model=list[SearchPartnersResponse],
    status_code=status.HTTP_200_OK,
    description="Search for partners by name within the user's city.",
)
async def search_partners(
    search_partner_request: SearchPartnerRequest,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    async with session:
        stmt = (
            select(Partner)
            .options(selectinload(Partner.city))
            .join(Partner.city)
            .filter(Partner.city_id == current_user.city_id)
        )
        if search_partner_request.name:
            stmt = stmt.filter(Partner.name.ilike(f"%{search_partner_request.name}%"))

        result = await session.execute(stmt)
        partners = result.scalars().all()
        if not partners:
            raise HTTPException(status_code=404, detail="No partners found.")

        return partners
