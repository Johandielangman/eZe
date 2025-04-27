# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: April 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // LIBRARY IMPORT // ===============

from fastapi import (
    APIRouter,
    Depends
)

# =============== // MODULE IMPORT // ===============

from dependencies import verify_token

# =============== // ROUTER // ===============

router: APIRouter = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}},
)

# =============== // ROUTES // ===============


@router.get("/")
async def root():
    return "Hello from root!"
