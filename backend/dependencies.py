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

from typing import (
    TYPE_CHECKING,
    Generator,
)

# =============== // LIBRARY IMPORT // ===============

import jwt
import psycopg2  # noqa: F401
from loguru import logger
from sqlmodel import (
    Session,
    create_engine,
    select
)
from fastapi.security import OAuth2PasswordBearer
from fastapi import (
    Depends,
    status,
    HTTPException
)

# =============== // MODULE IMPORT // ===============

import modules.db as db
import constants as c

# =============== // SETUP // ===============

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine


engine: 'Engine' = create_engine(c.DB_URL)


# =============== // DATABASE DEPENDENCIES // ===============

def create_all_db_tables(drop_before_create: bool = False) -> None:
    logger.info("Creating all tables if they have not been created already")
    db.schema.create_all(
        engine=engine,
        drop_before_create=drop_before_create
    )


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl='v1/auth/token'
)


def get_current_user(
    token: str = Depends(oauth2_bearer),
    session: Session = Depends(get_session)
) -> db.schema.User:
    try:
        payload = jwt.decode(
            token,
            c.JWT_SECRET_KEY,
            algorithms=[c.JWT_ALGORITHM]
        )
        user_id: str = payload.get("id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        user: db.schema.User = session.exec(
            select(db.schema.User).where(db.schema.User.id == user_id)
        ).one()
        return user
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        ) from None
