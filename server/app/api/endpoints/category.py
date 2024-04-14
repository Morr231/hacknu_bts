from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api import deps
from app.models import Category
from app.schemas.responses import CategoryResponse

router = APIRouter()


@router.get("/", response_model=list[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_categories(session: AsyncSession = Depends(deps.get_session)):
    async with session:
        results = await session.execute(select(Category))
        categories = results.scalars().all()
        return categories
