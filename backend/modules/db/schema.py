# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: April 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // STANDARD IMPORT // ===============

import time
from typing import (
    Optional,
    List
)

# =============== // LIBRARY IMPORT // ===============

from pydantic import EmailStr
from sqlmodel import (
    SQLModel,
    Field,
    Relationship
)
from ulid import ULID

# =============== // MODULE IMPORT // ===============

import modules.datastructures as dc


# Base TimestampedModel that other models can inherit from
class TimestampedModel(SQLModel):
    id: str = Field(default_factory=lambda: str(ULID()), primary_key=True)
    created_at: float = Field(default_factory=time.time)
    last_updated_at: float = Field(default_factory=time.time, sa_column_kwargs={"onupdate": time.time})


# ===== USER MODELS =====

class UserBase(SQLModel):
    name: str = Field(max_length=30)
    surname: Optional[str] = Field(max_length=30, default=None)
    email: EmailStr = Field(unique=True)


class UserCreate(UserBase):
    id: str = Field(default_factory=lambda: str(ULID()), primary_key=True)
    pass


class User(TimestampedModel, UserBase, table=True):
    __tablename__ = "user_account"

    # Relationships
    portfolios: List["Portfolios"] = Relationship(back_populates="user")


class UserRead(UserBase):
    id: str
    created_at: float
    last_updated_at: float


class UserReadWithPortfolios(UserRead):
    portfolios: List["PortfolioRead"] = []


# ===== PORTFOLIO MODELS =====

class PortfolioBase(SQLModel):
    name: str = Field(max_length=30)


class PortfolioCreate(PortfolioBase):
    user_id: str = Field(foreign_key="user_account.id")


class Portfolios(TimestampedModel, PortfolioBase, table=True):
    __tablename__ = "portfolios"

    # Foreign Keys
    user_id: str = Field(foreign_key="user_account.id")

    # Relationships
    user: User = Relationship(back_populates="portfolios")
    holdings: List["Holdings"] = Relationship(back_populates="portfolio")
    history: List["History"] = Relationship(back_populates="portfolio")


class PortfolioRead(PortfolioBase):
    id: str
    user_id: str
    created_at: float
    last_updated_at: float


class PortfolioReadWithRelations(PortfolioRead):
    holdings: List["HoldingRead"] = []
    history: List["HistoryRead"] = []


# ===== HISTORY MODELS =====

class HistoryBase(SQLModel):
    event: str = Field(max_length=30)


class HistoryCreate(HistoryBase):
    portfolio_id: str


class History(TimestampedModel, HistoryBase, table=True):
    __tablename__ = "history"

    # Foreign Keys
    portfolio_id: str = Field(foreign_key="portfolios.id")

    # Relationships
    portfolio: Portfolios = Relationship(back_populates="history")


class HistoryRead(HistoryBase):
    id: str
    portfolio_id: str
    created_at: float
    last_updated_at: float


# ===== STOCK MODELS =====

class StockBase(dc.StockData):
    ticker: str = Field(unique=True)


class StockCreate(StockBase):
    pass


class Stocks(TimestampedModel, StockBase, table=True):
    __tablename__ = "stocks"

    # Relationships
    holdings: List["Holdings"] = Relationship(back_populates="stock")


class StockRead(StockBase):
    id: str
    created_at: float
    last_updated_at: float


class StockReadWithHoldings(StockRead):
    holdings: List["HoldingRead"] = []


# ===== HOLDING MODELS =====

class HoldingBase(SQLModel):
    purchased_at: float


class HoldingCreate(HoldingBase):
    portfolio_id: str
    stock_id: str


class Holdings(TimestampedModel, HoldingBase, table=True):
    __tablename__ = "holdings"

    # Foreign Keys
    portfolio_id: str = Field(foreign_key="portfolios.id")
    stock_id: str = Field(foreign_key="stocks.id")

    # Relationships
    portfolio: Portfolios = Relationship(back_populates="holdings")
    stock: Stocks = Relationship(back_populates="holdings")


class HoldingRead(HoldingBase):
    id: str
    portfolio_id: str
    stock_id: str
    created_at: float
    last_updated_at: float


# Resolve forward references
UserReadWithPortfolios.update_forward_refs()
PortfolioReadWithRelations.update_forward_refs()
StockReadWithHoldings.update_forward_refs()


def _create_db_and_tables(engine) -> None:
    SQLModel.metadata.create_all(engine)
