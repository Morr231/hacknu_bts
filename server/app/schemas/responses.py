from pydantic import BaseModel, ConfigDict, EmailStr


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccessTokenResponse(BaseResponse):
    token_type: str = "Bearer"
    access_token: str
    expires_at: int
    refresh_token: str
    refresh_token_expires_at: int


class CardTypeResponse(BaseResponse):
    id: int
    name: str


class BankResponse(BaseResponse):
    id: int
    name: str
    card_types: list[CardTypeResponse]


class ListBankResponse(BaseResponse):
    banks: list[BankResponse]


class BankCardResponse(BaseResponse):
    id: int
    card_number: str
    bank: BankResponse
    card_type: CardTypeResponse


class CityResponse(BaseResponse):
    id: int
    name: str


class ListCityResponse(BaseResponse):
    cities: list[CityResponse]


class SearchPartnersResponse(BaseResponse):
    id: int
    name: str
    address: str
    category_id: int
    cashback_percent: float
    description: str


class CategoryResponse(BaseResponse):
    id: int
    name: str


class OfferCategoryResponse(BaseResponse):
    card_type: CardTypeResponse
    bank: BankResponse
    category: CategoryResponse
    cashback_percent: float


class PaymentResponse(BaseResponse):
    id: int
    bank_name: str
    card_type: CardTypeResponse
    cashback_percent: float
    category: CategoryResponse
    created_at: str


class UserResponse(BaseResponse):
    user_id: str
    email: EmailStr
    full_name: str
    phone_number: str
    city: CityResponse | None = None
    bank_cards: list[BankCardResponse]
    payments: list[PaymentResponse]
