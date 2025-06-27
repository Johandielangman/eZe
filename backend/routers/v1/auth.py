# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: June 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // STANDARD IMPORT // ===============

from datetime import timedelta, datetime, timezone

# =============== // LIBRARY IMPORT // ===============


import jwt
from pydantic import BaseModel
from sqlmodel import (
    Session,
    select
)
from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
)


# =============== // MODULE IMPORT // ===============

import constants as c
import modules.db as db
from dependencies import get_session

# =============== // ROUTER // ===============

router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


# =============== // CRYPTOGRAPHY SETUP // ===============


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        c.JWT_SECRET_KEY,
        algorithm=c.JWT_ALGORITHM
    )
    return encoded_jwt


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
) -> Token:
    user: db.schema.User | None = session.exec(
        select(db.schema.User).where(db.schema.User.email == form_data.username)
    ).first()

    if not user or not c.BCRYPT_CONTEXT.verify(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "id": user.id
        },
        expires_delta=access_token_expires
    )
    return Token(
        access_token=access_token,
        token_type="bearer"
    )
