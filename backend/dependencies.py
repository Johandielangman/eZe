from typing import Annotated
from fastapi import Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import requests
from backend.modules.datastructures.api import TokenPayload

from loguru import logger

security = HTTPBearer()

# Replace with your actual values
KIND_AUTH_DOMAIN = "https://happybread.kinde.com"
KIND_AUDIENCE = "https://happybread.kinde.com/api"
KIND_ISSUER = f"{KIND_AUTH_DOMAIN}"


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")


def get_public_key():
    jwks_url = f"{KIND_AUTH_DOMAIN}/.well-known/jwks"
    jwks = requests.get(
        url=jwks_url,
        timeout=30
    ).json()
    return jwks


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenPayload:
    logger.debug("Verifying user...")
    token = credentials.credentials
    try:
        jwks = get_public_key()
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header["kid"]
        key = next(k for k in jwks["keys"] if k["kid"] == kid)

        payload = jwt.decode(
            token,
            key=jwt.algorithms.RSAAlgorithm.from_jwk(key),
            issuer=KIND_ISSUER,
            audience="https://happybread.kinde.com/api",
            algorithms=["RS256"],
        )
        logger.info(payload)
        return TokenPayload(**payload)  # contains user info
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token Validation Failed: {str(e)}")
