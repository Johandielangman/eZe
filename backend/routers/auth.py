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
    TYPE_CHECKING
)

# =============== // LIBRARY IMPORT // ===============

from loguru import logger
from fastapi import (
    Depends,
    Response,
    APIRouter,
    Request
)
from kinde_sdk import ApiException
from fastapi.responses import (
    RedirectResponse
)


# =============== // MODULE IMPORT // ===============

from modules.datastructures.api import TokenPayload, AccessTokenResponse
from dependencies import (
    verify_token,
    kinde_client
)

if TYPE_CHECKING:
    from kinde_sdk.kinde_api_client import KindeApiClient

# =============== // ROUTER // ===============

router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

# =============== // ROUTES // ===============


@router.get("/ping")
async def kinde(user: TokenPayload = Depends(verify_token)) -> Response:
    return Response(
        content="pong!",
        media_type="text/plain"
    )


@router.get('/login', include_in_schema=False)
async def login(kinde_client: 'KindeApiClient' = Depends(kinde_client)):
    return RedirectResponse(kinde_client.get_login_url())


@router.get('/kinde_callback', include_in_schema=False)
async def kinde_callback(
    code: str,
    request: Request,
    kinde_client: 'KindeApiClient' = Depends(kinde_client),
    scope: str = None,
    state: str = None
) -> AccessTokenResponse:
    logger.debug(f"Received callback with {code=}, {scope=}, {state=}")
    try:
        return AccessTokenResponse(**kinde_client.fetch_token_value(authorization_response=request.url))
    except ApiException as e:
        logger.error(f"Error getting token: {e}")
        return Response(
            content=f"Error getting token: {e}",
            media_type="text/plain"
        )
