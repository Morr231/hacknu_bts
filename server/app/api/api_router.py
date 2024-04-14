from fastapi import APIRouter

from app.api import api_messages
from app.api.endpoints import (
    auth,
    bank,
    card,
    category,
    city,
    offer,
    payment,
    search,
    users,
)

auth_router = APIRouter()
auth_router.include_router(auth.router, prefix="/auth", tags=["auth"])

api_router = APIRouter(
    responses={
        401: {
            "description": "No `Authorization` access token header, token is invalid or user removed",
            "content": {
                "application/json": {
                    "examples": {
                        "not authenticated": {
                            "summary": "No authorization token header",
                            "value": {"detail": "Not authenticated"},
                        },
                        "invalid token": {
                            "summary": "Token validation failed, decode failed, it may be expired or malformed",
                            "value": {"detail": "Token invalid: {detailed error msg}"},
                        },
                        "removed user": {
                            "summary": api_messages.JWT_ERROR_USER_REMOVED,
                            "value": {"detail": api_messages.JWT_ERROR_USER_REMOVED},
                        },
                    }
                }
            },
        },
    }
)
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(bank.router, prefix="/banks", tags=["banks"])
api_router.include_router(card.router, prefix="/cards", tags=["cards"])
api_router.include_router(city.router, prefix="/cities", tags=["cities"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(category.router, prefix="/categories", tags=["categories"])
api_router.include_router(offer.router, prefix="/offers", tags=["offers"])
api_router.include_router(payment.router, prefix="/payments", tags=["payments"])
