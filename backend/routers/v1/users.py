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
    List
)

# =============== // LIBRARY IMPORT // ===============

from sqlmodel import (
    Session,
    select
)
from fastapi import (
    APIRouter,
    Depends,
    status
)

# =============== // MODULE IMPORT // ===============

import modules.db as db
from dependencies import (
    verify_token,
    get_session
)

# =============== // ROUTER // ===============

router: APIRouter = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}},
)

# =============== // ROUTES // ===============


@router.post("/", response_model=db.schema.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user: db.schema.UserCreate,
    session: Session = Depends(get_session)
):
    """Create a new user in the database
    You don't _have_ to give a user id! The server can create one FOR you (UUID).
    But it is highly recommended to use the Kinde User Id for this step!
    """
    db_user = db.schema.User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/", response_model=List[db.schema.UserRead])
def read_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Read users from the database
    TODO: Add permissions! Lol.
    """
    users: List[db.schema.UserRead] = session.exec(select(db.schema.User).offset(skip).limit(limit)).all()
    return users
