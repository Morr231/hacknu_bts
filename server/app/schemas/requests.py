from pydantic import BaseModel, EmailStr


class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class RefreshTokenRequest(BaseRequest):
    refresh_token: str


class UserUpdatePasswordRequest(BaseRequest):
    password: str


class UserCreateRequest(BaseRequest):
    email: EmailStr
    password: str
    full_name: str
    phone_number: str
    city_id: int


class CardCreateRequest(BaseRequest):
    card_number: str
    card_type_id: int
    bank_id: int


class SearchPartnerRequest(BaseRequest):
    name: str


class OfferCategoryRequest(BaseModel):
    category_id: int


class OfferPartnerRequest(BaseModel):
    partner_id: int


class CreatePaymentRequest(BaseModel):
    card_type_id: int
    cashback_percent: float
    category_id: int
