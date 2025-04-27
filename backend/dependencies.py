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

import traceback
from typing import (
    TYPE_CHECKING,
    Generator,
    Dict
)

# =============== // LIBRARY IMPORT // ===============

from loguru import logger
from fastapi import (
    Depends,
    HTTPException
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from sqlmodel import Session, create_engine
from kinde_sdk.kinde_api_client import KindeApiClient
from kinde_sdk import Configuration


# =============== // MODULE IMPORT // ===============

from modules.datastructures.db import _create_db_and_tables
from modules.datastructures.api import TokenPayload
import constants as c

# =============== // SETUP // ===============

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine


security = HTTPBearer()
engine: 'Engine' = create_engine(c.DATABASE_URL)


# =============== // DATABASE DEPENDENCIES // ===============

def create_db_and_tables() -> None:
    _create_db_and_tables(engine=engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

# =============== // AUTHENTICATION DEPENDENCIES // ===============


def get_kinde_client() -> KindeApiClient:
    kinde_client = KindeApiClient(**{
        "configuration": Configuration(host=c.KINDE_ISSUER_URL),
        "domain": c.KINDE_ISSUER_URL,
        "client_id": c.KINDE_CLIENT_ID,
        "client_secret": c.KINDE_CLIENT_SECRET,
        "grant_type": c.KINDE_GRANT_TYPE,
        "callback_url": "http://localhost:8000/auth/kinde_callback",
        "code_verifier": "joasd923nsad09823noaguesr9u3qtewrnaio90eutgersgdsfg"
    })
    return kinde_client


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenPayload:
    logger.debug("Verifying user...")
    try:
        client: KindeApiClient = get_kinde_client()
        decoded_token: Dict = client._decode_token_if_needed_value(
            "access_token",
            {"access_token": credentials.credentials}
        )
        return TokenPayload(**decoded_token['access_token'] | {"token": credentials.credentials})
    except Exception as e:
        logger.error(f"Token Validation failed: {e}")
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=401, detail="Token Validation Failed")
