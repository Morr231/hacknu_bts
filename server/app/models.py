# SQL Alchemy models declaration.
# https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models
# mapped_column syntax from SQLAlchemy 2.0.

# https://alembic.sqlalchemy.org/en/latest/tutorial.html
# Note, it is used by alembic migrations logic, see `alembic/env.py`

# Alembic shortcuts:
# # create migration
# alembic revision --autogenerate -m "migration_name"

# # apply all migrations
# alembic upgrade head


import uuid
from datetime import datetime

from sqlalchemy import (
    UUID,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class User(Base):
    __tablename__ = "user_account"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(256), nullable=False, unique=True, index=True)
    full_name = Column(String(256), nullable=False)
    phone_number = Column(String(16), nullable=False)
    city_id = Column(
        BigInteger, ForeignKey("city.id", ondelete="CASCADE"), nullable=False
    )
    hashed_password = Column(String(128), nullable=False)
    refresh_tokens = relationship("RefreshToken", back_populates="user")
    bank_cards = relationship("BankCard", back_populates="user")
    city = relationship("City", back_populates="users", lazy="joined")
    payments = relationship("Payment", back_populates="user")


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id = Column(BigInteger, primary_key=True)
    refresh_token = Column(String(512), nullable=False, unique=True, index=True)
    used = Column(Boolean, nullable=False, default=False)
    exp = Column(BigInteger, nullable=False)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("user_account.user_id", ondelete="CASCADE")
    )
    user = relationship("User", back_populates="refresh_tokens")


class Bank(Base):
    __tablename__ = "bank"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(256), nullable=False)
    cards = relationship("BankCard", back_populates="bank")
    types = relationship("CardType", back_populates="bank")


class BankCard(Base):
    __tablename__ = "bank_card"

    id = Column(BigInteger, primary_key=True)
    card_number = Column(String(16), nullable=False)
    bank_id = Column(
        BigInteger, ForeignKey("bank.id", ondelete="CASCADE"), nullable=False
    )
    card_type_id = Column(
        BigInteger, ForeignKey("card_type.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user_account.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    user = relationship("User", back_populates="bank_cards")
    bank = relationship("Bank", back_populates="cards")
    card_type = relationship("CardType", back_populates="cards")


class City(Base):
    __tablename__ = "city"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(256), nullable=False)
    users = relationship("User", back_populates="city")
    partners = relationship("Partner", back_populates="city")


class CardType(Base):
    __tablename__ = "card_type"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(256), nullable=False)
    bank_id = Column(
        BigInteger, ForeignKey("bank.id", ondelete="CASCADE"), nullable=False
    )
    default_cashback = Column(Float, nullable=False, default=0.0)
    bank = relationship("Bank", back_populates="types")
    cards = relationship("BankCard", back_populates="card_type")
    partners = relationship("Partner", back_populates="card_type")
    offers = relationship("Offer", back_populates="card_type")
    payments = relationship("Payment", back_populates="card_type")


class Category(Base):
    __tablename__ = "category"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(256), nullable=False)
    partners = relationship("Partner", back_populates="category")
    offers = relationship("Offer", back_populates="category")
    payments = relationship("Payment", back_populates="category")


class Partner(Base):
    __tablename__ = "partner"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(256), nullable=False)
    category_id = Column(
        BigInteger, ForeignKey("category.id", ondelete="CASCADE"), nullable=False
    )
    city_id = Column(
        BigInteger, ForeignKey("city.id", ondelete="CASCADE"), nullable=False
    )
    cashback_percent = Column(Float, nullable=False)
    card_type_id = Column(
        BigInteger, ForeignKey("card_type.id", ondelete="CASCADE"), nullable=False
    )
    address = Column(String(256), nullable=False)
    description = Column(Text)

    category = relationship("Category", back_populates="partners")
    city = relationship("City", back_populates="partners")
    card_type = relationship("CardType", back_populates="partners")


class Offer(Base):
    __tablename__ = "offer"

    id = Column(BigInteger, primary_key=True)
    category_id = Column(
        BigInteger, ForeignKey("category.id", ondelete="CASCADE"), nullable=False
    )
    card_type_id = Column(
        BigInteger, ForeignKey("card_type.id", ondelete="CASCADE"), nullable=False
    )
    cashback_percent = Column(Float, nullable=False)
    description = Column(String(512))

    category = relationship("Category", back_populates="offers")
    card_type = relationship("CardType", back_populates="offers")


class Payment(Base):
    __tablename__ = "payment"

    id = Column(BigInteger, primary_key=True)
    category_id = Column(
        BigInteger, ForeignKey("category.id", ondelete="CASCADE"), nullable=False
    )
    card_type_id = Column(
        BigInteger, ForeignKey("card_type.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user_account.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    cashback_percent = Column(Float, nullable=False)
    category = relationship("Category", back_populates="payments")
    card_type = relationship("CardType", back_populates="payments")
    user = relationship("User", back_populates="payments")
