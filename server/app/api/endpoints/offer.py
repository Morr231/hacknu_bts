from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.api import deps
from app.models import Bank, BankCard, CardType, Category, Offer, Partner, User
from app.schemas.requests import OfferCategoryRequest, OfferPartnerRequest
from app.schemas.responses import (
    BankResponse,
    CardTypeResponse,
    CategoryResponse,
    OfferCategoryResponse,
)

router = APIRouter()


@router.get(
    "/category",
    response_model=list[OfferCategoryResponse],
    status_code=status.HTTP_200_OK,
    description="Search for offers by category and card type available to the user, including bank details.",
)
async def search_offer_category(
    search_offer: OfferCategoryRequest = Depends(),
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    async with session:
        # Get card types available to the user
        user_card_types = await session.execute(
            select(BankCard.card_type_id).where(
                BankCard.user_id == current_user.user_id
            )
        )
        user_card_type_ids = {uct for uct in user_card_types.scalars().all()}

        # Fetch offers based on the user's card types
        results = await session.execute(
            select(Offer)
            .join(CardType, Offer.card_type_id == CardType.id)
            .join(Bank, CardType.bank_id == Bank.id)
            .filter(
                Offer.category_id == search_offer.category_id,
                Offer.card_type_id.in_(user_card_type_ids),
            )
            .options(
                selectinload(Offer.card_type).joinedload(CardType.bank),
                selectinload(Offer.category),
            )
        )

        offer_list = []
        for offer in results.scalars():
            bank_response = BankResponse(
                id=offer.card_type.bank.id,
                name=offer.card_type.bank.name,
                card_types=[
                    CardTypeResponse(id=ct.id, name=ct.name)
                    for ct in offer.card_type.bank.types
                ],
            )
            response = OfferCategoryResponse(
                card_type=CardTypeResponse(
                    id=offer.card_type.id, name=offer.card_type.name
                ),
                bank=bank_response,
                category=CategoryResponse(
                    id=offer.category.id, name=offer.category.name
                ),
                cashback_percent=offer.cashback_percent,
            )
            offer_list.append(response)

        # Retrieve category details for the user's card types
        category_detail = await session.execute(
            select(Category).where(Category.id == search_offer.category_id)
        )
        category = category_detail.scalar_one()

        # Retrieve additional card type information for the user and create more responses
        card_type_details = await session.execute(
            select(CardType)
            .where(CardType.id.in_(user_card_type_ids))
            .options(joinedload(CardType.bank))
        )
        for card_type in card_type_details.scalars():
            response = OfferCategoryResponse(
                card_type=CardTypeResponse(id=card_type.id, name=card_type.name),
                bank=BankResponse(
                    id=card_type.bank.id,
                    name=card_type.bank.name,
                    card_types=[
                        CardTypeResponse(id=ct.id, name=ct.name)
                        for ct in card_type.bank.types
                    ],
                ),
                category=CategoryResponse(id=category.id, name=category.name),
                cashback_percent=card_type.default_cashback,
            )
            if (response.cashback_percent > 0) and (response not in offer_list):
                offer_list.append(response)

        return offer_list


@router.get(
    "/partners",
    response_model=list[OfferCategoryResponse],
    status_code=status.HTTP_200_OK,
    description="Search for offers by the partner's category and card type available to the user, including bank details and special partner details.",
)
async def search_offer_by_partner(
    search_partner: OfferPartnerRequest = Depends(),
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    async with session:
        # Fetch partner details
        partner = await session.execute(
            select(Partner).where(Partner.id == search_partner.partner_id)
        )
        partner = partner.scalars().first()
        if not partner:
            raise HTTPException(status_code=404, detail="Partner not found")

        # Get card types available to the user
        user_card_types = await session.execute(
            select(BankCard.card_type_id).where(
                BankCard.user_id == current_user.user_id
            )
        )
        user_card_type_ids = {uct for uct in user_card_types.scalars().all()}

        # Fetch offers related to the partner's category_id and user's card types
        results = await session.execute(
            select(Offer)
            .join(CardType, Offer.card_type_id == CardType.id)
            .join(Bank, CardType.bank_id == Bank.id)
            .filter(
                Offer.category_id == partner.category_id,
                Offer.card_type_id.in_(user_card_type_ids),
            )
            .options(
                selectinload(Offer.card_type).joinedload(CardType.bank),
                selectinload(Offer.category),
            )
        )

        offer_list = []
        for offer in results.scalars():
            bank_response = BankResponse(
                id=offer.card_type.bank.id,
                name=offer.card_type.bank.name,
                card_types=[
                    CardTypeResponse(id=ct.id, name=ct.name)
                    for ct in offer.card_type.bank.types
                ],
            )
            response = OfferCategoryResponse(
                card_type=CardTypeResponse(
                    id=offer.card_type.id, name=offer.card_type.name
                ),
                bank=bank_response,
                category=CategoryResponse(
                    id=offer.category.id, name=offer.category.name
                ),
                cashback_percent=offer.cashback_percent,
            )
            offer_list.append(response)

        # Special entry for partner's exclusive offer, if the partner's card type is one of the user's card types
        if partner.card_type_id in user_card_type_ids:
            special_offer_response = OfferCategoryResponse(
                card_type=CardTypeResponse(
                    id=partner.card_type.id, name=partner.card_type.name
                ),
                bank=BankResponse(
                    id=partner.card_type.bank.id,
                    name=partner.card_type.bank.name,
                    card_types=[
                        CardTypeResponse(id=ct.id, name=ct.name)
                        for ct in partner.card_type.bank.types
                    ],
                ),
                category=CategoryResponse(
                    id=partner.category_id,
                    name=(
                        await session.execute(
                            select(Category.name).where(
                                Category.id == partner.category_id
                            )
                        )
                    )
                    .scalars()
                    .first(),
                ),
                cashback_percent=partner.cashback_percent,
            )
            offer_list.append(special_offer_response)

        # Retrieve category details for the user's card types
        category_detail = await session.execute(
            select(Category).where(Category.id == partner.category_id)
        )
        category = category_detail.scalar_one()

        # Retrieve additional card type information for the user and create more responses
        card_type_details = await session.execute(
            select(CardType)
            .where(CardType.id.in_(user_card_type_ids))
            .options(joinedload(CardType.bank))
        )
        for card_type in card_type_details.scalars():
            response = OfferCategoryResponse(
                card_type=CardTypeResponse(id=card_type.id, name=card_type.name),
                bank=BankResponse(
                    id=card_type.bank.id,
                    name=card_type.bank.name,
                    card_types=[
                        CardTypeResponse(id=ct.id, name=ct.name)
                        for ct in card_type.bank.types
                    ],
                ),
                category=CategoryResponse(id=category.id, name=category.name),
                cashback_percent=card_type.default_cashback,
            )
            if (response.cashback_percent > 0) and (response not in offer_list):
                offer_list.append(response)

        return offer_list
