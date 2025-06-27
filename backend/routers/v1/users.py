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


# =============== // LIBRARY IMPORT // ===============

from sqlmodel import (
    Session,
)
from fastapi import (
    APIRouter,
    Depends,
    status,
)

# =============== // MODULE IMPORT // ===============

import modules.db as db
import constants as c
from dependencies import (
    get_session,
    get_current_user
)

# =============== // ROUTER // ===============

router: APIRouter = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

# =============== // ROUTES // ===============


@router.post(
    "/",
    response_model=db.schema.UserRead,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user: db.schema.UserCreate,
    session: Session = Depends(get_session)
):
    db_user = db.schema.User.model_validate(user)

    db_user.password_hash = c.BCRYPT_CONTEXT.hash(user.password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/", response_model=db.schema.UserRead)
def read_user(
    user: db.schema.UserRead = Depends(get_current_user)
):
    return user
