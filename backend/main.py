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
from contextlib import asynccontextmanager

# =============== // LIBRARY IMPORT // ===============

from loguru import logger
import httpx
from fastapi import (
    Depends,
    FastAPI,
    Response,
    Request
)

# =============== // MODULE IMPORT // ===============

from backend.modules.datastructures.api import TokenPayload
import backend.constants as c
import backend.modules.utils as utils
from backend.internal import admin, meta
from backend.dependencies import (
    get_query_token,
    get_token_header,
    verify_token
)

# ====> APIs
from backend.routers.v1 import router as router_v1


# =============== // SETUP // ===============

# ====> LOGGER
utils.setup_logger(logger)
logger.bind(name="root-logger")


# ====> LIFECYCLE
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug("Starting Server 🚀")
    yield
    logger.warning("Shutting down gracefully...")
    logger.warning("Cleanup complete. Server will now exit.")

# ====> APP
app = FastAPI(
    **meta.fast_api_metadata | {
        "lifespan": lifespan
    }
)

# =============== // ROUTER CONFIG // ===============

app.include_router(router_v1)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header), Depends(get_query_token)],
    responses={418: {"description": "I'm a teapot"}},
)


# =============== // MIDDLEWARE // ===============

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time: int = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.debug(
        f"[{request.client.host}] Request: "
        f"{request.method} {request.url} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.4f}s"
    )
    return response

# =============== // ADDITIONAL PATHS // ===============


@app.get("/")
async def root() -> Response:
    return Response(
        content="Hello from root!",
        media_type="text/plain"
    )


@app.get("/get_token")
async def get_token(
    client_id: str,
    client_secret: str,
    audience: str = f"{c.KINDE_ISSUER_URL}/api",
    grant_type: str = "client_credentials",
) -> Response:
    logger.debug(f"Requesting token from {client_id=}")

    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.post(
            url=f"{c.KINDE_ISSUER_URL}/oauth2/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "audience": audience,
                "grant_type": grant_type,
                "client_id": client_id,
                "client_secret": client_secret
            },
            timeout=30
        )

    if response.status_code != 200:
        logger.error(f"Error getting token: {response.status_code} - {response.text}")
        response.raise_for_status()
    return Response(
        content=response.text,
        media_type="application/json"
    )


@app.get("/ping")
async def ping() -> Response:
    """Test if the server is up and running"""
    return Response(
        content="pong!",
        media_type="text/plain"
    )


@app.get("/ping_auth")
async def kinde(user: TokenPayload = Depends(verify_token)) -> Response:
    return Response(
        content="pong!",
        media_type="text/plain"
    )
