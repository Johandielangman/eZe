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

from contextlib import asynccontextmanager
import argparse
import time

# =============== // LIBRARY IMPORT // ===============

from loguru import logger
import uvicorn
from fastapi import (
    FastAPI,
    Response,
    Request
)
from fastapi.responses import (
    HTMLResponse,
    FileResponse
)


# =============== // MODULE IMPORT // ===============

from dependencies import create_db_and_tables
import constants as c
import modules.utils as utils
from internal import meta

# ====> APIs
from routers.v1 import router as router_v1
from routers.auth import router as auth_router


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
app.include_router(auth_router)


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
    return HTMLResponse((c.META_DIR / "index.html").read_text())


@app.get("/ping")
async def ping() -> Response:
    """Test if the server is up and running"""
    return Response(
        content="pong!",
        media_type="text/plain"
    )


@app.get("/terms", include_in_schema=False)
async def terms() -> HTMLResponse:
    return HTMLResponse((c.META_DIR / "terms.html").read_text())


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(str(c.ASSETS_ROOT / "images" / "favicon.ico"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run FastAPI server with options.")

    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host address")
    parser.add_argument("--port", type=int, default=8000, help="Port number")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--proxy-headers", action="store_true", help="Enable proxy headers")
    parser.add_argument("--root-path", type=str, default="", help="Set root path for the application")

    parser.add_argument("--create-db", action="store_true", help="Create all tables")

    args = parser.parse_args()
    logger.info(f"args received: {args}")

    if args.create_db:
        logger.info("Creating Database")
        create_db_and_tables()

    uvicorn.run(
        "main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        proxy_headers=args.proxy_headers,
        root_path=args.root_path
    )
