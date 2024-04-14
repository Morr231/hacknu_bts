from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import City
from app.schemas.responses import CityResponse, ListCityResponse

router = APIRouter()


@router.get(
    "/",
    description="Get cities",
    response_model=ListCityResponse,
    status_code=status.HTTP_200_OK,
)
async def get_cities(session: AsyncSession = Depends(deps.get_session)):
    async with session:
        # Fetch all cities from the database
        stmt = select(City)
        result = await session.execute(stmt)
        cities = result.scalars().all()

        # Transform the cities into CityResponse objects
        city_responses = [CityResponse(id=city.id, name=city.name) for city in cities]

        return ListCityResponse(cities=city_responses)
