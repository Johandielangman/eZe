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
    Annotated,
    Dict
)

# =============== // LIBRARY IMPORT // ===============

import requests
from loguru import logger
from fastapi import (
    Depends,
    HTTPException,
    Header
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from kinde_sdk.kinde_api_client import KindeApiClient
from kinde_sdk import Configuration


# =============== // MODULE IMPORT // ===============

from modules.datastructures.api import TokenPayload
import constants as c


security = HTTPBearer()


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")


def get_public_key():
    jwks_url = f"{c.KINDE_ISSUER_URL}/.well-known/jwks"
    jwks = requests.get(
        url=jwks_url,
        timeout=30
    ).json()
    return jwks


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
