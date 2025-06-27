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
)

# =============== // LIBRARY IMPORT // ===============

from sqlalchemy.engine import Engine
from pydantic import EmailStr
from sqlmodel import (
    SQLModel,
    Field,
)
from ulid import ULID


# Base TimestampedModel that other models can inherit from
class TimestampedModel(SQLModel):
    id: str = Field(default_factory=lambda: str(ULID()), primary_key=True)
    created_at: float = Field(default_factory=time.time)
    last_updated_at: float = Field(default_factory=time.time, sa_column_kwargs={"onupdate": time.time})


# ===== USER MODELS =====

class UserBase(SQLModel):
    name: str = Field(max_length=150)
    surname: Optional[str] = Field(max_length=150, default=None)
    email: EmailStr = Field(unique=True, index=True)


class UserCreate(UserBase):
    password: str = Field(max_length=4_000, min_length=8)
    pass


class User(TimestampedModel, UserBase, table=True):
    __tablename__ = "user_account"
    __table_args__ = {"extend_existing": True}

    id: str = Field(default_factory=lambda: str(ULID()), primary_key=True)
    password_hash: str = Field(max_length=4_000, default="")
    is_verified: bool = Field(default=False)
    role: str = Field(default="user", max_length=50)


class UserRead(UserBase):
    id: str
    created_at: float
    last_updated_at: float


def create_all(
    engine: Engine,
    drop_before_create: bool = False
) -> None:
    if drop_before_create:
        SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
