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

from modules.datastructures.db import (
    User,
    UserCreate,
    UserRead
)
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


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    session: Session = Depends(get_session)
):
    """Create a new user in the database
    You don't _have_ to give a user id! The server can create one FOR you (UUID).
    But it is highly recommended to use the Kinde User Id for this step!
    """
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/", response_model=List[UserRead])
def read_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Read users from the database
    TODO: Add permissions! Lol.
    """
    users: List[UserRead] = session.exec(select(User).offset(skip).limit(limit)).all()
    return users
