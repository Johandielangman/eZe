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

import psycopg2  # noqa: F401
from loguru import logger
from fastapi import (
    Request,
)
from sqlmodel import Session, create_engine


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


def get_session(request: Request) -> Generator[Session, None, None]:
    if "get_session" in request.app.dependency_overrides:
        yield request.app.dependency_overrides["get_session"]()
    else:
        with Session(engine) as session:
            yield session
