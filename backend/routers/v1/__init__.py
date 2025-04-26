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

from fastapi import APIRouter

# =============== // MODULE IMPORT // ===============

from backend.routers.v1 import items


# =============== // DEFINE THE ROUTER // ===============

router: APIRouter = APIRouter(
    prefix="/v1",
    responses={404: {"description": "Not found"}},
)
router.include_router(items.router)
