# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: April 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

import time
from typing import (
    Optional,
    List
)
from sqlalchemy import (
    String,
    Float,
    ForeignKey
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)
from ulid import ULID


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    # ====> STANDARD VARIABLES
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(ULID()))
    created_at: Mapped[float] = mapped_column(default=time.time)
    last_updated_at: Mapped[float] = mapped_column(default=time.time, onupdate=time.time)

    # ====> COLUMNS
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)

    # ====> LOOKUPS
    portfolios: Mapped[List["Portfolios"]] = relationship(back_populates="user")


class Portfolios(Base):
    __tablename__ = "portfolios"

    # ====> STANDARD VARIABLES
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(ULID()))
    created_at: Mapped[float] = mapped_column(default=time.time)
    last_updated_at: Mapped[float] = mapped_column(default=time.time, onupdate=time.time)

    # ====> COLUMNS
    name: Mapped[str] = mapped_column(String(10))

    # ====> LOOKUPS
    user_id: Mapped[str] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="portfolios")

    holdings: Mapped[List["Holdings"]] = relationship(back_populates="portfolio")
    history: Mapped[List["History"]] = relationship(back_populates="portfolio")


class History(Base):
    __tablename__ = "history"

    # ====> STANDARD VARIABLES
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(ULID()))
    created_at: Mapped[float] = mapped_column(default=time.time)
    last_updated_at: Mapped[float] = mapped_column(default=time.time, onupdate=time.time)

    # ====> COLUMNS
    event: Mapped[str] = mapped_column(String(30))

    # ====> LOOKUPS
    portfolio_id: Mapped[str] = mapped_column(ForeignKey("portfolios.id"))
    portfolio: Mapped[Portfolios] = relationship(back_populates="history")


class Holdings(Base):
    __tablename__ = "holdings"

    # ====> STANDARD VARIABLES
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(ULID()))
    created_at: Mapped[float] = mapped_column(default=time.time)
    last_updated_at: Mapped[float] = mapped_column(default=time.time, onupdate=time.time)

    # ====> COLUMNS
    purchased_at: Mapped[float] = mapped_column(Float)

    # ====> LOOKUPS
    portfolio_id: Mapped[str] = mapped_column(ForeignKey("portfolios.id"))
    portfolio: Mapped[Portfolios] = relationship(back_populates="holdings")

    stock_id: Mapped[str] = mapped_column(ForeignKey("stocks.id"))
    stock: Mapped["Stocks"] = relationship(back_populates="holdings")


class Stocks(Base):
    __tablename__ = "stocks"

    # ====> STANDARD VARIABLES
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(ULID()))
    created_at: Mapped[float] = mapped_column(default=time.time)
    last_updated_at: Mapped[float] = mapped_column(default=time.time, onupdate=time.time)

    # ====> COLUMNS
    ticker: Mapped[str] = mapped_column(unique=True, nullable=False)

    # ====> LOOKUPS
    holdings: Mapped[List["Holdings"]] = relationship(back_populates="stock")
